# 🔄 Lab: Git Restore ใน MLOps Application

## 📚 ภาพรวมของ Lab

Lab นี้จะสอนการใช้คำสั่ง `git restore` ในบริบทของการพัฒนา Machine Learning Pipeline โดยจำลองสถานการณ์จริงที่เกิดขึ้นระหว่างการทำงาน เช่น การแก้ไขโค้ดผิดพลาด การทดลองที่ไม่สำเร็จ และการต้องการย้อนกลับไปใช้เวอร์ชันก่อนหน้า

---

## 🎯 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. เข้าใจแนวคิดและความสำคัญของ `git restore` ใน MLOps workflow
2. ใช้ `git restore` เพื่อยกเลิกการเปลี่ยนแปลงไฟล์ใน Working Directory
3. ใช้ `git restore --staged` เพื่อยกเลิกไฟล์ที่อยู่ใน Staging Area
4. ใช้ `git restore --source` เพื่อกู้คืนไฟล์จาก commit เฉพาะ
5. ประยุกต์ใช้ `git restore` ในสถานการณ์จริงของการพัฒนา ML Pipeline

---

## 📖 ทฤษฎี: Git Restore คืออะไร?

### 🔑 แนวคิดหลัก

ลองนึกภาพว่าคุณกำลังเขียนรายงานด้วย Microsoft Word ถ้าคุณพิมพ์ผิดหรือลบข้อความไปโดยไม่ตั้งใจ คุณจะกด **Ctrl+Z** เพื่อย้อนกลับ ใช่ไหม?

`git restore` ก็ทำหน้าที่คล้ายๆ กัน แต่ทรงพลังกว่ามาก เพราะมันสามารถย้อนกลับไปหาเวอร์ชันใดก็ได้ในประวัติการทำงานของคุณ ไม่ใช่แค่ขั้นตอนก่อนหน้า

### 📜 ความเป็นมา

ก่อนหน้านี้ Git ใช้คำสั่ง `git checkout` ทำหลายอย่างพร้อมกัน ทั้งสลับ branch และกู้คืนไฟล์ ซึ่งทำให้สับสน ในเดือนสิงหาคม 2019 (Git 2.23) จึงแยกออกมาเป็น 2 คำสั่งที่ชัดเจน:

| คำสั่งเดิม | คำสั่งใหม่ | หน้าที่ |
|-----------|-----------|---------|
| `git checkout <branch>` | `git switch <branch>` | สลับ branch |
| `git checkout -- <file>` | `git restore <file>` | กู้คืนไฟล์ |

### 🏠 ทำความเข้าใจ "บ้าน" ของ Git (Git Areas)

ก่อนจะใช้ `git restore` ได้อย่างมั่นใจ คุณต้องเข้าใจว่า Git แบ่งพื้นที่ทำงานออกเป็น 3 ส่วน เปรียบเหมือน "บ้าน" ที่มี 3 ห้อง:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      🏠 บ้านของ Git (Git Areas)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐ │
│  │  🛠️ ห้องทำงาน      │   │  📦 ห้องจัดเตรียม   │   │  🏛️ ห้องเก็บของถาวร │ │
│  │  (Working         │   │  (Staging Area    │   │  (Repository)     │ │
│  │   Directory)      │   │   / Index)        │   │                   │ │
│  │                   │   │                   │   │                   │ │
│  │  • ไฟล์ที่คุณ      │   │  • ไฟล์ที่เลือกแล้ว │   │  • ประวัติที่บันทึก  │ │
│  │    กำลังแก้ไข      │   │    ว่าจะ commit   │   │    ถาวรแล้ว        │ │
│  │  • ยังไม่ได้เลือก   │   │  • รอการ commit   │   │  • กู้คืนได้เสมอ    │ │
│  │    ว่าจะเก็บ       │   │                   │   │                   │ │
│  └───────────────────┘   └───────────────────┘   └───────────────────┘ │
│           │                       │                       │            │
│           │    git add ───────▶   │    git commit ─────▶  │            │
│           │                       │                       │            │
│           │   ◀─── git restore    │  ◀── git restore      │            │
│           │        --staged       │      --source         │            │
│           │                       │                       │            │
│           └───────────────────────┴───────────────────────┘            │
│                            ▲                                           │
│                            │                                           │
│                   git restore (กู้คืนจาก commit ล่าสุด)                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**อธิบายแต่ละห้อง:**

| ห้อง | ชื่อภาษาอังกฤษ | คำอธิบาย | เปรียบเทียบ |
|------|---------------|----------|------------|
| 🛠️ ห้องทำงาน | Working Directory | ไฟล์ที่คุณเห็นและแก้ไขได้ในโฟลเดอร์โปรเจกต์ | โต๊ะทำงานที่มีเอกสารกระจัดกระจาย |
| 📦 ห้องจัดเตรียม | Staging Area (Index) | ไฟล์ที่คุณเลือกแล้วว่าจะ commit ในรอบถัดไป | กล่องที่ใส่เอกสารที่จัดเรียบร้อยแล้ว รอส่งไปเก็บ |
| 🏛️ ห้องเก็บของถาวร | Repository | ประวัติ commit ทั้งหมด เก็บถาวรอย่างปลอดภัย | ตู้เซฟเก็บเอกสารสำคัญ ล็อคกุญแจไว้ |

### 🎮 คำสั่ง git restore ที่สำคัญ

