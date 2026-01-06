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

### ความเป็นมา

`git restore` เป็นคำสั่งที่ถูกเพิ่มเข้ามาใน Git 2.23 (สิงหาคม 2019) เพื่อแยกหน้าที่ออกจากคำสั่ง `git checkout` ที่เคยทำหลายอย่างพร้อมกัน ทำให้การใช้งานชัดเจนและปลอดภัยมากขึ้น

### Git Areas ที่ต้องเข้าใจ

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Git Workflow Areas                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   Working       │    │    Staging      │    │   Repository    │ │
│  │   Directory     │───▶│    Area         │───▶│   (Commits)     │ │
│  │                 │    │   (Index)       │    │                 │ │
│  │  ไฟล์ที่กำลัง    │    │  ไฟล์ที่พร้อม    │    │  ประวัติที่บันทึก │ │
│  │  แก้ไขอยู่       │    │  commit         │    │  แล้ว           │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│           ▲                     ▲                     │            │
│           │                     │                     │            │
│           └─────────────────────┴─────────────────────┘            │
│                      git restore (กู้คืน)                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### คำสั่ง git restore ที่สำคัญ

| คำสั่ง | หน้าที่ |
|--------|---------|
| `git restore <file>` | ยกเลิกการเปลี่ยนแปลงใน Working Directory |
| `git restore --staged <file>` | ยกเลิกการ add ไฟล์ออกจาก Staging Area |
| `git restore --source=<commit> <file>` | กู้คืนไฟล์จาก commit ที่ระบุ |
| `git restore .` | ยกเลิกการเปลี่ยนแปลงทุกไฟล์ |

### ความสำคัญใน MLOps

ในการพัฒนา Machine Learning Pipeline เรามักจะต้อง:

1. **ทดลองปรับ hyperparameters** - บางครั้งผลลัพธ์แย่ลง ต้องย้อนกลับ
2. **แก้ไข preprocessing logic** - อาจทำให้ data pipeline พัง
3. **เปลี่ยน model architecture** - ผลการ train อาจไม่ดี
4. **ปรับแต่ง evaluation metrics** - อาจคำนวณผิดพลาด

`git restore` ช่วยให้เราสามารถ "ย้อนเวลา" กลับไปใช้โค้ดเวอร์ชันที่ทำงานได้อย่างรวดเร็ว

---

## 🛠️ การเตรียมความพร้อม

### ขั้นตอนที่ 0.1: ตั้งค่า Git (ทำครั้งแรกครั้งเดียว)

> ⚠️ **หมายเหตุ**: ถ้าเคยตั้งค่า Git แล้ว ให้ข้ามไปขั้นตอนที่ 0.2 ได้เลย

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

---

## 📝 Lab Exercise

### 🎬 สถานการณ์จำลอง

คุณเป็น ML Engineer ที่กำลังพัฒนา Classification Pipeline สำหรับ Iris Dataset โดยมีหน้าที่:
1. เตรียมข้อมูล (Data Preparation)
2. Train โมเดล (Model Training)
3. ประเมินผล (Model Evaluation)

ระหว่างการทำงาน คุณจะพบปัญหาต่างๆ และต้องใช้ `git restore` เพื่อแก้ไข

---

### ขั้นตอนที่ 1: สร้างไฟล์เริ่มต้น - Data Preparation

สร้างไฟล์ `data_prep.py` สำหรับเตรียมข้อมูล:

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

Commit ไฟล์แรก:

```bash
git add data_prep.py
git commit -m "feat: add data preparation module"
```

---

### ขั้นตอนที่ 2: สร้างไฟล์ Training

สร้างไฟล์ `train.py` สำหรับ train โมเดล:

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

Commit ไฟล์ training:

```bash
git add train.py
git commit -m "feat: add model training module"
```

---

### ขั้นตอนที่ 3: สร้างไฟล์ Evaluation

สร้างไฟล์ `evaluate.py` สำหรับประเมินผลโมเดล:

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

Commit ไฟล์ evaluation:

