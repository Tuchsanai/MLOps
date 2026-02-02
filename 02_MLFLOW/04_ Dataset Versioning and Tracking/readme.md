# 🚀 Lab: Model Deployment with MLflow

## 📋 ภาพรวมของ Lab

Lab นี้จะพานักศึกษาไปเรียนรู้การนำโมเดล Machine Learning ไป Deploy เป็น REST API โดยใช้ MLflow ซึ่งเป็นทักษะสำคัญในการทำงานจริง เพราะโมเดลที่ Train เสร็จแล้วจะไม่มีประโยชน์ถ้าไม่สามารถนำไปใช้งานได้

### 🎯 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. **บันทึกและลงทะเบียนโมเดล** - Log model พร้อม metadata และ register เข้า Model Registry
2. **Deploy โมเดลเป็น REST API** - ใช้ MLflow Model Serving เปิดให้บริการโมเดล
3. **เรียกใช้โมเดลผ่าน HTTP** - ส่ง request ไปยัง API และรับผลลัพธ์กลับมา
4. **จัดการ Model Versioning** - เปลี่ยน Stage ของโมเดล (Staging → Production)

---

## 📚 ทฤษฎี: Model Deployment with MLflow

### MLflow Models Component

**MLflow Models** เป็น component ที่ใช้สำหรับ packaging และ deploying โมเดล โดยมีคุณสมบัติหลัก:

```
┌─────────────────────────────────────────────────────────────┐
│                      MLflow Models                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │   Model Flavor  │    │  Model Serving  │                │
│  ├─────────────────┤    ├─────────────────┤                │
│  │ • sklearn       │    │ • REST API      │                │
│  │ • pytorch       │    │ • Batch         │                │
│  │ • tensorflow    │    │ • Streaming     │                │
│  │ • onnx          │    │                 │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  ┌─────────────────────────────────────────┐               │
│  │           Model Registry                 │               │
│  ├─────────────────────────────────────────┤               │
│  │ • Version Control                        │               │
│  │ • Stage Management (Staging/Production)  │               │
│  │ • Model Lineage                          │               │
│  └─────────────────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### MLflow Model Registry

**Model Registry** เป็นที่เก็บโมเดลแบบรวมศูนย์ ช่วยจัดการ version และ stage ของโมเดล:

```
┌─────────────────────────────────────────────────────────────┐
│                 Model Registry Workflow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌────────┐      ┌─────────┐      ┌────────────┐          │
│   │  None  │ ──>  │ Staging │ ──>  │ Production │          │
│   └────────┘      └─────────┘      └────────────┘          │
│       │               │                  │                  │
│    Register        ทดสอบ             Deploy                │
│    โมเดล           QA/UAT           ใช้งานจริง              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Stage | คำอธิบาย |
|-------|----------|
| **None** | โมเดลที่เพิ่ง register |
| **Staging** | โมเดลที่กำลังทดสอบ |
| **Production** | โมเดลที่ใช้งานจริง |
| **Archived** | โมเดลเก่าที่เก็บถาวร |

### MLflow Model Serving

**mlflow models serve** คือคำสั่งสำหรับ deploy โมเดลเป็น REST API:

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                       MLflow Model Serving Architecture                        ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║    ┌─────────────────┐       ┌─────────────────────┐       ┌────────────────┐  ║
║    │                 │       │                     │       │                │  ║
║    │     Client      │       │   MLflow Serving    │       │     Model      │  ║
║    │                 │ HTTP  │                     │ Load  │                │  ║
║    │  ┌───────────┐  │ ───▶  │  ┌───────────────┐  │ ───▶  │  ┌──────────┐  │  ║
║    │  │  Request  │  │       │  │  REST API     │  │       │  │ Artifact │  │  ║
║    │  │  (JSON)   │  │       │  │  /invocations │  │       │  │ (.pkl)   │  │  ║
║    │  └───────────┘  │ ◀───  │  └───────────────┘  │ ◀───  │  └──────────┘  │  ║
║    │                 │ JSON  │                     │Predict│                │  ║
║    └─────────────────┘       └─────────────────────┘       └────────────────┘  ║
║                                                                                ║
║      📱 curl / Python           🖥️ localhost:5001           📦 MLflow Model    ║
║         requests                                               Registry        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

