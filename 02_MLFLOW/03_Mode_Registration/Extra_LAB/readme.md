# 📝 การบ้าน: MLflow Model Registry

**วิชา:** Machine Learning Operations (MLOps)  
**หัวข้อ:** MLflow Model Registry

---

## 📋 คำแนะนำทั่วไป

1. ทำการบ้านใน Jupyter Notebook หรือ Python script
2. MLflow Server ต้องรันอยู่ที่ `http://127.0.0.1:5000`
3. ใส่ชื่อ-นามสกุล และรหัสนักศึกษาในไฟล์ที่ส่ง

### 📤 สิ่งที่ต้องส่งให้ TA ตรวจสอบ
- ไฟล์ code (.ipynb หรือ .py) พร้อมผลลัพธ์การรัน
- Screenshot หน้า MLflow UI แสดง Registered Model และ Versions
- ตารางเปรียบเทียบ accuracy ของแต่ละ Model Version
- ตารางสรุปสำหรับแต่ละข้อ

---

# 📚 ข้อที่ 1: Wine Quality Classification Model Registry

## 🎯 วัตถุประสงค์
ฝึกการใช้ MLflow Model Registry กับข้อมูล Wine Quality โดยการ train หลาย models, ลงทะเบียนเข้า Registry, จัดการ versions และ aliases

## 📖 โจทย์

นักศึกษาต้องสร้างระบบจำแนกคุณภาพไวน์ (Wine Quality Classification) โดยใช้ MLflow Model Registry เพื่อจัดการโมเดลหลายเวอร์ชัน

### งานที่ต้องทำ:

1. **Train Model 3 Versions**
   - Version 1: `DecisionTreeClassifier` (baseline)
   - Version 2: `RandomForestClassifier` (n_estimators=100)
   - Version 3: `GradientBoostingClassifier` (n_estimators=100)
   
2. **ลงทะเบียน Models เข้า Registry**
   - ใช้ชื่อ Registered Model: `wine-quality-classifier`
   - เพิ่ม Description ที่อธิบายโมเดลอย่างชัดเจน
   - เพิ่ม Tags สำหรับ Registered Model: `task`, `dataset`, `team`
   - เพิ่ม Tags สำหรับแต่ละ Version: `model_type`, `status`

3. **จัดการ Aliases**
   - กำหนด `baseline` alias ให้ Version 1
   - กำหนด `staging` alias ให้ Version ที่มี accuracy สูงเป็นอันดับ 2
   - กำหนด `champion` alias ให้ Version ที่มี accuracy สูงที่สุด

4. **โหลดและทดสอบ Models**
   - โหลด champion model จาก Registry
   - ทดสอบทำนายกับข้อมูล test set 10 ตัวอย่าง
   - แสดงผล predictions และ actual values

### 🔧 Code เริ่มต้น - ข้อที่ 1

```python
# === การบ้านข้อที่ 1: Wine Quality Classification ===
# ชื่อ-นามสกุล: _______________
# รหัสนักศึกษา: _______________

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.models import infer_signature
import numpy as np

# === Setup ===
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# === โหลดข้อมูล Wine Quality ===
wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

print(f"✅ โหลดข้อมูล Wine Quality สำเร็จ")
print(f"📊 Training samples: {len(X_train)}")
print(f"📊 Test samples: {len(X_test)}")
print(f"📊 Features: {wine.feature_names}")
print(f"📊 Classes: {wine.target_names}")

# === กำหนดชื่อ Registered Model ===
MODEL_NAME = "wine-quality-classifier"

# === สร้าง Experiment ===
mlflow.set_experiment("wine-quality-homework")

# TODO: เขียน code ต่อจากนี้
# 1. Train และลงทะเบียน Model Version 1 (DecisionTree)
# 2. Train และลงทะเบียน Model Version 2 (RandomForest)
# 3. Train และลงทะเบียน Model Version 3 (GradientBoosting)
# 4. เพิ่ม Description และ Tags
# 5. กำหนด Aliases
# 6. โหลดและทดสอบ Champion Model

```

### 📋 Expected Output - ข้อที่ 1