```bash
git add evaluate.py
git commit -m "feat: add model evaluation module"
```

ตรวจสอบ commits ที่มี:

```bash
git log --oneline
```

ผลลัพธ์ที่คาดหวัง:
```
abc1234 feat: add model evaluation module
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

---

## 🚨 สถานการณ์ปัญหาและการแก้ไขด้วย Git Restore

### 📍 สถานการณ์ที่ 1: แก้ไขโค้ดผิดพลาดใน Working Directory

**ปัญหา**: คุณต้องการทดลองเปลี่ยน hyperparameters แต่ทำให้โค้ดพังและยังไม่ได้ commit

#### ขั้นตอน 1.1: แก้ไขไฟล์ให้ผิดพลาด

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

#### ขั้นตอน 1.2: ตรวจสอบสถานะ

```bash
# ดูสถานะไฟล์
git status

# ดูความแตกต่าง
git diff train.py
```

ผลลัพธ์ที่คาดหวัง:
```
On branch main
Changes not staged for commit:
  modified:   train.py
```

#### ขั้นตอน 1.3: ลองรันโค้ดที่พัง

```bash
python train.py
```

ผลลัพธ์ที่คาดหวัง: **Error!**

#### ขั้นตอน 1.4: ใช้ git restore เพื่อกู้คืน

```bash
# กู้คืนไฟล์ train.py กลับไปเป็นเวอร์ชันล่าสุดที่ commit
git restore train.py

# ตรวจสอบว่าไฟล์กลับมาเป็นปกติ
git status
git diff train.py

# ลองรันอีกครั้ง - ควรทำงานได้
python train.py
```

**สิ่งที่เกิดขึ้น**: ไฟล์ `train.py` กลับมาเป็นเวอร์ชันที่ commit ไว้ล่าสุด

---

### 📍 สถานการณ์ที่ 2: ยกเลิกไฟล์ที่ add ไปแล้ว (Staged)

**ปัญหา**: คุณแก้ไขไฟล์หลายไฟล์และ add ไปหมด แต่ต้องการยกเลิก add บางไฟล์

#### ขั้นตอน 2.1: แก้ไขหลายไฟล์

```bash
# แก้ไข data_prep.py - เพิ่ม feature ใหม่
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

```bash
# แก้ไข evaluate.py - เพิ่มการบันทึก metrics เป็นไฟล์ (แต่ยังไม่พร้อม)
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

#### ขั้นตอน 2.2: Add ทุกไฟล์ไปก่อน

```bash
git add .
git status
```

ผลลัพธ์ที่คาดหวัง:
```
Changes to be committed:
  modified:   data_prep.py
  modified:   evaluate.py
```

#### ขั้นตอน 2.3: ตัดสินใจว่า evaluate.py ยังไม่พร้อม commit

```bash
# ยกเลิก staging เฉพาะ evaluate.py
git restore --staged evaluate.py

# ตรวจสอบสถานะ
git status
```

ผลลัพธ์ที่คาดหวัง:
```
Changes to be committed:
  modified:   data_prep.py

Changes not staged for commit:
  modified:   evaluate.py
```

#### ขั้นตอน 2.4: Commit เฉพาะ data_prep.py

```bash
git commit -m "feat: add feature engineering to data_prep"

# ตัดสินใจว่า evaluate.py ยังไม่พร้อม ให้กู้คืนกลับเป็นเวอร์ชันเดิม
git restore evaluate.py

# ตรวจสอบ
git status
```

---

### 📍 สถานการณ์ที่ 3: กู้คืนไฟล์จาก Commit เฉพาะ

**ปัญหา**: คุณต้องการกู้คืน evaluate.py จาก commit แรกที่สร้างมัน เพราะเวอร์ชันปัจจุบันซับซ้อนเกินไป

#### ขั้นตอน 3.1: ดูประวัติ commits

```bash
git log --oneline
```

ผลลัพธ์ตัวอย่าง:
```
xyz7890 feat: add feature engineering to data_prep
abc1234 feat: add model evaluation module
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

