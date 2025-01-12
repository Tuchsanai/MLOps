# DVC Pipeline Lab for ML Project

This lab will guide you through setting up and running a DVC pipeline for a machine learning project. The project involves data preparation, model training, and evaluation using Python in a virtual environment on an Ubuntu system without Python pre-installed.


## Files Overview

- `config.yaml`: Configuration file for data paths, target columns, and model parameters.
- `data_preparation.py`: Script for data cleaning, outlier removal, and preprocessing.
- `train.py`: Script to train a machine learning model.
- `eval.py`: Script to evaluate the trained model.
- `dvc.yaml`: Defines the DVC pipeline stages and dependencies.



## Prerequisites

- Ubuntu system
- Internet connection
- Basic understanding of Python and machine learning

## Setup Instructions

### Step 1: Install Python and Required Tools

1. Update the system package index:

   ```bash
   sudo apt update
   ```


2. Install Python and `venv` (if not already installed):

   ```bash
   sudo apt install -y python3 python3-venv python3-pip
   ```


3. Install `git` for version control:

   ```bash
   sudo apt install -y git
   ```


4. Install DVC:

   ```bash
   pip install dvc dvc-gs 
   ```

### Step 2: Clone the Project Repository

1. Clone the project repository:

   ```bash
   git clone https://github.com/Tuchsanai/MLOps_Class/tree/main/02_Data_Versioning_and_pipeline/week07/LAB02
   ```

   **Output:**

   ```bash
   Cloning into 'LAB02'...
   remote: Enumerating objects...
   remote: Counting objects...
   remote: Compressing objects...
   Receiving objects...
   Resolving deltas...
   ```

2. Navigate to the project directory:

   ```bash
   cd LAB02
   ```

### Step 3: Set Up a Python Virtual Environment

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

   **Output:**

   ```bash
   (venv) $
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   **Output:**

   ```bash
   Collecting omegaconf
   Downloading omegaconf-x.x.x.tar.gz (xx kB)
   ...
   Successfully installed omegaconf-x.x.x sklearn-x.x.x ...
   ```

### Step 4: Set Up DVC

1. Initialize DVC in the project:

   ```bash
   dvc init
   ```

   **Output:**

   ```bash
   Initializing DVC repository...
   You can now commit the changes to git.
   ```

2. Add the `data` directory to DVC tracking:

   ```bash
   dvc add data/iris.csv
   ```

   **Output:**

   ```bash
   Adding 'data/iris.csv'...
   To track the changes with git, run:

   	git add data/iris.csv.dvc .gitignore
   ```

3. Commit the changes to Git:

   ```bash
   git add .
   git commit -m "Initialize DVC and add dataset"
   ```

   **Output:**

   ```bash
   [main (root-commit) xxx] Initialize DVC and add dataset
   3 files changed, xx insertions(+)
   create mode 100644 data/iris.csv.dvc
   ```

### Step 5: Create the DVC Pipeline

1. Create a `dvc.yaml` file to define the pipeline:

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

2. Commit the pipeline configuration to Git:

   ```bash
   git add dvc.yaml .gitignore
   git commit -m "Add DVC pipeline configuration"
   ```

   **Output:**

   ```bash
   [main xxxxxxx] Add DVC pipeline configuration
   1 file changed, xx insertions(+)
   create mode 100644 dvc.yaml
   ```

### Step 6: Run the Pipeline

1. Execute the pipeline:

   ```bash
   dvc repro
   ```

   **Output:**

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
   [INFO] Accuracy: 0.9333
   [INFO] F1 (weighted): 0.9333

   Pipeline completed successfully.
   ```

2. Verify the pipeline stages and outputs:

   ```bash
   dvc pipeline show --ascii
   ```

   **Output:**

   ```bash
                     +-----------------+
                     | data/iris.csv  |
                     +-----------------+
                            *
                            *
                            v
                +-----------------------+
                | data/iris_prepared.csv|
                +-----------------------+
                            *
                            *
                            v
              +---------------------------+
              | data/trained_model.pkl    |
              +---------------------------+
   ```

### Step 7: Push Data and Artifacts to Remote Storage (Optional)

1. Set up a remote storage location (e.g., Google Cloud Storage, S3, etc.):

   ```bash
   dvc remote add -d myremote gs://dvc_tp
   dvc remote modify myremote credentialpath service_account.json
   ```

   **Output:**

   ```bash
   Setting 'myremote' as a default remote.
   ```

2. Push data and artifacts to the remote:

   ```bash
   dvc push
   ```

   **Output:**

   ```bash
   To track the changes with git, run:

   	git add .dvc/config
   ...
   ```

3. Commit the remote configuration to Git:

   ```bash
   git add .dvc/config
   git commit -m "Configure remote storage"
   ```

   **Output:**

   ```bash
   [main xxxxxxx] Configure remote storage
   1 file changed, xx insertions(+)
   create mode 100644 .dvc/config
   ```

## Expected Outputs

- Cleaned and prepared dataset: `data/iris_prepared.csv`
- Trained model file: `data/trained_model.pkl`
- Evaluation metrics printed to the console.

