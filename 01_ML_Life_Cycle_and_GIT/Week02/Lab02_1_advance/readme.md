# 🎓 Git Lab 03: การใช้งาน Git กับ Machine Learning Project (MLOps)

## 📋 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     ML Project Git Workflow Pipeline                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   LOCAL REPOSITORY                              REMOTE REPOSITORY               │
│   ════════════════                              ═════════════════               │
│                                                                                  │
│   ┌──────────────┐                              ┌──────────────┐                │
│   │   ML Code    │  git add                     │   GitHub/    │                │
│   │   + Data     │ ──────────┐                  │   GitLab     │                │
│   │   + Models   │           │                  └──────────────┘                │
│   └──────────────┘           ▼                         ▲                        │
│          │           ┌──────────────┐                  │                        │
│          │           │   Staging    │                  │                        │
│          │           │    Area      │                  │                        │
│          │           └──────────────┘                  │                        │
│          │                   │                         │                        │
│          │                   │ git commit              │ git push               │
│          │                   ▼                         │                        │
│          │           ┌──────────────┐                  │                        │
│          │           │    Local     │──────────────────┘                        │
│          │           │  Repository  │                                           │
│          │           │  (versions)  │                                           │
│          │           └──────────────┘                                           │
│          │                                                                      │
│   ┌──────────────────────────────────────────────────────────────────────┐     │
│   │                    ML Project Components                              │     │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │     │
│   │  │  Data   │  │ Feature │  │  Model  │  │  Eval   │  │ Config  │    │     │
│   │  │ Loading │─▶│Engineer │─▶│Training │─▶│ Metrics │─▶│  Files  │    │     │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │     │
│   └──────────────────────────────────────────────────────────────────────┘     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 โครงสร้างโปรเจค ML ที่จะสร้าง

```
ml-git-lab03_advance/
├── src/
│   ├── data_loader.py       # โหลดข้อมูล
│   ├── train.py             # training model
│   └── evaluate.py          # ประเมินผล model
├── config/
│   └── model_config.yaml    # ค่า hyperparameters
├── data/                    # เก็บข้อมูล (ไม่ track ไฟล์ใหญ่)
├── models/                  # เก็บ trained models (ไม่ track)
├── results/                 # ผลการทดลอง (ไม่ track)
├── requirements.txt         # dependencies
├── .gitignore              # กำหนดไฟล์ที่ไม่ต้อง track
└── README.md               # คำอธิบายโปรเจค
```

---

## 🎯 วัตถุประสงค์การเรียนรู้

1. เข้าใจการจัดโครงสร้างโปรเจค ML ที่เหมาะสมกับ Git
2. เรียนรู้การใช้ `.gitignore` สำหรับ ML project
3. ฝึกใช้ Git workflow กับ sklearn และ data pipeline
4. เข้าใจการ version control สำหรับ ML experiments

---

## ⚙️ Git Configuration (ทำครั้งเดียวก่อนเริ่ม Lab)

```bash
# ตั้งค่าชื่อผู้ใช้
git config --global user.name "Your Name"

# ตั้งค่าอีเมล
git config --global user.email "your.email@example.com"

# ตั้งค่า default branch เป็น main
git config --global init.defaultBranch main

# ตรวจสอบการตั้งค่า
git config --list
```

---

## 🚀 Part 1: สร้างโครงสร้างโปรเจค

### Step 1: สร้างโฟลเดอร์โปรเจค

```bash
mkdir ml-git-lab03_advance
cd ml-git-lab03_advance
```

---

### Step 2: เริ่มต้น Git Repository

```bash
git init
```

**ตัวอย่างผลลัพธ์:**
```
Initialized empty Git repository in /home/student/ml-git-lab03_advance/.git/
```

---

### Step 3: สร้างโครงสร้างโฟลเดอร์

```bash
mkdir -p src config data models results
```

---

### Step 4: สร้างไฟล์ .gitignore