```
ตารางเปรียบเทียบ Wine Quality Models:

| Version | Algorithm | Accuracy | F1-Score |
|---------|-----------|----------|----------|
| 1 | DecisionTree | XX% | XX |
| 2 | RandomForest | XX% | XX |
| 3 | GradientBoosting | XX% | XX |

Champion Model: Version 3 (GradientBoosting)
Alias Assignment:
- baseline → Version 1
- staging → Version 2
- champion → Version 3
```

---

# 📚 ข้อที่ 2: MNIST Digit Classification with PyTorch Neural Networks

## 🎯 วัตถุประสงค์
ฝึกการใช้ MLflow Model Registry กับ PyTorch Deep Learning models โดยการ train neural networks หลายสถาปัตยกรรม, ลงทะเบียนเข้า Registry, จัดการ versions และ aliases

## 📖 โจทย์

นักศึกษาต้องสร้างระบบจำแนกตัวเลข MNIST (Digit Classification) โดยใช้ PyTorch Neural Networks แล้วลงทะเบียนเข้า MLflow Model Registry

### งานที่ต้องทำ:

#### 1️⃣ **Prepare Data**
   - โหลด MNIST dataset (จำนวนตัวเลข 0-9)
   - แบ่ง data เป็น training set (70%) และ test set (30%)
   - Normalize images ให้เป็น range [0, 1]
   - บันทึกข้อมูลพื้นฐาน: จำนวน samples, image shape, จำนวน classes

#### 2️⃣ **Define Neural Network Architectures**
   
   สร้างโครงสร้าง Neural Network 3 แบบ:
   
   ```
   Version 1: Shallow Neural Network (Baseline)
   ├── Input: 28×28 = 784 pixels
   ├── Hidden Layer 1: 128 neurons + ReLU
   ├── Output Layer: 10 neurons (for 10 digits)
   └── Parameters: ~100K
   
   Version 2: Medium Deep Network (Improved)
   ├── Input: 28×28 = 784 pixels
   ├── Hidden Layer 1: 256 neurons + ReLU
   ├── Hidden Layer 2: 128 neurons + ReLU
   ├── Output Layer: 10 neurons
   └── Parameters: ~130K
   
   Version 3: Deeper Network with Dropout (Champion)
   ├── Input: 28×28 = 784 pixels
   ├── Hidden Layer 1: 512 neurons + ReLU + Dropout(0.2)
   ├── Hidden Layer 2: 256 neurons + ReLU + Dropout(0.2)
   ├── Hidden Layer 3: 128 neurons + ReLU + Dropout(0.1)
   ├── Output Layer: 10 neurons
   └── Parameters: ~300K
   ```

#### 3️⃣ **Train Models 3 Versions**
   
   ต้องฝึก Neural Networks 3 เวอร์ชัน:
   
   | Version | Architecture | Epochs | Learning Rate | Batch Size | Expected Accuracy |
   |---------|--------------|--------|---------------|------------|------------------|
   | **V1** | Shallow NN | 50 | 0.001 | 64 | ~95% |
   | **V2** | Medium Deep | 100 | 0.001 | 32 | ~97% |
   | **V3** | Deep + Dropout | 150 | 0.0005 | 32 | ~98% |
   
   **Hyperparameters ที่ต้องบันทึก:**
   - hidden_size_1, hidden_size_2, hidden_size_3
   - dropout_rate
   - learning_rate
   - batch_size
   - num_epochs
   - optimizer type
   - loss function

#### 4️⃣ **ลงทะเบียน Models เข้า Registry**
   - ใช้ชื่อ Registered Model: `mnist-digit-classifier`
   - เพิ่ม Description ที่อธิบาย architecture
   - เพิ่ม Tags สำหรับ Registered Model:
     - `task`: classification
     - `dataset`: mnist
     - `framework`: pytorch
     - `team`: your-team-name
   
   - เพิ่ม Tags สำหรับแต่ละ Version:
     - `model_type`: architecture name (e.g., "shallow-nn", "medium-deep-nn")
     - `status`: baseline / improved / champion
     - `num_parameters`: total parameters
     - `training_time_seconds`: เวลาในการฝึก

