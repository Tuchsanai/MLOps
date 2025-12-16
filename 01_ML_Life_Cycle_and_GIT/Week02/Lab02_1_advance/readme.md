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
│   ├── __init__.py
│   ├── data_loader.py       # โหลดและเตรียมข้อมูล
│   ├── feature_engineer.py  # สร้าง features
│   ├── train.py             # training model
│   └── evaluate.py          # ประเมินผล model
├── config/
│   └── model_config.yaml    # ค่า hyperparameters
├── data/
│   ├── raw/                 # ข้อมูลดิบ
│   └── processed/           # ข้อมูลที่ประมวลผลแล้ว
├── models/                  # เก็บ trained models
├── results/                 # ผลการทดลอง
├── notebooks/               # Jupyter notebooks (optional)
├── requirements.txt         # dependencies
├── .gitignore              # ไฟล์ที่ไม่ต้อง track
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
# ตั้งค่าชื่อผู้ใช้ (ใช้ชื่อจริงของนักศึกษา)
git config --global user.name "Your Name"

# ตั้งค่าอีเมล (ใช้อีเมลที่ลงทะเบียนกับ GitHub)
git config --global user.email "your.email@example.com"

# ตั้งค่า default branch เป็น main
git config --global init.defaultBranch main

# ตรวจสอบการตั้งค่า
git config --list
```

---

## 🚀 Part 1: เริ่มต้นสร้าง ML Project

### Step 1: สร้างโฟลเดอร์โปรเจค

```bash
mkdir ml-git-lab03_advance
cd ml-git-lab03_advance
```

**ตรวจสอบ:**
```bash
pwd
```

**ตัวอย่างผลลัพธ์:**
```
/home/student/ml-git-lab03_advance
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

### Step 3: สร้างโครงสร้างโฟลเดอร์ ML Project

```bash
mkdir -p src config data/raw data/processed models results notebooks
```

**ตรวจสอบ:**
```bash
ls -la
```

**ตัวอย่างผลลัพธ์:**
```
total 36
drwxr-xr-x 10 student student 4096 Dec 16 10:00 .
drwxr-xr-x  3 student student 4096 Dec 16 10:00 ..
drwxr-xr-x  2 student student 4096 Dec 16 10:00 config
drwxr-xr-x  4 student student 4096 Dec 16 10:00 data
drwxr-xr-x  7 student student 4096 Dec 16 10:00 .git
drwxr-xr-x  2 student student 4096 Dec 16 10:00 models
drwxr-xr-x  2 student student 4096 Dec 16 10:00 notebooks
drwxr-xr-x  2 student student 4096 Dec 16 10:00 results
drwxr-xr-x  2 student student 4096 Dec 16 10:00 src
```

---

### Step 4: สร้างไฟล์ .gitignore สำหรับ ML Project

> 📝 **สำคัญมาก:** ไฟล์ `.gitignore` ช่วยป้องกันไม่ให้ไฟล์ขนาดใหญ่ (data, models) หรือไฟล์ชั่วคราวถูก track

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb_checkpoints

