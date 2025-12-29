# %% [markdown]
# # 🧪 Lab: MLflow Tracking พื้นฐาน
# 
# **วัตถุประสงค์การเรียนรู้:**
# - เข้าใจองค์ประกอบหลัก 5 ส่วนของ MLflow Tracking
# - สามารถสร้าง Experiment และ Run ได้
# - บันทึก Parameters, Metrics และ Artifacts ได้อย่างถูกต้อง
# - บันทึกและโหลด Model ได้
# - เปรียบเทียบผลการทดลองผ่าน MLflow UI
# 
# **องค์ประกอบหลักของ MLflow Tracking:**
# | องค์ประกอบ | คำอธิบาย | ตัวอย่าง |
# |------------|----------|----------|
# | **Experiment** | กลุ่มของการทดลองที่เกี่ยวข้องกัน | `fraud-detection`, `customer-churn` |
# | **Run** | การทดลองแต่ละครั้ง | แต่ละครั้งที่ train model |
# | **Parameters** | ค่าที่ตั้งก่อนเริ่มทดลอง (Input) | `learning_rate=0.001`, `epochs=100` |
# | **Metrics** | ค่าที่วัดได้จากการทดลอง (Output) | `accuracy=0.92`, `loss=0.15` |
# | **Artifacts** | ไฟล์ที่สร้างจากการทดลอง | `model.pkl`, `confusion_matrix.png` |

