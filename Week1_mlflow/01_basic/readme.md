# MLflow Setup

---

## 0) Prerequisites

* Python 3.9–3.12
* `pip` and a clean virtual environment (recommended)
* OS: Linux, macOS, or Windows (PowerShell)
* Ports available: `8080` (tracking + UI)


---

## 1) Environment Setup

### 1.1 Create and activate a virtual environment

**macOS/Linux (bash):**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 1.2 Install packages

```bash
pip install mlflow scikit-learn pandas numpy 
```

> Tip: If you plan to try the model registry and serving, also install:
> `pip install mlflow[extras] fastapi uvicorn pydantic` (optional)

---

## 2) Launching the MLflow Tracking Server

You can start with the simplest ephemeral setup or a more realistic one with a SQLite backend and a local artifact store.

### 2.1 Minimal (in‑memory) quick start

```bash
mlflow server --host 127.0.0.1 --port 8080
```

Expected output (abbrev.):

```
INFO:     Started server process [28550]
INFO:     Application startup complete.
Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

Open the UI at `http://127.0.0.1:8080`.

> **Note:** Closing this terminal stops the server.

### 2.2 Recommended (persistent) setup

```bash
mkdir -p mlruns_db mlartifacts
mlflow server \
  --host 127.0.0.1 --port 8080 \
  --backend-store-uri sqlite:///mlruns_db/mlflow.db \
  --artifacts-destination ./mlartifacts \
  --serve-artifacts
```

* **Backend store**: experiment/run metadata in `sqlite:///mlruns_db/mlflow.db`
* **Artifact store**: model files and artifacts under `./mlartifacts`

### 2.3 Configure client(s) to talk to the server

In another terminal (same machine):

```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:8080        # macOS/Linux
# Windows PowerShell
# $Env:MLFLOW_TRACKING_URI = "http://127.0.0.1:8080"
```

Verify connectivity:

```bash
python -c "import mlflow; print('Tracking URI:', mlflow.get_tracking_uri())"
```