| คำสั่ง | ทำอะไร | เมื่อไหร่ใช้ |
|--------|--------|------------|
| `git restore <file>` | ยกเลิกการแก้ไขใน Working Directory | เมื่อแก้ไขผิด ยังไม่ได้ `git add` |
| `git restore --staged <file>` | เอาไฟล์ออกจาก Staging Area | เมื่อ `git add` ไปแล้ว แต่ยังไม่อยาก commit |
| `git restore --source=<commit> <file>` | กู้คืนไฟล์จาก commit ที่ระบุ | เมื่อต้องการเวอร์ชันเก่าจากประวัติ |
| `git restore .` | ยกเลิกการแก้ไขทุกไฟล์ | เมื่อทุกอย่างพังหมด ต้องการเริ่มใหม่ |

### 🤖 ทำไม Git Restore ถึงสำคัญใน MLOps?

ในการพัฒนา Machine Learning เราทำการทดลองบ่อยมาก และบ่อยครั้งที่ผลลัพธ์ไม่เป็นไปตามที่หวัง:

| สถานการณ์ | ปัญหาที่เกิด | วิธีแก้ด้วย git restore |
|-----------|-------------|------------------------|
| ปรับ hyperparameters | Accuracy ลดลง | กู้คืนค่า parameters เดิม |
| เปลี่ยน preprocessing | Data pipeline พัง | ย้อนกลับไปใช้โค้ดเดิม |
| ลอง model architecture ใหม่ | Training ช้าลง 10 เท่า | กู้คืน model เดิม |
| แก้ไข evaluation metrics | ผลลัพธ์คำนวณผิด | กลับไปใช้สูตรที่ถูกต้อง |

**ข้อดีของการใช้ git restore:**
- ⚡ กู้คืนได้ทันที ไม่ต้อง copy-paste จากที่อื่น
- 🛡️ ปลอดภัย ไม่มีทางทำให้ประวัติ commit เสียหาย
- 🎯 เลือกกู้คืนเฉพาะไฟล์ที่ต้องการได้

---

## 🎬 สถานการณ์จำลอง: เรื่องราวของ Lab นี้

### 📋 บทบาทของคุณ

คุณคือ **ML Engineer** ที่เพิ่งเข้าทำงานที่บริษัท DataTech ได้ 1 เดือน หัวหน้าทีมมอบหมายให้คุณพัฒนา **Classification Pipeline** สำหรับจำแนกพันธุ์ดอกไอริส (Iris) ซึ่งเป็นโปรเจกต์ฝึกหัดก่อนจะได้ทำโปรเจกต์จริง

### 🎯 เป้าหมายของโปรเจกต์

สร้าง ML Pipeline ที่ประกอบด้วย 3 ส่วนหลัก:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  📊 data_prep   │───▶│  🤖 train       │───▶│  📈 evaluate    │
│                 │    │                 │    │                 │
│  โหลด & เตรียม   │    │  Train โมเดล    │    │  วัดผล & รายงาน │
│  ข้อมูล         │    │  Random Forest  │    │  Accuracy, F1   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🚧 ปัญหาที่จะเกิดขึ้นระหว่างทาง

ในระหว่างการพัฒนา คุณจะพบเหตุการณ์ไม่คาดฝันหลายอย่าง:

| สถานการณ์ | ปัญหา | สิ่งที่จะเรียนรู้ |
|-----------|------|-----------------|
| **#1** | แก้ไขโค้ดผิดพลาด ทำให้โปรแกรมพัง | ใช้ `git restore` กู้คืนไฟล์ |
| **#2** | Add ไฟล์ผิด ไม่พร้อม commit | ใช้ `git restore --staged` ยกเลิก staging |
| **#3** | โค้ดเวอร์ชันใหม่ซับซ้อนเกินไป | ใช้ `git restore --source` กู้คืนจาก commit เก่า |
| **#4** | แก้ไขหลายไฟล์พร้อมกัน ทั้งหมดผิด | ใช้ `git restore .` กู้คืนทุกไฟล์ |

### 🗺️ แผนการทำ Lab

```
┌──────────────────────────────────────────────────────────────────────┐
│                        🗺️ แผนการทำ Lab                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Part 1: เตรียมความพร้อม                                             │
│  ├── ขั้นตอนที่ 0.1: ตั้งค่า Git (ครั้งแรกครั้งเดียว)                   │
│  └── ขั้นตอนที่ 0.2: สร้าง Project Environment                       │
│                                                                      │
│  Part 2: สร้าง ML Pipeline                                           │
│  ├── ขั้นตอนที่ 1: สร้าง data_prep.py → commit                       │
│  ├── ขั้นตอนที่ 2: สร้าง train.py → commit                           │
│  └── ขั้นตอนที่ 3: สร้าง evaluate.py → commit                        │
│                                                                      │
│  Part 3: เรียนรู้ git restore ผ่านสถานการณ์จำลอง                      │
│  ├── สถานการณ์ 1: กู้คืนไฟล์ใน Working Directory                     │
│  ├── สถานการณ์ 2: ยกเลิกไฟล์ที่ add ไปแล้ว (Staged)                  │
│  ├── สถานการณ์ 3: กู้คืนไฟล์จาก Commit เฉพาะ                         │
│  └── สถานการณ์ 4: กู้คืนหลายไฟล์พร้อมกัน                             │
│                                                                      │
│  Part 4: แบบฝึกหัดเพิ่มเติม & สรุป                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Part 1: การเตรียมความพร้อม

### ขั้นตอนที่ 0.1: ตั้งค่า Git (ทำครั้งแรกครั้งเดียว)

> ⚠️ **หมายเหตุ**: ถ้าเคยตั้งค่า Git แล้ว ให้ข้ามไปขั้นตอนที่ 0.2 ได้เลย

**ทำไมต้องตั้งค่า?** Git ต้องรู้ว่า "ใคร" เป็นคนทำการเปลี่ยนแปลง เพื่อบันทึกในประวัติ commit

```bash
# ตรวจสอบว่าตั้งค่าไว้แล้วหรือยัง
git config --global user.name
git config --global user.email
```

ถ้ายังไม่มีค่า ให้ตั้งค่าดังนี้:

```bash
# ตั้งค่าชื่อผู้ใช้ (ใส่ชื่อจริงของนักศึกษา)
git config --global user.name "Student Name"

