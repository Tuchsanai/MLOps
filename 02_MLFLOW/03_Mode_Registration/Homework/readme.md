# 📝 การบ้าน: MLflow Model Registry

**วิชา:** Machine Learning Operations (MLOps)  
**หัวข้อ:** MLflow Model Registry

---

## 📋 คำแนะนำทั่วไป

1. ทำการบ้านใน Jupyter Notebook หรือ Python script
2. MLflow Server ต้องรันอยู่ที่ `http://127.0.0.1:5000`
3. ใส่ชื่อ-นามสกุล และรหัสนักศึกษาในไฟล์ที่ส่ง

### 📤 สิ่งที่ต้องส่งให้ TA ตรวจสอบ
- ไฟล์ code (.ipynb หรือ .py) พร้อมผลลัพธ์การรัน
- Screenshot หน้า MLflow UI แสดง Registered Model และ Versions
- ตารางเปรียบเทียบ accuracy ของแต่ละ Model Version

---

## 📚 ข้อที่ 1: Wine Quality Classification Model Registry

### 🎯 วัตถุประสงค์
ฝึกการใช้ MLflow Model Registry กับข้อมูล Wine Quality โดยการ train หลาย models, ลงทะเบียนเข้า Registry, จัดการ versions และ aliases

### 📖 โจทย์

นักศึกษาต้องสร้างระบบจำแนกคุณภาพไวน์ (Wine Quality Classification) โดยใช้ MLflow Model Registry เพื่อจัดการโมเดลหลายเวอร์ชัน

**งานที่ต้องทำ:**

1. **Train Model 3 Versions**
   - Version 1: `DecisionTreeClassifier` (baseline)
   - Version 2: `RandomForestClassifier` (n_estimators=100)
   - Version 3: `GradientBoostingClassifier` (n_estimators=100)
   
2. **ลงทะเบียน Models เข้า Registry**
   - ใช้ชื่อ Registered Model: `wine-quality-classifier`
   - เพิ่ม Description ที่อธิบายโมเดลอย่างชัดเจน
   - เพิ่ม Tags สำหรับ Registered Model: `task`, `dataset`, `team`
   - เพิ่ม Tags สำหรับแต่ละ Version: `model_type`, `status`

3. **จัดการ Aliases**
   - กำหนด `baseline` alias ให้ Version 1
   - กำหนด `staging` alias ให้ Version ที่มี accuracy สูงเป็นอันดับ 2
   - กำหนด `champion` alias ให้ Version ที่มี accuracy สูงที่สุด

4. **โหลดและทดสอบ Models**
   - โหลด champion model จาก Registry
   - ทดสอบทำนายกับข้อมูล test set 10 ตัวอย่าง
   - แสดงผล predictions และ actual values

### 🔧 Code เริ่มต้น

```python
# === การบ้านข้อที่ 1: Wine Quality Classification ===
# ชื่อ-นามสกุล: _______________
# รหัสนักศึกษา: _______________

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.models import infer_signature
import numpy as np

# === Setup ===
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# === โหลดข้อมูล Wine Quality ===
wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

print(f"✅ โหลดข้อมูล Wine Quality สำเร็จ")
print(f"📊 Training samples: {len(X_train)}")
print(f"📊 Test samples: {len(X_test)}")
print(f"📊 Features: {wine.feature_names}")
print(f"📊 Classes: {wine.target_names}")

# === กำหนดชื่อ Registered Model ===
MODEL_NAME = "wine-quality-classifier"

# === สร้าง Experiment ===
mlflow.set_experiment("wine-quality-homework")

# TODO: เขียน code ต่อจากนี้
# 1. Train และลงทะเบียน Model Version 1 (DecisionTree)
# 2. Train และลงทะเบียน Model Version 2 (RandomForest)
# 3. Train และลงทะเบียน Model Version 3 (GradientBoosting)
# 4. เพิ่ม Description และ Tags
# 5. กำหนด Aliases
# 6. โหลดและทดสอบ Champion Model

```

---


**ขอให้โชคดีในการทำการบ้าน! 🎓**