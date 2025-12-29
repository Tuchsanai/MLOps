
---

## ⚙️ Pre-requisite: เตรียมความพร้อมก่อนเริ่ม Lab

### 📋 สิ่งที่ต้องมี

ก่อนเริ่ม Lab นี้ ต้องมี MLflow Server รันอยู่และเข้าถึงได้ที่ `http://127.0.0.1:8080`

### 🔍 ตรวจสอบ MLflow Server

เปิด Browser แล้วไปที่: [http://127.0.0.1:8080](http://127.0.0.1:8080)

![MLflow UI](./img/1.png)

---



## 🚀 ขั้นตอนการเตรียม Lab Environment

### ขั้นตอนที่ 1: สร้างโฟลเดอร์สำหรับ Lab

```bash
# สร้างโฟลเดอร์ Lab แยกจาก mlflowserver-lab
mkdir -p mlflow-tracking-lab

# เข้าไปในโฟลเดอร์
cd mlflow-tracking-lab
```

### ขั้นตอนที่ 2: สร้าง Virtual Environment

```bash
# สร้าง Virtual Environment
python -m venv .venv

# เปิดใช้งาน Virtual Environment
source .venv/bin/activate

# อัพเดท pip
python -m pip install --upgrade pip
```

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

```bash
# ติดตั้ง MLflow และ Libraries ที่จำเป็น
pip install mlflow scikit-learn pandas numpy matplotlib seaborn
```

### ขั้นตอนที่ 4: ตรวจสอบการติดตั้ง

```bash
# ตรวจสอบเวอร์ชัน MLflow
mlflow --version

# ตรวจสอบ Python packages
pip list | grep -E "mlflow|scikit-learn|pandas"
```

### ขั้นตอนที่ 5: ตั้งค่า Tracking URI

```bash
# ตั้งค่า Environment Variable เพื่อเชื่อมต่อกับ MLflow Server
export MLFLOW_TRACKING_URI=http://127.0.0.1:8080
```

> 💡 **Tip**: เพิ่มบรรทัดนี้ใน `.bashrc` หรือ `.zshrc` เพื่อไม่ต้องตั้งค่าทุกครั้ง

---

## 🗂️ โครงสร้างโฟลเดอร์ Lab

```
mlflow-tracking-lab/
├── README.md                    # ไฟล์นี้
├── .venv/                       # Virtual Environment
├── experiments/                 # โฟลเดอร์เก็บไฟล์ทดลอง
│   ├── lab1_basic_tracking.py
│   ├── lab2_training_loop.py
│   ├── lab3_sklearn_autolog.py
│   ├── lab4_hyperparameter.py
│   ├── lab5_custom_artifacts.py
│   └── lab6_query_runs.py
└── outputs/                     # โฟลเดอร์เก็บ output ชั่วคราว
```

สร้างโครงสร้างโฟลเดอร์:

```bash
mkdir -p experiments outputs
```

---

## 📝 Lab 1: Basic Tracking

### 🎯 วัตถุประสงค์
- เรียนรู้การใช้ `mlflow.start_run()`
- บันทึก Parameters, Metrics และ Artifacts
- ดูผลลัพธ์ใน MLflow UI

### 📖 ทฤษฎีที่เกี่ยวข้อง

การบันทึกข้อมูลใน MLflow มี 3 ขั้นตอนหลัก:

```
1. เริ่ม Run      →  2. บันทึกข้อมูล  →  3. จบ Run
   start_run()       log_param()         end_run()
                     log_metric()        (อัตโนมัติถ้าใช้ with)
                     log_artifact()
```

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab1_basic_tracking.py`:

```python
"""
Lab 1: Basic MLflow Tracking
============================
เรียนรู้การบันทึก Parameters, Metrics และ Artifacts พื้นฐาน
"""

import mlflow
import os

# ตั้งค่า Tracking URI (เชื่อมต่อกับ MLflow Server)
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# สร้างหรือเลือก Experiment
# ถ้า Experiment นี้ยังไม่มี จะสร้างใหม่อัตโนมัติ
mlflow.set_experiment("lab1-basic-tracking")

print("=" * 50)
print("Lab 1: Basic MLflow Tracking")
print("=" * 50)

# เริ่ม Run ใหม่
# ใช้ with statement เพื่อให้ปิด Run อัตโนมัติ
with mlflow.start_run(run_name="my-first-run"):
    
    # ดู Run ID ปัจจุบัน
    run_id = mlflow.active_run().info.run_id
    print(f"\n📌 Run ID: {run_id}")
    
    # -------------------------------------------------
    # 1. บันทึก Parameters (ค่าที่ตั้งก่อนทดลอง)
    # -------------------------------------------------
    print("\n1️⃣ บันทึก Parameters...")
    
    # บันทึกทีละค่า
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # บันทึกหลายค่าพร้อมกัน
    mlflow.log_params({
        "learning_rate": 0.01,
        "random_state": 42
    })
    
    print("   ✅ บันทึก Parameters เสร็จสิ้น")
    
    # -------------------------------------------------
    # 2. บันทึก Metrics (ค่าที่วัดได้จากการทดลอง)
    # -------------------------------------------------
    print("\n2️⃣ บันทึก Metrics...")
    
    # บันทึก Metrics ค่าเดียว
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_metric("precision", 0.89)
    mlflow.log_metric("recall", 0.94)
    mlflow.log_metric("f1_score", 0.91)
    
    # บันทึกหลายค่าพร้อมกัน
    mlflow.log_metrics({
        "train_loss": 0.15,
        "val_loss": 0.22
    })
    
    print("   ✅ บันทึก Metrics เสร็จสิ้น")
    
    # -------------------------------------------------
    # 3. บันทึก Artifacts (ไฟล์ที่สร้างจากการทดลอง)
    # -------------------------------------------------
    print("\n3️⃣ บันทึก Artifacts...")
    
    # สร้างไฟล์ตัวอย่างเพื่อบันทึกเป็น Artifact
    os.makedirs("outputs", exist_ok=True)
    
    # สร้างไฟล์ข้อความ
    with open("outputs/model_info.txt", "w") as f:
        f.write("Model: RandomForest\n")
        f.write("Version: 1.0\n")
        f.write("Accuracy: 0.92\n")
    
    # สร้างไฟล์ JSON
    import json
    config = {
        "model_type": "RandomForest",
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 10
        }
    }
    with open("outputs/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # บันทึกไฟล์เดี่ยว
    mlflow.log_artifact("outputs/model_info.txt")
    mlflow.log_artifact("outputs/config.json")
    
    print("   ✅ บันทึก Artifacts เสร็จสิ้น")
    
    # -------------------------------------------------
    # 4. เพิ่ม Tags (ข้อมูลเพิ่มเติมสำหรับการค้นหา)
    # -------------------------------------------------
    print("\n4️⃣ บันทึก Tags...")
    
    mlflow.set_tag("developer", "student")
    mlflow.set_tag("experiment_type", "baseline")
    mlflow.set_tag("dataset", "iris")
    
    print("   ✅ บันทึก Tags เสร็จสิ้น")

print("\n" + "=" * 50)
print("🎉 Lab 1 เสร็จสิ้น!")
print("=" * 50)
print(f"\n📊 ดูผลลัพธ์ได้ที่: http://127.0.0.1:8080")
print(f"   → เลือก Experiment: lab1-basic-tracking")
print(f"   → คลิกที่ Run: my-first-run")
```

### ▶️ วิธีรัน

```bash
cd mlflow-tracking-lab
source .venv/bin/activate
python experiments/lab1_basic_tracking.py
```

### ✅ ผลลัพธ์ที่คาดหวัง

1. เปิด MLflow UI ที่ http://127.0.0.1:8080
2. เลือก Experiment "lab1-basic-tracking"
3. คลิกที่ Run "my-first-run"
4. ตรวจสอบ:
   - **Parameters**: model_type, n_estimators, max_depth, etc.
   - **Metrics**: accuracy, precision, recall, f1_score, etc.
   - **Artifacts**: model_info.txt, config.json
   - **Tags**: developer, experiment_type, dataset

### 📝 แบบฝึกหัด Lab 1

1. เพิ่ม Parameter ใหม่ชื่อ `min_samples_split` มีค่าเป็น 5
2. เพิ่ม Metric ใหม่ชื่อ `auc_roc` มีค่าเป็น 0.95
3. สร้างไฟล์ `notes.md` และบันทึกเป็น Artifact
4. เพิ่ม Tag ชื่อ `version` มีค่าเป็น "v1.0"

---

## 📝 Lab 2: Training Loop Tracking

### 🎯 วัตถุประสงค์
- บันทึก Metrics ระหว่าง Training Loop
- เข้าใจการใช้ `step` parameter ใน `log_metric()`
- ดู Loss Curve ใน MLflow UI

### 📖 ทฤษฎีที่เกี่ยวข้อง

การบันทึก Metrics ตามเวลา:

```python
# step คือลำดับของการบันทึก (เช่น epoch number)
mlflow.log_metric("loss", value, step=epoch)

# MLflow จะสร้างกราฟอัตโนมัติเมื่อมีหลาย step
```

```
Loss Curve ที่จะได้:

    Loss
    1.0 ┤●
        │ ╲
    0.8 ┤  ●
        │   ╲
    0.6 ┤    ●
        │     ╲
    0.4 ┤      ●
        │       ╲●
    0.2 ┤         ╲●●
        │            ╲●●●
    0.0 ┼───────────────────
        0  2  4  6  8  10  Epoch
```

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab2_training_loop.py`:

```python
"""
Lab 2: Training Loop Tracking
=============================
เรียนรู้การบันทึก Metrics ระหว่างการ Training
"""

import mlflow
import numpy as np
import matplotlib.pyplot as plt
import os

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("lab2-training-loop")

print("=" * 50)
print("Lab 2: Training Loop Tracking")
print("=" * 50)

# -------------------------------------------------
# จำลองการ Training Model
# -------------------------------------------------
def simulate_training(epochs, initial_loss=1.0, learning_rate=0.1):
    """
    จำลอง Loss ที่ลดลงระหว่างการ Training
    """
    losses = []
    val_losses = []
    
    for epoch in range(epochs):
        # จำลอง Training Loss (ลดลงเรื่อยๆ)
        train_loss = initial_loss * np.exp(-learning_rate * epoch)
        train_loss += np.random.normal(0, 0.02)  # เพิ่ม noise เล็กน้อย
        train_loss = max(0.01, train_loss)  # ไม่ให้ติดลบ
        
        # จำลอง Validation Loss (ลดลงช้ากว่า Train)
        val_loss = initial_loss * np.exp(-learning_rate * 0.8 * epoch)
        val_loss += np.random.normal(0, 0.03)
        val_loss = max(0.02, val_loss)
        
        losses.append(train_loss)
        val_losses.append(val_loss)
    
    return losses, val_losses

# Parameters
EPOCHS = 50
LEARNING_RATE = 0.1
INITIAL_LOSS = 1.0

# เริ่ม Run
with mlflow.start_run(run_name="training-simulation"):
    
    # บันทึก Parameters
    print("\n📋 บันทึก Parameters...")
    mlflow.log_params({
        "epochs": EPOCHS,
        "learning_rate": LEARNING_RATE,
        "initial_loss": INITIAL_LOSS,
        "optimizer": "SGD",
        "batch_size": 32
    })
    
    # จำลองการ Training
    print(f"\n🏃 เริ่ม Training จำลอง {EPOCHS} epochs...")
    train_losses, val_losses = simulate_training(
        EPOCHS, INITIAL_LOSS, LEARNING_RATE
    )
    
    # บันทึก Metrics ทุก Epoch
    print("\n📊 บันทึก Metrics...")
    for epoch in range(EPOCHS):
        # บันทึก Loss พร้อม step
        mlflow.log_metric("train_loss", train_losses[epoch], step=epoch)
        mlflow.log_metric("val_loss", val_losses[epoch], step=epoch)
        
        # บันทึก Accuracy จำลอง (เพิ่มขึ้นเรื่อยๆ)
        train_acc = 0.5 + 0.45 * (1 - np.exp(-0.1 * epoch))
        val_acc = 0.5 + 0.40 * (1 - np.exp(-0.1 * epoch))
        
        mlflow.log_metric("train_accuracy", train_acc, step=epoch)
        mlflow.log_metric("val_accuracy", val_acc, step=epoch)
        
        # แสดง Progress ทุก 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"   Epoch {epoch+1}/{EPOCHS}: "
                  f"train_loss={train_losses[epoch]:.4f}, "
                  f"val_loss={val_losses[epoch]:.4f}")
    
    # บันทึก Final Metrics
    mlflow.log_metrics({
        "final_train_loss": train_losses[-1],
        "final_val_loss": val_losses[-1],
        "final_train_accuracy": train_acc,
        "final_val_accuracy": val_acc,
        "best_val_loss": min(val_losses),
        "best_epoch": val_losses.index(min(val_losses))
    })
    
    # -------------------------------------------------
    # สร้างกราฟ Loss Curve และบันทึกเป็น Artifact
    # -------------------------------------------------
    print("\n📈 สร้างกราฟ Loss Curve...")
    os.makedirs("outputs", exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # กราฟ Loss
    axes[0].plot(train_losses, label='Training Loss', color='blue')
    axes[0].plot(val_losses, label='Validation Loss', color='orange')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Loss Curve')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # กราฟ Accuracy
    train_accs = [0.5 + 0.45 * (1 - np.exp(-0.1 * e)) for e in range(EPOCHS)]
    val_accs = [0.5 + 0.40 * (1 - np.exp(-0.1 * e)) for e in range(EPOCHS)]
    
    axes[1].plot(train_accs, label='Training Accuracy', color='blue')
    axes[1].plot(val_accs, label='Validation Accuracy', color='orange')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Accuracy Curve')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("outputs/training_curves.png", dpi=150)
    plt.close()
    
    # บันทึกกราฟเป็น Artifact
    mlflow.log_artifact("outputs/training_curves.png")
    print("   ✅ บันทึกกราฟ training_curves.png")

print("\n" + "=" * 50)
print("🎉 Lab 2 เสร็จสิ้น!")
print("=" * 50)
print(f"\n📊 ดูผลลัพธ์ได้ที่: http://127.0.0.1:8080")
print(f"   → เลือก Experiment: lab2-training-loop")
print(f"   → คลิกที่ Run แล้วไปที่ tab 'Charts'")
print(f"   → จะเห็น Loss Curve และ Accuracy Curve")
```

### ▶️ วิธีรัน

```bash
python experiments/lab2_training_loop.py
```

### ✅ ผลลัพธ์ที่คาดหวัง

1. เปิด MLflow UI
2. เลือก Experiment "lab2-training-loop"
3. คลิกที่ Run แล้วไปที่ tab **"Charts"**
4. จะเห็นกราฟ:
   - train_loss และ val_loss ลดลงตาม epoch
   - train_accuracy และ val_accuracy เพิ่มขึ้นตาม epoch

### 📝 แบบฝึกหัด Lab 2

1. เปลี่ยน `EPOCHS` เป็น 100 และรันใหม่
2. เปลี่ยน `LEARNING_RATE` เป็น 0.05 และเปรียบเทียบผล
3. เพิ่มการบันทึก `learning_rate_decay` ทุก 10 epochs
4. สร้างกราฟเปรียบเทียบ Train vs Val Loss ในแนวตั้ง

---

## 📝 Lab 3: Scikit-learn Autolog

### 🎯 วัตถุประสงค์
- ใช้ `mlflow.sklearn.autolog()` 
- เข้าใจการบันทึกอัตโนมัติ
- ดู Model ที่บันทึกใน MLflow UI

### 📖 ทฤษฎีที่เกี่ยวข้อง

**Autolog** คือฟีเจอร์ของ MLflow ที่บันทึกข้อมูลอัตโนมัติ:

```
┌─────────────────────────────────────────────────────────────────┐
│                    mlflow.sklearn.autolog()                     │
│                                                                 │
│  บันทึกอัตโนมัติ:                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Parameters  │  │   Metrics   │  │       Artifacts         │  │
│  │             │  │             │  │                         │  │
│  │ • All model │  │ • accuracy  │  │ • Trained model         │  │
│  │   params    │  │ • f1_score  │  │ • Feature names         │  │
│  │ • Fit time  │  │ • precision │  │ • Confusion matrix      │  │
│  │             │  │ • recall    │  │ • Training data stats   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                 │
│  รองรับ Frameworks:                                             │
│  sklearn, pytorch, tensorflow, keras, xgboost, lightgbm, ...   │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab3_sklearn_autolog.py`:

```python
"""
Lab 3: Scikit-learn Autolog
===========================
เรียนรู้การใช้ mlflow.sklearn.autolog()
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("lab3-sklearn-autolog")

print("=" * 50)
print("Lab 3: Scikit-learn Autolog")
print("=" * 50)

# -------------------------------------------------
# Part 1: ทดลองกับ Iris Dataset
# -------------------------------------------------
print("\n📊 Part 1: Iris Dataset with RandomForest")
print("-" * 40)

# โหลดข้อมูล
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# เปิด Autolog
mlflow.sklearn.autolog(
    log_input_examples=True,
    log_model_signatures=True,
    log_models=True
)

# Training - MLflow จะบันทึกทุกอย่างอัตโนมัติ!
with mlflow.start_run(run_name="iris-randomforest"):
    print("\n🌲 Training RandomForest...")
    
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.set_tag("dataset", "iris")
    mlflow.set_tag("model_type", "RandomForest")
    
    print(f"   ✅ Test Accuracy: {accuracy:.4f}")

# -------------------------------------------------
# Part 2: ทดลองกับ Wine Dataset
# -------------------------------------------------
print("\n📊 Part 2: Wine Dataset with LogisticRegression")
print("-" * 40)

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

with mlflow.start_run(run_name="wine-logistic"):
    print("\n📈 Training Logistic Regression...")
    
    lr_model = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    lr_model.fit(X_train, y_train)
    
    predictions = lr_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("model_type", "LogisticRegression")
    
    print(f"   ✅ Test Accuracy: {accuracy:.4f}")

# -------------------------------------------------
# Part 3: เปรียบเทียบหลาย Models
# -------------------------------------------------
print("\n📊 Part 3: Model Comparison on Iris")
print("-" * 40)

X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

models = [
    ("DecisionTree", DecisionTreeClassifier(max_depth=5, random_state=42)),
    ("SVM", SVC(kernel='rbf', random_state=42)),
    ("KNN", KNeighborsClassifier(n_neighbors=5))
]

for model_name, model in models:
    with mlflow.start_run(run_name=f"iris-{model_name.lower()}"):
        print(f"\n🔄 Training {model_name}...")
        
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        mlflow.log_metric("test_accuracy", accuracy)
        mlflow.set_tag("dataset", "iris")
        mlflow.set_tag("model_type", model_name)
        
        print(f"   ✅ {model_name} Accuracy: {accuracy:.4f}")

mlflow.sklearn.autolog(disable=True)

print("\n" + "=" * 50)
print("🎉 Lab 3 เสร็จสิ้น!")
print("=" * 50)
print(f"\n📊 ดูผลลัพธ์ได้ที่: http://127.0.0.1:8080")
print(f"   → เลือก Experiment: lab3-sklearn-autolog")
print(f"   → เปรียบเทียบ Runs ได้โดยติ๊กเลือกหลาย Runs")
print(f"   → คลิก 'Compare' เพื่อดูการเปรียบเทียบ")
```

### ▶️ วิธีรัน

```bash
python experiments/lab3_sklearn_autolog.py
```

### ✅ ผลลัพธ์ที่คาดหวัง

1. เปิด MLflow UI
2. เลือก Experiment "lab3-sklearn-autolog"
3. จะเห็น 5 Runs พร้อม Parameters และ Metrics ที่บันทึกอัตโนมัติ

### 📝 แบบฝึกหัด Lab 3

1. เพิ่ม Model ใหม่: `GradientBoostingClassifier`
2. ทดลองกับ `load_digits()` dataset
3. เปรียบเทียบ 3 Models และหา Model ที่ดีที่สุด

---

## 📝 Lab 4: Hyperparameter Comparison

### 🎯 วัตถุประสงค์
- ทดลอง Hyperparameter หลายค่า
- ใช้ MLflow UI เปรียบเทียบผล

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab4_hyperparameter.py`:

```python
"""
Lab 4: Hyperparameter Comparison
================================
เรียนรู้การทดลอง Hyperparameters หลายค่าและเปรียบเทียบผล
"""

import mlflow
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("lab4-hyperparameter-tuning")

print("=" * 50)
print("Lab 4: Hyperparameter Comparison")
print("=" * 50)

# โหลดข้อมูล
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# กำหนด Hyperparameter Search Space
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5, 10]
}