# ตั้งค่าอีเมล (ใส่อีเมลจริงของนักศึกษา)
git config --global user.email "student@example.com"
```

ตรวจสอบการตั้งค่าทั้งหมด:

```bash
git config --global --list
```

---

### ขั้นตอนที่ 0.2: เตรียม Project Environment

**สิ่งที่จะทำ:** สร้างโฟลเดอร์โปรเจกต์ใหม่ และเริ่มต้น Git repository

```bash
# สร้างโฟลเดอร์สำหรับ Lab
mkdir -p ~/mlops-git-restore-lab
cd ~/mlops-git-restore-lab

# สร้าง Git repository ใหม่
git init

# สร้าง virtual environment (แนะนำ)
python3 -m venv venv
source venv/bin/activate

# ติดตั้ง dependencies
pip install scikit-learn pandas numpy
```

**ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in /home/user/mlops-git-restore-lab/.git/
```

**💡 อธิบาย:**
- `mkdir -p` สร้างโฟลเดอร์ (รวมถึง parent folders ถ้าไม่มี)
- `git init` สร้าง repository ว่างเปล่า พร้อมใช้งาน Git
- `python3 -m venv venv` สร้าง virtual environment เพื่อแยก dependencies

---

## 📝 Part 2: สร้าง ML Pipeline

ในส่วนนี้ เราจะสร้างไฟล์ 3 ไฟล์ และ commit ทีละไฟล์ เพื่อให้มีประวัติ commit ที่จะใช้ในการทดลอง `git restore`

### ขั้นตอนที่ 1: สร้างไฟล์ Data Preparation

**เป้าหมาย:** สร้างโมดูลสำหรับโหลดและเตรียมข้อมูล Iris Dataset

**ทำไมต้อง commit ทันที?** เพื่อสร้าง "จุดบันทึก" (restore point) ที่สามารถกลับมาได้

```bash
cat > data_prep.py << 'EOF'
"""
Data Preparation Module
สำหรับโหลดและเตรียมข้อมูล Iris Dataset
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_data():
    """โหลด Iris dataset และแปลงเป็น DataFrame"""
    iris = load_iris()
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    df['target_name'] = df['target'].map({
        0: 'setosa',
        1: 'versicolor', 
        2: 'virginica'
    })
    return df

def prepare_data(df, test_size=0.2, random_state=42):
    """แบ่งข้อมูลเป็น train/test sets"""
    X = df.drop(['target', 'target_name'], axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df = load_data()
    print("Dataset Info:")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())
    
    X_train, X_test, y_train, y_test = prepare_data(df)
EOF
```

**Commit ไฟล์แรก:**

```bash
git add data_prep.py
git commit -m "feat: add data preparation module"
```

**💡 อธิบายสิ่งที่เกิดขึ้น:**

| ขั้นตอน | คำสั่ง | สิ่งที่เกิดขึ้น |
|--------|--------|--------------|
| 1. สร้างไฟล์ | `cat > data_prep.py` | ไฟล์อยู่ใน Working Directory (ยังไม่ถูก track) |
| 2. เตรียม commit | `git add data_prep.py` | ย้ายไฟล์ไปยัง Staging Area |
| 3. บันทึกถาวร | `git commit -m "..."` | บันทึกไฟล์ลงใน Repository |

---

### ขั้นตอนที่ 2: สร้างไฟล์ Training

**เป้าหมาย:** สร้างโมดูลสำหรับ train โมเดล Random Forest

```bash
cat > train.py << 'EOF'
"""
Model Training Module
สำหรับ train โมเดล Classification
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from data_prep import load_data, prepare_data

def train_model(X_train, y_train, n_estimators=100, max_depth=5):
    """Train Random Forest Classifier"""
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    print(f"Model trained with {n_estimators} trees, max_depth={max_depth}")
    
    return model, scaler

def save_model(model, scaler, model_path="model.pkl", scaler_path="scaler.pkl"):
    """บันทึกโมเดลและ scaler"""
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == "__main__":
    # Load and prepare data
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    
    # Train model
    model, scaler = train_model(X_train, y_train)
    
    # Save model
    save_model(model, scaler)
EOF
```

**Commit ไฟล์ training:**

```bash
git add train.py
git commit -m "feat: add model training module"
```

**💡 สังเกต:** ตอนนี้เรามี 2 commits แล้ว

---

### ขั้นตอนที่ 3: สร้างไฟล์ Evaluation

**เป้าหมาย:** สร้างโมดูลสำหรับประเมินผลโมเดล

```bash
cat > evaluate.py << 'EOF'
"""
Model Evaluation Module
สำหรับประเมินผลโมเดล Classification
"""
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import pickle
import numpy as np
from data_prep import load_data, prepare_data

def load_model(model_path="model.pkl", scaler_path="scaler.pkl"):
    """โหลดโมเดลและ scaler"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

def evaluate_model(model, scaler, X_test, y_test):
    """ประเมินผลโมเดล"""
    # Scale test data
    X_test_scaled = scaler.transform(X_test)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    return metrics, y_pred

def print_evaluation_report(metrics, y_test, y_pred):
    """พิมพ์รายงานการประเมินผล"""
    print("=" * 50)
    print("MODEL EVALUATION REPORT")
    print("=" * 50)
    
    print("\n📊 Performance Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1_score']:.4f}")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, 
          target_names=['setosa', 'versicolor', 'virginica']))
    
    print("🔢 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    # Load data
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    
    # Load model
    model, scaler = load_model()
    
    # Evaluate
    metrics, y_pred = evaluate_model(model, scaler, X_test, y_test)
    print_evaluation_report(metrics, y_test, y_pred)
EOF
```