# %% [markdown]
# ---
# ## ⚙️ Pre-requisite: เตรียมความพร้อมก่อนเริ่ม Lab
# 
# ### 📋 สิ่งที่ต้องมี
# 
# ก่อนเริ่ม Lab นี้ ต้องมี MLflow Server รันอยู่และเข้าถึงได้ที่ `http://127.0.0.1:8080`
# 
# ### 🔍 ตรวจสอบ MLflow Server
# 
# เปิด Browser แล้วไปที่: [http://127.0.0.1:8080](http://127.0.0.1:8080)
# 
# ![MLflow UI](./img/1.png)

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 1: การเชื่อมต่อ MLflow Server
# 
# ### แนวคิด
# ก่อนใช้งาน MLflow Tracking ต้องกำหนด **Tracking URI** เพื่อบอกว่าจะเก็บข้อมูลการทดลองไว้ที่ไหน
# 
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.set_tracking_uri(uri)` | กำหนด URL ของ MLflow Server |
# | `mlflow.get_tracking_uri()` | ตรวจสอบ URL ที่กำหนดไว้ |
# 
# ### ทางเลือกอื่นสำหรับ Tracking URI
# | ประเภท | ตัวอย่าง URI | คำอธิบาย |
# |--------|--------------|----------|
# | Local File | `file:///path/to/mlruns` | เก็บในโฟลเดอร์ local |
# | Remote Server | `http://server:5000` | เก็บบน MLflow Server |
# | Databricks | `databricks` | เก็บบน Databricks |
# | SQLite | `sqlite:///mlflow.db` | เก็บใน SQLite database |

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
# ### แนวคิด
# **Experiment** คือกลุ่มของ Runs ที่เกี่ยวข้องกัน เปรียบเสมือน "โปรเจกต์" หรือ "หัวข้อการทดลอง"
# 
# ```
# Experiment: fraud-detection-project
# ├── Run 1: baseline-model
# ├── Run 2: lstm-v1
# ├── Run 3: lstm-v2-tuned
# └── Run 4: transformer-model
# ```
# 
# ### หลักการตั้งชื่อ Experiment
# | ✅ ชื่อที่ดี | ❌ ชื่อที่ควรหลีกเลี่ยง |
# |-------------|------------------------|
# | `fraud-detection-lstm` | `test` |
# | `customer-churn-prediction` | `experiment1` |
# | `image-classification-resnet` | `my_model` |
# 
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.set_experiment(name)` | สร้างหรือเลือก Experiment |
# | `mlflow.get_experiment_by_name(name)` | ดึงข้อมูล Experiment |
# 
# ### คุณสมบัติของ Experiment Object
# | คุณสมบัติ | คำอธิบาย |
# |-----------|----------|
# | `name` | ชื่อ Experiment |
# | `experiment_id` | ID เฉพาะของ Experiment |
# | `artifact_location` | ที่เก็บ Artifacts |
# | `lifecycle_stage` | สถานะ (`active` หรือ `deleted`) |
# | `tags` | Tags ที่กำหนด |

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
# ### แนวคิด
# **Run** คือการทดลองแต่ละครั้ง เป็นหน่วยพื้นฐานที่สุดของ MLflow Tracking
# ทุกครั้งที่ train model ด้วย hyperparameters ชุดใหม่ ควรสร้าง Run ใหม่
# 
# **Parameters** คือค่าที่เราตั้งก่อนเริ่มการทดลอง (Input Configuration) 
# เป็นค่าคงที่ตลอดการทดลอง ไม่เปลี่ยนแปลง
# 
# ### ประเภทของ Parameters
# | ประเภท | ตัวอย่าง |
# |--------|----------|
# | Model Hyperparameters | `learning_rate`, `batch_size`, `epochs` |
# | Data Parameters | `train_split`, `image_size` |
# | Architecture | `model_type`, `num_layers`, `hidden_units` |
# | Training Config | `optimizer`, `loss_function` |
# 
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.start_run(run_name)` | เริ่มต้น Run ใหม่ |
# | `mlflow.log_param(key, value)` | บันทึก Parameter ทีละค่า |
# | `mlflow.log_params(dict)` | บันทึกหลาย Parameters พร้อมกัน |
# | `mlflow.active_run()` | ดึงข้อมูล Run ที่กำลังทำงานอยู่ |
# 
# ### Context Manager (`with` statement)
# การใช้ `with mlflow.start_run()` มีข้อดีคือ:
# - Run จะถูกปิดอัตโนมัติเมื่อออกจาก block
# - ป้องกันการลืมปิด Run
# - จัดการ error ได้ดีกว่า

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
# ### แนวคิด
# **Metrics** คือค่าที่วัดได้จากการทดลอง (Output/Results) 
# สามารถบันทึกได้หลายครั้งพร้อม step number เพื่อติดตามการเปลี่ยนแปลงตามเวลา
# 
# ### ความแตกต่างระหว่าง Parameters และ Metrics
# | คุณสมบัติ | Parameters | Metrics |
# |-----------|------------|---------|
# | เวลาบันทึก | ก่อนเริ่มทดลอง | ระหว่าง/หลังทดลอง |
# | จำนวนค่า | ค่าเดียวต่อชื่อ | หลายค่าได้ (ต่าง step) |
# | การเปลี่ยนแปลง | คงที่ | เปลี่ยนได้ตามเวลา |
# | วัตถุประสงค์ | บอกว่าทำอะไร (Input) | บอกว่าได้ผลอย่างไร (Output) |
# 
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.log_metric(key, value, step)` | บันทึก Metric ค่าเดียว |
# | `mlflow.log_metrics(dict, step)` | บันทึกหลาย Metrics พร้อมกัน |
# 
# ### การใช้ Step Parameter
# Step ทำให้ MLflow สามารถสร้างกราฟแสดงการเปลี่ยนแปลงของ metric ตามเวลาได้

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
# ### แนวคิด
# **Artifacts** คือไฟล์ที่สร้างจากการทดลอง สามารถเป็นไฟล์ประเภทใดก็ได้
# MLflow จะเก็บไว้ใน Artifact Store
# 
# ### ประเภทของ Artifacts
# | ประเภท | ตัวอย่างไฟล์ |
# |--------|-------------|
# | Models | `model.pkl`, `model.h5`, `model.pt` |
# | Visualizations | `confusion_matrix.png`, `loss_curve.png` |
# | Data | `predictions.csv`, `feature_importance.json` |
# | Reports | `report.html`, `summary.pdf` |
# | Configs | `config.yaml`, `hyperparams.json` |
# 
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.log_artifact(local_path, artifact_path)` | บันทึกไฟล์เดี่ยว |
# | `mlflow.log_artifacts(local_dir, artifact_path)` | บันทึกทั้งโฟลเดอร์ |
# | `mlflow.log_figure(fig, artifact_file)` | บันทึก matplotlib figure |
# | `mlflow.log_dict(dict, artifact_file)` | บันทึก dictionary เป็น JSON |
# | `mlflow.log_text(text, artifact_file)` | บันทึก text |

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
# ### แนวคิด
# **Model Logging** เป็นฟีเจอร์สำคัญของ MLflow ที่ช่วยให้เราสามารถบันทึก Model 
# พร้อมกับข้อมูลที่จำเป็นสำหรับการนำไปใช้งาน (Deployment) ได้อย่างสมบูรณ์
# 
# ### ประโยชน์ของการบันทึก Model ผ่าน MLflow
# - บันทึก Model พร้อม dependencies และ environment
# - สามารถโหลด Model กลับมาใช้งานได้ง่าย
# - รองรับการ Deploy ไปยัง Production
# - เก็บ Model signature (input/output schema)
# 
# ### MLflow Model Flavors
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
# **ฟังก์ชันสำคัญ:**
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
# **รูปแบบ Model URI:**
# | รูปแบบ | ตัวอย่าง | คำอธิบาย |
# |--------|----------|----------|
# | Runs | `runs:/<run_id>/model` | โหลดจาก Run ID |
# | Models | `models:/<name>/<version>` | โหลดจาก Model Registry |
# | Local Path | `/path/to/model` | โหลดจาก local path |

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
# **ฟังก์ชันสำคัญ:**
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
# ### แนวคิด
# **Nested Runs** ใช้สำหรับจัดกลุ่มการทดลองที่เกี่ยวข้องกัน โดยเฉพาะในกรณี:
# - Hyperparameter Tuning (ทดลองหลายค่าพารามิเตอร์)
# - Cross-Validation (ทดลองหลาย folds)
# - Ensemble Models (รวมหลาย models)
# 
# ### โครงสร้าง Nested Runs
# ```
# Parent Run: hyperparameter-tuning
# ├── Child Run 1: lr=0.001 → accuracy=0.85
# ├── Child Run 2: lr=0.01  → accuracy=0.92 ⭐
# └── Child Run 3: lr=0.1   → accuracy=0.70
# ```
# 
# ### ข้อดีของ Nested Runs
# | ข้อดี | คำอธิบาย |
# |-------|----------|
# | จัดระเบียบ | จัดกลุ่มการทดลองที่เกี่ยวข้องไว้ด้วยกัน |
# | เปรียบเทียบง่าย | เห็นผลการทดลองทั้งหมดในที่เดียว |
# | สรุปผล | Parent Run เก็บผลลัพธ์ที่ดีที่สุด |
# | UI ชัดเจน | แสดงเป็น tree structure ใน MLflow UI |

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
# หลังจากบันทึกข้อมูลการทดลองแล้ว เราสามารถดูและวิเคราะห์ผลลัพธ์ผ่าน MLflow UI 
# ซึ่งเป็น Web Interface ที่ใช้งานง่าย
# 
# ### 8.1 การเข้าถึง MLflow UI
# 
# เปิด Browser แล้วไปที่: [http://127.0.0.1:8080](http://127.0.0.1:8080)
# 
# ![MLflow UI Homepage](./img/mlflow-ui-home.png)

