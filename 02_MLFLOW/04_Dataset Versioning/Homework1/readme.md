# 📝 การบ้าน: MLflow CSV Dataset Versioning

## วิชา MLOps — Dataset Versioning Lab

---

## คำชี้แจง

- การบ้านนี้มี **1 ข้อ** แบ่งเป็น 3 Steps ทำตามลำดับ
- ให้เขียน code ใน Python file (.py) หรือ Jupyter Notebook (.ipynb)
- **ส่ง:** ไฟล์ code + screenshot MLflow UI จำนวน 1 รูป (แสดง experiment ที่มี 2 runs)

---

## โจทย์: สร้างและ Track CSV Dataset 2 Versions ด้วย MLflow

ให้นักศึกษาสร้าง dataset ข้อมูลนักศึกษา (Student Dataset) จำนวน **2 versions** แล้ว log ทั้ง 2 versions ไปยัง MLflow จากนั้นเปรียบเทียบความแตกต่าง

ทำงานทั้งหมดภายใน experiment ชื่อ `"HW_Student_Dataset_{รหัสนักศึกษา}"`

---

### Step 1: สร้าง Dataset 2 Versions แล้วบันทึกเป็นไฟล์ CSV

#### Version 1 — ข้อมูลเริ่มต้น (1,000 rows)

สร้าง DataFrame ที่มี columns ต่อไปนี้:

| Column | วิธีสร้าง |
|--------|----------|
| `student_id` | 1 ถึง 1000 |
| `gpa` | สุ่มจาก `np.random.uniform(1.0, 4.0)` ทศนิยม 2 ตำแหน่ง |
| `study_hours` | สุ่มจาก `np.random.randint(1, 40)` |
| `passed` | สุ่ม 0 หรือ 1 (สัดส่วน 70% ผ่าน, 30% ไม่ผ่าน) |

บันทึกเป็นไฟล์ `students_v1.csv`

#### Version 2 — ข้อมูลที่เพิ่มขึ้น (1,500 rows)

สร้าง DataFrame เหมือน Version 1 แต่เปลี่ยน:
- จำนวน **1,500 rows**
- **เพิ่ม column ใหม่** ชื่อ `faculty` สุ่มจาก: `["วิศวกรรม", "วิทยาศาสตร์", "บริหาร", "ศิลปศาสตร์"]`

บันทึกเป็นไฟล์ `students_v2.csv`

#### 💡 Hint Step 1

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 1000

df_v1 = pd.DataFrame({
    'student_id': range(1, n + 1),
    'gpa': np.round(np.random.uniform(1.0, 4.0, n), 2),
    'study_hours': np.random.randint(1, 40, n),
    'passed': np.random.choice([0, 1], n, p=[0.3, 0.7])
})

df_v1.to_csv("students_v1.csv", index=False)
```

สำหรับ Version 2 ให้ทำคล้ายกัน แต่เปลี่ยน `n = 1500` และเพิ่ม column `faculty` โดยใช้ `np.random.choice()`

---

### Step 2: Log ทั้ง 2 Versions ไปยัง MLflow

สำหรับ **แต่ละ version** ให้สร้าง 1 run แล้ว log ข้อมูลตามตารางนี้:

| ประเภท | สิ่งที่ต้อง Log | ตัวอย่าง |
|--------|----------------|----------|
| **Parameter** | `dataset_version` | `"1.0.0"` หรือ `"2.0.0"` |
| **Parameter** | `dataset_name` | `"student_dataset"` |
| **Metric** | `num_rows` | จำนวนแถว |
| **Metric** | `num_columns` | จำนวน columns |
| **Metric** | `pass_rate` | สัดส่วนที่ `passed == 1` |
| **Artifact** | ไฟล์ CSV | `students_v1.csv` หรือ `students_v2.csv` |
| **Dataset Input** | `mlflow.log_input()` | ใช้ `mlflow.data.from_pandas()` |

- Run ที่ 1 ตั้งชื่อว่า `"student_v1"`
- Run ที่ 2 ตั้งชื่อว่า `"student_v2"`

#### 💡 Hint Step 2

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("HW_Student_Dataset_6xxxxxxxxx")  # ใส่รหัส นศ.

# ===== Log Version 1 =====
with mlflow.start_run(run_name="student_v1"):
    df = pd.read_csv("students_v1.csv")

    # สร้าง dataset object แล้ว log
    dataset = mlflow.data.from_pandas(df, source="students_v1.csv", name="student_dataset", targets="passed")
    mlflow.log_input(dataset, context="training")

    # log parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "student_dataset")

    # log metrics
    mlflow.log_metric("num_rows", len(df))
    # ... เพิ่ม metric ที่เหลือเอง ...

    # log artifact
    mlflow.log_artifact("students_v1.csv", artifact_path="datasets")
```

สำหรับ Version 2 ให้ทำเหมือนกัน แต่เปลี่ยน run_name, version, และใช้ไฟล์ `students_v2.csv`

---

### Step 3: เปรียบเทียบ 2 Versions

เขียน code ดึงข้อมูลจาก 2 runs มาแสดงผลเป็นตารางเปรียบเทียบ ตัวอย่างผลลัพธ์ที่ควรได้:

```
  Run Name    Version  Rows  Columns  Pass Rate
student_v1    1.0.0    1000     4       0.70
student_v2    2.0.0    1500     5       0.xx
```

#### 💡 Hint Step 3

```python
client = mlflow.tracking.MlflowClient()
experiment = mlflow.get_experiment_by_name("HW_Student_Dataset_6xxxxxxxxx")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"]
)

results = []
for run in runs:
    results.append({
        "Run Name": run.info.run_name,
        "Version": run.data.params.get("dataset_version"),
        "Rows": run.data.metrics.get("num_rows"),
        "Columns": run.data.metrics.get("num_columns"),
        "Pass Rate": run.data.metrics.get("pass_rate"),
    })

print(pd.DataFrame(results).to_string(index=False))
```

---

## สิ่งที่ต้องส่ง

1. ไฟล์ code (.py หรือ .ipynb)
2. Screenshot MLflow UI 1 รูป (แสดง experiment ที่มี 2 runs)

---

*💡 อย่าลืมเปิด MLflow server ก่อนรัน code:*
```bash
mlflow server --host 0.0.0.0 --port 5000
```