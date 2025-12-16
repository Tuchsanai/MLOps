# Lab 01: Git Fundamentals for MLOps

## 🎯 วัตถุประสงค์การเรียนรู้

หลังจากทำ Lab นี้เสร็จ นักศึกษาจะสามารถ:
1. อธิบายความสำคัญของ Version Control ในโปรเจค ML ได้
2. ใช้คำสั่ง Git พื้นฐาน (init, add, commit, diff, log) ได้
3. สร้าง `.gitignore` ที่เหมาะสมสำหรับโปรเจค ML ได้
4. แยกแยะได้ว่าไฟล์ใดควร track และไฟล์ใดไม่ควร track

---

## 📋 Pipeline Overview

### ภาพรวมของ Lab

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ML Project with Git Workflow                         │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1-2: Project Setup & First Commit
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   git init   │───▶│ Create Files │───▶│   git add    │───▶│  git commit  │
│              │    │  train.py    │    │   (stage)    │    │  (snapshot)  │
│ สร้าง repo   │    │  config.py   │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘

Step 3: Modify & Track Changes
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Edit train.py│───▶│   git diff   │───▶│   git add    │───▶│  git commit  │
│ (use config) │    │ ดูการเปลี่ยน  │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘

Step 4: Ignore ML Artifacts
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Run train.py │───▶│   สร้าง       │───▶│  git status  │
│ สร้าง model  │    │  .gitignore  │    │ ไม่เห็น model │
└──────────────┘    └──────────────┘    └──────────────┘

Step 5-6: Complete & Review
┌──────────────┐    ┌──────────────┐
│ Add predict  │───▶│   git log    │
│    .py       │    │  ดู history  │
└──────────────┘    └──────────────┘
```

---

### Git Areas ที่ต้องเข้าใจ

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Git Three Areas                                │
└─────────────────────────────────────────────────────────────────────────────┘

  Working Directory          Staging Area              Repository
  (โฟลเดอร์งาน)              (พื้นที่เตรียม)            (ประวัติถาวร)
 ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
 │                 │      │                 │      │                 │
 │   train.py ●    │      │   train.py ●    │      │   Commit #1     │
 │   config.py ●   │─────▶│   config.py ●   │─────▶│   Commit #2     │
 │   model.pkl ✗   │      │                 │      │   Commit #3     │
 │                 │ add  │                 │commit│       ▲         │
 │                 │      │                 │      │       │         │
 └─────────────────┘      └─────────────────┘      └───────┼─────────┘
                                                          │
        ● = tracked files                                 │
        ✗ = ignored files                            git log
```

---

