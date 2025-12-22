# 🧪 LAB: MLOps with Scikit-Learn และ Git Branch Workflow

## 📋 วัตถุประสงค์การเรียนรู้

หลังจากทำ LAB นี้เสร็จ นักศึกษาจะสามารถ:
- ✅ สร้างโปรเจกต์ Machine Learning ด้วย Scikit-Learn
- ✅ ใช้งาน Git Branch สำหรับการทดลอง ML Models ต่างๆ
- ✅ จัดการ Feature Engineering ใน Branch แยก
- ✅ ใช้ Pipeline ใน Linux สำหรับการวิเคราะห์ผลลัพธ์
- ✅ ใช้ `tree` ตรวจสอบโครงสร้างโปรเจกต์ ML
- ✅ ใช้ Here Document สร้างไฟล์ Python และ Config
- ✅ ติดตาม Model Experiments ด้วย Git
- ✅ เข้าใจ MLOps Workflow พื้นฐาน

---

## 📚 ความรู้พื้นฐาน

### MLOps คืออะไร?

**MLOps** (Machine Learning Operations) คือแนวปฏิบัติที่รวม ML, DevOps และ Data Engineering เข้าด้วยกัน เพื่อ:
- จัดการ ML Models อย่างเป็นระบบ
- ทำให้การ Deploy และ Monitor เป็นไปอย่างราบรื่น
- ติดตาม Experiments และ Versions

```
┌─────────────────────────────────────────────────────────────┐
│                      MLOps Lifecycle                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Data → Feature Engineering → Model Training → Evaluation  │
│     ↑                                                   ↓    │
│     └──────────── Monitoring ←── Deployment ←───────────┘   │
│                                                              │
│   🔧 Git: Version Control สำหรับทุกขั้นตอน                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### ทำไมต้องใช้ Git Branch กับ ML Projects?

| สถานการณ์ | Branch ที่ใช้ | ประโยชน์ |
|-----------|--------------|---------|
| ทดลอง Model ใหม่ | `experiment/random-forest` | ไม่กระทบ code หลัก |
| Feature Engineering | `feature/scaling-normalization` | พัฒนาแยก merge ทีหลัง |
| Hyperparameter Tuning | `tune/grid-search-rf` | เก็บ config แต่ละครั้ง |
| Bug Fix | `fix/data-leakage` | แก้ไขโดยไม่กระทบการทดลอง |

---

## 🔧 ความรู้เบื้องต้น: Pipeline ใน Linux สำหรับ ML

### Pipeline (`|`) คืออะไร?

**Pipeline** คือการส่งผลลัพธ์จากคำสั่งหนึ่งไปเป็น input ของอีกคำสั่งหนึ่ง โดยใช้เครื่องหมาย `|` (pipe)

```
คำสั่งที่ 1  |  คำสั่งที่ 2  |  คำสั่งที่ 3
    ↓              ↓              ↓
  output    →    input     →   output
            →              →    input
                           →   output (สุดท้าย)
```

### ตัวอย่าง Pipeline สำหรับ ML Projects

```bash
# ตัวอย่างที่ 1: นับจำนวน Python files
ls *.py | wc -l
```

**อธิบายทีละขั้นตอน:**
```
ls *.py         →  แสดงไฟล์ .py ทั้งหมด
                   train.py
                   model.py
                   evaluate.py
        |
        ↓
wc -l           →  นับจำนวนบรรทัด
                   ผลลัพธ์: 3
```

```bash
# ตัวอย่างที่ 2: ค้นหา experiments branches
git branch | grep "experiment"
```

**อธิบายทีละขั้นตอน:**
```
git branch      →  แสดงรายชื่อ branch
                   * main
                     experiment/random-forest
                     experiment/svm
                     feature/scaling
        |
        ↓
grep "experiment" →  กรองเฉพาะบรรทัดที่มี "experiment"
                      ผลลัพธ์:
                        experiment/random-forest
                        experiment/svm
```

```bash
# ตัวอย่างที่ 3: ดู commit ที่เกี่ยวกับ model
git log --oneline | grep -i "model" | head -5
```

```bash
# ตัวอย่างที่ 4: นับจำนวน experiment branches
git branch | grep "experiment" | wc -l
```

### สรุปคำสั่งที่ใช้บ่อยกับ Pipeline

| คำสั่ง | หน้าที่ | ตัวอย่าง |
|--------|--------|----------|
| `grep "text"` | กรองบรรทัดที่มีข้อความ | `cat log.txt \| grep "accuracy"` |
| `wc -l` | นับจำนวนบรรทัด | `ls *.py \| wc -l` |
| `head -n` | เอา n บรรทัดแรก | `cat results.csv \| head -10` |
| `tail -n` | เอา n บรรทัดสุดท้าย | `cat training.log \| tail -20` |
| `sort` | เรียงลำดับ | `cat scores.txt \| sort -n` |
| `cut -d, -f1` | ตัดคอลัมน์จาก CSV | `cat data.csv \| cut -d, -f1` |

---

## 🔧 ความรู้เบื้องต้น: Here Document (Heredoc)

### Here Document คืออะไร?

**Here Document** คือวิธีการเขียนข้อความหลายบรรทัดลงไฟล์โดยไม่ต้องกด Ctrl+D

```bash
cat > ชื่อไฟล์ << 'EOF'
เนื้อหาบรรทัดที่ 1
เนื้อหาบรรทัดที่ 2
เนื้อหาบรรทัดที่ 3
EOF
```

**อธิบาย:**
- `cat > ชื่อไฟล์` = สร้างไฟล์ใหม่
- `<< 'EOF'` = เริ่มต้น Here Document (EOF = End Of File, ใช้คำอื่นก็ได้)
- `EOF` = สิ้นสุด Here Document

### เปรียบเทียบวิธีสร้างไฟล์

| วิธี | ข้อดี | ข้อเสีย |
|------|-------|---------|
| `echo "text" > file` | ง่าย รวดเร็ว | เขียนได้แค่บรรทัดเดียว |
| `cat > file` แล้ว Ctrl+D | เขียนได้หลายบรรทัด | ต้องจำกด Ctrl+D |
| `cat > file << 'EOF'` | เขียนได้หลายบรรทัด, ชัดเจน | พิมพ์ยาวกว่า |

---

## 🛠️ เตรียมความพร้อม

### ขั้นตอนที่ 1: ตั้งค่า Git (ถ้ายังไม่เคยตั้ง)

```bash
# ตั้งค่าชื่อผู้ใช้
git config --global user.name "ชื่อของคุณ"

