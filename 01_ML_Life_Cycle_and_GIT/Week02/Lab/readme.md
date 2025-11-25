# 🧪 Lab: Git for Machine Learning Development

---

## 📋 Lab Overview

In this lab, you will learn how to use Git commands to track changes in a Machine Learning project. You will build a complete ML pipeline step-by-step, committing your work at each stage.

**What you will learn:**

| Git Command | Description |
|-------------|-------------|
| `git init` | Initialize a new repository |
| `git status` | Check current state of files |
| `git add` | Stage changes for commit |
| `git commit` | Save changes with descriptive message |
| `git log` | View commit history |
| `git push` | Upload commits to remote repository |
| `git pull` | Download commits from remote repository |

**ML Skills Applied:**

- Data loading with Pandas
- Data preprocessing and splitting
- Model training with Scikit-learn
- Model evaluation with metrics
- Model comparison and selection



# ✅ Lab Completion Checklist (รายละเอียดแต่ละขั้นตอน)

| Step | Task | Git Command | รายละเอียด | Status |
|:----:|------|-------------|------------|:------:|
| **1** | **Initialize Git repository** | `git init` | **เริ่มต้นระบบ Version Control**<br>• สร้างโฟลเดอร์โปรเจกต์ใหม่ `ml-iris-classifier`<br>• รันคำสั่ง `git init` เพื่อสร้าง hidden folder `.git/` ที่จะเก็บประวัติการเปลี่ยนแปลงทั้งหมด<br>• ตรวจสอบสถานะด้วย `git status` เพื่อยืนยันว่า repository พร้อมใช้งาน<br>• **ผลลัพธ์:** โฟลเดอร์ว่างที่พร้อมสำหรับการ track การเปลี่ยนแปลง | ☐ |
| **2** | **Create data loading function** | `git add` + `git commit` | **สร้างฟังก์ชันโหลดข้อมูล Iris Dataset**<br>• สร้างไฟล์ `train.py` พร้อมฟังก์ชัน `load_data()`<br>• ใช้ `sklearn.datasets.load_iris()` โหลด dataset<br>• แปลงข้อมูลเป็น Pandas DataFrame พร้อม column names<br>• ทดสอบโค้ดด้วย `python train.py`<br>• **Git workflow:** `git add train.py` → `git commit -m "Step 2: Add data loading function"`<br>• **ผลลัพธ์:** DataFrame ขนาด (150, 5) พร้อม target column | ☐ |
| **3** | **Add data preprocessing** | `git add` + `git commit` | **เพิ่มการเตรียมข้อมูลและแบ่ง Train/Test**<br>• สร้างฟังก์ชัน `preprocess_data()` ใหม่<br>• แยก Features (X) ออกจาก Target (y)<br>• ใช้ `train_test_split()` แบ่งข้อมูล 80% train, 20% test<br>• กำหนด `random_state=42` เพื่อให้ผลลัพธ์ reproducible<br>• **Git workflow:** `git status` → `git add train.py` → `git commit`<br>• **ผลลัพธ์:** Training set 120 samples, Test set 30 samples | ☐ |
| **4** | **Implement model training** | `git add` + `git commit` | **สร้างฟังก์ชัน Train Model แรก (Decision Tree)**<br>• สร้างฟังก์ชัน `train_model()` ใหม่<br>• ใช้ `DecisionTreeClassifier` จาก sklearn<br>• เรียก `.fit(X_train, y_train)` เพื่อ train model<br>• ทดสอบว่า model ถูกสร้างสำเร็จ<br>• **Git workflow:** `git add` → `git commit -m "Step 4: Add Decision Tree model training"`<br>• **ผลลัพธ์:** Model object พร้อมใช้งานสำหรับ prediction | ☐ |
| **5** | **Add model evaluation** | `git add` + `git commit` | **เพิ่มการประเมินผล Model**<br>• สร้างฟังก์ชัน `evaluate_model()` ใหม่<br>• ใช้ `model.predict()` ทำนายผล test set<br>• คำนวณ `accuracy_score` วัดความแม่นยำ<br>• สร้าง `classification_report` แสดง precision, recall, f1-score<br>• ปรับปรุง main execution ให้แสดงผลสวยงาม<br>• **Git workflow:** `git add` → `git commit`<br>• **ผลลัพธ์:** รายงาน accuracy และ classification metrics ครบถ้วน | ☐ |
| **6** | **Compare multiple models** | `git add` + `git commit` | **เปรียบเทียบหลาย Models**<br>• เพิ่มฟังก์ชัน `train_random_forest()` ใหม่<br>• ใช้ `RandomForestClassifier` กับ `n_estimators=100`<br>• Train และ evaluate ทั้ง Decision Tree และ Random Forest<br>• เปรียบเทียบ accuracy ของทั้งสอง models<br>• แสดงผลสรุปว่า model ไหนดีกว่า<br>• **Git workflow:** `git add` → `git commit -m "Step 6: Add Random Forest and compare"`<br>• **ผลลัพธ์:** ตารางเปรียบเทียบ accuracy ระหว่าง 2 models | ☐ |
| **7** | **Add model saving** | `git add` + `git commit` | **บันทึก Model ที่ดีที่สุดลงไฟล์**<br>• สร้างฟังก์ชัน `save_model()` ใช้ `joblib.dump()`<br>• สร้างฟังก์ชัน `load_model()` ใช้ `joblib.load()`<br>• เลือก best model จากการเปรียบเทียบ accuracy<br>• บันทึกเป็นไฟล์ `best_model.joblib`<br>• ทดสอบโหลด model กลับมาและ verify accuracy<br>• สร้างไฟล์ `.gitignore` กำหนด files ที่ไม่ต้อง track<br>• **Git workflow:** `git add train.py .gitignore best_model.joblib` → `git commit`<br>• **ผลลัพธ์:** ไฟล์ model พร้อมใช้งานใน production | ☐ |
| **8** | **Push to GitHub** | `git push` | **อัปโหลดโค้ดขึ้น Remote Repository**<br>• สร้าง repository ใหม่บน GitHub (ไม่ต้อง initialize)<br>• เชื่อมต่อ local กับ remote: `git remote add origin <URL>`<br>• ตรวจสอบการเชื่อมต่อ: `git remote -v`<br>• Push ขึ้น GitHub: `git push -u origin main`<br>• ใส่ GitHub credentials (username + Personal Access Token)<br>• **ผลลัพธ์:** โค้ดทั้งหมดปรากฏบน GitHub พร้อม commit history ครบทุก step | ☐ |
| **9** | **Pull changes from remote** | `git pull` | **ดึงการเปลี่ยนแปลงจาก Remote (จำลองการทำงานเป็นทีม)**<br>• แก้ไขไฟล์ `train.py` บน GitHub โดยตรง (เพิ่ม author info)<br>• Commit การเปลี่ยนแปลงบน GitHub<br>• กลับมาที่ local terminal รัน `git pull origin main`<br>• Git จะดึง commits ใหม่และ merge เข้ากับ local<br>• ตรวจสอบ history ด้วย `git log --oneline`<br>• **ผลลัพธ์:** Local repository อัปเดตตรงกับ remote พร้อม commit ใหม่จาก "teammate" | ☐ |

