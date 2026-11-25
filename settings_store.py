"""บันทึก provider / endpoint / model / API key ไว้ในเครื่อง
- Windows: เข้ารหัส API key ด้วย DPAPI (ผูกกับบัญชี Windows ที่ล็อกอินอยู่ คนอื่น/เครื่องอื่นถอดไม่ได้)
- OS อื่น: ไม่บันทึก key (ต้องใส่ใหม่ทุกครั้ง)
- key ที่บันทึกไว้จะถูกลบอัตโนมัติเมื่อครบ KEY_TTL_HOURS ชั่วโมง"""
import base64
import json
import os
import sys
import time
from pathlib import Path

CONFIG_DIR = Path(os.getenv("APPDATA") or Path.home() / ".config") / "SentimentReply"
CONFIG_FILE = CONFIG_DIR / "config.json"
IS_WINDOWS = sys.platform == "win32"
KEY_TTL_HOURS = 12   # API key ใช้ได้นานสุดกี่ชั่วโมง เกินแล้วลบทิ้ง (กัน key ค้างแล้วโดนคนอื่นเอาไปใช้)


# ---------------- DPAPI (Windows only) ----------------
def _dpapi(data: bytes, encrypt: bool) -> bytes:
    import ctypes
    from ctypes import wintypes

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    buf = ctypes.create_string_buffer(data, len(data))
    inp = BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    out = BLOB()
    crypt32, kernel32 = ctypes.windll.crypt32, ctypes.windll.kernel32
    fn = crypt32.CryptProtectData if encrypt else crypt32.CryptUnprotectData
    ok = fn(ctypes.byref(inp), None, None, None, None, 0, ctypes.byref(out))
    if not ok:
        raise OSError("DPAPI failed")
    try:
        return ctypes.string_at(out.pbData, out.cbData)
    finally:
        kernel32.LocalFree(out.pbData)


def _encrypt_key(key: str) -> str | None:
    if not IS_WINDOWS:
        return None
    return base64.b64encode(_dpapi(key.encode("utf-8"), True)).decode()


def _decrypt_key(blob: str) -> str:
    return _dpapi(base64.b64decode(blob), False).decode("utf-8")


# ---------------- public ----------------
def load_config() -> dict:
    """คืน {"provider", "endpoint", "model", "api_key", "api_key_saved_at", "shop"}
    api_key = "" ถ้าไม่มี / ถอดไม่ได้ / บันทึกไว้นานเกิน KEY_TTL_HOURS (กรณีนี้ลบออกจากไฟล์ด้วย)"""
    cfg = {"provider": "", "endpoint": "", "model": "", "api_key": "", "api_key_saved_at": 0.0, "shop": {}}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        cfg["provider"] = data.get("provider", "")
        cfg["endpoint"] = data.get("endpoint", "")
        cfg["model"] = data.get("model", "")
        cfg["shop"] = data.get("shop", {}) or {}
        saved_at = float(data.get("api_key_saved_at") or 0)
        if data.get("api_key_enc") and time.time() - saved_at > KEY_TTL_HOURS * 3600:
            forget_key()   # key เก่าเกินกำหนด (หรือบันทึกก่อนมีระบบหมดอายุ) -> ลบทิ้ง
        elif data.get("api_key_enc") and IS_WINDOWS:
            cfg["api_key"] = _decrypt_key(data["api_key_enc"])
            cfg["api_key_saved_at"] = saved_at
    except Exception:
        pass
    return cfg


def save_config(endpoint: str, model: str, api_key: str | None, provider: str = "") -> bool:
    """api_key=None/"" = เก็บ key เดิมไว้  คืน True ถ้า key ถูกบันทึก (เข้ารหัสแล้ว)"""
    old = {}
    try:
        old = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    data = {**old, "provider": provider, "endpoint": endpoint, "model": model, "api_key_enc": old.get("api_key_enc")}
    if api_key:
        data["api_key_enc"] = _encrypt_key(api_key)
        data["api_key_saved_at"] = time.time()
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return bool(data["api_key_enc"])


def save_shop(shop: dict) -> None:
    """บันทึกการตั้งค่าร้าน (ชื่อ ประเภท โทน คำลงท้าย กฎเพิ่มเติม) ไว้ในไฟล์เดียวกัน"""
    old = {}
    try:
        old = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    old["shop"] = shop
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")


def forget_key() -> None:
    """ลบ API key ที่บันทึกไว้ออกจากไฟล์ (ค่าอื่นเก็บไว้เหมือนเดิม)"""
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return
    if data.pop("api_key_enc", None) is not None or "api_key_saved_at" in data:
        data.pop("api_key_saved_at", None)
        CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