# %% [markdown]
# ### 8.2 ส่วนประกอบหลักของ MLflow UI
# 
# #### 📁 Experiments Sidebar (แถบด้านซ้าย)
# แสดงรายการ Experiments ทั้งหมด สามารถคลิกเลือกเพื่อดู Runs ภายใน
# 
# #### 📋 Runs Table (ตารางกลาง)
# แสดงรายการ Runs ทั้งหมดใน Experiment ที่เลือก พร้อมข้อมูล:
# - **Run Name**: ชื่อ Run
# - **Created**: วันเวลาที่สร้าง
# - **Duration**: ระยะเวลาที่ใช้
# - **Parameters**: ค่า Parameters ที่บันทึก
# - **Metrics**: ค่า Metrics ที่บันทึก

# %% [markdown]
# ### 8.3 การดูรายละเอียด Run
# 
# คลิกที่ Run Name เพื่อดูรายละเอียด จะเห็นหน้าที่แบ่งเป็น Tabs:
# 
# | Tab | คำอธิบาย |
# |-----|----------|
# | **Overview** | แสดงข้อมูลทั่วไปของ Run |
# | **Parameters** | แสดง Parameters ทั้งหมดที่บันทึก |
# | **Metrics** | แสดง Metrics พร้อมกราฟแสดงการเปลี่ยนแปลงตาม step |
# | **Artifacts** | แสดงไฟล์ที่บันทึกไว้ สามารถ Preview หรือ Download ได้ |

# %% [markdown]
# ### 8.4 การเปรียบเทียบหลาย Runs
# 
# #### วิธีการเปรียบเทียบ:
# 1. **เลือก Runs**: คลิก checkbox หน้า Runs ที่ต้องการเปรียบเทียบ
# 2. **คลิก Compare**: กดปุ่ม "Compare" ที่ด้านบน
# 
# #### หน้า Compare View:
# แสดงการเปรียบเทียบแบบ side-by-side:
# - **Parameters Comparison**: เปรียบเทียบค่า Parameters
# - **Metrics Comparison**: เปรียบเทียบค่า Metrics พร้อมกราฟ