total_experiments = (len(param_grid['n_estimators']) * 
                    len(param_grid['max_depth']) * 
                    len(param_grid['min_samples_split']))

print(f"\n📋 Total experiments: {total_experiments}")

best_accuracy = 0
best_params = None
experiment_count = 0

for n_est in param_grid['n_estimators']:
    for max_d in param_grid['max_depth']:
        for min_split in param_grid['min_samples_split']:
            experiment_count += 1
            
            max_d_str = str(max_d) if max_d is not None else "None"
            run_name = f"rf_nest{n_est}_depth{max_d_str}_split{min_split}"
            
            with mlflow.start_run(run_name=run_name):
                mlflow.log_params({
                    "n_estimators": n_est,
                    "max_depth": max_d if max_d is not None else "unlimited",
                    "min_samples_split": min_split,
                    "random_state": 42
                })
                
                model = RandomForestClassifier(
                    n_estimators=n_est,
                    max_depth=max_d,
                    min_samples_split=min_split,
                    random_state=42,
                    n_jobs=-1
                )
                model.fit(X_train, y_train)
                
                predictions = model.predict(X_test)
                
                accuracy = accuracy_score(y_test, predictions)
                precision = precision_score(y_test, predictions)
                recall = recall_score(y_test, predictions)
                f1 = f1_score(y_test, predictions)
                
                cv_scores = cross_val_score(model, X_train, y_train, cv=5)
                
                mlflow.log_metrics({
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1,
                    "cv_mean": cv_scores.mean(),
                    "cv_std": cv_scores.std()
                })
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_params = {
                        "n_estimators": n_est,
                        "max_depth": max_d,
                        "min_samples_split": min_split
                    }
                    mlflow.set_tag("is_best", "true")
                else:
                    mlflow.set_tag("is_best", "false")
                
                print(f"   [{experiment_count}/{total_experiments}] "
                      f"{run_name}: accuracy={accuracy:.4f}")

