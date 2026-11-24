import time

import pandas as pd
import streamlit as st

from core import (analyze_review, analyze_many, list_models, normalize_endpoint, read_reviews,
                  URGENCY_ORDER, DEFAULT_ENDPOINT, DEFAULT_MODEL)
from settings_store import load_config, save_config, save_shop, IS_WINDOWS
from shop_config import DEFAULT_SHOP, TONE_PRESETS, PARTICLES

st.set_page_config(page_title="AI Review Reply Assistant", page_icon="💬", layout="wide")
ss = st.session_state

SENT_ICON = {"positive": "🟢", "neutral": "🟡", "negative": "🔴"}
SENT_TH = {"positive": "บวก", "neutral": "กลาง", "negative": "ลบ"}
URG_ICON = {"high": "🚨", "medium": "⚠️", "low": "▫️"}
URG_TH = {"high": "ด่วนมาก", "medium": "ปานกลาง", "low": "ทั่วไป"}
ASP_TH = {"quality": "คุณภาพ", "shipping": "การจัดส่ง", "packaging": "แพ็กเกจ", "price": "ราคา",
          "service": "บริการ", "other": "อื่น ๆ"}
STATUS_TH = {"pending": "⏳ รออนุมัติ", "approved": "✅ อนุมัติแล้ว", "approved_edited": "✅ อนุมัติแล้ว (แก้ไข)"}
PAGE_SIZE = 10

# ---------------- state ----------------
if "saved" not in ss:
    ss.saved = load_config()
    ss.endpoint = ss.saved["endpoint"] or DEFAULT_ENDPOINT
    ss.model_id = ss.saved["model"] or DEFAULT_MODEL
    ss.model_list = []
    ss.df = None          # ผลวิเคราะห์
    ss.src = None         # รีวิวที่โหลดมา (ยังไม่วิเคราะห์)
    ss.src_name = ""
    ss.src_id = None
    ss.page = 0
    ss.analysis_seconds = None
    _shop = {**DEFAULT_SHOP, **ss.saved.get("shop", {})}
    ss.shop_name, ss.shop_desc, ss.shop_rules = _shop["name"], _shop["desc"], _shop["extra_rules"]
    ss.shop_tone = _shop["tone"] if _shop["tone"] in TONE_PRESETS else DEFAULT_SHOP["tone"]
    ss.shop_particle = _shop["particle"] if _shop["particle"] in PARTICLES else DEFAULT_SHOP["particle"]


def shop_now() -> dict:
    return {"name": ss.shop_name.strip() or DEFAULT_SHOP["name"], "desc": ss.shop_desc.strip() or DEFAULT_SHOP["desc"],
            "tone": ss.shop_tone, "particle": ss.shop_particle, "extra_rules": ss.shop_rules}


def _pick_model():
    ss.model_id = ss.model_pick


