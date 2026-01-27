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

---

## 📚 ข้อที่ 1: Wine Quality Classification Model Registry

### 🎯 วัตถุประสงค์
ฝึกการใช้ MLflow Model Registry กับข้อมูล Wine Quality โดยการ train หลาย models, ลงทะเบียนเข้า Registry, จัดการ versions และ aliases

### 📖 โจทย์

นักศึกษาต้องสร้างระบบจำแนกคุณภาพไวน์ (Wine Quality Classification) โดยใช้ MLflow Model Registry เพื่อจัดการโมเดลหลายเวอร์ชัน

**งานที่ต้องทำ:**

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

### 🔧 Code เริ่มต้น

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

---

## 📚 ข้อที่ 2: PyTorch MNIST Digit Classifier with Model Registry

### 🎯 วัตถุประสงค์
ฝึกการใช้ MLflow Model Registry กับ PyTorch Neural Network โดยการ train โมเดลจำแนกตัวเลข MNIST หลายเวอร์ชัน และจัดการผ่าน Registry

### 📖 โจทย์

นักศึกษาต้องสร้างระบบจำแนกตัวเลขลายมือเขียน (MNIST Digit Classification) ด้วย PyTorch และใช้ MLflow Model Registry จัดการโมเดล

**งานที่ต้องทำ:**

1. **สร้าง Neural Network Architecture**
   - สร้าง class `DigitClassifier` ที่สืบทอดจาก `nn.Module`
   - รับ parameter `hidden_size` เพื่อกำหนดขนาด hidden layer
   - Input: 64 features (8x8 image flattened)
   - Output: 10 classes (digits 0-9)

2. **Train Model 2 Versions**
   - Version 1: `hidden_size=32`, `epochs=50` (baseline)
   - Version 2: `hidden_size=64`, `epochs=100` (improved)
   - บันทึก parameters, metrics (accuracy, loss)
   - บันทึก training loss ทุก 10 epochs

3. **ลงทะเบียนและจัดการ Models**
   - ใช้ชื่อ Registered Model: `mnist-digit-classifier`
   - เพิ่ม Description และ Tags ที่เหมาะสม
   - กำหนด `baseline` alias ให้ Version 1
   - กำหนด `champion` alias ให้ Version ที่มี accuracy สูงกว่า

4. **โหลดและเปรียบเทียบ Models**
   - โหลดทั้ง baseline และ champion models
   - เปรียบเทียบ accuracy ของทั้ง 2 versions
   - แสดงผล predictions ของ champion model กับข้อมูล 5 ตัวอย่าง

### 🔧 Code เริ่มต้น

```python
# === การบ้านข้อที่ 2: PyTorch MNIST Digit Classifier ===
# ชื่อ-นามสกุล: _______________
# รหัสนักศึกษา: _______________

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mlflow.models import infer_signature
import torch
import torch.nn as nn
import numpy as np

# === Setup ===
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# === โหลดข้อมูล MNIST Digits (8x8) ===
digits = load_digits()
X = digits.data.astype('float32')  # (1797, 64)
y = digits.target  # 0-9

# Normalize
X = X / 16.0  # Max value is 16

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ โหลดข้อมูล MNIST Digits สำเร็จ")
print(f"📊 Training samples: {len(X_train)}")
print(f"📊 Test samples: {len(X_test)}")
print(f"📊 Input shape: {X_train.shape[1]} features (8x8 image flattened)")
print(f"📊 Classes: 0-9 (10 digits)")

# === กำหนดชื่อ Registered Model ===
MODEL_NAME = "mnist-digit-classifier"

# === สร้าง Experiment ===
mlflow.set_experiment("mnist-digit-homework")

# TODO: เขียน code ต่อจากนี้
# 1. สร้าง class DigitClassifier(nn.Module)
# 2. Train และลงทะเบียน Model Version 1 (hidden_size=32)
# 3. Train และลงทะเบียน Model Version 2 (hidden_size=64)
# 4. เพิ่ม Description, Tags และ Aliases
# 5. โหลดและเปรียบเทียบ Models

# === ตัวอย่าง Neural Network Structure ===
class DigitClassifier(nn.Module):
    def __init__(self, input_size=64, hidden_size=32, num_classes=10):
        super(DigitClassifier, self).__init__()
        # TODO: กำหนด layers
        # Hint: ใช้ nn.Linear, nn.ReLU
        # self.fc1 = nn.Linear(input_size, hidden_size)
        # self.relu = nn.ReLU()
        # self.fc2 = nn.Linear(hidden_size, num_classes)
        pass
    
    def forward(self, x):
        # TODO: กำหนด forward pass
        # out = self.fc1(x)
        # out = self.relu(out)
        # out = self.fc2(out)
        # return out
        pass

# === ตัวอย่างการสร้าง Model และ Train ===
# model_v1 = DigitClassifier(hidden_size=16)  # TODO: แก้ hidden_size ให้ตรงตามโจทย์
# loss_history = train_pytorch_model(model_v1, X_train, y_train, epochs=30, learning_rate=0.01)  # TODO: แก้ epochs ให้ตรงตามโจทย์

# === Helper Function สำหรับ Training ===
def train_pytorch_model(model, X_train, y_train, epochs=50, learning_rate=0.01):
    """
    Train PyTorch model และ return loss history
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    X_tensor = torch.FloatTensor(X_train)
    y_tensor = torch.LongTensor(y_train)
    
    loss_history = []
    
    for epoch in range(epochs):
        # Forward pass
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # บันทึก loss ทุก 10 epochs
        if (epoch + 1) % 10 == 0:
            loss_history.append((epoch + 1, loss.item()))
            print(f"   Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
    
    return loss_history

# === Helper Function สำหรับ Evaluation ===
def evaluate_pytorch_model(model, X_test, y_test):
    """
    Evaluate PyTorch model และ return accuracy
    """
    model.eval()
    with torch.no_grad():
        X_tensor = torch.FloatTensor(X_test)
        outputs = model(X_tensor)
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted.numpy() == y_test).sum() / len(y_test)
    return accuracy, predicted.numpy()

```

---

## 💡 คำแนะนำเพิ่มเติม

### การ Log Model พร้อมลงทะเบียน
```python
mlflow.sklearn.log_model(
    sk_model=model,
    artifact_path="model",
    signature=signature,
    registered_model_name="model-name"  # ระบุชื่อเพื่อลงทะเบียนอัตโนมัติ
)
```

### การเพิ่ม Description และ Tags
```python
client.update_registered_model(name="model-name", description="...")
client.set_registered_model_tag("model-name", "key", "value")
client.update_model_version(name="model-name", version="1", description="...")
client.set_model_version_tag("model-name", "1", "key", "value")
```

### การกำหนด Aliases
```python
client.set_registered_model_alias(name="model-name", alias="champion", version="1")
```

### การโหลด Model จาก Alias
```python
model = mlflow.sklearn.load_model(f"models:/model-name@champion")
# หรือ
model = mlflow.pytorch.load_model(f"models:/model-name@champion")
```



---

**🔗 MLflow Server URL:** http://127.0.0.1:5000

**ขอให้โชคดีในการทำการบ้าน! 🎓**