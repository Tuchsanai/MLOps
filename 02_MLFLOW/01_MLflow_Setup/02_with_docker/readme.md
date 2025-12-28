# Lab: Getting Started with MLflow using Docker

## 1. Lab Description

In this lab, students will:

* Set up **MLflow Tracking Server** using **Docker**
* Create persistent folders for:
    * experiment metadata (`mlruns_db`)
    * artifacts (models, plots, etc.) (`mlartifacts`)
* Run MLflow server in a container and access the **MLflow UI**
* Configure a simple **MLflow client** in Python
* Run a sample experiment and visualize results in MLflow

---

## 2. Learning Objectives

By the end of this lab, you should be able to:

1. Explain the role of **MLflow Tracking Server**
2. Run MLflow server using **Docker**
3. Use **SQLite** as the backend store and a local folder as the artifact store
4. Log parameters, metrics, and artifacts from a Python script to MLflow
5. View and compare runs in the **MLflow UI**

---

## 3. Lab Pipeline (Step-by-Step)

### Step 0 – Prepare Working Directory

#### 🐧 For Linux / macOS (Bash):

1. Create a main lab folder (if it does not exist) and enter it:

```bash
mkdir -p mlflow-lab
cd mlflow-lab
```

2. Create the required subdirectories for MLflow data:

```bash
mkdir -p mlruns_db mlartifacts
```

3. **Verify the folder structure:**

```bash
ls -F
```

#### 🪟 For Windows (Command Prompt / cmd):

1. Create a main lab folder (if it does not exist) and enter it:

```cmd
mkdir mlflow-lab
cd mlflow-lab
```

2. Create the required subdirectories for MLflow data:

```cmd
mkdir mlruns_db
mkdir mlartifacts
```

3. **Verify the folder structure:**

```cmd
dir
```

---

> **✅ Expected Output:**
> You should see the two folders:
>
> **Linux/macOS:**
> ```text
> mlartifacts/
> mlruns_db/
> ```
>
> **Windows (cmd):**
> ```text
> <DIR>          mlartifacts
> <DIR>          mlruns_db
> ```

---

### Step 1 – Start MLflow Server with Docker

Run the following Docker command **inside the `mlflow-lab` folder**.

#### 🐧 For Linux / macOS (Bash):

```bash
docker run -d \
  --name mlflow-server \
  -p 5000:5000 \
  -v "$(pwd)/mlruns_db:/mlflow/db" \
  -v "$(pwd)/mlartifacts:/mlflow/artifacts" \
  ghcr.io/mlflow/mlflow \
  mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:////mlflow/db/mlflow.db \
  --default-artifact-root /mlflow/artifacts
```

#### 🪟 For Windows (Command Prompt / cmd):

```cmd
docker run -d ^
  --name mlflow-server ^
  -p 5000:5000 ^
  -v "%cd%/mlruns_db:/mlflow/db" ^
  -v "%cd%/mlartifacts:/mlflow/artifacts" ^
  ghcr.io/mlflow/mlflow ^
  mlflow server ^
  --host 0.0.0.0 ^
  --port 5000 ^
  --backend-store-uri sqlite:////mlflow/db/mlflow.db ^
  --default-artifact-root /mlflow/artifacts
```

**Explanation for students:**

* `-p 5000:5000` – expose MLflow UI on `http://localhost:5000`
* `-v "$(pwd)/mlruns_db:/mlflow/db"` – map local folder → container DB folder
* `-v "$(pwd)/mlartifacts:/mlflow/artifacts"` – map local folder → artifacts
* `--backend-store-uri ...` – tells MLflow to use the SQLite DB file inside the container
* `--default-artifact-root ...` – tells MLflow to store large files (models) in the artifact folder

Check that the container is running:

```bash
docker ps
```

You should see `mlflow-server` in the list.

---

### Step 2 – Open MLflow UI

1. Open a browser and go to:

   **http://localhost:5000**

2. You should see the **MLflow UI** (Experiments page).

   * For now, it will be empty (no runs yet).

---

<!-- 
NOTE: The original lab appears to be truncated here. 
Based on the Lab Description and Learning Objectives, the following steps should be added:
- Step 3: Configure MLflow Client in Python
- Step 4: Run a Sample Experiment
- Step 5: View and Compare Results in MLflow UI
-->