# %% [markdown]
# ### 8.5 การค้นหาและ Filter Runs
# 
# #### ตัวอย่าง Filter Syntax:
# | Filter | ความหมาย |
# |--------|----------|
# | `metrics.accuracy > 0.9` | Runs ที่มี accuracy มากกว่า 0.9 |
# | `params.learning_rate = "0.01"` | Runs ที่ใช้ learning_rate = 0.01 |
# | `params.model_type = "MLP"` | Runs ที่ใช้ model_type = MLP |
# | `status = "FINISHED"` | Runs ที่ทำงานเสร็จแล้ว |

# %%
# ค้นหา Runs ใน Experiment
runs = mlflow.search_runs(
    experiment_names=["mlflow-tracking-lab"],
    order_by=["start_time DESC"],
    max_results=10
)

print("📋 Recent Runs:")
print("=" * 80)
for _, row in runs.iterrows():
    run_name = row.get("tags.mlflow.runName", "N/A")
    status = row["status"]
    start_time = row["start_time"]
    
    # ดึง metrics (ถ้ามี)
    accuracy = row.get("metrics.accuracy", "N/A")
    
    print(f"  Run: {run_name:<25} | Status: {status:<10} | Accuracy: {accuracy}")

print(f"\n🔗 ดูรายละเอียดเพิ่มเติมได้ที่: http://127.0.0.1:8080")

# %% [markdown]
# ### 8.6 การดู Nested Runs
# 
# Nested Runs จะแสดงเป็นโครงสร้าง tree ใน UI:
# 
# ```
# 📁 hyperparameter-tuning (Parent Run)
# ├── 📄 lr-0.001 (Child Run) - accuracy: 0.85
# ├── 📄 lr-0.01 (Child Run)  - accuracy: 0.92 ⭐
# └── 📄 lr-0.1 (Child Run)   - accuracy: 0.70
# ```
# 
# คลิกที่ Parent Run จะเห็น Child Runs ทั้งหมด

# %% [markdown]
# ### 8.7 การ Download Artifacts
# 
# #### วิธี Download ผ่าน UI:
# 1. เข้าไปที่หน้า Run Detail
# 2. คลิก Tab "Artifacts"
# 3. เลือกไฟล์ที่ต้องการ
# 4. คลิกปุ่ม Download

# %%
# Download artifacts ผ่าน Python
# หมายเหตุ: ต้องใส่ run_id จริงจากการทดลองก่อนหน้า

# ตัวอย่างการ download (uncomment เพื่อใช้งาน)
# run_id = "your-run-id-here"
# local_path = mlflow.artifacts.download_artifacts(
#     run_id=run_id,
#     artifact_path="",  # "" = download ทั้งหมด
#     dst_path="./downloaded_artifacts"
# )
# print(f"Downloaded to: {local_path}")

print("💡 Tip: ใช้ mlflow.artifacts.download_artifacts() เพื่อ download artifacts ผ่าน Python")

# %% [markdown]
# ### 8.8 การจัดการ Tags
# 
# Tags ช่วยจัดกลุ่มและค้นหา Runs ได้ง่ายขึ้น

# %%
with mlflow.start_run(run_name="tagged-run"):
    # บันทึก Tags
    mlflow.set_tag("team", "data-science")
    mlflow.set_tag("version", "v1.0")
    mlflow.set_tag("environment", "development")
    
    # บันทึกหลาย Tags พร้อมกัน
    mlflow.set_tags({
        "dataset": "iris",
        "framework": "sklearn"
    })
    
    # บันทึก parameter และ metric ตัวอย่าง
    mlflow.log_param("model", "demo")
    mlflow.log_metric("accuracy", 0.95)
    
    print("✅ บันทึก Tags สำเร็จ!")
    print("📌 Tags: team=data-science, version=v1.0, environment=development, dataset=iris, framework=sklearn")

# %% [markdown]
# ### 8.9 ตัวอย่างโค้ดสำหรับวิเคราะห์ผลการทดลอง

# %%
import pandas as pd

# ค้นหา Runs ทั้งหมดใน Experiment
runs = mlflow.search_runs(
    experiment_names=["mlflow-tracking-lab"],
    order_by=["metrics.accuracy DESC"],
    max_results=20
)

# แสดงสรุปผลการทดลอง
print("🏆 Top 5 Runs by Accuracy:")
print("=" * 80)

