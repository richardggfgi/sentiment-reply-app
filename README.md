# AI Customer Sentiment & Auto-Draft Reply
ระบบวิเคราะห์รีวิวลูกค้าและร่างคำตอบกลับร้านค้า · IT232 AI for IT · Final Project

วิเคราะห์รีวิวลูกค้า (อารมณ์ บวก/กลาง/ลบ · แง่มุมสินค้า · ความเร่งด่วน) แล้วร่างคำตอบตามโทนและกฎของร้าน
แอดมินตรวจ แก้ หรือกด "เขียนใหม่" ก่อนอนุมัติทุกครั้ง (Human-in-the-loop)

## วิธีรัน (Windows)
1. แตกไฟล์ zip
2. ดับเบิลคลิก `run.bat` ครั้งแรกจะติดตั้ง Python 3.12 และแพ็กเกจให้ (ใช้เวลาไม่กี่นาที) แล้วเปิดเบราว์เซอร์ที่ http://localhost:8501
3. ในแถบซ้าย หัวข้อ **Cloud API** เลือกแบบ API ใส่ Endpoint, Model ID และ API key แล้วกด "ทดสอบเชื่อมต่อ" และ "บันทึกการเชื่อมต่อ"
   - **Claude (Anthropic)** (ค่าเริ่มต้น): Endpoint `https://api.anthropic.com` · Model ค่าเริ่มต้น `claude-haiku-5-5` · คีย์จาก Claude Console (ส่งด้วย `Authorization: Bearer` ถ้าไม่ผ่านจะลอง `x-api-key` ให้อัตโนมัติ) ใช้กับ proxy ที่รองรับรูปแบบ Anthropic ได้ด้วย
   - **OpenAI-compatible**: เช่น Gemini Endpoint `https://generativelanguage.googleapis.com/v1beta/openai` · Model `gemini-2.5-flash` · คีย์จาก aistudio.google.com หรือบริการใดก็ได้ที่รองรับ `/chat/completions`
4. แท็บแรก: อัปโหลด `sample_reviews.csv` หรือ `restaurant_reviews_150.tsv` แล้วกด "เริ่มวิเคราะห์"

### ความปลอดภัยของ API key
- key ที่พิมพ์ในแถบข้างอยู่แค่ในหน้านั้น ปิดหน้าแล้วหาย และ **ลบอัตโนมัติเมื่อครบ 12 ชั่วโมง** (มีปุ่ม "ลบ key ออกตอนนี้")
- key ที่บันทึกในเครื่อง (Windows) เข้ารหัสไว้ และลบอัตโนมัติเมื่อครบ 12 ชั่วโมงเช่นกัน
- **ห้ามใส่ key ในไฟล์โค้ดหรืออัปโหลดขึ้น GitHub**

### ใส่ key ไว้ใน Streamlit Cloud (ไม่บังคับ)
ให้คนที่เปิดลิงก์ใช้ AI จริงได้โดยไม่ต้องใส่ key เอง: share.streamlit.io → แอป → ⋮ → **Settings → Secrets** แล้ววาง
```toml
ANTHROPIC_API_KEY = "วาง key ตรงนี้"
ANTHROPIC_ENDPOINT = "https://api.anthropic.com"   # ถ้าเป็น key ของ proxy ให้ใส่โดเมนของ proxy แทน
ANTHROPIC_KEY_UNTIL = "2026-11-27 18:00"           # เวลาไทย ต้องไม่เกิน 12 ชม. จากตอนนี้ (บังคับ)
```
- ไม่ใส่ `ANTHROPIC_KEY_UNTIL`, เลยเวลาแล้ว หรือตั้งเกิน 12 ชม. = แอปไม่ใช้ key นี้
- key ไม่แสดงบนหน้าเว็บ และส่งไปเฉพาะ endpoint ที่ตั้งไว้เท่านั้น (ถ้ามีคนเปลี่ยน endpoint จะไม่ส่ง key ไป)
- ใช้ key ของระบบ = ล็อกโมเดลเป็น Haiku และวิเคราะห์ได้ครั้งละไม่เกิน 150 รีวิว (กันคนเอาไปเผาโควตา)

