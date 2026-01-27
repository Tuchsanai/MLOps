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

# กำหนด MLflow Tracking URI
MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

# เชื่อมต่อ MLflow Server
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# สร้าง MLflow Client สำหรับจัดการ Registry
client = MlflowClient()

print(f"✅ เชื่อมต่อ MLflow Server: {mlflow.get_tracking_uri()}")

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
        registered_model_name=SKLEARN_MODEL_NAME  # ← ลงทะเบียนทันที!
    )
    
    sklearn_run_id_v1 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน Model Version 1 สำเร็จ!")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print(f"📊 F1 Score: {f1:.4f}")
    print(f"🆔 Run ID: {sklearn_run_id_v1}")


# %%

# เพิ่ม Description และ Tags ให้ Registered Model (ทำครั้งเดียวหลังสร้าง Model แรก)
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
# ### 2.2 วิธีที่ 2: ลงทะเบียนภายหลังจาก Run ที่มีอยู่แล้ว
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
# สมมติว่าตรวจสอบแล้วพบว่า Model นี้ดีที่สุด

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
    print(f"   📝 Description: {rm.description or 'ไม่มี'}")
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
# ## 📚 ส่วนที่ 4: การจัดการ Model Stages (Aliases)
#
# ### แนวคิด (MLflow 2.x)
# ใน MLflow 2.x แนะนำให้ใช้ **Model Aliases** แทน Stages เดิม
#
# | Concept เก่า (Stages) | Concept ใหม่ (Aliases) |
# |----------------------|----------------------|
# | `None`, `Staging`, `Production`, `Archived` | กำหนดเองได้ เช่น `champion`, `challenger` |
# | เปลี่ยน Stage ด้วย `transition_model_version_stage()` | กำหนด Alias ด้วย `set_registered_model_alias()` |
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
# การโหลด Model จาก Registry สามารถทำได้โดยการโหลดจาก **ARTIFACTS_BASE** โดยตรง
# ซึ่งเป็นวิธีที่เร็วที่สุดสำหรับ Production บน Server เดียวกัน
#
# ### โครงสร้างไฟล์ใน ARTIFACTS_BASE
# เมื่อใช้ `--serve-artifacts` กับ MLflow Server, **Models จะถูกเก็บในโฟลเดอร์ `models/` แยกต่างหาก**:
#
# ```
# mlartifacts/
# └── <experiment_id>/
#     ├── <run_id>/
#     │   └── artifacts/           # Artifacts ทั่วไป (plots, data, config)
#     └── models/                  # ⚠️ Models ถูกเก็บที่นี่!
#         └── m-<model_id>/        
#             └── artifacts/
#                 ├── MLmodel
#                 ├── model.pkl
#                 └── ...
# ```

# %%
import yaml

# กำหนด ARTIFACTS_BASE path ตาม MLflow Server configuration
ARTIFACTS_BASE = "/home/student/workspace/mlflowserver-lab/mlartifacts"

# ดึงข้อมูล Experiment ID
experiment = mlflow.get_experiment_by_name("model-registry-lab")
experiment_id = experiment.experiment_id

print(f"📁 ARTIFACTS_BASE: {ARTIFACTS_BASE}")
print(f"🆔 Experiment ID: {experiment_id}")

# %%
# Helper Function: ค้นหา Model ตาม flavor (sklearn, pytorch, etc.)

def find_model_path_by_flavor(artifacts_base: str, experiment_id: str, flavor: str = "sklearn") -> str:
    """
    ค้นหา model path จาก models/ folder ตาม flavor ที่ต้องการ
    (MLflow เก็บ models แยกใน models/ folder เมื่อใช้ --serve-artifacts)
    
    Args:
        artifacts_base: Base path ของ artifacts
        experiment_id: Experiment ID
        flavor: MLflow flavor ที่ต้องการ ("sklearn", "pytorch", "tensorflow", etc.)
    
    Returns:
        Full path ไปยัง model หรือ None ถ้าไม่พบ
    """
    models_folder = f"{artifacts_base}/{experiment_id}/models"
    
    if not os.path.exists(models_folder):
        print(f"⚠️ ไม่พบโฟลเดอร์: {models_folder}")
        return None
    
    # ค้นหา model folder ที่มี flavor ตรงกับที่ต้องการ
    for model_dir in os.listdir(models_folder):
        model_path = f"{models_folder}/{model_dir}/artifacts"
        mlmodel_file = f"{model_path}/MLmodel"
        
        if os.path.exists(mlmodel_file):
            # อ่าน MLmodel file เพื่อตรวจสอบ flavor
            with open(mlmodel_file, 'r') as f:
                mlmodel = yaml.safe_load(f)
            
            # ตรวจสอบว่ามี flavor ที่ต้องการหรือไม่
            if 'flavors' in mlmodel and flavor in mlmodel['flavors']:
                return model_path
    
    return None

