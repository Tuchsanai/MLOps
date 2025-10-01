
---

## Slide 1: หัวข้อหลัก
**MLflow คืออะไร (What is MLflow?)**

* MLflow = แพลตฟอร์ม **Open Source** สำหรับจัดการ **วงจรชีวิตของ Machine Learning (ML Lifecycle)**
* **พัฒนาโดย Databricks** ในปี 2018 และปล่อยเป็น Open Source
* ครอบคลุมตั้งแต่:
  * การทดลอง (Experimentation)
  * ความสามารถทำซ้ำได้ (Reproducibility)  
  * การนำไปใช้งาน (Deployment)
  * การจัดเก็บโมเดลแบบรวมศูนย์ (Model Registry)

**ทำไมต้อง MLflow?**
* แก้ปัญหาการขาดเครื่องมือมาตรฐานใน ML Operations
* ช่วยให้ทีม Data Science ทำงานร่วมกันได้อย่างมีประสิทธิภาพ
* ลดความซับซ้อนในการจัดการโมเดล ML

---

## Slide 2: ปัญหาก่อนมี MLflow
**Pain Points ที่นักวิจัย/วิศวกร ML มักเจอ:**

* 🔎 **ยากต่อการติดตามว่า Run ไหนดีที่สุด**
  * ลองหลายพารามิเตอร์แล้วลืมว่าชุดไหนให้ผลดี
  * ไม่มีระบบเปรียบเทียบผลลัพธ์

* 📂 **การจัดเก็บโมเดลไม่เป็นระบบ**
  * โมเดลกระจัดกระจายในหลายโฟลเดอร์
  * ไม่รู้ว่าโมเดลไหนคือ version ล่าสุด

* ⚙️ **การ deploy ไป production ซับซ้อน**
  * ต้องเขียนโค้ด API เอง
  * ปัญหา dependency และ environment ไม่ตรงกัน

* 🧩 **แต่ละองค์กรใช้ Framework ต่างกัน**
  * scikit-learn, PyTorch, TensorFlow, XGBoost
  * ไม่มีมาตรฐานเดียวกันในการจัดการ

* 👥 **ความร่วมมือในทีมยาก**
  * แชร์โมเดลและผลการทดลองลำบาก
  * Reproducibility ต่ำ

---

## Slide 3: โครงสร้างของ MLflow
**MLflow มี 4 คอมโพเนนต์หลัก**

### 1. **MLflow Tracking** 🔍
- บันทึกและติดตาม experiments
- เก็บ metrics, parameters, artifacts
- มี UI สำหรับดูผลลัพธ์

### 2. **MLflow Projects** 📦
- จัดแพ็กเกจโค้ด ML ให้ reproducible
- กำหนด dependencies และ environment
- รันได้บนหลาย platform

### 3. **MLflow Models** 🤖
- รูปแบบมาตรฐานสำหรับจัดเก็บโมเดล
- Support หลาย ML framework
- Deploy ได้หลายวิธี

### 4. **MLflow Model Registry** 🏛️
- ระบบ version control และ governance
- จัดการ lifecycle ของโมเดล
- Collaboration และ approval workflow

---

## Slide 4: MLflow Tracking - รายละเอียด
**ใช้บันทึกการทดลอง ML อย่างเป็นระบบ**

### สิ่งที่ Track ได้:
* **Parameters** - ค่าที่เราตั้งก่อนรันโมเดล
  * Hyperparameters เช่น learning_rate, alpha, n_estimators
  * Data preprocessing settings
  
* **Metrics** - ผลลัพธ์ที่วัดได้จากโมเดล
  * RMSE, Accuracy, F1-Score, AUC
  * สามารถ log หลายค่าในรันเดียว
  
* **Artifacts** - ไฟล์ต่างๆ ที่เกี่ยวข้อง
  * Model files (.pkl, .h5)
  * การ visualization (plots, confusion matrix)
  * Dataset samples, feature importance