# ---------------- sidebar ----------------
with st.sidebar:
    with st.expander("🏪 ตั้งค่าร้าน", expanded=True):
        st.text_input("ชื่อร้าน", key="shop_name")
        st.text_input("ขายอะไร / รายละเอียดร้าน", key="shop_desc", placeholder="เช่น ร้านเสื้อผ้าผู้หญิงบน Shopee")
        st.selectbox("โทนการตอบ", list(TONE_PRESETS), key="shop_tone")
        st.radio("คำลงท้าย", PARTICLES, key="shop_particle", horizontal=True)
        st.text_area("กฎเพิ่มเติมของร้าน (ไม่ใส่ก็ได้)", key="shop_rules", height=80,
                     placeholder="เช่น ถ้าลูกค้าถามเรื่องไซซ์ ให้แนะนำตารางไซซ์ในหน้าสินค้า")
        if st.button("บันทึกการตั้งค่าร้าน", width="stretch"):
            try:
                save_shop(shop_now())
                st.success("บันทึกแล้ว")
            except Exception as e:
                st.error(f"บันทึกไม่ได้: {e}")
        st.caption("คำตอบที่ร่างหลังจากนี้จะใช้การตั้งค่านี้ (กด 🔄 เขียนใหม่ เพื่อดูโทนใหม่กับรีวิวเดิม)")

    st.subheader("Cloud API")
    st.caption("ใส่โดเมนหรือ API URL ได้เลย ระบบเติม https:// และใช้ /v1 หากไม่ได้ระบุ path")
    st.text_input("API endpoint", key="endpoint")
    st.text_input("Model ID", key="model_id")
    saved_key = ss.saved["api_key"]
    api_key_in = st.text_input("API key", type="password",
                               placeholder="ตั้งค่าแล้ว — เว้นว่างเพื่อใช้ key เดิม" if saved_key else "วาง API key")
    api_key = api_key_in.strip() or saved_key
    conn = {"endpoint": ss.endpoint, "model": ss.model_id, "api_key": api_key, "shop": shop_now()} if api_key else None

    c1, c2 = st.columns(2)
    if c1.button("ดึงรายชื่อโมเดล", width="stretch"):
        if not api_key:
            st.error("ใส่ API key ก่อน")
        else:
            try:
                ss.model_list = list_models(ss.endpoint, api_key)
                st.success(f"พบ {len(ss.model_list)} โมเดล")
            except Exception as e:
                ss.model_list = []
                st.error(f"ดึงรายชื่อไม่ได้: {e}")
    if c2.button("ทดสอบเชื่อมต่อ", width="stretch"):
        if not conn:
            st.error("ใส่ API key ก่อน")
        else:
            t0 = time.time()
            with st.spinner("กำลังทดสอบ..."):
                a = analyze_review(conn, "ของดีมาก ส่งไว", 5)
            if a["error"]:
                st.error(a["reply"][:400])
            else:
                st.success(f"ใช้ได้ ✓ ตอบใน {time.time() - t0:.1f} วินาที")
    if ss.model_list:
        opts = ss.model_list
        st.selectbox("เลือกโมเดล", opts, index=opts.index(ss.model_id) if ss.model_id in opts else 0,
                     key="model_pick", on_change=_pick_model)

    if st.button("บันทึกการเชื่อมต่อ", type="primary", width="stretch"):
        try:
            key_saved = save_config(ss.endpoint, ss.model_id, api_key_in.strip() or None)
            ss.saved = load_config()
            st.success("บันทึกแล้ว" + ("" if key_saved else " (ไม่ได้บันทึก key)"))
        except Exception as e:
            st.error(f"บันทึกไม่ได้: {e}")
    st.caption("บันทึก endpoint และโมเดลไว้ในเครื่อง พร้อมเข้ารหัส API key ด้วยบัญชี Windows นี้ เปิดโปรแกรมใหม่ไม่ต้องใส่ซ้ำ"
               if IS_WINDOWS else "บันทึก endpoint และโมเดลไว้ในเครื่อง (API key จะไม่ถูกบันทึกบน OS นี้)")

    st.divider()
    workers = st.slider("จำนวนคำขอพร้อมกัน", 1, 8, 4,
                        help="มากขึ้น = เร็วขึ้น แต่ถ้า API มีลิมิตต่ำ (เช่น Gemini ฟรี) อาจโดน rate limit ให้ลดลง")
    if conn:
        st.info(f"ใช้: `{ss.model_id}`\n\n{normalize_endpoint(ss.endpoint)}")
    else:
        st.warning("โหมดเดโม: ยังไม่มี API key (ไม่ใช่ AI จริง)")

# ---------------- header ----------------
st.title("💬 AI Customer Sentiment & Auto-Draft Reply")
st.caption(f"ระบบวิเคราะห์รีวิวลูกค้าและร่างคำตอบกลับร้านค้า · ร้าน: **{shop_now()['name']}** · โทน: {ss.shop_tone}")
tab_up, tab_q, tab_dash = st.tabs(["1️⃣ อัปโหลด/วิเคราะห์", "2️⃣ คิวรีวิว (ตรวจก่อนส่ง)", "3️⃣ Dashboard"])


def _reset_cards():
    for k in [k for k in ss.keys() if str(k).startswith(("reply_", "regen_"))]:
        del ss[k]
    ss.page = 0


