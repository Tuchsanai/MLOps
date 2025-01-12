

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


```python
# data_preparation.py

import os
import pandas as pd
import numpy as np
from omegaconf import OmegaConf
from sklearn.preprocessing import LabelEncoder

def remove_outliers_iqr(df, column, threshold=1.5):
    """
    Removes rows from df where the specified column has outliers
    based on the IQR (Interquartile Range) method.
    
    threshold=1.5 is a common default; 3.0 is more conservative.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    # Filter out rows that are outside [lower_bound, upper_bound]
    mask = (df[column] >= lower_bound) & (df[column] <= upper_bound)
    df_cleaned = df[mask]
    return df_cleaned

def main():
    # 1. Load config
    config = OmegaConf.load("config.yaml")
    
    # 2. Read the raw data
    data_path = os.path.join(config.data.path, config.data.file_name)
    df = pd.read_csv(data_path)
    print("[INFO] Loaded raw data shape:", df.shape)

    # 3a. Remove duplicate rows (if any)
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    print(f"[INFO] Removed {initial_count - len(df)} duplicate rows.")

    # 3b. Drop rows with NaN values (if any)
    before_na = len(df)
    df.dropna(inplace=True)
    print(f"[INFO] Removed {before_na - len(df)} rows containing NaN values.")

    # 3c. Remove outliers using IQR for all numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        df = remove_outliers_iqr(df, col, threshold=1.5)
    print("[INFO] Data shape after outlier removal:", df.shape)

    # 3d. Encode the target column if it is categorical
    target_col = config.data.target_column
    if df[target_col].dtype == object:
        le = LabelEncoder()
        df[target_col] = le.fit_transform(df[target_col])
        print(f"[INFO] Converted '{target_col}' to numeric labels.")

    # 4. Save prepared data
    prepared_data_path = os.path.join(config.data.path, "iris_prepared.csv")
    df.to_csv(prepared_data_path, index=False)
    print(f"[INFO] Data prepared and saved to {prepared_data_path}")
    print("[INFO] Final prepared data shape:", df.shape)

if __name__ == "__main__":
    main()
```


```python
# train.py
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from omegaconf import OmegaConf

def main():
    # 1. Load config
    config = OmegaConf.load("config.yaml")

    # 2. Load prepared data
    prepared_data_path = os.path.join(config.data.path, "iris_prepared.csv")
    df = pd.read_csv(prepared_data_path)

    # 3. Separate features and target
    target_column = config.data.target_column
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # 4. Split data into train & test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.training.test_size,
        random_state=config.training.random_state
    )

    # 5. Choose model type based on config
    model_type = config.model.type
    if model_type == "logistic_regression":
        model = LogisticRegression(
            max_iter=config.model.hyperparameters.get("max_iter", 100)
        )
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier(
            max_depth=config.model.hyperparameters.get("max_depth", None),
            random_state=config.training.random_state
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # 6. Train model
    model.fit(X_train, y_train)
    
    # 7. Save the trained model
    model_path = os.path.join(config.data.path, "trained_model.pkl")
    joblib.dump(model, model_path)
    print(f"[INFO] Model trained and saved to {model_path}")

if __name__ == "__main__":
    main()
```


```python
# eval.py
import os
import joblib
import pandas as pd
from omegaconf import OmegaConf
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

def main():
    # 1. Load config
    config = OmegaConf.load("config.yaml")

    # 2. Load prepared data
    prepared_data_path = os.path.join(config.data.path, "iris_prepared.csv")
    df = pd.read_csv(prepared_data_path)

    # 3. Separate features and target
    target_column = config.data.target_column
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # 4. Split data (same split as in train.py)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.training.test_size,
        random_state=config.training.random_state
    )

    # 5. Load the trained model
    model_path = os.path.join(config.data.path, "trained_model.pkl")
    model = joblib.load(model_path)

    # 6. Predict on test set
    y_pred = model.predict(X_test)

    # 7. Evaluate metrics
    metrics_list = config.evaluation.metrics
    for metric in metrics_list:
        if metric.lower() == "accuracy":
            acc = accuracy_score(y_test, y_pred)
            print(f"[INFO] Accuracy: {acc:.4f}")
        elif metric.lower() == "f1":
            # Weighted average for multi-class
            f1 = f1_score(y_test, y_pred, average="weighted")
            print(f"[INFO] F1 (weighted): {f1:.4f}")
        else:
            print(f"[WARN] Metric '{metric}' is not implemented.")

if __name__ == "__main__":
    main()
```


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
   
   ```
         
         +-------------------+  
         | data/iris.csv.dvc |  
         +-------------------+  
                  *            
                  *            
                  *            
               +---------+       
               | prepare |       
               +---------+       
               **        **      
            **            *     
            *               **   
      +-------+               *  
      | train |             **   
      +-------+            *     
               **        **      
               **    **        
                  *  *          
            +----------+       
            | evaluate |       
            +----------+       

   
   ```

  