### ตัวอย่างโค้ด:
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# เริ่ม run
with mlflow.start_run():
    # Log parameters
    n_estimators = 100
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", 42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    
    # Predict and log metrics
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")
```

### MLflow UI Features:
* เปรียบเทียบ runs ที่ต่างกัน
* กรองและเรียงลำดับตาม metrics
* ดู artifacts และ plots
* Export ข้อมูลเป็น CSV

---

## Slide 5: MLflow Projects - รายละเอียด
**ทำให้โค้ด ML รันซ้ำได้ทุกที่ (Reproducible)**

### ส่วนประกอบหลัก:
* **MLproject file** - กำหนดการตั้งค่า
* **conda.yaml** - environment dependencies  
* **โค้ด Python** - logic หลักของ ML

### ตัวอย่าง MLproject file:
```yaml
name: wine-quality-prediction

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
      l1_ratio: {type: float, default: 0.1}
    command: "python train.py {alpha} {l1_ratio}"
  
  evaluate:
    parameters:
      model_path: string
    command: "python evaluate.py {model_path}"
```

### ตัวอย่าง conda.yaml:
```yaml
name: wine-quality
channels:
  - conda-forge
dependencies:
  - python=3.8
  - pandas=1.3.0
  - scikit-learn=0.24.2
  - mlflow=1.20.0
  - pip
  - pip:
    - matplotlib==3.4.2
```

### การรัน Project:
```bash
# รันจาก GitHub
mlflow run https://github.com/mlflow/mlflow-example

# รันจาก local directory
mlflow run . -P alpha=0.8 -P l1_ratio=0.2

# รันบน specific environment
mlflow run . --no-conda
```

---

## Slide 6: MLflow Models - รายละเอียด
**รูปแบบมาตรฐานสำหรับจัดเก็บและ deploy โมเดล**

### Supported Frameworks:
* **Traditional ML**: scikit-learn, XGBoost, LightGBM
* **Deep Learning**: TensorFlow, Keras, PyTorch
* **Statistical**: Statsmodels, Prophet
* **Custom**: Python function, R, Java

### Model Flavor คืออะไร?
แต่ละ framework มี "flavor" เป็นของตัวเอง:
```python
# Scikit-learn flavor
mlflow.sklearn.log_model(model, "sklearn_model")

# PyTorch flavor  
mlflow.pytorch.log_model(model, "pytorch_model")

# Custom Python function
mlflow.pyfunc.log_model("custom_model", python_model=wrapper)
```

### โครงสร้างของ MLflow Model:
```
my_model/
├── MLmodel              # Metadata file
├── model.pkl           # Actual model file
├── conda.yaml          # Dependencies
├── python_env.yaml     # Python environment
└── requirements.txt    # Pip requirements
```

### การ Deploy:
```bash
# Local REST API server
mlflow models serve -m models:/my_model/1 -p 5000

# Docker container
mlflow models build-docker -m models:/my_model/1 -n my_model_image

# Cloud deployment (AWS SageMaker)
mlflow deployments create -t sagemaker -m models:/my_model/1
```

### การใช้งานโมเดลที่ deploy แล้ว:
```python
import requests
import json

# ส่ง request ไป REST API
data = {"inputs": [[5.1, 3.5, 1.4, 0.2]]}
response = requests.post(
    "http://localhost:5000/invocations",
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
)
print(response.json())  # [0] (prediction result)
```

---

## Slide 7: Model Registry - รายละเอียด
**ระบบบริหารจัดการโมเดลอย่างเป็นระบบ**

### Model Stages:
1. **None** - โมเดลที่เพิ่งจดทะเบียน
2. **Staging** - โมเดลที่อยู่ระหว่างทดสอบ
3. **Production** - โมเดลที่ใช้งานจริง
4. **Archived** - โมเดลเก่าที่เก็บไว้อ้างอิง

### การจัดการโมเดลผ่าน Python API:
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# สร้าง registered model
model_name = "iris_classifier"
client.create_registered_model(model_name)

# เพิ่ม model version จาก run
run_id = "abc123"
model_uri = f"runs:/{run_id}/model"
client.create_model_version(
    name=model_name,
    source=model_uri,
    description="Random Forest trained on iris dataset"
)

# เปลี่ยน stage
client.transition_model_version_stage(
    name=model_name,
    version=1,
    stage="Production"
)

# เพิ่ม description/tags
client.update_model_version(
    name=model_name,
    version=1,
    description="Best performing model - 95% accuracy"
)
```

