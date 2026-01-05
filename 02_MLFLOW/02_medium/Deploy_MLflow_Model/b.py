# %% [markdown]
# # 🚀 Lab: Deploy MLflow Model as a Local Inference Server
#
# **วัตถุประสงค์การเรียนรู้ (Learning Objectives)**
#
# เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:
# 1. เข้าใจแนวคิดของ MLflow Model Serving และ Model Registry
# 2. บันทึก (Log) โมเดล Scikit-learn และ PyTorch ลงใน MLflow
# 3. Deploy โมเดลเป็น REST API Server บน Local Machine
# 4. ทดสอบการเรียกใช้งานโมเดลผ่าน HTTP Request
# 5. เปรียบเทียบวิธีการ Deploy ระหว่าง Scikit-learn และ PyTorch
#
# **ความรู้พื้นฐานที่ต้องมี (Prerequisites)**
# - Python Programming
# - Machine Learning พื้นฐาน
# - REST API พื้นฐาน
# - Docker (ไม่จำเป็น แต่จะช่วยให้เข้าใจมากขึ้น)

# %% [markdown]
# ---
# ## 📚 Part 1: ทฤษฎีและแนวคิดพื้นฐาน (Theory & Concepts)
# ---

# %% [markdown]
# ### 1.1 MLflow Model คืออะไร?
#
# **MLflow Model** เป็น format มาตรฐานสำหรับการ package โมเดล Machine Learning 
# ที่ออกแบบมาเพื่อให้สามารถ deploy ได้หลากหลาย platform
#
# ```
# ┌─────────────────────────────────────────────────────────────┐
# │                     MLflow Model Format                      │
# ├─────────────────────────────────────────────────────────────┤
# │  📁 model/                                                   │
# │  ├── 📄 MLmodel          (metadata & flavors)               │
# │  ├── 📄 conda.yaml       (dependencies)                     │
# │  ├── 📄 requirements.txt (pip dependencies)                 │
# │  ├── 📄 python_env.yaml  (python version)                   │
# │  └── 📦 model.pkl / model.pt (serialized model)             │
# └─────────────────────────────────────────────────────────────┘
# ```
#
# **MLmodel file** เป็นไฟล์ YAML ที่บอกข้อมูลสำคัญ:
# - **Flavors**: บอกว่าโมเดลถูกสร้างจาก framework ใด (sklearn, pytorch, tensorflow, etc.)
# - **Signature**: Input/Output schema ของโมเดล
# - **Input Example**: ตัวอย่าง input สำหรับการทดสอบ

# %% [markdown]
# ### 1.2 Model Serving Architecture
#
# ```
#                           MLflow Model Serving Architecture
#
#     ┌──────────────┐         ┌──────────────────────┐         ┌──────────────┐
#     │              │  HTTP   │                      │  Load   │              │
#     │   Client     │────────▶│   MLflow Serving     │────────▶│    Model     │
#     │  (Request)   │         │   (REST API Server)  │         │  (Artifact)  │
#     │              │◀────────│                      │◀────────│              │
#     └──────────────┘  JSON   └──────────────────────┘ Predict └──────────────┘
#                               
#     📱 curl / Python         🖥️ Port 5001              📦 MLflow Model
#        requests                  /invocations              Format
# ```
#
# **กระบวนการทำงาน:**
# 1. Client ส่ง HTTP POST request พร้อม input data (JSON format)
# 2. MLflow Serving รับ request และ parse input
# 3. โมเดลทำการ predict
# 4. ส่ง prediction กลับเป็น JSON response

# %% [markdown]
# ### 1.3 Model Flavor คืออะไร?
#
# **Flavor** คือ convention ที่บอกว่าโมเดลถูก serialize และ deserialize อย่างไร
#
# | Flavor | Framework | การใช้งาน |
# |--------|-----------|-----------|
# | `sklearn` | Scikit-learn | Classification, Regression |
# | `pytorch` | PyTorch | Deep Learning |
# | `tensorflow` | TensorFlow/Keras | Deep Learning |
# | `xgboost` | XGBoost | Gradient Boosting |
# | `pyfunc` | Any Python | Custom models |
#
# **ทำไมต้องมี Flavor?**
# - แต่ละ framework มีวิธี save/load โมเดลต่างกัน
# - Flavor ช่วยให้ MLflow รู้วิธีจัดการโมเดลแต่ละแบบ
# - ทำให้ deployment เป็นมาตรฐานเดียวกัน

# %% [markdown]
# ### 1.4 REST API Endpoints
#
# เมื่อ deploy โมเดลด้วย `mlflow models serve` จะได้ endpoints ดังนี้:
#
# | Endpoint | Method | Description |
# |----------|--------|-------------|
# | `/invocations` | POST | ส่ง data เพื่อทำ prediction |
# | `/ping` | GET | Health check |
# | `/health` | GET | Health check (alternative) |
# | `/version` | GET | MLflow version |
#
# **Input Format สำหรับ /invocations:**
#
# ```json
# // Format 1: dataframe_split (แนะนำ)
# {
#     "dataframe_split": {
#         "columns": ["feature1", "feature2"],
#         "data": [[1.0, 2.0], [3.0, 4.0]]
#     }
# }
#
# // Format 2: dataframe_records
# {
#     "dataframe_records": [
#         {"feature1": 1.0, "feature2": 2.0},
#         {"feature1": 3.0, "feature2": 4.0}
#     ]
# }
#
# // Format 3: instances (TensorFlow style)
# {
#     "instances": [[1.0, 2.0], [3.0, 4.0]]
# }
# ```

# %% [markdown]
# ---
# ## 🔧 Part 2: Environment Setup
# ---

# %% [markdown]
# ### 2.1 ติดตั้ง Dependencies
#
# รันคำสั่งนี้ใน terminal หรือ notebook cell:

# %%
# ติดตั้ง packages ที่จำเป็น
# #!pip install mlflow scikit-learn torch pandas numpy requests

# %% [markdown]
# ### 2.2 Import Libraries

# %%
# Standard libraries
import os
import json
import time
import subprocess
import warnings
import yaml  # สำหรับอ่าน MLmodel file
warnings.filterwarnings('ignore')

# Data manipulation
import numpy as np
import pandas as pd

# Machine Learning
from sklearn.datasets import load_iris, load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Deep Learning
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# MLflow
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from mlflow.tracking import MlflowClient
from mlflow.models import infer_signature

# HTTP requests
import requests

print("✅ All libraries imported successfully!")
print(f"📦 MLflow version: {mlflow.__version__}")
print(f"📦 PyTorch version: {torch.__version__}")

