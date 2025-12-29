# %% [markdown]
# # 🧪 Lab: MLflow Tracking พื้นฐาน
#
# **วัตถุประสงค์การเรียนรู้:**
# - เข้าใจองค์ประกอบหลัก 5 ส่วนของ MLflow Tracking
# - สามารถสร้าง Experiment และ Run ได้
# - บันทึก Parameters, Metrics และ Artifacts ได้อย่างถูกต้อง
# - เปรียบเทียบผลการทดลองผ่าน MLflow UI
#
# **ข้อกำหนดเบื้องต้น:**
# - Python 3.8+
# - MLflow (`pip install mlflow`)
# - matplotlib (`pip install matplotlib`)
#
# **การเชื่อมต่อ MLflow Server:**
# - URL: `http://127.0.0.1:8080`

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 1: การเชื่อมต่อ MLflow Server
#
# ก่อนเริ่มใช้งาน MLflow Tracking เราต้องกำหนด Tracking URI เพื่อบอกให้ MLflow รู้ว่า
# จะเก็บข้อมูลการทดลองไว้ที่ไหน ในกรณีนี้เราจะเชื่อมต่อกับ MLflow Server ที่รันอยู่ที่ `127.0.0.1:8080`
#
# **คำอธิบาย:**
# - `mlflow.set_tracking_uri()` ใช้กำหนด URL ของ MLflow Tracking Server
# - `mlflow.get_tracking_uri()` ใช้ตรวจสอบ URL ที่กำหนดไว้

# %%
import mlflow
import os