### Model Registry Features:
* **Version Control** - เก็บ history ของโมเดลทุก version
* **Stage Management** - จัดการ lifecycle อย่างเป็นระบบ
* **Annotations** - เพิ่ม comments และ descriptions
* **Webhooks** - integrate กับระบบอื่น
* **Access Control** - กำหนดสิทธิ์การเข้าถึง

---

## Slide 8: การใช้งานจริงใน Workflow
**End-to-end ML Workflow พร้อมตัวอย่างจริง**

### 1. **นักวิจัย ML** → สร้างโมเดล + track experiment
```python
# experiment.py
import mlflow
from sklearn.model_selection import GridSearchCV

mlflow.set_experiment("iris_classification")

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7]
}

for params in ParameterGrid(param_grid):
    with mlflow.start_run():
        # Log parameters
        mlflow.log_params(params)
        
        # Train model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Evaluate and log metrics
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log model if performance is good
        if accuracy > 0.90:
            mlflow.sklearn.log_model(model, "model")
```

### 2. **ทีม Data Engineer** → จัดแพ็กเกจเป็น Project
```yaml
# MLproject
name: iris_classifier_production

conda_env: conda.yaml

entry_points:
  train:
    parameters:
      data_path: {type: string, default: "data/iris.csv"}
      model_name: {type: string, default: "iris_classifier"}
    command: "python train.py --data-path {data_path} --model-name {model_name}"
  
  batch_predict:
    parameters:
      model_uri: string
      input_path: string
      output_path: string  
    command: "python predict.py --model-uri {model_uri} --input {input_path} --output {output_path}"
```

### 3. **ทีม MLOps** → Deploy และจัดการโมเดลใน Registry
```python
# deploy.py
from mlflow.tracking import MlflowClient
import mlflow.deployments

client = MlflowClient()

# Get best model from experiment
experiment = client.get_experiment_by_name("iris_classification")
runs = client.search_runs(experiment.experiment_id, order_by=["metrics.accuracy DESC"])
best_run = runs[0]

# Register the best model
model_uri = f"runs:/{best_run.info.run_id}/model"
registered_model = client.create_model_version(
    name="iris_classifier_prod",
    source=model_uri
)

# Deploy to production
mlflow.deployments.create_deployment(
    name="iris-api",
    model_uri=f"models:/iris_classifier_prod/{registered_model.version}",
    target_uri="http://my-mlflow-server"
)
```

### 4. **ธุรกิจ/แอปพลิเคชัน** → ใช้โมเดล Production
```python
# application.py
import mlflow.pyfunc

# Load production model
model = mlflow.pyfunc.load_model("models:/iris_classifier_prod/Production")

# Use in application
def predict_iris_species(sepal_length, sepal_width, petal_length, petal_width):
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(input_data)
    species_map = {0: "setosa", 1: "versicolor", 2: "virginica"}
    return species_map[prediction[0]]

# Example usage
result = predict_iris_species(5.1, 3.5, 1.4, 0.2)
print(f"Predicted species: {result}")
```

---

## Slide 9: Key Benefits ของ MLflow
**ข้อดีที่ทำให้ MLflow เป็นที่นิยม**

