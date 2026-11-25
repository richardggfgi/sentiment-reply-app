"""แกนของระบบ: วิเคราะห์รีวิว 1 อัน -> sentiment, aspects, urgency, ร่างคำตอบ
เรียก AI ได้ 2 แบบ:
- Claude (Anthropic): /v1/messages ยืนยันตัวตนด้วย Authorization: Bearer (ถ้าไม่ผ่านจะลอง x-api-key ให้อัตโนมัติ)
- OpenAI-compatible: /chat/completions ยืนยันตัวตนด้วย Bearer (Gemini, OpenAI หรือ gateway อื่น)"""
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import pandas as pd
import requests

from shop_config import DEFAULT_SHOP, TONE_PRESETS, RULES, EXAMPLES, apply_particle

DEFAULT_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
DEFAULT_MODEL = "gemini-2.5-flash"
ANTHROPIC_ENDPOINT = "https://api.anthropic.com"
ANTHROPIC_MODEL = "claude-haiku-5-5"       # ค่าเริ่มต้น: เร็วและประหยัด
ANTHROPIC_VERSION = "2026-10-21"      # เวอร์ชันล่าสุดตามเอกสาร Claude API
LEGACY_VERSION = "2023-06-01"         # สำรอง เผื่อ proxy ยังไม่รองรับเวอร์ชันใหม่
AUTH_MODES = ("bearer", "x-api-key")  # Bearer = วิธีหลัก, x-api-key = วิธีเดิมที่ยังรองรับ
_working = {}                         # host -> (auth, version) ที่ใช้ได้แล้ว จะได้ไม่ต้องลองใหม่ทุกครั้ง
PROVIDERS = {"anthropic": "Claude (Anthropic)", "openai": "OpenAI-compatible"}
PROVIDER_DEFAULTS = {"anthropic": (ANTHROPIC_ENDPOINT, ANTHROPIC_MODEL), "openai": (DEFAULT_ENDPOINT, DEFAULT_MODEL)}
MAX_TOKENS = 1024
ASPECTS = ["quality", "shipping", "packaging", "price", "service", "other"]
URGENCY_ORDER = {"high": 0, "medium": 1, "low": 2}
TIMEOUT = 45          # วินาทีต่อคำขอ
RETRIES = 2           # ลองใหม่เมื่อโดน rate limit / server error / timeout


# ---------------- endpoint helpers ----------------
def _base(url: str) -> str:
    url = (url or "").strip().rstrip("/")
    if url and not re.match(r"^https?://", url):
        url = "https://" + url
    return url


def strip_api_path(url: str) -> str:
    """เหลือแค่ฐาน URL เช่น https://claude.furi.moe/v1/chat/completions -> https://claude.furi.moe"""
    url = _base(url)
    changed = True
    while changed:
        changed = False
        for tail in ("/chat/completions", "/messages", "/v1"):
            if url.endswith(tail):
                url, changed = url[: -len(tail)].rstrip("/"), True
    return url


def provider_of(conn: dict | None) -> str:
    """ถ้าไม่ได้ระบุ provider: endpoint ของ anthropic.com = anthropic นอกนั้น = openai (เข้ากับ config เดิม)"""
    p = (conn or {}).get("provider")
    if p in PROVIDERS:
        return p
    return "anthropic" if "anthropic.com" in ((conn or {}).get("endpoint") or "") else "openai"


def normalize_endpoint(url: str, provider: str = "openai") -> str:
    """ใส่แค่โดเมนก็ได้
    openai: เติม https:// และ /v1 ถ้าไม่มี path แล้วต่อท้าย /chat/completions
    anthropic: เติม https:// แล้วต่อท้าย /v1/messages"""
    if provider == "anthropic":
        return (strip_api_path(url) or ANTHROPIC_ENDPOINT) + "/v1/messages"
    url = _base(url)
    if not url:
        return DEFAULT_ENDPOINT
    if url.endswith("/v1/messages"):          # ใส่ URL ของแบบ Claude มา -> เปลี่ยนเป็นของ OpenAI
        url = url[: -len("/messages")]
    if urlparse(url).path in ("", "/"):
        url += "/v1"
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    return url