#### 5️⃣ **บันทึก Training Metrics**
   
   บันทึกสำหรับแต่ละ epoch:
   - `train_loss`: Loss บน training set
   - `train_accuracy`: Accuracy บน training set
   - `test_loss`: Loss บน test set (optional, ทุก 5 epochs)
   - `test_accuracy`: Accuracy บน test set (optional, ทุก 5 epochs)
   
   บันทึกทั้งหมดเมื่อจบการฝึก:
   - `final_test_accuracy`: Accuracy สุดท้าย
   - `final_test_loss`: Loss สุดท้าย
   - `model_size_mb`: ขนาดไฟล์ model

#### 6️⃣ **จัดการ Aliases**
   - กำหนด `baseline` alias ให้ Version 1
   - กำหนด `staging` alias ให้ Version ที่มี accuracy สูงเป็นอันดับ 2
   - กำหนด `champion` alias ให้ Version ที่มี accuracy สูงที่สุด

#### 7️⃣ **โหลดและทดสอบ Models**
   - โหลด champion model จาก Registry โดยใช้ Alias
   - ทดสอบทำนายกับข้อมูล test set 20 ตัวอย่าง
   - แสดงผล predictions, actual values, และ confidence scores
   - คำนวณ accuracy บน test set

#### 8️⃣ **เปรียบเทียบ Models**
   
   สร้างตารางเปรียบเทียบ:
   
   ```
   | Metric | Version 1 | Version 2 | Version 3 |
   |--------|-----------|-----------|-----------|
   | Accuracy | | | |
   | Loss | | | |
   | Parameters | | | |
   | Training Time | | | |
   | Model Size | | | |
   ```

### 🔧 Code เริ่มต้น - ข้อที่ 2

```python
# === การบ้านข้อที่ 2: MNIST Digit Classification with PyTorch ===
# ชื่อ-นามสกุล: _______________
# รหัสนักศึกษา: _______________

import mlflow
from mlflow.tracking import MlflowClient
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, f1_score
from mlflow.models import infer_signature
import time
import numpy as np

# === Setup ===
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# === Data Preparation ===
# โหลด MNIST dataset
print("📥 โหลด MNIST Dataset...")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean and std
])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# สร้าง DataLoaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

print(f"✅ โหลดข้อมูล MNIST สำเร็จ")
print(f"📊 Training samples: {len(train_dataset)}")
print(f"📊 Test samples: {len(test_dataset)}")
print(f"📊 Input shape: (1, 28, 28)")
print(f"📊 Number of classes: 10 (digits 0-9)")

# === กำหนดชื่อ Registered Model ===
MODEL_NAME = "mnist-digit-classifier"

# === สร้าง Experiment ===
mlflow.set_experiment("mnist-pytorch-homework")

# === Define Neural Network Classes ===

class ShallowNN(nn.Module):
    """Version 1: Shallow Neural Network (Baseline)"""
    def __init__(self, input_size=784, hidden_size=128, num_classes=10):
        super(ShallowNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


class MediumDeepNN(nn.Module):
    """Version 2: Medium Deep Neural Network (Improved)"""
    def __init__(self, input_size=784, hidden_size1=256, hidden_size2=128, num_classes=10):
        super(MediumDeepNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.fc3 = nn.Linear(hidden_size2, num_classes)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out


class DeepNNWithDropout(nn.Module):
    """Version 3: Deep Neural Network with Dropout (Champion)"""
    def __init__(self, input_size=784, hidden_size1=512, hidden_size2=256, 
                 hidden_size3=128, dropout_rate=0.2, num_classes=10):
        super(DeepNNWithDropout, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout_rate)
        
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.dropout2 = nn.Dropout(dropout_rate)
        
        self.fc3 = nn.Linear(hidden_size2, hidden_size3)
        self.dropout3 = nn.Dropout(dropout_rate * 0.5)
        
        self.fc4 = nn.Linear(hidden_size3, num_classes)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout1(out)
        
        out = self.fc2(out)
        out = self.relu(out)
        out = self.dropout2(out)
        
        out = self.fc3(out)
        out = self.relu(out)
        out = self.dropout3(out)
        
        out = self.fc4(out)
        return out


# === Helper Functions ===

def count_parameters(model):
    """นับจำนวน parameters ทั้งหมดของ model"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def train_epoch(model, train_loader, criterion, optimizer, device):
    """ฝึก model 1 epoch"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Statistics
        total_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    avg_loss = total_loss / len(train_loader)
    accuracy = 100 * correct / total
    
    return avg_loss, accuracy


def evaluate(model, test_loader, criterion, device):
    """ประเมินผล model บน test set"""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    avg_loss = total_loss / len(test_loader)
    accuracy = 100 * correct / total
    
    return avg_loss, accuracy


def get_sample_input(train_loader, device):
    """ดึง batch แรกจาก train set สำหรับ signature"""
    for images, labels in train_loader:
        return images[:5].to(device)


# === Device Configuration ===
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\n🖥️  ใช้ Device: {device}")

# TODO: เขียน code ต่อจากนี้
# 1. Train และลงทะเบียน Model Version 1 (ShallowNN)
# 2. Train และลงทะเบียน Model Version 2 (MediumDeepNN)
# 3. Train และลงทะเบียน Model Version 3 (DeepNNWithDropout)
# 4. เพิ่ม Description และ Tags
# 5. เปรียบเทียบผล accuracy ของ 3 versions
# 6. กำหนด Aliases (baseline, staging, champion)
# 7. โหลดและทดสอบ Champion Model
# 8. ทำการทำนายบน 20 ตัวอย่างจาก test set

# ===== Hints =====
# - ใช้ `mlflow.pytorch.log_model()` สำหรับลงทะเบียน PyTorch models
# - บันทึก training metrics ด้วย `mlflow.log_metric()`
# - ใช้ `mlflow.log_param()` สำหรับ hyperparameters
# - เลือก champion model โดยดู accuracy สูงสุด
# - ใช้ `mlflow.pytorch.load_model()` สำหรับโหลด model จาก Registry

```

