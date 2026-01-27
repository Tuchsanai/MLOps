# %% [markdown]
# # 🏛️ Lab: MLflow Model Registry
#
# **วัตถุประสงค์การเรียนรู้:**
# - เข้าใจแนวคิดและประโยชน์ของ Model Registry
# - สามารถลงทะเบียน Model เข้า Registry ได้
# - จัดการ Model Versions และ Stages ได้
# - โหลด Model จาก Registry มาใช้งานได้
# - เข้าใจ Model Lifecycle Management
#
# **สิ่งที่ต้องมีก่อนเริ่ม Lab:**
# - MLflow Server รันอยู่ที่ `http://127.0.0.1:5000`
# - ผ่าน Lab MLflow Tracking พื้นฐานมาแล้ว

# %% [markdown]
# ---
# ## 📚 ทฤษฎีพื้นฐาน
#
# ### 🔄 Machine Learning Lifecycle คืออะไร?
#
# ก่อนที่เราจะเข้าใจ Model Registry เราต้องเข้าใจ **Machine Learning Lifecycle** ก่อน
#
# ```
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                        Machine Learning Lifecycle                            │
# ├─────────────────────────────────────────────────────────────────────────────┤
# │                                                                              │
# │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
# │   │   Data   │───▶│  Model   │───▶│  Model   │───▶│  Model   │              │
# │   │Collection│    │ Training │    │Evaluation│    │Deployment│              │
# │   └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
# │        │               │               │               │                     │
# │        ▼               ▼               ▼               ▼                     │
# │   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
# │   │   Data   │    │Experiment│    │  Model   │    │Monitoring│              │
# │   │Processing│    │ Tracking │    │ Registry │    │& Logging │              │
# │   └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
# │                                                                              │
# │                    ◀─────── Feedback Loop ───────▶                          │
# │                                                                              │
# └─────────────────────────────────────────────────────────────────────────────┘
# ```
#
# **แต่ละขั้นตอนมีความสำคัญดังนี้:**
#
# | ขั้นตอน | คำอธิบาย | ปัญหาที่พบบ่อย |
# |---------|----------|---------------|
# | Data Collection | รวบรวมข้อมูลจากแหล่งต่างๆ | ข้อมูลไม่สอดคล้องกัน, ขาดการติดตาม |
# | Model Training | ฝึกโมเดลด้วย Algorithm ต่างๆ | ไม่รู้ว่าใช้ hyperparameters อะไร |
# | Model Evaluation | ประเมินประสิทธิภาพโมเดล | เปรียบเทียบโมเดลยาก |
# | Model Deployment | นำโมเดลไปใช้งานจริง | ไม่รู้ว่าโมเดลไหนใช้งานอยู่ |

# %% [markdown]
# ---
# ### 🤔 ปัญหาที่เกิดขึ้นเมื่อไม่มี Model Registry
#
# ลองนึกภาพสถานการณ์นี้:
#
# ```
# 📁 โฟลเดอร์โปรเจกต์ของคุณ (ไม่มี Model Registry)
# ├── model_v1.pkl
# ├── model_v2.pkl
# ├── model_v2_fixed.pkl
# ├── model_v2_fixed_final.pkl
# ├── model_v2_fixed_final_REAL.pkl      ← 😱 อันไหนดีที่สุด?
# ├── model_best.pkl
# ├── model_best_new.pkl
# └── model_production_maybe.pkl          ← 😵 งง!
# ```
#
# **ปัญหาที่พบบ่อย:**
#
# | ปัญหา | ผลกระทบ |
# |-------|---------|
# | 🔍 **หาโมเดลไม่เจอ** | ไม่รู้ว่าโมเดลไหนดีที่สุด ต้องฝึกใหม่ |
# | 📊 **ไม่รู้ Hyperparameters** | จำไม่ได้ว่าใช้ค่าอะไรฝึก |
# | 🔄 **ไม่มี Version Control** | ไม่สามารถย้อนกลับไปใช้โมเดลเก่าได้ |
# | 👥 **ทำงานเป็นทีมยาก** | ไม่รู้ว่าใครแก้ไขอะไร เมื่อไหร่ |
# | 🚀 **Deploy ยาก** | ไม่มั่นใจว่าโมเดลไหนพร้อม Production |
# | 📝 **ไม่มี Audit Trail** | ไม่สามารถตรวจสอบย้อนหลังได้ |

# %% [markdown]
# ---
# ### 🏛️ Model Registry คืออะไร?
#
# **Model Registry** คือระบบจัดการโมเดลแบบรวมศูนย์ (Centralized Model Management) ที่ช่วยแก้ปัญหาทั้งหมดข้างต้น
#
# ```
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                         🏛️ MLflow Model Registry                            │
# ├─────────────────────────────────────────────────────────────────────────────┤
# │                                                                              │
# │  ┌─────────────────────────────────────────────────────────────────────┐    │
# │  │  📦 Registered Model: "iris-classifier"                              │    │
# │  │  ├── 📋 Description: โมเดลจำแนกดอกไอริส                               │    │
# │  │  ├── 🏷️ Tags: [classification, sklearn, production-ready]           │    │
# │  │  │                                                                   │    │
# │  │  ├── 📌 Version 1 ─────────────────────────────────────────────────  │    │
# │  │  │   ├── Stage: ⚫ Archived                                          │    │
# │  │  │   ├── Created: 2024-01-15 10:30:00                               │    │
# │  │  │   ├── Accuracy: 0.92                                             │    │
# │  │  │   ├── Algorithm: RandomForest(n_estimators=50)                   │    │
# │  │  │   └── Run ID: abc123...                                          │    │
# │  │  │                                                                   │    │
# │  │  ├── 📌 Version 2 ─────────────────────────────────────────────────  │    │
# │  │  │   ├── Stage: 🟡 Staging                                          │    │
# │  │  │   ├── Created: 2024-01-20 14:45:00                               │    │
# │  │  │   ├── Accuracy: 0.95                                             │    │
# │  │  │   ├── Algorithm: RandomForest(n_estimators=100)                  │    │
# │  │  │   └── Run ID: def456...                                          │    │
# │  │  │                                                                   │    │
# │  │  └── 📌 Version 3 ─────────────────────────────────────────────────  │    │
# │  │      ├── Stage: 🟢 Production  ← กำลังใช้งานจริง                      │    │
# │  │      ├── Created: 2024-01-25 09:00:00                               │    │
# │  │      ├── Accuracy: 0.97                                             │    │
# │  │      ├── Algorithm: GradientBoosting(n_estimators=100)              │    │
# │  │      └── Run ID: ghi789...                                          │    │
# │  └─────────────────────────────────────────────────────────────────────┘    │
# │                                                                              │
# └─────────────────────────────────────────────────────────────────────────────┘
# ```