---

## 📝 สรุป Git Workflow ในแต่ละ Step

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: git init                                               │
│  └── สร้าง repository เปล่า                                      │
├─────────────────────────────────────────────────────────────────┤
│  Step 2-7: วงจรการพัฒนาโค้ด (ทำซ้ำทุก feature)                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. แก้ไข/เพิ่มโค้ด                                       │    │
│  │  2. ทดสอบโค้ด (python train.py)                          │    │
│  │  3. git status   → ดูไฟล์ที่เปลี่ยนแปลง                    │    │
│  │  4. git add      → เลือกไฟล์ที่จะ commit                  │    │
│  │  5. git commit   → บันทึกการเปลี่ยนแปลงพร้อม message       │    │
│  │  6. git log      → ตรวจสอบ history                        │    │
│  └─────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│  Step 8: git push                                               │
│  └── อัปโหลดทุก commits ขึ้น GitHub                              │
├─────────────────────────────────────────────────────────────────┤
│  Step 9: git pull                                               │
│  └── ดึง commits ใหม่จาก GitHub มายัง local                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Let's Begin!

---

# Step 1: Initialize Git Repository

## 1.1 Create Project Folder

Open your terminal and run:

```bash
# Create project folder
mkdir ml-iris-classifier
cd ml-iris-classifier
```

## 1.2 Initialize Git

```bash
# Initialize empty Git repository
git init
```

**Expected output:**

```
Initialized empty Git repository in /path/to/ml-iris-classifier/.git/
```

