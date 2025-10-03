
# 🔎 Evidently AI: เครื่องมือสำหรับตรวจสอบคุณภาพข้อมูลและติดตามการทำงานของโมเดล

## 📌 บทนำ

ในการพัฒนา **Machine Learning (ML)** และ **AI** ปัญหาที่มักเกิดขึ้นหลังจากการนำโมเดลไปใช้งานจริงคือ

* คุณภาพข้อมูลที่เปลี่ยนไป (**Data Quality Issues**)
* การกระจายตัวของข้อมูลเปลี่ยนจากตอน train (**Data Drift**)
* สมรรถนะของโมเดลตกลงเมื่อใช้งานกับข้อมูลจริง (**Model Performance Degradation**)

**Evidently AI** จึงถูกพัฒนาขึ้นมาเพื่อช่วย **ติดตาม ตรวจสอบ และทำรายงาน** เกี่ยวกับข้อมูลและโมเดลอย่างเป็นระบบ โดยสามารถใช้งานได้ตั้งแต่ใน **Jupyter Notebook**, การ integrate กับ **MLflow**, ไปจนถึงการ deploy ใน production pipeline

---

## 🛠️ ความสามารถหลักของ Evidently AI

1. **Data Quality Monitoring**

   * ตรวจสอบ missing values, outliers, data type mismatches
   * ทำ Data Summary และสถิติพื้นฐานแบบอัตโนมัติ

2. **Data Drift Detection**

   * เปรียบเทียบ distribution ระหว่าง **reference dataset (train/valid)** และ **current dataset (production/test)**
   * รองรับทั้ง feature แบบ **ตัวเลข (numerical)** และ **หมวดหมู่ (categorical)**
   * ใช้สถิติต่าง ๆ เช่น KS-test, Chi-Square, Jensen–Shannon Divergence

3. **Target Drift & Prediction Drift**

   * ตรวจสอบว่า target (หรือ label) ที่เกิดขึ้นจริงใน production distribution เปลี่ยนไปจากตอน train หรือไม่
   * ใช้เพื่อเช็กว่าโมเดลยังคงทำนายได้แม่นยำหรือมี drift เกิดขึ้น

4. **Model Performance Monitoring**

   * ประเมิน performance ของโมเดล เช่น Accuracy, Precision, Recall, F1, ROC-AUC
   * สร้างรายงาน performance ระหว่าง production vs training

5. **Integration & Reports**

   * Export เป็น **HTML Report** หรือ **JSON**
   * ใช้ร่วมกับ **MLflow, Airflow, Prefect, Kubernetes** หรือ CI/CD pipeline ได้
   * มี Preset Report ที่พร้อมใช้งาน เช่น `DataDriftPreset()`, `DataQualityPreset()`

---

## 📊 ตัวอย่างการใช้งานเบื้องต้น

```python
import pandas as pd
from sklearn.datasets import load_iris
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

# โหลดข้อมูล Iris
df = load_iris(as_frame=True).frame

# สร้าง Report ตรวจสอบคุณภาพข้อมูล
report = Report([DataQualityPreset()])
report.run(reference_data=df, current_data=df)

# บันทึกเป็น HTML
report.save_html("data_quality_report.html")

# สร้าง Report ตรวจสอบ Data Drift
drift_report = Report([DataDriftPreset()])
drift_report.run(reference_data=df.iloc[:80], current_data=df.iloc[80:])
drift_report.save_html("data_drift_report.html")
```

---

## ✅ สรุป

Evidently AI เป็นเครื่องมือที่ช่วยให้นักพัฒนาและนักวิจัย **เข้าใจการเปลี่ยนแปลงของข้อมูลและประสิทธิภาพของโมเดล** ได้ชัดเจนขึ้น ช่วยให้การทำ **MLOps** ครบวงจรยิ่งขึ้น โดยสามารถเริ่มต้นใช้งานได้ง่ายใน Jupyter Notebook และสามารถขยายไปสู่ระดับ Production Monitoring ได้อย่างยืดหยุ่น