> 📝 **ทำไมต้องมี .gitignore?**  
> ในโปรเจค ML มีไฟล์ที่ไม่ควร track เช่น ไฟล์ข้อมูลขนาดใหญ่ และ model files เพราะ:
> - ไฟล์ใหญ่ทำให้ repository ช้า
> - ไฟล์เหล่านี้สามารถ generate ใหม่ได้จาก code

```bash
cat > .gitignore << 'EOF'
# Python cache
__pycache__/
*.pyc

# Data files (ไฟล์ข้อมูลขนาดใหญ่)
data/*.csv
data/*.pkl

# Model files (ไฟล์ model)
models/*.pkl
models/*.joblib

# Results (ผลลัพธ์ที่ generate ใหม่ได้)
results/*.png
results/*.json

# Keep folder structure
!data/.gitkeep
!models/.gitkeep
!results/.gitkeep
EOF
```

---

### Step 5: สร้าง .gitkeep เพื่อรักษาโฟลเดอร์ว่าง

> 📝 **ทำไมต้องมี .gitkeep?**  
> Git ไม่ track โฟลเดอร์ว่าง ดังนั้นใช้ไฟล์เปล่านี้เพื่อรักษาโครงสร้าง

```bash
touch data/.gitkeep models/.gitkeep results/.gitkeep
```

---

### Step 6: สร้าง requirements.txt

```bash
cat > requirements.txt << 'EOF'
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
pyyaml>=6.0
joblib>=1.3.0
EOF
```

---

### Step 7: สร้าง README.md

> 📝 **README.md คืออะไร?**  
> เป็นไฟล์อธิบายโปรเจคที่จะแสดงหน้าแรกใน GitHub ช่วยให้คนอื่นเข้าใจโปรเจคได้เร็ว

```bash
cat > README.md << 'ENDOFFILE'
# ML Git Lab 03 - Iris Classification

## รายละเอียดโปรเจค
โปรเจคนี้สาธิตการใช้ Git กับ Machine Learning โดยใช้ Iris dataset

## วิธีใช้งาน

    # ติดตั้ง dependencies
    pip install -r requirements.txt

    # Train model
    python src/train.py

    # Evaluate model
    python src/evaluate.py

## Dataset
- ชื่อ: Iris Dataset
- Features: 4 (ความยาว/ความกว้างของกลีบดอกและกลีบเลี้ยง)
- Classes: 3 ชนิด (setosa, versicolor, virginica)
ENDOFFILE
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat README.md
```

**ตัวอย่างผลลัพธ์:**
```
# ML Git Lab 03 - Iris Classification

## รายละเอียดโปรเจค
โปรเจคนี้สาธิตการใช้ Git กับ Machine Learning โดยใช้ Iris dataset

## วิธีใช้งาน

    # ติดตั้ง dependencies
    pip install -r requirements.txt
...
```

---

### Step 8: Commit ครั้งแรก

**ตรวจสอบสถานะ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main

No commits yet

Untracked files:
        .gitignore
        README.md
        data/
        models/
        requirements.txt
        results/
```

**เพิ่มไฟล์และ commit:**
```bash
git add .
git commit -m "Initial commit: สร้างโครงสร้างโปรเจค ML"
```

**ตัวอย่างผลลัพธ์:**
```
[main (root-commit) a1b2c3d] Initial commit: สร้างโครงสร้างโปรเจค ML
 6 files changed, 45 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 data/.gitkeep
 create mode 100644 models/.gitkeep
 create mode 100644 requirements.txt
 create mode 100644 results/.gitkeep