print("\n" + "=" * 50)
print(f"🏆 Best Accuracy: {best_accuracy:.4f}")
print(f"   Best Params: {best_params}")
print("=" * 50)
```

### ▶️ วิธีรัน

```bash
python experiments/lab4_hyperparameter.py
```

---

## 📝 Lab 5: Custom Artifacts

### 🎯 วัตถุประสงค์
- สร้างและบันทึก Confusion Matrix
- บันทึก Feature Importance
- สร้าง Custom Visualizations

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab5_custom_artifacts.py`:

```python
"""
Lab 5: Custom Artifacts
=======================
เรียนรู้การสร้างและบันทึก Custom Artifacts
"""

import mlflow
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_curve, auc
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os
import warnings
warnings.filterwarnings('ignore')

mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("lab5-custom-artifacts")

os.makedirs("outputs", exist_ok=True)

data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

with mlflow.start_run(run_name="detailed-analysis"):
    
    params = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    mlflow.log_params(params)
    
    model = RandomForestClassifier(**params, n_jobs=-1)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    predictions_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Malignant', 'Benign'],
                yticklabels=['Malignant', 'Benign'])
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig("outputs/confusion_matrix.png", dpi=150)
    plt.close()
    mlflow.log_artifact("outputs/confusion_matrix.png")
    
    # 2. ROC Curve
    fpr, tpr, _ = roc_curve(y_test, predictions_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2,
             label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.savefig("outputs/roc_curve.png", dpi=150)
    plt.close()
    mlflow.log_metric("roc_auc", roc_auc)
    mlflow.log_artifact("outputs/roc_curve.png")
    
    # 3. Feature Importance
    feature_importance = pd.DataFrame({
        'feature': data.feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    feature_importance.to_csv("outputs/feature_importance.csv", index=False)
    mlflow.log_artifact("outputs/feature_importance.csv")
    
    plt.figure(figsize=(10, 8))
    top_features = feature_importance.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importance')
    plt.title('Top 15 Feature Importance')
    plt.gca().invert_yaxis()
    plt.savefig("outputs/feature_importance.png", dpi=150)
    plt.close()
    mlflow.log_artifact("outputs/feature_importance.png")
    
    print(f"✅ Accuracy: {accuracy:.4f}")
    print(f"✅ ROC AUC: {roc_auc:.4f}")

print("\n🎉 Lab 5 เสร็จสิ้น!")
print("📊 ดู Artifacts ได้ที่ MLflow UI → Artifacts tab")
```

