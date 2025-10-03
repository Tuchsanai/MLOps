
# 📊 Introduction to Evidently AI

## 🎯 Objective

เรียนรู้การใช้ **Evidently AI** เพื่อ

* ตรวจสอบคุณภาพของข้อมูล (Data Quality)
* ตรวจจับการเปลี่ยนแปลงของข้อมูล (Data Drift / Concept Drift)
* สร้างรายงานวิเคราะห์ข้อมูล (Monitoring Reports)
* เชื่อมต่อกับ MLOps Workflow (เช่น MLflow, CI/CD, Airflow ฯลฯ)

---

## 📦 Step 0: Installation

ติดตั้ง Evidently AI ด้วยคำสั่ง:

```bash
pip install evidently
```

---

## 🔍 Step 1: ตรวจสอบคุณภาพข้อมูล (Data Quality Report)

Evidently สามารถสร้างรายงานคุณภาพข้อมูล เช่น missing values, outliers, distribution ฯลฯ

```python
import pandas as pd
from evidently.report import Report
from evidently.metrics import DataQualityPreset

# โหลด dataset ตัวอย่าง
df = pd.read_csv("https://raw.githubusercontent.com/evidentlyai/evidently/main/examples/data/data.csv")

# สร้างรายงาน Data Quality
report = Report(metrics=[DataQualityPreset()])
report.run(reference_data=None, current_data=df)

# แสดงผลใน Notebook
report.show()

# บันทึกเป็น HTML
report.save_html("data_quality_report.html")
```

📌 รายงานนี้ช่วยให้นักศึกษารู้ว่าข้อมูลที่ใช้ train/test มี **คุณภาพเพียงพอ** หรือไม่ เช่น missing values เยอะเกินไป หรือ feature distribution ผิดปกติ

---

## 📈 Step 2: ตรวจจับ Data Drift

เมื่อโมเดลใช้งานจริง ข้อมูลใหม่ (production data) อาจไม่เหมือนกับข้อมูลที่ใช้ train → โมเดลเสี่ยงต่อการ **เสื่อมคุณภาพ (model decay)**

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# reference = ข้อมูล train
reference = df.sample(500, random_state=42)

# current = ข้อมูลใหม่ที่เข้าโมเดล
current = df.sample(500, random_state=99)

# สร้างรายงาน Data Drift
drift_report = Report(metrics=[DataDriftPreset()])
drift_report.run(reference_data=reference, current_data=current)

# แสดงผล
drift_report.show()
drift_report.save_html("data_drift_report.html")
```

📌 จะได้รายงานบอกว่า feature ไหน drift, p-value, statistical test, และสรุปว่าข้อมูลเปลี่ยนแปลงไปมากน้อยแค่ไหน

---

## 🧠 Step 3: ตรวจสอบ Performance ของโมเดล

Evidently ยังสามารถใช้วัด performance drift เช่น accuracy, precision, recall, ROC curve ฯลฯ

```python
from evidently.report import Report
from evidently.metric_preset import ClassificationPreset

# ข้อมูลตัวอย่าง
y_true = df['target']
y_pred = (df['feature_1'] > 0.5).astype(int)

# รวมข้อมูล
eval_df = pd.DataFrame({"target": y_true, "prediction": y_pred})

# รายงาน Performance
perf_report = Report(metrics=[ClassificationPreset()])
perf_report.run(reference_data=eval_df, current_data=eval_df)

perf_report.show()
perf_report.save_html("classification_report.html")
```

📌 ใช้เพื่อตรวจสอบว่าโมเดลยังทำงานดีอยู่ใน production หรือไม่

---

## 🔗 Step 4: เชื่อมต่อกับ MLOps Workflow

Evidently สามารถ integrate เข้ากับเครื่องมือ MLOps ได้ เช่น

* **MLflow** → log รายงานเป็น artifact
* **Airflow / Prefect** → รันรายงานอัตโนมัติทุกวัน
* **Grafana / Prometheus** → สร้าง dashboard monitoring

ตัวอย่างเชื่อมกับ MLflow:

```python
import mlflow

with mlflow.start_run(run_name="data_quality_check"):
    report = Report(metrics=[DataQualityPreset()])
    report.run(current_data=df)
    report.save_html("dq_report.html")
    
    mlflow.log_artifact("dq_report.html")
```

---

## 📚 Use Cases ที่เหมาะสำหรับนักศึกษา

* 🧪 **ก่อน train โมเดล** → ตรวจสอบ dataset ให้แน่ใจว่าคุณภาพดี
* 🚀 **หลัง deploy โมเดล** → ตรวจสอบ production data drift
* 📉 **ระหว่างใช้งานจริง** → สร้าง monitoring dashboard
* 📑 **ทำรายงานวิชาการ** → สร้าง HTML report ที่ export ไปประกอบงานวิจัยได้

---

## 🎓 สรุป

**Evidently AI** เป็นเครื่องมือสำคัญสำหรับการทำ **Responsible AI และ MLOps** เพราะช่วยให้นักศึกษาและนักวิจัย

* เข้าใจปัญหาคุณภาพข้อมูล
* มอนิเตอร์โมเดลเมื่อใช้งานจริง
* สร้างรายงานเชิงสถิติอย่างสวยงาม
* ป้องกันโมเดลเสื่อมคุณภาพจาก Data Drift