# Data files (ไฟล์ข้อมูลขนาดใหญ่)
data/raw/*.csv
data/raw/*.json
data/raw/*.xlsx
data/processed/*.csv
data/processed/*.pkl
data/processed/*.parquet
!data/raw/.gitkeep
!data/processed/.gitkeep

# Model files (ไฟล์ model ขนาดใหญ่)
models/*.pkl
models/*.joblib
models/*.h5
models/*.pt
models/*.pth
!models/.gitkeep

# Results (ผลลัพธ์ที่ generate ใหม่ได้)
results/*.png
results/*.csv
results/*.json
!results/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.key
credentials.json
EOF
```

**ตรวจสอบ:**
```bash
cat .gitignore
```

---

### Step 5: สร้าง .gitkeep สำหรับโฟลเดอร์ว่าง

> 📝 **อธิบาย:** Git ไม่ track โฟลเดอร์ว่าง ดังนั้นใช้ `.gitkeep` เพื่อรักษาโครงสร้าง

```bash
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch models/.gitkeep
touch results/.gitkeep
touch notebooks/.gitkeep
```

**ตรวจสอบ:**
```bash
ls -la data/raw/
```

**ตัวอย่างผลลัพธ์:**
```
total 8
drwxr-xr-x 2 student student 4096 Dec 16 10:05 .
drwxr-xr-x 4 student student 4096 Dec 16 10:00 ..
-rw-r--r-- 1 student student    0 Dec 16 10:05 .gitkeep
```

---

### Step 6: สร้างไฟล์ requirements.txt

```bash
cat > requirements.txt << 'EOF'
# ML Libraries
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0

# Data Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Configuration
pyyaml>=6.0

# Model Persistence
joblib>=1.3.0
EOF
```

**ตรวจสอบ:**
```bash
cat requirements.txt
```

---

### Step 7: สร้าง README.md

```bash
cat > README.md << 'EOF'
# ML Git Lab 03 - Scikit-learn Classification Project

## 📋 Project Overview
โปรเจคนี้สาธิตการใช้ Git workflow กับ Machine Learning project โดยใช้ Iris dataset และ scikit-learn

## 🏗️ Project Structure
```
ml-git-lab03_advance/
├── src/              # Source code
├── config/           # Configuration files
├── data/             # Data files
├── models/           # Trained models
├── results/          # Evaluation results
└── notebooks/        # Jupyter notebooks
```

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python src/train.py

# Evaluate model
python src/evaluate.py
```

## 📊 Dataset
- **Name:** Iris Dataset
- **Source:** scikit-learn built-in
- **Features:** 4 (sepal/petal length/width)
- **Classes:** 3 (setosa, versicolor, virginica)

## 👥 Contributors
- Student Name
EOF
```

---

### Step 8: สร้าง src/__init__.py

```bash
cat > src/__init__.py << 'EOF'
"""
ML Git Lab 03 - Scikit-learn Classification Project
====================================================
โมดูลสำหรับ training และ evaluation ของ ML models
"""

__version__ = "1.0.0"
__author__ = "MLOps Student"
EOF
```

---

### Step 9: Commit ครั้งแรก - Project Structure

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        README.md
        config/
        data/
        models/
        notebooks/
        requirements.txt
        results/
        src/
```

```bash
git add .
git commit -m "Initial commit: ML project structure with .gitignore"
```

**ตัวอย่างผลลัพธ์:**
```
[main (root-commit) a1b2c3d] Initial commit: ML project structure with .gitignore
 8 files changed, 95 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 data/processed/.gitkeep
 create mode 100644 data/raw/.gitkeep
 create mode 100644 models/.gitkeep
 create mode 100644 notebooks/.gitkeep
 create mode 100644 requirements.txt
 create mode 100644 results/.gitkeep
 create mode 100644 src/__init__.py
```

**ดู log:**
```bash
git log --oneline
```

**ตัวอย่างผลลัพธ์:**
```
a1b2c3d (HEAD -> main) Initial commit: ML project structure with .gitignore
```

---

## 📊 Part 2: สร้าง Data Loading Module

### Step 10: สร้าง data_loader.py

```bash
cat > src/data_loader.py << 'EOF'
"""
Data Loader Module
==================
โมดูลสำหรับโหลดและเตรียมข้อมูล Iris dataset
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def load_iris_data():
    """
    โหลด Iris dataset จาก scikit-learn
    
    Returns:
        tuple: (X, y, feature_names, target_names)
    """
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    
    print(f"✅ Loaded Iris dataset")
    print(f"   - Samples: {X.shape[0]}")
    print(f"   - Features: {X.shape[1]}")
    print(f"   - Classes: {len(target_names)}")
    
    return X, y, feature_names, target_names


def create_dataframe(X, y, feature_names, target_names):
    """
    สร้าง DataFrame จากข้อมูล
    
    Args:
        X: Feature matrix
        y: Target vector
        feature_names: ชื่อ features
        target_names: ชื่อ classes
    
    Returns:
        pd.DataFrame: DataFrame ที่มีข้อมูลทั้งหมด
    """
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    df['target_name'] = df['target'].map(
        lambda x: target_names[x]
    )
    return df


def split_data(X, y, test_size=0.2, random_state=42):
    """
    แบ่งข้อมูลเป็น train และ test sets
    
    Args:
        X: Feature matrix
        y: Target vector
        test_size: สัดส่วน test set (default: 0.2)
        random_state: random seed (default: 42)
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y
    )
    
    print(f"✅ Data split completed")
    print(f"   - Train samples: {X_train.shape[0]}")
    print(f"   - Test samples: {X_test.shape[0]}")
    
    return X_train, X_test, y_train, y_test


def get_data_summary(df):
    """
    สรุปข้อมูลเบื้องต้น
    
    Args:
        df: DataFrame
    
    Returns:
        dict: สรุปข้อมูล
    """
    summary = {
        'n_samples': len(df),
        'n_features': len(df.columns) - 2,  # ไม่นับ target columns
        'class_distribution': df['target_name'].value_counts().to_dict(),
        'missing_values': df.isnull().sum().sum()
    }
    return summary


if __name__ == "__main__":
    # ทดสอบ module
    print("=" * 50)
    print("Testing Data Loader Module")
    print("=" * 50)
    
    # โหลดข้อมูล
    X, y, feature_names, target_names = load_iris_data()
    
    # สร้าง DataFrame
    df = create_dataframe(X, y, feature_names, target_names)
    print(f"\n📊 DataFrame shape: {df.shape}")
    print(f"\n📋 First 5 rows:")
    print(df.head())
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # สรุปข้อมูล
    summary = get_data_summary(df)
    print(f"\n📈 Data Summary:")
    for key, value in summary.items():
        print(f"   - {key}: {value}")
EOF
```

**ตรวจสอบไฟล์:**
```bash
cat src/data_loader.py
```

---

### Step 11: ทดสอบ data_loader.py

```bash
python src/data_loader.py
```

**ตัวอย่างผลลัพธ์:**
```
==================================================
Testing Data Loader Module
==================================================
✅ Loaded Iris dataset
   - Samples: 150
   - Features: 4
   - Classes: 3

📊 DataFrame shape: (150, 6)

📋 First 5 rows:
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  target target_name
0                5.1               3.5                1.4               0.2       0      setosa
1                4.9               3.0                1.4               0.2       0      setosa
2                4.7               3.2                1.3               0.2       0      setosa
3                4.6               3.1                1.5               0.2       0      setosa
4                5.0               3.6                1.4               0.2       0      setosa
✅ Data split completed
   - Train samples: 120
   - Test samples: 30

📈 Data Summary:
   - n_samples: 150
   - n_features: 4
   - class_distribution: {'setosa': 50, 'versicolor': 50, 'virginica': 50}
   - missing_values: 0
```

---

### Step 12: Commit Data Loader

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/data_loader.py

nothing added to commit but untracked files present (use "git add" to track)
```

```bash
git add src/data_loader.py
git commit -m "Add data_loader module with Iris dataset support"
```

**ตัวอย่างผลลัพธ์:**
```
[main b2c3d4e] Add data_loader module with Iris dataset support
 1 file changed, 107 insertions(+)
 create mode 100644 src/data_loader.py
```

---

## 🔧 Part 3: สร้าง Feature Engineering Module

### Step 13: สร้าง feature_engineer.py

```bash
cat > src/feature_engineer.py << 'EOF'
"""
Feature Engineering Module
==========================
โมดูลสำหรับสร้างและแปลง features
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder


class FeatureEngineer:
    """
    Class สำหรับจัดการ feature engineering
    """
    
    def __init__(self, scaling_method='standard'):
        """
        Initialize FeatureEngineer
        
        Args:
            scaling_method: วิธีการ scale ('standard' หรือ 'minmax')
        """
        self.scaling_method = scaling_method
        self.scaler = None
        self.feature_names = None
        
    def fit(self, X, feature_names=None):
        """
        Fit scaler กับข้อมูล
        
        Args:
            X: Feature matrix
            feature_names: ชื่อ features (optional)
        """
        if self.scaling_method == 'standard':
            self.scaler = StandardScaler()
        elif self.scaling_method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown scaling method: {self.scaling_method}")
        
        self.scaler.fit(X)
        self.feature_names = feature_names
        print(f"✅ Scaler fitted with {self.scaling_method} method")
        
    def transform(self, X):
        """
        Transform ข้อมูลด้วย scaler ที่ fit แล้ว
        
        Args:
            X: Feature matrix
        
        Returns:
            np.ndarray: Scaled features
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit() first.")
        
        X_scaled = self.scaler.transform(X)
        return X_scaled
    
    def fit_transform(self, X, feature_names=None):
        """
        Fit และ transform ในขั้นตอนเดียว
        
        Args:
            X: Feature matrix
            feature_names: ชื่อ features (optional)
        
        Returns:
            np.ndarray: Scaled features
        """
        self.fit(X, feature_names)
        return self.transform(X)
    
    def create_polynomial_features(self, X, degree=2):
        """
        สร้าง polynomial features
        
        Args:
            X: Feature matrix
            degree: degree ของ polynomial (default: 2)
        
        Returns:
            np.ndarray: Features พร้อม polynomial terms
        """
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=degree, include_bias=False)
        X_poly = poly.fit_transform(X)
        print(f"✅ Created polynomial features (degree={degree})")
        print(f"   - Original features: {X.shape[1]}")
        print(f"   - New features: {X_poly.shape[1]}")
        return X_poly
    
    def get_feature_statistics(self, X):
        """
        คำนวณสถิติของ features
        
        Args:
            X: Feature matrix
        
        Returns:
            pd.DataFrame: สถิติของแต่ละ feature
        """
        if self.feature_names is not None:
            columns = self.feature_names
        else:
            columns = [f'feature_{i}' for i in range(X.shape[1])]
        
        df = pd.DataFrame(X, columns=columns)
        stats = df.describe().T
        stats['variance'] = df.var()
        return stats


def create_interaction_features(X, feature_names=None):
    """
    สร้าง interaction features (คูณกันระหว่าง features)
    
    Args:
        X: Feature matrix
        feature_names: ชื่อ features (optional)
    
    Returns:
        tuple: (X_new, new_feature_names)
    """
    n_features = X.shape[1]
    interactions = []
    new_names = []
    
    if feature_names is None:
        feature_names = [f'f{i}' for i in range(n_features)]
    
    for i in range(n_features):
        for j in range(i+1, n_features):
            interactions.append(X[:, i] * X[:, j])
            new_names.append(f'{feature_names[i]}_x_{feature_names[j]}')
    
    X_interactions = np.column_stack(interactions)
    X_new = np.hstack([X, X_interactions])
    all_names = list(feature_names) + new_names
    
    print(f"✅ Created {len(interactions)} interaction features")
    
    return X_new, all_names


if __name__ == "__main__":
    # ทดสอบ module
    print("=" * 50)
    print("Testing Feature Engineering Module")
    print("=" * 50)
    
    # Import data_loader
    from data_loader import load_iris_data, split_data
    
    # โหลดข้อมูล
    X, y, feature_names, target_names = load_iris_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # ทดสอบ FeatureEngineer
    print("\n📊 Testing StandardScaler:")
    fe = FeatureEngineer(scaling_method='standard')
    X_train_scaled = fe.fit_transform(X_train, feature_names)
    X_test_scaled = fe.transform(X_test)
    
    print(f"   - Train mean (should be ~0): {X_train_scaled.mean(axis=0).round(2)}")
    print(f"   - Train std (should be ~1): {X_train_scaled.std(axis=0).round(2)}")
    
    # ทดสอบ interaction features
    print("\n📊 Testing Interaction Features:")
    X_new, new_names = create_interaction_features(X_train[:5], feature_names)
    print(f"   - Original shape: {X_train[:5].shape}")
    print(f"   - New shape: {X_new.shape}")
    print(f"   - New feature names: {new_names[-3:]}")
    
    # ดูสถิติ
    print("\n📈 Feature Statistics (scaled data):")
    stats = fe.get_feature_statistics(X_train_scaled)
    print(stats[['mean', 'std', 'min', 'max']].round(3))
EOF
```

---

### Step 14: ทดสอบ feature_engineer.py

```bash
cd src
python feature_engineer.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
==================================================
Testing Feature Engineering Module
==================================================
✅ Loaded Iris dataset
   - Samples: 150
   - Features: 4
   - Classes: 3
✅ Data split completed
   - Train samples: 120
   - Test samples: 30

📊 Testing StandardScaler:
✅ Scaler fitted with standard method
   - Train mean (should be ~0): [-0.  0. -0.  0.]
   - Train std (should be ~1): [1. 1. 1. 1.]

📊 Testing Interaction Features:
✅ Created 6 interaction features
   - Original shape: (5, 4)
   - New shape: (5, 10)
   - New feature names: ['petal length (cm)_x_petal width (cm)', ...]

📈 Feature Statistics (scaled data):
                     mean    std    min    max
sepal length (cm)   -0.000  1.004 -1.870  2.492
sepal width (cm)     0.000  1.004 -2.431  2.791
petal length (cm)    0.000  1.004 -1.567  1.785
petal width (cm)    -0.000  1.004 -1.447  1.712
```

---

### Step 15: Commit Feature Engineering Module

```bash
git add src/feature_engineer.py
git commit -m "Add feature_engineer module with scaling and transformations"
```

**ตัวอย่างผลลัพธ์:**
```
[main c3d4e5f] Add feature_engineer module with scaling and transformations
 1 file changed, 168 insertions(+)
 create mode 100644 src/feature_engineer.py
```

---

## 🤖 Part 4: สร้าง Training Module

### Step 16: สร้าง config/model_config.yaml

```bash
cat > config/model_config.yaml << 'EOF'
# Model Configuration
# ===================

# Data settings
data:
  test_size: 0.2
  random_state: 42

# Feature engineering
features:
  scaling_method: standard  # standard or minmax
  create_interactions: false
  polynomial_degree: 1

# Model settings
model:
  type: random_forest  # random_forest, logistic_regression, svm
  
  # Random Forest parameters
  random_forest:
    n_estimators: 100
    max_depth: 5
    min_samples_split: 2
    min_samples_leaf: 1
    random_state: 42
  
  # Logistic Regression parameters
  logistic_regression:
    C: 1.0
    max_iter: 1000
    random_state: 42
  
  # SVM parameters
  svm:
    C: 1.0
    kernel: rbf
    gamma: scale
    random_state: 42

# Training settings
training:
  cross_validation: true
  cv_folds: 5
  verbose: true

# Output settings
output:
  save_model: true
  model_path: models/model.joblib
  save_results: true
  results_path: results/metrics.json
EOF
```

---

### Step 17: สร้าง train.py

```bash
cat > src/train.py << 'EOF'
"""
Model Training Module
=====================
โมดูลสำหรับ training ML models
"""

import os
import sys
import yaml
import json
import joblib
import numpy as np
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

# Import local modules
from data_loader import load_iris_data, split_data
from feature_engineer import FeatureEngineer


def load_config(config_path='../config/model_config.yaml'):
    """
    โหลด configuration จากไฟล์ YAML
    
    Args:
        config_path: path ไปยังไฟล์ config
    
    Returns:
        dict: configuration
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    print(f"✅ Loaded config from {config_path}")
    return config


def create_model(config):
    """
    สร้าง model ตาม configuration
    
    Args:
        config: configuration dict
    
    Returns:
        sklearn model instance
    """
    model_type = config['model']['type']
    
    if model_type == 'random_forest':
        params = config['model']['random_forest']
        model = RandomForestClassifier(**params)
    elif model_type == 'logistic_regression':
        params = config['model']['logistic_regression']
        model = LogisticRegression(**params)
    elif model_type == 'svm':
        params = config['model']['svm']
        model = SVC(**params)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    print(f"✅ Created {model_type} model")
    return model


def train_model(model, X_train, y_train, config):
    """
    Train model
    
    Args:
        model: sklearn model
        X_train: training features
        y_train: training labels
        config: configuration dict
    
    Returns:
        tuple: (trained_model, cv_scores)
    """
    cv_scores = None
    
    # Cross-validation ถ้าเปิดใช้งาน
    if config['training']['cross_validation']:
        n_folds = config['training']['cv_folds']
        cv_scores = cross_val_score(model, X_train, y_train, cv=n_folds)
        print(f"✅ Cross-validation ({n_folds} folds):")
        print(f"   - Scores: {cv_scores.round(4)}")
        print(f"   - Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    
    # Train final model
    model.fit(X_train, y_train)
    print(f"✅ Model trained on {X_train.shape[0]} samples")
    
    return model, cv_scores


def save_model(model, scaler, config, output_path):
    """
    บันทึก model และ scaler
    
    Args:
        model: trained model
        scaler: fitted scaler
        config: configuration
        output_path: path สำหรับบันทึก
    """
    model_data = {
        'model': model,
        'scaler': scaler,
        'config': config,
        'timestamp': datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(model_data, output_path)
    print(f"✅ Model saved to {output_path}")


def save_training_results(results, output_path):
    """
    บันทึกผลการ training
    
    Args:
        results: dict ของผลลัพธ์
        output_path: path สำหรับบันทึก
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Results saved to {output_path}")


def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("🚀 ML Training Pipeline")
    print("=" * 60)
    
    # 1. Load configuration
    print("\n📁 Step 1: Loading configuration...")
    config = load_config()
    
    # 2. Load data
    print("\n📊 Step 2: Loading data...")
    X, y, feature_names, target_names = load_iris_data()
    
    # 3. Split data
    print("\n✂️ Step 3: Splitting data...")
    test_size = config['data']['test_size']
    random_state = config['data']['random_state']
    X_train, X_test, y_train, y_test = split_data(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # 4. Feature engineering
    print("\n🔧 Step 4: Feature engineering...")
    scaling_method = config['features']['scaling_method']
    fe = FeatureEngineer(scaling_method=scaling_method)
    X_train_scaled = fe.fit_transform(X_train, feature_names)
    X_test_scaled = fe.transform(X_test)
    
    # 5. Create model
    print("\n🤖 Step 5: Creating model...")
    model = create_model(config)
    
    # 6. Train model
    print("\n🎯 Step 6: Training model...")
    model, cv_scores = train_model(model, X_train_scaled, y_train, config)
    
    # 7. Evaluate on test set
    print("\n📈 Step 7: Evaluating on test set...")
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    print(f"   - Train accuracy: {train_score:.4f}")
    print(f"   - Test accuracy: {test_score:.4f}")
    
    # 8. Save model
    if config['output']['save_model']:
        print("\n💾 Step 8: Saving model...")
        model_path = config['output']['model_path']
        save_model(model, fe.scaler, config, model_path)
    
    # 9. Save results
    if config['output']['save_results']:
        print("\n📝 Step 9: Saving results...")
        results = {
            'model_type': config['model']['type'],
            'train_accuracy': float(train_score),
            'test_accuracy': float(test_score),
            'cv_scores': cv_scores.tolist() if cv_scores is not None else None,
            'cv_mean': float(cv_scores.mean()) if cv_scores is not None else None,
            'cv_std': float(cv_scores.std()) if cv_scores is not None else None,
            'n_train_samples': int(X_train.shape[0]),
            'n_test_samples': int(X_test.shape[0]),
            'timestamp': datetime.now().isoformat()
        }
        results_path = config['output']['results_path']
        save_training_results(results, results_path)
    
    print("\n" + "=" * 60)
    print("✅ Training pipeline completed!")
    print("=" * 60)
    
    return model, fe.scaler, results


if __name__ == "__main__":
    model, scaler, results = main()
EOF
```

---

### Step 18: ทดสอบ train.py

```bash
cd src
python train.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
============================================================
🚀 ML Training Pipeline
============================================================

📁 Step 1: Loading configuration...
✅ Loaded config from ../config/model_config.yaml

📊 Step 2: Loading data...
✅ Loaded Iris dataset
   - Samples: 150
   - Features: 4
   - Classes: 3

✂️ Step 3: Splitting data...
✅ Data split completed
   - Train samples: 120
   - Test samples: 30

🔧 Step 4: Feature engineering...
✅ Scaler fitted with standard method

🤖 Step 5: Creating model...
✅ Created random_forest model

🎯 Step 6: Training model...
✅ Cross-validation (5 folds):
   - Scores: [0.9583 0.9167 0.9583 0.9583 0.9167]
   - Mean: 0.9417 (+/- 0.0385)
✅ Model trained on 120 samples

📈 Step 7: Evaluating on test set...
   - Train accuracy: 1.0000
   - Test accuracy: 0.9667

💾 Step 8: Saving model...
✅ Model saved to ../models/model.joblib

📝 Step 9: Saving results...
✅ Results saved to ../results/metrics.json

============================================================
✅ Training pipeline completed!
============================================================
```

---

### Step 19: ตรวจสอบว่า .gitignore ทำงาน

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config/model_config.yaml
        src/train.py

nothing added to commit but untracked files present (use "git add" to track)
```

> 📝 **สังเกต:** ไฟล์ `models/model.joblib` และ `results/metrics.json` ไม่แสดงเพราะถูก ignore แล้ว!

**ตรวจสอบไฟล์ที่ถูก ignore:**
```bash
git status --ignored
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config/model_config.yaml
        src/train.py

Ignored files:
  (use "git add -f <file>..." to include in what will be committed)
        models/model.joblib
        results/metrics.json
        src/__pycache__/
```

---

### Step 20: Commit Training Module

```bash
git add config/model_config.yaml src/train.py
git commit -m "Add training pipeline with config and model saving"
```

**ตัวอย่างผลลัพธ์:**
```
[main d4e5f6g] Add training pipeline with config and model saving
 2 files changed, 242 insertions(+)
 create mode 100644 config/model_config.yaml
 create mode 100644 src/train.py
```

---

## 📈 Part 5: สร้าง Evaluation Module

### Step 21: สร้าง evaluate.py

```bash
cat > src/evaluate.py << 'EOF'
"""
Model Evaluation Module
=======================
โมดูลสำหรับประเมินผล ML models
"""

import os
import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from data_loader import load_iris_data, split_data


def load_model(model_path):
    """
    โหลด model จากไฟล์
    
    Args:
        model_path: path ไปยังไฟล์ model
    
    Returns:
        dict: model data (model, scaler, config, timestamp)
    """
    model_data = joblib.load(model_path)
    print(f"✅ Loaded model from {model_path}")
    print(f"   - Model type: {type(model_data['model']).__name__}")
    print(f"   - Trained at: {model_data['timestamp']}")
    return model_data


def evaluate_model(model, X_test, y_test, target_names):
    """
    ประเมินผล model
    
    Args:
        model: trained model
        X_test: test features
        y_test: test labels
        target_names: ชื่อ classes
    
    Returns:
        dict: evaluation metrics
    """
    # ทำนายผล
    y_pred = model.predict(X_test)
    
    # คำนวณ metrics
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision_macro': float(precision_score(y_test, y_pred, average='macro')),
        'recall_macro': float(recall_score(y_test, y_pred, average='macro')),
        'f1_macro': float(f1_score(y_test, y_pred, average='macro')),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'classification_report': classification_report(
            y_test, y_pred, target_names=target_names, output_dict=True
        )
    }
    
    return metrics, y_pred


def plot_confusion_matrix(cm, target_names, output_path):
    """
    สร้าง confusion matrix plot
    
    Args:
        cm: confusion matrix
        target_names: ชื่อ classes
        output_path: path สำหรับบันทึกรูป
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=target_names,
        yticklabels=target_names
    )
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✅ Confusion matrix saved to {output_path}")


def plot_feature_importance(model, feature_names, output_path):
    """
    สร้าง feature importance plot (สำหรับ tree-based models)
    
    Args:
        model: trained model
        feature_names: ชื่อ features
        output_path: path สำหรับบันทึกรูป
    """
    if not hasattr(model, 'feature_importances_'):
        print("⚠️ Model doesn't have feature_importances_")
        return
    
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title('Feature Importances')
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.xlabel('Feature')
    plt.ylabel('Importance')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"✅ Feature importance plot saved to {output_path}")


def print_evaluation_report(metrics, target_names):
    """
    แสดงผลการประเมิน
    
    Args:
        metrics: dict ของ metrics
        target_names: ชื่อ classes
    """
    print("\n" + "=" * 60)
    print("📊 Evaluation Report")
    print("=" * 60)
    
    print(f"\n🎯 Overall Metrics:")
    print(f"   - Accuracy:  {metrics['accuracy']:.4f}")
    print(f"   - Precision: {metrics['precision_macro']:.4f}")
    print(f"   - Recall:    {metrics['recall_macro']:.4f}")
    print(f"   - F1-Score:  {metrics['f1_macro']:.4f}")
    
    print(f"\n📋 Per-Class Metrics:")
    report = metrics['classification_report']
    for class_name in target_names:
        class_metrics = report[class_name]
        print(f"   {class_name}:")
        print(f"      - Precision: {class_metrics['precision']:.4f}")
        print(f"      - Recall:    {class_metrics['recall']:.4f}")
        print(f"      - F1-Score:  {class_metrics['f1-score']:.4f}")
    
    print(f"\n📈 Confusion Matrix:")
    cm = np.array(metrics['confusion_matrix'])
    print(f"   {cm}")


def save_evaluation_results(metrics, output_path):
    """
    บันทึกผลการประเมิน
    
    Args:
        metrics: dict ของ metrics
        output_path: path สำหรับบันทึก
    """
    results = {
        **metrics,
        'timestamp': datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Evaluation results saved to {output_path}")


def main():
    """
    Main evaluation pipeline
    """
    print("=" * 60)
    print("📊 ML Evaluation Pipeline")
    print("=" * 60)
    
    # 1. Load model
    print("\n📁 Step 1: Loading model...")
    model_path = '../models/model.joblib'
    model_data = load_model(model_path)
    model = model_data['model']
    scaler = model_data['scaler']
    config = model_data['config']
    
    # 2. Load data
    print("\n📊 Step 2: Loading data...")
    X, y, feature_names, target_names = load_iris_data()
    
    # 3. Split data (ใช้ random_state เดียวกับตอน train)
    print("\n✂️ Step 3: Splitting data...")
    test_size = config['data']['test_size']
    random_state = config['data']['random_state']
    X_train, X_test, y_train, y_test = split_data(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # 4. Scale data
    print("\n🔧 Step 4: Scaling test data...")
    X_test_scaled = scaler.transform(X_test)
    
    # 5. Evaluate
    print("\n📈 Step 5: Evaluating model...")
    metrics, y_pred = evaluate_model(model, X_test_scaled, y_test, target_names)
    
    # 6. Print report
    print_evaluation_report(metrics, target_names)
    
    # 7. Create plots
    print("\n🎨 Step 6: Creating visualizations...")
    cm = np.array(metrics['confusion_matrix'])
    plot_confusion_matrix(cm, target_names, '../results/confusion_matrix.png')
    plot_feature_importance(model, feature_names, '../results/feature_importance.png')
    
    # 8. Save results
    print("\n💾 Step 7: Saving results...")
    save_evaluation_results(metrics, '../results/evaluation_metrics.json')
    
    print("\n" + "=" * 60)
    print("✅ Evaluation pipeline completed!")
    print("=" * 60)
    
    return metrics


if __name__ == "__main__":
    metrics = main()
EOF
```

---

### Step 22: ทดสอบ evaluate.py

```bash
cd src
python evaluate.py
cd ..
```

**ตัวอย่างผลลัพธ์:**
```
============================================================
📊 ML Evaluation Pipeline
============================================================

📁 Step 1: Loading model...
✅ Loaded model from ../models/model.joblib
   - Model type: RandomForestClassifier
   - Trained at: 2024-12-16T10:30:00

📊 Step 2: Loading data...
✅ Loaded Iris dataset
   - Samples: 150
   - Features: 4
   - Classes: 3

✂️ Step 3: Splitting data...
✅ Data split completed
   - Train samples: 120
   - Test samples: 30

🔧 Step 4: Scaling test data...

📈 Step 5: Evaluating model...

============================================================
📊 Evaluation Report
============================================================

🎯 Overall Metrics:
   - Accuracy:  0.9667
   - Precision: 0.9722
   - Recall:    0.9667
   - F1-Score:  0.9665

📋 Per-Class Metrics:
   setosa:
      - Precision: 1.0000
      - Recall:    1.0000
      - F1-Score:  1.0000
   versicolor:
      - Precision: 0.9167
      - Recall:    1.0000
      - F1-Score:  0.9565
   virginica:
      - Precision: 1.0000
      - Recall:    0.9000
      - F1-Score:  0.9474

📈 Confusion Matrix:
   [[10  0  0]
    [ 0 10  0]
    [ 0  1  9]]

🎨 Step 6: Creating visualizations...
✅ Confusion matrix saved to ../results/confusion_matrix.png
✅ Feature importance plot saved to ../results/feature_importance.png

💾 Step 7: Saving results...
✅ Evaluation results saved to ../results/evaluation_metrics.json

============================================================
✅ Evaluation pipeline completed!
============================================================
```

---

### Step 23: Commit Evaluation Module

```bash
git add src/evaluate.py
git commit -m "Add evaluation module with metrics and visualizations"
```

**ตัวอย่างผลลัพธ์:**
```
[main e5f6g7h] Add evaluation module with metrics and visualizations
 1 file changed, 218 insertions(+)
 create mode 100644 src/evaluate.py
```

---

## 🌐 Part 6: การทำงานกับ Remote Repository

### Step 24: ดู Commit History ทั้งหมด

```bash
git log --oneline --graph --all
```

**ตัวอย่างผลลัพธ์:**
```
* e5f6g7h (HEAD -> main) Add evaluation module with metrics and visualizations
* d4e5f6g Add training pipeline with config and model saving
* c3d4e5f Add feature_engineer module with scaling and transformations
* b2c3d4e Add data_loader module with Iris dataset support
* a1b2c3d Initial commit: ML project structure with .gitignore
```

---

### Step 25: เพิ่ม Remote Repository

> ⚠️ **หมายเหตุ:** ให้นักศึกษาสร้าง repository บน GitHub ก่อน

**วิธีสร้าง Repository บน GitHub:**
1. ไปที่ https://github.com
2. คลิก "New repository"
3. ตั้งชื่อ `ml-git-lab03_advance`
4. **ไม่ต้อง** เลือก "Add a README file"
5. คลิก "Create repository"

```bash
git remote add origin https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git
```

**ตรวจสอบ:**
```bash
git remote -v
```

**ตัวอย่างผลลัพธ์:**
```
origin  https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git (fetch)
origin  https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git (push)
```

---

### Step 26: Push ไปยัง Remote

```bash
git push -u origin main
```

**ตัวอย่างผลลัพธ์:**
```
Enumerating objects: 22, done.
Counting objects: 100% (22/22), done.
Delta compression using up to 8 threads
Compressing objects: 100% (18/18), done.
Writing objects: 100% (22/22), 7.15 KiB | 1.43 MiB/s, done.
Total 22 (delta 3), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

### Step 27: ตรวจสอบ Remote Branches

```bash
git branch -a
```

**ตัวอย่างผลลัพธ์:**
```
* main
  remotes/origin/main
```

---

## 🔄 Part 7: การทดลองเปลี่ยน Model Configuration

### Step 28: สร้างการเปลี่ยนแปลง - เปลี่ยนเป็น SVM

```bash
cat > config/model_config.yaml << 'EOF'
# Model Configuration
# ===================
# Updated: Changed to SVM model

# Data settings
data:
  test_size: 0.2
  random_state: 42

# Feature engineering
features:
  scaling_method: standard
  create_interactions: false
  polynomial_degree: 1

# Model settings - CHANGED TO SVM
model:
  type: svm  # Changed from random_forest
  
  # Random Forest parameters
  random_forest:
    n_estimators: 100
    max_depth: 5
    min_samples_split: 2
    min_samples_leaf: 1
    random_state: 42
  
  # Logistic Regression parameters
  logistic_regression:
    C: 1.0
    max_iter: 1000
    random_state: 42
  
  # SVM parameters - USING THESE NOW
  svm:
    C: 1.0
    kernel: rbf
    gamma: scale
    random_state: 42

# Training settings
training:
  cross_validation: true
  cv_folds: 5
  verbose: true

# Output settings
output:
  save_model: true
  model_path: models/model.joblib
  save_results: true
  results_path: results/metrics.json
EOF
```

---

### Step 29: ตรวจสอบการเปลี่ยนแปลงด้วย git diff

```bash
git diff config/model_config.yaml
```

**ตัวอย่างผลลัพธ์:**
```diff
diff --git a/config/model_config.yaml b/config/model_config.yaml
index abc1234..def5678 100644
--- a/config/model_config.yaml
+++ b/config/model_config.yaml
@@ -1,5 +1,6 @@
 # Model Configuration
 # ===================
+# Updated: Changed to SVM model
 
 # Data settings
 data:
@@ -12,8 +13,8 @@ features:
   create_interactions: false
   polynomial_degree: 1
 
-# Model settings
-model:
-  type: random_forest
+# Model settings - CHANGED TO SVM
+model:
+  type: svm  # Changed from random_forest
```

---

### Step 30: Train และ Evaluate ใหม่ด้วย SVM

```bash
cd src
python train.py
python evaluate.py
cd ..
```

**ตัวอย่างผลลัพธ์ (บางส่วน):**
```
🤖 Step 5: Creating model...
✅ Created svm model

🎯 Step 6: Training model...
✅ Cross-validation (5 folds):
   - Scores: [0.9583 0.9583 1.0000 0.9583 0.9167]
   - Mean: 0.9583 (+/- 0.0527)
...
   - Test accuracy: 0.9667
```

---

### Step 31: Commit การเปลี่ยนแปลง config

```bash
git add config/model_config.yaml
git commit -m "Experiment: Switch to SVM model for comparison"
```

**ตัวอย่างผลลัพธ์:**
```
[main f6g7h8i] Experiment: Switch to SVM model for comparison
 1 file changed, 5 insertions(+), 3 deletions(-)
```

---

### Step 32: Push การเปลี่ยนแปลงขึ้น Remote

```bash
git push
```

**ตัวอย่างผลลัพธ์:**
```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 456 bytes | 456.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/ml-git-lab03_advance.git
   e5f6g7h..f6g7h8i  main -> main
```

---

## 🔍 Part 8: การใช้ git checkout กับ ML Project

### Step 33: ดูไฟล์ config เวอร์ชันก่อนหน้า

```bash
git log --oneline config/model_config.yaml
```

**ตัวอย่างผลลัพธ์:**
```
f6g7h8i (HEAD -> main, origin/main) Experiment: Switch to SVM model for comparison
d4e5f6g Add training pipeline with config and model saving
```

**ดูไฟล์ config เวอร์ชัน Random Forest:**
```bash
git show d4e5f6g:config/model_config.yaml | head -20
```

**ตัวอย่างผลลัพธ์:**
```yaml
# Model Configuration
# ===================

# Data settings
data:
  test_size: 0.2
  random_state: 42

# Feature engineering
features:
  scaling_method: standard
  create_interactions: false
  polynomial_degree: 1

# Model settings
model:
  type: random_forest  # <-- เห็นว่าเป็น random_forest
```

---

### Step 34: กู้คืน config เวอร์ชัน Random Forest (ถ้าต้องการ)

```bash
# ดึงไฟล์ config เวอร์ชันเก่ามาดู
git checkout d4e5f6g -- config/model_config.yaml

# ตรวจสอบ
cat config/model_config.yaml | grep "type:"
```

**ตัวอย่างผลลัพธ์:**
```
  type: random_forest
```

**ยกเลิกการเปลี่ยนแปลง (กลับไปเป็น SVM):**
```bash
git restore config/model_config.yaml
```

---

## 📊 Part 9: สรุปคำสั่งที่เรียนรู้

### คำสั่ง Git พื้นฐาน

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git init` | สร้าง repository ใหม่ |
| `git add <file>` | เพิ่มไฟล์เข้า staging |
| `git add .` | เพิ่มทุกไฟล์เข้า staging |
| `git commit -m "msg"` | บันทึกการเปลี่ยนแปลง |
| `git status` | ตรวจสอบสถานะ |
| `git log --oneline` | ดูประวัติ commit |
| `git diff <file>` | ดูความเปลี่ยนแปลง |

### คำสั่ง Remote

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git remote add origin <url>` | เพิ่ม remote |
| `git push -u origin main` | push และตั้ง upstream |
| `git push` | push (หลังตั้ง upstream) |
| `git fetch origin` | ดึงข้อมูลจาก remote |
| `git pull origin main` | fetch + merge |

### คำสั่งสำหรับ ML Workflow

| คำสั่ง | ใช้ทำอะไร |
|--------|----------|
| `git status --ignored` | ดูไฟล์ที่ถูก ignore (models, data) |
| `git show <commit>:<file>` | ดูไฟล์ config เวอร์ชันเก่า |
| `git checkout <commit> -- <file>` | กู้คืนไฟล์เวอร์ชันเก่า |
| `git log --oneline <file>` | ดูประวัติการเปลี่ยนแปลงไฟล์ |

---


---

## 🧹 ทำความสะอาด (Optional)

```bash
# กลับไปโฟลเดอร์ก่อนหน้า
cd ..

# ลบโฟลเดอร์โปรเจค (ถ้าต้องการ)
rm -rf ml-git-lab03_advance
```

---

## 📚 อ้างอิงเพิ่มเติม

- [Git Documentation](https://git-scm.com/doc)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [MLOps Principles](https://ml-ops.org/)
- [DVC - Data Version Control](https://dvc.org/) (สำหรับจัดการ data และ model files ขนาดใหญ่)