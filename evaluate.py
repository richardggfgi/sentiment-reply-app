"""วัดความแม่นยำของ Sentiment เทียบกับป้ายที่ทีมติดเอง (คอลัมน์ label)
ใช้: python evaluate.py labeled_reviews.csv   (ไม่ใส่ชื่อไฟล์ = ใช้ sample_reviews.csv)
ใช้การเชื่อมต่อที่กด "บันทึกการเชื่อมต่อ" ไว้ในแอป
รีวิวที่เรียก AI ไม่สำเร็จจะถูกตัดออกจากการคำนวณ และแจ้งจำนวนให้"""
import sys
import time

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

from core import analyze_many, read_reviews
from settings_store import load_config

path = sys.argv[1] if len(sys.argv) > 1 else "sample_reviews.csv"
workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4  # จำนวนคำขอพร้อมกัน
df = read_reviews(path, path)
if "label" not in df.columns:
    sys.exit("ไฟล์ไม่มีคอลัมน์ label/Liked จึงวัดความแม่นยำไม่ได้")
cfg = load_config()
conn = cfg if cfg.get("api_key") else None  # cfg มี shop ที่บันทึกไว้ในแอปด้วย
if not conn:
    sys.exit("ยังไม่มี API key ที่บันทึกไว้ เปิดแอปแล้วกด 'บันทึกการเชื่อมต่อ' ก่อน")
print("โมเดล:", cfg["model"], "|", cfg["endpoint"], "| รีวิว:", len(df))

t0 = time.time()
res = analyze_many(conn, list(zip(df["text"], df["rating"])), workers,
                   lambda d, tot: print(f"\r{d}/{tot}", end="", flush=True))
print(f"\nใช้เวลา {time.time() - t0:.1f} วินาที")

keep = [i for i, a in enumerate(res) if not a["error"]]
fails = [a["reply"][:200] for a in res if a["error"]]
if fails:
    print(f"!! เรียก AI ไม่สำเร็จ {len(fails)} รีวิว (ไม่นำมาคำนวณ) ตัวอย่าง: {fails[0]}")
if not keep:
    sys.exit("ไม่มีผลลัพธ์ให้คำนวณ")
preds = [res[i]["sentiment"] for i in keep]
truth = df["label"].iloc[keep]
labels = ["positive", "neutral", "negative"]
print(f"คำนวณจาก {len(preds)} รีวิว")
print(classification_report(truth, preds, labels=labels, digits=3, zero_division=0))
print("Confusion matrix (แถว=จริง, คอลัมน์=ทำนาย):")
print(pd.DataFrame(confusion_matrix(truth, preds, labels=labels), index=labels, columns=labels))