```

---

## 📊 Part 2: สร้าง Data Loader

### Step 9: สร้าง data_loader.py

> 📝 **Module นี้ทำอะไร?**  
> โหลด Iris dataset จาก sklearn และแบ่งข้อมูลเป็น train/test

```bash
cat > src/data_loader.py << 'EOF'
"""
Data Loader Module - โหลดและเตรียมข้อมูล Iris
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def load_data():
    """โหลด Iris dataset"""
    iris = load_iris()
    print(f"โหลดข้อมูลสำเร็จ: {iris.data.shape[0]} ตัวอย่าง, {iris.data.shape[1]} features")
    return iris.data, iris.target, iris.feature_names, iris.target_names


def split_data(X, y, test_size=0.2, random_state=42):
    """แบ่งข้อมูลเป็น train และ test"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"แบ่งข้อมูล: Train={len(X_train)}, Test={len(X_test)}")
    return X_train, X_test, y_train, y_test


# ทดสอบเมื่อรันไฟล์นี้โดยตรง
if __name__ == "__main__":
    X, y, feature_names, target_names = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Features: {feature_names}")
    print(f"Classes: {list(target_names)}")
EOF
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat src/data_loader.py
```

---

### Step 10: ทดสอบ data_loader.py

```bash
python src/data_loader.py
```

**ตัวอย่างผลลัพธ์:**
```
โหลดข้อมูลสำเร็จ: 150 ตัวอย่าง, 4 features
แบ่งข้อมูล: Train=120, Test=30
Features: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
Classes: ['setosa', 'versicolor', 'virginica']
```

---

### Step 11: Commit Data Loader

```bash
git add src/data_loader.py
git commit -m "Add data_loader: โหลดและแบ่งข้อมูล Iris"
```

**ตัวอย่างผลลัพธ์:**
```
[main b2c3d4e] Add data_loader: โหลดและแบ่งข้อมูล Iris
 1 file changed, 25 insertions(+)
 create mode 100644 src/data_loader.py
```

---

## ⚙️ Part 3: สร้าง Config และ Training Module

### Step 12: สร้าง model_config.yaml

> 📝 **ทำไมต้องแยก config เป็นไฟล์?**  
> - ง่ายต่อการเปลี่ยน hyperparameters โดยไม่ต้องแก้ code
> - Git สามารถ track การเปลี่ยนแปลง config ได้
> - สามารถย้อนกลับไปดู config ของการทดลองก่อนหน้าได้

```bash
cat > config/model_config.yaml << 'EOF'
# ==========================================
# Model Configuration
# ==========================================

# การแบ่งข้อมูล
data:
  test_size: 0.2
  random_state: 42

# ประเภท model ที่ใช้
model:
  type: random_forest

  # Random Forest parameters
  random_forest:
    n_estimators: 100
    max_depth: 5
    random_state: 42

  # SVM parameters
  svm:
    C: 1.0
    kernel: rbf
    random_state: 42

# การ training
training:
  cross_validation: true
  cv_folds: 5

# output (path relative จาก src/)
output:
  model_path: ../models/model.joblib
  results_path: ../results/metrics.json
EOF
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat config/model_config.yaml
```

---

### Step 13: สร้าง train.py

> 📝 **Module นี้ทำอะไร?**  
> - อ่าน config จาก YAML file
> - โหลดข้อมูลและ scale features
> - Train model ตาม config
> - บันทึก model ไว้ใช้ต่อ

```bash
cat > src/train.py << 'EOF'
"""
Training Module - Train ML model ตาม config
"""
import yaml
import joblib
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

from data_loader import load_data, split_data


def load_config(path='../config/model_config.yaml'):
    """อ่าน config จากไฟล์ YAML"""
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    print(f"โหลด config จาก {path}")
    return config


def create_model(config):
    """สร้าง model ตาม config"""
    model_type = config['model']['type']
    
    if model_type == 'random_forest':
        params = config['model']['random_forest']
        model = RandomForestClassifier(**params)
    elif model_type == 'svm':
        params = config['model']['svm']
        model = SVC(**params)
    else:
        raise ValueError(f"ไม่รู้จัก model: {model_type}")
    
    print(f"สร้าง {model_type} model")
    return model


