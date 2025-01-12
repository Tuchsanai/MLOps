

# LAB: MLOps with OmegaConf Configuration

Below is an example **MLOps lab** that demonstrates how to use **OmegaConf** for configuration management in a simple ML workflow on the **Iris dataset**. The lab includes:

- A **config.yaml** file (using [OmegaConf](https://omegaconf.readthedocs.io/en/latest/)) that specifies data paths, target column, model choices, and training hyperparameters.  
- Three Python scripts:  
  1. **data_preparation.py**: Loads and prepares data.  
  2. **train.py**: Trains a specified model.  
  3. **eval.py**: Evaluates the trained model on hold-out data.  

> **Note**: This example assumes an **Ubuntu** system *without* Python installed. You will install Python, create a virtual environment, install dependencies, and run the scripts inside that environment.

---

## 1. Repository Structure

After you clone or download the repo from:  
> [https://github.com/Tuchsanai/MLOps/tree/main/03_Automating_MLLearning_Cycle/week07/LAB02](https://github.com/Tuchsanai/MLOps/tree/main/03_Automating_MLLearning_Cycle/week07/LAB02)

Your folder might look like this:

```
├── data/
│   └── iris.csv       <- Your raw dataset
├── config.yaml         <- OmegaConf configuration file
├── data_preparation.py
├── train.py
├── eval.py
└── README.md           <- This file with instructions
```

---

## 2. Installing Python & Setting Up the Environment

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
4. **Install required Python packages** (e.g., scikit-learn, pandas, OmegaConf):
   ```bash
   pip install pandas scikit-learn omegaconf
   ```

> **Tip**: You could also maintain a `requirements.txt` file for easier installation.

---

## 3. Configuration File: `config.yaml`

Below is an **example** configuration file using OmegaConf. You can customize it as needed. In this example, we show how you might switch between multiple model types (e.g., Logistic Regression or Decision Tree) and configure hyperparameters.

```yaml
data:
  path: "./data/"
  file_name: "iris.csv"
  target_column: "species"    # The column to predict (classification)

model:
  type: "logistic_regression"  # Options: "logistic_regression", "decision_tree"
  hyperparameters:
    # LogisticRegression params example
    max_iter: 200
    # DecisionTreeClassifier params example
    # max_depth: 3

training:
  test_size: 0.2
  random_state: 42

evaluation:
  metrics:
    - "accuracy"
    - "f1"
```

**Key Points**:  
- `data.path` & `data.file_name` specify where to find your raw dataset.  
- `data.target_column` is the name of the column we’ll predict.  
- `model.type` can be changed to “logistic_regression” or “decision_tree” to select a different model.  
- `model.hyperparameters` holds model-specific settings (e.g., number of iterations, max depth, etc.).  
- `training.test_size` is the fraction of the dataset to use for testing.  
- `training.random_state` ensures reproducibility.  
- `evaluation.metrics` are the metrics we want to calculate (e.g., accuracy, f1).

---

## 4. Data Preparation: `data_preparation.py`

This script loads the **Iris dataset** from the specified path, does any required cleaning or transformation, and saves the prepared data to a new file (or keeps it in memory for further steps). In many production workflows, you might store the cleaned data in some intermediate format (e.g., CSV, Parquet, or even a database).

```python
# data_preparation.py
import os
import pandas as pd
from omegaconf import OmegaConf

def main():
    # 1. Load config
    config = OmegaConf.load("config.yaml")
    
    # 2. Read the raw data
    data_path = os.path.join(config.data.path, config.data.file_name)
    df = pd.read_csv(data_path)
    
    # 3. (Optional) Clean or transform data
    # For example, let's just drop rows with NaN (if any).
    # The iris dataset might not have missing data, but this is illustrative.
    df.dropna(inplace=True)
    
    # 4. Save prepared data (optional). For simplicity, we’ll just overwrite or keep in memory.
    prepared_data_path = os.path.join(config.data.path, "iris_prepared.csv")
    df.to_csv(prepared_data_path, index=False)
    print(f"Data prepared and saved to {prepared_data_path}")

if __name__ == "__main__":
    main()
```

> **Note**: In a real scenario, you might have a more elaborate data-cleaning process.  

---

## 5. Model Training: `train.py`

This script loads **prepared data**, splits it into training and test sets, instantiates the model from the config, trains it, and saves the trained model to disk.

```python
# train.py
import os
import joblib  # for saving/loading model
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
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    main()
```

---

## 6. Model Evaluation: `eval.py`

This script loads the **trained model**, loads (or re-splits) the test data, and calculates the requested metrics (e.g., accuracy, F1-score).

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

    # 6. Make predictions on test set
    y_pred = model.predict(X_test)

    # 7. Evaluate with specified metrics
    metrics_list = config.evaluation.metrics
    for metric in metrics_list:
        if metric.lower() == "accuracy":
            acc = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {acc:.4f}")
        elif metric.lower() == "f1":
            # For multi-class: average can be "weighted", "macro", etc.
            f1 = f1_score(y_test, y_pred, average="weighted")
            print(f"F1 (weighted): {f1:.4f}")
        else:
            print(f"Metric '{metric}' is not implemented.")

if __name__ == "__main__":
    main()
```

---

## 7. Usage

Once everything is set up:

1. **Clone** the repo and **cd** into it:
   ```bash
   git clone https://github.com/Tuchsanai/MLOps.git
   cd MLOps/03_Automating_MLLearning_Cycle/week07/LAB02
   ```

2. **(Optional) Adjust** your `config.yaml` to change the model type or hyperparameters.

3. **Run data preparation**:
   ```bash
   python data_preparation.py
   ```

4. **Train the model**:
   ```bash
   python train.py
   ```

5. **Evaluate the model**:
   ```bash
   python eval.py
   ```

---

## 8. Summary & Next Steps

- You have a basic end-to-end workflow: **data prep** → **train** → **eval**.  
- All configuration (paths, hyperparameters, etc.) is controlled by **OmegaConf** in `config.yaml`.  
- You can experiment with **different models** (Logistic Regression vs. Decision Tree) by changing the `model.type`.  
- You can add **new metrics** (e.g., precision, recall) inside `eval.py`.  
- In a full production pipeline, you’d incorporate **CI/CD** steps and possibly use containers (Docker) to deploy.

Feel free to expand this lab by adding:
- **Data validation** steps (e.g., using [Great Expectations](https://greatexpectations.io/)).
- **Logging and monitoring** (e.g., MLflow, Neptune, Weights & Biases).
- **Orchestration** (e.g., Airflow, Prefect) for scheduled runs and better pipeline management.

---

**Congratulations!** You have a working MLOps lab with **OmegaConf**, allowing you to **configure** and **automate** your ML workflow on **Ubuntu** (or any environment).  