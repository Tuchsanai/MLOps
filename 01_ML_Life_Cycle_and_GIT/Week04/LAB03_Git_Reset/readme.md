# 🔄 Lab: Git Reset ใน MLOps Pipeline

## 📋 สารบัญ
1. [บทนำ](#บทนำ)
2. [ทฤษฎี Git Reset](#ทฤษฎี-git-reset)
3. [สถานการณ์จำลองใน MLOps](#สถานการณ์จำลองใน-mlops)
4. [Lab Exercise](#lab-exercise)
5. [สรุป](#สรุป)

---

## บทนำ

ในการทำงาน Machine Learning Operations (MLOps) เราต้องทำงานกับ code หลายเวอร์ชัน ตั้งแต่ขั้นตอนการเตรียมข้อมูล (Data Preparation), การฝึกโมเดล (Training), การทดสอบ (Testing) และการประเมินผล (Evaluation) 

การใช้ Git เป็นเครื่องมือสำคัญในการติดตามการเปลี่ยนแปลงของ code แต่บางครั้งเราอาจทำผิดพลาด เช่น:
- Commit code ที่มี bug
- ทดลองปรับ hyperparameters แล้วผลลัพธ์แย่ลง
- เปลี่ยน model architecture แล้วต้องการย้อนกลับ

**Git Reset** คือเครื่องมือที่ช่วยให้เราย้อนกลับไปยังสถานะก่อนหน้าได้

---

## ทฤษฎี Git Reset

### Git มี 3 พื้นที่หลัก (Three Trees)

```
┌─────────────────────────────────────────────────────────────────┐
│                        Git Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│   │  Working     │    │   Staging    │    │    HEAD      │      │
│   │  Directory   │───▶│    Area      │───▶│  (Commits)   │      │
│   │              │    │   (Index)    │    │              │      │
│   └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                    │               │
│         │    git add        │    git commit      │               │
│         └───────────────────┴────────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

1. **Working Directory**: ไฟล์ที่เราแก้ไขอยู่บนเครื่อง
2. **Staging Area (Index)**: ไฟล์ที่ถูก `git add` รอ commit
3. **HEAD**: ตำแหน่ง commit ล่าสุดที่ branch ชี้อยู่

### ประเภทของ Git Reset

```
┌─────────────────────────────────────────────────────────────────┐
│                    Git Reset Types Comparison                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Reset Type      │ HEAD │ Staging │ Working Dir │ Use Case      │
│  ────────────────┼──────┼─────────┼─────────────┼───────────────│
│  --soft          │  ✓   │    ✗    │      ✗      │ Redo commit   │
│  --hard          │  ✓   │    ✓    │      ✓      │ Discard all   │
│                                                                  │
│  ✓ = Reset/Change    ✗ = Keep unchanged                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 1. `git reset --soft <commit>`
- ย้าย HEAD ไปยัง commit ที่ระบุ
- **เก็บ** การเปลี่ยนแปลงใน Staging Area
- **เก็บ** การเปลี่ยนแปลงใน Working Directory
- **ใช้เมื่อ**: ต้องการรวม commits หลายอันเป็นอันเดียว

```
Before: A -- B -- C -- D (HEAD)
After:  A -- B (HEAD)
        Changes from C, D are staged
```

#### 2. `git reset --hard <commit>`
- ย้าย HEAD ไปยัง commit ที่ระบุ
- **ลบ** การเปลี่ยนแปลงจาก Staging Area
- **ลบ** การเปลี่ยนแปลงจาก Working Directory
- **ใช้เมื่อ**: ต้องการทิ้งทุกอย่างและกลับไปสถานะก่อนหน้า
- ⚠️ **อันตราย**: การเปลี่ยนแปลงที่ไม่ได้ commit จะหายไปถาวร!

```
Before: A -- B -- C -- D (HEAD)
After:  A -- B (HEAD)
        Changes from C, D are GONE!
```

### การอ้างอิง Commit

```bash
HEAD~1  # 1 commit ก่อนหน้า HEAD
HEAD~2  # 2 commits ก่อนหน้า HEAD
HEAD~n  # n commits ก่อนหน้า HEAD
<commit-hash>  # ใช้ hash โดยตรง เช่น abc1234
```

---

## สถานการณ์จำลองใน MLOps

### 🎭 บทบาทของคุณในสถานการณ์นี้

คุณเป็น **ML Engineer** ในทีม Data Science ของบริษัทแห่งหนึ่ง ได้รับมอบหมายให้พัฒนา **Classification Model** สำหรับทำนายพฤติกรรมลูกค้า โดยใช้ scikit-learn

### 📅 ไทม์ไลน์ของเหตุการณ์

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        📅 TIMELINE OF EVENTS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  วันที่ 1: เริ่มต้นโปรเจค                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  09:00  ✅ สร้างโปรเจคและ initialize Git                                      │
│  10:00  ✅ เขียน config.py กำหนดใช้ RandomForestClassifier                    │
│  11:00  ✅ เขียน prepare_data.py สำหรับเตรียมข้อมูล                            │
│  14:00  ✅ เขียน train.py สำหรับ train model                                  │
│  16:00  ✅ เขียน evaluate.py สำหรับประเมินผล                                  │
│  17:00  ✅ รัน pipeline ครั้งแรก ได้ Accuracy ~92% 🎉                          │
│                                                                              │
│  วันที่ 2: ปัญหาเกิดขึ้น!                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  09:00  🤔 หัวหน้าบอกว่า RandomForest ช้าเกินไป อยากลอง DecisionTree          │
│  10:00  ⚠️ แก้ config.py เปลี่ยนเป็น DecisionTree                             │
│  11:00  ⚠️ แก้ train.py ให้ใช้ DecisionTreeClassifier                         │
│  12:00  ❌ รัน pipeline ใหม่ ได้ Accuracy แค่ ~75% 😱                          │
│  13:00  😰 หัวหน้าบอกว่าผลแย่ลงมาก ต้องกลับไปใช้ RandomForest!                 │
│                                                                              │
│  🆘 ปัญหา: จะย้อนกลับไปใช้ code เดิมได้อย่างไร?                                 │
│  💡 คำตอบ: ใช้ Git Reset!                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🎯 สิ่งที่คุณจะได้เรียนรู้จาก Lab นี้

| ขั้นตอน | สิ่งที่จะทำ | สิ่งที่จะได้เรียนรู้ |
|---------|------------|---------------------|
| Step 0-4 | สร้าง ML Pipeline (Baseline) | การสร้างโปรเจค ML ที่มี version control ที่ดี |
| Step 5 | รัน Pipeline ครั้งแรก | การทดสอบ baseline และบันทึกผลลัพธ์ |
| Step 6 | เปลี่ยน Model (ทำผิดพลาด) | จำลองสถานการณ์ที่ทำผิดพลาดในงานจริง |
| Step 7 | พบว่าผลแย่ลง | เข้าใจความสำคัญของการ track changes |
| วิธีที่ 1 | `git reset --hard` | ย้อนกลับและลบทุกอย่างที่ผิดพลาด |
| วิธีที่ 2 | `git reset --soft` | ย้อนกลับแต่เก็บ code ไว้ศึกษา |

### 🔍 ภาพรวมของ Commits ที่จะเกิดขึ้น

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         📊 COMMIT HISTORY VISUALIZATION                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  หลังจากทำ Step 0-5 (Baseline - ผลดี ✅):                                     │
│                                                                              │
│  [1]──────[2]──────[3]──────[4]──────[5]                                    │
│   │        │        │        │        │                                      │
│   │        │        │        │        └─► "Add evaluation module"            │
│   │        │        │        └──────────► "Add training module (RF)"         │
│   │        │        └───────────────────► "Add data preparation"             │
│   │        └────────────────────────────► "Add config (RandomForest)"        │
│   └─────────────────────────────────────► "Initial commit"                   │
│                                                                              │
│  หลังจากทำ Step 6-7 (เปลี่ยน Model - ผลแย่ ❌):                                │
│                                                                              │
│  [1]──[2]──[3]──[4]──[5]──[6]──[7]                                          │
│                            │    │                                            │
│                            │    └─► "Update train.py to DecisionTree" ❌     │
│                            └──────► "Change config to DecisionTree" ❌       │
│                                                                              │
│  เป้าหมาย: ใช้ Git Reset กลับไปที่ commit [5] ✅                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Lab Exercise

### 📁 โครงสร้างโปรเจค

```
git-reset-mlops-lab/
├── README.md
├── data/
│   └── (จะสร้างจาก code)
├── src/
│   ├── prepare_data.py
│   ├── train.py
│   ├── evaluate.py
│   └── config.py
└── models/
    └── (จะเก็บ model)
```

---

## 🚀 เริ่มต้น Lab

### Step 0: สร้างโฟลเดอร์และ Initialize Git

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- สร้างโครงสร้างโฟลเดอร์สำหรับโปรเจค ML
- Initialize Git repository เพื่อเริ่มติดตามการเปลี่ยนแปลง
- สร้าง commit แรก (Initial commit)

**📝 อธิบาย:**
ทุกโปรเจค ML ที่ดีควรมีโครงสร้างที่ชัดเจน:
- `data/` - เก็บข้อมูล train/test
- `src/` - เก็บ source code
- `models/` - เก็บ trained models

**ขั้นตอนที่ 0.1: ตั้งค่า Git User (สำคัญมาก! ต้องทำก่อน)**

```bash
# ตั้งค่าชื่อและอีเมล (จำเป็นสำหรับการ commit)
git config --global user.email "student@example.com"
git config --global user.name "Student"
```

**💡 อธิบาย:**
- `git config --global user.email` - ตั้งค่าอีเมลที่จะแสดงใน commit
- `git config --global user.name` - ตั้งค่าชื่อที่จะแสดงใน commit
- `--global` หมายถึงใช้กับทุก repository ในเครื่อง
- ⚠️ ถ้าไม่ตั้งค่า Git จะไม่ยอมให้ commit!

**🔍 ตรวจสอบการตั้งค่า:**
```bash
git config --global user.name
git config --global user.email
```

**ขั้นตอนที่ 0.2: สร้างโฟลเดอร์โปรเจค**

```bash
# สร้างโฟลเดอร์โปรเจค
mkdir -p git-reset-mlops-lab/{data,src,models}
cd git-reset-mlops-lab
```

**ขั้นตอนที่ 0.3: Initialize Git Repository**

```bash
# Initialize Git repository
git init
```

**✅ ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in .../git-reset-mlops-lab/.git/
```

**ขั้นตอนที่ 0.4: สร้าง Initial Commit**

```bash
# สร้างไฟล์ README.md
echo "# MLOps Git Reset Lab" > README.md

# เพิ่มไฟล์เข้า staging area
git add README.md

# สร้าง commit แรก
git commit -m "Initial commit"
```

**✅ ผลลัพธ์ที่คาดหวัง:**
```
[main (root-commit) xxxxxxx] Initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

**🔍 ตรวจสอบสถานะ:**
```bash
git log --oneline
# ควรเห็น: xxxxxxx (HEAD -> main) Initial commit
```

---

### Step 1: สร้างไฟล์ Configuration

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- สร้างไฟล์ config.py ที่รวมการตั้งค่าทั้งหมดไว้ที่เดียว
- กำหนดให้ใช้ **RandomForestClassifier** เป็น baseline model
- นี่คือ **"สถานะที่ดี"** ที่เราต้องการกลับมาในภายหลัง

**📝 อธิบาย:**
การแยก configuration ออกจาก code หลักเป็น best practice เพราะ:
- ง่ายต่อการเปลี่ยน hyperparameters
- ไม่ต้องแก้ไขหลายไฟล์เมื่อต้องการปรับค่า
- ติดตามการเปลี่ยนแปลงได้ง่ายด้วย Git

```bash
cat > src/config.py << 'EOF'
"""
Configuration file for ML Pipeline
"""

# Data Configuration
DATA_CONFIG = {
    "n_samples": 1000,
    "n_features": 20,
    "n_classes": 2,
    "test_size": 0.2,
    "random_state": 42
}

# Model Configuration
MODEL_CONFIG = {
    "model_type": "random_forest",  # random_forest, decision_tree, logistic
    "n_estimators": 100,
    "max_depth": 10,
    "random_state": 42
}

# Paths
PATHS = {
    "data_dir": "data",
    "model_dir": "models",
    "train_data": "data/train.csv",
    "test_data": "data/test.csv",
    "model_path": "models/model.pkl"
}
EOF
```

**Commit การเปลี่ยนแปลง:**

```bash
git add src/config.py
git commit -m "Add configuration file with RandomForest settings"
```

**💡 สังเกต:** เราตั้งค่า `model_type: "random_forest"` และ `n_estimators: 100` ซึ่งจะให้ผลลัพธ์ที่ดี

---

### Step 2: สร้างไฟล์เตรียมข้อมูล

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- สร้าง module สำหรับเตรียมข้อมูล (Data Preparation)
- สร้างข้อมูลจำลองด้วย `make_classification`
- แบ่งข้อมูลเป็น train/test sets

**📝 อธิบาย:**
ในโปรเจค ML จริง ขั้นตอนนี้จะเป็นการ:
- โหลดข้อมูลจาก database หรือ file
- ทำ data cleaning และ preprocessing
- แบ่งข้อมูลสำหรับ training และ testing

สำหรับ Lab นี้ เราใช้ `make_classification` เพื่อสร้างข้อมูลจำลองที่มี pattern ชัดเจน

```bash
cat > src/prepare_data.py << 'EOF'
"""
Data Preparation Module
สร้างและเตรียมข้อมูลสำหรับ training และ testing
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import os

# Import configuration
import sys
sys.path.append('src')
from config import DATA_CONFIG, PATHS


def generate_data():
    """สร้างข้อมูลจำลองสำหรับ classification"""
    print("=" * 50)
    print("📊 Generating synthetic data...")
    print("=" * 50)
    
    X, y = make_classification(
        n_samples=DATA_CONFIG["n_samples"],
        n_features=DATA_CONFIG["n_features"],
        n_informative=15,
        n_redundant=5,
        n_classes=DATA_CONFIG["n_classes"],
        random_state=DATA_CONFIG["random_state"]
    )
    
    # สร้าง DataFrame
    feature_names = [f"feature_{i}" for i in range(DATA_CONFIG["n_features"])]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y
    
    print(f"✅ Generated {len(df)} samples with {DATA_CONFIG['n_features']} features")
    return df


def split_data(df):
    """แบ่งข้อมูลเป็น train และ test sets"""
    print("\n📂 Splitting data into train/test sets...")
    
    X = df.drop("target", axis=1)
    y = df["target"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=DATA_CONFIG["test_size"],
        random_state=DATA_CONFIG["random_state"],
        stratify=y
    )
    
    # รวมกลับเป็น DataFrame
    train_df = pd.concat([X_train.reset_index(drop=True), 
                          y_train.reset_index(drop=True).rename("target")], axis=1)
    test_df = pd.concat([X_test.reset_index(drop=True), 
                         y_test.reset_index(drop=True).rename("target")], axis=1)
    
    print(f"✅ Train set: {len(train_df)} samples")
    print(f"✅ Test set: {len(test_df)} samples")
    
    return train_df, test_df


def save_data(train_df, test_df):
    """บันทึกข้อมูลลงไฟล์"""
    print("\n💾 Saving data to files...")
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs(PATHS["data_dir"], exist_ok=True)
    
    train_df.to_csv(PATHS["train_data"], index=False)
    test_df.to_csv(PATHS["test_data"], index=False)
    
    print(f"✅ Saved train data to: {PATHS['train_data']}")
    print(f"✅ Saved test data to: {PATHS['test_data']}")


def main():
    """Main function สำหรับ data preparation"""
    print("\n" + "🚀 DATA PREPARATION PIPELINE 🚀".center(50))
    print("=" * 50)
    
    # Generate data
    df = generate_data()
    
    # Split data
    train_df, test_df = split_data(df)
    
    # Save data
    save_data(train_df, test_df)
    
    print("\n" + "=" * 50)
    print("✨ Data preparation completed successfully! ✨")
    print("=" * 50)


if __name__ == "__main__":
    main()
EOF
```

**Commit การเปลี่ยนแปลง:**

```bash
git add src/prepare_data.py
git commit -m "Add data preparation module"
```

**✅ ผลลัพธ์ที่คาดหวัง:**
```
[main xxxxxxx] Add data preparation module
 1 file changed, XX insertions(+)
 create mode 100644 src/prepare_data.py
```

---

### Step 3: สร้างไฟล์ Training (Version 1 - RandomForest) ⭐

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- สร้าง module สำหรับ train model
- ใช้ **RandomForestClassifier** ซึ่งเป็น model ที่ดี
- นี่คือ **"Version ที่ถูกต้อง"** ที่เราต้องการเก็บไว้

**📝 อธิบาย:**
RandomForestClassifier เป็น ensemble method ที่รวม Decision Trees หลายต้นเข้าด้วยกัน:
- ให้ผลลัพธ์ที่ดีกว่า Decision Tree เดี่ยว
- มีความ robust ต่อ overfitting
- เหมาะกับข้อมูลที่มีหลาย features

**⚠️ สำคัญ:** จำไว้ว่านี่คือ version ที่ดี ในขั้นตอนถัดไปเราจะเปลี่ยนไปใช้ model อื่นที่แย่กว่า

```bash
cat > src/train.py << 'EOF'
"""
Model Training Module - Version 1
ใช้ RandomForestClassifier
"""

import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier

# Import configuration
import sys
sys.path.append('src')
from config import MODEL_CONFIG, PATHS


def load_train_data():
    """โหลดข้อมูล training"""
    print("📂 Loading training data...")
    train_df = pd.read_csv(PATHS["train_data"])
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]
    print(f"✅ Loaded {len(X_train)} training samples")
    return X_train, y_train


def create_model():
    """สร้าง model ตาม configuration"""
    print(f"\n🔧 Creating model: RandomForestClassifier")
    
    model = RandomForestClassifier(
        n_estimators=MODEL_CONFIG["n_estimators"],
        max_depth=MODEL_CONFIG["max_depth"],
        random_state=MODEL_CONFIG["random_state"],
        n_jobs=-1
    )
    
    print(f"   - n_estimators: {MODEL_CONFIG['n_estimators']}")
    print(f"   - max_depth: {MODEL_CONFIG['max_depth']}")
    
    return model


def train_model(model, X_train, y_train):
    """Train model"""
    print("\n🏋️ Training model...")
    model.fit(X_train, y_train)
    print("✅ Training completed!")
    return model


def save_model(model):
    """บันทึก model"""
    print("\n💾 Saving model...")
    os.makedirs(PATHS["model_dir"], exist_ok=True)
    
    with open(PATHS["model_path"], "wb") as f:
        pickle.dump(model, f)
    
    print(f"✅ Model saved to: {PATHS['model_path']}")


def main():
    """Main training pipeline"""
    print("\n" + "🚀 MODEL TRAINING PIPELINE 🚀".center(50))
    print("=" * 50)
    
    # Load data
    X_train, y_train = load_train_data()
    
    # Create model
    model = create_model()
    
    # Train model
    model = train_model(model, X_train, y_train)
    
    # Save model
    save_model(model)
    
    print("\n" + "=" * 50)
    print("✨ Training completed successfully! ✨")
    print("=" * 50)


if __name__ == "__main__":
    main()
EOF
```

**Commit การเปลี่ยนแปลง:**

```bash
git add src/train.py
git commit -m "Add training module with RandomForest"
```

**💡 สังเกต:** ใน commit message เราระบุชัดเจนว่าใช้ "RandomForest" เพื่อให้ดู history ได้ง่าย

---

### Step 4: สร้างไฟล์ Evaluation

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- สร้าง module สำหรับประเมินผล model
- คำนวณ metrics ต่างๆ เช่น Accuracy, Precision, Recall, F1-Score
- แสดง Confusion Matrix และ Classification Report

**📝 อธิบาย:**
การประเมินผล model เป็นขั้นตอนสำคัญใน ML pipeline:
- **Accuracy**: สัดส่วนที่ทำนายถูกทั้งหมด
- **Precision**: ความแม่นยำเมื่อทำนายว่าเป็น positive
- **Recall**: ความสามารถในการหา positive ทั้งหมด
- **F1-Score**: ค่าเฉลี่ยแบบ harmonic ของ Precision และ Recall

```bash
cat > src/evaluate.py << 'EOF'
"""
Model Evaluation Module
ประเมินผล model ด้วย metrics ต่างๆ
"""

import pandas as pd
import pickle
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    classification_report,
    confusion_matrix
)
import numpy as np

# Import configuration
import sys
sys.path.append('src')
from config import PATHS


def load_test_data():
    """โหลดข้อมูล test"""
    print("📂 Loading test data...")
    test_df = pd.read_csv(PATHS["test_data"])
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]
    print(f"✅ Loaded {len(X_test)} test samples")
    return X_test, y_test


def load_model():
    """โหลด trained model"""
    print("📂 Loading model...")
    with open(PATHS["model_path"], "rb") as f:
        model = pickle.load(f)
    print(f"✅ Model loaded: {type(model).__name__}")
    return model


def evaluate_model(model, X_test, y_test):
    """ประเมินผล model"""
    print("\n📊 Evaluating model...")
    print("=" * 50)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, average='weighted'),
        "Recall": recall_score(y_test, y_pred, average='weighted'),
        "F1-Score": f1_score(y_test, y_pred, average='weighted')
    }
    
    # Print metrics
    print("\n📈 EVALUATION METRICS:")
    print("-" * 30)
    for metric, value in metrics.items():
        print(f"   {metric}: {value:.4f}")
    
    # Confusion Matrix
    print("\n📋 CONFUSION MATRIX:")
    print("-" * 30)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Classification Report
    print("\n📑 CLASSIFICATION REPORT:")
    print("-" * 30)
    print(classification_report(y_test, y_pred))
    
    return metrics


def main():
    """Main evaluation pipeline"""
    print("\n" + "🚀 MODEL EVALUATION PIPELINE 🚀".center(50))
    print("=" * 50)
    
    # Load test data
    X_test, y_test = load_test_data()
    
    # Load model
    model = load_model()
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    print("\n" + "=" * 50)
    print("✨ Evaluation completed! ✨")
    print("=" * 50)
    
    return metrics


if __name__ == "__main__":
    main()
EOF
```

**Commit การเปลี่ยนแปลง:**

```bash
git add src/evaluate.py
git commit -m "Add evaluation module"
```

**✅ ตอนนี้เรามี 5 commits แล้ว:**
```
[5] Add evaluation module           <-- HEAD อยู่ตรงนี้
[4] Add training module with RandomForest
[3] Add data preparation module
[2] Add configuration file with RandomForest settings
[1] Initial commit
```

---

### Step 5: รัน Pipeline ครั้งแรก (Baseline) ✅

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- รัน ML pipeline ทั้งหมดเพื่อสร้าง baseline
- บันทึกผลลัพธ์ Accuracy ไว้เปรียบเทียบ
- ตรวจสอบ Git history

**📝 อธิบาย:**
ขั้นตอนนี้เป็นการรัน pipeline ด้วย **RandomForestClassifier** ซึ่งควรให้ผลลัพธ์ที่ดี (Accuracy ประมาณ 90-95%)

ผลลัพธ์นี้จะเป็น **Baseline** ที่เราจะใช้เปรียบเทียบเมื่อเปลี่ยน model

```bash
# รัน data preparation
python src/prepare_data.py

# รัน training
python src/train.py

# รัน evaluation
python src/evaluate.py
```

**✅ ผลลัพธ์ที่คาดหวัง:**
```
📈 EVALUATION METRICS:
------------------------------
   Accuracy: 0.9200  <-- ประมาณ 90-95%
   Precision: 0.9205
   Recall: 0.9200
   F1-Score: 0.9199
```

**📝 บันทึกผล Baseline:**

| Metric | ค่าที่ได้ (กรอกเอง) |
|--------|---------------------|
| Accuracy | _____________ |
| Model | RandomForestClassifier |

**ตรวจสอบ Git Log:**

```bash
git log --oneline
```

ผลลัพธ์ควรจะเป็น:

```
abc1234 (HEAD -> main) Add evaluation module
def5678 Add training module with RandomForest
ghi9012 Add data preparation module
jkl3456 Add configuration file with RandomForest settings
mno7890 Initial commit
```

**💡 จุดสำคัญ:**
- Commit `def5678` (Add training module with RandomForest) คือจุดที่เราต้องการกลับมา
- บันทึก commit hash ไว้ใช้ในขั้นตอนถัดไป

---

## 🔴 สถานการณ์ปัญหา: เปลี่ยนไปใช้ DecisionTree แล้วผลแย่ลง

### Step 6: ทีมตัดสินใจเปลี่ยน Model เป็น DecisionTree ❌

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- จำลองสถานการณ์ที่ทีมตัดสินใจเปลี่ยน model
- เรียนรู้ว่าการเปลี่ยนแปลงบางอย่างอาจทำให้ผลแย่ลง
- สร้าง commits ที่เราต้องการ "undo" ในภายหลัง

**📝 สถานการณ์:**
หัวหน้าทีมบอกว่า:
> "RandomForest ช้าเกินไป ลองเปลี่ยนเป็น DecisionTree ดูสิ มันเร็วกว่าเยอะ"

คุณจึงทำตาม โดยเปลี่ยน:
1. `config.py` - เปลี่ยน model_type เป็น decision_tree
2. `train.py` - เปลี่ยนจาก RandomForestClassifier เป็น DecisionTreeClassifier

**⚠️ ข้อผิดพลาดที่จะเกิด:**
- DecisionTree เดี่ยวมักจะ overfit หรือ underfit
- `max_depth=3` น้อยเกินไป ทำให้ model เรียนรู้ได้ไม่ดี
- ผลลัพธ์จะแย่กว่า RandomForest มาก

**เปลี่ยน config:**

```bash
cat > src/config.py << 'EOF'
"""
Configuration file for ML Pipeline
เปลี่ยนเป็น Decision Tree เพื่อลดความซับซ้อน
"""

# Data Configuration
DATA_CONFIG = {
    "n_samples": 1000,
    "n_features": 20,
    "n_classes": 2,
    "test_size": 0.2,
    "random_state": 42
}

# Model Configuration - CHANGED TO DECISION TREE
MODEL_CONFIG = {
    "model_type": "decision_tree",
    "max_depth": 3,  # ลด max_depth มาก
    "random_state": 42
}

# Paths
PATHS = {
    "data_dir": "data",
    "model_dir": "models",
    "train_data": "data/train.csv",
    "test_data": "data/test.csv",
    "model_path": "models/model.pkl"
}
EOF
```

```bash
git add src/config.py
git commit -m "Change model to DecisionTree for simplicity"
```

**💡 สังเกต:** นี่คือ commit ที่ 6 - commit แรกที่ "ผิดพลาด"

**เปลี่ยน train.py:**

```bash
cat > src/train.py << 'EOF'
"""
Model Training Module - Version 2
เปลี่ยนเป็น DecisionTreeClassifier (BAD DECISION!)
"""

import pandas as pd
import pickle
import os
from sklearn.tree import DecisionTreeClassifier

# Import configuration
import sys
sys.path.append('src')
from config import MODEL_CONFIG, PATHS


def load_train_data():
    """โหลดข้อมูล training"""
    print("📂 Loading training data...")
    train_df = pd.read_csv(PATHS["train_data"])
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]
    print(f"✅ Loaded {len(X_train)} training samples")
    return X_train, y_train


def create_model():
    """สร้าง model - DecisionTree"""
    print(f"\n🔧 Creating model: DecisionTreeClassifier")
    
    model = DecisionTreeClassifier(
        max_depth=MODEL_CONFIG["max_depth"],
        random_state=MODEL_CONFIG["random_state"]
    )
    
    print(f"   - max_depth: {MODEL_CONFIG['max_depth']}")
    
    return model


def train_model(model, X_train, y_train):
    """Train model"""
    print("\n🏋️ Training model...")
    model.fit(X_train, y_train)
    print("✅ Training completed!")
    return model


def save_model(model):
    """บันทึก model"""
    print("\n💾 Saving model...")
    os.makedirs(PATHS["model_dir"], exist_ok=True)
    
    with open(PATHS["model_path"], "wb") as f:
        pickle.dump(model, f)
    
    print(f"✅ Model saved to: {PATHS['model_path']}")


def main():
    """Main training pipeline"""
    print("\n" + "🚀 MODEL TRAINING PIPELINE 🚀".center(50))
    print("=" * 50)
    
    # Load data
    X_train, y_train = load_train_data()
    
    # Create model
    model = create_model()
    
    # Train model
    model = train_model(model, X_train, y_train)
    
    # Save model
    save_model(model)
    
    print("\n" + "=" * 50)
    print("✨ Training completed successfully! ✨")
    print("=" * 50)


if __name__ == "__main__":
    main()
EOF
```

```bash
git add src/train.py
git commit -m "Update train.py to use DecisionTree"
```

**💡 สังเกต:** นี่คือ commit ที่ 7 - commit ที่สองที่ "ผิดพลาด"

**📊 สถานะ Git ตอนนี้:**
```
[7] Update train.py to use DecisionTree      <-- HEAD อยู่ตรงนี้ ❌
[6] Change model to DecisionTree for simplicity  ❌
[5] Add evaluation module                     ✅
[4] Add training module with RandomForest     ✅ <-- เป้าหมาย: กลับไปจุดนี้
[3] Add data preparation module               ✅
[2] Add configuration file with RandomForest  ✅
[1] Initial commit                            ✅
```

---

### Step 7: รัน Pipeline ใหม่และพบปัญหา 😱

**🎯 วัตถุประสงค์ของขั้นตอนนี้:**
- รัน pipeline ด้วย DecisionTree และเปรียบเทียบกับ Baseline
- เห็นว่าผลลัพธ์แย่ลงจริง
- เข้าใจความจำเป็นที่ต้องย้อนกลับ

**📝 อธิบาย:**
เราจะรัน pipeline อีกครั้งและเปรียบเทียบผลลัพธ์:
- **Baseline (RandomForest)**: Accuracy ~92%
- **หลังเปลี่ยน (DecisionTree)**: Accuracy ~75%

ผลต่าง **17%** ถือว่าแย่ลงมาก! หัวหน้าจึงสั่งให้กลับไปใช้ RandomForest

```bash
# รัน training ใหม่
python src/train.py

# รัน evaluation
python src/evaluate.py
```

**❌ ผลลัพธ์ที่คาดหวัง (แย่กว่าเดิม):**
```
📈 EVALUATION METRICS:
------------------------------
   Accuracy: 0.7500  <-- ลดลงมาก! 😱
   Precision: 0.7520
   Recall: 0.7500
   F1-Score: 0.7480
```

**📝 เปรียบเทียบผลลัพธ์:**

| Metric | Baseline (RF) | หลังเปลี่ยน (DT) | ผลต่าง |
|--------|---------------|-----------------|--------|
| Accuracy | ~0.92 | ~0.75 | -17% 📉 |
| Model | RandomForest | DecisionTree | |

**ดู Git Log ปัจจุบัน:**

```bash
git log --oneline
```

```
xyz9999 (HEAD -> main) Update train.py to use DecisionTree     ❌ ลบอันนี้
uvw8888 Change model to DecisionTree for simplicity            ❌ ลบอันนี้
abc1234 Add evaluation module
def5678 Add training module with RandomForest  <-- ต้องการกลับไปจุดนี้ ✅
ghi9012 Add data preparation module
jkl3456 Add configuration file with RandomForest settings
mno7890 Initial commit
```

**🆘 ปัญหา:**
- เรามี 2 commits ที่ผิดพลาด (commit 6 และ 7)
- ต้องการย้อนกลับไป commit 5 (หรือ HEAD~2)
- เราจะใช้ Git Reset!

---

## 🛠️ การแก้ปัญหาด้วย Git Reset

ตอนนี้เราต้องการย้อนกลับไปใช้ RandomForest มี 2 วิธีหลัก:
1. **`git reset --hard`**: ลบทุกอย่างและกลับไปสถานะเดิม
2. **`git reset --soft`**: กลับไปสถานะเดิมแต่เก็บ code ไว้ศึกษา

---

### วิธีที่ 1: ใช้ `git reset --hard` (ทิ้งการเปลี่ยนแปลงทั้งหมด) 🔴

**🎯 วัตถุประสงค์:**
- ย้อนกลับไปสถานะก่อนหน้าทั้งหมด
- ลบ commits ที่ผิดพลาดออก
- **ลบ** การเปลี่ยนแปลงใน Working Directory ด้วย

**📝 อธิบาย:**
`git reset --hard` เป็นคำสั่งที่ "รุนแรง" ที่สุด:
- ย้าย HEAD ไปยัง commit ที่ระบุ
- ลบทุกอย่างใน Staging Area
- ลบทุกอย่างใน Working Directory
- **การเปลี่ยนแปลงที่ไม่ได้ commit จะหายไปถาวร!**

**⚠️ คำเตือน:** วิธีนี้จะลบการเปลี่ยนแปลงถาวร! ใช้เมื่อแน่ใจว่าไม่ต้องการ code เดิมแล้ว

```
ก่อนใช้ --hard:
┌─────────────────────────────────────────────────────────────────┐
│  [1]──[2]──[3]──[4]──[5]──[6]──[7]                              │
│                            │    │                                │
│                            │    └─► DecisionTree train.py ❌     │
│                            └──────► DecisionTree config ❌       │
│                       │                                          │
│                       └──► HEAD อยู่ตรงนี้                        │
└─────────────────────────────────────────────────────────────────┘

หลังใช้ --hard HEAD~2:
┌─────────────────────────────────────────────────────────────────┐
│  [1]──[2]──[3]──[4]──[5]                                        │
│                       │                                          │
│                       └──► HEAD ย้ายมาอยู่ตรงนี้ ✅               │
│                                                                  │
│  Commits [6] และ [7] หายไป! 🗑️                                  │
│  Working Directory กลับเป็น RandomForest ✅                      │
└─────────────────────────────────────────────────────────────────┘
```

```bash
# ดู commit ที่ต้องการกลับไป
git log --oneline

# Reset กลับไป 2 commits (กลับไปก่อนที่จะเปลี่ยนเป็น DecisionTree)
git reset --hard HEAD~2

# หรือใช้ commit hash
# git reset --hard def5678
```

**✅ ผลลัพธ์ที่คาดหวัง:**
```
HEAD is now at abc1234 Add evaluation module
```

**ตรวจสอบผลลัพธ์:**

```bash
# ดู log - ควรเหลือแค่ 5 commits
git log --oneline

# ดู content ของ train.py (ควรกลับมาเป็น RandomForest)
cat src/train.py

# ดู content ของ config.py (ควรกลับมาเป็น RandomForest)
cat src/config.py
```

**📝 สิ่งที่ควรเห็น:**
- `git log` แสดงแค่ 5 commits (ไม่มี DecisionTree commits)
- `src/train.py` มี `RandomForestClassifier`
- `src/config.py` มี `model_type: "random_forest"`

**รัน Pipeline อีกครั้งเพื่อยืนยัน:**

```bash
python src/train.py
python src/evaluate.py
```

**✅ ผลลัพธ์ควรกลับมาดีเหมือนเดิม:**
```
📈 EVALUATION METRICS:
------------------------------
   Accuracy: 0.9200  <-- กลับมา ~92% แล้ว! 🎉
```

**📝 บันทึกผล:**

| สถานะ | Accuracy | คำสั่งที่ใช้ |
|-------|----------|-------------|
| Baseline | ~0.92 | - |
| หลังเปลี่ยน DT | ~0.75 | - |
| หลัง reset --hard | ~0.92 ✅ | `git reset --hard HEAD~2` |

---

### วิธีที่ 2: ใช้ `git reset --soft` (เก็บการเปลี่ยนแปลงไว้ใน staging) 🟡

**🎯 วัตถุประสงค์:**
- ย้อนกลับไปสถานะก่อนหน้า
- **เก็บ** การเปลี่ยนแปลงไว้ใน Staging Area
- สามารถดู code เดิมได้ก่อนตัดสินใจ

**📝 อธิบาย:**
`git reset --soft` เป็นคำสั่งที่ "อ่อนโยน" กว่า:
- ย้าย HEAD ไปยัง commit ที่ระบุ
- **เก็บ** ทุกอย่างใน Staging Area
- **เก็บ** ทุกอย่างใน Working Directory
- สามารถ commit ใหม่ได้ทันที หรือแก้ไขก่อนก็ได้

**✅ เหมาะเมื่อ:**
- ต้องการรวม commits หลายอันเป็นอันเดียว
- ต้องการเก็บ code ไว้ศึกษาก่อนลบ
- ต้องการแก้ไข commit message

```
ก่อนใช้ --soft:
┌─────────────────────────────────────────────────────────────────┐
│  [1]──[2]──[3]──[4]──[5]──[6]──[7]                              │
│                                   │                              │
│                                   └─► HEAD อยู่ตรงนี้            │
└─────────────────────────────────────────────────────────────────┘

หลังใช้ --soft HEAD~2:
┌─────────────────────────────────────────────────────────────────┐
│  [1]──[2]──[3]──[4]──[5]                                        │
│                       │                                          │
│                       └──► HEAD ย้ายมาอยู่ตรงนี้                 │
│                                                                  │
│  📦 Staging Area:                                                │
│  ├── modified: src/config.py (DecisionTree changes)             │
│  └── modified: src/train.py (DecisionTree changes)              │
│                                                                  │
│  💡 การเปลี่ยนแปลงยังอยู่! พร้อม commit ใหม่ได้                   │
└─────────────────────────────────────────────────────────────────┘
```

**⚠️ ก่อนทดลอง:** ให้ทำซ้ำ Step 6 อีกครั้งเพื่อสร้างสถานการณ์ใหม่ (ถ้าทำ --hard ไปแล้ว)

```bash
# ทำซ้ำ Step 6 ถ้าจำเป็น (สร้าง commits ที่ผิดพลาดใหม่)
# ... (ทำตาม Step 6)

# ใช้ reset --soft
git reset --soft HEAD~2
```

**ตรวจสอบสถานะ:**

```bash
git status
```

**✅ ผลลัพธ์ที่คาดหวัง:**

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/config.py
        modified:   src/train.py
```

**📝 สังเกต:**
- การเปลี่ยนแปลงยังอยู่ใน "Changes to be committed" (Staging Area)
- ไฟล์ยังเป็น DecisionTree อยู่!
- แต่ HEAD ย้ายกลับไปแล้ว

**🔍 ดูความแตกต่าง:**

```bash
# ดูว่ามีอะไรอยู่ใน staging
git diff --staged
```

จะเห็นการเปลี่ยนแปลงจาก RandomForest เป็น DecisionTree

**ทางเลือกหลังจากใช้ --soft:**

| ทางเลือก | คำสั่ง | ผลลัพธ์ |
|---------|--------|---------|
| Commit ใหม่ | `git commit -m "..."` | รวม changes เป็น 1 commit |
| Unstage ทั้งหมด | `git restore --staged .` | ย้ายไป working dir |
| ยกเลิก changes | `git restore --staged . && git restore .` | กลับไปเป็น RF |

**ตัวอย่าง: ยกเลิกการเปลี่ยนแปลงทั้งหมด**

```bash
# Unstage ไฟล์
git restore --staged .

# ยกเลิก changes ใน working directory
git restore .

# ตรวจสอบ - ควรกลับเป็น RandomForest
cat src/train.py
```

---

## 📝 แบบฝึกหัดเพิ่มเติม

### แบบฝึกหัด 1: ใช้ `git reflog` เพื่อกู้คืน 🆘

**สถานการณ์:** คุณทำ `git reset --hard` ไปแล้ว แต่ตระหนักว่าต้องการ code ที่ลบไป!

**📝 อธิบาย:**
`git reflog` เก็บประวัติการเคลื่อนไหวของ HEAD ทั้งหมด แม้ว่า commits จะถูก reset ไปแล้วก็ยังกู้คืนได้ (ภายใน 30 วัน)

```bash
# ดู reflog (บันทึกการเคลื่อนไหวของ HEAD)
git reflog
```

**ผลลัพธ์ตัวอย่าง:**
```
abc1234 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
xyz9999 HEAD@{1}: commit: Update train.py to use DecisionTree
uvw8888 HEAD@{2}: commit: Change model to DecisionTree for simplicity
abc1234 HEAD@{3}: commit: Add evaluation module
```

**กู้คืน:**
```bash
# กลับไปยัง commit ที่ต้องการ (DecisionTree version)
git reset --hard xyz9999

# หรือใช้ reflog reference
git reset --hard HEAD@{1}
```

**💡 สรุป:** `git reflog` เป็น "safety net" ที่ช่วยกู้คืนงานที่หายไปจาก `reset --hard`

---

### แบบฝึกหัด 2: รวม Commits ด้วย Reset --soft (Squash) 📦

**สถานการณ์:** คุณมี commits เล็กๆ หลายอันที่อยากรวมเป็น commit เดียว

```
ก่อน squash:
abc1234 Fix typo in train.py
def5678 Add comment in train.py  
ghi9012 Update train.py formatting
jkl3456 Actual training code change
```

**ขั้นตอน:**
```bash
# Reset --soft กลับไป 4 commits แต่เก็บ changes ไว้
git reset --soft HEAD~4

# Commit ใหม่เป็น 1 commit
git commit -m "Update training module with improvements"
```

**หลัง squash:**
```
mno7890 Update training module with improvements  <-- รวมเป็น 1 commit!
```

**💡 ประโยชน์:**
- History สะอาดขึ้น
- ง่ายต่อการ review
- ง่ายต่อการ revert ถ้าจำเป็น

---

### แบบฝึกหัด 3: ทดลองด้วยตัวเอง 🧪

ลองทำตามขั้นตอนต่อไปนี้:

1. สร้าง 3 commits ใหม่ (เช่น แก้ไข config.py 3 ครั้ง)
2. ใช้ `git reset --soft HEAD~3` เพื่อรวมเป็น 1 commit
3. ใช้ `git reset --hard HEAD~1` เพื่อลบ commit นั้น
4. ใช้ `git reflog` และ `git reset --hard <hash>` เพื่อกู้คืน

**📝 บันทึกผลการทดลอง:**

| ขั้นตอน | คำสั่งที่ใช้ | ผลลัพธ์ |
|---------|-------------|---------|
| 1 | git commit (x3) | |
| 2 | git reset --soft HEAD~3 | |
| 3 | git reset --hard HEAD~1 | |
| 4 | git reflog + git reset | |

---

## 🔍 เปรียบเทียบ `--soft` vs `--hard`

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPARISON: --soft vs --hard                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  git reset --soft HEAD~2                git reset --hard HEAD~2             │
│  ─────────────────────────              ─────────────────────────            │
│                                                                              │
│  ┌──────────────┐                       ┌──────────────┐                    │
│  │ HEAD moved ✓ │                       │ HEAD moved ✓ │                    │
│  └──────────────┘                       └──────────────┘                    │
│  ┌──────────────┐                       ┌──────────────┐                    │
│  │ Staging: KEEP│                       │ Staging: GONE│                    │
│  └──────────────┘                       └──────────────┘                    │
│  ┌──────────────┐                       ┌──────────────┐                    │
│  │ Working: KEEP│                       │ Working: GONE│                    │
│  └──────────────┘                       └──────────────┘                    │
│                                                                              │
│  ✅ ปลอดภัย                              ⚠️ อันตราย                          │
│  📁 เก็บ code ไว้                        🗑️ ลบทุกอย่าง                       │
│  🔄 สามารถ commit ใหม่                   ❌ กู้คืนยาก                         │
│                                                                              │
│  Use Case:                              Use Case:                            │
│  - รวม commits                          - ทิ้งงานที่ผิดพลาด                   │
│  - แก้ commit message                   - กลับไปสถานะเดิมทั้งหมด              │
│  - ศึกษา code ก่อนลบ                    - ล้าง history                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

| คำสั่ง | ผลลัพธ์ | Use Case |
|--------|---------|----------|
| `git reset --hard` | ลบทุกอย่าง กลับไป commit เดิม | ต้องการทิ้งการเปลี่ยนแปลงทั้งหมด |
| `git reset --soft` | เก็บ changes ไว้ใน staging | รวม commits / แก้ commit message |
| `git revert` | สร้าง commit ใหม่ที่ undo | ปลอดภัยกว่า ใช้กับ shared branches |
| `git checkout` | ย้ายไปดู commit อื่น | ดู code เก่าโดยไม่เปลี่ยน branch |

---

## 🎯 Best Practices สำหรับ MLOps

1. **Commit บ่อยๆ และมีความหมาย**: แต่ละ commit ควรทำสิ่งเดียว
2. **ใช้ branch สำหรับ experiments**: ไม่ควรทดลองบน main/master
3. **เขียน commit message ที่ดี**: บอกว่าทำอะไร และทำไม
4. **ระวังการใช้ `--hard`**: ควรมั่นใจก่อนใช้
5. **ใช้ `git reflog`**: เป็น safety net ถ้าทำผิด
6. **Track experiments**: ใช้ MLflow หรือ DVC ร่วมกับ Git

---

## 📚 คำถามทบทวน

1. `git reset --soft` ต่างจาก `git reset --hard` อย่างไร?
2. `HEAD~3` หมายถึงอะไร?
3. ทำไมควรระวังการใช้ `git reset --hard` บน shared branches?
4. ถ้าทำ `git reset --hard` ผิดพลาดไป จะกู้คืนได้อย่างไร?
5. เมื่อไหร่ควรใช้ `git reset --soft` แทน `git reset --hard`?

---

## สรุป

Git Reset เป็นเครื่องมือที่ทรงพลังสำหรับการจัดการ version control ใน MLOps:

- **`--soft`**: ย้าย HEAD, เก็บ staging และ working directory ไว้
- **`--hard`**: ย้าย HEAD, reset ทุกอย่าง (⚠️ อันตราย)

ใน MLOps การใช้ Git Reset ช่วยให้เราสามารถ:
- ย้อนกลับไปใช้ model version ที่ดีกว่า
- แก้ไขการ commit ที่ผิดพลาด
- จัดระเบียบ commit history

---

## 📖 อ้างอิง

- [Git Reset Documentation](https://git-scm.com/docs/git-reset)
- [Atlassian Git Reset Tutorial](https://www.atlassian.com/git/tutorials/undoing-changes/git-reset)
- [MLOps Best Practices](https://ml-ops.org/)

---

