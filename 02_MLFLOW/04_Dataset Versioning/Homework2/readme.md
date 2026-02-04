# 📝 การบ้านข้อ 2: MLflow Image Dataset Versioning

## วิชา MLOps — Dataset Versioning Lab

---

## คำชี้แจง

- การบ้านนี้มี **1 ข้อ** แบ่งเป็น 3 Steps ทำตามลำดับ
- ให้เขียน code ใน Python file (.py) หรือ Jupyter Notebook (.ipynb)
- **ส่ง:** ไฟล์ code + screenshot MLflow UI จำนวน 1 รูป (แสดง experiment ที่มี 2 runs)

---

## โจทย์: สร้างและ Track Image Dataset 2 Versions ด้วย MLflow

ให้นักศึกษาจัดเตรียมรูปภาพ แมว (cat) และ สุนัข (dog) จาก Internet แล้วจัดเป็น dataset **2 versions** ดังนี้

| Version | เนื้อหา |
|---------|--------|
| **v1** | รูปแมว 2 รูป |
| **v2** | รูปแมว 1 รูป + รูปสุนัข 2 รูป (เพิ่ม class ใหม่) |

จากนั้น log ทั้ง 2 versions ไปยัง MLflow แล้วเปรียบเทียบความแตกต่าง

ทำงานทั้งหมดภายใน experiment ชื่อ `"HW_Image_Dataset_{รหัสนักศึกษา}"`

---

### Step 1: เตรียมรูปภาพและจัดโครงสร้างโฟลเดอร์

#### 1.1 หารูปภาพจาก Internet

ให้นักศึกษาหารูปภาพเอง โดย download จากเว็บไซต์ เช่น:
- https://unsplash.com (ค้นหา "cat", "dog")
- https://www.pexels.com (ค้นหา "cat", "dog")
- หรือเว็บอื่นๆ ที่ให้ใช้รูปได้ฟรี

รูปที่ใช้:
- รูปแมว รวม **2 รูป** (ใช้ใน v1 และ v2)
- รูปสุนัข รวม **2 รูป** (ใช้ใน v2)
- format: `.jpg` หรือ `.png`

#### 1.2 จัดโครงสร้างโฟลเดอร์

สร้างโฟลเดอร์ตามโครงสร้างนี้:

```
image_dataset/
├── v1/
│   └── cat/
│       ├── cat_01.jpg
│       └── cat_02.jpg
│
└── v2/
    ├── cat/
    │   └── cat_01.jpg
    └── dog/
        ├── dog_01.jpg
        └── dog_02.jpg
```

#### 💡 Hint Step 1

```python
import os

# สร้างโฟลเดอร์
os.makedirs("image_dataset/v1/cat", exist_ok=True)
os.makedirs("image_dataset/v2/cat", exist_ok=True)
os.makedirs("image_dataset/v2/dog", exist_ok=True)

print("✅ สร้างโฟลเดอร์เสร็จแล้ว")
print("📌 ให้นำรูปที่ download มาวางในโฟลเดอร์ตามโครงสร้างด้านบน")
```

หลังจากสร้างโฟลเดอร์แล้ว ให้ **copy รูปที่ download มาวางในโฟลเดอร์** ตามโครงสร้าง หรือจะเขียน code ย้ายไฟล์ก็ได้

---

### Step 2: Log ทั้ง 2 Versions ไปยัง MLflow

สำหรับ **แต่ละ version** ให้สร้าง 1 run แล้ว log ข้อมูลตามตารางนี้:

| ประเภท | สิ่งที่ต้อง Log | ตัวอย่าง |
|--------|----------------|----------|
| **Parameter** | `dataset_version` | `"1.0.0"` หรือ `"2.0.0"` |
| **Parameter** | `dataset_name` | `"cat_dog_dataset"` |
| **Parameter** | `num_classes` | จำนวน class (v1 = 1, v2 = 2) |
| **Parameter** | `class_names` | เช่น `["cat"]` หรือ `["cat", "dog"]` |
| **Metric** | `total_images` | จำนวนรูปทั้งหมด |
| **Metric** | `class_cat_count` | จำนวนรูปแมว |
| **Metric** | `class_dog_count` | จำนวนรูปสุนัข (v1 = 0, v2 = 2) |
| **Artifact** | รูปภาพทั้งหมด | log แยกตาม class เช่น `samples/cat/`, `samples/dog/` |

- Run ที่ 1 ตั้งชื่อว่า `"image_v1"`
- Run ที่ 2 ตั้งชื่อว่า `"image_v2"`

#### 💡 Hint Step 2

```python
import mlflow
from datetime import datetime

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("HW_Image_Dataset_6xxxxxxxxx")  # ใส่รหัส นศ.

# ===== ฟังก์ชันนับรูปในโฟลเดอร์ =====
def count_images(dataset_dir):
    """นับจำนวนรูปแยกตาม class"""
    class_counts = {}
    total = 0
    for class_name in os.listdir(dataset_dir):
        class_path = os.path.join(dataset_dir, class_name)
        if os.path.isdir(class_path):
            images = [f for f in os.listdir(class_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
            class_counts[class_name] = len(images)
            total += len(images)
    return class_counts, total

# ===== Log Version 1 =====
with mlflow.start_run(run_name="image_v1"):
    dataset_dir = "image_dataset/v1"
    class_counts, total = count_images(dataset_dir)

    # log parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "cat_dog_dataset")
    mlflow.log_param("num_classes", len(class_counts))
    mlflow.log_param("class_names", list(class_counts.keys()))

    # log metrics
    mlflow.log_metric("total_images", total)
    mlflow.log_metric("class_cat_count", class_counts.get("cat", 0))
    mlflow.log_metric("class_dog_count", class_counts.get("dog", 0))

    # log รูปภาพเป็น artifact
    for class_name in class_counts:
        class_path = os.path.join(dataset_dir, class_name)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            mlflow.log_artifact(img_path, artifact_path=f"samples/{class_name}")

    print(f"✅ Version 1 logged! Total images: {total}")
```

สำหรับ Version 2 ให้ทำเหมือนกัน แต่เปลี่ยน `run_name="image_v2"`, `dataset_version="2.0.0"`, และ `dataset_dir="image_dataset/v2"`

---

### Step 3: เปรียบเทียบ 2 Versions

เขียน code ดึงข้อมูลจาก 2 runs มาแสดงผลเป็นตารางเปรียบเทียบ ตัวอย่างผลลัพธ์ที่ควรได้:

```
 Run Name  Version  Total Images  Cat  Dog  Num Classes
 image_v1    1.0.0             2    2    0            1
 image_v2    2.0.0             3    1    2            2
```

#### 💡 Hint Step 3

```python
import pandas as pd

client = mlflow.tracking.MlflowClient()
experiment = mlflow.get_experiment_by_name("HW_Image_Dataset_6xxxxxxxxx")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"]
)

results = []
for run in runs:
    results.append({
        "Run Name": run.info.run_name,
        "Version": run.data.params.get("dataset_version"),
        "Total Images": run.data.metrics.get("total_images"),
        "Cat": run.data.metrics.get("class_cat_count"),
        "Dog": run.data.metrics.get("class_dog_count"),
        "Num Classes": run.data.params.get("num_classes"),
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