# %% [markdown]
# ### 2.3 Setup MLflow Tracking Server
#
# **สำคัญ:** ก่อนรัน Lab นี้ ต้อง setup MLflow Tracking Server ก่อน
#
# #### Step 1: สร้างโฟลเดอร์สำหรับ Lab
# ```bash
# # 2.1 สร้างโฟลเดอร์สำหรับเก็บไฟล์ Lab
# mkdir -p /home/student/workspace/mlflowserver-lab
#
# # 2.2 เข้าไปในโฟลเดอร์
# cd /home/student/workspace/mlflowserver-lab
#
# # 2.3 สร้างโฟลเดอร์เก็บข้อมูล
# mkdir -p /home/student/workspace/mlflowserver-lab/mlruns_db
# mkdir -p /home/student/workspace/mlflowserver-lab/mlartifacts
# ```
#
# #### Step 2: Start MLflow Server
# ```bash
# # 2.4 เปิด Server ให้เข้าถึงได้จากทุก IP
# nohup mlflow server \
#   --host 0.0.0.0 --port 5000 \
#   --backend-store-uri sqlite:////home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db \
#   --artifacts-destination /home/student/workspace/mlflowserver-lab/mlartifacts \
#   --serve-artifacts > mlflow.log 2>&1 &
# ```
#
# #### ตรวจสอบ Server
# ```bash
# # ดู log
# tail -f mlflow.log
#
# # ตรวจสอบ process
# ps aux | grep mlflow
#
# # ทดสอบเชื่อมต่อ
# curl http://127.0.0.1:5000/health
# ```
#
# **Architecture:**
# ```
# /home/student/workspace/mlflowserver-lab/
# ├── mlruns_db/
# │   └── mlflow.db          <- Backend Store (SQLite)
# ├── mlartifacts/           <- Artifact Store
# │   └── {experiment_id}/
# │       └── {run_id}/
# │           └── artifacts/
# └── mlflow.log             <- Server Log
#
# ┌─────────────────┐      HTTP       ┌─────────────────────┐
# │   Jupyter Lab   │ ◄─────────────► │  MLflow Tracking    │
# │   (Client)      │   Port 5000     │  Server             │
# └─────────────────┘                 └─────────────────────┘
#                                              │
#                               ┌──────────────┴──────────────┐
#                               ▼                              ▼
#                     ┌─────────────────┐           ┌─────────────────┐
#                     │  Backend Store  │           │  Artifact Store │
#                     │  (SQLite DB)    │           │  (Local Files)  │
#                     └─────────────────┘           └─────────────────┘
# ```

# %%
# กำหนด MLflow Configuration
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "Model_Deployment_Lab"

# Paths (สำหรับอ้างอิง)
LAB_BASE_PATH = "/home/student/workspace/mlflowserver-lab"
MLRUNS_DB_PATH = f"{LAB_BASE_PATH}/mlruns_db"
ARTIFACTS_PATH = f"{LAB_BASE_PATH}/mlartifacts"

# เชื่อมต่อ MLflow Server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# สร้าง MlflowClient สำหรับ interact กับ server
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

# ตั้งค่า experiment
mlflow.set_experiment(EXPERIMENT_NAME)

print(f"📍 MLflow Tracking URI: {MLFLOW_TRACKING_URI}")
print(f"📁 Lab Base Path: {LAB_BASE_PATH}")
print(f"📁 Artifacts Path: {ARTIFACTS_PATH}")
print(f"🔬 Experiment: {EXPERIMENT_NAME}")

# %%
# ตรวจสอบการเชื่อมต่อ MLflow Server
print("🔍 ตรวจสอบการเชื่อมต่อ MLflow Server...")
print("-" * 50)

try:
    # ทดสอบเชื่อมต่อ
    response = requests.get(f"{MLFLOW_TRACKING_URI}/health", timeout=5)
    if response.status_code == 200:
        print("✅ MLflow Server is running!")
    
    # ดึงข้อมูล experiment
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment:
        print(f"📌 Experiment ID: {experiment.experiment_id}")
        print(f"📁 Artifact Location: {experiment.artifact_location}")
    else:
        print(f"📝 Creating new experiment: {EXPERIMENT_NAME}")
        
    # แสดง experiments ทั้งหมด
    print(f"\n📋 Available Experiments:")
    experiments = client.search_experiments()
    for exp in experiments:
        print(f"   - {exp.name} (ID: {exp.experiment_id})")
    
    # ตรวจสอบโฟลเดอร์
    print(f"\n📁 Directory Structure:")
    if os.path.exists(LAB_BASE_PATH):
        print(f"   ✅ {LAB_BASE_PATH}")
        if os.path.exists(MLRUNS_DB_PATH):
            print(f"   ✅ {MLRUNS_DB_PATH}")
        if os.path.exists(ARTIFACTS_PATH):
            print(f"   ✅ {ARTIFACTS_PATH}")
    else:
        print(f"   ⚠️ Lab directory not found: {LAB_BASE_PATH}")
        
except requests.exceptions.ConnectionError:
    print("❌ ไม่สามารถเชื่อมต่อ MLflow Server ได้!")
    print("💡 กรุณา start MLflow Server ด้วยคำสั่ง:")
    print()
    print("   # สร้างโฟลเดอร์")
    print("   mkdir -p /home/student/workspace/mlflowserver-lab/mlruns_db")
    print("   mkdir -p /home/student/workspace/mlflowserver-lab/mlartifacts")
    print()
    print("   # Start Server")
    print("   cd /home/student/workspace/mlflowserver-lab")
    print("   nohup mlflow server \\")
    print("     --host 0.0.0.0 --port 5000 \\")
    print("     --backend-store-uri sqlite:////home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db \\")
    print("     --artifacts-destination /home/student/workspace/mlflowserver-lab/mlartifacts \\")
    print("     --serve-artifacts > mlflow.log 2>&1 &")
except Exception as e:
    print(f"⚠️ Error: {e}")

# %% [markdown]
# ### 2.4 Helper Functions สำหรับค้นหา Model Path
#
# เมื่อใช้ MLflow Server กับ `--serve-artifacts` artifacts จะถูกเก็บในโครงสร้าง:
#
# ```
# /home/student/workspace/mlflowserver-lab/
# └── mlartifacts/
#     └── {experiment_id}/
#         └── {run_id}/
#             └── artifacts/
#                 └── {artifact_path}/
#                     ├── MLmodel
#                     ├── model.pkl (sklearn)
#                     └── data/ (pytorch)
# ```

# %%
def get_experiment_id(experiment_name: str) -> str:
    """ดึง experiment ID จากชื่อ experiment"""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment:
        return experiment.experiment_id
    return None


def get_artifact_base_path() -> str:
    """ดึง artifact base path จาก experiment"""
    return ARTIFACTS_PATH


def find_model_path_by_run_id(run_id: str, artifact_path: str = "sklearn_model") -> str:
    """
    ค้นหา model path จาก run_id
    
    Args:
        run_id: MLflow Run ID
        artifact_path: Path ของ artifact ที่ log ไว้
    
    Returns:
        Full path หรือ Model URI
    """
    return f"runs:/{run_id}/{artifact_path}"


def find_model_path_local(experiment_id: str, run_id: str, artifact_name: str = "sklearn_model") -> str:
    """
    ค้นหา model path จาก local artifacts folder
    
    Args:
        experiment_id: Experiment ID
        run_id: Run ID
        artifact_name: ชื่อ artifact (sklearn_model, pytorch_model, etc.)
    
    Returns:
        Local path ไปยัง model
    """
    model_path = f"{ARTIFACTS_PATH}/{experiment_id}/{run_id}/artifacts/{artifact_name}"
    if os.path.exists(model_path):
        return model_path
    return None