#### ขั้นตอน 3.2: สมมติว่าเราทำการเปลี่ยนแปลง evaluate.py แล้ว commit

```bash
# แก้ไข evaluate.py อีกครั้ง
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

#### ขั้นตอน 3.3: กู้คืนไฟล์จาก commit เดิม

```bash
# ดู commits อีกครั้ง
git log --oneline

# หา commit hash ของ "feat: add model evaluation module"
# สมมติว่าเป็น abc1234

# กู้คืนจาก commit นั้น (ใช้ commit hash จริงของคุณ)
git restore --source=HEAD~1 evaluate.py

# หรือใช้ commit hash โดยตรง
# git restore --source=abc1234 evaluate.py

# ตรวจสอบว่าไฟล์กลับมาเป็นเวอร์ชันเรียบง่าย
cat evaluate.py

# Commit การเปลี่ยนแปลง
git add evaluate.py
git commit -m "revert: restore simple evaluation module"
```

---

### 📍 สถานการณ์ที่ 4: กู้คืนหลายไฟล์พร้อมกัน

**ปัญหา**: คุณแก้ไขหลายไฟล์พร้อมกัน แต่ทั้งหมดผิดพลาด ต้องกู้คืนทั้งหมด

#### ขั้นตอน 4.1: แก้ไขหลายไฟล์ให้ผิดพลาด

```bash
# แก้ไข data_prep.py ให้ผิด
echo "# BROKEN!" > data_prep.py

# แก้ไข train.py ให้ผิด
echo "# BROKEN!" > train.py

# ตรวจสอบสถานะ
git status
```

#### ขั้นตอน 4.2: กู้คืนทุกไฟล์พร้อมกัน

```bash
# กู้คืนทุกไฟล์ใน directory ปัจจุบัน
git restore .

# หรือกู้คืนเฉพาะบางไฟล์
# git restore data_prep.py train.py

# ตรวจสอบ
git status
cat data_prep.py | head -10
```

---

## 📊 สรุปคำสั่ง Git Restore

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Git Restore Command Summary                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  🔹 Discard changes in Working Directory:                             │
│     git restore <file>                                                 │
│     git restore .                       # ทุกไฟล์                      │
│                                                                        │
│  🔹 Unstage file (remove from Staging Area):                          │
│     git restore --staged <file>                                        │
│     git restore --staged .              # ทุกไฟล์                      │
│                                                                        │
│  🔹 Restore file from specific commit:                                │
│     git restore --source=<commit> <file>                               │
│     git restore --source=HEAD~2 <file>  # 2 commits ก่อน             │
│                                                                        │
│  🔹 Combined operations:                                               │
│     git restore --source=<commit> --staged --worktree <file>          │
│     (กู้คืนทั้ง staging และ working directory)                        │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---



## 🎓 บทสรุป

### สิ่งที่ได้เรียนรู้

1. **git restore** เป็นเครื่องมือสำคัญในการจัดการกับความผิดพลาดระหว่างการพัฒนา
2. การแยกแยะระหว่าง **Working Directory**, **Staging Area**, และ **Repository** มีความสำคัญ
3. ใน MLOps การทดลองและย้อนกลับเป็นเรื่องปกติ - `git restore` ช่วยให้ทำได้อย่างปลอดภัย
4. การใช้ `--source` ช่วยให้กู้คืนไฟล์จาก commit ใดก็ได้ในประวัติ

### Best Practices

1. **Commit บ่อยๆ** - ทำให้มี restore points มากขึ้น
2. **เขียน commit message ที่ชัดเจน** - ช่วยให้หา commit ที่ต้องการได้ง่าย
3. **ใช้ `git status` บ่อยๆ** - รู้ว่าอยู่ในสถานะไหน
4. **ทดสอบก่อน commit** - ลดโอกาสที่ต้อง restore

---

## 📚 อ้างอิง

- [Git Documentation - git restore](https://git-scm.com/docs/git-restore)
- [Pro Git Book](https://git-scm.com/book)
- [MLOps Best Practices](https://ml-ops.org/)