def models_url(endpoint: str, provider: str = "openai") -> str:
    if provider == "anthropic":
        return normalize_endpoint(endpoint, provider)[: -len("/messages")] + "/models?limit=100"
    return normalize_endpoint(endpoint)[: -len("/chat/completions")] + "/models"


def auth_headers(api_key: str, provider: str = "openai", auth: str = "bearer", version: str = ANTHROPIC_VERSION) -> dict:
    if provider == "anthropic":
        h = {"anthropic-version": version, "Content-Type": "application/json"}
        h.update({"Authorization": f"Bearer {api_key}"} if auth == "bearer" else {"x-api-key": api_key})
        return h
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _send(method: str, url: str, api_key: str, provider: str, **kw) -> requests.Response:
    """ส่งคำขอ ถ้าเป็น Claude จะลอง Bearer ก่อน ถ้าโดนปฏิเสธ (401/403) ลอง x-api-key
    และถ้าเวอร์ชันใหม่ใช้ไม่ได้ ลองเวอร์ชันเก่า แล้วจำวิธีที่ใช้ได้ไว้"""
    if provider != "anthropic":
        return requests.request(method, url, headers=auth_headers(api_key), timeout=TIMEOUT, **kw)
    host = urlparse(url).netloc
    combos = [(a, v) for a in AUTH_MODES for v in (ANTHROPIC_VERSION, LEGACY_VERSION)]
    if host in _working:
        combos.remove(_working[host]); combos.insert(0, _working[host])
    r = None
    for auth, version in combos:
        r = requests.request(method, url, headers=auth_headers(api_key, provider, auth, version), timeout=TIMEOUT, **kw)
        if r.status_code in (401, 403):
            continue
        if r.status_code == 400 and "version" in r.text.lower():
            continue
        if r.status_code == 200:
            _working[host] = (auth, version)
        return r
    return r


def list_models(endpoint: str, api_key: str, provider: str = "openai") -> list[str]:
    """ดึงรายชื่อโมเดลจาก endpoint (raise error พร้อมข้อความจาก server ถ้าไม่สำเร็จ)"""
    r = _send("GET", models_url(endpoint, provider), api_key, provider)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
    ids = [m.get("id", "") for m in r.json().get("data", [])]
    return sorted({i.replace("models/", "") for i in ids if i})


# ---------------- prompt ----------------
def build_system_prompt(shop: dict | None = None) -> str:
    """สร้าง System Prompt จากการตั้งค่าร้าน (ชื่อ ประเภทสินค้า โทน คำลงท้าย กฎเพิ่มเติม)"""
    shop = {**DEFAULT_SHOP, **(shop or {})}
    particle = shop["particle"]
    tone = TONE_PRESETS.get(shop["tone"], TONE_PRESETS[DEFAULT_SHOP["tone"]])
    particle_rule = (f'- ลงท้ายประโยคด้วย "{particle}" (เช่น {apply_particle("ค่ะ / นะคะ", particle)})' if particle
                     else "- ไม่ใช้คำลงท้าย ค่ะ/ครับ/นะคะ/นะครับ เขียนให้สุภาพและเป็นกลาง")
    examples = "\n\n".join(
        f"รีวิว: {e['review']}\nผลลัพธ์: "
        + json.dumps({**e["output"], "reply": apply_particle(e["output"]["reply"], particle)}, ensure_ascii=False)
        for e in EXAMPLES
    )
    extra = (shop.get("extra_rules") or "").strip()
    extra_block = f"\nกฎเพิ่มเติมของร้าน (สำคัญกว่ากฎทั่วไป):\n{extra}\n" if extra else ""
    return f"""คุณคือผู้ช่วยแอดมินของร้าน "{shop['name']}" ({shop['desc']})
หน้าที่: อ่านรีวิวลูกค้า วิเคราะห์ แล้วร่างคำตอบ

โทนการตอบ ({shop['tone']}):
{tone}
{particle_rule}

กฎที่ต้องทำตาม:
{RULES}{extra_block}
ตอบเป็น JSON object อย่างเดียว ห้ามมีข้อความอื่น รูปแบบ:
{{"sentiment": "positive|neutral|negative",
 "aspects": [รายการจาก {ASPECTS}],
 "urgency": "low|medium|high",
 "reply": "คำตอบ"}}

ตัวอย่าง:
{examples}
"""