## 1.3 Check Git Status

```bash
# Check repository status
git status
```

**Expected output:**

```
On branch main
No commits yet
nothing to commit (create or copy files and use "git add" to track)
```

✅ **Checkpoint:** You have created a new Git repository!

---

# Step 2: Create Project Structure & Load Data

## 2.1 Create Python File

Create a new file named `train.py`:

```python
# train.py
# Step 2: Load and explore the Iris dataset

import pandas as pd
from sklearn.datasets import load_iris

def load_data():
    """Load Iris dataset and return as DataFrame"""
    # Load built-in Iris dataset
    iris = load_iris()
    
    # Create DataFrame
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    
    # Add target column
    df['target'] = iris.target
    
    return df

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    
    # Show basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
```

## 2.2 Test Your Code

```bash
# Run the script
python train.py
```

**Expected output:**

```
Loading Iris dataset...

Dataset shape: (150, 5)

First 5 rows:
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  target
0                5.1               3.5                1.4               0.2       0
1                4.9               3.0                1.4               0.2       0
...
```

## 2.3 Stage and Commit Changes

```bash
# Check what files are untracked
git status
```

**Output:**

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        train.py
```

```bash
# Stage the file
git add train.py

# Check status again
git status
```

**Output:**

```
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   train.py
```

```bash
# Commit with descriptive message
git commit -m "Step 2: Add data loading function for Iris dataset"
```

## 2.4 View Commit History

```bash
# View commit log
git log --oneline
```

**Output:**

```
abc1234 (HEAD -> main) Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** First commit completed! Your data loading code is saved.

---

# Step 3: Add Data Preprocessing

## 3.1 Update train.py - Add Preprocessing

Edit `train.py` to add data splitting:

```python
# train.py
# Step 3: Add data preprocessing and splitting

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    # Separate features (X) and target (y)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42  # For reproducibility
    )
    
    return X_train, X_test, y_train, y_test

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\nSplitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
```

## 3.2 Test Your Code

```bash
python train.py
```

**Expected output:**

```
Loading Iris dataset...
Dataset shape: (150, 5)

Splitting data into train/test sets...
Training set size: 120
Test set size: 30
```

## 3.3 Stage and Commit Changes

```bash
# Check what changed
git status
```

**Output:**

```
Changes not staged for commit:
        modified:   train.py
```

```bash
# Stage changes
git add train.py

# Commit with message
git commit -m "Step 3: Add data preprocessing and train/test split"
```

## 3.4 View Updated History

```bash
git log --oneline
```

**Output:**