# ตั้งค่าอีเมล
git config --global user.email "your.email@example.com"

# ตรวจสอบการตั้งค่า
git config --list
```

### ขั้นตอนที่ 2: สร้างโปรเจกต์ ML สำหรับฝึก

```bash
# สร้างโฟลเดอร์ใหม่
mkdir sklearn-mlops-lab
cd sklearn-mlops-lab

# เริ่มต้น Git repository
git init

# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in /path/to/sklearn-mlops-lab/.git/
```

### ขั้นตอนที่ 3: ตรวจสอบ Python และ Scikit-Learn

```bash
# ตรวจสอบ Python version
python3 --version

# ตรวจสอบ pip
pip3 --version

# ติดตั้ง scikit-learn (ถ้ายังไม่มี)
pip3 install scikit-learn pandas numpy joblib

# ตรวจสอบว่าติดตั้งสำเร็จ
python3 -c "import sklearn; print(f'sklearn version: {sklearn.__version__}')"
```

---

## 📝 แบบฝึกหัดที่ 0: สร้างโครงสร้างโปรเจกต์ ML ด้วย Here Document

### 0.1 สร้างไฟล์ README.md

```bash
cat > README.md << 'EOF'
# Sklearn MLOps Lab
โปรเจกต์สำหรับเรียนรู้ MLOps ด้วย Scikit-Learn และ Git

## 📁 โครงสร้างโปรเจกต์
```
sklearn-mlops-lab/
├── data/           # ข้อมูลสำหรับ training
├── models/         # โมเดลที่ train แล้ว
├── src/            # source code
├── notebooks/      # Jupyter notebooks
├── configs/        # configuration files
├── results/        # ผลลัพธ์การทดลอง
└── tests/          # unit tests
```

## 🎯 เป้าหมาย
- เรียนรู้การใช้ Git Branch กับ ML Projects
- ทดลอง Models หลายๆ แบบใน Branches ต่างๆ
- ติดตาม Experiments อย่างเป็นระบบ

## 👤 ผู้จัดทำ
- นักศึกษา: [ชื่อของคุณ]
- รหัส: [รหัสนักศึกษา]
EOF
```

```bash
# ตรวจสอบไฟล์ที่สร้าง
cat README.md
```

### 0.2 สร้างโครงสร้างโฟลเดอร์

```bash
# สร้างโฟลเดอร์ทั้งหมด
mkdir -p data/raw data/processed
mkdir -p models
mkdir -p src/data src/features src/models src/utils
mkdir -p notebooks
mkdir -p configs
mkdir -p results
mkdir -p tests
```

### 0.3 ใช้ tree ดูโครงสร้างโปรเจกต์

```bash
# ดูโครงสร้างโฟลเดอร์
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── configs
├── data
│   ├── processed
│   └── raw
├── models
├── notebooks
├── results
├── src
│   ├── data
│   ├── features
│   ├── models
│   └── utils
└── tests

13 directories, 1 file
```

### 0.4 สร้างไฟล์ requirements.txt

```bash
cat > requirements.txt << 'EOF'
# Core ML Libraries
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0

# Model Persistence
joblib>=1.3.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Utilities
python-dotenv>=1.0.0
PyYAML>=6.0

# Testing
pytest>=7.4.0
EOF
```

### 0.5 สร้างไฟล์ .gitignore สำหรับ ML Projects

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
venv/
.env/
env/

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data files (large files)
data/raw/*.csv
data/raw/*.xlsx
data/processed/*.pkl
*.parquet

# Model files (large files)
models/*.pkl
models/*.joblib
*.h5
*.pt
*.pth

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Results (optional - อาจต้องการ track)
# results/

# Secrets
.env
*.key
EOF
```

### 0.6 สร้างไฟล์ __init__.py สำหรับ packages

```bash
# สร้าง __init__.py ในทุก package
touch src/__init__.py
touch src/data/__init__.py
touch src/features/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

### 0.7 ดูโครงสร้างโปรเจกต์ที่สมบูรณ์

```bash
# ดูโครงสร้างพร้อมไฟล์
tree -a -I '.git'
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── .gitignore
├── README.md
├── configs
├── data
│   ├── processed
│   └── raw
├── models
├── notebooks
├── requirements.txt
├── results
├── src
│   ├── __init__.py
│   ├── data
│   │   └── __init__.py
│   ├── features
│   │   └── __init__.py
│   ├── models
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
└── tests
    └── __init__.py