**Commit ไฟล์ evaluation:**

```bash
git add evaluate.py
git commit -m "feat: add model evaluation module"
```

---

### ✅ ตรวจสอบประวัติ Commits

```bash
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
abc1234 feat: add model evaluation module
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

**💡 อธิบาย:** ตอนนี้เรามี 3 commits ซึ่งเปรียบเหมือน 3 "จุดบันทึก" ที่สามารถกลับไปได้ทุกเมื่อ

```
┌──────────────────────────────────────────────────────────────────────┐
│                    📸 Commits ที่เรามีตอนนี้                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [ghi9012]              [def5678]              [abc1234]            │
│      │                      │                      │                 │
│      ▼                      ▼                      ▼                 │
│  ┌────────┐            ┌────────┐            ┌────────┐             │
│  │data_   │───────────▶│train.py│───────────▶│evaluate│─────▶ HEAD  │
│  │prep.py │            │        │            │.py     │             │
│  └────────┘            └────────┘            └────────┘             │
│                                                                      │
│   Commit #1             Commit #2             Commit #3              │
│   (เก่าสุด)                                   (ใหม่สุด)              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🚨 Part 3: สถานการณ์ปัญหาและการแก้ไขด้วย Git Restore

### 📍 สถานการณ์ที่ 1: แก้ไขโค้ดผิดพลาดใน Working Directory

#### 🎭 เรื่องราว

วันจันทร์เช้า คุณตื่นมาด้วยความตั้งใจว่าจะปรับปรุง train.py ให้ดีขึ้น คุณต้องการทดลองเปลี่ยน hyperparameters แต่เผลอพิมพ์ผิด ทำให้โค้ดพังทั้งหมด และคุณ **ยังไม่ได้ commit**

#### 🎯 สิ่งที่จะเรียนรู้

**`git restore <file>`** - กู้คืนไฟล์จาก commit ล่าสุด (HEAD) ไปยัง Working Directory