# กำหนด Tracking URI ไปยัง MLflow Server
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# ตรวจสอบว่าเชื่อมต่อถูกต้อง
print(f"✅ MLflow Tracking URI: {mlflow.get_tracking_uri()}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 2: การสร้าง Experiment
#
# **Experiment** คือกลุ่มของ Runs ที่เกี่ยวข้องกัน เปรียบเสมือน "โปรเจกต์" หรือ "หัวข้อการทดลอง"
# ทุก Run ต้องอยู่ภายใต้ Experiment ใดเสมอ
#
# **หลักการตั้งชื่อ Experiment:**
# - ใช้ชื่อที่สื่อความหมายชัดเจน เช่น `fraud-detection-lstm`, `customer-churn-prediction`
# - หลีกเลี่ยงชื่อทั่วไป เช่น `test`, `experiment1`
# - ใช้ kebab-case หรือ snake_case เพื่อความสม่ำเสมอ
#
# **คำอธิบาย:**
# - `mlflow.set_experiment()` สร้างหรือเลือก Experiment (ถ้ามีอยู่แล้วจะเลือกใช้อันเดิม)
# - `mlflow.get_experiment_by_name()` ดึงข้อมูล Experiment ตามชื่อที่กำหนด

# %%
# สร้างหรือเลือก Experiment
experiment_name = "mlflow-tracking-lab"
mlflow.set_experiment(experiment_name)

# ดูข้อมูล Experiment
experiment = mlflow.get_experiment_by_name(experiment_name)
print(f"📁 Experiment Name: {experiment.name}")
print(f"🆔 Experiment ID: {experiment.experiment_id}")
print(f"📂 Artifact Location: {experiment.artifact_location}")
print(f"🔄 Lifecycle Stage: {experiment.lifecycle_stage}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 3: การสร้าง Run และบันทึก Parameters
#
# **Run** คือการทดลองแต่ละครั้ง เป็นหน่วยพื้นฐานที่สุดของ MLflow Tracking
# ทุกครั้งที่ train model ด้วย hyperparameters ชุดใหม่ ควรสร้าง Run ใหม่
#
# **Parameters** คือค่าที่เราตั้งก่อนเริ่มการทดลอง (Input Configuration) 
# เป็นค่าคงที่ตลอดการทดลอง ไม่เปลี่ยนแปลง
#
# **ประเภทของ Parameters:**
# | ประเภท | ตัวอย่าง |
# |--------|----------|
# | Model Hyperparameters | learning_rate, batch_size, epochs |
# | Data Parameters | train_split, image_size |
# | Architecture | model_type, num_layers |
# | Training Config | optimizer, loss_function |
#
# **คำอธิบาย:**
# - `mlflow.start_run()` เริ่มต้น Run ใหม่ (ใช้ context manager เพื่อปิด Run อัตโนมัติ)
# - `mlflow.log_param()` บันทึก Parameter ทีละค่า
# - `mlflow.log_params()` บันทึกหลาย Parameters พร้อมกัน (dictionary)

# %%
# กลับมาใช้ Experiment หลัก
mlflow.set_experiment("mlflow-tracking-lab")

# สร้าง Run และบันทึก Parameters
with mlflow.start_run(run_name="demo-parameters"):
    
    # วิธีที่ 1: บันทึกทีละค่า
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 100)
    
    # วิธีที่ 2: บันทึกหลายค่าพร้อมกัน (แนะนำ)
    mlflow.log_params({
        "optimizer": "adam",
        "dropout": 0.5,
        "hidden_units": 256,
        "activation": "relu",
        "model_type": "MLP"
    })
    
    # ดู Run ID
    run_id = mlflow.active_run().info.run_id
    print(f"✅ สร้าง Run สำเร็จ!")
    print(f"🆔 Run ID: {run_id}")
    print(f"📝 บันทึก Parameters: learning_rate, batch_size, epochs, optimizer, dropout, hidden_units, activation, model_type")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 4: การบันทึก Metrics
#
# **Metrics** คือค่าที่วัดได้จากการทดลอง (Output/Results) 
# สามารถบันทึกได้หลายครั้งพร้อม step number เพื่อติดตามการเปลี่ยนแปลงตามเวลา
#
# **ความแตกต่างระหว่าง Parameters และ Metrics:**
# | คุณสมบัติ | Parameters | Metrics |
# |-----------|------------|---------|
# | เวลาบันทึก | ก่อนเริ่มทดลอง | ระหว่าง/หลังทดลอง |
# | จำนวนค่า | ค่าเดียวต่อชื่อ | หลายค่าได้ (ต่าง step) |
# | การเปลี่ยนแปลง | คงที่ | เปลี่ยนได้ตามเวลา |
# | วัตถุประสงค์ | บอกว่าทำอะไร (Input) | บอกว่าได้ผลอย่างไร (Output) |
#
# **คำอธิบาย:**
# - `mlflow.log_metric()` บันทึก Metric ค่าเดียว (สามารถระบุ step ได้)
# - `mlflow.log_metrics()` บันทึกหลาย Metrics พร้อมกัน
# - parameter `step` ใช้ระบุลำดับ เช่น epoch number

# %%
import random

with mlflow.start_run(run_name="demo-metrics"):
    
    # บันทึก Parameters ก่อน
    mlflow.log_params({
        "learning_rate": 0.01,
        "epochs": 10,
        "batch_size": 64
    })
    
    # จำลองการ Training และบันทึก Metrics ทุก epoch
    print("🚀 เริ่มการจำลอง Training...")
    
    for epoch in range(10):
        # จำลองค่า loss และ accuracy (ในการใช้งานจริงจะได้จากการ train)
        train_loss = 1.0 - (epoch * 0.08) + random.uniform(-0.05, 0.05)
        val_loss = 1.0 - (epoch * 0.07) + random.uniform(-0.05, 0.05)
        train_acc = 0.5 + (epoch * 0.04) + random.uniform(-0.02, 0.02)
        val_acc = 0.5 + (epoch * 0.035) + random.uniform(-0.02, 0.02)
        
        # บันทึก Metrics พร้อม step
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "train_accuracy": train_acc,
            "val_accuracy": val_acc
        }, step=epoch)
        
        print(f"  Epoch {epoch+1}/10 - train_loss: {train_loss:.4f}, val_loss: {val_loss:.4f}, train_acc: {train_acc:.4f}, val_acc: {val_acc:.4f}")
    
    # บันทึก Final Metrics
    mlflow.log_metrics({
        "final_accuracy": val_acc,
        "final_loss": val_loss
    })
    
    print(f"\n✅ Training เสร็จสิ้น!")
    print(f"📊 Final Accuracy: {val_acc:.4f}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 5: การบันทึก Artifacts
#
# **Artifacts** คือไฟล์ที่สร้างจากการทดลอง สามารถเป็นไฟล์ประเภทใดก็ได้
# MLflow จะเก็บไว้ใน Artifact Store
#
# **ประเภทของ Artifacts:**
# | ประเภท | ตัวอย่าง |
# |--------|----------|
# | Models | model.pkl, model.h5, model.pt |
# | Visualizations | confusion_matrix.png, loss_curve.png |
# | Data | predictions.csv, feature_importance.json |
# | Reports | report.html, summary.pdf |
#
# **คำอธิบาย:**
# - `mlflow.log_artifact()` บันทึกไฟล์เดี่ยว
# - `mlflow.log_artifacts()` บันทึกทั้งโฟลเดอร์
# - `mlflow.log_figure()` บันทึก matplotlib figure โดยตรง
# - `mlflow.log_dict()` บันทึก dictionary เป็น JSON
# - `mlflow.log_text()` บันทึก text

# %%
import matplotlib.pyplot as plt
import json

# สร้างโฟลเดอร์สำหรับเก็บไฟล์ชั่วคราว
os.makedirs("outputs", exist_ok=True)

with mlflow.start_run(run_name="demo-artifacts"):
    
    # บันทึก Parameters และ Metrics
    mlflow.log_params({"model": "demo", "epochs": 10})
    mlflow.log_metric("accuracy", 0.92)
    
    # ----- Artifact 1: บันทึก Figure จาก matplotlib -----
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # กราฟ Loss
    epochs = range(1, 11)
    train_loss = [1.0, 0.8, 0.65, 0.52, 0.42, 0.35, 0.30, 0.26, 0.23, 0.20]
    val_loss = [1.1, 0.9, 0.75, 0.62, 0.55, 0.50, 0.47, 0.45, 0.44, 0.43]
    
    axes[0].plot(epochs, train_loss, 'b-', label='Train Loss')
    axes[0].plot(epochs, val_loss, 'r-', label='Validation Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training & Validation Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # กราฟ Accuracy
    train_acc = [0.5, 0.6, 0.68, 0.74, 0.79, 0.83, 0.86, 0.88, 0.90, 0.92]
    val_acc = [0.48, 0.55, 0.62, 0.68, 0.72, 0.75, 0.77, 0.78, 0.79, 0.80]
    
    axes[1].plot(epochs, train_acc, 'b-', label='Train Accuracy')
    axes[1].plot(epochs, val_acc, 'r-', label='Validation Accuracy')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Training & Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    
    # บันทึก figure โดยตรง (วิธีที่แนะนำ)
    mlflow.log_figure(fig, artifact_file="plots/training_curves.png")
    plt.close(fig)
    print("✅ บันทึก training_curves.png สำเร็จ")
    
    # ----- Artifact 2: บันทึก Dictionary เป็น JSON -----
    config = {
        "model_architecture": "CNN",
        "input_shape": [224, 224, 3],
        "num_classes": 10,
        "layers": ["Conv2D", "MaxPooling", "Conv2D", "MaxPooling", "Dense", "Softmax"]
    }
    mlflow.log_dict(config, artifact_file="config/model_config.json")
    print("✅ บันทึก model_config.json สำเร็จ")
    
    # ----- Artifact 3: บันทึก Text -----
    model_info = """Model: CNN Classifier v1.0
Created: 2024
Author: MLflow Lab
Description: Demo model for MLflow Tracking Lab
"""
    mlflow.log_text(model_info, artifact_file="models/model_info.txt")
    print("✅ บันทึก model_info.txt สำเร็จ")
    
    # ----- Artifact 4: บันทึกไฟล์จากโฟลเดอร์ -----
    # สร้างไฟล์ตัวอย่างในโฟลเดอร์ outputs
    with open("outputs/predictions.csv", "w") as f:
        f.write("id,true_label,predicted_label,confidence\n")
        f.write("1,cat,cat,0.95\n")
        f.write("2,dog,dog,0.88\n")
        f.write("3,bird,cat,0.45\n")
    
    mlflow.log_artifact("outputs/predictions.csv", artifact_path="data")
    print("✅ บันทึก predictions.csv สำเร็จ")
    
    print(f"\n📦 Artifacts ทั้งหมดถูกบันทึกเรียบร้อย!")
    print(f"🔗 ดูได้ที่ MLflow UI: http://127.0.0.1:8080")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 6: การบันทึก Model (Model Logging)
#
# **Model Logging** เป็นฟีเจอร์สำคัญของ MLflow ที่ช่วยให้เราสามารถบันทึก Model 
# พร้อมกับข้อมูลที่จำเป็นสำหรับการนำไปใช้งาน (Deployment) ได้อย่างสมบูรณ์
#
# **ประโยชน์ของการบันทึก Model ผ่าน MLflow:**
# - บันทึก Model พร้อม dependencies และ environment
# - สามารถโหลด Model กลับมาใช้งานได้ง่าย
# - รองรับการ Deploy ไปยัง Production
# - เก็บ Model signature (input/output schema)
#
# **MLflow รองรับ Model Flavors หลายประเภท:**
# | Flavor | Library | ฟังก์ชัน |
# |--------|---------|----------|
# | `mlflow.sklearn` | Scikit-learn | `log_model()`, `load_model()` |
# | `mlflow.pytorch` | PyTorch | `log_model()`, `load_model()` |
# | `mlflow.tensorflow` | TensorFlow/Keras | `log_model()`, `load_model()` |
# | `mlflow.xgboost` | XGBoost | `log_model()`, `load_model()` |
# | `mlflow.pyfunc` | Generic Python | `log_model()`, `load_model()` |

# %% [markdown]
# ### 6.1 การบันทึก Scikit-learn Model
#
# **คำอธิบาย:**
# - `mlflow.sklearn.log_model()` บันทึก sklearn model
# - `artifact_path` กำหนดชื่อโฟลเดอร์ที่จะเก็บ model
# - `signature` บันทึก input/output schema ของ model
# - `input_example` ตัวอย่าง input สำหรับอ้างอิง

# %%
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from mlflow.models import infer_signature

# โหลดข้อมูล Iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

with mlflow.start_run(run_name="sklearn-model-demo"):
    
    # กำหนด hyperparameters
    n_estimators = 100
    max_depth = 5
    random_state = 42
    
    # บันทึก Parameters
    mlflow.log_params({
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "random_state": random_state,
        "model_type": "RandomForestClassifier"
    })
    
    # สร้างและ Train Model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    # ทำนายและคำนวณ Metrics
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # บันทึก Metrics
    mlflow.log_metric("accuracy", accuracy)
    print(f"📊 Accuracy: {accuracy:.4f}")
    
    # สร้าง Signature (input/output schema)
    signature = infer_signature(X_train, model.predict(X_train))
    
    # บันทึก Model พร้อม signature และ input example
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        signature=signature,
        input_example=X_train[:3]  # ตัวอย่าง input 3 แถวแรก
    )
    
    print(f"✅ บันทึก Model สำเร็จ!")
    print(f"📦 Model ถูกเก็บไว้ใน artifacts/model/")
    
    # เก็บ run_id สำหรับใช้โหลด model ภายหลัง
    sklearn_run_id = mlflow.active_run().info.run_id
    print(f"🆔 Run ID: {sklearn_run_id}")

# %% [markdown]
# ### 6.2 การโหลด Model กลับมาใช้งาน
#
# **วิธีการโหลด Model:**
# - ใช้ `mlflow.<flavor>.load_model()` โหลด model ตาม flavor
# - ระบุ path ในรูปแบบ `runs:/<run_id>/<artifact_path>`
# - หรือใช้ `models:/<model_name>/<version>` สำหรับ registered models
#
# **คำอธิบาย:**
# - `mlflow.sklearn.load_model()` โหลด sklearn model
# - `mlflow.pyfunc.load_model()` โหลด model เป็น generic Python function

# %%
# โหลด Model กลับมาใช้งาน
model_uri = f"runs:/{sklearn_run_id}/model"

# วิธีที่ 1: โหลดเป็น sklearn model (ได้ native sklearn object)
loaded_model = mlflow.sklearn.load_model(model_uri)
print(f"✅ โหลด Model สำเร็จ: {type(loaded_model)}")

# วิธีที่ 2: โหลดเป็น pyfunc (generic Python function)
pyfunc_model = mlflow.pyfunc.load_model(model_uri)
print(f"✅ โหลดเป็น PyFunc: {type(pyfunc_model)}")

# ทดสอบทำนาย
sample_data = X_test[:5]
predictions = loaded_model.predict(sample_data)
print(f"\n🔮 ทดสอบทำนาย 5 ตัวอย่างแรก:")
print(f"   Predictions: {predictions}")
print(f"   Actual:      {y_test[:5]}")

# %% [markdown]
# ### 6.3 การบันทึก PyTorch Model
#
# **คำอธิบาย:**
# - `mlflow.pytorch.log_model()` บันทึก PyTorch model
# - รองรับทั้ง `nn.Module` และ `torch.jit.ScriptModule`
# - สามารถระบุ `conda_env` หรือ `pip_requirements` ได้

# %%
import torch
import torch.nn as nn

# สร้าง Simple Neural Network
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

with mlflow.start_run(run_name="pytorch-model-demo"):
    
    # กำหนด hyperparameters
    input_size = 4
    hidden_size = 16
    num_classes = 3
    learning_rate = 0.01
    epochs = 100
    
    # บันทึก Parameters
    mlflow.log_params({
        "input_size": input_size,
        "hidden_size": hidden_size,
        "num_classes": num_classes,
        "learning_rate": learning_rate,
        "epochs": epochs,
        "model_type": "SimpleNN"
    })
    
    # สร้าง Model
    pytorch_model = SimpleNN(input_size, hidden_size, num_classes)
    
    # เตรียมข้อมูล
    X_tensor = torch.FloatTensor(X_train)
    y_tensor = torch.LongTensor(y_train)
    
    # Training
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(pytorch_model.parameters(), lr=learning_rate)
    
    print("🚀 เริ่ม Training PyTorch Model...")
    for epoch in range(epochs):
        outputs = pytorch_model(X_tensor)
        loss = criterion(outputs, y_tensor)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            mlflow.log_metric("train_loss", loss.item(), step=epoch)
            print(f"   Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
    
    # คำนวณ Accuracy
    pytorch_model.eval()
    with torch.no_grad():
        X_test_tensor = torch.FloatTensor(X_test)
        outputs = pytorch_model(X_test_tensor)
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted.numpy() == y_test).sum() / len(y_test)
    
    mlflow.log_metric("accuracy", accuracy)
    print(f"\n📊 Test Accuracy: {accuracy:.4f}")
    
    # สร้าง Signature
    signature = infer_signature(
        X_train, 
        pytorch_model(torch.FloatTensor(X_train)).detach().numpy()
    )
    
    # บันทึก PyTorch Model
    mlflow.pytorch.log_model(
        pytorch_model=pytorch_model,
        artifact_path="pytorch_model",
        signature=signature,
        input_example=X_train[:3]
    )
    
    print(f"✅ บันทึก PyTorch Model สำเร็จ!")
    pytorch_run_id = mlflow.active_run().info.run_id
    print(f"🆔 Run ID: {pytorch_run_id}")

# %% [markdown]
# ### 6.4 การบันทึก Model ด้วย Autolog
#
# **Autolog** เป็นฟีเจอร์ที่ช่วยบันทึก Parameters, Metrics และ Model อัตโนมัติ
# โดยไม่ต้องเขียนโค้ดบันทึกเอง
#
# **รองรับหลาย Framework:**
# - `mlflow.sklearn.autolog()`
# - `mlflow.pytorch.autolog()`
# - `mlflow.tensorflow.autolog()`
# - `mlflow.xgboost.autolog()`
# - `mlflow.lightgbm.autolog()`
#
# **คำอธิบาย:**
# - เรียก `autolog()` ก่อนเริ่ม training
# - MLflow จะบันทึกทุกอย่างอัตโนมัติ

# %%
from sklearn.linear_model import LogisticRegression

# เปิด Autolog สำหรับ sklearn
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="autolog-demo"):
    # แค่ train model ตามปกติ MLflow จะบันทึกทุกอย่างอัตโนมัติ
    auto_model = LogisticRegression(max_iter=200, C=1.0, solver='lbfgs')
    auto_model.fit(X_train, y_train)
    
    # คำนวณ accuracy (Autolog จะบันทึก metrics พื้นฐานให้)
    accuracy = auto_model.score(X_test, y_test)
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"✅ Autolog บันทึก Parameters, Metrics และ Model อัตโนมัติ!")