```

---

## 📝 แบบฝึกหัดที่ 1: สร้าง Data Loading Module

### 1.1 สร้างไฟล์ load_data.py

```bash
cat > src/data/load_data.py << 'EOF'
"""
Data Loading Module
โมดูลสำหรับโหลดและจัดการข้อมูล
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split


def load_sklearn_dataset(name: str = 'iris') -> tuple:
    """
    โหลด dataset จาก sklearn
    
    Args:
        name: ชื่อ dataset ('iris', 'wine', 'breast_cancer')
    
    Returns:
        tuple: (X, y, feature_names, target_names)
    """
    datasets = {
        'iris': load_iris,
        'wine': load_wine,
        'breast_cancer': load_breast_cancer
    }
    
    if name not in datasets:
        raise ValueError(f"Dataset '{name}' not found. Available: {list(datasets.keys())}")
    
    data = datasets[name]()
    
    print(f"✓ Loaded {name} dataset")
    print(f"  Samples: {data.data.shape[0]}")
    print(f"  Features: {data.data.shape[1]}")
    print(f"  Classes: {len(data.target_names)}")
    
    return data.data, data.target, data.feature_names, data.target_names


def split_data(X, y, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    แบ่งข้อมูลเป็น train และ test sets
    
    Args:
        X: features
        y: targets
        test_size: สัดส่วนของ test set
        random_state: seed สำหรับ reproducibility
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"✓ Data split completed")
    print(f"  Train: {X_train.shape[0]} samples")
    print(f"  Test: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test


def create_dataframe(X, y, feature_names) -> pd.DataFrame:
    """
    สร้าง DataFrame จาก numpy arrays
    """
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    return df


if __name__ == "__main__":
    # ทดสอบ module
    X, y, features, targets = load_sklearn_dataset('iris')
    X_train, X_test, y_train, y_test = split_data(X, y)
    df = create_dataframe(X, y, features)
    print(f"\n📊 DataFrame shape: {df.shape}")
    print(df.head())
EOF
```

### 1.2 ทดสอบ Data Loading Module

```bash
# รัน module
python3 src/data/load_data.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
✓ Loaded iris dataset
  Samples: 150
  Features: 4
  Classes: 3
✓ Data split completed
  Train: 120 samples
  Test: 30 samples

📊 DataFrame shape: (150, 5)
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  target
0                5.1               3.5                1.4               0.2       0
1                4.9               3.0                1.4               0.2       0
2                4.7               3.2                1.3               0.2       0
3                4.6               3.1                1.5               0.2       0
4                5.0               3.6                1.4               0.2       0
```

### 1.3 Commit Initial Structure

```bash
# ดูสถานะ
git status

# เพิ่มไฟล์ทั้งหมด
git add .

# Commit ครั้งแรก
git commit -m "Initial commit: สร้างโครงสร้าง ML project พร้อม data loading module"

# ดู log
git log --oneline
```

---

## 📝 แบบฝึกหัดที่ 2: สร้าง Feature Engineering Module ใน Branch ใหม่

### 2.1 สร้าง Branch สำหรับ Feature Engineering

```bash
# สร้าง branch ใหม่และสลับไป
git switch -c feature/preprocessing

# ตรวจสอบว่าอยู่ branch ไหน
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
* feature/preprocessing
  main
```

### 2.2 สร้างไฟล์ preprocessing.py

```bash
cat > src/features/preprocessing.py << 'EOF'
"""
Feature Preprocessing Module
โมดูลสำหรับ preprocessing features
"""

import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class FeaturePreprocessor:
    """
    Class สำหรับ preprocessing features
    """
    
    def __init__(self, scaling_method: str = 'standard'):
        """
        Initialize preprocessor
        
        Args:
            scaling_method: วิธีการ scale ('standard', 'minmax', 'robust')
        """
        self.scaling_method = scaling_method
        self.scaler = self._get_scaler()
        self.is_fitted = False
    
    def _get_scaler(self):
        """เลือก scaler ตาม method ที่กำหนด"""
        scalers = {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler(),
            'robust': RobustScaler()
        }
        
        if self.scaling_method not in scalers:
            raise ValueError(f"Unknown scaling method: {self.scaling_method}")
        
        return scalers[self.scaling_method]
    
    def fit(self, X):
        """Fit scaler กับข้อมูล training"""
        self.scaler.fit(X)
        self.is_fitted = True
        print(f"✓ Fitted {self.scaling_method} scaler")
        return self
    
    def transform(self, X):
        """Transform ข้อมูลด้วย scaler ที่ fit แล้ว"""
        if not self.is_fitted:
            raise RuntimeError("Scaler has not been fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(X)
        print(f"✓ Transformed data with {self.scaling_method} scaler")
        return X_scaled
    
    def fit_transform(self, X):
        """Fit และ transform ในขั้นตอนเดียว"""
        self.fit(X)
        return self.transform(X)
    
    def get_stats(self):
        """แสดงสถิติของ scaler"""
        if not self.is_fitted:
            return None
        
        if hasattr(self.scaler, 'mean_'):
            print("\n📊 Scaler Statistics:")
            print(f"  Mean: {self.scaler.mean_}")
            print(f"  Scale: {self.scaler.scale_}")
        elif hasattr(self.scaler, 'data_min_'):
            print("\n📊 Scaler Statistics:")
            print(f"  Min: {self.scaler.data_min_}")
            print(f"  Max: {self.scaler.data_max_}")


def preprocess_pipeline(X_train, X_test, method: str = 'standard'):
    """
    Pipeline สำหรับ preprocessing ข้อมูล
    
    Args:
        X_train: training features
        X_test: test features
        method: scaling method
    
    Returns:
        tuple: (X_train_scaled, X_test_scaled, preprocessor)
    """
    preprocessor = FeaturePreprocessor(scaling_method=method)
    
    # Fit กับ train data เท่านั้น!
    X_train_scaled = preprocessor.fit_transform(X_train)
    
    # Transform test data ด้วย parameters จาก train
    X_test_scaled = preprocessor.transform(X_test)
    
    return X_train_scaled, X_test_scaled, preprocessor


if __name__ == "__main__":
    # ทดสอบ module
    import sys
    sys.path.insert(0, '.')
    from src.data.load_data import load_sklearn_dataset, split_data
    
    # โหลดข้อมูล
    X, y, features, targets = load_sklearn_dataset('iris')
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    print("\n" + "="*50)
    print("Testing StandardScaler")
    print("="*50)
    
    # ทดสอบ StandardScaler
    X_train_scaled, X_test_scaled, preprocessor = preprocess_pipeline(
        X_train, X_test, method='standard'
    )
    
    preprocessor.get_stats()
    
    print(f"\n📈 Original X_train mean: {X_train.mean(axis=0)}")
    print(f"📉 Scaled X_train mean: {X_train_scaled.mean(axis=0)}")
    
    print("\n" + "="*50)
    print("Testing MinMaxScaler")
    print("="*50)
    
    # ทดสอบ MinMaxScaler
    X_train_mm, X_test_mm, _ = preprocess_pipeline(
        X_train, X_test, method='minmax'
    )
    
    print(f"\n📈 MinMax X_train range: [{X_train_mm.min():.2f}, {X_train_mm.max():.2f}]")
EOF
```

### 2.3 ทดสอบ Preprocessing Module

```bash
# รัน module
python3 src/features/preprocessing.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
✓ Loaded iris dataset
  Samples: 150
  Features: 4
  Classes: 3
✓ Data split completed
  Train: 120 samples
  Test: 30 samples

==================================================
Testing StandardScaler
==================================================
✓ Fitted standard scaler
✓ Transformed data with standard scaler
✓ Transformed data with standard scaler

📊 Scaler Statistics:
  Mean: [5.84583333 3.06333333 3.7775     1.20583333]
  Scale: [0.82898063 0.44344109 1.75004544 0.76508862]

📈 Original X_train mean: [5.84583333 3.06333333 3.7775     1.20583333]
📉 Scaled X_train mean: [-1.11022302e-15 -5.62883073e-16  3.28903977e-16  1.11022302e-16]

==================================================
Testing MinMaxScaler
==================================================
✓ Fitted minmax scaler
✓ Transformed data with minmax scaler
✓ Transformed data with minmax scaler

📈 MinMax X_train range: [0.00, 1.00]
```

### 2.4 ใช้ tree ดูโครงสร้างที่เปลี่ยนแปลง

```bash
# ดูเฉพาะ src/features
tree src/features
```

**ผลลัพธ์ที่คาดหวัง:**
```
src/features
├── __init__.py
└── preprocessing.py

0 directories, 2 files
```

### 2.5 Commit และดู Branch

```bash
# ดูสถานะ
git status

# Commit
git add .
git commit -m "feat: เพิ่ม feature preprocessing module พร้อม scalers"

# ดู log
git log --oneline
```

### 2.6 ดู refs ของ Git

```bash
# ดูว่า Git เก็บ branch ไว้ที่ไหน
tree .git/refs/heads
```

**ผลลัพธ์ที่คาดหวัง:**
```
.git/refs/heads
├── feature
│   └── preprocessing
└── main

1 directory, 2 files
```

---

## 📝 แบบฝึกหัดที่ 3: สร้าง Model Training Module ใน Branch ใหม่

### 3.1 กลับไป main และสร้าง branch ใหม่

```bash
# กลับไป main
git switch main

# ดูโครงสร้าง - สังเกตว่า preprocessing.py หายไป
tree src/features

# สร้าง branch ใหม่สำหรับ experiment
git switch -c experiment/logistic-regression

# ตรวจสอบ branches ทั้งหมด
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
* experiment/logistic-regression
  feature/preprocessing
  main
```

### 3.2 สร้างไฟล์ train.py

```bash
cat > src/models/train.py << 'EOF'
"""
Model Training Module
โมดูลสำหรับ training ML models
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from datetime import datetime