# %%
# ค้นหาและโหลด sklearn model จาก ARTIFACTS_BASE
print("📥 โหลด Scikit-learn Model จาก ARTIFACTS_BASE:")
print("-" * 50)

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
    print("💡 ตรวจสอบว่า ARTIFACTS_BASE path ถูกต้อง")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 6: การลงทะเบียน PyTorch Model
#
# ### แนวคิด
# PyTorch Model สามารถลงทะเบียนได้เหมือนกับ Scikit-learn
# โดยใช้ `mlflow.pytorch.log_model()` พร้อม `registered_model_name`
#
# ### ข้อควรระวัง
# - ต้องสร้าง Signature ที่ถูกต้องสำหรับ PyTorch Model
# - Input ต้องเป็น numpy array dtype float32

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
        name="model",
        signature=signature,
        input_example=X_train_float32[:3],
        registered_model_name=PYTORCH_MODEL_NAME
    )
    
    pytorch_run_id_v1 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน PyTorch Model Version 1 สำเร็จ!")
    print(f"🆔 Run ID: {pytorch_run_id_v1}")

# เพิ่ม Description และ Tags ให้ PyTorch Registered Model (ทำครั้งเดียวหลังสร้าง Model แรก)
client.update_registered_model(
    name=PYTORCH_MODEL_NAME,
    description="""
    🌸 Iris Flower Classification Model (PyTorch)
    
    Purpose: จำแนกประเภทดอกไอริส 3 ชนิด (Setosa, Versicolor, Virginica)
    Architecture: Simple Neural Network (Input -> Hidden -> Output)
    Input: 4 features (float32)
    Output: 3 class logits
    
    Team: Data Science Team
    """
)

# เพิ่ม Tags ให้ Registered Model
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "task", "classification")
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "dataset", "iris")
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "team", "data-science")
client.set_registered_model_tag(PYTORCH_MODEL_NAME, "framework", "pytorch")

# เพิ่ม Description และ Tags ให้ Version 1
client.update_model_version(
    name=PYTORCH_MODEL_NAME,
    version="1",
    description="Baseline SimpleNN (hidden_size=16). Initial PyTorch version."
)
client.set_model_version_tag(PYTORCH_MODEL_NAME, "1", "architecture", "SimpleNN")
client.set_model_version_tag(PYTORCH_MODEL_NAME, "1", "status", "baseline")

print(f"✅ เพิ่ม Description และ Tags สำหรับ PyTorch Model และ Version 1 สำเร็จ!")

# %%
# Train และลงทะเบียน PyTorch Model Version 2 (Deeper Network)
with mlflow.start_run(run_name="pytorch-nn-v2"):
    
    # Hyperparameters ที่ปรับปรุง
    hidden_size = 32
    learning_rate = 0.005
    epochs = 150
    
    mlflow.log_params({
        "hidden_size": hidden_size,
        "learning_rate": learning_rate,
        "epochs": epochs,
        "model_type": "SimpleNN-Deeper"
    })
    
    # สร้าง Model ใหม่
    pytorch_model_v2 = IrisClassifier(hidden_size=hidden_size)
    
    # Training
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
    
    # Evaluate
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
    
    # ลงทะเบียนเป็น Version ใหม่
    mlflow.pytorch.log_model(
        pytorch_model=pytorch_model_v2,
        name="model",
        signature=signature,
        input_example=X_train_float32[:3],
        registered_model_name=PYTORCH_MODEL_NAME
    )
    
    pytorch_run_id_v2 = mlflow.active_run().info.run_id
    
    print(f"✅ ลงทะเบียน PyTorch Model Version 2 สำเร็จ!")
    print(f"🆔 Run ID: {pytorch_run_id_v2}")

# เพิ่ม Description และ Tags ให้ Version 2
client.update_model_version(
    name=PYTORCH_MODEL_NAME,
    version="2",
    description="Deeper SimpleNN (hidden_size=32). Improved accuracy, ready for production."
)
client.set_model_version_tag(PYTORCH_MODEL_NAME, "2", "architecture", "SimpleNN-Deeper")
client.set_model_version_tag(PYTORCH_MODEL_NAME, "2", "status", "champion")
client.set_model_version_tag(PYTORCH_MODEL_NAME, "2", "deployment_status", "production")

print(f"✅ เพิ่ม Description และ Tags สำหรับ Version 2 สำเร็จ!")

# %%
# กำหนด Aliases สำหรับ PyTorch Models
client.set_registered_model_alias(
    name=PYTORCH_MODEL_NAME,
    alias="baseline",
    version="1"
)

client.set_registered_model_alias(
    name=PYTORCH_MODEL_NAME,
    alias="champion",
    version="2"
)