# ---------------- tab 1: upload / analyze ----------------
with tab_up:
    with st.expander("✍️ ลองรีวิวเดียว (เหมาะกับเดโมสด)"):
        one = st.text_area("พิมพ์รีวิว", placeholder="เช่น ส่งช้ามาก ของมาไม่ครบ", key="one_text")
        if st.button("วิเคราะห์และร่างคำตอบ", key="one_go", disabled=not one.strip()):
            t0 = time.time()
            with st.spinner("AI กำลังคิด..."):
                a = analyze_review(conn, one.strip())
            if a["error"]:
                st.error(a["reply"][:400])
            else:
                st.markdown(f"{SENT_ICON[a['sentiment']]} {SENT_TH[a['sentiment']]} · {URG_ICON[a['urgency']]} {URG_TH[a['urgency']]} · "
                            f"{', '.join(ASP_TH.get(x, x) for x in a['aspects'])} · {time.time() - t0:.1f} วินาที")
                st.info(a["reply"])
    st.write("อัปโหลดไฟล์ CSV หรือ TSV ที่มีคอลัมน์ข้อความรีวิว (`text` หรือ `Review`) "
             "จะมี `rating` และ `label` ด้วยก็ได้ หรือกดใช้ข้อมูลตัวอย่าง")
    up = st.file_uploader("ไฟล์รีวิว", type=["csv", "tsv"])
    if st.button("ใช้ข้อมูลตัวอย่าง (12 รีวิว)"):
        ss.src, ss.src_name, ss.src_id = read_reviews("sample_reviews.csv", "sample_reviews.csv"), "ข้อมูลตัวอย่าง", "sample"
    if up is not None:
        fid = getattr(up, "file_id", None) or f"{up.name}-{up.size}"
        if fid != ss.src_id:  # โหลดเฉพาะตอนเปลี่ยนไฟล์ ไม่โหลดซ้ำทุกครั้งที่กดปุ่ม
            try:
                ss.src, ss.src_name, ss.src_id = read_reviews(up, up.name), up.name, fid
            except Exception as e:
                st.error(f"อ่านไฟล์ไม่ได้: {e}")

    if ss.src is not None:
        n_all = len(ss.src)
        st.success(f"โหลด **{ss.src_name}** แล้ว: {n_all} รีวิว"
                   + (" (มีป้ายคำตอบ ใช้วัดความแม่นยำได้)" if "label" in ss.src.columns else ""))
        with st.expander("ดูตัวอย่างข้อมูล"):
            st.dataframe(ss.src.head(20), width="stretch", hide_index=True)
        n = st.number_input("จำนวนรีวิวที่จะวิเคราะห์", 1, n_all, min(n_all, 50),
                            help="ไฟล์ใหญ่ ๆ ลองทีละน้อยก่อน จะได้ไม่เปลือง API")
        est = n * 4 / max(1, workers)
        st.caption(f"ใช้เวลาประมาณ {est:.0f}–{est * 2:.0f} วินาที (ขึ้นกับความเร็วของ API) · เรียก AI {n} ครั้ง")
        if st.button("▶️ เริ่มวิเคราะห์", type="primary"):
            sub = ss.src.head(int(n)).reset_index(drop=True)
            bar = st.progress(0.0, text="กำลังวิเคราะห์...")
            t0 = time.time()
            res = analyze_many(conn, list(zip(sub["text"], sub["rating"])), workers,
                               lambda d, tot: bar.progress(d / tot, text=f"วิเคราะห์ {d}/{tot}"))
            ss.analysis_seconds = time.time() - t0
            out = sub.copy()
            for k in ["sentiment", "aspects", "urgency", "reply", "error"]:
                out[k] = [a[k] for a in res]
            out.insert(0, "id", range(1, len(out) + 1))
            out["status"] = "pending"
            ss.df = out
            _reset_cards()
            errs = int(out["error"].sum())
            bar.empty()
            if errs:
                st.error(f"เรียก AI ไม่สำเร็จ {errs}/{len(out)} รีวิว (ใช้คำตอบเดโมแทน)\n\n"
                         f"สาเหตุตัวอย่าง: {out.loc[out['error'], 'reply'].iloc[0][:400]}")
            st.success(f"วิเคราะห์เสร็จ {len(out)} รีวิว ใน {ss.analysis_seconds:.1f} วินาที "
                       f"(เฉลี่ย {ss.analysis_seconds / len(out):.1f} วินาที/รีวิว) ไปที่แท็บ 2 ได้เลย")