def _clean_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", flags=re.S)
    if not m:
        raise ValueError(f"ไม่พบ JSON ในคำตอบ: {str(text)[:150]}")
    return json.loads(m.group(0))


def _normalize(d: dict) -> dict:
    sentiment = d.get("sentiment", "neutral")
    if sentiment not in ("positive", "neutral", "negative"):
        sentiment = "neutral"
    urgency = d.get("urgency", "low")
    if urgency not in URGENCY_ORDER:
        urgency = "low"
    aspects = [a for a in d.get("aspects", []) if a in ASPECTS] or ["other"]
    return {"sentiment": sentiment, "aspects": aspects, "urgency": urgency, "reply": str(d.get("reply", "")).strip()}


# ---------- โหมดเดโม (ไม่มี API key) : แค่ให้ UI ทำงานได้ ไม่ใช่ AI จริง ----------
_NEG = ["แตก", "เสีย", "ช้า", "ผิดหวัง", "ไม่ตรงปก", "แย่", "ห่วย", "คืน", "บุบ", "แพ้", "คัน", "ผื่น"]
_POS = ["ดี", "ชอบ", "ประทับใจ", "เร็ว", "ไว", "สวย", "ใส", "คุ้ม"]


def _mock(text: str, particle: str = "ค่ะ") -> dict:
    neg = sum(w in text for w in _NEG)
    pos = sum(w in text for w in _POS)
    if neg > pos:
        s, u = "negative", ("high" if any(w in text for w in ["แตก", "แพ้", "คัน", "ผื่น"]) else "medium")
        reply = "ต้องขอโทษคุณลูกค้าด้วยนะคะ ทางร้านเสียใจที่ประสบการณ์ไม่ดี รบกวนทักแชทร้านเพื่อให้แอดมินตรวจสอบและดูแลต่อค่ะ"
    elif pos > neg:
        s, u = "positive", "low"
        reply = "ขอบคุณคุณลูกค้ามากนะคะ ดีใจที่ชอบค่ะ แวะมาอุดหนุนอีกนะคะ 💕"
    else:
        s, u = "neutral", "low"
        reply = "ขอบคุณที่ให้ความเห็นนะคะ ทางร้านจะนำไปปรับปรุงค่ะ"
    return {"sentiment": s, "aspects": ["other"], "urgency": u, "reply": "[DEMO] " + apply_particle(reply, particle)}


def _particle(conn: dict | None) -> str:
    return {**DEFAULT_SHOP, **((conn or {}).get("shop") or {})}["particle"]