```
def5678 (HEAD -> main) Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** You now have 2 commits tracking your progress!

---

# Step 4: Train Initial Model

## 4.1 Update train.py - Add Model Training

Edit `train.py` to add a simple model:

```python
# train.py
# Step 4: Add model training with Decision Tree

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Train a Decision Tree classifier"""
    # Create model
    model = DecisionTreeClassifier(random_state=42)
    
    # Train model
    model.fit(X_train, y_train)
    
    return model

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\nSplitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    print("\nTraining Decision Tree model...")
    model = train_model(X_train, y_train)
    print("Model training completed!")
    print(f"Model type: {type(model).__name__}")
```

## 4.2 Test Your Code

```bash
python train.py
```

**Expected output:**

```
Loading Iris dataset...
Dataset shape: (150, 5)

Splitting data into train/test sets...
Training set size: 120
Test set size: 30

Training Decision Tree model...
Model training completed!
Model type: DecisionTreeClassifier
```

## 4.3 Stage and Commit

```bash
# Check status
git status

# Stage and commit
git add train.py
git commit -m "Step 4: Add Decision Tree model training"

# View history
git log --oneline
```

**Output:**

```
ghi9012 (HEAD -> main) Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Model training step committed!

---

# Step 5: Add Model Evaluation

## 5.1 Update train.py - Add Evaluation

Edit `train.py` to add evaluation metrics:

```python
# train.py
# Step 5: Add model evaluation

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Generate classification report
    report = classification_report(y_test, y_pred)
    
    return accuracy, report, y_pred

# Main execution
if __name__ == "__main__":
    # Load data
    print("=" * 50)
    print("IRIS CLASSIFICATION PIPELINE")
    print("=" * 50)
    
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train model
    print("\n[3] Training Decision Tree model...")
    model = train_model(X_train, y_train)
    print("    Model training completed!")
    
    # Evaluate model
    print("\n[4] Evaluating model...")
    accuracy, report, y_pred = evaluate_model(model, X_test, y_test)
    
    print(f"\n{'=' * 50}")
    print("EVALUATION RESULTS")
    print(f"{'=' * 50}")
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nClassification Report:\n{report}")
```

## 5.2 Test Your Code

```bash
python train.py
```

**Expected output:**

```
==================================================
IRIS CLASSIFICATION PIPELINE
==================================================

[1] Loading Iris dataset...
    Dataset shape: (150, 5)

[2] Splitting data into train/test sets...
    Training set size: 120
    Test set size: 30

[3] Training Decision Tree model...
    Model training completed!

[4] Evaluating model...

==================================================
EVALUATION RESULTS
==================================================

Accuracy: 1.0000 (100.00%)

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00        10
           1       1.00      1.00      1.00         9
           2       1.00      1.00      1.00        11

    accuracy                           1.00        30
   macro avg       1.00      1.00      1.00        30
weighted avg       1.00      1.00      1.00        30
```

## 5.3 Stage and Commit

```bash
git add train.py
git commit -m "Step 5: Add model evaluation with accuracy and classification report"

# View full history
git log --oneline
```

**Output:**

```
jkl3456 (HEAD -> main) Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Complete ML pipeline committed!

---

# Step 6: Improve Model (Try Different Algorithm)

## 6.1 Update train.py - Add Random Forest

Edit `train.py` to compare two models:

```python
# train.py
# Step 6: Compare Decision Tree vs Random Forest

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_decision_tree(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier"""
    model = RandomForestClassifier(
        n_estimators=100,  # Number of trees
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report, y_pred

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("IRIS CLASSIFICATION - MODEL COMPARISON")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train and evaluate Decision Tree
    print("\n" + "=" * 60)
    print("MODEL 1: Decision Tree")
    print("=" * 60)
    dt_model = train_decision_tree(X_train, y_train)
    dt_accuracy, dt_report, _ = evaluate_model(dt_model, X_test, y_test)
    print(f"Accuracy: {dt_accuracy:.4f} ({dt_accuracy*100:.2f}%)")
    
    # Train and evaluate Random Forest
    print("\n" + "=" * 60)
    print("MODEL 2: Random Forest")
    print("=" * 60)
    rf_model = train_random_forest(X_train, y_train)
    rf_accuracy, rf_report, _ = evaluate_model(rf_model, X_test, y_test)
    print(f"Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
    print(f"Random Forest Accuracy: {rf_accuracy*100:.2f}%")
    
    if rf_accuracy > dt_accuracy:
        print("\n✓ Random Forest performs better!")
    elif dt_accuracy > rf_accuracy:
        print("\n✓ Decision Tree performs better!")
    else:
        print("\n✓ Both models perform equally!")
```

## 6.2 Test Your Code

```bash
python train.py
```

## 6.3 Stage and Commit

```bash
git add train.py
git commit -m "Step 6: Add Random Forest and compare with Decision Tree"

# View history
git log --oneline
```

**Output:**

```
mno7890 (HEAD -> main) Step 6: Add Random Forest and compare with Decision Tree
jkl3456 Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Model comparison committed!

---

# Step 7: Save Model to File

## 7.1 Update train.py - Add Model Saving

Edit `train.py` to save the best model:

```python
# train.py
# Step 7: Save the best model to file

import pandas as pd
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_decision_tree(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier"""
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report, y_pred

def save_model(model, filename):
    """Save model to file using joblib"""
    joblib.dump(model, filename)
    print(f"Model saved to: {filename}")

def load_model(filename):
    """Load model from file"""
    model = joblib.load(filename)
    print(f"Model loaded from: {filename}")
    return model

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("IRIS CLASSIFICATION - TRAIN AND SAVE MODEL")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train models
    print("\n[3] Training models...")
    dt_model = train_decision_tree(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    
    # Evaluate models
    print("\n[4] Evaluating models...")
    dt_accuracy, _, _ = evaluate_model(dt_model, X_test, y_test)
    rf_accuracy, _, _ = evaluate_model(rf_model, X_test, y_test)
    
    print(f"    Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
    print(f"    Random Forest Accuracy: {rf_accuracy*100:.2f}%")
    
    # Select and save best model
    print("\n[5] Saving best model...")
    if rf_accuracy >= dt_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
    else:
        best_model = dt_model
        best_name = "Decision Tree"
    
    save_model(best_model, "best_model.joblib")
    print(f"    Best model: {best_name}")
    
    # Verify saved model works
    print("\n[6] Verifying saved model...")
    loaded_model = load_model("best_model.joblib")
    loaded_accuracy, _, _ = evaluate_model(loaded_model, X_test, y_test)
    print(f"    Loaded model accuracy: {loaded_accuracy*100:.2f}%")
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
```

## 7.2 Test Your Code

```bash
python train.py
```

## 7.3 Create .gitignore

Create `.gitignore` to manage which files Git should track:

```bash
# Create .gitignore file
echo "# Python cache files" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "" >> .gitignore
echo "# Optional: Ignore large model files" >> .gitignore
echo "# *.joblib" >> .gitignore
```

## 7.4 Stage and Commit All Files

```bash
# Check status - you should see new files
git status

# Add all files
git add train.py
git add .gitignore
git add best_model.joblib

# Commit
git commit -m "Step 7: Add model saving and loading with joblib"

# View complete history
git log --oneline
```

**Output:**

```
pqr1234 (HEAD -> main) Step 7: Add model saving and loading with joblib
mno7890 Step 6: Add Random Forest and compare with Decision Tree
jkl3456 Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Complete pipeline with model saving!

---

# Step 8: Push to Remote Repository (GitHub)

## 8.1 Create Repository on GitHub

1. Go to https://github.com
2. Click **"New repository"** (green button)
3. Repository name: `ml-iris-classifier`
4. Choose **Public** or **Private**
5. ⚠️ **Do NOT** check "Initialize this repository with a README"
6. Click **"Create repository"**

## 8.2 Connect Local to Remote

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ml-iris-classifier.git

# Verify remote connection
git remote -v
```

**Output:**

```
origin  https://github.com/YOUR_USERNAME/ml-iris-classifier.git (fetch)
origin  https://github.com/YOUR_USERNAME/ml-iris-classifier.git (push)
```

## 8.3 Push to GitHub

```bash
# Push main branch to remote
git push -u origin main
```

You will be prompted for GitHub credentials (username and personal access token).

**Output:**

```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Writing objects: 100% (15/15), 3.45 KiB | 3.45 MiB/s, done.
Total 15 (delta 0), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/ml-iris-classifier.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Checkpoint:** Your code is now on GitHub!

---

# Step 9: Simulate Team Collaboration (Pull)

## 9.1 Make Changes on GitHub (Simulate Teammate)

1. Go to your repository on GitHub
2. Click on `train.py`
3. Click the **pencil icon** (Edit this file)
4. Add these lines at the top of the file:

```python
# train.py
# Author: Your Name
# Date: 2024
# Description: Iris Classification Pipeline for MLOps Lab
```

5. Scroll down and click **"Commit changes"**
6. Add commit message: `Add author information`

## 9.2 Pull Changes to Local

```bash
# Check current status
git status

# Pull changes from remote
git pull origin main
```

**Output:**

```
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Total 3 (delta 1), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
From https://github.com/YOUR_USERNAME/ml-iris-classifier
   pqr1234..stu5678  main -> origin/main
Updating pqr1234..stu5678
Fast-forward
 train.py | 4 ++++
 1 file changed, 4 insertions(+)
```

## 9.3 View Updated History

```bash
git log --oneline
```

**Output:**

```
stu5678 (HEAD -> main, origin/main) Add author information
pqr1234 Step 7: Add model saving and loading with joblib
mno7890 Step 6: Add Random Forest and compare with Decision Tree
jkl3456 Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** You successfully pulled changes from remote!

---

# 📊 Git Commands Summary

| Command | Description | When to Use |
|---------|-------------|-------------|
| `git init` | Initialize new repository | Start of project (once) |
| `git status` | Check current state | Before add/commit |
| `git add <file>` | Stage specific file | After modifying code |
| `git add .` | Stage all changed files | After modifying multiple files |
| `git commit -m "msg"` | Save staged changes | After completing a feature |
| `git log` | View full commit history | Review project history |
| `git log --oneline` | View compact history | Quick overview |
| `git remote add` | Connect to GitHub | Setup (once) |
| `git push` | Upload to GitHub | Share your work |
| `git pull` | Download from GitHub | Get team updates |

---