**คำสั่ง Deploy:**
```bash
mlflow models serve -m "models:/<MODEL_NAME>/<VERSION>" --port <PORT> --no-conda
```

| Parameter | คำอธิบาย |
|-----------|----------|
| `-m` | ที่อยู่ของโมเดล (models:/name/version หรือ models:/name/Stage) |
| `--port` | Port ที่จะเปิด API |
| `--no-conda` | ไม่สร้าง conda environment ใหม่ |

### 🔄 Flow การทำงานใน Lab

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Train     │ -> │   Log &     │ -> │   Deploy    │ -> │   Predict   │
│   Model     │    │  Register   │    │   as API    │    │   via HTTP  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 📁 Part 1: เตรียมสภาพแวดล้อม

ก่อนเริ่มทำ Lab เราต้องเตรียมเครื่องมือและโครงสร้างโปรเจคให้พร้อม

### Step 1.1: ติดตั้ง Dependencies

เปิด Terminal แล้วรันคำสั่งต่อไปนี้เพื่อติดตั้ง library ที่จำเป็น:

```bash
pip install requests
```

### Step 1.2: สร้างโครงสร้างโปรเจค

สร้างโฟลเดอร์สำหรับเก็บไฟล์ Lab:

```bash
# สร้างโฟลเดอร์หลักและโฟลเดอร์ย่อย
mkdir -p ~/mlflow-deployment-lab/{models,data}
```

**โครงสร้างที่ได้:**
```
mlflow-deployment-lab/
├── train_sklearn.py      # ไฟล์ train โมเดล Scikit-Learn
├── train_pytorch.py      # ไฟล์ train โมเดล PyTorch
├── predict_client.py     # ไฟล์เรียกใช้ API
├── model_management.py   # ไฟล์จัดการ Model Stage
├── models/               # เก็บโมเดลที่ export
├── data/                 # เก็บข้อมูล
├── mlruns_db/            # เก็บ MLflow database
└── mlartifacts/          # เก็บ MLflow artifacts
```

### Step 1.3: เริ่ม MLflow Tracking Server

MLflow Server ทำหน้าที่เป็นศูนย์กลางในการเก็บข้อมูล experiment และโมเดล

**สร้างโฟลเดอร์สำหรับ Server:**

```bash
# สร้างโฟลเดอร์สำหรับเก็บข้อมูล MLflow
mkdir -p ~/mlflow-deployment-lab/mlruns_db
mkdir -p ~/mlflow-deployment-lab/mlartifacts

# เข้าไปในโฟลเดอร์ lab
cd ~/mlflow-deployment-lab
```

**เริ่ม Server:**

```bash
# รัน MLflow Server ใน background
nohup mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:///$(pwd)/mlruns_db/mlflow.db \
  --artifacts-destination $(pwd)/mlartifacts \
  --serve-artifacts > mlflow.log 2>&1 &
```

**อธิบายพารามิเตอร์:**
| Parameter | ความหมาย |
|-----------|----------|
| `--host 0.0.0.0` | เปิดให้เข้าถึงได้จากทุก IP |
| `--port 5000` | ใช้ port 5000 |
| `--backend-store-uri` | ที่เก็บข้อมูล experiment (SQLite) |
| `--artifacts-destination` | ที่เก็บไฟล์ model artifacts |
| `--serve-artifacts` | เปิดให้ดาวน์โหลด artifacts ได้ |

**ทดสอบ:** เปิด browser ไปที่ `http://localhost:5000` จะเห็นหน้า MLflow UI

---

## 🌳 Part 2: Train และ Deploy โมเดล Scikit-Learn

ในส่วนนี้เราจะสร้างโมเดล Random Forest สำหรับจำแนกดอกไม้ Iris แล้ว deploy เป็น API

### Step 2.1: ทำความเข้าใจ Iris Dataset

Iris Dataset ประกอบด้วย:
- **Features (4 ตัว):** ความยาว/ความกว้างของกลีบดอกและกลีบเลี้ยง
- **Target (3 classes):** Setosa, Versicolor, Virginica

### Step 2.2: สร้างไฟล์ Training

สร้างไฟล์ `train_sklearn.py` ด้วยคำสั่ง:

```bash
cat > train_sklearn.py << 'EOF'
"""
train_sklearn.py
================
ไฟล์นี้ทำหน้าที่:
1. โหลดข้อมูล Iris
2. Train โมเดล Random Forest
3. Log ผลลัพธ์ไปยัง MLflow
4. Register โมเดลเข้า Model Registry
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# ==========================================
# STEP 1: ตั้งค่า MLflow
# ==========================================
# บอก MLflow ว่า Server อยู่ที่ไหน
mlflow.set_tracking_uri("http://localhost:5000")

# สร้าง/เลือก experiment
mlflow.set_experiment("sklearn-iris-classification")

def train_and_register_model():
    """
    ฟังก์ชันหลักสำหรับ train และ register โมเดล
    """
    
    # ==========================================
    # STEP 2: โหลดและเตรียมข้อมูล
    # ==========================================
    print("📂 กำลังโหลดข้อมูล Iris...")
    iris = load_iris()
    
    # แปลงเป็น DataFrame เพื่อให้จัดการง่าย
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = iris.target
    
    # แบ่งข้อมูล 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42  # กำหนดค่าคงที่เพื่อให้ผลลัพธ์ reproducible
    )
    
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Test samples: {len(X_test)}")
    
    # ==========================================
    # STEP 3: กำหนด Hyperparameters
    # ==========================================
    params = {
        "n_estimators": 100,      # จำนวนต้นไม้
        "max_depth": 5,           # ความลึกสูงสุด
        "min_samples_split": 2,   # จำนวน sample ขั้นต่ำในการ split
        "random_state": 42
    }
    
    # ==========================================
    # STEP 4: Train โมเดลพร้อม MLflow Tracking
    # ==========================================
    print("\n🚀 เริ่ม Training...")
    
    # เริ่ม MLflow run
    with mlflow.start_run(run_name="rf-iris-model") as run:
        
        # 4.1 Log parameters
        mlflow.log_params(params)
        print("   ✅ Logged parameters")
        
        # 4.2 Train โมเดล
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        print("   ✅ Model trained")
        
        # 4.3 Evaluate โมเดล
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # 4.4 Log metrics
        mlflow.log_metric("accuracy", accuracy)
        print(f"   ✅ Accuracy: {accuracy:.4f}")
        
        # 4.5 สร้าง input example (ตัวอย่างข้อมูล input)
        # MLflow จะใช้สิ่งนี้สร้าง model signature อัตโนมัติ
        input_example = X_train.head(5)
        
        # 4.6 Log และ Register โมเดล
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="iris-classifier",  # ชื่อใน Registry
            input_example=input_example
        )
        print("   ✅ Model logged and registered")
        
        # แสดงข้อมูลสรุป
        print("\n" + "="*50)
        print("📊 สรุปผลการ Training")
        print("="*50)
        print(f"   Run ID: {run.info.run_id}")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Model Name: iris-classifier")
        print(f"   MLflow UI: http://localhost:5000")
        
        return run.info.run_id

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    run_id = train_and_register_model()
EOF
```

### Step 2.3: รัน Training Script

```bash
# รัน training (ต้องอยู่ในโฟลเดอร์ ~/mlflow-deployment-lab)
python train_sklearn.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
📂 กำลังโหลดข้อมูล Iris...
   - Training samples: 120
   - Test samples: 30

🚀 เริ่ม Training...
   ✅ Logged parameters
   ✅ Model trained
   ✅ Accuracy: 1.0000
   ✅ Model logged and registered

==================================================
📊 สรุปผลการ Training
==================================================
   Run ID: abc123...
   Accuracy: 1.0000
   Model Name: iris-classifier
   MLflow UI: http://localhost:5000
```

**ตรวจสอบใน MLflow UI:**
1. เปิด http://localhost:5000
2. คลิกที่ experiment "sklearn-iris-classification"
3. จะเห็น run พร้อม parameters และ metrics
4. ไปที่ tab "Models" จะเห็น "iris-classifier" ที่ลงทะเบียนแล้ว

### Step 2.4: Deploy โมเดลเป็น REST API

เปิด **Terminal ใหม่** (Terminal 2) แล้วรันคำสั่ง:

```bash
mlflow models serve \
    -m "models:/iris-classifier/1" \
    --port 5001 \
    --no-conda
```

**อธิบายพารามิเตอร์:**
| Parameter | ความหมาย |
|-----------|----------|
| `-m "models:/iris-classifier/1"` | ใช้โมเดล iris-classifier version 1 |
| `--port 5001` | เปิด API ที่ port 5001 |
| `--no-conda` | ไม่ใช้ conda environment (ใช้ environment ปัจจุบัน) |

**รอจนเห็นข้อความ:** `Listening at: http://127.0.0.1:5001`

### Step 2.5: ทดสอบ API ด้วย curl

เปิด **Terminal ใหม่** (Terminal 3) แล้วทดสอบ:

```bash
curl -X POST http://localhost:5001/invocations \
    -H "Content-Type: application/json" \
    -d '{
        "dataframe_split": {
            "columns": ["sepal length (cm)", "sepal width (cm)", 
                       "petal length (cm)", "petal width (cm)"],
            "data": [
                [5.1, 3.5, 1.4, 0.2],
                [6.2, 2.9, 4.3, 1.3],
                [7.7, 3.0, 6.1, 2.3]
            ]
        }
    }'
```

**ผลลัพธ์ที่คาดหวัง:**
```json
{"predictions": [0, 1, 2]}
```

**แปลความหมาย:**
- `0` = Setosa (ตัวอย่างแรก)
- `1` = Versicolor (ตัวอย่างที่สอง)
- `2` = Virginica (ตัวอย่างที่สาม)

---

## 🔥 Part 3: Train และ Deploy โมเดล PyTorch

ในส่วนนี้เราจะสร้าง Neural Network สำหรับจำแนกตัวเลขลายมือ (Digits 0-9)

### Step 3.1: ทำความเข้าใจ Digits Dataset

- **Input:** ภาพตัวเลขขนาด 8x8 pixels = 64 features
- **Output:** ตัวเลข 0-9 (10 classes)

### Step 3.2: สร้างไฟล์ Training

สร้างไฟล์ `train_pytorch.py` ด้วยคำสั่ง:

```bash
cat > train_pytorch.py << 'EOF'
"""
train_pytorch.py
================
ไฟล์นี้ทำหน้าที่:
1. สร้าง Neural Network architecture
2. Train โมเดลด้วย PyTorch
3. Log ผลลัพธ์ทุก epoch ไปยัง MLflow
4. Register โมเดลเข้า Model Registry
"""

import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# ==========================================
# STEP 1: ตั้งค่า MLflow
# ==========================================
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("pytorch-digits-classification")


# ==========================================
# STEP 2: กำหนด Neural Network Architecture
# ==========================================
class DigitClassifier(nn.Module):
    """
    Neural Network สำหรับจำแนกตัวเลข
    
    โครงสร้าง:
    - Input Layer: 64 neurons (8x8 pixels)
    - Hidden Layer 1: 128 neurons + ReLU + Dropout
    - Hidden Layer 2: 64 neurons + ReLU + Dropout
    - Output Layer: 10 neurons (digits 0-9)
    """
    
    def __init__(self, input_size=64, hidden_size=128, num_classes=10):
        super(DigitClassifier, self).__init__()
        
        self.network = nn.Sequential(
            # Layer 1: Input -> Hidden
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),  # ป้องกัน overfitting
            
            # Layer 2: Hidden -> Hidden
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.3),
            
            # Layer 3: Hidden -> Output
            nn.Linear(hidden_size // 2, num_classes)
        )
    
    def forward(self, x):
        return self.network(x)


# ==========================================
# STEP 3: ฟังก์ชันเตรียมข้อมูล
# ==========================================
def prepare_data():
    """โหลดและเตรียมข้อมูล Digits Dataset"""
    
    print("📂 กำลังโหลดข้อมูล Digits...")
    digits = load_digits()
    X, y = digits.data, digits.target
    
    # Normalize ข้อมูลให้อยู่ในช่วงที่เหมาะสม
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # แปลงเป็น PyTorch Tensor
    X_train = torch.FloatTensor(X_train)
    X_test = torch.FloatTensor(X_test)
    y_train = torch.LongTensor(y_train)
    y_test = torch.LongTensor(y_test)
    
    # สร้าง DataLoader สำหรับ batch training
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Test samples: {len(X_test)}")
    
    return train_loader, test_loader, X_test, y_test


# ==========================================
# STEP 4: ฟังก์ชัน Training และ Evaluation
# ==========================================
def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train โมเดลหนึ่ง epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # สะสมสถิติ
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += y_batch.size(0)
        correct += predicted.eq(y_batch).sum().item()
    
    return total_loss / len(train_loader), correct / total


def evaluate(model, test_loader, criterion, device):
    """ประเมินผลโมเดลบน test set"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():  # ไม่ต้องคำนวณ gradient
        for X_batch, y_batch in test_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += y_batch.size(0)
            correct += predicted.eq(y_batch).sum().item()
    
    return total_loss / len(test_loader), correct / total


# ==========================================
# STEP 5: ฟังก์ชันหลัก
# ==========================================
def train_and_register_model():
    """Train และ Register โมเดล PyTorch"""
    
    # เลือก device (GPU ถ้ามี, ไม่งั้นใช้ CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Using device: {device}")
    
    # เตรียมข้อมูล
    train_loader, test_loader, X_test, y_test = prepare_data()
    
    # กำหนด hyperparameters
    params = {
        "input_size": 64,
        "hidden_size": 128,
        "num_classes": 10,
        "learning_rate": 0.001,
        "epochs": 50,
        "batch_size": 32
    }
    
    print("\n🚀 เริ่ม Training...")
    
    with mlflow.start_run(run_name="pytorch-digits-model") as run:
        
        # Log parameters
        mlflow.log_params(params)
        
        # สร้างโมเดล
        model = DigitClassifier(
            input_size=params["input_size"],
            hidden_size=params["hidden_size"],
            num_classes=params["num_classes"]
        ).to(device)
        
        # กำหนด loss function และ optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=params["learning_rate"])
        
        # Training loop
        best_accuracy = 0
        for epoch in range(params["epochs"]):
            train_loss, train_acc = train_epoch(
                model, train_loader, criterion, optimizer, device
            )
            test_loss, test_acc = evaluate(
                model, test_loader, criterion, device
            )
            
            # Log metrics ทุก epoch
            mlflow.log_metrics({
                "train_loss": train_loss,
                "train_accuracy": train_acc,
                "test_loss": test_loss,
                "test_accuracy": test_acc
            }, step=epoch)
            
            # แสดงผลทุก 10 epochs
            if (epoch + 1) % 10 == 0:
                print(f"   Epoch {epoch+1:3d}/{params['epochs']}: "
                      f"Train Acc={train_acc:.4f}, Test Acc={test_acc:.4f}")
            
            # เก็บ best accuracy
            if test_acc > best_accuracy:
                best_accuracy = test_acc
        
        # Log final metrics
        mlflow.log_metric("best_accuracy", best_accuracy)
        
        # สร้าง input example
        input_example = X_test[:5].numpy()
        
        # Log และ Register โมเดล
        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path="model",
            registered_model_name="digits-classifier-pytorch",
            input_example=input_example
        )
        
        # แสดงข้อมูลสรุป
        print("\n" + "="*50)
        print("📊 สรุปผลการ Training")
        print("="*50)
        print(f"   Run ID: {run.info.run_id}")
        print(f"   Best Accuracy: {best_accuracy:.4f}")
        print(f"   Model Name: digits-classifier-pytorch")
        print(f"   MLflow UI: http://localhost:5000")
        
        return run.info.run_id


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    run_id = train_and_register_model()
EOF
```

### Step 3.3: รัน Training Script

```bash
python train_pytorch.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
🖥️  Using device: cpu
📂 กำลังโหลดข้อมูล Digits...
   - Training samples: 1437
   - Test samples: 360

🚀 เริ่ม Training...
   Epoch  10/50: Train Acc=0.9721, Test Acc=0.9556
   Epoch  20/50: Train Acc=0.9930, Test Acc=0.9722
   Epoch  30/50: Train Acc=0.9965, Test Acc=0.9750
   Epoch  40/50: Train Acc=0.9979, Test Acc=0.9778
   Epoch  50/50: Train Acc=0.9986, Test Acc=0.9778

==================================================
📊 สรุปผลการ Training
==================================================
   Run ID: xyz789...
   Best Accuracy: 0.9778
   Model Name: digits-classifier-pytorch
   MLflow UI: http://localhost:5000
```