### 📋 Expected Output - ข้อที่ 2

```
ตารางเปรียบเทียบ MNIST PyTorch Models:

| Version | Architecture | Accuracy | Loss | Parameters | Training Time |
|---------|--------------|----------|------|------------|---------------|
| 1 | Shallow NN | 95-96% | XX | ~100K | XX sec |
| 2 | Medium Deep | 97-98% | XX | ~130K | XX sec |
| 3 | Deep + Dropout | 98-99% | XX | ~300K | XX sec |

Champion Model: Version 3 (Deep NN with Dropout)
Alias Assignment:
- baseline → Version 1
- staging → Version 2
- champion → Version 3

Sample Predictions (20 samples):
Predicted: [X, X, X, ...]
Actual:    [X, X, X, ...]
Confidence: [XX%, XX%, XX%, ...]
```

---

# 📋 Grading Rubric

## ข้อที่ 1: Wine Quality (Scikit-learn)

| Criteria | Points | Notes |
|----------|--------|-------|
| **Data Loading & Preparation** | 10 | โหลด wine dataset, split train/test |
| **Model 1 (DecisionTree)** | 10 | Train, log metrics, register model |
| **Model 2 (RandomForest)** | 10 | Train, log metrics, register model |
| **Model 3 (GradientBoosting)** | 10 | Train, log metrics, register model |
| **MLflow Registry Setup** | 10 | Description, Tags, Aliases |
| **Model Loading & Testing** | 10 | Load champion, predict, show results |
| **Code Quality** | 10 | Comments, structure, error handling |
| **Subtotal** | **70** | - |

## ข้อที่ 2: MNIST (PyTorch)

| Criteria | Points | Notes |
|----------|--------|-------|
| **Data Preparation** | 10 | โหลด MNIST, normalize, DataLoader |
| **Model 1 (Shallow NN)** | 10 | Train, log metrics, register model |
| **Model 2 (Medium Deep)** | 10 | Train, log metrics, register model |
| **Model 3 (Deep + Dropout)** | 10 | Train, log metrics, register model |
| **MLflow Registry Setup** | 10 | Description, Tags, Aliases |
| **Model Loading & Testing** | 10 | Load champion, predict, show results |
| **Code Quality** | 10 | Comments, structure, error handling |
| **Subtotal** | **70** | - |

## Overall Quality

| Criteria | Points | Notes |
|----------|--------|-------|
| **MLflow UI Screenshots** | 10 | Show registered models and versions |
| **Comparison Tables** | 10 | Clear presentation of results |
| **Code Organization** | 10 | Well-structured, easy to read |
| **Subtotal** | **30** | - |

## **TOTAL GRADE: 100 Points**

---

# 💡 Tips & Tricks