### ไฟล์ในโปรเจค ML: Track vs Ignore

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ML Project Files Classification                          │
└─────────────────────────────────────────────────────────────────────────────┘

         ✅ TRACK (เก็บใน Git)              ❌ IGNORE (ไม่เก็บใน Git)
        ─────────────────────              ──────────────────────────
        
        ┌─────────────────┐                ┌─────────────────┐
        │   train.py      │                │   model.pkl     │
        │   (source code) │                │   (binary file) │
        └─────────────────┘                └─────────────────┘
        
        ┌─────────────────┐                ┌─────────────────┐
        │   config.py     │                │   data/*.csv    │
        │   (settings)    │                │   (large files) │
        └─────────────────┘                └─────────────────┘
        
        ┌─────────────────┐                ┌─────────────────┐
        │   predict.py    │                │   logs/*.log    │
        │   (source code) │                │   (generated)   │
        └─────────────────┘                └─────────────────┘
        
        ┌─────────────────┐                ┌─────────────────┐
        │   .gitignore    │                │   .env          │
        │   (config)      │                │   (secrets!)    │
        └─────────────────┘                └─────────────────┘
        
        ┌─────────────────┐                ┌─────────────────┐
        │ requirements.txt│                │  __pycache__/   │
        │   (deps list)   │                │   (cache)       │
        └─────────────────┘                └─────────────────┘
```

---

### โครงสร้างโปรเจคที่จะสร้าง

```
ml-git-lab01_advance/
├── .git/                  # Git repository (ซ่อนอยู่)
├── .gitignore             # ✅ กำหนดไฟล์ที่ไม่ต้อง track
├── config.py              # ✅ Hyperparameters
├── train.py               # ✅ Training script
├── predict.py             # ✅ Prediction script
├── model.pkl              # ❌ Ignored (generated)
├── .env                   # ❌ Ignored (secrets)
├── data/                  # ❌ Ignored (data files)
│   └── dataset.csv
└── logs/                  # ❌ Ignored (logs)
    └── training.log
```

---

### คำสั่ง Git ที่จะใช้ใน Lab

| คำสั่ง | หน้าที่ | เมื่อไหร่ใช้ |
|--------|---------|-------------|
| `git config` | ตั้งค่า Git | ก่อนเริ่มใช้งานครั้งแรก |
| `git init` | สร้าง repository ใหม่ | เริ่มโปรเจคใหม่ |
| `git status` | ดูสถานะไฟล์ | ก่อน add/commit |
| `git add <file>` | เพิ่มไฟล์เข้า staging | เตรียม commit |
| `git commit -m "msg"` | บันทึก snapshot | หลัง add |
| `git diff` | ดูความเปลี่ยนแปลง | ก่อน add |
| `git log` | ดูประวัติ commits | ตรวจสอบ history |
| `git branch -m` | เปลี่ยนชื่อ branch | จัดการ branch |

---

## 📝 Prerequisites

- Git ติดตั้งแล้ว (`git --version`)
- Python 3.x พร้อม scikit-learn (`pip install scikit-learn`)

---

## ⚙️ Git Configuration (ทำครั้งเดียวก่อนเริ่ม Lab)

ก่อนเริ่มใช้งาน Git ต้องตั้งค่าข้อมูลประจำตัวของผู้ใช้ก่อน เพื่อให้ Git รู้ว่าใครเป็นคนทำการเปลี่ยนแปลง

### ตั้งค่าชื่อผู้ใช้และอีเมล

```bash
git config --global user.name "YourUsername"
git config --global user.email "youremail@example.com"
```

📤 **ไม่มี Output** (ถ้าสำเร็จจะไม่แสดงอะไร)

---

### ตรวจสอบการตั้งค่า

```bash
git config --global --list
```

📤 **Expected Output:**
```
user.name=YourUsername
user.email=youremail@example.com
```

---

### 💡 คำอธิบาย

| Option | ความหมาย |
|--------|----------|
| `--global` | ตั้งค่าสำหรับทุก repository ในเครื่อง (ถ้าไม่ใส่จะตั้งค่าเฉพาะ repo ปัจจุบัน) |
| `user.name` | ชื่อที่จะแสดงใน commit history (ควรใช้ชื่อจริงหรือ username ที่ใช้ใน GitHub) |
| `user.email` | อีเมลที่ใช้ (ควรตรงกับอีเมลที่ลงทะเบียนใน GitHub เพื่อเชื่อมโยง commit กับบัญชี) |

> ⚠️ **สำคัญ**: ข้อมูลนี้จะถูกบันทึกในทุก commit ที่คุณสร้าง และจะแสดงให้คนอื่นเห็นเมื่อ push ขึ้น GitHub ดังนั้นควรใช้ข้อมูลที่เหมาะสม

---

### ทำไมต้องตั้งค่านี้?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Commit ประกอบด้วยอะไรบ้าง?                          │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │  commit abc1234                                              │
  │  Author: YourUsername <youremail@example.com>  ◀── จาก config│
  │  Date:   Mon Jan 1 10:00:00 2024 +0700                       │
  │                                                              │
  │      Initial commit: training script and config              │
  │                                                              │
  │  Files changed:                                              │
  │      config.py (new)                                         │
  │      train.py (new)                                          │
  └──────────────────────────────────────────────────────────────┘
```

ทุกครั้งที่ทำ `git commit` Git จะบันทึก:
- **ใคร** ทำการเปลี่ยนแปลง (จาก `user.name` และ `user.email`)
- **เมื่อไหร่** (timestamp อัตโนมัติ)
- **อะไร** เปลี่ยนแปลง (ไฟล์ที่ถูก staged)
- **ทำไม** (จาก commit message)

---

### ระดับของ Git Config

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Git Config Levels                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Level          │  Flag       │  ไฟล์ที่เก็บ           │  ขอบเขต        │
  ├─────────────────┼─────────────┼───────────────────────┼────────────────┤
  │  System         │  --system   │  /etc/gitconfig       │  ทุก user      │
  │  Global (User)  │  --global   │  ~/.gitconfig         │  user ปัจจุบัน  │
  │  Local (Repo)   │  --local    │  .git/config          │  repo นี้เท่านั้น│
  └─────────────────────────────────────────────────────────────────────────┘
  
  Priority (สูง → ต่ำ): Local > Global > System
```

> 💡 **Tip**: ใช้ `--global` สำหรับการตั้งค่าทั่วไป แต่ถ้าต้องการใช้ชื่อ/อีเมลต่างกันในแต่ละโปรเจค ให้ใช้ `--local` (หรือไม่ใส่ flag) ภายใน repository นั้น

---

## 🔬 Lab Instructions

### Step 1: Initial Setup

1. **สร้างโฟลเดอร์โปรเจค**:
```bash
mkdir ml-git-lab01_advance
cd ml-git-lab01_advance
```

2. **Initialize Git repository**:
```bash
git init
```

📤 **Expected Output:**
```
Initialized empty Git repository in /path/to/ml-git-lab01_advance/.git/
```

> 💡 **สังเกต**: จะเห็นข้อความ "Initialized empty Git repository" และมีโฟลเดอร์ `.git` ซ่อนอยู่

---

### Step 2: Create ML Project Files

1. **สร้าง training script** (`train.py`):
```bash
cat > train.py << 'EOF'
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to model.pkl")
EOF
```

📄 **ไฟล์ที่สร้าง: `train.py`**
```python
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to model.pkl")
```

---

2. **สร้าง configuration file** (`config.py`):
```bash
cat > config.py << 'EOF'
# Model hyperparameters
N_ESTIMATORS = 100
RANDOM_STATE = 42
TEST_SIZE = 0.2
EOF
```

📄 **ไฟล์ที่สร้าง: `config.py`**
```python
# Model hyperparameters
N_ESTIMATORS = 100
RANDOM_STATE = 42
TEST_SIZE = 0.2
```

---

3. **ตรวจสอบสถานะ**:
```bash
git status
```

📤 **Expected Output:**
```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config.py
        train.py

nothing added to commit but untracked files present (use "git add" to track)
```

> 💡 **สังเกต**: `train.py` และ `config.py` เป็น "Untracked files" (สีแดงใน terminal)

---

4. **Stage ไฟล์**:
```bash
git add train.py config.py
git status
```

📤 **Expected Output:**
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   config.py
        new file:   train.py
```

> 💡 **สังเกต**: ไฟล์เปลี่ยนเป็น "Changes to be committed" (สีเขียวใน terminal)

---

5. **Commit**:
```bash
git commit -m "Initial commit: training script and config"
```

📤 **Expected Output:**
```
[master (root-commit) abc1234] Initial commit: training script and config
 2 files changed, 24 insertions(+)
 create mode 100644 config.py
 create mode 100644 train.py
```

---

### Step 3: Modify Code and Use `git diff`

1. **แก้ไข train.py ให้ใช้ค่าจาก config**:
```bash
cat > train.py << 'EOF'
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from config import N_ESTIMATORS, RANDOM_STATE, TEST_SIZE

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

# Train model
model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to model.pkl")
EOF
```

📄 **ไฟล์ที่แก้ไข: `train.py` (Version 2)**
```python
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from config import N_ESTIMATORS, RANDOM_STATE, TEST_SIZE  # ← NEW: import config

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE  # ← CHANGED: use config values
)

# Train model
model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)  # ← CHANGED
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to model.pkl")
```

---

🔍 **การเปรียบเทียบ Before vs After:**

| บรรทัด | Before (Version 1) | After (Version 2) |
|--------|-------------------|-------------------|
| 6 | *(ไม่มี)* | `from config import N_ESTIMATORS, RANDOM_STATE, TEST_SIZE` |
| 10 | `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)` | `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)` |
| 13 | `model = RandomForestClassifier(n_estimators=100, random_state=42)` | `model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)` |

---

2. **ดูความเปลี่ยนแปลงด้วย `git diff`**:
```bash
git diff
```

📤 **Expected Output:**
```diff
diff --git a/train.py b/train.py
index abc1234..def5678 100644
--- a/train.py
+++ b/train.py
@@ -3,14 +3,16 @@ from sklearn.datasets import load_iris
 from sklearn.model_selection import train_test_split
 from sklearn.ensemble import RandomForestClassifier
 from sklearn.metrics import accuracy_score
+from config import N_ESTIMATORS, RANDOM_STATE, TEST_SIZE
 
 # Load data
 X, y = load_iris(return_X_y=True)
-X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
+X_train, X_test, y_train, y_test = train_test_split(
+    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
+)
 
 # Train model
-model = RandomForestClassifier(n_estimators=100, random_state=42)
+model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
 model.fit(X_train, y_train)
 
 # Evaluate
```

> 💡 **อ่าน diff output:**
> - บรรทัดที่ขึ้นต้นด้วย `-` (สีแดง) = บรรทัดที่ถูกลบ
> - บรรทัดที่ขึ้นต้นด้วย `+` (สีเขียว) = บรรทัดที่ถูกเพิ่ม
> - บรรทัดที่ไม่มีเครื่องหมาย = บรรทัดที่ไม่เปลี่ยนแปลง (context)

---

3. **Commit การเปลี่ยนแปลง**:
```bash
git add train.py
git commit -m "Refactor: use config for hyperparameters"
```

📤 **Expected Output:**
```
[master def5678] Refactor: use config for hyperparameters
 1 file changed, 5 insertions(+), 3 deletions(-)
```

---

### Step 4: Ignore ML Artifacts with `.gitignore`

1. **รัน training เพื่อสร้าง model file**:
```bash
python train.py
```

📤 **Expected Output:**
```
Accuracy: 1.0000
Model saved to model.pkl
```

> 📁 **ไฟล์ที่ถูกสร้าง:** `model.pkl` (binary file ~5KB)

---

2. **สร้างไฟล์ที่ไม่ควร track**:
```bash
mkdir -p data logs
echo "sample,data" > data/dataset.csv
echo "2024-01-01 Training started..." > logs/training.log
echo "API_KEY=secret123" > .env
```

📁 **ไฟล์ที่ถูกสร้าง:**

**`data/dataset.csv`:**
```csv
sample,data
```

**`logs/training.log`:**
```
2024-01-01 Training started...
```

**`.env`:**
```
API_KEY=secret123
```

---

3. **ตรวจสอบสถานะ (ก่อนสร้าง .gitignore)**:
```bash
git status
```

📤 **Expected Output:**
```
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env
        data/
        logs/
        model.pkl

nothing added to commit but untracked files present (use "git add" to track)
```

> ⚠️ **ปัญหา**: Git เห็นทุกไฟล์ที่สร้างใหม่ รวมถึงไฟล์ที่ไม่ควร track!

---

4. **สร้าง `.gitignore`**:
```bash
cat > .gitignore << 'EOF'
# Model artifacts
*.pkl
*.joblib
*.h5

# Data files
data/
*.csv

# Logs
logs/
*.log

# Environment and secrets
.env
.env.*

# Python cache
__pycache__/
*.pyc
.ipynb_checkpoints/
EOF
```

📄 **ไฟล์ที่สร้าง: `.gitignore`**
```gitignore
# Model artifacts
*.pkl
*.joblib
*.h5

# Data files
data/
*.csv

# Logs
logs/
*.log

# Environment and secrets
.env
.env.*

# Python cache
__pycache__/
*.pyc
.ipynb_checkpoints/
```

> 💡 **Pattern ที่ใช้:**
> - `*.pkl` = ignore ทุกไฟล์ที่ลงท้ายด้วย `.pkl`
> - `data/` = ignore ทั้งโฟลเดอร์ `data`
> - `.env.*` = ignore ไฟล์ที่ขึ้นต้นด้วย `.env.` เช่น `.env.local`, `.env.production`

---

5. **ตรวจสอบสถานะอีกครั้ง (หลังสร้าง .gitignore)**:
```bash
git status
```

📤 **Expected Output:**
```
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore

nothing added to commit but untracked files present (use "git add" to track)
```

> ✅ **สำเร็จ!** เห็นเฉพาะ `.gitignore` — ไม่เห็น `model.pkl`, `.env`, `data/`, `logs/` แล้ว

---

🔍 **เปรียบเทียบ git status: Before vs After `.gitignore`**

| Before .gitignore | After .gitignore |
|-------------------|------------------|
| `.env` ❌ | *(hidden)* |
| `data/` ❌ | *(hidden)* |
| `logs/` ❌ | *(hidden)* |
| `model.pkl` ❌ | *(hidden)* |
| | `.gitignore` ✅ |

---

6. **Commit .gitignore**:
```bash
git add .gitignore
git commit -m "Add .gitignore for ML artifacts"
```

📤 **Expected Output:**
```
[master ghi9012] Add .gitignore for ML artifacts
 1 file changed, 18 insertions(+)
 create mode 100644 .gitignore
```

---

### Step 5: Add Prediction Script

1. **สร้าง prediction script**:
```bash
cat > predict.py << 'EOF'
import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Sample prediction
sample = np.array([[5.1, 3.5, 1.4, 0.2]])
prediction = model.predict(sample)
species = ["setosa", "versicolor", "virginica"]
print(f"Predicted species: {species[prediction[0]]}")
EOF
```

📄 **ไฟล์ที่สร้าง: `predict.py`**
```python
import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Sample prediction
sample = np.array([[5.1, 3.5, 1.4, 0.2]])
prediction = model.predict(sample)
species = ["setosa", "versicolor", "virginica"]
print(f"Predicted species: {species[prediction[0]]}")
```

---

2. **ทดสอบรัน**:
```bash
python predict.py
```

📤 **Expected Output:**
```
Predicted species: setosa
```

---

3. **ตรวจสอบสถานะและ Commit**:
```bash
git status
```

📤 **Expected Output:**
```
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        predict.py

nothing added to commit but untracked files present (use "git add" to track)
```

```bash
git add predict.py
git commit -m "Add prediction script"
```

📤 **Expected Output:**
```
[master jkl3456] Add prediction script
 1 file changed, 12 insertions(+)
 create mode 100644 predict.py
```

---

### Step 6: Review History

```bash
git log --oneline --graph --all
```

📤 **Expected Output:**
```
* jkl3456 (HEAD -> master) Add prediction script
* ghi9012 Add .gitignore for ML artifacts
* def5678 Refactor: use config for hyperparameters
* abc1234 Initial commit: training script and config
```

> 💡 **อ่าน git log:**
> - `*` = commit
> - `(HEAD -> master)` = ตำแหน่งปัจจุบัน
> - hash (`jkl3456`) = commit ID ย่อ
> - ข้อความหลัง hash = commit message

---

**ดูรายละเอียดเพิ่มเติม:**
```bash
git log --stat
```

📤 **Expected Output:**
```
commit jkl3456...
Author: Your Name <your@email.com>
Date:   Mon Jan 1 12:00:00 2024 +0700

    Add prediction script

 predict.py | 12 ++++++++++++
 1 file changed, 12 insertions(+)

commit ghi9012...
Author: Your Name <your@email.com>
Date:   Mon Jan 1 11:30:00 2024 +0700

    Add .gitignore for ML artifacts

 .gitignore | 18 ++++++++++++++++++
 1 file changed, 18 insertions(+)

commit def5678...
Author: Your Name <your@email.com>
Date:   Mon Jan 1 11:00:00 2024 +0700

    Refactor: use config for hyperparameters

 train.py | 8 +++++---
 1 file changed, 5 insertions(+), 3 deletions(-)

commit abc1234...
Author: Your Name <your@email.com>
Date:   Mon Jan 1 10:00:00 2024 +0700

    Initial commit: training script and config

 config.py |  4 ++++
 train.py  | 20 ++++++++++++++++++++
 2 files changed, 24 insertions(+)
```

---

### Step 7: Rename Branch (Optional)

1. **ดู branch ปัจจุบัน**:
```bash
git branch
```

📤 **Expected Output:**
```
* master
```

2. **เปลี่ยนชื่อเป็น main**:
```bash
git branch -m main
git branch
```

📤 **Expected Output:**
```
* main
```

---

## 📊 สรุปไฟล์ทั้งหมดในโปรเจค

### ไฟล์ที่ Track (อยู่ใน Git)

| ไฟล์ | ขนาดโดยประมาณ | สร้างใน Step |
|------|---------------|--------------|
| `train.py` | ~600 bytes | Step 2, แก้ไขใน Step 3 |
| `config.py` | ~80 bytes | Step 2 |
| `.gitignore` | ~200 bytes | Step 4 |
| `predict.py` | ~300 bytes | Step 5 |

### ไฟล์ที่ Ignore (ไม่อยู่ใน Git)

| ไฟล์ | ทำไมไม่ track | สร้างใน Step |
|------|---------------|--------------|
| `model.pkl` | Binary file, สร้างใหม่ได้ | Step 4 |
| `.env` | มี secrets/API keys | Step 4 |
| `data/dataset.csv` | Data files ใหญ่ | Step 4 |
| `logs/training.log` | Generated files | Step 4 |

---

## ✅ Checklist สิ่งที่ต้องทำได้

- [ ] ตั้งค่า Git config (user.name, user.email) ได้
- [ ] สร้าง Git repository ใหม่ได้
- [ ] ใช้ `git status` ตรวจสอบสถานะได้
- [ ] ใช้ `git add` และ `git commit` ได้
- [ ] ใช้ `git diff` ดูการเปลี่ยนแปลงได้
- [ ] สร้าง `.gitignore` สำหรับ ML project ได้
- [ ] อธิบายได้ว่าทำไม model files ไม่ควรเก็บใน Git

---

## 📚 Summary

| คำสั่ง | หน้าที่ |
|--------|---------|
| `git config --global` | ตั้งค่า Git สำหรับทุก repo |
| `git init` | สร้าง repository |
| `git status` | ดูสถานะไฟล์ |
| `git add` | Stage ไฟล์ |
| `git commit` | บันทึก snapshot |
| `git diff` | ดูความเปลี่ยนแปลง |
| `.gitignore` | กำหนดไฟล์ที่ไม่ track |
| `git log` | ดูประวัติ |
| `git branch -m` | เปลี่ยนชื่อ branch |

---

## 🔑 Key Takeaways

1. **ก่อนใช้ Git ครั้งแรก** → ตั้งค่า `user.name` และ `user.email` ด้วย `git config --global`
2. **ทุกครั้งที่สร้างไฟล์** → ตรวจสอบด้วย `git status`
3. **ก่อน commit** → ใช้ `git diff` ดูว่าเปลี่ยนอะไรบ้าง
4. **ML project ต้องมี `.gitignore`** → ไม่ track model files, data, secrets
5. **Commit message ควรอธิบาย "ทำอะไร"** → เช่น "Add", "Fix", "Refactor"