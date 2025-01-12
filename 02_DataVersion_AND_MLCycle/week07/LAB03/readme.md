

# DVC Pipeline Lab for ML Project

This lab will guide you through setting up and running a DVC pipeline for a machine learning project. The project covers the following stages:

1. Data preparation  
2. Model training  
3. Model evaluation  

You will use Python within a virtual environment on an Ubuntu system where Python may not be pre-installed.

---

## File Overview

- **config.yaml**: Configuration file for data paths, target columns, and model parameters.  
- **data_preparation.py**: Cleans data, removes outliers, and does basic preprocessing.  
- **train.py**: Trains a machine learning model.  
- **eval.py**: Evaluates the trained model.  
- **dvc.yaml**: Defines DVC pipeline stages, dependencies, and outputs.  
- **requirements.txt**: Lists required Python dependencies.  

---

## Prerequisites

- Ubuntu system (with internet access)  
- Basic understanding of Python and machine learning  
- Git installed  

---

## Setup Instructions

### 1. Install Python and Required Tools

1. **Update the package index**:
   ```bash
   sudo apt update
   ```

2. **Install Python, `venv`, and `pip`**:
   ```bash
   sudo apt install -y python3 python3-venv python3-pip
   ```

3. **Install Git** (if you haven’t already):
   ```bash
   sudo apt install -y git
   ```

---

### 2. Clone the Project Repository

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tuchsanai/MLOps.git
   ```
   **Example output**:
   ```bash
   Cloning into 'MLOps'...
   remote: Enumerating objects: 1564, done.
   remote: Counting objects: 100% (113/113), done.
   remote: Compressing objects: 100% (86/86), done.
   remote: Total 1564 (delta 41), reused 89 (delta 19), pack-reused 1451 (from 2)
   Receiving objects: 100% (1564/1564), 123.85 MiB | 13.21 MiB/s, done.
   Resolving deltas: 100% (397/397), done.
   ```

2. **Navigate to the project directory**:
   ```bash
   cd MLOps/02_DataVersion_AND_MLCycle/week07/LAB03
   ```

---

### 3. Set Up a Python Virtual Environment

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```
   Your prompt should now look like:
   ```bash
   (venv) $
   ```

3. **Install required Python packages**:
   ```bash
   pip install pandas scikit-learn omegaconf joblib
   pip install dvc dvc-gs
   ```
   Alternatively, if a `requirements.txt` file is available:
   ```bash
   pip install -r requirements.txt
   ```

---

### 4. Initialize DVC

1. **Initialize Git and DVC**:
   ```bash
   git init
   dvc init
   ```
   **Example output**:
   ```bash
   Initializing DVC repository...
   You can now commit the changes to git.
   ```

2. **Add the `data` directory to DVC**:
   ```bash
   dvc add data/iris.csv
   ```
 

3. **Commit these changes to Git**:
   ```bash
   git add .
   git commit -m "Initialize DVC and add dataset"
   ```
   **Example output**:
   ```bash
   [main (root-commit) xxx] Initialize DVC and add dataset
   3 files changed, xx insertions(+)
   create mode 100644 data/iris.csv.dvc
   ```

---

### 5. Create the DVC Pipeline

1. **Create or update the `dvc.yaml` file** (in the current directory):
   ```yaml
   stages:
     prepare:
       cmd: python data_preparation.py
       deps:
         - data/iris.csv
         - data_preparation.py
       outs:
         - data/iris_prepared.csv

     train:
       cmd: python train.py
       deps:
         - data/iris_prepared.csv
         - train.py
       outs:
         - data/trained_model.pkl

     evaluate:
       cmd: python eval.py
       deps:
         - data/iris_prepared.csv
         - eval.py
         - data/trained_model.pkl
   ```

2. **Commit the DVC pipeline configuration**:
   ```bash
   git add dvc.yaml .gitignore
   git commit -m "Add DVC pipeline configuration"
   ```
   **Example output**:
   ```bash
   [main xxxxxxx] Add DVC pipeline configuration
   1 file changed, xx insertions(+)
   create mode 100644 dvc.yaml
   ```

---

### 6. Run the Pipeline

1. **Reproduce (run) the pipeline**:
   ```bash
   dvc repro
   ```
   **Example output**:
   ```bash
   'data/iris_prepared.csv' didn't exist. Stage 'prepare' is being run:
   > python data_preparation.py
   [INFO] Loaded raw data shape: (150, 5)
   [INFO] Removed 0 duplicate rows.
   [INFO] Removed 0 rows containing NaN values.
   [INFO] Data shape after outlier removal: (150, 5)
   [INFO] Converted 'species' to numeric labels.
   [INFO] Data prepared and saved to data/iris_prepared.csv
   ...
   Stage 'train' is being run:
   > python train.py
   [INFO] Model trained and saved to data/trained_model.pkl
   ...
   Stage 'evaluate' is being run:
   > python eval.py
   [INFO] Accuracy: 0.8961
   [INFO] F1 (weighted): 0.8961

   Pipeline completed successfully.
   ```

2. **Visualize the pipeline (optional)**:
   ```bash
   dvc dag
   ```
   **Example output**:
    +-------------------+
    | data/iris.csv.dvc |
    +-------------------+
            *
            *
            *
       +---------+
       | prepare |
       +---------+
       **       **
     **           *
    *              **
+-------+            *
| train |          **
+-------+         *
      **       **
        **   **
          * *
     +----------+
     | evaluate |
     +----------+

  