# %% [markdown]
# ---
# ### 🎯 ประโยชน์ของ Model Registry
#
# | ประโยชน์ | คำอธิบาย | ตัวอย่าง |
# |----------|----------|----------|
# | **🔢 Version Control** | ติดตามทุกเวอร์ชันของโมเดล | ย้อนกลับไปใช้ Version 2 ได้ทันที |
# | **📊 Metadata Tracking** | เก็บข้อมูลที่เกี่ยวข้องทั้งหมด | Parameters, Metrics, Artifacts |
# | **🚦 Stage Management** | จัดการสถานะการใช้งาน | Staging → Production |
# | **👥 Collaboration** | ทำงานร่วมกันเป็นทีม | ทุกคนเห็นโมเดลเดียวกัน |
# | **📝 Audit Trail** | ติดตามการเปลี่ยนแปลง | ใครเปลี่ยนอะไร เมื่อไหร่ |
# | **🔗 Lineage** | เชื่อมโยงกับ Experiment | รู้ว่าโมเดลมาจาก Run ไหน |

# %% [markdown]
# ---
# ### 🚦 Model Stages (สถานะของโมเดล)
#
# MLflow Model Registry มี 4 สถานะหลัก:
#
# ```
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                          Model Stage Lifecycle                               │
# ├─────────────────────────────────────────────────────────────────────────────┤
# │                                                                              │
# │     ┌────────────┐                                                          │
# │     │    None    │  ← โมเดลเพิ่งลงทะเบียน ยังไม่กำหนดสถานะ                    │
# │     │    ⚪      │                                                          │
# │     └─────┬──────┘                                                          │
# │           │                                                                  │
# │           ▼                                                                  │
# │     ┌────────────┐                                                          │
# │     │  Staging   │  ← กำลังทดสอบ (QA/Testing Environment)                    │
# │     │    🟡      │    - ทดสอบ Performance                                    │
# │     └─────┬──────┘    - ทดสอบ Integration                                    │
# │           │                                                                  │
# │           ▼                                                                  │
# │     ┌────────────┐                                                          │
# │     │ Production │  ← ใช้งานจริง (Live Environment)                          │
# │     │    🟢      │    - ให้บริการ Users จริง                                 │
# │     └─────┬──────┘    - ต้องมี Monitoring                                    │
# │           │                                                                  │
# │           ▼                                                                  │
# │     ┌────────────┐                                                          │
# │     │  Archived  │  ← เก็บถาวร (ไม่ใช้งานแล้ว แต่ยังเข้าถึงได้)               │
# │     │    ⚫      │    - เก็บไว้ Reference                                    │
# │     └────────────┘    - สามารถ Rollback ได้                                  │
# │                                                                              │
# └─────────────────────────────────────────────────────────────────────────────┘
# ```
#
# **รายละเอียดแต่ละ Stage:**
#
# | Stage | สัญลักษณ์ | คำอธิบาย | ใครใช้งาน | ตัวอย่าง Use Case |
# |-------|----------|----------|----------|------------------|
# | **None** | ⚪ | สถานะเริ่มต้น | Data Scientists | เพิ่งฝึกเสร็จ กำลังประเมินผล |
# | **Staging** | 🟡 | ทดสอบก่อน Production | QA Team, ML Engineers | ทดสอบกับข้อมูลจริงในสภาพแวดล้อมทดสอบ |
# | **Production** | 🟢 | ใช้งานจริง | End Users | ให้บริการผ่าน API |
# | **Archived** | ⚫ | เก็บถาวร | ทุกคน (อ่านอย่างเดียว) | เก็บโมเดลเก่าไว้ Reference |

# %% [markdown]
# ---
# ### 🔗 ความสัมพันธ์ระหว่าง Components ใน MLflow
#
# ```
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                    MLflow Components Relationship                            │
# ├─────────────────────────────────────────────────────────────────────────────┤
# │                                                                              │
# │  ┌─────────────────────────────────────────────────────────────────────┐    │
# │  │                    🧪 MLflow Tracking                                │    │
# │  │  ┌─────────────────────────────────────────────────────────────┐    │    │
# │  │  │  📁 Experiment: "iris-classification"                        │    │    │
# │  │  │  ├── 🏃 Run 1: random-forest-v1                              │    │    │
# │  │  │  │   ├── Parameters: {n_estimators: 50}                     │    │    │
# │  │  │  │   ├── Metrics: {accuracy: 0.92}                          │    │    │
# │  │  │  │   └── Artifacts: [model.pkl]                             │    │    │
# │  │  │  │                           │                               │    │    │
# │  │  │  │                           │  register_model()             │    │    │
# │  │  │  │                           ▼                               │    │    │
# │  │  │  ├── 🏃 Run 2: random-forest-v2  ────────────────────────┐   │    │    │
# │  │  │  │   └── Metrics: {accuracy: 0.95}                       │   │    │    │
# │  │  │  │                           │                            │   │    │    │
# │  │  │  │                           ▼                            │   │    │    │
# │  │  │  └── 🏃 Run 3: gradient-boosting  ───────────────────────┐│  │    │    │
# │  │  │      └── Metrics: {accuracy: 0.97}                       ││  │    │    │
# │  │  └──────────────────────────────────────────────────────────┘│  │    │    │
# │  └─────────────────────────────────────────────────────────────────┘    │    │
# │                                 │                                    │    │    │
# │                                 ▼                                    ▼    │    │
# │  ┌─────────────────────────────────────────────────────────────────────┐    │
# │  │                    🏛️ MLflow Model Registry                         │    │
# │  │  ├── Version 1 ← from Run 1 (Stage: Archived)                      │    │
# │  │  ├── Version 2 ← from Run 2 (Stage: Staging)                       │    │
# │  │  └── Version 3 ← from Run 3 (Stage: Production)                    │    │
# │  └─────────────────────────────────────────────────────────────────────┘    │
# │                                                                              │
# └─────────────────────────────────────────────────────────────────────────────┘
# ```

# %% [markdown]
# ---
# ## ⚙️ Pre-requisite: เตรียมความพร้อมก่อนเริ่ม Lab
#
# ### 📋 สิ่งที่ต้องมี
#
# 1. MLflow Server รันอยู่และเข้าถึงได้ที่ `http://127.0.0.1:5000`
# 2. ผ่าน Lab MLflow Tracking พื้นฐานมาแล้ว
#
# ### 🔍 ตรวจสอบ MLflow Server
#
# เปิด Browser แล้วไปที่: [http://127.0.0.1:5000](http://127.0.0.1:5000)

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 1: การเชื่อมต่อ MLflow Server
#
# ### แนวคิด
# ก่อนใช้งาน MLflow Model Registry ต้องเชื่อมต่อกับ MLflow Server ที่รัน Model Registry
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.set_tracking_uri(uri)` | กำหนด URL ของ MLflow Server |
# | `MlflowClient()` | สร้าง Client สำหรับจัดการ Registry |

# %%
import mlflow
from mlflow.tracking import MlflowClient
import os
import yaml

# กำหนด MLflow Tracking URI
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

# เชื่อมต่อ MLflow Server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# สร้าง MLflow Client สำหรับจัดการ Registry
client = MlflowClient()

# กำหนด ARTIFACTS_BASE path ตาม MLflow Server configuration
ARTIFACTS_BASE = "/home/student/workspace/mlflowserver-lab/mlartifacts"

print(f"✅ เชื่อมต่อ MLflow Server: {mlflow.get_tracking_uri()}")
print(f"📁 ARTIFACTS_BASE: {ARTIFACTS_BASE}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 2: การสร้างและลงทะเบียน Model (Scikit-learn)
#
# ### แนวคิด
# การลงทะเบียน Model เข้า Registry มี 2 วิธีหลัก:
#
# | วิธี | คำอธิบาย | Use Case |
# |------|----------|----------|
# | **วิธีที่ 1:** `registered_model_name` ใน `log_model()` | ลงทะเบียนพร้อม Train | ใช้เมื่อต้องการลงทะเบียนทันที |
# | **วิธีที่ 2:** `mlflow.register_model()` | ลงทะเบียนภายหลัง | ใช้เมื่อต้องการเลือก Model ที่ดีที่สุดก่อน |
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.sklearn.log_model(..., registered_model_name)` | บันทึกและลงทะเบียนพร้อมกัน |
# | `mlflow.register_model(model_uri, name)` | ลงทะเบียน Model ที่บันทึกไว้แล้ว |
# | `client.update_registered_model(name, description)` | อัพเดท Description ของ Model |
# | `client.set_registered_model_tag(name, key, value)` | เพิ่ม Tag ให้ Model |
# | `client.set_model_version_tag(name, version, key, value)` | เพิ่ม Tag ให้ Version |