print(f"✅ กำหนด Aliases สำหรับ PyTorch Models สำเร็จ!")
print(f"   - Version 1: baseline")
print(f"   - Version 2: champion")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 7: การโหลด PyTorch Model จาก Registry
#
# ### แนวคิด
# การโหลด PyTorch Model ใช้วิธีเดียวกับ Scikit-learn โดยโหลดจาก ARTIFACTS_BASE โดยตรง

# %%
# โหลด PyTorch Model จาก ARTIFACTS_BASE
print("📥 โหลด PyTorch Model จาก ARTIFACTS_BASE:")
print("-" * 50)

pytorch_model_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, flavor="pytorch")

if pytorch_model_path:
    print(f"📦 PyTorch Model Path: {pytorch_model_path}")
    
    # โหลด model
    loaded_pytorch_model = mlflow.pytorch.load_model(pytorch_model_path)
    print(f"✅ โหลด PyTorch Model สำเร็จ: {type(loaded_pytorch_model)}")
    
    # ทดสอบทำนาย
    loaded_pytorch_model.eval()
    with torch.no_grad():
        X_test_tensor = torch.FloatTensor(X_test_float32[:5])
        outputs = loaded_pytorch_model(X_test_tensor)
        _, predicted = torch.max(outputs.data, 1)
        print(f"\n🔮 ทดสอบทำนาย 5 ตัวอย่างแรก:")
        print(f"   Predictions: {predicted.numpy()}")
        print(f"   Actual:      {y_test[:5]}")
else:
    print("⚠️ ไม่พบ PyTorch model ใน ARTIFACTS_BASE")
    print("💡 ตรวจสอบว่า ARTIFACTS_BASE path ถูกต้อง")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 8: การค้นหา Models และ Versions
#
# ### แนวคิด
# MLflow Client มีฟังก์ชันค้นหาที่ทรงพลัง สามารถ Filter ตามเงื่อนไขต่างๆ ได้
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `client.search_registered_models(filter_string)` | ค้นหา Models |
# | `client.search_model_versions(filter_string)` | ค้นหา Versions |

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

# ใช้ run_id จากการ train ก่อนหน้า
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
# ### แนวคิด
# การลบ Model หรือ Version ต้องทำอย่างระมัดระวัง
#
# ### ฟังก์ชันสำคัญ
# | ฟังก์ชัน | คำอธิบาย |
# |----------|----------|
# | `client.delete_model_version(name, version)` | ลบ Version เฉพาะ |
# | `client.delete_registered_model(name)` | ลบ Model ทั้งหมด |
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

# # ลบ Model ทั้งหมด (ต้องลบ Versions ก่อน)
# client.delete_registered_model(
#     name=SKLEARN_MODEL_NAME
# )
# print("✅ ลบ Model ทั้งหมดสำเร็จ!")

print("💡 การลบเป็น Destructive Operation - ใช้อย่างระมัดระวัง!")
print("💡 แนะนำให้ใช้ Archive หรือ Alias แทนการลบ")

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 10: Best Practices สำหรับ Model Registry
#
# ### 10.1 การตั้งชื่อ Model
#
# | ✅ ชื่อที่ดี | ❌ ชื่อที่ควรหลีกเลี่ยง |
# |-------------|------------------------|
# | `fraud-detection-xgboost` | `model1` |
# | `customer-churn-predictor` | `test` |
# | `image-classifier-resnet50` | `my_model` |
# | `nlp-sentiment-bert` | `final_model_v2_REAL` |
#
# ### 10.2 การใช้ Aliases
#
# | Alias | Use Case |
# |-------|----------|
# | `champion` | Model ที่ใช้ใน Production |
# | `challenger` | Model ที่กำลังทดสอบเพื่อแทน champion |
# | `baseline` | Model แรกสำหรับเปรียบเทียบ |
# | `staging` | Model ที่กำลัง QA |
#
# ### 10.3 การใช้ Tags
#
# | Tag | ตัวอย่าง |
# |-----|----------|
# | `task` | classification, regression, clustering |
# | `framework` | sklearn, pytorch, tensorflow |
# | `team` | data-science, ml-engineering |
# | `environment` | development, staging, production |
# | `approved_by` | ชื่อผู้อนุมัติ |

# %% [markdown]
# ---
# ## 📚 ส่วนที่ 11: การดู Registry ผ่าน MLflow UI
#
# ### การเข้าถึง Model Registry UI
#
# เปิด Browser ไปที่: [http://127.0.0.1:5000/#/models](http://127.0.0.1:5000/#/models)
#
# ### ส่วนประกอบของ Model Registry UI
#
# | ส่วน | คำอธิบาย |
# |------|----------|
# | **Models List** | รายการ Registered Models ทั้งหมด |
# | **Model Details** | รายละเอียดของ Model (คลิกที่ชื่อ) |
# | **Versions Tab** | รายการ Versions ทั้งหมด |
# | **Aliases Tab** | รายการ Aliases ที่กำหนด |
# | **Tags** | แสดง Tags ของ Model |