def main():
    print("=" * 50)
    print("เริ่มต้น Training Pipeline")
    print("=" * 50)
    
    # 1. โหลด config
    config = load_config()
    
    # 2. โหลดข้อมูล
    X, y, feature_names, target_names = load_data()
    X_train, X_test, y_train, y_test = split_data(
        X, y, 
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    
    # 3. Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Scale features เรียบร้อย")
    
    # 4. สร้างและ train model
    model = create_model(config)
    
    # Cross-validation
    if config['training']['cross_validation']:
        cv_scores = cross_val_score(
            model, X_train_scaled, y_train, 
            cv=config['training']['cv_folds']
        )
        print(f"Cross-validation: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    # Train final model
    model.fit(X_train_scaled, y_train)
    
    # 5. ประเมินผล
    train_acc = model.score(X_train_scaled, y_train)
    test_acc = model.score(X_test_scaled, y_test)
    print(f"Train Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    
    # 6. บันทึก model
    model_data = {
        'model': model,
        'scaler': scaler,
        'config': config,
        'feature_names': feature_names,
        'target_names': list(target_names),
        'timestamp': datetime.now().isoformat()
    }
    joblib.dump(model_data, config['output']['model_path'])
    print(f"บันทึก model ที่ {config['output']['model_path']}")
    
    print("=" * 50)
    print("Training เสร็จสิ้น!")
    print("=" * 50)


if __name__ == "__main__":
    main()
EOF
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat src/train.py
```

---

### Step 14: ทดสอบ train.py

```bash
cd src
python train.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
==================================================
เริ่มต้น Training Pipeline
==================================================
โหลด config จาก ../config/model_config.yaml
โหลดข้อมูลสำเร็จ: 150 ตัวอย่าง, 4 features
แบ่งข้อมูล: Train=120, Test=30
Scale features เรียบร้อย
สร้าง random_forest model
Cross-validation: 0.9417 (+/- 0.0385)
Train Accuracy: 1.0000
Test Accuracy: 0.9667
บันทึก model ที่ ../models/model.joblib
==================================================
Training เสร็จสิ้น!
==================================================
```

---

### Step 15: ตรวจสอบว่า .gitignore ทำงาน

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Untracked files:
        config/model_config.yaml
        src/train.py
```

> 📝 **สังเกต:** ไฟล์ `models/model.joblib` ไม่แสดง เพราะถูก ignore แล้ว!

**ดูไฟล์ที่ถูก ignore:**
```bash
git status --ignored
```

**ตัวอย่างผลลัพธ์:**
```
Ignored files:
        models/model.joblib
        src/__pycache__/
```

---

### Step 16: Commit Training Module

```bash
git add config/model_config.yaml src/train.py
git commit -m "Add training pipeline พร้อม config file"
```

**ตัวอย่างผลลัพธ์:**
```
[main c3d4e5f] Add training pipeline พร้อม config file
 2 files changed, 95 insertions(+)
 create mode 100644 config/model_config.yaml
 create mode 100644 src/train.py
```

---

## 📈 Part 4: สร้าง Evaluation Module

### Step 17: สร้าง evaluate.py

> 📝 **Module นี้ทำอะไร?**  
> - โหลด model ที่ train ไว้
> - คำนวณ metrics ต่างๆ
> - สร้าง confusion matrix plot

```bash
cat > src/evaluate.py << 'EOF'
"""
Evaluation Module - ประเมินผล ML model
"""
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from data_loader import load_data, split_data


def load_model(path):
    """โหลด model จากไฟล์"""
    model_data = joblib.load(path)
    print(f"โหลด model จาก {path}")
    print(f"  - ประเภท: {type(model_data['model']).__name__}")
    print(f"  - Train เมื่อ: {model_data['timestamp']}")
    return model_data


def evaluate(model, X_test, y_test, target_names):
    """ประเมินผล model"""
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    return metrics, y_pred


def plot_confusion_matrix(cm, target_names, save_path):
    """สร้าง confusion matrix plot"""
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    
    # แสดงตัวเลขในแต่ละช่อง
    for i in range(len(target_names)):
        for j in range(len(target_names)):
            plt.text(j, i, str(cm[i][j]), ha='center', va='center',
                    color='white' if cm[i][j] > cm.max()/2 else 'black')
    
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"บันทึก confusion matrix ที่ {save_path}")


def main():
    print("=" * 50)
    print("เริ่มต้น Evaluation Pipeline")
    print("=" * 50)
    
    # 1. โหลด model
    model_data = load_model('../models/model.joblib')
    model = model_data['model']
    scaler = model_data['scaler']
    config = model_data['config']
    target_names = model_data['target_names']
    
    # 2. โหลดข้อมูล (ใช้ random_state เดียวกับตอน train)
    X, y, _, _ = load_data()
    _, X_test, _, y_test = split_data(
        X, y,
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    
    # 3. Scale ข้อมูล
    X_test_scaled = scaler.transform(X_test)
    
    # 4. ประเมินผล
    metrics, y_pred = evaluate(model, X_test_scaled, y_test, target_names)
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")
    
    # 5. สร้าง confusion matrix plot
    cm = np.array(metrics['confusion_matrix'])
    plot_confusion_matrix(cm, target_names, '../results/confusion_matrix.png')
    
    # 6. บันทึกผลลัพธ์
    results = {
        'accuracy': metrics['accuracy'],
        'model_type': config['model']['type'],
        'timestamp': datetime.now().isoformat()
    }
    with open('../results/metrics.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"บันทึกผลลัพธ์ที่ ../results/metrics.json")
    
    print("=" * 50)
    print("Evaluation เสร็จสิ้น!")
    print("=" * 50)


if __name__ == "__main__":
    main()
EOF
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat src/evaluate.py
```

---

### Step 18: ทดสอบ evaluate.py

```bash
cd src
python evaluate.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
==================================================
เริ่มต้น Evaluation Pipeline
==================================================
โหลด model จาก ../models/model.joblib
  - ประเภท: RandomForestClassifier
  - Train เมื่อ: 2024-12-16T10:30:00
โหลดข้อมูลสำเร็จ: 150 ตัวอย่าง, 4 features
แบ่งข้อมูล: Train=120, Test=30

Classification Report:
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       0.91      1.00      0.95        10
   virginica       1.00      0.90      0.95        10

    accuracy                           0.97        30

Test Accuracy: 0.9667
บันทึก confusion matrix ที่ ../results/confusion_matrix.png
บันทึกผลลัพธ์ที่ ../results/metrics.json
==================================================
Evaluation เสร็จสิ้น!
==================================================
```

---

### Step 19: Commit Evaluation Module

```bash
git add src/evaluate.py
git commit -m "Add evaluation module พร้อม confusion matrix plot"
```

**ตัวอย่างผลลัพธ์:**
```
[main d4e5f6g] Add evaluation module พร้อม confusion matrix plot
 1 file changed, 85 insertions(+)
 create mode 100644 src/evaluate.py
```

---

## 🌐 Part 5: การทำงานกับ Remote Repository

### Step 20: ดู Commit History

```bash
git log --oneline
```

**ตัวอย่างผลลัพธ์:**
```
d4e5f6g (HEAD -> main) Add evaluation module พร้อม confusion matrix plot
c3d4e5f Add training pipeline พร้อม config file
b2c3d4e Add data_loader: โหลดและแบ่งข้อมูล Iris
a1b2c3d Initial commit: สร้างโครงสร้างโปรเจค ML
```

---

### Step 21: สร้าง Repository บน GitHub

**ทำตามขั้นตอนนี้:**
1. ไปที่ https://github.com
2. คลิก **"New repository"**
3. ตั้งชื่อ `ml-git-lab03_advance`
4. **ไม่ต้อง** เลือก "Add a README file" (เพราะเรามีแล้ว)
5. คลิก **"Create repository"**

---

### Step 22: เชื่อมต่อกับ Remote และ Push

```bash
# เพิ่ม remote (แทน YOUR_USERNAME ด้วย username ของนักศึกษา)
git remote add origin https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git

# ตรวจสอบ remote
git remote -v

# Push ขึ้น GitHub
git push -u origin main
```

**ตัวอย่างผลลัพธ์:**
```
origin  https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git (fetch)
origin  https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git (push)

Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Writing objects: 100% (15/15), 3.5 KiB | 1.75 MiB/s, done.
To https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

## 🔄 Part 6: ทดลองเปลี่ยน Model (Experiment)

> 📝 **สถานการณ์:** เราต้องการทดลองเปลี่ยนจาก Random Forest เป็น SVM

### Step 23: แก้ไข config เปลี่ยนเป็น SVM

```bash
cat > config/model_config.yaml << 'EOF'
# ==========================================
# Model Configuration
# EXPERIMENT: เปลี่ยนจาก Random Forest เป็น SVM
# ==========================================

data:
  test_size: 0.2
  random_state: 42

model:
  type: svm

  random_forest:
    n_estimators: 100
    max_depth: 5
    random_state: 42

  svm:
    C: 1.0
    kernel: rbf
    random_state: 42

training:
  cross_validation: true
  cv_folds: 5

output:
  model_path: ../models/model.joblib
  results_path: ../results/metrics.json
EOF
```

---

### Step 24: ดูการเปลี่ยนแปลงด้วย git diff

```bash
git diff config/model_config.yaml
```

**ตัวอย่างผลลัพธ์:**
```diff
@@ -1,12 +1,13 @@
 # ==========================================
 # Model Configuration
+# EXPERIMENT: เปลี่ยนจาก Random Forest เป็น SVM
 # ==========================================
 
 data:
   test_size: 0.2
   random_state: 42
 
 model:
-  type: random_forest
+  type: svm
```

> 📝 **อ่าน diff:**
> - บรรทัดที่ขึ้นต้นด้วย `-` คือถูกลบ
> - บรรทัดที่ขึ้นต้นด้วย `+` คือถูกเพิ่ม

---

### Step 25: Train และ Evaluate ใหม่

```bash
cd src
python train.py
python evaluate.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
สร้าง svm model
Cross-validation: 0.9583 (+/- 0.0527)
Test Accuracy: 0.9667
```

---

### Step 26: Commit การทดลอง

```bash
git add config/model_config.yaml
git commit -m "Experiment: เปลี่ยนจาก RandomForest เป็น SVM"
```

**ตัวอย่างผลลัพธ์:**
```
[main e5f6g7h] Experiment: เปลี่ยนจาก RandomForest เป็น SVM
 1 file changed, 2 insertions(+), 1 deletion(-)
```

---

### Step 27: Push ขึ้น Remote

```bash
git push
```

**ตัวอย่างผลลัพธ์:**
```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Writing objects: 100% (4/4), 456 bytes | 456.00 KiB/s, done.
To https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git
   d4e5f6g..e5f6g7h  main -> main
```

---

## 🔍 Part 7: การดูและกู้คืน Config เวอร์ชันเก่า

### Step 28: ดูประวัติการเปลี่ยนแปลง config

```bash
git log --oneline config/model_config.yaml
```

**ตัวอย่างผลลัพธ์:**
```
e5f6g7h (HEAD -> main) Experiment: เปลี่ยนจาก RandomForest เป็น SVM
c3d4e5f Add training pipeline พร้อม config file
```

---

### Step 29: ดู config เวอร์ชันก่อนหน้า (Random Forest)

> 📝 **ใช้ git show เพื่อดูไฟล์โดยไม่เปลี่ยน working directory**

```bash
git show c3d4e5f:config/model_config.yaml
```

**ตัวอย่างผลลัพธ์:**
```yaml
# ==========================================
# Model Configuration
# ==========================================

...
model:
  type: random_forest
...
```

> 📝 **สังเกต:** เห็นว่าเวอร์ชันก่อนใช้ `type: random_forest`

---

### Step 30: กู้คืน config เวอร์ชัน Random Forest (ถ้าต้องการ)

```bash
# ดึง config เวอร์ชันเก่ามา
git checkout c3d4e5f -- config/model_config.yaml

# ตรวจสอบว่าเปลี่ยนแล้ว
cat config/model_config.yaml | grep "type:"
```

**ตัวอย่างผลลัพธ์:**
```
  type: random_forest
```

**ถ้าไม่ต้องการเปลี่ยน ยกเลิกด้วย:**
```bash
git restore config/model_config.yaml
```

---

## 📊 Part 8: สรุปคำสั่งที่เรียนรู้

### คำสั่ง Git พื้นฐาน

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git init` | สร้าง repository ใหม่ |
| `git add <file>` | เพิ่มไฟล์เข้า staging |
| `git add .` | เพิ่มทุกไฟล์ |
| `git commit -m "msg"` | บันทึกการเปลี่ยนแปลง |
| `git status` | ตรวจสอบสถานะ |
| `git status --ignored` | ดูไฟล์ที่ถูก ignore |
| `git log --oneline` | ดูประวัติ commit |
| `git diff <file>` | ดูการเปลี่ยนแปลง |

### คำสั่ง Remote

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git remote add origin <url>` | เพิ่ม remote |
| `git push -u origin main` | push ครั้งแรก |
| `git push` | push (หลังตั้ง upstream) |
| `git pull` | ดึงการเปลี่ยนแปลงจาก remote |

### คำสั่งดูและกู้คืนไฟล์

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git log --oneline <file>` | ดูประวัติของไฟล์ |
| `git show <commit>:<file>` | ดูไฟล์เวอร์ชันเก่า |
| `git checkout <commit> -- <file>` | กู้คืนไฟล์เวอร์ชันเก่า |
| `git restore <file>` | ยกเลิกการเปลี่ยนแปลง |

---

## 🎯 Best Practices สำหรับ ML Project กับ Git

### 1. โครงสร้างที่ดี
```
project/
├── src/           # โค้ด ✅ track
├── config/        # config ✅ track
├── data/          # ข้อมูล ❌ ignore ไฟล์ใหญ่
├── models/        # models ❌ ignore
├── results/       # ผลลัพธ์ ❌ ignore
└── .gitignore     # กำหนดไฟล์ที่ไม่ track
```

### 2. สิ่งที่ควร Track
- ✅ Source code (.py)
- ✅ Config files (.yaml, .json)
- ✅ Requirements.txt
- ✅ README.md
- ✅ .gitignore

### 3. สิ่งที่ไม่ควร Track
- ❌ ไฟล์ข้อมูลขนาดใหญ่ (.csv, .parquet)
- ❌ Model files (.pkl, .joblib, .h5)
- ❌ ผลลัพธ์ที่ generate ใหม่ได้ (.png, results)
- ❌ Python cache (__pycache__)

### 4. Commit Message ที่ดี
```
✅ "Add data_loader: โหลดและแบ่งข้อมูล Iris"
✅ "Add training pipeline พร้อม config file"
✅ "Experiment: เปลี่ยนจาก RandomForest เป็น SVM"
✅ "Fix: แก้ bug ใน feature scaling"

❌ "update"
❌ "fix bug"
❌ "asdfgh"
```


---

## 🧹 ทำความสะอาด (Optional)

```bash
cd ..
rm -rf ml-git-lab03_advance
```

---

## 📚 อ้างอิงเพิ่มเติม

- [Git Documentation](https://git-scm.com/doc)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [MLOps Principles](https://ml-ops.org/)
- [DVC - Data Version Control](https://dvc.org/) (สำหรับจัดการ data และ model ขนาดใหญ่)