class ModelTrainer:
    """
    Class สำหรับ training และ evaluate models
    """
    
    def __init__(self, model_name: str = 'logistic_regression'):
        """
        Initialize trainer
        
        Args:
            model_name: ชื่อ model
        """
        self.model_name = model_name
        self.model = self._get_model()
        self.is_trained = False
        self.training_history = {}
    
    def _get_model(self):
        """สร้าง model instance"""
        if self.model_name == 'logistic_regression':
            return LogisticRegression(max_iter=200, random_state=42)
        else:
            raise ValueError(f"Unknown model: {self.model_name}")
    
    def train(self, X_train, y_train):
        """Train model"""
        print(f"🚀 Training {self.model_name}...")
        
        start_time = datetime.now()
        self.model.fit(X_train, y_train)
        end_time = datetime.now()
        
        self.is_trained = True
        self.training_history['training_time'] = (end_time - start_time).total_seconds()
        self.training_history['n_samples'] = X_train.shape[0]
        self.training_history['n_features'] = X_train.shape[1]
        
        # Train accuracy
        train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, train_pred)
        self.training_history['train_accuracy'] = train_acc
        
        print(f"✓ Training completed in {self.training_history['training_time']:.2f}s")
        print(f"  Train Accuracy: {train_acc:.4f}")
        
        return self
    
    def evaluate(self, X_test, y_test, target_names=None):
        """Evaluate model"""
        if not self.is_trained:
            raise RuntimeError("Model has not been trained. Call train() first.")
        
        print(f"\n📊 Evaluating {self.model_name}...")
        
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        test_acc = accuracy_score(y_test, y_pred)
        self.training_history['test_accuracy'] = test_acc
        
        print(f"  Test Accuracy: {test_acc:.4f}")
        
        # Classification report
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Confusion matrix
        print("🔢 Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return y_pred, test_acc
    
    def save_model(self, filepath: str = None):
        """Save trained model"""
        if not self.is_trained:
            raise RuntimeError("Model has not been trained.")
        
        if filepath is None:
            os.makedirs('models', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f'models/{self.model_name}_{timestamp}.joblib'
        
        joblib.dump({
            'model': self.model,
            'model_name': self.model_name,
            'training_history': self.training_history
        }, filepath)
        
        print(f"✓ Model saved to: {filepath}")
        return filepath
    
    def get_summary(self):
        """แสดงสรุปผลการ training"""
        print("\n" + "="*50)
        print(f"📈 Training Summary: {self.model_name}")
        print("="*50)
        for key, value in self.training_history.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    # ทดสอบ module
    import sys
    sys.path.insert(0, '.')
    from src.data.load_data import load_sklearn_dataset, split_data
    
    # โหลดข้อมูล
    X, y, features, targets = load_sklearn_dataset('iris')
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # สร้างและ train model
    trainer = ModelTrainer('logistic_regression')
    trainer.train(X_train, y_train)
    
    # Evaluate
    y_pred, accuracy = trainer.evaluate(X_test, y_test, target_names=targets)
    
    # แสดงสรุป
    trainer.get_summary()
    
    # Save model
    model_path = trainer.save_model()
EOF
```

### 3.3 ทดสอบ Training Module

```bash
# รัน module
python3 src/models/train.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
✓ Loaded iris dataset
  Samples: 150
  Features: 4
  Classes: 3
✓ Data split completed
  Train: 120 samples
  Test: 30 samples
🚀 Training logistic_regression...
✓ Training completed in 0.02s
  Train Accuracy: 0.9750

📊 Evaluating logistic_regression...
  Test Accuracy: 0.9667

📋 Classification Report:
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       0.91      1.00      0.95        10
   virginica       1.00      0.90      0.95        10

    accuracy                           0.97        30
   macro avg       0.97      0.97      0.97        30
weighted avg       0.97      0.97      0.97        30

🔢 Confusion Matrix:
[[10  0  0]
 [ 0 10  0]
 [ 0  1  9]]

==================================================
📈 Training Summary: logistic_regression
==================================================
  training_time: 0.0234
  n_samples: 120
  n_features: 4
  train_accuracy: 0.9750
  test_accuracy: 0.9667
✓ Model saved to: models/logistic_regression_20241215_143022.joblib
```

### 3.4 ใช้ tree ดูโครงสร้าง

```bash
# ดูโครงสร้างทั้งหมด
tree -I '__pycache__'
```

### 3.5 Commit

```bash
git add .
git commit -m "experiment: เพิ่ม Logistic Regression trainer พร้อม evaluation"

# ดู log ทุก branch
git log --oneline --graph --all
```

---

## 📝 แบบฝึกหัดที่ 4: สร้าง Experiment อื่นๆ ใน Branches แยก

### 4.1 สร้าง Branch สำหรับ Random Forest

```bash
# กลับไป main
git switch main

# สร้าง branch ใหม่
git switch -c experiment/random-forest
```

### 4.2 แก้ไข train.py เพื่อเพิ่ม Random Forest

```bash
cat > src/models/train.py << 'EOF'
"""
Model Training Module
โมดูลสำหรับ training ML models - Random Forest Version
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os
from datetime import datetime


class ModelTrainer:
    """
    Class สำหรับ training และ evaluate models
    """
    
    def __init__(self, model_name: str = 'random_forest', **kwargs):
        """
        Initialize trainer
        
        Args:
            model_name: ชื่อ model
            **kwargs: hyperparameters สำหรับ model
        """
        self.model_name = model_name
        self.hyperparameters = kwargs
        self.model = self._get_model()
        self.is_trained = False
        self.training_history = {}
    
    def _get_model(self):
        """สร้าง model instance"""
        default_params = {
            'n_estimators': 100,
            'max_depth': None,
            'min_samples_split': 2,
            'random_state': 42
        }
        
        # รวม default กับ user params
        params = {**default_params, **self.hyperparameters}
        
        if self.model_name == 'random_forest':
            return RandomForestClassifier(**params)
        else:
            raise ValueError(f"Unknown model: {self.model_name}")
    
    def train(self, X_train, y_train):
        """Train model"""
        print(f"🌲 Training {self.model_name}...")
        print(f"   Hyperparameters: {self.hyperparameters}")
        
        start_time = datetime.now()
        self.model.fit(X_train, y_train)
        end_time = datetime.now()
        
        self.is_trained = True
        self.training_history['training_time'] = (end_time - start_time).total_seconds()
        self.training_history['n_samples'] = X_train.shape[0]
        self.training_history['n_features'] = X_train.shape[1]
        self.training_history['hyperparameters'] = self.hyperparameters
        
        # Train accuracy
        train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, train_pred)
        self.training_history['train_accuracy'] = train_acc
        
        print(f"✓ Training completed in {self.training_history['training_time']:.2f}s")
        print(f"  Train Accuracy: {train_acc:.4f}")
        
        return self
    
    def evaluate(self, X_test, y_test, target_names=None):
        """Evaluate model"""
        if not self.is_trained:
            raise RuntimeError("Model has not been trained. Call train() first.")
        
        print(f"\n📊 Evaluating {self.model_name}...")
        
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        test_acc = accuracy_score(y_test, y_pred)
        self.training_history['test_accuracy'] = test_acc
        
        print(f"  Test Accuracy: {test_acc:.4f}")
        
        # Classification report
        print("\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=target_names))
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            print("\n🎯 Feature Importances:")
            importances = self.model.feature_importances_
            for i, imp in enumerate(importances):
                print(f"  Feature {i}: {imp:.4f}")
        
        return y_pred, test_acc
    
    def save_model(self, filepath: str = None):
        """Save trained model"""
        if not self.is_trained:
            raise RuntimeError("Model has not been trained.")
        
        if filepath is None:
            os.makedirs('models', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f'models/{self.model_name}_{timestamp}.joblib'
        
        joblib.dump({
            'model': self.model,
            'model_name': self.model_name,
            'training_history': self.training_history
        }, filepath)
        
        print(f"✓ Model saved to: {filepath}")
        return filepath
    
    def get_summary(self):
        """แสดงสรุปผลการ training"""
        print("\n" + "="*50)
        print(f"🌲 Training Summary: {self.model_name}")
        print("="*50)
        for key, value in self.training_history.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            elif isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    - {k}: {v}")
            else:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    # ทดสอบ module
    import sys
    sys.path.insert(0, '.')
    from src.data.load_data import load_sklearn_dataset, split_data
    
    # โหลดข้อมูล
    X, y, features, targets = load_sklearn_dataset('iris')
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # ทดลอง hyperparameters ต่างๆ
    experiments = [
        {'n_estimators': 50, 'max_depth': 3},
        {'n_estimators': 100, 'max_depth': 5},
        {'n_estimators': 200, 'max_depth': None}
    ]
    
    results = []
    
    for exp in experiments:
        print("\n" + "="*60)
        trainer = ModelTrainer('random_forest', **exp)
        trainer.train(X_train, y_train)
        y_pred, accuracy = trainer.evaluate(X_test, y_test, target_names=targets)
        results.append({
            'params': exp,
            'test_accuracy': accuracy
        })
    
    # สรุปผลทั้งหมด
    print("\n" + "="*60)
    print("📊 EXPERIMENT SUMMARY")
    print("="*60)
    for i, result in enumerate(results):
        print(f"\nExperiment {i+1}:")
        print(f"  Params: {result['params']}")
        print(f"  Test Accuracy: {result['test_accuracy']:.4f}")
EOF
```

### 4.3 ทดสอบ Random Forest

```bash
python3 src/models/train.py
```

### 4.4 Commit

```bash
git add .
git commit -m "experiment: ทดลอง Random Forest กับ hyperparameters ต่างๆ"
```

### 4.5 ดู branches ทั้งหมด

```bash
# ดู branches ทั้งหมด
git branch -v

# ใช้ Pipeline นับ experiment branches
git branch | grep "experiment" | wc -l

# ดู log ทุก branch
git log --oneline --graph --all --decorate
```

**ผลลัพธ์ที่คาดหวัง:**
```
* def5678 (HEAD -> experiment/random-forest) experiment: ทดลอง Random Forest
| * ghi9012 (experiment/logistic-regression) experiment: เพิ่ม Logistic Regression
|/
| * abc1234 (feature/preprocessing) feat: เพิ่ม feature preprocessing module
|/
* xyz7890 (main) Initial commit: สร้างโครงสร้าง ML project
```

---

## 📝 แบบฝึกหัดที่ 5: สร้าง Configuration Files

### 5.1 สร้าง Config Branch

```bash
# สร้าง branch ใหม่จาก main
git switch main
git switch -c feature/config-system
```

### 5.2 สร้าง Config File ด้วย YAML

```bash
cat > configs/experiment_config.yaml << 'EOF'
# Experiment Configuration
# ไฟล์ config สำหรับการทดลอง ML

# Dataset settings
dataset:
  name: iris
  test_size: 0.2
  random_state: 42

# Preprocessing settings
preprocessing:
  scaling_method: standard  # standard, minmax, robust
  handle_missing: drop      # drop, impute

# Model settings
models:
  logistic_regression:
    max_iter: 200
    solver: lbfgs
    
  random_forest:
    n_estimators: 100
    max_depth: null
    min_samples_split: 2
    
  svm:
    kernel: rbf
    C: 1.0
    gamma: scale

# Training settings
training:
  cross_validation: 5
  verbose: true
  
# Output settings
output:
  save_model: true
  model_dir: models/
  results_dir: results/
  log_file: logs/training.log
EOF
```

### 5.3 สร้าง Config Reader

```bash
cat > src/utils/config.py << 'EOF'
"""
Configuration Management Module
โมดูลสำหรับจัดการ configuration
"""

import yaml
from pathlib import Path


def load_config(config_path: str = 'configs/experiment_config.yaml') -> dict:
    """
    โหลด configuration จากไฟล์ YAML
    
    Args:
        config_path: path ไปยังไฟล์ config
    
    Returns:
        dict: configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"✓ Loaded config from: {config_path}")
    return config


def get_model_config(config: dict, model_name: str) -> dict:
    """
    ดึง config สำหรับ model เฉพาะ
    
    Args:
        config: full configuration
        model_name: ชื่อ model
    
    Returns:
        dict: model configuration
    """
    models = config.get('models', {})
    
    if model_name not in models:
        raise ValueError(f"Model '{model_name}' not found in config")
    
    return models[model_name]


def print_config(config: dict, indent: int = 0):
    """
    แสดง config แบบสวยงาม
    """
    for key, value in config.items():
        prefix = "  " * indent
        if isinstance(value, dict):
            print(f"{prefix}📁 {key}:")
            print_config(value, indent + 1)
        else:
            print(f"{prefix}  • {key}: {value}")


if __name__ == "__main__":
    # ทดสอบ module
    config = load_config()
    
    print("\n📋 Full Configuration:")
    print("="*50)
    print_config(config)
    
    print("\n🌲 Random Forest Config:")
    print("="*50)
    rf_config = get_model_config(config, 'random_forest')
    print(rf_config)
EOF
```

### 5.4 ติดตั้ง PyYAML และทดสอบ

```bash
# ติดตั้ง PyYAML (ถ้ายังไม่มี)
pip3 install pyyaml

# ทดสอบ
python3 src/utils/config.py
```

### 5.5 ใช้ tree ดูโครงสร้าง configs

```bash
tree configs
```

### 5.6 Commit

```bash
git add .
git commit -m "feat: เพิ่มระบบ configuration พร้อม YAML support"
```

---

## 📝 แบบฝึกหัดที่ 6: การ Merge Branches

### 6.1 Merge Feature/Preprocessing เข้า Main

```bash
# ไปที่ main
git switch main

# ดูสถานะก่อน merge
git log --oneline --graph --all

# Merge feature/preprocessing
git merge feature/preprocessing -m "Merge: รวม preprocessing module เข้า main"

# ดูสถานะหลัง merge
git log --oneline --graph --all
```

### 6.2 Merge Feature/Config-System

```bash
# Merge config system
git merge feature/config-system -m "Merge: รวม config system เข้า main"

# ดู log
git log --oneline --graph --all
```

### 6.3 ดูโครงสร้างหลัง Merge

```bash
# ดูโครงสร้างทั้งหมด
tree -I '__pycache__|*.pyc|models'
```

**ผลลัพธ์ที่คาดหวัง (หลัง merge):**
```
.
├── README.md
├── configs
│   └── experiment_config.yaml
├── data
│   ├── processed
│   └── raw
├── notebooks
├── requirements.txt
├── results
├── src
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   └── load_data.py
│   ├── features
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── models
│   │   └── __init__.py
│   └── utils
│       ├── __init__.py
│       └── config.py
└── tests
    └── __init__.py
```

### 6.4 ใช้ Pipeline ตรวจสอบผลลัพธ์

```bash
# นับจำนวนไฟล์ Python ทั้งหมด
find . -name "*.py" | wc -l

# ดูเฉพาะไฟล์ที่ไม่ใช่ __init__.py
find . -name "*.py" | grep -v "__init__"

# นับ commits ทั้งหมด
git log --oneline | wc -l

# ดู branches ที่ merge แล้ว
git branch --merged main
```

---

## 📝 แบบฝึกหัดที่ 7: สร้าง Complete Pipeline Script

### 7.1 สร้าง Main Pipeline

```bash
cat > run_experiment.py << 'EOF'
#!/usr/bin/env python3
"""
Main Experiment Pipeline
รัน experiment ทั้งหมดจาก config
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, '.')

from src.data.load_data import load_sklearn_dataset, split_data
from src.features.preprocessing import preprocess_pipeline
from src.utils.config import load_config, get_model_config


def run_experiment(config_path: str = 'configs/experiment_config.yaml'):
    """
    รัน experiment ตาม config
    """
    print("="*60)
    print("🚀 Starting ML Experiment Pipeline")
    print("="*60)
    
    # 1. Load config
    config = load_config(config_path)
    
    # 2. Load data
    print("\n📥 Loading Data...")
    dataset_config = config['dataset']
    X, y, features, targets = load_sklearn_dataset(dataset_config['name'])
    X_train, X_test, y_train, y_test = split_data(
        X, y, 
        test_size=dataset_config['test_size'],
        random_state=dataset_config['random_state']
    )
    
    # 3. Preprocess
    print("\n⚙️ Preprocessing...")
    prep_config = config['preprocessing']
    X_train_scaled, X_test_scaled, preprocessor = preprocess_pipeline(
        X_train, X_test,
        method=prep_config['scaling_method']
    )
    
    # 4. Summary
    print("\n" + "="*60)
    print("✅ Pipeline Summary")
    print("="*60)
    print(f"  Dataset: {dataset_config['name']}")
    print(f"  Train samples: {X_train.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")
    print(f"  Features: {X_train.shape[1]}")
    print(f"  Scaling: {prep_config['scaling_method']}")
    print(f"  Classes: {list(targets)}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, targets


def main():
    parser = argparse.ArgumentParser(description='Run ML Experiment')
    parser.add_argument(
        '--config', '-c',
        default='configs/experiment_config.yaml',
        help='Path to config file'
    )
    
    args = parser.parse_args()
    
    try:
        run_experiment(args.config)
        print("\n🎉 Experiment completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
EOF
```

### 7.2 ทดสอบ Pipeline

```bash
# รัน pipeline
python3 run_experiment.py

# รันด้วย config อื่น (ถ้ามี)
# python3 run_experiment.py --config configs/another_config.yaml
```

### 7.3 Commit

```bash
git add .
git commit -m "feat: เพิ่ม main experiment pipeline script"
```

---

## 📝 แบบฝึกหัดที่ 8: การลบและจัดการ Branches

### 8.1 ดู Branches ที่ Merge แล้ว

```bash
# ดู branches ที่ merge เข้า main แล้ว
git branch --merged main

# ดู branches ที่ยังไม่ได้ merge
git branch --no-merged main
```

### 8.2 ลบ Branch ที่ Merge แล้ว

```bash
# ลบ feature branches ที่ merge แล้ว
git branch -d feature/preprocessing
git branch -d feature/config-system

# ตรวจสอบ
git branch
```

### 8.3 เปลี่ยนชื่อ Branch

```bash
# เปลี่ยนชื่อ experiment branch
git branch -m experiment/logistic-regression experiment/lr-baseline
git branch -m experiment/random-forest experiment/rf-baseline

# ดูผลลัพธ์
git branch -v
```

---

## 📝 แบบฝึกหัดที่ 9: สร้าง Results Tracking

### 9.1 สร้าง Results Logger

```bash
cat > src/utils/logger.py << 'EOF'
"""
Results Logging Module
โมดูลสำหรับ log ผลลัพธ์การทดลอง
"""

import json
import csv
from datetime import datetime
from pathlib import Path


class ExperimentLogger:
    """
    Class สำหรับ log ผลลัพธ์ experiment
    """
    
    def __init__(self, results_dir: str = 'results'):
        """
        Initialize logger
        
        Args:
            results_dir: โฟลเดอร์สำหรับเก็บ results
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # CSV file สำหรับเก็บผลลัพธ์
        self.csv_file = self.results_dir / 'experiments.csv'
        self._init_csv()
    
    def _init_csv(self):
        """สร้าง CSV header ถ้ายังไม่มี"""
        if not self.csv_file.exists():
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'experiment_name',
                    'model_name',
                    'dataset',
                    'train_accuracy',
                    'test_accuracy',
                    'hyperparameters',
                    'notes'
                ])
            print(f"✓ Created results CSV: {self.csv_file}")
    
    def log_experiment(
        self,
        experiment_name: str,
        model_name: str,
        dataset: str,
        train_accuracy: float,
        test_accuracy: float,
        hyperparameters: dict = None,
        notes: str = ''
    ):
        """
        Log ผลลัพธ์ experiment
        """
        timestamp = datetime.now().isoformat()
        
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                experiment_name,
                model_name,
                dataset,
                f'{train_accuracy:.4f}',
                f'{test_accuracy:.4f}',
                json.dumps(hyperparameters) if hyperparameters else '',
                notes
            ])
        
        print(f"✓ Logged experiment: {experiment_name}")
    
    def get_all_results(self):
        """อ่านผลลัพธ์ทั้งหมด"""
        results = []
        
        if self.csv_file.exists():
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                results = list(reader)
        
        return results
    
    def get_best_experiment(self, metric: str = 'test_accuracy'):
        """หา experiment ที่ดีที่สุด"""
        results = self.get_all_results()
        
        if not results:
            return None
        
        best = max(results, key=lambda x: float(x[metric]))
        return best
    
    def print_summary(self):
        """แสดงสรุปผลลัพธ์"""
        results = self.get_all_results()
        
        if not results:
            print("📭 No experiments logged yet")
            return
        
        print("\n" + "="*70)
        print("📊 Experiment Results Summary")
        print("="*70)
        print(f"{'Experiment':<20} {'Model':<15} {'Train Acc':<12} {'Test Acc':<12}")
        print("-"*70)
        
        for r in results:
            print(f"{r['experiment_name']:<20} {r['model_name']:<15} "
                  f"{r['train_accuracy']:<12} {r['test_accuracy']:<12}")
        
        # Best experiment
        best = self.get_best_experiment()
        if best:
            print("\n🏆 Best Experiment:")
            print(f"   {best['experiment_name']} - Test Accuracy: {best['test_accuracy']}")