# ปิด Autolog หลังใช้งาน
mlflow.sklearn.autolog(disable=True)

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 7: Nested Runs (การรันซ้อนกัน)
#
# **Nested Runs** ใช้สำหรับจัดกลุ่มการทดลองที่เกี่ยวข้องกัน โดยเฉพาะในกรณี:
# - Hyperparameter Tuning (ทดลองหลายค่าพารามิเตอร์)
# - Cross-Validation (ทดลองหลาย folds)
# - Ensemble Models (รวมหลาย models)
#
# **โครงสร้าง:**
# ```
# Parent Run: hyperparameter-tuning
# ├── Child Run 1: lr=0.001
# ├── Child Run 2: lr=0.01
# └── Child Run 3: lr=0.1
# ```
#
# **คำอธิบาย:**
# - ใช้ `nested=True` ใน `mlflow.start_run()` เพื่อสร้าง Child Run
# - Parent Run จะรวบรวม Child Runs ทั้งหมดไว้ด้วยกัน
# - ช่วยให้จัดระเบียบและเปรียบเทียบผลการทดลองได้ง่าย

# %%
# จำลอง Hyperparameter Tuning ด้วย Nested Runs
learning_rates = [0.001, 0.01, 0.1]

with mlflow.start_run(run_name="hyperparameter-tuning"):
    print("🔄 เริ่ม Hyperparameter Tuning...")
    
    # บันทึก Parameters ของ Parent Run
    mlflow.log_param("experiment_type", "learning_rate_search")
    mlflow.log_param("search_space", str(learning_rates))
    
    best_accuracy = 0
    best_lr = None
    
    for lr in learning_rates:
        # สร้าง Child Run สำหรับแต่ละ learning rate
        with mlflow.start_run(run_name=f"lr-{lr}", nested=True):
            mlflow.log_param("learning_rate", lr)
            
            # จำลองการ training (ในการใช้งานจริงจะ train model จริง)
            # learning rate ที่เหมาะสมคือ 0.01
            if lr == 0.01:
                accuracy = 0.92 + random.uniform(-0.02, 0.02)
            elif lr == 0.001:
                accuracy = 0.85 + random.uniform(-0.02, 0.02)
            else:  # lr = 0.1
                accuracy = 0.70 + random.uniform(-0.05, 0.05)
            
            mlflow.log_metric("accuracy", accuracy)
            print(f"  ✅ lr={lr} → accuracy={accuracy:.4f}")
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_lr = lr
    
    # บันทึกผลลัพธ์ที่ดีที่สุดใน Parent Run
    mlflow.log_metric("best_accuracy", best_accuracy)
    mlflow.log_param("best_learning_rate", best_lr)
    
    print(f"\n🏆 Best Result: lr={best_lr}, accuracy={best_accuracy:.4f}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 8: การดูข้อมูลจาก MLflow UI
#
# หลังจากบันทึกข้อมูลแล้ว สามารถดูผลลัพธ์ได้ที่ MLflow UI
#
# **วิธีเข้าถึง MLflow UI:**
# 1. เปิด Browser
# 2. ไปที่ URL: `http://127.0.0.1:8080`
#
# **สิ่งที่สามารถทำได้ใน MLflow UI:**
# - เปรียบเทียบ Runs หลายๆ ตัว
# - ดูกราฟ Metrics ตาม step
# - Download Artifacts
# - ค้นหา Runs ด้วย Filter
# - จัดกลุ่ม Runs ด้วย Tags
#
# **คำอธิบาย:**
# - `mlflow.search_runs()` ค้นหา Runs ใน Experiment
# - สามารถ filter ด้วย parameters และ metrics ได้

# %%
# ค้นหา Runs ใน Experiment
runs = mlflow.search_runs(
    experiment_names=["mlflow-tracking-lab"],
    order_by=["start_time DESC"],
    max_results=5
)

print("📋 Recent Runs:")
print("=" * 80)
for _, row in runs.iterrows():
    run_name = row.get("tags.mlflow.runName", "N/A")
    status = row["status"]
    start_time = row["start_time"]
    print(f"  Run: {run_name:<30} | Status: {status:<10} | Started: {start_time}")

print(f"\n🔗 ดูรายละเอียดเพิ่มเติมได้ที่: http://127.0.0.1:8080")

# %% [markdown]
# ---
# ## 📝 สรุปบทเรียน
#
# ในบทเรียนนี้ได้เรียนรู้:
#
# | องค์ประกอบ | คำอธิบาย | ฟังก์ชันหลัก |
# |------------|----------|--------------|
# | **Experiment** | กลุ่มของ Runs ที่เกี่ยวข้องกัน | `mlflow.set_experiment()` |
# | **Run** | การทดลองแต่ละครั้ง | `mlflow.start_run()` |
# | **Parameters** | ค่าที่ตั้งก่อนเริ่มทดลอง (Input) | `mlflow.log_param()`, `mlflow.log_params()` |
# | **Metrics** | ค่าที่วัดได้จากการทดลอง (Output) | `mlflow.log_metric()`, `mlflow.log_metrics()` |
# | **Artifacts** | ไฟล์ที่สร้างจากการทดลอง | `mlflow.log_artifact()`, `mlflow.log_figure()` |
# | **Model** | บันทึกและโหลด ML Model | `mlflow.sklearn.log_model()`, `mlflow.pytorch.log_model()` |
#
# **Best Practices:**
# - ตั้งชื่อ Experiment และ Run ให้สื่อความหมาย
# - บันทึก Parameters ทุกค่าที่มีผลต่อผลลัพธ์
# - บันทึก Metrics พร้อม step เพื่อติดตามการเปลี่ยนแปลง
# - ใช้ Nested Runs สำหรับ Hyperparameter Tuning
# - บันทึก Artifacts ที่สำคัญ เช่น model, plots, config
# - ใช้ `signature` และ `input_example` เมื่อบันทึก Model
# - พิจารณาใช้ `autolog()` สำหรับความสะดวก

# %%
# ทำความสะอาดไฟล์ชั่วคราว
import shutil
if os.path.exists("outputs"):
    shutil.rmtree("outputs")
print("🧹 ทำความสะอาดไฟล์ชั่วคราวเรียบร้อย")