# %%
# สรุปข้อมูล Models ที่ลงทะเบียนใน Lab นี้
print("📦 สรุป Registered Models ใน Lab นี้:")
print("=" * 60)

for model_name in [SKLEARN_MODEL_NAME, PYTORCH_MODEL_NAME]:
    model = client.get_registered_model(model_name)
    versions = client.search_model_versions(f"name = '{model_name}'")
    
    print(f"\n🏷️ {model_name}")
    print(f"   📝 Versions: {len(list(versions))}")
    print(f"   📝 Aliases: {model.aliases}")
    
    # ดึง champion version
    try:
        champion = client.get_model_version_by_alias(model_name, "champion")
        run = client.get_run(champion.run_id)
        accuracy = run.data.metrics.get("accuracy", "N/A")
        print(f"   🏆 Champion (v{champion.version}): accuracy = {accuracy:.4f if isinstance(accuracy, float) else accuracy}")
    except:
        print(f"   🏆 Champion: ไม่มี")

print(f"\n🔗 ดูรายละเอียดที่: http://127.0.0.1:5000/#/models")

# %% [markdown]
# ---
# ## 📝 สรุปบทเรียน
#
# ในบทเรียนนี้ได้เรียนรู้:
#
# | หัวข้อ | สิ่งที่เรียนรู้ |
# |--------|--------------|
# | **Model Registry คืออะไร** | ระบบจัดการ Model แบบรวมศูนย์ |
# | **การลงทะเบียน Model** | 2 วิธี: พร้อม Train หรือ ภายหลัง |
# | **Model Versions** | ติดตามทุก Version ของ Model |
# | **Model Aliases** | กำหนด Alias เช่น champion, staging |
# | **การโหลด Model** | โหลดจาก ARTIFACTS_BASE โดยตรง (เร็วที่สุด!) |
# | **Description & Tags** | เพิ่มข้อมูลให้ Model ตอนลงทะเบียน |
# | **การค้นหา** | ค้นหา Models และ Versions |
#
# ### ฟังก์ชันสำคัญที่ใช้
#
# | Category | ฟังก์ชัน |
# |----------|----------|
# | **ลงทะเบียน** | `mlflow.sklearn.log_model(..., registered_model_name)` |
# | **ลงทะเบียน (ภายหลัง)** | `mlflow.register_model(model_uri, name)` |
# | **โหลด Model (sklearn)** | `mlflow.sklearn.load_model(model_path)` |
# | **โหลด Model (pytorch)** | `mlflow.pytorch.load_model(model_path)` |
# | **ค้นหา Model Path** | `find_model_path_by_flavor(artifacts_base, experiment_id, flavor)` |
# | **กำหนด Alias** | `client.set_registered_model_alias(name, alias, version)` |
# | **เพิ่ม Description** | `client.update_registered_model(name, description)` |
# | **เพิ่ม Tag (Model)** | `client.set_registered_model_tag(name, key, value)` |
# | **เพิ่ม Tag (Version)** | `client.set_model_version_tag(name, version, key, value)` |
# | **ดู Model** | `client.get_registered_model(name)` |
# | **ดู Version** | `client.get_model_version(name, version)` |
# | **ค้นหา** | `client.search_model_versions(filter_string)` |
#
#
# ### การโหลด Model จาก ARTIFACTS_BASE
#
# ```python
# # 1. กำหนด ARTIFACTS_BASE path
# ARTIFACTS_BASE = "/path/to/mlartifacts"
#
# # 2. ใช้ find_model_path_by_flavor() ค้นหา model path
# model_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, flavor="sklearn")
#
# # 3. โหลด model
# model = mlflow.sklearn.load_model(model_path)
# ```
#
# **หมายเหตุ:** เมื่อใช้ `--serve-artifacts` กับ MLflow Server, models จะถูกเก็บในโฟลเดอร์ `models/` แยกต่างหาก

# %% [markdown]
# ---
# ## 🔗 แหล่งข้อมูลเพิ่มเติม
#
# - [MLflow Model Registry Documentation](https://mlflow.org/docs/latest/model-registry.html)
# - [MLflow Model Registry Concepts](https://mlflow.org/docs/latest/concepts.html#model-registry)
# - [MLflow Python API - Model Registry](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.register_model)
# - [Model Aliases and Tags](https://mlflow.org/docs/latest/model-registry.html#model-aliases)
#
# ---
#
# *Lab นี้จัดทำขึ้นสำหรับการเรียนรู้ MLflow Model Registry*
#
# **MLflow Server URL: http://127.0.0.1:5000**