if __name__ == "__main__":
    # ทดสอบ logger
    logger = ExperimentLogger()
    
    # Log ตัวอย่าง experiments
    logger.log_experiment(
        experiment_name='baseline-lr',
        model_name='logistic_regression',
        dataset='iris',
        train_accuracy=0.975,
        test_accuracy=0.967,
        hyperparameters={'max_iter': 200},
        notes='Baseline experiment'
    )
    
    logger.log_experiment(
        experiment_name='rf-100trees',
        model_name='random_forest',
        dataset='iris',
        train_accuracy=1.0,
        test_accuracy=0.933,
        hyperparameters={'n_estimators': 100, 'max_depth': 5},
        notes='Random Forest with 100 trees'
    )
    
    logger.log_experiment(
        experiment_name='rf-200trees',
        model_name='random_forest',
        dataset='iris',
        train_accuracy=1.0,
        test_accuracy=0.967,
        hyperparameters={'n_estimators': 200, 'max_depth': None},
        notes='Random Forest with 200 trees'
    )
    
    # แสดงสรุป
    logger.print_summary()
EOF
```

### 9.2 ทดสอบ Logger

```bash
python3 src/utils/logger.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
✓ Created results CSV: results/experiments.csv
✓ Logged experiment: baseline-lr
✓ Logged experiment: rf-100trees
✓ Logged experiment: rf-200trees