```
┌─────────────────────────────────────────────────────────────────────┐
│                 สถานการณ์ที่ 1: ไฟล์พังใน Working Directory          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Repository                Working Directory                       │
│   (commit ล่าสุด)            (ไฟล์พัง!)                             │
│                                                                     │
│   ┌──────────────┐          ┌──────────────┐                       │
│   │  train.py    │          │  train.py    │                       │
│   │  ✅ ใช้งานได้  │ ◀─────── │  ❌ พัง!      │                       │
│   │              │ git      │  n_estimators│                       │
│   │  n_estimators│ restore  │  = -999      │                       │
│   │  = 100       │          │  max_depth   │                       │
│   │  max_depth   │          │  = "invalid" │                       │
│   │  = 5         │          │              │                       │
│   └──────────────┘          └──────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### ขั้นตอน 1.1: แก้ไขไฟล์ให้ผิดพลาด (จำลองความผิดพลาด)

```bash
cat > train.py << 'EOF'
"""
Model Training Module - BROKEN VERSION
สำหรับ train โมเดล Classification
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from data_prep import load_data, prepare_data

def train_model(X_train, y_train, n_estimators=100, max_depth=5):
    """Train Random Forest Classifier"""
    # BUG: ลืมใส่ scaler!
    
    # Train model with WRONG parameters
    model = RandomForestClassifier(
        n_estimators=-999,  # BUG: ค่าติดลบ!
        max_depth="invalid",  # BUG: ชนิดข้อมูลผิด!
        random_state=42
    )
    model.fit(X_train, y_train)  # BUG: ไม่ได้ scale ข้อมูล!
    
    print(f"Model trained!")
    
    return model  # BUG: ไม่ได้ return scaler!

def save_model(model, scaler, model_path="model.pkl", scaler_path="scaler.pkl"):
    """บันทึกโมเดลและ scaler"""
    # เหมือนเดิม แต่จะพังเพราะไม่มี scaler
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train)  # จะ Error!
    save_model(model, None)  # จะ Error!
EOF
```

**💡 สังเกต bugs ที่ใส่ไว้:**
- `n_estimators=-999` → ค่าติดลบ ไม่ถูกต้อง
- `max_depth="invalid"` → ต้องเป็นตัวเลข ไม่ใช่ string
- ลืม scaler ทำให้โค้ดพังต่อเนื่อง

#### ขั้นตอน 1.2: ตรวจสอบสถานะ

```bash
# ดูสถานะไฟล์
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   train.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**💡 สังเกต:** Git บอกเราเองว่าใช้ `git restore <file>` เพื่อยกเลิกการเปลี่ยนแปลงได้!

```bash
# ดูความแตกต่างระหว่างไฟล์ปัจจุบันกับ commit ล่าสุด
git diff train.py
```

**💡 อธิบาย `git diff`:**
- บรรทัดที่ขึ้นต้นด้วย `-` (สีแดง) = ถูกลบออก
- บรรทัดที่ขึ้นต้นด้วย `+` (สีเขียว) = ถูกเพิ่มเข้ามา

#### ขั้นตอน 1.3: ลองรันโค้ดที่พัง (เพื่อยืนยันว่าพังจริง)

```bash
python train.py
```

**ผลลัพธ์ที่คาดหวัง:** Error! เพราะ parameters ไม่ถูกต้อง

#### ขั้นตอน 1.4: ใช้ git restore เพื่อกู้คืน

```bash
# กู้คืนไฟล์ train.py กลับไปเป็นเวอร์ชันล่าสุดที่ commit
git restore train.py
```

**ตรวจสอบผลลัพธ์:**

```bash
# ตรวจสอบว่าไฟล์กลับมาเป็นปกติ
git status

# ดู diff อีกครั้ง - ไม่ควรมีความแตกต่าง
git diff train.py

# ลองรันอีกครั้ง - ควรทำงานได้
python train.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
Training set size: 120
Test set size: 30
Model trained with 100 trees, max_depth=5
Model saved to model.pkl
Scaler saved to scaler.pkl
```

#### 📝 สรุปสถานการณ์ที่ 1

| ก่อน | หลัง |
|-----|------|
| `train.py` มี bugs | `train.py` กลับมาเป็นเวอร์ชันที่ใช้งานได้ |
| `git status` แสดง modified | `git status` แสดง clean |
| รันโค้ดแล้ว Error | รันโค้ดได้ปกติ |

---

### 📍 สถานการณ์ที่ 2: ยกเลิกไฟล์ที่ add ไปแล้ว (Staged)

#### 🎭 เรื่องราว

วันอังคาร คุณแก้ไขไฟล์หลายไฟล์พร้อมกัน แล้วใช้ `git add .` เพื่อ add ทั้งหมด แต่หลังจากนั้นคุณรู้ตัวว่า evaluate.py ยังไม่พร้อม commit เพราะมี experimental features ที่ยังไม่ได้ทดสอบ

#### 🎯 สิ่งที่จะเรียนรู้

**`git restore --staged <file>`** - เอาไฟล์ออกจาก Staging Area กลับไปยัง Working Directory

```
┌─────────────────────────────────────────────────────────────────────┐
│                 สถานการณ์ที่ 2: Unstage ไฟล์                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Working Directory          Staging Area                           │
│                                                                     │
│   ┌──────────────┐          ┌──────────────┐                       │
│   │  data_prep   │          │  data_prep   │  ✅ พร้อม commit      │
│   │  (แก้ไขแล้ว)  │───add──▶│  (แก้ไขแล้ว)  │                       │
│   └──────────────┘          └──────────────┘                       │
│                                                                     │
│   ┌──────────────┐          ┌──────────────┐                       │
│   │  evaluate    │◀──────── │  evaluate    │  ❌ ยังไม่พร้อม!       │
│   │  (ยังไม่เสร็จ) │  git     │  (ยังไม่เสร็จ) │                       │
│   └──────────────┘ restore  └──────────────┘                       │
│                    --staged                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### ขั้นตอน 2.1: แก้ไขหลายไฟล์

**แก้ไข data_prep.py** (เพิ่ม feature engineering):

```bash
cat > data_prep.py << 'EOF'
"""
Data Preparation Module - Updated Version
สำหรับโหลดและเตรียมข้อมูล Iris Dataset
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_data():
    """โหลด Iris dataset และแปลงเป็น DataFrame"""
    iris = load_iris()
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    df['target_name'] = df['target'].map({
        0: 'setosa',
        1: 'versicolor', 
        2: 'virginica'
    })
    return df

def add_features(df):
    """เพิ่ม engineered features - NEW FUNCTION"""
    df['sepal_ratio'] = df['sepal length (cm)'] / df['sepal width (cm)']
    df['petal_ratio'] = df['petal length (cm)'] / df['petal width (cm)']
    df['sepal_area'] = df['sepal length (cm)'] * df['sepal width (cm)']
    df['petal_area'] = df['petal length (cm)'] * df['petal width (cm)']
    return df

def prepare_data(df, test_size=0.2, random_state=42, add_engineered=False):
    """แบ่งข้อมูลเป็น train/test sets"""
    if add_engineered:
        df = add_features(df)
    
    feature_cols = [col for col in df.columns if col not in ['target', 'target_name']]
    X = df[feature_cols]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Number of features: {X_train.shape[1]}")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df = load_data()
    print("Original Dataset:")
    print(df.head())
    
    X_train, X_test, y_train, y_test = prepare_data(df, add_engineered=True)
    print("\nFeatures:", X_train.columns.tolist())
EOF
```

**แก้ไข evaluate.py** (เพิ่ม experimental features ที่ยังไม่พร้อม):

```bash
cat > evaluate.py << 'EOF'
"""
Model Evaluation Module - EXPERIMENTAL VERSION
สำหรับประเมินผลโมเดล Classification
WARNING: This version has experimental features!
"""
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import pickle
import json
import numpy as np
from datetime import datetime
from data_prep import load_data, prepare_data