# %% [markdown]
# ### 2.1 วิธีที่ 1: ลงทะเบียนพร้อม Train (Scikit-learn)

# %%
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.models import infer_signature
import numpy as np

# โหลดข้อมูล
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# ตั้งชื่อ Registered Model
SKLEARN_MODEL_NAME = "iris-classifier-sklearn"

# สร้างหรือเลือก Experiment
mlflow.set_experiment("model-registry-lab")

# %%
# Train และลงทะเบียน Model Version 1 (RandomForest n=50)
with mlflow.start_run(run_name="sklearn-rf-v1"):
    # Hyperparameters
    n_estimators = 50
    max_depth = 5
    
    # บันทึก Parameters
    mlflow.log_params({
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "model_type": "RandomForestClassifier",
        "version_note": "Baseline model"
    })
    
    # Train Model
    model_v1 = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model_v1.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_v1.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # บันทึก Metrics
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1_score": f1
    })
    
    # สร้าง Signature
    signature = infer_signature(X_train, model_v1.predict(X_train))
    
    # บันทึกและลงทะเบียน Model พร้อมกัน
    mlflow.sklearn.log_model(
        sk_model=model_v1,
        artifact_path="model",
        signature=signature,
        input_example=X_train[:3],
        registered_model_name=SKLEARN_MODEL_NAME
    )
    
    sklearn_run_id_v1 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน Model Version 1 สำเร็จ!")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 F1 Score: {f1:.4f}")
    print(f"🆔 Run ID: {sklearn_run_id_v1}")

# %%
# เพิ่ม Description และ Tags ให้ Registered Model
client.update_registered_model(
    name=SKLEARN_MODEL_NAME,
    description="""
    🌸 Iris Flower Classification Model (Scikit-learn)
    
    Purpose: จำแนกประเภทดอกไอริส 3 ชนิด (Setosa, Versicolor, Virginica)
    Input: 4 features (sepal length, sepal width, petal length, petal width)
    Output: Class prediction (0, 1, 2)
    
    Team: Data Science Team
    Contact: ds-team@example.com
    """
)

# เพิ่ม Tags ให้ Registered Model
client.set_registered_model_tag(SKLEARN_MODEL_NAME, "task", "classification")
client.set_registered_model_tag(SKLEARN_MODEL_NAME, "dataset", "iris")
client.set_registered_model_tag(SKLEARN_MODEL_NAME, "team", "data-science")
client.set_registered_model_tag(SKLEARN_MODEL_NAME, "framework", "sklearn")

# เพิ่ม Description และ Tags ให้ Version 1
client.update_model_version(
    name=SKLEARN_MODEL_NAME,
    version="1",
    description="Baseline model with RandomForest (n_estimators=50). Initial version for comparison."
)
client.set_model_version_tag(SKLEARN_MODEL_NAME, "1", "model_type", "RandomForest")
client.set_model_version_tag(SKLEARN_MODEL_NAME, "1", "status", "baseline")

print(f"✅ เพิ่ม Description และ Tags สำหรับ Model และ Version 1 สำเร็จ!")

# %%
# Train และลงทะเบียน Model Version 2 (RandomForest n=100)
with mlflow.start_run(run_name="sklearn-rf-v2"):
    
    # Hyperparameters ที่ปรับปรุง
    n_estimators = 100
    max_depth = 10
    
    mlflow.log_params({
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "model_type": "RandomForestClassifier",
        "version_note": "Improved model with more trees"
    })
    
    # Train Model
    model_v2 = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model_v2.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_v2.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1_score": f1
    })
    
    signature = infer_signature(X_train, model_v2.predict(X_train))
    
    # ลงทะเบียนเป็น Version ใหม่ของ Model เดิม
    mlflow.sklearn.log_model(
        sk_model=model_v2,
        artifact_path="model",
        signature=signature,
        input_example=X_train[:3],
        registered_model_name=SKLEARN_MODEL_NAME
    )
    
    sklearn_run_id_v2 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน Model Version 2 สำเร็จ!")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 F1 Score: {f1:.4f}")
    print(f"🆔 Run ID: {sklearn_run_id_v2}")

# %%
# เพิ่ม Description และ Tags ให้ Version 2
client.update_model_version(
    name=SKLEARN_MODEL_NAME,
    version="2",
    description="Improved RandomForest (n_estimators=100). Better accuracy than baseline."
)
client.set_model_version_tag(SKLEARN_MODEL_NAME, "2", "model_type", "RandomForest")
client.set_model_version_tag(SKLEARN_MODEL_NAME, "2", "status", "improved")

print(f"✅ เพิ่ม Description และ Tags สำหรับ Version 2 สำเร็จ!")

# %% [markdown]
# ###  ลงทะเบียนภายหลังจาก Run ที่มีอยู่แล้ว
#
# ใช้เมื่อต้องการ:
# - เลือก Model ที่ดีที่สุดจากหลายๆ Run ก่อนลงทะเบียน
# - ลงทะเบียน Model ที่ Train ไว้ก่อนหน้านี้

# %%
from sklearn.ensemble import GradientBoostingClassifier

# Train Model ใหม่โดยยังไม่ลงทะเบียน
with mlflow.start_run(run_name="sklearn-gb-candidate") as run:
    
    mlflow.log_params({
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 5,
        "model_type": "GradientBoostingClassifier",
        "version_note": "Gradient Boosting candidate"
    })
    
    model_gb = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model_gb.fit(X_train, y_train)
    
    y_pred = model_gb.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1_score": f1
    })
    
    signature = infer_signature(X_train, model_gb.predict(X_train))
    
    # บันทึก Model แต่ยังไม่ลงทะเบียน
    mlflow.sklearn.log_model(
        sk_model=model_gb,
        artifact_path="model",
        signature=signature,
        input_example=X_train[:3]
    )
    
    candidate_run_id = run.info.run_id
    
    print(f"✅ บันทึก Model สำเร็จ (ยังไม่ลงทะเบียน)")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 F1 Score: {f1:.4f}")
    print(f"🆔 Run ID: {candidate_run_id}")