# ---------------- tab 2: review queue ----------------
@st.fragment
def review_card(rid: int, conn):
    """การ์ด 1 รีวิว กดปุ่มในนี้จะรีเฟรชแค่การ์ดนี้ ไม่โหลดทั้งหน้า"""
    df = ss.df
    i = df.index[df["id"] == rid][0]
    key = f"reply_{rid}"

    if ss.pop(f"regen_{rid}", False):
        with st.spinner("กำลังเขียนคำตอบใหม่..."):
            a = analyze_review(conn, str(df.at[i, "text"]), df.at[i, "rating"],
                               temperature=0.9, avoid=ss.get(key) or df.at[i, "reply"])
        df.at[i, "reply"] = a["reply"]
        df.at[i, "status"] = "pending"
        ss[key] = a["reply"]
        if a["error"]:
            st.error(a["reply"][:300])
    if key not in ss:
        ss[key] = df.at[i, "reply"]

    r = df.loc[i]
    rating = r["rating"]
    stars = f" · {'⭐' * int(rating)}" if pd.notna(rating) and str(rating).replace(".", "").isdigit() else ""
    with st.container(border=True):
        st.markdown(f"{SENT_ICON[r['sentiment']]} {URG_ICON[r['urgency']]} **#{rid}** · "
                    f"{SENT_TH[r['sentiment']]} · {URG_TH[r['urgency']]} · "
                    f"{', '.join(ASP_TH.get(a, a) for a in r['aspects'])}{stars}")
        st.markdown(f"> {r['text']}")
        st.text_area("ร่างคำตอบ (แก้ไขได้)", key=key, height=100)
        c1, c2, c3 = st.columns([1, 1, 2])
        if r["status"] == "pending":
            if c1.button("✅ อนุมัติ", key=f"ok_{rid}", width="stretch"):
                draft = ss[key]
                df.at[i, "status"] = "approved_edited" if draft.strip() != str(r["reply"]).strip() else "approved"
                df.at[i, "reply"] = draft
                st.rerun()
        else:
            if c1.button("↩️ ยกเลิก", key=f"undo_{rid}", width="stretch"):
                df.at[i, "status"] = "pending"
                st.rerun()
        c2.button("🔄 เขียนใหม่", key=f"re_{rid}", width="stretch",
                  on_click=lambda: ss.update({f"regen_{rid}": True}))
        c3.markdown(f"<div style='padding-top:.45rem'>{STATUS_TH[r['status']]}</div>", unsafe_allow_html=True)