======================================================================
📊 Experiment Results Summary
======================================================================
Experiment           Model           Train Acc    Test Acc    
----------------------------------------------------------------------
baseline-lr          logistic_regression 0.9750       0.9670      
rf-100trees          random_forest   1.0000       0.9330      
rf-200trees          random_forest   1.0000       0.9670      

🏆 Best Experiment:
   baseline-lr - Test Accuracy: 0.9670
```

### 9.3 ดูไฟล์ผลลัพธ์

```bash
# ดู CSV ที่สร้าง
cat results/experiments.csv

# ใช้ Pipeline วิเคราะห์
cat results/experiments.csv | head -5

# นับจำนวน experiments
cat results/experiments.csv | wc -l
```

### 9.4 Commit

```bash
git add .
git commit -m "feat: เพิ่ม experiment results logger"
```

---

## 📝 แบบฝึกหัดที่ 10: สรุปและ Final Structure

### 10.1 ดูโครงสร้างโปรเจกต์สุดท้าย

```bash
tree -I '__pycache__|*.pyc|.git'
```

**ผลลัพธ์ที่คาดหวังสุดท้าย:**
```
.
├── README.md
├── configs
│   └── experiment_config.yaml
├── data
│   ├── processed
│   └── raw
├── models
│   └── logistic_regression_XXXXXXXX.joblib
├── notebooks
├── requirements.txt
├── results
│   └── experiments.csv
├── run_experiment.py
├── src
│   ├── __init__.py
│   ├── data
│   │   ├── __init__.py
│   │   └── load_data.py
│   ├── features
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── models
│   │   ├── __init__.py
│   │   └── train.py
│   └── utils
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
└── tests
    └── __init__.py
