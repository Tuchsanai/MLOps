https://scbtechx.io/th/blogs/data-science/blog-mlflow-machine-learning/



---

# 📊 Slide Deck: MLflow คืออะไร

---

## Slide 1: หัวข้อหลัก

**MLflow คืออะไร (What is MLflow?)**

* MLflow = แพลตฟอร์ม **Open Source** สำหรับจัดการ **วงจรชีวิตของ Machine Learning (ML Lifecycle)**
* ครอบคลุมตั้งแต่:

  * การทดลอง (Experimentation)
  * ความสามารถทำซ้ำได้ (Reproducibility)
  * การนำไปใช้งาน (Deployment)
  * การจัดเก็บโมเดลแบบรวมศูนย์ (Model Registry)

---

## Slide 2: ปัญหาก่อนมี MLflow

* นักวิจัย/วิศวกร ML มักเจอปัญหา:

  * 🔎 ยากต่อการติดตามว่า **Run ไหนดีที่สุด**
  * 📂 การจัดเก็บโมเดลไม่เป็นระบบ
  * ⚙️ การ deploy ไป production ซับซ้อน
  * 🧩 แต่ละองค์กรใช้ Framework ต่างกัน (scikit-learn, PyTorch, TensorFlow)

---

## Slide 3: โครงสร้างของ MLflow

MLflow มี **4 คอมโพเนนต์หลัก**

1. **Tracking** – บันทึก experiment (metrics, params, artifacts)
2. **Projects** – จัดแพ็กเกจโค้ด ML ให้ reproducible
3. **Models** – เก็บและ deploy โมเดลในหลาย format
4. **Model Registry** – ระบบ version control + governance ของโมเดล

---

## Slide 4: MLflow Tracking

* ใช้บันทึกการทดลอง ML
* สิ่งที่ Track ได้:

  * Hyperparameters (เช่น alpha, learning_rate)
  * Metrics (RMSE, Accuracy, F1-Score)
  * Artifacts (ไฟล์ CSV, รูป, pickle model)
* สามารถดูผลผ่าน **MLflow UI**

```python
import mlflow
with mlflow.start_run():
    mlflow.log_param("alpha", 0.5)
    mlflow.log_metric("rmse", 0.75)
    mlflow.sklearn.log_model(model, "model")
```

---

## Slide 5: MLflow Projects

* ทำให้โค้ด ML รันซ้ำได้ทุกที่
* ใช้ไฟล์ `MLproject` กำหนด dependencies
* รันด้วยคำสั่งเดียว เช่น:

```bash
mlflow run https://github.com/mlflow/mlflow-example
```

---

## Slide 6: MLflow Models

* รูปแบบมาตรฐานสำหรับจัดเก็บโมเดล
* Support หลาย Framework (sklearn, PyTorch, TensorFlow, XGBoost)
* สามารถ deploy ได้หลายวิธี เช่น:

  * REST API
  * Docker container
  * Cloud platforms (Azure ML, Sagemaker)

---

## Slide 7: Model Registry

* ใช้บริหารจัดการโมเดลอย่างเป็นระบบ
* ความสามารถ:

  * Versioning
  * Stage Transition (Staging → Production → Archived)
  * Annotation/Comments

---

## Slide 8: การใช้งานจริงใน Workflow

1. นักวิจัย ML → สร้างโมเดล + track experiment
2. ทีม Data Engineer → จัดแพ็กเกจเป็น Project
3. ทีม MLOps → Deploy และจัดการโมเดลใน Registry
4. ธุรกิจ → ใช้โมเดล Production ได้จริง

---

## Slide 9: Key Benefits ของ MLflow

* ✅ ใช้ได้กับ Framework หลากหลาย (agnostic)
* ✅ ติดตาม experiment ได้ง่าย
* ✅ Deploy สะดวก (multi-platform)
* ✅ บริหารจัดการโมเดลแบบ version control

---

## Slide 10: สรุป

**MLflow = One-stop platform**
สำหรับการจัดการ **Machine Learning Lifecycle**
ตั้งแต่ต้นจนจบ → **Experiment → Reproduce → Deploy → Manage**

---