# %%
# ตัดสินใจลงทะเบียน Model ภายหลัง
model_uri = f"runs:/{candidate_run_id}/model"

# ลงทะเบียนเป็น Version ใหม่
result = mlflow.register_model(
    model_uri=model_uri,
    name=SKLEARN_MODEL_NAME
)

print(f"✅ ลงทะเบียน Model ภายหลังสำเร็จ!")
print(f"📦 Model Name: {result.name}")
print(f"📌 Version: {result.version}")

# เพิ่ม Description และ Tags ให้ Version 3 (GradientBoosting)
client.update_model_version(
    name=SKLEARN_MODEL_NAME,
    version="3",
    description="GradientBoosting model. Best performance, deployed as champion."
)
client.set_model_version_tag(SKLEARN_MODEL_NAME, "3", "model_type", "GradientBoosting")
client.set_model_version_tag(SKLEARN_MODEL_NAME, "3", "deployment_status", "production")
client.set_model_version_tag(SKLEARN_MODEL_NAME, "3", "approved_by", "ML-Team-Lead")
client.set_model_version_tag(SKLEARN_MODEL_NAME, "3", "approval_date", "2024-01-25")

print(f"✅ เพิ่ม Description และ Tags สำหรับ Version 3 สำเร็จ!")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 3: การดูข้อมูล Registered Models
#
# ### แนวคิด
# หลังจากลงทะเบียน Model แล้ว สามารถดูข้อมูลได้หลายวิธี
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `client.search_registered_models()` | ค้นหา Registered Models ทั้งหมด |
# | `client.get_registered_model(name)` | ดูข้อมูล Model ตามชื่อ |
# | `client.search_model_versions(filter_string)` | ค้นหา Versions ของ Model |
# | `client.get_model_version(name, version)` | ดูข้อมูล Version เฉพาะ |

# %%
# ดู Registered Models ทั้งหมด
print("📦 Registered Models ทั้งหมด:")
print("=" * 60)

for rm in client.search_registered_models():
    print(f"\n🏷️ Model Name: {rm.name}")
    print(f"   📝 Description: {rm.description[:50] + '...' if rm.description and len(rm.description) > 50 else rm.description or 'ไม่มี'}")
    print(f"   📅 Created: {rm.creation_timestamp}")
    print(f"   📅 Last Updated: {rm.last_updated_timestamp}")

# %%
# ดูข้อมูล Versions ของ Model เฉพาะ
print(f"\n📌 Versions ของ '{SKLEARN_MODEL_NAME}':")
print("=" * 60)

versions = client.search_model_versions(f"name='{SKLEARN_MODEL_NAME}'")

for v in versions:
    print(f"\n  Version {v.version}:")
    print(f"    - Status: {v.status}")
    print(f"    - Stage: {v.current_stage}")
    print(f"    - Run ID: {v.run_id}")
    print(f"    - Created: {v.creation_timestamp}")

# %%
# ดูข้อมูล Version เฉพาะพร้อม Metrics จาก Run
print(f"\n📊 รายละเอียด Version พร้อม Metrics:")
print("=" * 60)

versions = client.search_model_versions(f"name='{SKLEARN_MODEL_NAME}'")

for v in versions:
    print(f"\n📌 Version {v.version}:")
    
    # ดึงข้อมูล Run ที่เกี่ยวข้อง
    run = client.get_run(v.run_id)
    
    # แสดง Parameters
    print(f"  Parameters:")
    for key, value in run.data.params.items():
        print(f"    - {key}: {value}")
    
    # แสดง Metrics
    print(f"  Metrics:")
    for key, value in run.data.metrics.items():
        print(f"    - {key}: {value:.4f}")

# %%
# ดู Tags ทั้งหมดของ Model และ Versions
model_info = client.get_registered_model(SKLEARN_MODEL_NAME)
print(f"\n📝 Tags ของ '{SKLEARN_MODEL_NAME}':")
for tag in model_info.tags:
    print(f"   - {tag}: {model_info.tags[tag]}")