```

### 10.2 ดู Git Log ทั้งหมด

```bash
# ดู log แบบ graph
git log --oneline --graph --all --decorate

# ใช้ Pipeline นับ commits ที่มี "feat"
git log --oneline | grep "feat" | wc -l

# ดู commits ที่มี "experiment"
git log --oneline | grep -i "experiment"
```

### 10.3 สรุป Branches

```bash
# ดู branches ทั้งหมด
git branch -a -v

# ใช้ Pipeline นับ branches
echo "Total branches: $(git branch | wc -l)"
echo "Experiment branches: $(git branch | grep experiment | wc -l)"
echo "Feature branches: $(git branch | grep feature | wc -l)"
```

---

## 📋 สรุปคำสั่งสำคัญ

### คำสั่ง Linux Pipeline

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `cat > file << 'EOF'` | สร้างไฟล์หลายบรรทัด (heredoc) |
| `tree` | ดูโครงสร้างไฟล์และโฟลเดอร์ |
| `cmd1 \| cmd2` | Pipeline: ส่ง output ไปเป็น input |
| `grep "text"` | กรองบรรทัดที่มีข้อความ |
| `wc -l` | นับจำนวนบรรทัด |
| `find . -name "*.py"` | ค้นหาไฟล์ Python |

### คำสั่ง Git Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch` | ดูรายการ branches |
| `git switch -c <branch>` | สร้างและสลับ branch |
| `git switch <branch>` | สลับ branch |
| `git merge <branch>` | รวม branch |
| `git branch -d <branch>` | ลบ branch |
| `git branch -m <old> <new>` | เปลี่ยนชื่อ branch |
| `git branch --merged` | ดู branches ที่ merge แล้ว |