### ✅ **Framework Agnostic** - ใช้ได้กับ Framework หลากหลาย
* ไม่ต้องเปลี่ยน workflow เดิม
* Support ทั้ง traditional ML และ deep learning
* Plugin architecture สำหรับ framework ใหม่ๆ

### ✅ **ติดตาม Experiment ได้ง่าย**
* UI ที่ user-friendly สำหรับเปรียบเทียบ runs
* Automatic logging สำหรับ popular libraries
* Search และ filter experiments ได้อย่างละเอียด

### ✅ **Deploy สะดวก (Multi-platform)**
* One-click deployment to REST API
* Support cloud platforms หลักๆ
* Batch inference และ real-time serving

### ✅ **บริหารจัดการโมเดลแบบ Version Control**
* Git-like versioning สำหรับ ML models
* Stage management และ approval workflow
* Lineage tracking - รู้ว่าโมเดลมาจาก experiment ไหน

### ✅ **Open Source และ Active Community**
* ฟรี ไม่มีค่าใช้จ่าย
* Community plugins และ integrations
* Enterprise support จาก Databricks

### ✅ **Integration ที่หลากหลาย**
* Apache Spark, Kubernetes, Docker
* Cloud services: AWS, Azure, GCP
* Popular ML tools: Jupyter, Docker, Git

---

## Slide 10: สรุป
**MLflow = One-stop Platform สำหรับ Machine Learning Lifecycle**

### จากต้นจนจบ: **Experiment → Reproduce → Deploy → Manage**

#### 🔄 **Complete ML Lifecycle Management**
* ไม่ต้องใช้หลายเครื่องมือแยกกัน
* Seamless workflow จาก research ถึง production
* ลดเวลาในการจัดการ infrastructure

#### 🚀 **เตรียมพร้อมสำหรับการเรียนต่อ**
* ติดตั้ง MLflow: `pip install mlflow`
* เริ่มต้น tracking server: `mlflow ui`
* ทดลองกับ example projects จาก GitHub

#### 📚 **แหล่งเรียนรู้เพิ่มเติม**
* [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
* [MLflow GitHub Examples](https://github.com/mlflow/mlflow/tree/master/examples)
* [Databricks MLflow Tutorials](https://docs.databricks.com/mlflow/index.html)

### 💡 **ข้อควรจำ**
MLflow ไม่ใช่แค่เครื่องมือ แต่เป็น **methodology** ในการทำ ML อย่างเป็นระบบและมีมาตรฐาน ช่วยให้ทีมทำงานร่วมกันได้อย่างมีประสิทธิภาพและโมเดลสามารถนำไปใช้งานจริงได้

---

## Slide เพิ่มเติม: ตัวอย่างการติดตั้งและเริ่มต้น

### การติดตั้ง MLflow
```bash
# ติดตั้งพื้นฐาน
pip install mlflow

# ติดตั้งพร้อม dependencies เพิ่มเติม
pip install mlflow[extras]

# หรือใช้ conda
conda install -c conda-forge mlflow
```

### เริ่มต้นใช้งาน
```bash
# เริ่ม MLflow UI
mlflow ui

# เริ่มที่ port อื่น
mlflow ui --port 5001

# ตั้งค่า backend store (สำหรับ production)
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

### ตัวอย่างโค้ดเบื้องต้น
```python
import mlflow
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ตั้งชื่อ experiment
mlflow.set_experiment("my_first_experiment")

# สร้างข้อมูลตัวอย่าง
X = np.random.randn(100, 1)
y = 2 * X.squeeze() + np.random.randn(100)

# เริ่ม MLflow run
with mlflow.start_run():
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    
    # Log parameters and metrics
    mlflow.log_param("n_samples", len(X))
    mlflow.log_metric("mse", mse)
    
    # Log model
    mlflow.sklearn.log_model(model, "linear_regression")
    
    print(f"MSE: {mse}")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
```

หลังจากรันโค้ดนี้ สามารถไปดูผลลัพธ์ได้ที่ http://localhost:5000