### Step 3.4: Deploy โมเดล PyTorch

เปิด **Terminal ใหม่** (Terminal 4) แล้วรัน:

```bash
mlflow models serve \
    -m "models:/digits-classifier-pytorch/1" \
    --port 5002 \
    --no-conda
```

### Step 3.5: ทดสอบ API

```bash
# ส่งข้อมูลภาพตัวเลข (64 features)
curl -X POST http://localhost:5002/invocations \
    -H "Content-Type: application/json" \
    -d '{
        "inputs": [[0.0, 0.0, 5.0, 13.0, 9.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 13.0, 15.0, 10.0, 15.0, 5.0, 0.0,
                    0.0, 3.0, 15.0, 2.0, 0.0, 11.0, 8.0, 0.0,
                    0.0, 4.0, 12.0, 0.0, 0.0, 8.0, 8.0, 0.0,
                    0.0, 5.0, 8.0, 0.0, 0.0, 9.0, 8.0, 0.0,
                    0.0, 4.0, 11.0, 0.0, 1.0, 12.0, 7.0, 0.0,
                    0.0, 2.0, 14.0, 5.0, 10.0, 12.0, 0.0, 0.0,
                    0.0, 0.0, 6.0, 13.0, 10.0, 0.0, 0.0, 0.0]]
    }'
```

---

## 🐍 Part 4: สร้าง Python Client

แทนที่จะใช้ curl ทุกครั้ง เราสามารถสร้าง Python script สำหรับเรียกใช้ API

### Step 4.1: สร้างไฟล์ Client

สร้างไฟล์ `predict_client.py` ด้วยคำสั่ง:

```bash
cat > predict_client.py << 'EOF'
"""
predict_client.py
=================
Client สำหรับเรียกใช้ Deployed Models ผ่าน HTTP API

การใช้งาน:
    python predict_client.py
"""

import requests
import json
import numpy as np
from sklearn.datasets import load_iris, load_digits


def predict_sklearn(data, port=5001):
    """
    เรียก Prediction จาก Sklearn Model
    
    Args:
        data: list ของ samples [[f1, f2, f3, f4], ...]
        port: port ของ API server
    
    Returns:
        dict: ผลลัพธ์จาก API
    """
    url = f"http://localhost:{port}/invocations"
    
    # สร้าง payload ในรูปแบบ dataframe_split
    payload = {
        "dataframe_split": {
            "columns": [
                "sepal length (cm)", 
                "sepal width (cm)", 
                "petal length (cm)", 
                "petal width (cm)"
            ],
            "data": data
        }
    }
    
    # ส่ง POST request
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def predict_pytorch(data, port=5002):
    """
    เรียก Prediction จาก PyTorch Model
    
    Args:
        data: list ของ samples [[f1, f2, ..., f64], ...]
        port: port ของ API server
    
    Returns:
        dict: ผลลัพธ์จาก API
    """
    url = f"http://localhost:{port}/invocations"
    
    # PyTorch model ใช้รูปแบบ inputs
    payload = {"inputs": data}
    
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def demo_sklearn():
    """Demo การเรียกใช้ Sklearn Model"""
    
    print("="*60)
    print("🌸 Demo: Sklearn Iris Classification")
    print("="*60)
    
    # เตรียมข้อมูลทดสอบ
    test_samples = [
        [5.1, 3.5, 1.4, 0.2],  # คาดว่าเป็น Setosa
        [6.2, 2.9, 4.3, 1.3],  # คาดว่าเป็น Versicolor
        [7.7, 3.0, 6.1, 2.3],  # คาดว่าเป็น Virginica
    ]
    
    # ชื่อ class
    iris = load_iris()
    class_names = iris.target_names
    
    try:
        # เรียก API
        result = predict_sklearn(test_samples)
        predictions = result['predictions']
        
        # แสดงผล
        print("\n📊 ผลการทำนาย:\n")
        for i, (sample, pred) in enumerate(zip(test_samples, predictions)):
            print(f"   Sample {i+1}: {sample}")
            print(f"   ➜ Predicted: {pred} ({class_names[pred]})")
            print()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   ตรวจสอบว่า model server กำลังทำงานที่ port 5001")


def demo_pytorch():
    """Demo การเรียกใช้ PyTorch Model"""
    
    print("="*60)
    print("🔢 Demo: PyTorch Digits Classification")
    print("="*60)
    
    # โหลดข้อมูลจริง
    digits = load_digits()
    
    # เลือก 3 ตัวอย่าง
    indices = [0, 100, 200]
    test_samples = digits.data[indices].tolist()
    true_labels = digits.target[indices]
    
    try:
        # เรียก API
        result = predict_pytorch(test_samples)
        preds = result.get('predictions', result)
        
        # แสดงผล
        print("\n📊 ผลการทำนาย:\n")
        for i, (idx, true_label) in enumerate(zip(indices, true_labels)):
            pred = preds[i]
            
            # ถ้าได้ logits ให้หา argmax
            if isinstance(pred, list):
                pred_class = np.argmax(pred)
            else:
                pred_class = pred
            
            is_correct = pred_class == true_label
            
            print(f"   Sample {i+1} (index {idx}):")
            print(f"   ➜ True label: {true_label}")
            print(f"   ➜ Predicted:  {pred_class}")
            print(f"   ➜ Status: {'✅ ถูกต้อง' if is_correct else '❌ ผิด'}")
            print()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   ตรวจสอบว่า model server กำลังทำงานที่ port 5002")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("\n" + "🚀"*30)
    print("\n   MLflow Model Deployment - Prediction Demo\n")
    print("🚀"*30 + "\n")
    
    # ทดสอบ Sklearn Model
    demo_sklearn()
    
    print("\n")
    
    # ทดสอบ PyTorch Model
    demo_pytorch()
EOF
```