version_info = client.get_model_version(SKLEARN_MODEL_NAME, "3")
print(f"\n📝 Tags ของ Version 3:")
for tag in version_info.tags:
    print(f"   - {tag}: {version_info.tags[tag]}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 4: การจัดการ Model Stages Aliases  (การตั้งชื่อนามแฝงให้ Model)
#
#
# ### ฟังก์ชันสำคัญ (MLflow 2.x - Aliases)
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `client.set_registered_model_alias(name, alias, version)` | กำหนด Alias ให้ Version |
# | `client.delete_registered_model_alias(name, alias)` | ลบ Alias |
# | `client.get_model_version_by_alias(name, alias)` | ดึง Version ตาม Alias |

# %% [markdown]
# ### 4.1 การใช้ Model Aliases (แนะนำสำหรับ MLflow 2.x)

# %%
# กำหนด Aliases ให้แต่ละ Version

# Version 1: กำหนดเป็น "baseline"
client.set_registered_model_alias(
    name=SKLEARN_MODEL_NAME,
    alias="baseline",
    version="1"
)
print(f"✅ กำหนด Alias 'baseline' ให้ Version 1")

# Version 2: กำหนดเป็น "staging"
client.set_registered_model_alias(
    name=SKLEARN_MODEL_NAME,
    alias="staging",
    version="2"
)
print(f"✅ กำหนด Alias 'staging' ให้ Version 2")

# Version 3: กำหนดเป็น "champion" (Production)
client.set_registered_model_alias(
    name=SKLEARN_MODEL_NAME,
    alias="champion",
    version="3"
)
print(f"✅ กำหนด Alias 'champion' ให้ Version 3")

# %%
# ดู Model Version จาก Alias
champion_version = client.get_model_version_by_alias(
    name=SKLEARN_MODEL_NAME,
    alias="champion"
)

print(f"\n🏆 Champion Model:")
print(f"   Version: {champion_version.version}")
print(f"   Run ID: {champion_version.run_id}")

# %%
# แสดง Aliases ทั้งหมดของ Model
model_info = client.get_registered_model(SKLEARN_MODEL_NAME)
print(f"\n📝 Aliases ของ '{SKLEARN_MODEL_NAME}':")
print(f"   {model_info.aliases}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 5: การโหลด Model จาก Registry
#
# ### แนวคิด
# การโหลด Model จาก Registry มีหลายวิธี ขึ้นอยู่กับ Use Case:
#
# | วิธี | URI Format | Use Case |
# |------|-----------|----------|
# | **โดย Model Name + Version** | `models:/<model_name>/<version>` | โหลด Version เฉพาะ |
# | **โดย Model Name + Alias** | `models:/<model_name>@<alias>` | โหลดตาม Alias (เช่น champion) |
# | **โดย Run ID** | `runs:/<run_id>/<artifact_path>` | โหลดจาก Run โดยตรง |
# | **โดย ARTIFACTS_BASE + Search** | Local path | โหลดโดยตรงจาก Disk (เร็วที่สุด) |
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `mlflow.sklearn.load_model(model_uri)` | โหลด Scikit-learn Model |
# | `mlflow.pytorch.load_model(model_uri)` | โหลด PyTorch Model |
# | `mlflow.pyfunc.load_model(model_uri)` | โหลด Model แบบ Generic |

# %% [markdown]
# ### 5.1 โหลด Model โดยใช้ Model Name และ Version

# %%
# โหลด Model โดยระบุ Version
print("📥 วิธีที่ 1: โหลด Model โดยระบุ Version")
print("=" * 60)

# โหลด Version 1
model_uri_v1 = f"models:/{SKLEARN_MODEL_NAME}/1"
print(f"\n🔗 Model URI: {model_uri_v1}")

loaded_model_v1 = mlflow.sklearn.load_model(model_uri_v1)
print(f"✅ โหลด Version 1 สำเร็จ: {type(loaded_model_v1)}")

# ทดสอบทำนาย
predictions_v1 = loaded_model_v1.predict(X_test[:5])
print(f"🔮 Predictions (v1): {predictions_v1}")
print(f"📋 Actual:          {y_test[:5]}")

# %%
# โหลด Version 3
model_uri_v3 = f"models:/{SKLEARN_MODEL_NAME}/3"
print(f"\n🔗 Model URI: {model_uri_v3}")

loaded_model_v3 = mlflow.sklearn.load_model(model_uri_v3)
print(f"✅ โหลด Version 3 สำเร็จ: {type(loaded_model_v3)}")

# ทดสอบทำนาย
predictions_v3 = loaded_model_v3.predict(X_test[:5])
print(f"🔮 Predictions (v3): {predictions_v3}")
print(f"📋 Actual:          {y_test[:5]}")

# %% [markdown]
# ### 5.2 โหลด Model โดยใช้ Alias (แนะนำสำหรับ Production)

# %%
# โหลด Model โดยใช้ Alias
print("\n📥 วิธีที่ 2: โหลด Model โดยใช้ Alias")
print("=" * 60)

# โหลด Champion Model
model_uri_champion = f"models:/{SKLEARN_MODEL_NAME}@champion"
print(f"\n🔗 Model URI: {model_uri_champion}")

loaded_champion = mlflow.sklearn.load_model(model_uri_champion)
print(f"✅ โหลด Champion Model สำเร็จ: {type(loaded_champion)}")

# ทดสอบทำนาย
predictions_champion = loaded_champion.predict(X_test[:5])
print(f"🔮 Predictions (champion): {predictions_champion}")
print(f"📋 Actual:                 {y_test[:5]}")

# %%
# โหลด Baseline Model
model_uri_baseline = f"models:/{SKLEARN_MODEL_NAME}@baseline"
print(f"\n🔗 Model URI: {model_uri_baseline}")

loaded_baseline = mlflow.sklearn.load_model(model_uri_baseline)
print(f"✅ โหลด Baseline Model สำเร็จ: {type(loaded_baseline)}")

# เปรียบเทียบ Accuracy
accuracy_baseline = accuracy_score(y_test, loaded_baseline.predict(X_test))
accuracy_champion = accuracy_score(y_test, loaded_champion.predict(X_test))

print(f"\n📊 เปรียบเทียบ Accuracy:")
print(f"   Baseline: {accuracy_baseline:.4f}")
print(f"   Champion: {accuracy_champion:.4f}")
print(f"   ปรับปรุง: +{(accuracy_champion - accuracy_baseline) * 100:.2f}%")


# %% [markdown]
# ### 5.4 โหลด Model จาก ARTIFACTS_BASE โดยตรง (เร็วที่สุด)
#
# วิธีนี้เหมาะสำหรับ:
# - Production ที่ต้องการความเร็วสูงสุด
# - Server เดียวกันกับ MLflow Server
# - ไม่ต้องผ่าน Network

# %%
# Helper Function: ค้นหา Model Path จาก ARTIFACTS_BASE

def find_all_models_in_artifacts(artifacts_base: str, experiment_id: str) -> list:
    """
    ค้นหา models ทั้งหมดใน ARTIFACTS_BASE
    
    Returns:
        List of dict containing model info
    """
    models_folder = f"{artifacts_base}/{experiment_id}/models"
    found_models = []
    
    if not os.path.exists(models_folder):
        print(f"⚠️ ไม่พบโฟลเดอร์: {models_folder}")
        return found_models
    
    for model_dir in os.listdir(models_folder):
        model_path = f"{models_folder}/{model_dir}/artifacts"
        mlmodel_file = f"{model_path}/MLmodel"
        
        if os.path.exists(mlmodel_file):
            with open(mlmodel_file, 'r') as f:
                mlmodel = yaml.safe_load(f)
            
            flavors = list(mlmodel.get('flavors', {}).keys())
            found_models.append({
                'model_id': model_dir,
                'path': model_path,
                'flavors': flavors,
                'mlmodel': mlmodel
            })
    
    return found_models


def find_model_path_by_flavor(artifacts_base: str, experiment_id: str, flavor: str = "sklearn") -> str:
    """
    ค้นหา model path จาก models/ folder ตาม flavor ที่ต้องการ
    
    Returns:
        Full path ไปยัง model หรือ None ถ้าไม่พบ
    """
    models = find_all_models_in_artifacts(artifacts_base, experiment_id)
    
    for model in models:
        if flavor in model['flavors']:
            return model['path']
    
    return None


def find_model_path_by_run_id(artifacts_base: str, experiment_id: str, run_id: str) -> str:
    """
    ค้นหา model path จาก run_id
    
    Returns:
        Full path ไปยัง model หรือ None ถ้าไม่พบ
    """
    # ค้นหาใน artifacts folder ของ run
    run_artifacts = f"{artifacts_base}/{experiment_id}/{run_id}/artifacts/model"
    
    if os.path.exists(run_artifacts):
        return run_artifacts
    
    return None

# %%
# ดึงข้อมูล Experiment ID
experiment = mlflow.get_experiment_by_name("model-registry-lab")
experiment_id = experiment.experiment_id

print(f"📁 ARTIFACTS_BASE: {ARTIFACTS_BASE}")
print(f"🆔 Experiment ID: {experiment_id}")

# %%
# แสดง Models ทั้งหมดใน ARTIFACTS_BASE
print("\n📦 Models ทั้งหมดใน ARTIFACTS_BASE:")
print("=" * 60)

all_models = find_all_models_in_artifacts(ARTIFACTS_BASE, experiment_id)

for i, model in enumerate(all_models, 1):
    print(f"\n{i}. Model ID: {model['model_id']}")
    print(f"   Path: {model['path']}")
    print(f"   Flavors: {model['flavors']}")

# %%
# โหลด sklearn model จาก ARTIFACTS_BASE
print("\n📥 วิธีที่ 4: โหลด Model จาก ARTIFACTS_BASE โดยตรง")
print("=" * 60)

sklearn_model_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, flavor="sklearn")

if sklearn_model_path:
    print(f"📦 Model Path: {sklearn_model_path}")
    
    # โหลด model
    loaded_sklearn_model = mlflow.sklearn.load_model(sklearn_model_path)
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_sklearn_model)}")
    
    # ทดสอบทำนาย
    predictions = loaded_sklearn_model.predict(X_test[:5])
    print(f"\n🔮 ทดสอบทำนาย 5 ตัวอย่างแรก:")
    print(f"   Predictions: {predictions}")
    print(f"   Actual:      {y_test[:5]}")
