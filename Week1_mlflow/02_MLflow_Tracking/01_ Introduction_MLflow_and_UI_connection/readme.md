
# 🚀 Introduction to MLflow Tracking – Hello World

## 🎯 Objective

In this lab, you will learn the fundamentals of **MLflow Tracking** and explore the **MLflow UI**.
You will practice how to:

* Launch and connect to the MLflow Tracking Server
* Create and manage experiments
* Log parameters, metrics, and artifacts
* Visualize results in the MLflow UI

This lab serves as your **first step** toward experiment management and reproducible ML workflows.

---

## 📦 Step 0: Setup Environment

Before starting, install the required Python packages:

```bash
pip install mlflow scikit-learn pandas numpy
```

✅ After installation, verify MLflow is available:

```bash
mlflow --version
```

---

## ⚙️ Step 1: Launch MLflow Tracking Server

You have two options to start the tracking server:

### 🔹 Method 1: Quick Start (In-Memory Backend)

```bash
mlflow server --host 127.0.0.1 --port 8080
```

* Uses in-memory storage (data lost when process ends).
* Best for **quick demos**.

---

### 🔹 Method 2: Persistent Tracking with SQLite + Local Artifacts

Instead of just `mlflow ui`, run MLflow with a **persistent backend** and **artifact store**:

```bash
mkdir -p mlruns_db mlartifacts
mlflow server \
  --host 127.0.0.1 --port 8080 \
  --backend-store-uri sqlite:///mlruns_db/mlflow.db \
  --artifacts-destination ./mlartifacts \
  --serve-artifacts
```

💡 Explanation of flags:

* **Backend Store URI** → Saves experiments, runs, params, metrics in SQLite.
* **Artifacts Destination** → Stores logged files (plots, models, text files).
* **Serve Artifacts** → Makes artifacts browsable via MLflow UI.

---

## 🌐 Step 2: Connect to MLflow UI

Once the server is running, open your browser at:

👉 [http://127.0.0.1:8080](http://127.0.0.1:8080)

Here you can view **experiments**, explore **runs**, and inspect **artifacts**.

---

## 📝 Step 3: Create Your First Experiment (Jupyter Notebook)

Follow these steps in a Jupyter Notebook:

### 🔹 Cell 1: Import Dependencies

```python
import mlflow
import mlflow.sklearn
from datetime import datetime
```

---

### 🔹 Cell 2: Set Experiment Name

```python
mlflow.set_experiment("Lab1_Hello_MLflow")
```

---

### 🔹 Cell 3: Run Experiment – Log Parameters, Metrics, and Artifacts

```python
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)
    
    # Log metrics
    mlflow.log_metric("accuracy", 0.85)
    mlflow.log_metric("loss", 0.15)
    
    # Log an artifact (text file)
    with open("hello.txt", "w") as f:
        f.write(f"Hello MLflow! Time: {datetime.now()}")
    mlflow.log_artifact("hello.txt")
    
    print("✅ Run completed! Check MLflow UI")
```

📊 Example UI view:
![Experiment Overview](./img/1.png)
![Run Details](./img/2.png)
![Artifact Browser](./img/3.png)
![Artifact Browser1](./img/31.png)


---

### 🔹 Cell 4: Simulating Metrics Over Time

```python
import mlflow, os, time
mlflow.set_experiment("Lab1_Hello_MLflow")

with mlflow.start_run(run_name="hello-run"):
    # Params
    mlflow.log_param("learning_rate", 0.05)
    mlflow.log_param("batch_size", 64)

    # Metrics (simulate improvement)
    for step, acc in enumerate([0.78, 0.81, 0.84]):
        mlflow.log_metric("accuracy", acc, step=step)
        time.sleep(0.2)

    # Artifact
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/readme.txt", "w") as f:
        f.write("Hello MLflow! This file is tracked as an artifact.")
    mlflow.log_artifact("artifacts/readme.txt")

print("✅ Lab 1 complete. Check MLflow UI → Experiments → Lab1_Hello_MLflow.")
```

📊 Example UI view:
![Metrics Visualization](./img/4.png)
![Run Comparisons](./img/5.png)
![Artifacts View](./img/6.png)

---

## 🖥️ MLflow UI Walkthrough

When you open the MLflow UI, you’ll see:

* **Experiment List** → Displays all available experiments (e.g., `Lab1_Hello_MLflow`).
* **Runs Table** → Each run shows parameters, metrics, and status.
* **Run Detail Page** → Drill down into metrics charts, logged artifacts, and tags.
* **Artifact Browser** → Access files and outputs logged during runs.

---

✨ **Congratulations!**
You have successfully launched MLflow, created experiments, logged runs, and explored results in the MLflow UI. This is the foundation for **tracking, comparing, and reproducing ML experiments** in future labs.

---

Do you want me to also **add a "Next Steps" section** at the end (like Lab 2 preview → Model Training & Signature Inference), so it smoothly connects to your step-by-step lab series?