### Git Pipeline Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch \| grep "feature"` | หา feature branches |
| `git log --oneline \| wc -l` | นับจำนวน commits |
| `git log --oneline \| grep "fix"` | หา fix commits |

---

## 🧪 แบบทดสอบความเข้าใจ

1. **ทำไมต้องใช้ Git Branch กับ ML Projects?**

2. **ความแตกต่างระหว่าง `fit()` และ `transform()` ใน sklearn คืออะไร?**

3. **ทำไมต้อง fit preprocessor กับ training data เท่านั้น?**

4. **คำสั่ง `git branch | grep "experiment" | wc -l` ทำอะไร?**

5. **ข้อดีของการใช้ YAML config files คืออะไร?**

<details>
<summary>💡 คลิกเพื่อดูเฉลย</summary>

1. เพื่อทดลอง models/features ต่างๆ โดยไม่กระทบ code หลัก และสามารถเก็บ experiments แต่ละอันแยกกันได้

2. `fit()` เรียนรู้ parameters จากข้อมูล (เช่น mean, std), `transform()` ใช้ parameters ที่เรียนรู้แล้วเพื่อแปลงข้อมูล

3. เพื่อป้องกัน data leakage - ถ้า fit กับ test data ด้วย จะทำให้ model "เห็น" ข้อมูลที่ควรจะเป็น unseen data

4. นับจำนวน branches ที่มีคำว่า "experiment" ในชื่อ

5. อ่านง่าย, แก้ไขง่าย, รองรับ hierarchical data, สามารถ version control ได้, แยก config ออกจาก code

</details>

---

## ✅ Checklist ก่อนจบ LAB

- [ ] เข้าใจการใช้ Pipeline (`|`) กับ ML workflows
- [ ] ใช้ Here Document สร้างไฟล์ Python และ YAML ได้
- [ ] สร้างโครงสร้าง ML project อย่างเป็นระบบ
- [ ] ใช้ Git Branch สำหรับ experiments ต่างๆ ได้
- [ ] เข้าใจ sklearn preprocessing pipeline
- [ ] Merge branches และจัดการ branch ได้
- [ ] สร้างระบบ config และ logging สำหรับ experiments
- [ ] ใช้ `tree` ตรวจสอบโครงสร้างโปรเจกต์ได้
- [ ] ใช้ Pipeline กับ git commands ได้

---

## 🎯 แบบฝึกหัดเพิ่มเติม

### Challenge 1: เพิ่ม SVM Experiment
สร้าง branch ใหม่ `experiment/svm` และทดลอง SVM classifier กับ hyperparameters ต่างๆ

### Challenge 2: Cross-Validation
เพิ่ม cross-validation ใน training pipeline และ log ผลลัพธ์

### Challenge 3: Feature Selection
สร้าง branch `feature/selection` และเพิ่ม feature selection methods (SelectKBest, RFE)

### Challenge 4: Model Comparison Report
สร้าง script ที่เปรียบเทียบ models ทั้งหมดจาก experiments.csv และสร้าง visualization

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Scikit-Learn Documentation](https://scikit-learn.org/stable/)
- [Git Branching Strategies](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [MLOps Principles](https://ml-ops.org/)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)

---

**Happy Learning! 🎓**