# ---------------- main ----------------
def analyze_review(conn: dict | None, text: str, rating=None, temperature: float = 0.4, avoid: str | None = None) -> dict:
    """conn = {"provider"?, "endpoint", "model", "api_key", "shop"?} หรือ None (โหมดเดโม)
    avoid = คำตอบเดิม (ตอนกด "สร้างใหม่") ให้ AI เขียนเวอร์ชันที่ใช้ถ้อยคำต่างไป
    คืน dict: sentiment, aspects, urgency, reply, error (True ถ้าเรียก AI ไม่สำเร็จ)"""
    if not conn or not conn.get("api_key"):
        return {**_mock(text, _particle(conn)), "error": False}
    user_msg = f"รีวิว (ดาว {rating if rating == rating and rating else '-'}): {text}"
    if avoid:
        user_msg += f"\n\nคำตอบเดิมที่แอดมินไม่เลือก: {avoid}\nเขียน reply ใหม่ที่ใช้ถ้อยคำและโครงประโยคต่างจากเดิมชัดเจน แต่ยังทำตามโทนและกฎเหมือนเดิม"
    provider = provider_of(conn)
    system = build_system_prompt(conn.get("shop"))
    if provider == "anthropic":
        body = {
            "model": conn.get("model") or ANTHROPIC_MODEL,
            "max_tokens": MAX_TOKENS,   # API เวอร์ชันใหม่ไม่รับ temperature จึงไม่ส่ง
            "system": system,
            "messages": [{"role": "user", "content": user_msg}],
        }
    else:
        body = {
            "model": conn.get("model") or DEFAULT_MODEL,
            "temperature": temperature,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user_msg}],
        }
    url = normalize_endpoint(conn.get("endpoint"), provider)
    last_err = None
    for attempt in range(RETRIES + 1):
        try:
            r = _send("POST", url, conn["api_key"], provider, json=body)
            if r.status_code in (429, 529) or r.status_code >= 500:
                last_err = RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
                time.sleep(2 * (attempt + 1))
                continue
            if r.status_code == 400 and "temperature" in r.text and "temperature" in body:
                body.pop("temperature")   # บางโมเดลไม่รับ temperature -> ส่งใหม่โดยไม่ใส่
                continue
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
            data = r.json()
            if provider == "anthropic":
                content = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
            else:
                content = data["choices"][0]["message"]["content"]
            return {**_normalize(_clean_json(content)), "error": False}
        except requests.Timeout:
            last_err = RuntimeError(f"timeout เกิน {TIMEOUT} วินาที")
        except Exception as e:  # JSON เพี้ยน / key ผิด ฯลฯ -> ไม่ต้องลองซ้ำ
            last_err = e
            break
    out = _mock(text, _particle(conn))
    out["reply"] = f"[ERROR: {str(last_err)[:300]}] " + out["reply"]
    return {**out, "error": True}


def analyze_many(conn, items, workers: int = 4, on_progress=None) -> list[dict]:
    """วิเคราะห์หลายรีวิวพร้อมกัน items = [(text, rating), ...] คืนผลตามลำดับเดิม"""
    results = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max(1, int(workers))) as ex:
        futs = {ex.submit(analyze_review, conn, t, r): k for k, (t, r) in enumerate(items)}
        for done, f in enumerate(as_completed(futs), 1):
            results[futs[f]] = f.result()
            if on_progress:
                on_progress(done, len(items))
    return results


def read_reviews(f, name: str) -> pd.DataFrame:
    """อ่าน CSV/TSV แล้วแปลงเป็นคอลัมน์มาตรฐาน text, rating, label
    รองรับชื่อคอลัมน์หลายแบบ เช่น Review/Liked (ชุดข้อมูล Kaggle) -> text/label"""
    sep = "\t" if name.lower().endswith(".tsv") else ","
    raw = pd.read_csv(f, sep=sep)
    cols = {str(c).strip().lower(): c for c in raw.columns}
    pick = lambda names: next((cols[n] for n in names if n in cols), None)
    text_col = pick(["text", "review", "comment", "รีวิว", "ข้อความ"])
    if text_col is None:
        raise ValueError(f"ไม่พบคอลัมน์ข้อความรีวิว (ต้องชื่อ text หรือ review) คอลัมน์ที่มี: {list(raw.columns)}")
    rating_col = pick(["rating", "stars", "ดาว"])
    label_col = pick(["label", "liked", "sentiment"])
    out = pd.DataFrame({"text": raw[text_col].astype(str).str.strip()})
    out["rating"] = raw[rating_col] if rating_col is not None else None
    if label_col is not None:
        lab = raw[label_col].astype(str).str.strip().str.lower()
        out["label"] = lab.replace({"1": "positive", "0": "negative", "pos": "positive", "neg": "negative"})
    return out[out["text"].str.len() > 0].reset_index(drop=True)