## สำหรับข้อที่ 1 (Wine Quality - Scikit-learn)

1. **Model Registration Pattern:**
   ```python
   with mlflow.start_run(run_name="wine-v1"):
       mlflow.log_params({...})
       model = DecisionTreeClassifier(...)
       model.fit(X_train, y_train)
       mlflow.log_metrics({...})
       signature = infer_signature(X_train, model.predict(X_train))
       mlflow.sklearn.log_model(
           model, 
           "model", 
           signature=signature,
           registered_model_name="wine-quality-classifier"
       )
   ```

2. **Tag Management:**
   ```python
   client.set_registered_model_tag(model_name, "task", "classification")
   client.set_model_version_tag(model_name, "1", "model_type", "DecisionTree")
   ```

3. **Alias Management:**
   ```python
   client.set_registered_model_alias(model_name, "champion", "3")
   champion = client.get_model_version_by_alias(model_name, "champion")
   ```

## สำหรับข้อที่ 2 (MNIST - PyTorch)

1. **Device Management:**
   ```python
   device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
   model = model.to(device)
   images = images.to(device)
   ```

2. **Model Signature for PyTorch:**
   ```python
   sample_input = get_sample_input(train_loader, device)
   signature = infer_signature(
       sample_input.cpu().numpy().reshape(5, -1),
       model(sample_input).detach().cpu().numpy()
   )
   ```

3. **Logging Metrics by Epoch:**
   ```python
   for epoch in range(num_epochs):
       train_loss, train_acc = train_epoch(...)
       test_loss, test_acc = evaluate(...)
       
       mlflow.log_metric("train_loss", train_loss, step=epoch)
       mlflow.log_metric("train_accuracy", train_acc, step=epoch)
       if epoch % 5 == 0:
           mlflow.log_metric("test_loss", test_loss, step=epoch)
           mlflow.log_metric("test_accuracy", test_acc, step=epoch)
   ```

4. **Viewing Results:**
   - Open browser: http://127.0.0.1:5000
   - ไปที่ "Models" tab เพื่อดู registered models
   - ไปที่ "Experiments" tab เพื่อดู runs และ metrics

---

# 🔗 ทรัพยากรที่เป็นประโยชน์

## Scikit-learn (ข้อที่ 1)
- [Scikit-learn Classification Models](https://scikit-learn.org/stable/supervised_learning.html)
- [Wine Dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html)

## PyTorch (ข้อที่ 2)
- [PyTorch Neural Networks](https://pytorch.org/docs/stable/nn.html)
- [PyTorch Loss Functions](https://pytorch.org/docs/stable/nn.html#loss-functions)
- [PyTorch Optimizers](https://pytorch.org/docs/stable/optim.html)
- [MNIST Dataset](https://pytorch.org/vision/stable/datasets.html#mnist)

## MLflow
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Scikit-learn Integration](https://mlflow.org/docs/latest/models.html#scikit-learn)
- [MLflow PyTorch Integration](https://mlflow.org/docs/latest/models.html#pytorch)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/mlflow.html)

---

# 📊 ตัวอย่างผลลัพธ์ที่คาดหวัง

## ข้อที่ 1 - Wine Quality Accuracy
- DecisionTree: ~90-92%
- RandomForest: ~95-97%
- GradientBoosting: ~97-99% ✓ (Champion)

## ข้อที่ 2 - MNIST Accuracy
- Shallow NN: ~95-96%
- Medium Deep: ~95-97%
- Deep + Dropout: ~97-99% ✓ (Champion)

---

# 📝 Submission Checklist

- [ ] ข้อที่ 1: code ที่ complete
- [ ] ข้อที่ 1: screenshot MLflow UI
- [ ] ข้อที่ 1: table comparing 3 models
- [ ] ข้อที่ 2: code ที่ complete
- [ ] ข้อที่ 2: screenshot MLflow UI
- [ ] ข้อที่ 2: table comparing 3 models
- [ ] ข้อที่ 2: sample predictions output
- [ ] สรุปผล (summary) สำหรับทั้ง 2 ข้อ
- [ ] ไฟล์ที่ส่งมีชื่อและรหัสนักศึกษา

---

**ขอให้โชคดีในการทำการบ้าน! 🎓**

**MLflow Server URL:** http://127.0.0.1:5000

---