else:
    print("⚠️ ไม่พบ sklearn model ใน ARTIFACTS_BASE")

# %% [markdown]
# ### 5.5 โหลด Model จาก Run ID + ARTIFACTS_BASE

# %%
# โหลด Model จาก Run ID โดยใช้ ARTIFACTS_BASE
print("\n📥 วิธีที่ 5: โหลด Model จาก Run ID + ARTIFACTS_BASE")
print("=" * 60)

model_path_from_run = find_model_path_by_run_id(ARTIFACTS_BASE, experiment_id, sklearn_run_id_v1)

if model_path_from_run:
    print(f"🆔 Run ID: {sklearn_run_id_v1}")
    print(f"📦 Model Path: {model_path_from_run}")
    
    loaded_from_run_path = mlflow.sklearn.load_model(model_path_from_run)
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_from_run_path)}")
    
    predictions = loaded_from_run_path.predict(X_test[:5])
    print(f"\n🔮 Predictions: {predictions}")
    print(f"📋 Actual:      {y_test[:5]}")
else:
    print(f"⚠️ ไม่พบ model สำหรับ Run ID: {sklearn_run_id_v1}")

# %% [markdown]
# ### 5.6 โหลด Model จาก Alias โดยค้นหา Version ก่อน

# %%
# โหลด Model จาก Alias โดยค้นหา Version และ Run ID ก่อน
print("\n📥 วิธีที่ 6: โหลด Model จาก Alias (ค้นหา Version ก่อน)")
print("=" * 60)

# ค้นหา Version จาก Alias
alias_to_load = "champion"
version_info = client.get_model_version_by_alias(SKLEARN_MODEL_NAME, alias_to_load)

print(f"🏷️ Alias: {alias_to_load}")
print(f"📌 Version: {version_info.version}")
print(f"🆔 Run ID: {version_info.run_id}")

# โหลดจาก Run ID
model_path = find_model_path_by_run_id(ARTIFACTS_BASE, experiment_id, version_info.run_id)

if model_path:
    print(f"📦 Model Path: {model_path}")
    
    loaded_from_alias = mlflow.sklearn.load_model(model_path)
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_from_alias)}")
    
    predictions = loaded_from_alias.predict(X_test[:5])
    print(f"\n🔮 Predictions: {predictions}")
    print(f"📋 Actual:      {y_test[:5]}")
else:
    # Fallback: ใช้ Model URI
    print("💡 ไม่พบใน ARTIFACTS_BASE, ใช้ Model URI แทน")
    model_uri = f"models:/{SKLEARN_MODEL_NAME}@{alias_to_load}"
    loaded_from_alias = mlflow.sklearn.load_model(model_uri)
    print(f"✅ โหลด Model สำเร็จ: {type(loaded_from_alias)}")

# %% [markdown]
# ### 5.7 โหลด Model แบบ Generic ด้วย PyFunc

# %%
# โหลด Model แบบ Generic ด้วย PyFunc
print("\n📥 วิธีที่ 7: โหลด Model แบบ Generic ด้วย PyFunc")
print("=" * 60)

model_uri = f"models:/{SKLEARN_MODEL_NAME}@champion"
print(f"🔗 Model URI: {model_uri}")

# PyFunc สามารถโหลด Model ได้ทุก flavor
pyfunc_model = mlflow.pyfunc.load_model(model_uri)
print(f"✅ โหลด Model สำเร็จ: {type(pyfunc_model)}")

# ทดสอบทำนาย
predictions_pyfunc = pyfunc_model.predict(X_test[:5])
print(f"\n🔮 Predictions: {predictions_pyfunc}")
print(f"📋 Actual:      {y_test[:5]}")

# %% [markdown]
# ### 5.8 สรุปวิธีการโหลด Model

# %%
# สรุปวิธีการโหลด Model ทั้งหมด
print("\n📋 สรุปวิธีการโหลด Model ทั้งหมด:")
print("=" * 70)

summary = """
| วิธี | URI/Path | Use Case |
|------|----------|----------|
| 1. Model Name + Version | models:/<name>/<version> | โหลด Version เฉพาะ |
| 2. Model Name + Alias | models:/<name>@<alias> | Production (แนะนำ) |
| 3. Run ID | runs:/<run_id>/<artifact_path> | Debug, Reproduce |
| 4. ARTIFACTS_BASE + Flavor | Local path | เร็วที่สุด (same server) |
| 5. ARTIFACTS_BASE + Run ID | Local path | เร็ว + ระบุ Run ได้ |
| 6. Alias → Version → Run ID | Local path | ยืดหยุ่น |
| 7. PyFunc (Generic) | models:/<name>@<alias> | ใช้ได้ทุก Framework |
"""
print(summary)

# %%
# ทดสอบ Performance การโหลด Model
import time

print("\n⏱️ เปรียบเทียบเวลาโหลด Model:")
print("=" * 60)

# วิธี 1: Model URI (via Network/API)
start = time.time()
_ = mlflow.sklearn.load_model(f"models:/{SKLEARN_MODEL_NAME}@champion")
time_uri = time.time() - start
print(f"1. Model URI (models:/<name>@alias): {time_uri:.4f} วินาที")

# วิธี 2: ARTIFACTS_BASE (Direct Disk Access)
sklearn_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, "sklearn")
if sklearn_path:
    start = time.time()
    _ = mlflow.sklearn.load_model(sklearn_path)
    time_disk = time.time() - start
    print(f"2. ARTIFACTS_BASE (Direct Disk):     {time_disk:.4f} วินาที")
    
    if time_disk < time_uri:
        print(f"\n💡 Direct Disk Access เร็วกว่า {(time_uri/time_disk):.1f}x")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 6: การลงทะเบียน PyTorch Model
#
# ### แนวคิด
# PyTorch Model สามารถลงทะเบียนได้เหมือนกับ Scikit-learn
# โดยใช้ `mlflow.pytorch.log_model()` พร้อม `registered_model_name`

# %%
import torch
import torch.nn as nn