with tab_q:
    df = ss.df
    if df is None:
        st.info("ยังไม่มีข้อมูล ไปที่แท็บ 1 แล้วกด ▶️ เริ่มวิเคราะห์")
    else:
        f1, f2, f3 = st.columns([1.2, 1.5, 1.5])
        show = f1.radio("สถานะ", ["รออนุมัติ", "อนุมัติแล้ว", "ทั้งหมด"], horizontal=True, on_change=lambda: ss.update(page=0))
        sents = f2.multiselect("Sentiment", ["negative", "neutral", "positive"], ["negative", "neutral", "positive"],
                               format_func=lambda s: f"{SENT_ICON[s]} {SENT_TH[s]}", on_change=lambda: ss.update(page=0))
        q = f3.text_input("ค้นหาในรีวิว", on_change=lambda: ss.update(page=0))

        view = df[df["sentiment"].isin(sents)]
        if show == "รออนุมัติ":
            view = view[view["status"] == "pending"]
        elif show == "อนุมัติแล้ว":
            view = view[view["status"] != "pending"]
        if q:
            view = view[view["text"].str.contains(q, case=False, regex=False)]
        view = view.assign(_u=view["urgency"].map(URGENCY_ORDER),
                           _s=view["sentiment"].map({"negative": 0, "neutral": 1, "positive": 2})
                           ).sort_values(["_u", "_s", "id"])

        pages = max(1, -(-len(view) // PAGE_SIZE))
        ss.page = min(ss.page, pages - 1)
        st.caption(f"{len(view)} รีวิว · เรียงตามความเร่งด่วน (ลบ/ด่วนอยู่บนสุด) · หน้า {ss.page + 1}/{pages}")
        if view.empty:
            st.success("ไม่มีรีวิวค้าง 🎉" if show == "รออนุมัติ" else "ไม่พบรีวิวตามตัวกรอง")
        for rid in view["id"].iloc[ss.page * PAGE_SIZE:(ss.page + 1) * PAGE_SIZE]:
            review_card(int(rid), conn)

        if pages > 1:
            p1, p2, p3 = st.columns([1, 2, 1])
            if p1.button("◀ ก่อนหน้า", disabled=ss.page == 0, width="stretch"):
                ss.page -= 1
                st.rerun()
            p2.markdown(f"<div style='text-align:center;padding-top:.45rem'>หน้า {ss.page + 1} / {pages}</div>",
                        unsafe_allow_html=True)
            if p3.button("ถัดไป ▶", disabled=ss.page >= pages - 1, width="stretch"):
                ss.page += 1
                st.rerun()


# ---------------- tab 3: dashboard ----------------
with tab_dash:
    df = ss.df
    if df is None:
        st.info("ยังไม่มีข้อมูล")
    else:
        total = len(df)
        neg = int((df["sentiment"] == "negative").sum())
        urgent = int((df["urgency"] == "high").sum())
        approved = int(df["status"].str.startswith("approved").sum())
        no_edit = int((df["status"] == "approved").sum())
        m = st.columns(5)
        m[0].metric("รีวิวทั้งหมด", total)
        m[1].metric("รีวิวลบ", f"{neg / total * 100:.0f}%")
        m[2].metric("ด่วนมาก 🚨", urgent)
        m[3].metric("อนุมัติแล้ว", f"{approved}/{total}")
        m[4].metric("ส่งได้โดยไม่แก้", f"{(no_edit / approved * 100) if approved else 0:.0f}%")

        ok = df[~df["error"]]
        if "label" in df.columns and len(ok):
            labeled = ok[ok["label"].isin(["positive", "neutral", "negative"])]
            if len(labeled):
                acc = (labeled["sentiment"] == labeled["label"]).mean()
                st.metric("ความแม่นยำ Sentiment เทียบป้ายในไฟล์", f"{acc * 100:.1f}%",
                          help=f"คำนวณจาก {len(labeled)} รีวิวที่มีป้ายและเรียก AI สำเร็จ")
                if not labeled["label"].eq("neutral").any() and labeled["sentiment"].eq("neutral").any():
                    st.caption("ไฟล์นี้ไม่มีป้าย neutral รีวิวที่ AI ตอบว่า 'กลาง' จึงนับเป็นผิด")
        if df["error"].any():
            st.warning(f"เรียก AI ไม่สำเร็จ {int(df['error'].sum())} รีวิว (ไม่นับในความแม่นยำ)")
        if ss.analysis_seconds:
            st.caption(f"เวลาวิเคราะห์: {ss.analysis_seconds:.1f} วินาที (เฉลี่ย {ss.analysis_seconds / total:.1f} วินาที/รีวิว)")

        c1, c2 = st.columns(2)
        c1.subheader("Sentiment")
        c1.bar_chart(df["sentiment"].map(SENT_TH).value_counts())
        c2.subheader("เรื่องที่ลูกค้าบ่น (รีวิวลบ)")
        asp = df[df["sentiment"] == "negative"]["aspects"].explode().map(lambda a: ASP_TH.get(a, a)).value_counts()
        if len(asp):
            c2.bar_chart(asp)
        else:
            c2.write("ไม่มีรีวิวลบ")

        export = df.drop(columns=["error"]).assign(aspects=df["aspects"].map(", ".join))
        st.download_button("⬇️ ดาวน์โหลดผลลัพธ์ (CSV)", export.to_csv(index=False).encode("utf-8-sig"), "results.csv")