### ▶️ วิธีรัน

```bash
python experiments/lab5_custom_artifacts.py
```

---

## 📝 Lab 6: Query & Search Runs

### 🎯 วัตถุประสงค์
- ใช้ MLflow API ค้นหา Runs
- เปรียบเทียบ Runs ด้วย Python

### 💻 โค้ดทดลอง

สร้างไฟล์ `experiments/lab6_query_runs.py`:

```python
"""
Lab 6: Query & Search Runs
==========================
เรียนรู้การใช้ MLflow API ค้นหาและเปรียบเทียบ Runs
"""

import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd

mlflow.set_tracking_uri("http://127.0.0.1:8080")

print("=" * 50)
print("Lab 6: Query & Search Runs")
print("=" * 50)

client = MlflowClient()

# 1. List Experiments
print("\n📋 1. List All Experiments")
experiments = client.search_experiments()
for exp in experiments:
    print(f"   ID: {exp.experiment_id} | Name: {exp.name}")

# 2. Get Experiment by Name
print("\n🔍 2. Get Experiment by Name")
exp_name = "lab4-hyperparameter-tuning"
experiment = client.get_experiment_by_name(exp_name)

if experiment:
    exp_id = experiment.experiment_id
    print(f"   Found: {experiment.name} (ID: {exp_id})")
    
    # 3. Search Runs
    print("\n🔎 3. Search Runs with accuracy > 0.95")
    runs_high_acc = mlflow.search_runs(
        experiment_ids=[exp_id],
        filter_string="metrics.accuracy > 0.95",
        order_by=["metrics.accuracy DESC"]
    )
    print(f"   พบ {len(runs_high_acc)} runs")
    
    # 4. Top 5 Runs
    print("\n📊 4. Top 5 Runs by Accuracy")
    top_runs = mlflow.search_runs(
        experiment_ids=[exp_id],
        order_by=["metrics.accuracy DESC"],
        max_results=5
    )
    
    if len(top_runs) > 0:
        cols = ['run_id', 'params.n_estimators', 'metrics.accuracy']
        available = [c for c in cols if c in top_runs.columns]
        print(top_runs[available].to_string(index=False))
    
    # 5. Statistics
    print("\n📈 5. Accuracy Statistics")
    all_runs = mlflow.search_runs(experiment_ids=[exp_id])
    if 'metrics.accuracy' in all_runs.columns:
        print(f"   Mean: {all_runs['metrics.accuracy'].mean():.4f}")
        print(f"   Max:  {all_runs['metrics.accuracy'].max():.4f}")
        print(f"   Min:  {all_runs['metrics.accuracy'].min():.4f}")
else:
    print(f"   ❌ Experiment '{exp_name}' not found. กรุณารัน Lab 4 ก่อน")

print("\n🎉 Lab 6 เสร็จสิ้น!")
```

