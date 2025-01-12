Below is the **complete MLOps lab** that demonstrates how to use **OmegaConf** for configuration management in a simple ML workflow on the **Iris dataset**. It includes:

1. A **config.yaml** file for all configuration.  
2. Three **Python scripts** for the pipeline:  
   - **data_preparation.py**: Loads and prepares/cleans the data.  
   - **train.py**: Trains the model.  
   - **eval.py**: Evaluates the model.  
3. **Ubuntu** setup instructions for installing Python and dependencies.  
4. Instructions for **cloning** the repository from GitHub.

---

## 1. Repository Structure

Once you **clone** the repository from:

> [https://github.com/Tuchsanai/MLOps/tree/main/03_Automating_MLLearning_Cycle/week07/LAB02](https://github.com/Tuchsanai/MLOps/tree/main/03_Automating_MLLearning_Cycle/week07/LAB02)

You’ll see something like:

```
├── data/
│   └── iris.csv             <- Your raw dataset
├── config.yaml              <- OmegaConf configuration file
├── data_preparation.py      <- Script to clean/prepare data
├── train.py                 <- Script to train model
├── eval.py                  <- Script to evaluate model
└── README.md                <- This file with instructions
```

---

## 2. Cloning the Project

**Steps** to clone or download:

1. **Navigate** to a directory on your machine where you want to store the project.
2. Run the following in your terminal:
   ```bash
   git clone https://github.com/Tuchsanai/MLOps.git
   ```
3. Then **navigate** to the lab folder:
   ```bash
   cd MLOps/02_Auto_DataVersion_AND_MLCyCle/week07/LAB02
   ```
4. You should now see the files listed above (e.g., `config.yaml`, `data_preparation.py`, etc.).

---

## 3. Ubuntu Setup: Python & Virtual Environment

Since the Ubuntu system has no Python installed, let’s install Python and set up a **virtual environment**:

1. **Update apt** and install Python 3, pip, and venv:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip python3-venv
   ```
2. **Create a virtual environment** (e.g., named `venv`):
   ```bash
   python3 -m venv venv
   ```
3. **Activate** the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. **Install required Python packages** (e.g., `pandas`, `scikit-learn`, `OmegaConf`):
   ```bash
   pip install pandas scikit-learn omegaconf joblib
   ```

> **Tip**: In a production setting, you might store your package requirements in a `requirements.txt`.

---

## 4. Configuration File: `config.yaml`

Below is an **example** configuration file using **OmegaConf**. You can customize it as needed.

```yaml
data:
  path: "./data/"
  file_name: "iris.csv"
  target_column: "species"

model:
  type: "logistic_regression"  # Options: "logistic_regression" or "decision_tree"
  hyperparameters:
    # LogisticRegression params
    max_iter: 200
    # DecisionTreeClassifier params
    # max_depth: 3

training:
  test_size: 0.2
  random_state: 42

evaluation:
  metrics:
    - "accuracy"
    - "f1"
```

**Key Points**  
- `data.path` & `data.file_name`: Specifies where to load the raw data.  
- `data.target_column`: The name of the column to predict.  
- `model.type`: A switch to pick between logistic regression or a decision tree.  
- `model.hyperparameters`: Key/value pairs for model-specific settings.  
- `training.test_size`: The fraction of the dataset used for testing.  
- `training.random_state`: Random seed for reproducibility.  
- `evaluation.metrics`: The metrics to compute (e.g., accuracy, F1-score).

---

## 5. Data Preparation: `data_preparation.py`

Below is a more **extensive** data preparation script that includes common cleaning tasks: removing duplicates, dropping NaNs, handling outliers via IQR, and optional label encoding for the target column.

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

### What This Script Does

1. **Load Config**: Uses OmegaConf to load `config.yaml`.  
2. **Load Data**: Reads the raw CSV (`iris.csv`).  
3. **Remove Duplicates** / **Drop NaNs**: Cleans up the data.  
4. **Outlier Removal** (IQR): Removes rows considered outliers in numeric columns.  
5. **Label Encoding** (Optional): Converts the target column to numeric if it’s object-type.  
6. **Save** the cleaned data into `iris_prepared.csv`.

---

## 6. Training: `train.py`

This script loads **prepared data**, splits it into training and test sets, and trains either a logistic regression or a decision tree classifier.

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

---

## 7. Evaluation: `eval.py`

This script loads the **trained model**, re-splits the data in the same manner, and evaluates performance metrics.

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

---

## 8. Usage

Once you’ve **cloned** the repo, installed **Python** and **dependencies**, and **activated** your virtual environment:

1. **Check your `config.yaml`**  
   - Verify the paths (`data.path`, `data.file_name`) and the `target_column`.
   - Switch model type (e.g., `"logistic_regression"` or `"decision_tree"`) if desired.

2. **Run data preparation**:
   ```bash
   python data_preparation.py
   ```
   - This will clean and transform `iris.csv` → `iris_prepared.csv`.

3. **Train the model**:
   ```bash
   python train.py
   ```
   - This trains your chosen model and saves it to `trained_model.pkl`.

4. **Evaluate the model**:
   ```bash
   python eval.py
   ```
   - This will print out the requested metrics (e.g., accuracy, F1).

---