top_runs = runs.head(5)
for idx, row in top_runs.iterrows():
    run_name = row.get("tags.mlflow.runName", "N/A")
    accuracy = row.get("metrics.accuracy", 0)
    lr = row.get("params.learning_rate", "N/A")
    
    if pd.notna(accuracy):
        print(f"  {run_name:<30} | Accuracy: {accuracy:.4f} | LR: {lr}")
    else:
        print(f"  {run_name:<30} | Accuracy: N/A | LR: {lr}")

# วิเคราะห์ความสัมพันธ์ระหว่าง Parameters และ Metrics
print("\n📊 Analysis:")
if "params.learning_rate" in runs.columns and "metrics.accuracy" in runs.columns:
    # กรองเฉพาะ rows ที่มีค่า accuracy
    valid_runs = runs[runs["metrics.accuracy"].notna()]
    
    if len(valid_runs) > 0:
        # หา learning_rate ที่ให้ accuracy สูงสุด
        best_idx = valid_runs["metrics.accuracy"].idxmax()
        best_lr = valid_runs.loc[best_idx, "params.learning_rate"]
        best_acc = valid_runs.loc[best_idx, "metrics.accuracy"]
        
        print(f"  Best Learning Rate: {best_lr}")
        print(f"  Best Accuracy: {best_acc:.4f}")
    else:
        print("  ไม่พบข้อมูล accuracy ใน runs")

print(f"\n🔗 ดูรายละเอียดเพิ่มเติมได้ที่: http://127.0.0.1:8080")

# %% [markdown]
# ### 8.10 สรุปความสามารถ MLflow UI
# 
# | ฟีเจอร์ | คำอธิบาย | วิธีใช้งาน |
# |---------|----------|-----------|
# | **View Experiments** | ดูรายการ Experiments | คลิกที่ sidebar ซ้าย |
# | **View Runs** | ดูรายการ Runs | คลิกที่ Experiment |
# | **Run Details** | ดูรายละเอียด Run | คลิกที่ Run Name |
# | **Compare Runs** | เปรียบเทียบหลาย Runs | เลือก Runs แล้วกด Compare |
# | **View Metrics Graph** | ดูกราฟ Metrics | Tab Metrics ใน Run Detail |
# | **Download Artifacts** | ดาวน์โหลดไฟล์ | Tab Artifacts แล้วกด Download |
# | **Search & Filter** | ค้นหา Runs | ใช้ Search box |
# | **View Nested Runs** | ดู Parent-Child Runs | คลิกที่ Parent Run |

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
# ### Best Practices
# 
# #### 1. การตั้งชื่อ
# - ✅ ใช้ชื่อที่สื่อความหมาย: `fraud-detection-lstm-v2`
# - ❌ หลีกเลี่ยงชื่อทั่วไป: `test`, `experiment1`
# 
# #### 2. การบันทึก Parameters
# - บันทึกทุกค่าที่มีผลต่อผลลัพธ์
# - ใช้ `log_params()` สำหรับหลายค่าพร้อมกัน
# 
# #### 3. การบันทึก Metrics
# - บันทึกพร้อม `step` เพื่อติดตามการเปลี่ยนแปลง
# - บันทึกทั้ง training และ validation metrics
# 
# #### 4. การบันทึก Artifacts
# - บันทึก plots, configs และ models
# - จัดโครงสร้างโฟลเดอร์ให้ชัดเจน
# 
# #### 5. การบันทึก Model
# - ใช้ `signature` และ `input_example`
# - พิจารณาใช้ `autolog()` สำหรับความสะดวก
# 
# #### 6. การจัดระเบียบ
# - ใช้ Nested Runs สำหรับ Hyperparameter Tuning
# - ใช้ Tags เพื่อจัดกลุ่ม Runs

# %%
# ทำความสะอาดไฟล์ชั่วคราว
import shutil
if os.path.exists("outputs"):
    shutil.rmtree("outputs")
print("🧹 ทำความสะอาดไฟล์ชั่วคราวเรียบร้อย")

# %% [markdown]
# ---
# ## 🔗 แหล่งข้อมูลเพิ่มเติม
# 
# - [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
# - [MLflow Tracking Guide](https://mlflow.org/docs/latest/tracking.html)
# - [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
# - [MLflow Projects](https://mlflow.org/docs/latest/projects.html)
# 
# ---
# 
# *Lab นี้จัดทำขึ้นสำหรับการเรียนรู้ MLflow Tracking*