# สร้าง Simple Neural Network
class IrisClassifier(nn.Module):
    def __init__(self, input_size=4, hidden_size=16, num_classes=3):
        super(IrisClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# ตั้งชื่อ Registered Model สำหรับ PyTorch
PYTORCH_MODEL_NAME = "iris-classifier-pytorch"

# %%
# Train และลงทะเบียน PyTorch Model Version 1
with mlflow.start_run(run_name="pytorch-nn-v1"):
    
    # Hyperparameters
    hidden_size = 16
    learning_rate = 0.01
    epochs = 100
    
    mlflow.log_params({
        "hidden_size": hidden_size,
        "learning_rate": learning_rate,
        "epochs": epochs,
        "model_type": "SimpleNN"
    })
    
    # สร้าง Model
    pytorch_model = IrisClassifier(hidden_size=hidden_size)
    
    # เตรียมข้อมูล
    X_train_float32 = X_train.astype('float32')
    X_test_float32 = X_test.astype('float32')
    X_tensor = torch.FloatTensor(X_train_float32)
    y_tensor = torch.LongTensor(y_train)
    
    # Training
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(pytorch_model.parameters(), lr=learning_rate)
    
    print("🚀 Training PyTorch Model...")
    for epoch in range(epochs):
        outputs = pytorch_model(X_tensor)
        loss = criterion(outputs, y_tensor)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 25 == 0:
            mlflow.log_metric("train_loss", loss.item(), step=epoch)
            print(f"   Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
    
    # Evaluate
    pytorch_model.eval()
    with torch.no_grad():
        X_test_tensor = torch.FloatTensor(X_test_float32)
        outputs = pytorch_model(X_test_tensor)
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted.numpy() == y_test).sum() / len(y_test)
    
    mlflow.log_metric("accuracy", accuracy)
    print(f"\n📊 Test Accuracy: {accuracy:.4f}")
    
    # สร้าง Signature
    signature = infer_signature(
        X_train_float32,
        pytorch_model(torch.FloatTensor(X_train_float32)).detach().numpy()
    )
    
    # บันทึกและลงทะเบียน PyTorch Model
    mlflow.pytorch.log_model(
        pytorch_model=pytorch_model,
        artifact_path="model",
        signature=signature,
        input_example=X_train_float32[:3],
        registered_model_name=PYTORCH_MODEL_NAME
    )
    
    pytorch_run_id_v1 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน PyTorch Model Version 1 สำเร็จ!")
    print(f"🆔 Run ID: {pytorch_run_id_v1}")

# %%
# เพิ่ม Description และ Tags ให้ PyTorch Model
client.update_registered_model(
    name=PYTORCH_MODEL_NAME,
    description="""
    🌸 Iris Flower Classification Model (PyTorch)
    
    Purpose: จำแนกประเภทดอกไอริส 3 ชนิด
    Architecture: Simple Neural Network (Input -> Hidden -> Output)
    Input: 4 features (float32)
    Output: 3 class logits
    """
)

client.set_registered_model_tag(PYTORCH_MODEL_NAME, "task", "classification")
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "dataset", "iris")
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "framework", "pytorch")

client.update_model_version(
    name=PYTORCH_MODEL_NAME,
    version="1",
    description="Baseline SimpleNN (hidden_size=16)."
)
client.set_model_version_tag(PYTORCH_MODEL_NAME, "1", "architecture", "SimpleNN")

print(f"✅ เพิ่ม Description และ Tags สำเร็จ!")

# %%
# Train และลงทะเบียน PyTorch Model Version 2
with mlflow.start_run(run_name="pytorch-nn-v2"):
    
    hidden_size = 32
    learning_rate = 0.005
    epochs = 150
    
    mlflow.log_params({
        "hidden_size": hidden_size,
        "learning_rate": learning_rate,
        "epochs": epochs,
        "model_type": "SimpleNN-Deeper"
    })
    
    pytorch_model_v2 = IrisClassifier(hidden_size=hidden_size)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(pytorch_model_v2.parameters(), lr=learning_rate)
    
    print("🚀 Training PyTorch Model v2...")
    for epoch in range(epochs):
        outputs = pytorch_model_v2(X_tensor)
        loss = criterion(outputs, y_tensor)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 50 == 0:
            mlflow.log_metric("train_loss", loss.item(), step=epoch)
            print(f"   Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
    
    pytorch_model_v2.eval()
    with torch.no_grad():
        X_test_tensor = torch.FloatTensor(X_test_float32)
        outputs = pytorch_model_v2(X_test_tensor)
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted.numpy() == y_test).sum() / len(y_test)
    
    mlflow.log_metric("accuracy", accuracy)
    print(f"\n📊 Test Accuracy: {accuracy:.4f}")
    
    signature = infer_signature(
        X_train_float32,
        pytorch_model_v2(torch.FloatTensor(X_train_float32)).detach().numpy()
    )
    
    mlflow.pytorch.log_model(
        pytorch_model=pytorch_model_v2,
        artifact_path="model",
        signature=signature,
        input_example=X_train_float32[:3],
        registered_model_name=PYTORCH_MODEL_NAME
    )
    
    pytorch_run_id_v2 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน PyTorch Model Version 2 สำเร็จ!")
    print(f"🆔 Run ID: {pytorch_run_id_v2}")

# %%
# เพิ่ม Tags และกำหนด Aliases สำหรับ PyTorch Models
client.update_model_version(
    name=PYTORCH_MODEL_NAME,
    version="2",
    description="Deeper SimpleNN (hidden_size=32). Better performance."
)
client.set_model_version_tag(PYTORCH_MODEL_NAME, "2", "architecture", "SimpleNN-Deeper")
client.set_model_version_tag(PYTORCH_MODEL_NAME, "2", "status", "champion")

client.set_registered_model_alias(PYTORCH_MODEL_NAME, "baseline", "1")
client.set_registered_model_alias(PYTORCH_MODEL_NAME, "champion", "2")

print(f"✅ กำหนด Aliases สำหรับ PyTorch Models สำเร็จ!")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 7: การโหลด PyTorch Model จาก Registry

# %%
# โหลด PyTorch Model ด้วยวิธีต่างๆ
print("📥 โหลด PyTorch Model จาก Registry:")
print("=" * 60)

# วิธี 1: ใช้ Model URI + Alias
print("\n1️⃣ โหลดด้วย Model URI + Alias:")
pytorch_uri = f"models:/{PYTORCH_MODEL_NAME}@champion"
print(f"   URI: {pytorch_uri}")

loaded_pytorch = mlflow.pytorch.load_model(pytorch_uri)
print(f"   ✅ โหลดสำเร็จ: {type(loaded_pytorch)}")

loaded_pytorch.eval()
with torch.no_grad():
    test_tensor = torch.FloatTensor(X_test_float32[:5])
    outputs = loaded_pytorch(test_tensor)
    _, predicted = torch.max(outputs.data, 1)
    print(f"   🔮 Predictions: {predicted.numpy()}")
    print(f"   📋 Actual:      {y_test[:5]}")

# %%
# วิธี 2: โหลดจาก ARTIFACTS_BASE
print("\n2️⃣ โหลดจาก ARTIFACTS_BASE:")

pytorch_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, flavor="pytorch")

if pytorch_path:
    print(f"   Path: {pytorch_path}")
    
    loaded_pytorch_disk = mlflow.pytorch.load_model(pytorch_path)
    print(f"   ✅ โหลดสำเร็จ: {type(loaded_pytorch_disk)}")
    
    loaded_pytorch_disk.eval()
    with torch.no_grad():
        outputs = loaded_pytorch_disk(test_tensor)
        _, predicted = torch.max(outputs.data, 1)
        print(f"   🔮 Predictions: {predicted.numpy()}")
else:
    print("   ⚠️ ไม่พบ PyTorch model ใน ARTIFACTS_BASE")

# %%
# วิธี 3: โหลดจาก Alias → Version → Run ID
print("\n3️⃣ โหลดจาก Alias → Version → Run ID:")

version_info = client.get_model_version_by_alias(PYTORCH_MODEL_NAME, "champion")
print(f"   Alias: champion → Version: {version_info.version}")
print(f"   Run ID: {version_info.run_id}")

