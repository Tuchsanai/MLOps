

# LAB: MLOps with OmegaConf Configuration

This lab demonstrates how to manage configuration for data preparation, training, and evaluation using [OmegaConf](https://omegaconf.readthedocs.io/en/2.1_branch/) in a Python-based machine learning project. We will:

1. Set up a local Python environment on Ubuntu (which starts out without Python).
2. Clone the repository containing the scripts and sample data.
3. Install the necessary dependencies.
4. Run the data preparation, training, and evaluation scripts with a shared configuration file (`config.yaml`) using OmegaConf.

---

## 1. Prerequisites

- **Ubuntu** (or a similar Linux environment).
- **git** installed (to clone the repository).  
  If git is not installed, you can do so by:  
  ```bash
  sudo apt-get update && sudo apt-get install -y git
  ```
- **Python** is not installed on the system by default. We will install Python 3.8+ (example) using apt-get.

### Install Python 3 (If needed)

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip
```

## 2. Clone the Repository

Clone the lab code from the provided URL:

```bash
git clone https://github.com/Tuchsanai/MLOps_Class.git
```

You can find the code for this lab in the path:
```
MLOps_Class/
  └── 02_Data Versioning_and_pipeline
       └── week07
           └── LAB02
```

Change directory into the lab folder:
```bash
cd MLOps_Class/02_Data Versioning_and_pipeline /week07/LAB02
```

## 3. Create and Activate a Python Virtual Environment

Inside the `LAB02` folder, create and activate a virtual environment (named, for example, `venv`):

```bash
python3 -m venv venv
source venv/bin/activate
```

Verify that your environment is active. Your shell prompt should be prefixed with `(venv)`.

## 4. Install Dependencies

Install the required dependencies (including [OmegaConf](https://pypi.org/project/omegaconf/)):

```bash
pip install -r requirements.txt
```

*(If there is no `requirements.txt`, create one manually or install packages individually, e.g., `pip install omegaconf pandas scikit-learn` as needed.)*

## 5. Configuration File: `config.yaml`

Within this lab, we use a single YAML configuration file to set parameters for data preparation, model training, and evaluation. Below is an example structure:

```yaml
data:
  path: "./data/"       # Path to your data directory
  file_name: "raw.csv"  # Name of the CSV file within data path

model:
  type: "LogisticRegression"  # e.g., "LogisticRegression", "RandomForest", etc.
  hyperparameters:
    C: 1.0
    max_iter: 100

training:
  random_state: 42
  test_size: 0.2

evaluation:
  metrics: ["accuracy", "f1"]  # List of metrics you want to compute
```

Feel free to adjust the fields in `config.yaml` based on your project requirements (e.g., feature columns, additional hyperparameters, or alternative models).

## 6. Scripts

We have three scripts that each load `config.yaml` via OmegaConf:

1. **`data_preparation.py`**  
   - Loads raw data from `data.path`.
   - Performs any preprocessing steps (e.g., cleaning, feature engineering).
   - Saves the processed dataset for training.

2. **`train.py`**  
   - Reads processed data.
   - Instantiates the model defined in `model.type` with `model.hyperparameters`.
   - Trains the model with `training` parameters (e.g., `random_state`, `test_size`).
   - Saves the trained model artifact.

3. **`eval.py`**  
   - Loads the trained model and test set.
   - Computes specified metrics (e.g., `accuracy`, `f1`) from `evaluation.metrics`.
   - Prints or logs the results.

### Example: `data_preparation.py`

```python
#!/usr/bin/env python3
from omegaconf import OmegaConf
import pandas as pd
import os

def main(config):
    # Example: load data
    data_path = os.path.join(config.data.path, config.data.file_name)
    df = pd.read_csv(data_path)

    # Example: Basic cleaning or transformations
    df.dropna(inplace=True)

    # Example: Save processed data
    processed_data_path = os.path.join(config.data.path, "processed.csv")
    df.to_csv(processed_data_path, index=False)
    print(f"Data preparation complete. Processed data saved to {processed_data_path}")

if __name__ == "__main__":
    config = OmegaConf.load("config.yaml")
    main(config)
```

### Example: `train.py`

```python
#!/usr/bin/env python3
from omegaconf import OmegaConf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

def main(config):
    # Load processed data
    processed_data_path = os.path.join(config.data.path, "processed.csv")
    df = pd.read_csv(processed_data_path)

    # Split data (Example: last column is target)
    # Adjust this based on config or project requirement
    X = df.drop(df.columns[-1], axis=1)
    y = df[df.columns[-1]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config.training.test_size, 
        random_state=config.training.random_state
    )

    # Instantiate model from config
    if config.model.type == "LogisticRegression":
        model = LogisticRegression(**config.model.hyperparameters)
    else:
        raise ValueError("Only LogisticRegression is supported in this example.")

    # Train model
    model.fit(X_train, y_train)

    # Save model
    model_path = os.path.join(config.data.path, "trained_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model training complete. Trained model saved to {model_path}")

if __name__ == "__main__":
    config = OmegaConf.load("config.yaml")
    main(config)
```

### Example: `eval.py`

```python
#!/usr/bin/env python3
from omegaconf import OmegaConf
import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, f1_score

def main(config):
    # Load processed data
    processed_data_path = os.path.join(config.data.path, "processed.csv")
    df = pd.read_csv(processed_data_path)

    # Split data similarly
    X = df.drop(df.columns[-1], axis=1)
    y = df[df.columns[-1]]

    # Load trained model
    model_path = os.path.join(config.data.path, "trained_model.pkl")
    model = joblib.load(model_path)

    # Predict
    y_pred = model.predict(X)

    # Evaluate
    metrics = {}
    if "accuracy" in config.evaluation.metrics:
        metrics["accuracy"] = accuracy_score(y, y_pred)
    if "f1" in config.evaluation.metrics:
        metrics["f1"] = f1_score(y, y_pred, average="weighted")

    print("Evaluation Results:")
    for m, score in metrics.items():
        print(f"{m}: {score:.4f}")

if __name__ == "__main__":
    config = OmegaConf.load("config.yaml")
    main(config)
```

## 7. Run the Scripts

After creating or modifying `config.yaml` in the `LAB02` folder, you can run each script as follows:

1. **Data Preparation**  
   ```bash
   python data_preparation.py
   ```
2. **Training**  
   ```bash
   python train.py
   ```
3. **Evaluation**  
   ```bash
   python eval.py
   ```

## 8. Lab Flow

1. **Data Preparation**: This step ensures your raw data is cleaned and organized for training. Modify the data path or any other preprocessing steps as desired in `config.yaml`.
2. **Training**: Use `train.py` to train and save your model. Adjust hyperparameters (`model.hyperparameters`) and data split details (`training.test_size`, etc.) in `config.yaml`.
3. **Evaluation**: Compute various metrics (accuracy, F1, etc.) specified under `evaluation.metrics` in `config.yaml` and confirm that your model performs as expected.

## 9. Customization

- Change the model type (e.g., `RandomForestClassifier`) and its hyperparameters by editing the `model` section in `config.yaml` and updating `train.py` accordingly.
- Update the target column, additional preprocessing steps, or evaluation metrics based on your specific data and project goals.
- Extend the pipeline to include more advanced tasks like hyperparameter tuning or cross-validation.

---

## Troubleshooting

1. **OmegaConf import error**: Ensure `OmegaConf` is installed in your current environment. Check by running `pip show omegaconf`.
2. **File not found**: Verify that your paths in `config.yaml` are correct.
3. **Model import error**: If you change the model type, ensure the correct scikit-learn class is imported in `train.py`.

---

## Conclusion

You now have a fully configurable pipeline for data preparation, training, and evaluation, all controlled by **OmegaConf** through a single `config.yaml`. This structure helps maintain cleaner, more scalable ML projects while making experimentation simpler.

> **Tip**: Extend this lab by adding version control for data (e.g., DVC), containerizing your environment with Docker, or using a CI/CD pipeline to automate testing and deployment.

---

**Happy Learning and Experimenting!**