### ▶️ วิธีรัน

```bash
python experiments/lab6_query_runs.py
```

---

## 📚 สรุป

### 🎯 สิ่งที่ได้เรียนรู้

| Lab | หัวข้อ | สิ่งที่เรียนรู้ |
|-----|--------|----------------|
| 1 | Basic Tracking | log_param, log_metric, log_artifact |
| 2 | Training Loop | บันทึก Metrics ตาม step/epoch |
| 3 | Sklearn Autolog | autolog() บันทึกอัตโนมัติ |
| 4 | Hyperparameter | Grid Search + เปรียบเทียบผล |
| 5 | Custom Artifacts | Confusion Matrix, ROC, Feature Importance |
| 6 | Query Runs | ค้นหาและวิเคราะห์ Runs ด้วย API |

### 📌 คำสั่งสำคัญที่ควรจำ

```python
# ตั้งค่าเชื่อมต่อ Server
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# เลือก Experiment
mlflow.set_experiment("my-experiment")

# เริ่ม Run
with mlflow.start_run(run_name="my-run"):
    mlflow.log_param("key", value)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.1, step=epoch)
    mlflow.log_artifact("file.png")
    mlflow.set_tag("key", "value")

# Autolog
mlflow.sklearn.autolog()

# ค้นหา Runs
runs = mlflow.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.accuracy > 0.9"
)
```