pytorch_run_path = find_model_path_by_run_id(ARTIFACTS_BASE, experiment_id, version_info.run_id)

if pytorch_run_path:
    print(f"   Path: {pytorch_run_path}")
    loaded_pytorch_run = mlflow.pytorch.load_model(pytorch_run_path)
    print(f"   ✅ โหลดสำเร็จ: {type(loaded_pytorch_run)}")
else:
    print("   ⚠️ ไม่พบใน ARTIFACTS_BASE, ใช้ Model URI แทน")
    loaded_pytorch_run = mlflow.pytorch.load_model(f"runs:/{version_info.run_id}/model")
    print(f"   ✅ โหลดสำเร็จ: {type(loaded_pytorch_run)}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 8: การค้นหา Models และ Versions

# %%
# ค้นหา Models ที่มี Tag เฉพาะ
print("🔍 ค้นหา Models ที่เป็น classification task:")
print("-" * 40)

models = client.search_registered_models(
    filter_string="tags.task = 'classification'"
)

for model in models:
    print(f"  📦 {model.name}")

# %%
# ค้นหา Versions ของ Model เฉพาะ
print(f"\n🔍 Versions ทั้งหมดของ '{SKLEARN_MODEL_NAME}':")
print("-" * 40)

versions = client.search_model_versions(
    filter_string=f"name = '{SKLEARN_MODEL_NAME}'"
)

for v in versions:
    print(f"  📌 Version {v.version}: {v.current_stage}")

# %%
# ค้นหา Model Versions โดยใช้ run_id
print(f"\n🔍 ค้นหา Version จาก Run ID:")
print("-" * 40)

versions = client.search_model_versions(
    filter_string=f"run_id = '{sklearn_run_id_v1}'"
)

for v in versions:
    print(f"  📦 Model: {v.name}")
    print(f"  📌 Version: {v.version}")
    print(f"  🆔 Run ID: {v.run_id}")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 9: การลบ Model และ Version
#
# **⚠️ ข้อควรระวัง:**
# - การลบไม่สามารถยกเลิกได้
# - ต้องลบ Versions ทั้งหมดก่อนลบ Model
# - ควรใช้ Archive แทนการลบถ้าต้องการเก็บไว้ Reference

# %%
# ตัวอย่างการลบ (Uncomment เพื่อทดลอง)

# # ลบ Version เฉพาะ
# client.delete_model_version(
#     name=SKLEARN_MODEL_NAME,
#     version="1"
# )
# print("✅ ลบ Version 1 สำเร็จ!")

# # ลบ Alias ก่อนลบ Model
# client.delete_registered_model_alias(SKLEARN_MODEL_NAME, "baseline")
# client.delete_registered_model_alias(SKLEARN_MODEL_NAME, "staging")
# client.delete_registered_model_alias(SKLEARN_MODEL_NAME, "champion")

# # ลบ Model ทั้งหมด
# client.delete_registered_model(name=SKLEARN_MODEL_NAME)
# print("✅ ลบ Model ทั้งหมดสำเร็จ!")

print("💡 การลบเป็น Destructive Operation - ใช้อย่างระมัดระวัง!")
print("💡 แนะนำให้ใช้ Archive หรือ Alias แทนการลบ")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 10: สรุปและ Best Practices

# %%
# สรุปข้อมูล Models ที่ลงทะเบียนใน Lab นี้
print("📦 สรุป Registered Models ใน Lab นี้:")
print("=" * 60)

for model_name in [SKLEARN_MODEL_NAME, PYTORCH_MODEL_NAME]:
    try:
        model = client.get_registered_model(model_name)
        versions = list(client.search_model_versions(f"name = '{model_name}'"))
        
        print(f"\n🏷️ {model_name}")
        print(f"   📝 Versions: {len(versions)}")
        print(f"   📝 Aliases: {model.aliases}")
        
        try:
            champion = client.get_model_version_by_alias(model_name, "champion")
            run = client.get_run(champion.run_id)
            accuracy = run.data.metrics.get("accuracy", "N/A")
            print(f"   🏆 Champion (v{champion.version}): accuracy = {accuracy:.4f if isinstance(accuracy, float) else accuracy}")
        except:
            print(f"   🏆 Champion: ไม่มี")
    except:
        print(f"\n🏷️ {model_name}: ไม่พบ")

print(f"\n🔗 ดูรายละเอียดที่: http://127.0.0.1:5000/#/models")

# %% [markdown]
# ---
# ## 📝 สรุปบทเรียน
#
# ### วิธีการโหลด Model ทั้งหมด
#
# | วิธี | URI/Path | Use Case | ความเร็ว |
# |------|----------|----------|----------|
# | Model Name + Version | `models:/<name>/<version>` | โหลด Version เฉพาะ | ปานกลาง |
# | Model Name + Alias | `models:/<name>@<alias>` | Production (แนะนำ) | ปานกลาง |
# | Run ID | `runs:/<run_id>/<path>` | Debug, Reproduce | ปานกลาง |
# | ARTIFACTS_BASE + Flavor | Local path | Same server | เร็วที่สุด |
# | ARTIFACTS_BASE + Run ID | Local path | Same server + ระบุ Run | เร็วที่สุด |
# | Alias → Version → Run ID | Local path | ยืดหยุ่น | เร็วที่สุด |
# | PyFunc (Generic) | `models:/<name>@<alias>` | ใช้ได้ทุก Framework | ปานกลาง |
#
# ### ฟังก์ชันสำคัญ
#
# | Category | ฟังก์ชัน |
# |----------|----------|
# | **ลงทะเบียน** | `mlflow.sklearn.log_model(..., registered_model_name)` |
# | **โหลด (sklearn)** | `mlflow.sklearn.load_model(uri_or_path)` |
# | **โหลด (pytorch)** | `mlflow.pytorch.load_model(uri_or_path)` |
# | **โหลด (generic)** | `mlflow.pyfunc.load_model(uri_or_path)` |
# | **กำหนด Alias** | `client.set_registered_model_alias(name, alias, version)` |
# | **ค้นหา Version จาก Alias** | `client.get_model_version_by_alias(name, alias)` |
#
# ### การโหลด Model จาก ARTIFACTS_BASE
#
# ```python
# # 1. กำหนด path
# ARTIFACTS_BASE = "/path/to/mlartifacts"
#
# # 2. ค้นหา model path
# model_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, "sklearn")
# # หรือ
# model_path = find_model_path_by_run_id(ARTIFACTS_BASE, experiment_id, run_id)
#
# # 3. โหลด model
# model = mlflow.sklearn.load_model(model_path)
# ```

# %% [markdown]
# ---
# ## 🔗 แหล่งข้อมูลเพิ่มเติม
#
# - [MLflow Model Registry Documentation](https://mlflow.org/docs/latest/model-registry.html)
# - [Model Aliases and Tags](https://mlflow.org/docs/latest/model-registry.html#model-aliases)
# - [MLflow Python API](https://mlflow.org/docs/latest/python_api/mlflow.html)
#
# ---
#
# **MLflow Server URL: http://127.0.0.1:5000**