### Step 4.2: รัน Client

```bash
python predict_client.py
```

**ผลลัพธ์ที่คาดหวัง:**
```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

   MLflow Model Deployment - Prediction Demo

🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

============================================================
🌸 Demo: Sklearn Iris Classification
============================================================

📊 ผลการทำนาย:

   Sample 1: [5.1, 3.5, 1.4, 0.2]
   ➜ Predicted: 0 (setosa)

   Sample 2: [6.2, 2.9, 4.3, 1.3]
   ➜ Predicted: 1 (versicolor)

   Sample 3: [7.7, 3.0, 6.1, 2.3]
   ➜ Predicted: 2 (virginica)


============================================================
🔢 Demo: PyTorch Digits Classification
============================================================

📊 ผลการทำนาย:

   Sample 1 (index 0):
   ➜ True label: 0
   ➜ Predicted:  0
   ➜ Status: ✅ ถูกต้อง

   Sample 2 (index 100):
   ➜ True label: 4
   ➜ Predicted:  4
   ➜ Status: ✅ ถูกต้อง

   Sample 3 (index 200):
   ➜ True label: 3
   ➜ Predicted:  3
   ➜ Status: ✅ ถูกต้อง
```

---

## 🔄 Part 5: Model Stage Management

MLflow มีระบบ Stage สำหรับจัดการ lifecycle ของโมเดล

### Stage ที่มีใน MLflow

| Stage | ความหมาย | การใช้งาน |
|-------|----------|----------|
| `None` | ยังไม่กำหนด | โมเดลที่เพิ่ง register |
| `Staging` | กำลังทดสอบ | โมเดลที่กำลัง QA/testing |
| `Production` | ใช้งานจริง | โมเดลที่ deploy ให้ users |
| `Archived` | เก็บถาวร | โมเดลเก่าที่ไม่ใช้แล้ว |

### Step 5.1: สร้างไฟล์จัดการ Stage

สร้างไฟล์ `model_management.py` ด้วยคำสั่ง:

```bash
cat > model_management.py << 'EOF'
"""
model_management.py
===================
จัดการ Model Versions และ Stage Transitions
"""

from mlflow import MlflowClient

# สร้าง client เชื่อมต่อกับ MLflow Server
client = MlflowClient("http://localhost:5000")


def list_model_versions(model_name):
    """
    แสดง versions ทั้งหมดของโมเดล
    
    Args:
        model_name: ชื่อโมเดลใน Registry
    """
    print(f"\n📦 Model: {model_name}")
    print("-" * 50)
    
    versions = client.search_model_versions(f"name='{model_name}'")
    
    if not versions:
        print("   ไม่พบ version ใดๆ")
        return []
    
    for v in versions:
        print(f"   Version {v.version}:")
        print(f"      - Stage: {v.current_stage}")
        print(f"      - Status: {v.status}")
        print(f"      - Run ID: {v.run_id[:8]}...")
    
    return versions


def transition_stage(model_name, version, new_stage):
    """
    เปลี่ยน stage ของโมเดล
    
    Args:
        model_name: ชื่อโมเดล
        version: version ที่ต้องการเปลี่ยน
        new_stage: stage ใหม่ (None, Staging, Production, Archived)
    """
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=new_stage
    )
    print(f"✅ Transitioned {model_name} v{version} → {new_stage}")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔄 Model Stage Management")
    print("="*60)
    
    # แสดง versions ของ sklearn model
    list_model_versions("iris-classifier")
    
    # เปลี่ยนเป็น Production
    transition_stage("iris-classifier", "1", "Production")
    
    print()
    
    # แสดง versions ของ pytorch model
    list_model_versions("digits-classifier-pytorch")
    
    # เปลี่ยนเป็น Staging
    transition_stage("digits-classifier-pytorch", "1", "Staging")
EOF
```

### Step 5.2: รันและทดสอบ

```bash
python model_management.py
```

### Step 5.3: Deploy โมเดลจาก Production Stage

หลังจากเปลี่ยน stage เป็น Production แล้ว สามารถ deploy โดยอ้างอิง stage ได้:

```bash
# หยุด server เดิมก่อน (Ctrl+C ที่ Terminal 2)

# Deploy ใหม่จาก Production stage
mlflow models serve \
    -m "models:/iris-classifier/Production" \
    --port 5001 \
    --no-conda
```

**ข้อดี:** เมื่อมี version ใหม่ที่ดีกว่า แค่เปลี่ยน stage ของ version ใหม่เป็น Production แล้ว restart server ก็จะได้โมเดลใหม่

---

## 📊 สรุป

### คำสั่งสำคัญที่ใช้ใน Lab

| งาน | คำสั่ง/วิธีการ |
|-----|---------------|
| Log Sklearn Model | `mlflow.sklearn.log_model(model, "model")` |
| Log PyTorch Model | `mlflow.pytorch.log_model(model, "model")` |
| Register Model | เพิ่ม `registered_model_name="..."` |
| Serve Model | `mlflow models serve -m "models:/name/version" --port XXXX` |
| เปลี่ยน Stage | `client.transition_model_version_stage()` |

### Flow การทำงานจริง

```
1. Data Scientist Train โมเดล
        ↓
2. Log โมเดลไปยัง MLflow
        ↓
3. Register ใน Model Registry
        ↓
4. QA ทดสอบ (Stage: Staging)
        ↓
5. Approve แล้วเปลี่ยนเป็น Production
        ↓
6. Deploy ด้วย mlflow models serve
        ↓
7. Applications เรียกใช้ผ่าน REST API
```

---

## 📚 แหล่งข้อมูลเพิ่มเติม

- [MLflow Models Documentation](https://mlflow.org/docs/latest/models.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow REST API Reference](https://mlflow.org/docs/latest/rest-api.html)
- [Deploying MLflow Models](https://mlflow.org/docs/latest/deployment/index.html)

---

## ❓ FAQ

**Q: ทำไม curl ไม่ทำงาน?**

A: ตรวจสอบว่า:
1. Model server กำลังทำงานอยู่ (`ps aux | grep mlflow`)
2. Port ถูกต้อง
3. Format ของ JSON ถูกต้อง

**Q: จะหยุด model server ยังไง?**

A: กด `Ctrl+C` ที่ Terminal ที่รัน server หรือใช้ `kill` กับ process ID

**Q: ความแตกต่างระหว่าง dataframe_split กับ inputs?**

A: 
- `dataframe_split`: ใช้กับ sklearn models (มี column names)
- `inputs`: ใช้กับ pytorch models (เป็น array ธรรมดา)