### 🔗 แหล่งเรียนรู้เพิ่มเติม

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Tracking Guide](https://mlflow.org/docs/latest/tracking.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/index.html)

---

## ❓ FAQ - คำถามที่พบบ่อย

### Q1: ทำไม MLflow UI ไม่แสดงผล?
**A:** ตรวจสอบว่า MLflow Server รันอยู่หรือไม่:
```bash
cd ../mlflowserver-lab
source .venv/bin/activate
mlflow server --host 127.0.0.1 --port 8080 \
  --backend-store-uri sqlite:///mlruns_db/mlflow.db \
  --artifacts-destination ./mlartifacts --serve-artifacts
```

### Q2: Error "MLFLOW_TRACKING_URI not set"
**A:** ตั้งค่า Environment Variable:
```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:8080
```

### Q3: Artifacts ไม่แสดงใน UI
**A:** ตรวจสอบว่า Server รันด้วย `--serve-artifacts` flag

---

## 🏁 Checklist ก่อนส่ง Lab

- [ ] รัน Lab 1-6 สำเร็จ
- [ ] ดูผลใน MLflow UI ได้
- [ ] เข้าใจความแตกต่างระหว่าง Parameters, Metrics, Artifacts
- [ ] ทำแบบฝึกหัดท้าย Lab อย่างน้อย 2 ข้อต่อ Lab

---

**🎉 ขอให้สนุกกับการเรียนรู้ MLflow Tracking!**