def find_models_by_flavor_from_server(experiment_name: str, flavor: str = "sklearn") -> list:
    """
    ค้นหา models จาก MLflow Server ตาม flavor
    
    Args:
        experiment_name: ชื่อ experiment
        flavor: MLflow flavor ("sklearn", "pytorch", etc.)
    
    Returns:
        List ของ model info
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        return []
    
    # ค้นหา runs ทั้งหมดใน experiment
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"]
    )
    
    found_models = []
    for run in runs:
        run_id = run.info.run_id
        
        # ลองโหลด model info
        try:
            # กำหนด artifact paths ที่เป็นไปได้
            possible_paths = [
                f"runs:/{run_id}/sklearn_model",
                f"runs:/{run_id}/pytorch_model",
                f"runs:/{run_id}/model"
            ]
            
            for model_uri in possible_paths:
                try:
                    model_info = mlflow.models.get_model_info(model_uri)
                    if flavor in model_info.flavors:
                        # หา local path ด้วย
                        artifact_name = model_uri.split("/")[-1]
                        local_path = find_model_path_local(
                            experiment.experiment_id, 
                            run_id, 
                            artifact_name
                        )
                        
                        found_models.append({
                            'run_id': run_id,
                            'run_name': run.info.run_name,
                            'model_uri': model_uri,
                            'local_path': local_path,
                            'flavors': list(model_info.flavors.keys()),
                            'status': run.info.status
                        })
                        break
                except:
                    continue
        except Exception as e:
            continue
    
    return found_models


def find_models_by_flavor_local(experiment_id: str, flavor: str = "sklearn") -> list:
    """
    ค้นหา models จาก local artifacts folder ตาม flavor
    
    Args:
        experiment_id: Experiment ID
        flavor: MLflow flavor ("sklearn", "pytorch", etc.)
    
    Returns:
        List ของ model info
    """
    experiment_path = f"{ARTIFACTS_PATH}/{experiment_id}"
    found_models = []
    
    if not os.path.exists(experiment_path):
        print(f"⚠️ ไม่พบโฟลเดอร์: {experiment_path}")
        return found_models
    
    # วนหา run folders
    for run_id in os.listdir(experiment_path):
        run_path = f"{experiment_path}/{run_id}"
        if not os.path.isdir(run_path):
            continue
            
        artifacts_path = f"{run_path}/artifacts"
        if not os.path.exists(artifacts_path):
            continue
        
        # วนหา artifact folders (sklearn_model, pytorch_model, etc.)
        for artifact_name in os.listdir(artifacts_path):
            model_path = f"{artifacts_path}/{artifact_name}"
            mlmodel_file = f"{model_path}/MLmodel"
            
            if os.path.exists(mlmodel_file):
                with open(mlmodel_file, 'r') as f:
                    mlmodel = yaml.safe_load(f)
                
                if 'flavors' in mlmodel and flavor in mlmodel['flavors']:
                    found_models.append({
                        'run_id': run_id,
                        'artifact_name': artifact_name,
                        'local_path': model_path,
                        'model_uri': f"runs:/{run_id}/{artifact_name}",
                        'flavors': list(mlmodel['flavors'].keys())
                    })
    
    return found_models


def list_registered_models():
    """แสดง registered models ทั้งหมด"""
    try:
        registered_models = client.search_registered_models()
        return registered_models
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []


print("✅ Helper functions defined successfully!")

# %% [markdown]
# ---
# ## 🌲 Part 3: Scikit-learn Model Deployment
# ---

# %% [markdown]
# ### 3.1 เตรียมข้อมูล Iris Dataset
#
# **Iris Dataset** เป็น dataset มาตรฐานสำหรับการเรียนรู้ Classification
# - 150 samples
# - 4 features: sepal length, sepal width, petal length, petal width
# - 3 classes: setosa, versicolor, virginica

# %%
# Load Iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

# แสดงข้อมูลเบื้องต้น
print("📊 Dataset Info:")
print(f"   Shape: {X.shape}")
print(f"   Features: {list(X.columns)}")
print(f"   Classes: {list(iris.target_names)}")
print()
print("📋 Sample data:")
X.head()

# %%
# แบ่งข้อมูล train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✂️ Train set: {X_train.shape[0]} samples")
print(f"✂️ Test set: {X_test.shape[0]} samples")

# %% [markdown]
# ### 3.2 Train และ Log Scikit-learn Model
#
# **ขั้นตอนการ Log Model:**
# 1. เริ่ม MLflow run
# 2. Train model
# 3. Log parameters, metrics
# 4. สร้าง signature และ input example
# 5. Log model ด้วย `mlflow.sklearn.log_model()`

# %%
# Train และ Log RandomForest model
with mlflow.start_run(run_name="sklearn_randomforest") as run:
    
    # กำหนด hyperparameters
    n_estimators = 100
    max_depth = 5
    random_state = 42
    
    # Log parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("model_type", "RandomForestClassifier")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    
    # สร้าง signature (บอก input/output schema)
    signature = infer_signature(X_train, model.predict(X_train))
    
    # สร้าง input example สำหรับการทดสอบ
    input_example = X_train.head(3)
    
    # Log model พร้อม signature และ input example
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="sklearn_model",
        signature=signature,
        input_example=input_example,
        registered_model_name="iris_classifier_sklearn"  # Register model ด้วย
    )
    
    # เก็บ run_id สำหรับใช้ deploy
    sklearn_run_id = run.info.run_id
    
    # ============================================
    # FIX: ใช้ runs:/ URI แทน models:/ URI
    # เพราะ runs:/ URI ใช้งานได้กว้างกว่า
    # ============================================
    sklearn_model_uri = f"runs:/{sklearn_run_id}/sklearn_model"
    
    print("=" * 60)
    print("✅ Scikit-learn Model Logged Successfully!")
    print("=" * 60)
    print(f"📌 Run ID: {sklearn_run_id}")
    print(f"📦 Model URI (runs:/): {sklearn_model_uri}")
    print(f"📦 Model URI (models:/): models:/iris_classifier_sklearn/1")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print()
    print("📋 Model Signature:")
    print(signature)

# %% [markdown]
# ### 3.3 ตรวจสอบ Model Artifacts
#
# ดูโครงสร้างไฟล์ที่ MLflow สร้างขึ้น:

# %%
# แสดง model URI
print(f"📦 Model URI: {sklearn_model_uri}")
print()

# Load และตรวจสอบ model info
model_info = mlflow.models.get_model_info(sklearn_model_uri)
print("📋 Model Info:")
print(f"   Flavors: {list(model_info.flavors.keys())}")
print(f"   Run ID: {model_info.run_id}")
print()

# แสดง MLmodel file content
print("📄 MLmodel file content:")

# ============================================
# FIX: ใช้ runs:/ URI สำหรับ download_artifacts
# แทนที่จะใช้ models:/ URI ที่อาจทำให้เกิด error
# ============================================
try:
    # วิธีที่ 1: ใช้ runs:/ URI (แนะนำ)
    mlmodel_path = mlflow.artifacts.download_artifacts(sklearn_model_uri + "/MLmodel")
    with open(mlmodel_path, 'r') as f:
        print(f.read())
except Exception as e:
    print(f"⚠️ Method 1 (runs:/ URI) failed: {e}")
    
    # วิธีที่ 2: ใช้ local path โดยตรง
    try:
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        local_mlmodel_path = f"{ARTIFACTS_PATH}/{experiment.experiment_id}/{sklearn_run_id}/artifacts/sklearn_model/MLmodel"
        
        if os.path.exists(local_mlmodel_path):
            print(f"\n📁 Using local path: {local_mlmodel_path}")
            with open(local_mlmodel_path, 'r') as f:
                print(f.read())
        else:
            print(f"⚠️ Local path not found: {local_mlmodel_path}")
            
            # วิธีที่ 3: แสดงข้อมูลจาก model_info แทน
            print("\n📋 Alternative: Showing MLmodel info from API:")
            print(f"   Model URI: {model_info.model_uri}")
            print(f"   Flavors: {model_info.flavors}")
            if model_info.signature:
                print(f"   Signature Inputs: {model_info.signature.inputs}")
                print(f"   Signature Outputs: {model_info.signature.outputs}")
    except Exception as e2:
        print(f"⚠️ Method 2 (local path) also failed: {e2}")
        print("\n📋 Showing available model info:")
        print(f"   Run ID: {sklearn_run_id}")
        print(f"   Flavors: {list(model_info.flavors.keys())}")

# %% [markdown]
# ### 3.4 Test Model Locally (ก่อน Deploy)
#
# มี 2 วิธีในการ load model จาก MLflow Server:
# 1. **จาก Model URI** - ใช้ `runs:/<run_id>/<artifact_path>`
# 2. **จาก Registered Model** - ใช้ `models:/<model_name>/<version>`

# %%
# วิธีที่ 1: Load model จาก Model URI (runs:/)
print("🧪 วิธีที่ 1: Load จาก Model URI (runs:/)")
print("-" * 50)
print(f"📦 Model URI: {sklearn_model_uri}")

loaded_model_uri = mlflow.sklearn.load_model(sklearn_model_uri)

test_data = X_test.head(5)
predictions = loaded_model_uri.predict(test_data)

for i, (idx, row) in enumerate(test_data.iterrows()):
    pred_class = iris.target_names[predictions[i]]
    actual_class = iris.target_names[y_test.iloc[i]]
    status = "✅" if predictions[i] == y_test.iloc[i] else "❌"
    print(f"   Sample {i+1}: Predicted={pred_class}, Actual={actual_class} {status}")

# %%
# วิธีที่ 2: Load model จาก Registered Model Name
print("\n🧪 วิธีที่ 2: Load จาก Registered Model (models:/)")
print("-" * 50)

registered_model_uri = "models:/iris_classifier_sklearn/1"
print(f"📦 Registered Model URI: {registered_model_uri}")

try:
    loaded_registered_model = mlflow.sklearn.load_model(registered_model_uri)
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_registered_model)}")
    
    # ทดสอบทำนาย
    predictions = loaded_registered_model.predict(X_test[:5])
    print(f"\n🔮 ทดสอบทำนาย 5 ตัวอย่างแรก:")
    print(f"   Predictions: {predictions}")
    print(f"   Actual:      {y_test[:5].values}")
except Exception as e:
    print(f"⚠️ Error loading registered model: {e}")
    print("💡 Model อาจยังไม่ได้ register หรือ version ไม่ถูกต้อง")
    print(f"💡 ใช้ runs:/ URI แทน: {sklearn_model_uri}")

# %%
# ค้นหา sklearn models ทั้งหมดจาก MLflow Server
print("\n📋 ค้นหา Sklearn Models จาก MLflow Server:")
print("-" * 50)

sklearn_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="sklearn")
for i, model in enumerate(sklearn_models, 1):
    print(f"   {i}. Run: {model['run_name']} ({model['run_id'][:8]}...)")
    print(f"      URI: {model['model_uri']}")
    if model.get('local_path'):
        print(f"      Local: {model['local_path']}")
    print(f"      Flavors: {model['flavors']}")
    print(f"      Status: {model['status']}")

# %%
# ค้นหา sklearn models จาก local artifacts folder
print("\n📋 ค้นหา Sklearn Models จาก Local Artifacts:")
print("-" * 50)

experiment_id = get_experiment_id(EXPERIMENT_NAME)
if experiment_id:
    local_sklearn_models = find_models_by_flavor_local(experiment_id, flavor="sklearn")
    for i, model in enumerate(local_sklearn_models, 1):
        print(f"   {i}. Run ID: {model['run_id'][:8]}...")
        print(f"      Local Path: {model['local_path']}")
        print(f"      Model URI: {model['model_uri']}")
        print(f"      Flavors: {model['flavors']}")

# %% [markdown]
# ### 3.5 Deploy Scikit-learn Model as REST API
#
# **วิธีการ Deploy:**
#
# ```bash
# mlflow models serve -m <model_uri> -p <port> --no-conda
# ```
#
# **Parameters:**
# - `-m`: Model URI (runs:/<run_id>/model หรือ models:/<name>/<version>)
# - `-p`: Port number
# - `--no-conda`: ไม่ใช้ conda environment (ใช้ current environment)
# - `--host`: Host address (default: 127.0.0.1)

# %%
# แสดงคำสั่ง deploy
print("🚀 Deploy Scikit-learn Model")
print("=" * 60)
print()
print("📋 รันคำสั่งนี้ใน Terminal แยกต่างหาก:")
print()
print("# วิธีที่ 1: ใช้ runs:/ URI (แนะนำ)")
print(f'mlflow models serve -m "{sklearn_model_uri}" -p 5001 --no-conda')
print()
print("# วิธีที่ 2: ใช้ registered model name")
print('mlflow models serve -m "models:/iris_classifier_sklearn/1" -p 5001 --no-conda')
print()
print("=" * 60)
print("⏳ รอให้ server start แล้วค่อยรัน cell ถัดไป...")
print("   (จะเห็นข้อความ 'Listening at: http://127.0.0.1:5001')")

# %% [markdown]
# ### 3.6 ทดสอบ REST API (Scikit-learn)
#
# **หลังจาก server start แล้ว** รัน cell นี้เพื่อทดสอบ:

# %%
def test_sklearn_api(port=5001):
    """ทดสอบ REST API สำหรับ Scikit-learn model"""
    
    base_url = f"http://127.0.0.1:{port}"
    
    # Test 1: Health check
    print("🔍 Test 1: Health Check")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed! Make sure server is running.")
        return
    
    # Test 2: Prediction with dataframe_split format
    print()
    print("🔍 Test 2: Prediction (dataframe_split format)")
    print("-" * 40)
    
    # เตรียม test data
    test_samples = X_test.head(3).values.tolist()
    
    payload = {
        "dataframe_split": {
            "columns": list(X.columns),
            "data": test_samples
        }
    }
    
    print(f"   📤 Request payload:")
    print(f"      {json.dumps(payload, indent=6)}")
    
    response = requests.post(
        f"{base_url}/invocations",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    print()
    print(f"   📥 Response:")
    print(f"      Status: {response.status_code}")
    print(f"      Predictions: {response.json()}")
    
    # แปลง predictions เป็นชื่อ class
    predictions = response.json()['predictions']
    print()
    print("   📊 Prediction Results:")
    for i, pred in enumerate(predictions):
        print(f"      Sample {i+1}: {iris.target_names[pred]}")
    
    # Test 3: Prediction with instances format
    print()
    print("🔍 Test 3: Prediction (instances format)")
    print("-" * 40)
    
    payload_instances = {
        "instances": test_samples
    }
    
    response = requests.post(
        f"{base_url}/invocations",
        headers={"Content-Type": "application/json"},
        json=payload_instances
    )
    
    print(f"   📥 Response: {response.json()}")
    
    print()
    print("✅ All API tests completed!")

# เรียกใช้ function ทดสอบ
# ⚠️ Uncomment บรรทัดด้านล่างหลังจาก start server แล้ว
# test_sklearn_api(5001)

# %% [markdown]
# ### 3.7 ทดสอบด้วย curl command
#
# สามารถทดสอบด้วย curl ใน terminal ได้:
#
# ```bash
# # Health check
# curl http://127.0.0.1:5001/health
#
# # Prediction
# curl -X POST http://127.0.0.1:5001/invocations \
#      -H "Content-Type: application/json" \
#      -d '{"dataframe_split": {"columns": ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"], "data": [[5.1, 3.5, 1.4, 0.2]]}}'
# ```

# %% [markdown]
# ---
# ## 🔥 Part 4: PyTorch Model Deployment
# ---

# %% [markdown]
# ### 4.1 เตรียมข้อมูล Wine Dataset
#
# **Wine Dataset** เป็น dataset สำหรับ classification
# - 178 samples
# - 13 features (chemical analysis)
# - 3 classes (wine types)

# %%
# Load Wine dataset
wine = load_wine()
X_wine = pd.DataFrame(wine.data, columns=wine.feature_names)
y_wine = wine.target

# Normalize features (สำคัญมากสำหรับ Neural Network)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_wine_scaled = scaler.fit_transform(X_wine)

print("📊 Wine Dataset Info:")
print(f"   Shape: {X_wine.shape}")
print(f"   Features: {len(wine.feature_names)} features")
print(f"   Classes: {list(wine.target_names)}")
print()
print("📋 Sample features:")
print(f"   {wine.feature_names[:5]}...")

# %%
# แบ่ง train/test
X_train_wine, X_test_wine, y_train_wine, y_test_wine = train_test_split(
    X_wine_scaled, y_wine, test_size=0.2, random_state=42, stratify=y_wine
)

# แปลงเป็น PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train_wine)
y_train_tensor = torch.LongTensor(y_train_wine)
X_test_tensor = torch.FloatTensor(X_test_wine)
y_test_tensor = torch.LongTensor(y_test_wine)

# สร้าง DataLoader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

print(f"✂️ Train set: {X_train_tensor.shape[0]} samples")
print(f"✂️ Test set: {X_test_tensor.shape[0]} samples")
print(f"📦 Tensor shapes: X={X_train_tensor.shape}, y={y_train_tensor.shape}")

# %% [markdown]
# ### 4.2 สร้าง Neural Network Model
#
# **โครงสร้าง Network:**
# ```
# Input (13 features)
#     ↓
# Linear(13, 64) + ReLU + Dropout(0.3)
#     ↓
# Linear(64, 32) + ReLU + Dropout(0.3)
#     ↓
# Linear(32, 3) → Output (3 classes)
# ```

# %%
class WineClassifier(nn.Module):
    """Neural Network สำหรับ Wine Classification"""
    
    def __init__(self, input_dim=13, hidden1=64, hidden2=32, output_dim=3):
        super(WineClassifier, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden2, output_dim)
        )
    
    def forward(self, x):
        return self.network(x)

# สร้าง model instance
pytorch_model = WineClassifier()
print("🏗️ Model Architecture:")
print(pytorch_model)
print()
print(f"📊 Total parameters: {sum(p.numel() for p in pytorch_model.parameters()):,}")

# %% [markdown]
# ### 4.3 Train PyTorch Model

# %%
def train_pytorch_model(model, train_loader, X_test, y_test, epochs=100, lr=0.001):
    """Train PyTorch model และ return metrics"""
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    history = {'loss': [], 'accuracy': []}
    
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        
        # Evaluate
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test)
            _, predicted = torch.max(test_outputs, 1)
            accuracy = (predicted == y_test).sum().item() / len(y_test)
        model.train()
        
        history['loss'].append(epoch_loss / len(train_loader))
        history['accuracy'].append(accuracy)
        
        if (epoch + 1) % 20 == 0:
            print(f"   Epoch [{epoch+1}/{epochs}] Loss: {epoch_loss/len(train_loader):.4f}, Acc: {accuracy:.4f}")
    
    return history

# Train model
print("🏋️ Training PyTorch Model...")
print("-" * 40)
history = train_pytorch_model(
    pytorch_model, train_loader, 
    X_test_tensor, y_test_tensor,
    epochs=100, lr=0.001
)

print("-" * 40)
print(f"✅ Training completed! Final accuracy: {history['accuracy'][-1]:.4f}")

# %% [markdown]
# ### 4.4 Log PyTorch Model to MLflow
#
# **ความแตกต่างจาก Scikit-learn:**
# - ใช้ `mlflow.pytorch.log_model()` แทน `mlflow.sklearn.log_model()`
# - ต้องระบุ input signature อย่างชัดเจน
# - สามารถ log เป็น scripted model หรือ regular model

# %%
# Log PyTorch model to MLflow
with mlflow.start_run(run_name="pytorch_wine_classifier") as run:
    
    # Log parameters
    mlflow.log_param("model_type", "Neural Network")
    mlflow.log_param("hidden1", 64)
    mlflow.log_param("hidden2", 32)
    mlflow.log_param("epochs", 100)
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("optimizer", "Adam")
    
    # Log metrics
    mlflow.log_metric("final_accuracy", history['accuracy'][-1])
    mlflow.log_metric("final_loss", history['loss'][-1])
    
    # Log training history
    for i, (loss, acc) in enumerate(zip(history['loss'], history['accuracy'])):
        mlflow.log_metric("train_loss", loss, step=i)
        mlflow.log_metric("train_accuracy", acc, step=i)
    
    # เตรียม input example
    input_example = X_test_tensor[:3].numpy()
    
    # สร้าง signature
    # สำหรับ PyTorch ต้องใช้ numpy array ในการ infer signature
    pytorch_model.eval()
    with torch.no_grad():
        sample_output = pytorch_model(X_test_tensor[:3]).numpy()
    
    signature = infer_signature(input_example, sample_output)
    
    # Log model
    model_info = mlflow.pytorch.log_model(
        pytorch_model=pytorch_model,
        artifact_path="pytorch_model",
        signature=signature,
        input_example=input_example,
        registered_model_name="wine_classifier_pytorch"
    )
    
    pytorch_run_id = run.info.run_id
    
    # ============================================
    # FIX: ใช้ runs:/ URI แทน models:/ URI
    # ============================================
    pytorch_model_uri = f"runs:/{pytorch_run_id}/pytorch_model"
    
    print("=" * 60)
    print("✅ PyTorch Model Logged Successfully!")
    print("=" * 60)
    print(f"📌 Run ID: {pytorch_run_id}")
    print(f"📦 Model URI (runs:/): {pytorch_model_uri}")
    print(f"📦 Model URI (models:/): models:/wine_classifier_pytorch/1")
    print(f"📊 Final Accuracy: {history['accuracy'][-1]:.4f}")
    print()
    print("📋 Model Signature:")
    print(signature)

# %% [markdown]
# ### 4.5 Test PyTorch Model Locally
#
# เช่นเดียวกับ Scikit-learn สามารถ load PyTorch model จาก MLflow Server ได้:

# %%
# วิธีที่ 1: Load จาก Model URI
print("🧪 วิธีที่ 1: Load PyTorch Model จาก Model URI (runs:/)")
print("-" * 50)
print(f"📦 Model URI: {pytorch_model_uri}")

loaded_pytorch_model = mlflow.pytorch.load_model(pytorch_model_uri)
loaded_pytorch_model.eval()

with torch.no_grad():
    test_input = X_test_tensor[:5]
    outputs = loaded_pytorch_model(test_input)
    _, predictions = torch.max(outputs, 1)

for i in range(5):
    pred_class = wine.target_names[predictions[i]]
    actual_class = wine.target_names[y_test_tensor[i]]
    status = "✅" if predictions[i] == y_test_tensor[i] else "❌"
    print(f"   Sample {i+1}: Predicted={pred_class}, Actual={actual_class} {status}")

# %%
# วิธีที่ 2: Load จาก Registered Model
print("\n🧪 วิธีที่ 2: Load PyTorch Model จาก Registered Model (models:/)")
print("-" * 50)

registered_pytorch_uri = "models:/wine_classifier_pytorch/1"
print(f"📦 Registered Model URI: {registered_pytorch_uri}")

try:
    loaded_pt_registered = mlflow.pytorch.load_model(registered_pytorch_uri)
    loaded_pt_registered.eval()
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_pt_registered)}")
    
    # ทดสอบทำนาย
    with torch.no_grad():
        test_input = X_test_tensor[:5]
        outputs = loaded_pt_registered(test_input)
        _, predictions = torch.max(outputs, 1)
    
    print(f"\n🔮 ทดสอบทำนาย 5 ตัวอย่างแรก:")
    print(f"   Predictions: {predictions.numpy()}")
    print(f"   Actual:      {y_test_tensor[:5].numpy()}")
except Exception as e:
    print(f"⚠️ Error loading registered model: {e}")
    print("💡 Model อาจยังไม่ได้ register หรือ version ไม่ถูกต้อง")
    print(f"💡 ใช้ runs:/ URI แทน: {pytorch_model_uri}")

# %%
# ค้นหา pytorch models ทั้งหมดจาก MLflow Server
print("\n📋 ค้นหา PyTorch Models จาก MLflow Server:")
print("-" * 50)

pytorch_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="pytorch")
for i, model in enumerate(pytorch_models, 1):
    print(f"   {i}. Run: {model['run_name']} ({model['run_id'][:8]}...)")
    print(f"      URI: {model['model_uri']}")
    if model.get('local_path'):
        print(f"      Local: {model['local_path']}")
    print(f"      Flavors: {model['flavors']}")
    print(f"      Status: {model['status']}")

# %%
# ค้นหา pytorch models จาก local artifacts folder
print("\n📋 ค้นหา PyTorch Models จาก Local Artifacts:")
print("-" * 50)

experiment_id = get_experiment_id(EXPERIMENT_NAME)
if experiment_id:
    local_pytorch_models = find_models_by_flavor_local(experiment_id, flavor="pytorch")
    for i, model in enumerate(local_pytorch_models, 1):
        print(f"   {i}. Run ID: {model['run_id'][:8]}...")
        print(f"      Local Path: {model['local_path']}")
        print(f"      Model URI: {model['model_uri']}")
        print(f"      Flavors: {model['flavors']}")

# %% [markdown]
# ### 4.6 Deploy PyTorch Model as REST API
#
# **หมายเหตุ:** PyTorch model ต้องใช้ pyfunc flavor ในการ serve

# %%
print("🚀 Deploy PyTorch Model")
print("=" * 60)
print()
print("📋 รันคำสั่งนี้ใน Terminal แยกต่างหาก:")
print()
print("# วิธีที่ 1: ใช้ runs:/ URI (แนะนำ)")
print(f'mlflow models serve -m "{pytorch_model_uri}" -p 5002 --no-conda')
print()
print("# วิธีที่ 2: ใช้ registered model name")
print('mlflow models serve -m "models:/wine_classifier_pytorch/1" -p 5002 --no-conda')
print()
print("=" * 60)
print("⏳ รอให้ server start แล้วค่อยรัน cell ถัดไป...")

# %% [markdown]
# ### 4.7 ทดสอบ REST API (PyTorch)

# %%
def test_pytorch_api(port=5002):
    """ทดสอบ REST API สำหรับ PyTorch model"""
    
    base_url = f"http://127.0.0.1:{port}"
    
    # Test 1: Health check
    print("🔍 Test 1: Health Check")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed! Make sure server is running.")
        return
    
    # Test 2: Prediction
    print()
    print("🔍 Test 2: Prediction")
    print("-" * 40)
    
    # เตรียม test data (ใช้ scaled data)
    test_samples = X_test_wine[:3].tolist()
    
    payload = {
        "instances": test_samples
    }
    
    print(f"   📤 Sending {len(test_samples)} samples...")
    
    response = requests.post(
        f"{base_url}/invocations",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    print(f"   📥 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   📊 Raw output shape: {len(result['predictions'])} x {len(result['predictions'][0])}")
        
        # แปลง logits เป็น class predictions
        predictions = np.argmax(result['predictions'], axis=1)
        print()
        print("   📊 Prediction Results:")
        for i, pred in enumerate(predictions):
            actual = y_test_wine[i]
            status = "✅" if pred == actual else "❌"
            print(f"      Sample {i+1}: {wine.target_names[pred]} (actual: {wine.target_names[actual]}) {status}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    print()
    print("✅ PyTorch API test completed!")

# เรียกใช้ function ทดสอบ
# ⚠️ Uncomment บรรทัดด้านล่างหลังจาก start server แล้ว
# test_pytorch_api(5002)

# %% [markdown]
# ---
# ## 📊 Part 5: Load Models จาก MLflow Server (Session Restart)
# ---

# %% [markdown]
# ### 5.1 เมื่อ Restart Session
#
# เมื่อ restart Jupyter session สามารถ load model จาก MLflow Server ได้หลายวิธี:
#
# **วิธีที่ 1: ใช้ Run ID (แนะนำ)**
# ```python
# model_uri = f"runs:/{run_id}/sklearn_model"
# model = mlflow.sklearn.load_model(model_uri)
# ```
#
# **วิธีที่ 2: ใช้ Registered Model Name**
# ```python
# model_uri = "models:/iris_classifier_sklearn/1"
# model = mlflow.sklearn.load_model(model_uri)
# ```
#
# **วิธีที่ 3: ค้นหาจาก MLflow Server**
# ```python
# models = find_models_by_flavor_from_server(experiment_name, "sklearn")
# model = mlflow.sklearn.load_model(models[0]['model_uri'])
# ```

# %%
# ตัวอย่าง: Reconnect และ Load model หลังจาก restart session
print("🔄 Reconnect to MLflow Server After Session Restart")
print("=" * 60)

# Step 1: Reconnect to MLflow Server
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "Model_Deployment_Lab"
LAB_BASE_PATH = "/home/student/workspace/mlflowserver-lab"
ARTIFACTS_PATH = f"{LAB_BASE_PATH}/mlartifacts"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

print(f"📍 Connected to: {MLFLOW_TRACKING_URI}")
print(f"📁 Artifacts Path: {ARTIFACTS_PATH}")

# Step 2: ดึงข้อมูล experiment
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment:
    print(f"📌 Experiment ID: {experiment.experiment_id}")
    
    # Step 3: ค้นหา runs ล่าสุด
    print("\n📋 Recent Runs:")
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=5
    )
    
    for run in runs:
        print(f"   - {run.info.run_name} ({run.info.run_id[:8]}...)")
        print(f"     Status: {run.info.status}")
        print(f"     Started: {run.info.start_time}")
else:
    print("⚠️ Experiment not found. Please run training cells first.")

# %%
# ค้นหาและ load sklearn model
print("\n📥 Loading Scikit-learn Model from Server...")
print("-" * 50)

sklearn_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="sklearn")

if sklearn_models:
    # ใช้ model ล่าสุด
    latest_sklearn = sklearn_models[0]
    print(f"📦 Found: {latest_sklearn['run_name']}")
    print(f"   URI: {latest_sklearn['model_uri']}")
    
    sklearn_model_reloaded = mlflow.sklearn.load_model(latest_sklearn['model_uri'])
    print(f"✅ Loaded: {type(sklearn_model_reloaded).__name__}")
else:
    print("⚠️ No sklearn models found")

# %%
# ค้นหาและ load pytorch model
print("\n📥 Loading PyTorch Model from Server...")
print("-" * 50)

pytorch_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="pytorch")

if pytorch_models:
    # ใช้ model ล่าสุด
    latest_pytorch = pytorch_models[0]
    print(f"📦 Found: {latest_pytorch['run_name']}")
    print(f"   URI: {latest_pytorch['model_uri']}")
    
    pytorch_model_reloaded = mlflow.pytorch.load_model(latest_pytorch['model_uri'])
    pytorch_model_reloaded.eval()
    print(f"✅ Loaded: {type(pytorch_model_reloaded).__name__}")
else:
    print("⚠️ No pytorch models found")

# %% [markdown]
# ### 5.2 แสดง Registered Models
#
# ดู models ทั้งหมดที่ register ไว้ใน Model Registry:

# %%
print("📋 Registered Models in Model Registry:")
print("=" * 60)

registered_models = list_registered_models()

if registered_models:
    for rm in registered_models:
        print(f"\n📦 {rm.name}")
        # ดึง versions
        versions = client.search_model_versions(f"name='{rm.name}'")
        for v in versions:
            print(f"   Version {v.version}: {v.current_stage}")
            print(f"   Run ID: {v.run_id[:8]}...")
            print(f"   URI: models:/{rm.name}/{v.version}")
else:
    print("   No registered models found")

# %% [markdown]
# ### 5.3 Deploy Commands สำหรับ Models จาก Server

# %%
print("🚀 Deploy Commands")
print("=" * 60)

experiment_id = get_experiment_id(EXPERIMENT_NAME)

# Sklearn
sklearn_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="sklearn")
if sklearn_models:
    print("\n📋 Deploy Scikit-learn Model:")
    print()
    print("   # วิธีที่ 1: Using Run URI (แนะนำ - ผ่าน MLflow Server)")
    print(f'   mlflow models serve -m "{sklearn_models[0]["model_uri"]}" -p 5001 --no-conda')
    print()
    print("   # วิธีที่ 2: Using Registered Model")
    print('   mlflow models serve -m "models:/iris_classifier_sklearn/1" -p 5001 --no-conda')
    
    if sklearn_models[0].get('local_path'):
        print()
        print("   # วิธีที่ 3: Using Local Path (Direct)")
        print(f'   mlflow models serve -m "{sklearn_models[0]["local_path"]}" -p 5001 --no-conda')

# PyTorch
pytorch_models = find_models_by_flavor_from_server(EXPERIMENT_NAME, flavor="pytorch")
if pytorch_models:
    print("\n📋 Deploy PyTorch Model:")
    print()
    print("   # วิธีที่ 1: Using Run URI (แนะนำ - ผ่าน MLflow Server)")
    print(f'   mlflow models serve -m "{pytorch_models[0]["model_uri"]}" -p 5002 --no-conda')
    print()
    print("   # วิธีที่ 2: Using Registered Model")
    print('   mlflow models serve -m "models:/wine_classifier_pytorch/1" -p 5002 --no-conda')
    
    if pytorch_models[0].get('local_path'):
        print()
        print("   # วิธีที่ 3: Using Local Path (Direct)")
        print(f'   mlflow models serve -m "{pytorch_models[0]["local_path"]}" -p 5002 --no-conda')

print()
print("=" * 60)
print("💡 Tips:")
print("   - วิธีที่ 1 (runs:/) แนะนำเพราะทำงานได้เสถียรกว่า")
print("   - วิธีที่ 2 (models:/) ต้องมี model registered ก่อน")
print("   - วิธีที่ 3 ใช้ local path โดยตรง ไม่ต้องมี Server")
print(f"   - Artifacts อยู่ที่: {ARTIFACTS_PATH}")

# %% [markdown]
# ---
# ## 📊 Part 6: เปรียบเทียบและสรุป
# ---

# %% [markdown]
# ### 6.1 เปรียบเทียบ Scikit-learn vs PyTorch Deployment
#
# | Feature | Scikit-learn | PyTorch |
# |---------|--------------|---------|
# | **Log Function** | `mlflow.sklearn.log_model()` | `mlflow.pytorch.log_model()` |
# | **Model Format** | pickle (.pkl) | PyTorch state dict |
# | **Flavor** | sklearn, pyfunc | pytorch, pyfunc |
# | **Input Format** | DataFrame, numpy | Tensor, numpy |
# | **Output** | Direct predictions | Logits (need argmax) |
# | **Preprocessing** | Built into model | May need separate |
# | **Serve Command** | Same | Same |

# %% [markdown]
# ### 6.2 เปรียบเทียบ Model URI Formats
#
# | URI Format | ตัวอย่าง | ใช้งานกับ | หมายเหตุ |
# |------------|---------|-----------|----------|
# | `runs:/` | `runs:/{run_id}/sklearn_model` | load_model, download_artifacts | **แนะนำ** - เสถียรที่สุด |
# | `models:/` | `models:/iris_classifier/1` | load_model | ต้อง register model ก่อน |
# | Local path | `/path/to/model` | load_model, serve | ไม่ต้องมี Server |

# %% [markdown]
# ### 6.3 สรุป Model URIs และ Paths
#
# รัน cell นี้เพื่อดู Model URIs ทั้งหมด:

# %%
print("📋 Summary of Logged Models")
print("=" * 60)

# ตรวจสอบว่ามี variables หรือไม่
try:
    print()
    print("🌲 Scikit-learn Model (Iris Classification):")
    print(f"   Run ID: {sklearn_run_id}")
    print(f"   Model URI (runs:/): {sklearn_model_uri}")
    print(f"   Registered Name: iris_classifier_sklearn")
    print(f"   Registered URI: models:/iris_classifier_sklearn/1")
except NameError:
    print("⚠️ Sklearn model variables not found. Run training cells first.")

try:
    print()
    print("🔥 PyTorch Model (Wine Classification):")
    print(f"   Run ID: {pytorch_run_id}")
    print(f"   Model URI (runs:/): {pytorch_model_uri}")
    print(f"   Registered Name: wine_classifier_pytorch")
    print(f"   Registered URI: models:/wine_classifier_pytorch/1")
except NameError:
    print("⚠️ PyTorch model variables not found. Run training cells first.")

print()
print("=" * 60)
print("📁 File Locations:")
print(f"   Lab Base: {LAB_BASE_PATH}")
print(f"   Artifacts: {ARTIFACTS_PATH}")
print(f"   Database: {MLRUNS_DB_PATH}/mlflow.db")

print()
print("=" * 60)
print("🚀 Deploy Commands:")
print()
print("# Using Run URI (แนะนำ):")
try:
    print(f'mlflow models serve -m "{sklearn_model_uri}" -p 5001 --no-conda')
    print(f'mlflow models serve -m "{pytorch_model_uri}" -p 5002 --no-conda')
except NameError:
    print("# Run training cells first to get model URIs")
print()
print("# Using Registered Model:")
print('mlflow models serve -m "models:/iris_classifier_sklearn/1" -p 5001 --no-conda')
print('mlflow models serve -m "models:/wine_classifier_pytorch/1" -p 5002 --no-conda')
print()
print("=" * 60)
print("🌐 MLflow UI: http://127.0.0.1:5000")

# %% [markdown]
# ### 6.4 Best Practices สำหรับ Production
#
# **1. ใช้ `runs:/` URI สำหรับ download_artifacts:**
# ```python
# # ✅ แนะนำ - ใช้ runs:/ URI
# mlmodel_path = mlflow.artifacts.download_artifacts(f"runs:/{run_id}/model/MLmodel")
#
# # ⚠️ อาจมีปัญหา - ใช้ models:/ URI
# mlmodel_path = mlflow.artifacts.download_artifacts(f"models:/my_model/1/MLmodel")
# ```
#
# **2. ใช้ Model Signature เสมอ:**
# ```python
# signature = infer_signature(X_train, model.predict(X_train))
# mlflow.sklearn.log_model(model, "model", signature=signature)
# ```
#
# **3. บันทึก Input Example:**
# - ช่วยให้ทดสอบ model ได้ง่าย
# - เป็น documentation ให้คนอื่นเข้าใจ input format
#
# **4. ใช้ Model Registry:**
# - Version control สำหรับ models
# - Stage transitions (Staging → Production)
# - Model lineage tracking
#
# **5. Containerization:**
# ```bash
# # Build Docker image
# mlflow models build-docker -m "runs:/{run_id}/model" -n my_model_image
#
# # Run container
# docker run -p 5001:8080 my_model_image
# ```
#
# **6. Environment Management:**
# - ใช้ conda.yaml หรือ requirements.txt
# - Pin dependency versions
# - Test ใน isolated environment

# %% [markdown]
# ---
# ## 🎯 Part 7: แบบฝึกหัด (Exercises)
# ---

# %% [markdown]
# ### Exercise 1: Deploy Logistic Regression Model
#
# **Task:** Train และ Deploy Logistic Regression model สำหรับ Iris dataset
#
# **Steps:**
# 1. Train LogisticRegression model
# 2. Log ลง MLflow พร้อม signature
# 3. Deploy เป็น REST API บน port 5003
# 4. ทดสอบด้วย requests

# %%
# TODO: เขียน code ที่นี่
# Hint: ใช้ LogisticRegression() จาก sklearn.linear_model

# Your code here:
# ...

# %% [markdown]
# ### Exercise 2: Custom PyTorch Model
#
# **Task:** สร้าง Neural Network ที่มี architecture ต่างจากตัวอย่าง
#
# **Requirements:**
# - เพิ่ม layer เป็น 4 hidden layers
# - ใช้ BatchNormalization
# - Log ลง MLflow และ deploy

# %%
# TODO: เขียน code ที่นี่

# Your code here:
# ...

# %% [markdown]
# ### Exercise 3: Batch Prediction API
#
# **Task:** เขียน function ที่ส่ง batch prediction ไปยัง API
#
# **Requirements:**
# - รับ DataFrame เป็น input
# - ส่ง request ไป API
# - Return predictions พร้อม class names

# %%
def batch_predict(df, api_url, class_names):
    """
    ส่ง batch prediction ไปยัง MLflow serving API
    
    Args:
        df: pandas DataFrame ที่มี features
        api_url: URL ของ API (e.g., "http://127.0.0.1:5001/invocations")
        class_names: list ของชื่อ classes
    
    Returns:
        DataFrame พร้อม predictions
    """
    # TODO: Implement this function
    pass

# Test your function:
# result = batch_predict(X_test.head(10), "http://127.0.0.1:5001/invocations", iris.target_names)
# print(result)

# %% [markdown]
# ---
# ## 📚 Part 8: References และแหล่งเรียนรู้เพิ่มเติม
# ---
#
# **Official Documentation:**
# - [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
# - [MLflow Models](https://mlflow.org/docs/latest/models.html)
# - [MLflow Model Serving](https://mlflow.org/docs/latest/deployment/index.html)
#
# **Tutorials:**
# - [MLflow Quickstart](https://mlflow.org/docs/latest/getting-started/index.html)
# - [Deploy Models with MLflow](https://mlflow.org/docs/latest/deployment/deploy-model-locally.html)
#
# **Advanced Topics:**
# - Docker deployment
# - Kubernetes deployment
# - Cloud deployment (AWS SageMaker, Azure ML, GCP)
# - Model monitoring และ A/B testing

# %% [markdown]
# ---
# ## ✅ Checklist ก่อนส่งงาน
#
# - [ ] รัน notebook จนจบโดยไม่มี error
# - [ ] Log models ทั้ง Scikit-learn และ PyTorch สำเร็จ
# - [ ] Deploy และทดสอบ REST API ได้
# - [ ] ทำแบบฝึกหัดอย่างน้อย 1 ข้อ
# - [ ] เข้าใจความแตกต่างระหว่าง sklearn และ pytorch deployment
#
# ---
#
# **🎉 ยินดีด้วย! คุณจบ Lab นี้แล้ว!**
#
# ตอนนี้คุณสามารถ:
# - Log และ Deploy ML models ด้วย MLflow
# - สร้าง REST API สำหรับ model inference
# - เข้าใจ Model Signature และ Input Format
# - เปรียบเทียบการ deploy ระหว่าง frameworks ต่างๆ