def load_model(model_path="model.pkl", scaler_path="scaler.pkl"):
    """โหลดโมเดลและ scaler"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

def evaluate_model(model, scaler, X_test, y_test):
    """ประเมินผลโมเดล"""
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted'),
        'timestamp': datetime.now().isoformat(),  # EXPERIMENTAL
        'experiment_id': 'exp_001'  # EXPERIMENTAL - hardcoded!
    }
    
    return metrics, y_pred

def save_metrics_to_file(metrics, filepath="metrics.json"):
    """EXPERIMENTAL: บันทึก metrics เป็นไฟล์ JSON"""
    # TODO: ยังไม่ได้ handle edge cases
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {filepath}")

def print_evaluation_report(metrics, y_test, y_pred):
    """พิมพ์รายงานการประเมินผล"""
    print("=" * 50)
    print("MODEL EVALUATION REPORT (EXPERIMENTAL)")
    print("=" * 50)
    
    print("\n📊 Performance Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1_score']:.4f}")
    
    print(f"\n🕐 Timestamp: {metrics.get('timestamp', 'N/A')}")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, 
          target_names=['setosa', 'versicolor', 'virginica']))

if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    model, scaler = load_model()
    metrics, y_pred = evaluate_model(model, scaler, X_test, y_test)
    print_evaluation_report(metrics, y_test, y_pred)
    save_metrics_to_file(metrics)  # EXPERIMENTAL
EOF
```

#### ขั้นตอน 2.2: Add ทุกไฟล์ไปก่อน (จำลองการ add โดยไม่ได้คิดก่อน)

```bash
git add .
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   data_prep.py
        modified:   evaluate.py
```

**💡 สังเกต:** Git บอกเราว่าใช้ `git restore --staged <file>` เพื่อ unstage ได้

#### ขั้นตอน 2.3: ตัดสินใจว่า evaluate.py ยังไม่พร้อม commit

**สาเหตุ:**
- มี experimental features ที่ยังไม่ได้ทดสอบ
- ยังมี TODO ที่ยังไม่ได้ทำ
- อาจทำให้ production พัง

```bash
# ยกเลิก staging เฉพาะ evaluate.py
git restore --staged evaluate.py

# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   data_prep.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   evaluate.py
```

**💡 อธิบาย:**
- `data_prep.py` ยังอยู่ใน Staging Area → พร้อม commit
- `evaluate.py` กลับไปอยู่ใน Working Directory → ยังไม่ถูก commit

#### ขั้นตอน 2.4: Commit เฉพาะ data_prep.py

```bash
git commit -m "feat: add feature engineering to data_prep"
```

#### ขั้นตอน 2.5: ตัดสินใจว่า evaluate.py ยังไม่พร้อม ให้กู้คืนเวอร์ชันเดิม

```bash
# กู้คืน evaluate.py กลับไปเป็นเวอร์ชันเดิม (ไม่มี experimental features)
git restore evaluate.py

# ตรวจสอบ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch main
nothing to commit, working tree clean
```

#### 📝 สรุปสถานการณ์ที่ 2

| ขั้นตอน | คำสั่ง | ผลลัพธ์ |
|--------|--------|---------|
| แก้ไข 2 ไฟล์ | - | ทั้ง 2 ไฟล์อยู่ใน Working Directory |
| Add ทั้งหมด | `git add .` | ทั้ง 2 ไฟล์อยู่ใน Staging Area |
| Unstage 1 ไฟล์ | `git restore --staged evaluate.py` | evaluate.py กลับไป Working Directory |
| Commit | `git commit -m "..."` | เฉพาะ data_prep.py ถูก commit |
| กู้คืน | `git restore evaluate.py` | evaluate.py กลับไปเวอร์ชันเดิม |

---

### 📍 สถานการณ์ที่ 3: กู้คืนไฟล์จาก Commit เฉพาะ

#### 🎭 เรื่องราว

วันพุธ หัวหน้าทีมบอกว่า evaluate.py เวอร์ชันปัจจุบันซับซ้อนเกินไป (over-engineered) และอยากให้กลับไปใช้เวอร์ชันแรกที่เรียบง่ายกว่า ปัญหาคือ คุณได้ commit เวอร์ชันซับซ้อนไปแล้ว

#### 🎯 สิ่งที่จะเรียนรู้

**`git restore --source=<commit> <file>`** - กู้คืนไฟล์จาก commit ที่ระบุ

```
┌─────────────────────────────────────────────────────────────────────┐
│                 สถานการณ์ที่ 3: กู้คืนจาก commit เฉพาะ                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Commit History (เก่า → ใหม่)                                       │
│                                                                     │
│   [abc1234]         [def5678]         [xyz7890]                     │
│       │                 │                 │                         │
│       ▼                 ▼                 ▼                         │
│   ┌─────────┐       ┌─────────┐       ┌─────────┐                   │
│   │evaluate │       │evaluate │       │evaluate │──▶ HEAD           │
│   │ Simple  │       │ Medium  │       │ Complex │   (ปัจจุบัน)       │
│   │ Version │       │         │       │ Version │                   │
│   └─────────┘       └─────────┘       └─────────┘                   │
│       ▲                                                             │
│       │                                                             │
│       └─────────── git restore --source=abc1234 evaluate.py        │
│                    (กู้คืนเวอร์ชันเรียบง่าย)                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### ขั้นตอน 3.1: ดูประวัติ commits

```bash
git log --oneline
```

**ผลลัพธ์ตัวอย่าง:**
```
xyz7890 feat: add feature engineering to data_prep
abc1234 feat: add model evaluation module
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

**💡 จด commit hash ของ "feat: add model evaluation module" ไว้** เพราะนั่นคือเวอร์ชันเรียบง่ายที่เราต้องการ

#### ขั้นตอน 3.2: สร้างเวอร์ชันซับซ้อนแล้ว commit (จำลองการ over-engineer)

```bash
cat > evaluate.py << 'EOF'
"""
Model Evaluation Module - TOO COMPLEX VERSION
มี features มากเกินไป!
"""
from sklearn.metrics import *
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os
import sys
from data_prep import load_data, prepare_data

# Setup logging - OVER-ENGINEERED!
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """OVER-ENGINEERED: ไม่จำเป็นต้องเป็น class"""
    
    def __init__(self, model_path="model.pkl", scaler_path="scaler.pkl"):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.metrics_history = []
        logger.info("ModelEvaluator initialized")
        
    def load_model(self):
        logger.info(f"Loading model from {self.model_path}")
        # ... โค้ดยาวมาก ...
        pass
        
    # ... methods อื่นๆ อีกมากมาย ...

# ทำให้โค้ดซับซ้อนเกินไป!
if __name__ == "__main__":
    print("This version is too complex!")
    print("We need to go back to the simple version!")
EOF

git add evaluate.py
git commit -m "refactor: over-engineer evaluation module"
```

#### ขั้นตอน 3.3: ดู commits อีกครั้ง

```bash
git log --oneline
```

**ผลลัพธ์ตัวอย่าง:**
```
pqr4567 refactor: over-engineer evaluation module
xyz7890 feat: add feature engineering to data_prep
abc1234 feat: add model evaluation module         ← เราต้องการเวอร์ชันนี้!
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

#### ขั้นตอน 3.4: กู้คืนไฟล์จาก commit เดิม

**วิธีที่ 1: ใช้ HEAD~N** (N = จำนวน commits ย้อนกลับ)

```bash
# HEAD~2 หมายถึง 2 commits ก่อน HEAD
git restore --source=HEAD~2 evaluate.py
```

**วิธีที่ 2: ใช้ commit hash โดยตรง** (แนะนำ เพราะแม่นยำกว่า)

```bash
# ใช้ commit hash จริงของคุณ (จากขั้นตอน 3.3)
git restore --source=abc1234 evaluate.py
```

#### ขั้นตอน 3.5: ตรวจสอบและ commit การเปลี่ยนแปลง

```bash
# ตรวจสอบว่าไฟล์กลับมาเป็นเวอร์ชันเรียบง่าย
cat evaluate.py

# ดู status
git status

# Commit การเปลี่ยนแปลง
git add evaluate.py
git commit -m "revert: restore simple evaluation module"
```

#### 📝 สรุปสถานการณ์ที่ 3

| ขั้นตอน | สิ่งที่เกิดขึ้น |
|--------|--------------|
| มี commit ที่ over-engineered | evaluate.py ซับซ้อนเกินไป |
| ใช้ `git log` หา commit hash | รู้ว่าเวอร์ชันไหนที่ต้องการ |
| ใช้ `git restore --source=<commit>` | กู้คืนเวอร์ชันเรียบง่าย |
| Commit | บันทึกการกู้คืนเป็น commit ใหม่ |

---

### 📍 สถานการณ์ที่ 4: กู้คืนหลายไฟล์พร้อมกัน

#### 🎭 เรื่องราว

วันพฤหัส คุณกำลังรีบทำงานก่อนประชุม เผลอรันคำสั่งที่เขียนทับไฟล์หลายๆ ไฟล์ ทำให้โค้ดพังหมด โชคดีที่ยังไม่ได้ commit

#### 🎯 สิ่งที่จะเรียนรู้

**`git restore .`** - กู้คืนทุกไฟล์ใน directory ปัจจุบัน

```
┌─────────────────────────────────────────────────────────────────────┐
│                 สถานการณ์ที่ 4: กู้คืนหลายไฟล์พร้อมกัน                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Working Directory (พังหมด!)        Repository (ยังดี!)             │
│                                                                     │
│   ┌──────────────┐                   ┌──────────────┐               │
│   │ data_prep.py │  ◀────────────────│ data_prep.py │               │
│   │ "# BROKEN!"  │   git restore .   │ (เวอร์ชันดี)  │               │
│   └──────────────┘                   └──────────────┘               │
│   ┌──────────────┐                   ┌──────────────┐               │
│   │ train.py     │  ◀────────────────│ train.py     │               │
│   │ "# BROKEN!"  │   git restore .   │ (เวอร์ชันดี)  │               │
│   └──────────────┘                   └──────────────┘               │
│                                                                     │
│   ❌ ทั้งโปรเจกต์พัง!                   ✅ ทุกอย่างกลับมา!             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### ขั้นตอน 4.1: แก้ไขหลายไฟล์ให้ผิดพลาด (จำลองอุบัติเหตุ)

```bash
# แก้ไข data_prep.py ให้ผิด
echo "# BROKEN!" > data_prep.py

# แก้ไข train.py ให้ผิด
echo "# BROKEN!" > train.py

# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch main
Changes not staged for commit:
        modified:   data_prep.py
        modified:   train.py
```

```bash
# ดูเนื้อหาที่ถูกเขียนทับ - ไฟล์พังหมดแล้ว!
echo "=== data_prep.py ==="
cat data_prep.py

echo ""
echo "=== train.py ==="
cat train.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
=== data_prep.py ===
# BROKEN!

=== train.py ===
# BROKEN!
```

😱 **ทั้งสองไฟล์มีแค่ "# BROKEN!" หมดแล้ว!**

#### ขั้นตอน 4.2: กู้คืนทุกไฟล์พร้อมกัน

```bash
# กู้คืนทุกไฟล์ใน directory ปัจจุบัน
git restore .
```

**💡 หรือกู้คืนเฉพาะบางไฟล์:**
```bash
git restore data_prep.py train.py
```

#### ขั้นตอน 4.3: ตรวจสอบผลลัพธ์

```bash
# ตรวจสอบสถานะ
git status

# ดูเนื้อหาที่กู้คืนมา
echo "=== data_prep.py (หลัง restore) ==="
head -20 data_prep.py

echo ""
echo "=== train.py (หลัง restore) ==="
head -20 train.py
```

**ผลลัพธ์ที่คาดหวัง:** ไฟล์ทั้งสองกลับมามีโค้ดเต็มเหมือนเดิม!

#### 📝 สรุปสถานการณ์ที่ 4

| ก่อน | หลัง |
|-----|------|
| หลายไฟล์พังพร้อมกัน | ทุกไฟล์กลับมาเป็นปกติ |
| ต้องกู้คืนทีละไฟล์? ไม่! | ใช้ `git restore .` คำสั่งเดียวจบ |

---

## 📊 สรุปคำสั่ง Git Restore

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Git Restore Command Summary                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  🔹 Discard changes in Working Directory:                              │
│     git restore <file>                                                 │
│     git restore .                       # ทุกไฟล์                      │
│                                                                        │
│  🔹 Unstage file (remove from Staging Area):                           │
│     git restore --staged <file>                                        │
│     git restore --staged .              # ทุกไฟล์                      │
│                                                                        │
│  🔹 Restore file from specific commit:                                 │
│     git restore --source=<commit> <file>                               │
│     git restore --source=HEAD~2 <file>  # 2 commits ก่อน               │
│                                                                        │
│  🔹 Combined operations:                                               │
│     git restore --source=<commit> --staged --worktree <file>           │
│     (กู้คืนทั้ง staging และ working directory)                         │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 📋 Quick Reference Table

| สถานการณ์ | คำสั่ง | ผลลัพธ์ |
|-----------|--------|---------|
| แก้ไขผิด ยังไม่ได้ add | `git restore <file>` | กลับไปเป็น commit ล่าสุด |
| Add ไปแล้ว ไม่อยาก commit | `git restore --staged <file>` | เอาออกจาก staging |
| ต้องการเวอร์ชันเก่า | `git restore --source=<commit> <file>` | กู้คืนจาก commit ที่ระบุ |
| ทุกอย่างพัง! | `git restore .` | กู้คืนทั้งหมด |

---

## ✅ Part 4: แบบฝึกหัดเพิ่มเติม

### แบบฝึกหัดที่ 1: Basic Restore

**เป้าหมาย:** ฝึกใช้ `git restore` กับการเปลี่ยนแปลงเล็กน้อย

1. แก้ไข `train.py` โดยเปลี่ยน `n_estimators=100` เป็น `n_estimators=10`
2. ใช้ `git diff` ดูความแตกต่าง
3. ใช้ `git restore train.py` กู้คืนไฟล์
4. ตรวจสอบว่าไฟล์กลับมาเป็นค่าเดิม (`n_estimators=100`)

### แบบฝึกหัดที่ 2: Staged Restore

**เป้าหมาย:** ฝึกใช้ `git restore --staged`

1. แก้ไข `evaluate.py` เพิ่ม comment ใดๆ (เช่น `# This is a test`)
2. ใช้ `git add evaluate.py`
3. ตรวจสอบด้วย `git status` ว่าไฟล์อยู่ใน staging
4. ใช้ `git restore --staged evaluate.py`
5. ตรวจสอบด้วย `git status` ว่าไฟล์กลับไปอยู่ใน working directory
6. ใช้ `git restore evaluate.py` เพื่อยกเลิกการเปลี่ยนแปลงทั้งหมด

### แบบฝึกหัดที่ 3: Source Restore

**เป้าหมาย:** ฝึกใช้ `git restore --source`

1. ดู commit history ด้วย `git log --oneline`
2. เลือก commit ที่มี `data_prep.py` เวอร์ชันแรก (ก่อน feature engineering)
3. ใช้ `git restore --source=<commit_hash> data_prep.py`
4. ตรวจสอบความแตกต่างด้วย `git diff data_prep.py`
5. ตัดสินใจว่าจะ commit หรือ restore กลับตามต้องการ

---

## 🎓 บทสรุป

### สิ่งที่ได้เรียนรู้

1. **git restore** เป็นเครื่องมือสำคัญในการจัดการกับความผิดพลาดระหว่างการพัฒนา
2. การแยกแยะระหว่าง **Working Directory**, **Staging Area**, และ **Repository** มีความสำคัญ
3. ใน MLOps การทดลองและย้อนกลับเป็นเรื่องปกติ - `git restore` ช่วยให้ทำได้อย่างปลอดภัย
4. การใช้ `--source` ช่วยให้กู้คืนไฟล์จาก commit ใดก็ได้ในประวัติ

### Best Practices สำหรับ MLOps

| Practice | เหตุผล |
|----------|--------|
| **Commit บ่อยๆ** | ทำให้มี restore points มากขึ้น ย้อนกลับได้หลายจุด |
| **เขียน commit message ที่ชัดเจน** | ช่วยให้หา commit ที่ต้องการได้ง่ายเมื่อต้อง restore |
| **ใช้ `git status` บ่อยๆ** | รู้ว่าอยู่ในสถานะไหน ก่อนตัดสินใจใช้คำสั่ง |
| **ทดสอบก่อน commit** | ลดโอกาสที่ต้อง restore เพราะ commit โค้ดที่พัง |
| **ใช้ branch สำหรับ experiment** | แยก experiments ออกจาก main branch |

### ⚠️ ข้อควรระวัง

| คำสั่ง | ข้อควรระวัง |
|--------|------------|
| `git restore <file>` | การเปลี่ยนแปลงที่ไม่ได้ commit จะหายไปถาวร! |
| `git restore .` | ทุกไฟล์จะถูกกู้คืน ตรวจสอบให้ดีก่อนใช้ |
| `git restore --source` | ไฟล์จะเปลี่ยน แต่ยังไม่ได้ commit อัตโนมัติ |

---

## 📚 อ้างอิง

- [Git Documentation - git restore](https://git-scm.com/docs/git-restore)
- [Pro Git Book](https://git-scm.com/book)
- [MLOps Best Practices](https://ml-ops.org/)