ถ้าไม่ใส่ API key แอปจะอยู่ใน **โหมดเดโม** (ใช้คำสำคัญง่ายๆ ไม่ใช่ AI) ไว้ดูหน้าตาเท่านั้น

### วิธีรันแบบอื่น (มี Python อยู่แล้ว / macOS / Linux)
```
pip install -r requirements.txt
streamlit run app.py
```

## ไฟล์ในโปรเจกต์
| ไฟล์ | หน้าที่ |
|---|---|
| `app.py` | หน้าเว็บ Streamlit: ตั้งค่าร้าน, คิวรีวิว, แดชบอร์ด |
| `theme.py`, `.streamlit/config.toml` | หน้าตาแอป (ธีมเดียวกับสไลด์ของกลุ่ม) |
| `core.py` | เรียก AI ผ่าน Claude API (Anthropic Messages) หรือ API แบบ OpenAI-compatible, สร้าง System Prompt, แปลงผลเป็น JSON |
| `shop_config.py` | โทนการตอบ กฎของร้าน และตัวอย่าง Few-shot |
| `settings_store.py` | บันทึกการตั้งค่า (API key เข้ารหัสด้วย Windows DPAPI ไม่ได้เก็บไว้ในโฟลเดอร์นี้) |
| `evaluate.py`, `evaluate.bat`, `evaluate_th.bat` | วัดความแม่นยำของ Sentiment เทียบกับป้ายจริง (ชุดอังกฤษ / ชุดไทย) |
| `finetune_wangchanberta.ipynb` | Notebook สำหรับ Google Colab: fine-tune WangchanBERTa ด้วยข้อมูล Wisesight |
| `sample_reviews.csv` | รีวิวตัวอย่าง 12 รีวิว (เขียนเองเพื่อทดสอบหน้าแอป) |
| `restaurant_reviews_150.tsv` | รีวิวร้านอาหารภาษาอังกฤษ 150 รีวิว (บวก 75 / ลบ 75) ใช้วัดผล |
| `restaurant_reviews_150_th.tsv` | รีวิวชุดเดียวกันที่เขียนใหม่เป็นภาษาไทยแบบรีวิวจริง ป้ายเดิม |

## ผลการวัด
| การทดสอบ | ผล |
|---|---|
| LLM ในแอป (gpt-6-luna) กับรีวิวร้านอาหารภาษาไทย 150 รีวิว | Accuracy 95.3% (เฉลี่ย 1.6 วินาทีต่อรีวิว) |
| LLM ในแอป กับรีวิวต้นฉบับภาษาอังกฤษ 150 รีวิว | Accuracy 96.7% |
| WangchanBERTa ก่อน fine-tune (ชุดทดสอบ Wisesight 1,161 ข้อความ) | Accuracy 41.9% |
| Baseline TF-IDF + Logistic Regression (ชุดเดียวกัน) | Accuracy 85.5% |
| WangchanBERTa หลัง fine-tune (ชุดเดียวกัน) | Accuracy 88.0% · Macro-F1 87.7% |

Fine-tune ด้วย 8,000 ข้อความ 2 epochs บน Google Colab (Tesla T4) ใช้เวลาประมาณ 1.5 นาที

## ข้อจำกัด
- ข้อมูล fine-tune (Wisesight) เป็นข้อความโซเชียลมีเดียไทยทั่วไป ไม่ใช่รีวิวสินค้าโดยตรง
- โมเดลที่ fine-tune แยกได้แค่บวก/ลบ และไม่ได้ต่อเข้ากับแอป (แอปใช้ LLM ผ่าน API)
- ไฟล์รีวิวร้านอาหารไม่มีป้าย "กลาง" รีวิวที่ AI ตอบว่ากลางจึงนับเป็นผิด
- รับรีวิวจากไฟล์ CSV/TSV ยังไม่ได้ดึงจาก Shopee/Lazada อัตโนมัติ
