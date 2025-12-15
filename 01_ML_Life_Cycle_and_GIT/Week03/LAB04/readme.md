# MLOps Lab: Version-Controlled Machine Learning Experiments

## 🎯 Objective

Learn how to manage Machine Learning experiments using Git version control with scikit-learn. Students will:
1. Set up a Python virtual environment for ML projects
2. Track model experiments with Git branches
3. Compare different model versions systematically
4. Resolve conflicts when merging experiment results
5. Apply MLOps best practices for reproducible ML workflows

---

## 📊 Experiment Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        MLOps EXPERIMENT WORKFLOW                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │   main branch    │
                              │  (baseline model)│
                              │  Logistic Reg    │
                              │  Accuracy: 0.85  │
                              └────────┬─────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
              ▼                        ▼                        ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ exp/random-forest│    │ exp/svm-model   │    │ exp/ensemble    │
    │                 │    │                 │    │                 │
    │ Random Forest   │    │ SVM Classifier  │    │ Voting Ensemble │
    │ Accuracy: 0.89  │    │ Accuracy: 0.87  │    │ Accuracy: 0.91  │
    │                 │    │                 │    │                 │
    │ Hyperparameters:│    │ Hyperparameters:│    │ Combines:       │
    │ n_estimators=100│    │ kernel='rbf'    │    │ RF + SVM + LR   │
    │ max_depth=10    │    │ C=1.0           │    │                 │
    └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │  Merge & Compare │
                          │  Best Model:     │
                          │  Ensemble 0.91   │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │   main branch   │
                          │ (updated with   │
                          │  best model)    │
                          └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW STEPS:                                                                │
│  1. Setup Environment → 2. Create Baseline → 3. Branch Experiments →            │
│  4. Train Models → 5. Track Results → 6. Compare & Merge → 7. Document          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mlops-experiment/
├── data/
│   └── dataset.csv          # Training data
├── models/
│   └── model_info.json      # Model metadata & metrics
├── src/
│   ├── train.py             # Training script
│   ├── evaluate.py          # Evaluation script
│   └── utils.py             # Utility functions
├── results/
│   └── metrics.txt          # Experiment results
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

---

## 🔧 Lab Setup

### Step 1: Create Project Directory and Initialize Git

```bash
# Create project directory
mkdir mlops-experiment
cd mlops-experiment

# Initialize Git repository
git init

# Configure Git (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

**Explanation:**
- `mkdir mlops-experiment`: Creates a new directory for the ML project
- `git init`: Initializes an empty Git repository to track changes

---

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv mlops-env

# Activate virtual environment
# On Linux/Mac:
source mlops-env/bin/activate

# On Windows:
# mlops-env\Scripts\activate

# Verify activation
which python
```

**Explanation:**
- `python3 -m venv mlops-env`: Creates an isolated Python environment
- `source mlops-env/bin/activate`: Activates the virtual environment
- Virtual environments ensure reproducibility and dependency isolation

---

### Step 3: Install Dependencies

**Create a file named `requirements.txt`** in the project root directory with the following content:

```
scikit-learn==1.3.0
pandas==2.0.3
numpy==1.24.3
joblib==1.3.1
```

Then install the dependencies:

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import sklearn; print(f'scikit-learn version: {sklearn.__version__}')"
```

**Explanation:**
- `requirements.txt`: Lists all Python dependencies with specific versions for reproducibility
- `pip install -r requirements.txt`: Installs all listed packages

---

### Step 4: Create Project Structure

```bash
# Create directories
mkdir -p data models src results
```

**Create a file named `.gitignore`** in the project root directory with the following content:

```
# Virtual environment
mlops-env/
venv/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Model files (large binary files)
*.pkl
*.joblib

# IDE settings
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

**Explanation:**
- `.gitignore`: Specifies files that Git should not track (virtual environments, cache, large model files)

---

## 📝 Task 1: Create Baseline Model (main branch)

### Step 1.1: Create Sample Dataset

**Create a file named `create_dataset.py`** inside the `src/` directory with the following content:

```python
"""
Create a sample dataset for ML experiments
"""
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

def create_dataset(n_samples=1000, n_features=20, random_state=42):
    """Generate a classification dataset"""
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=random_state
    )
    
    # Create feature names
    feature_names = [f'feature_{i}' for i in range(n_features)]
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df

if __name__ == "__main__":
    # Generate and save dataset
    df = create_dataset()
    df.to_csv('data/dataset.csv', index=False)
    print(f"Dataset created: {df.shape[0]} samples, {df.shape[1]} columns")
    print(f"Target distribution:\n{df['target'].value_counts()}")
```

Then run the script:

```bash
# Run the script
python src/create_dataset.py
```

**Explanation:**
- Creates a synthetic classification dataset using scikit-learn
- Saves data to `data/dataset.csv` for consistent experiments

---

### Step 1.2: Create Training Script

**Create a file named `train.py`** inside the `src/` directory with the following content:

```python
"""
Training script for ML experiments
"""
import json
import argparse
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_logistic_regression(X_train, y_train):
    """Train Logistic Regression model"""
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    return model, {'model_type': 'LogisticRegression', 'max_iter': 1000}

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Logistic Regression (Baseline)")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_logistic_regression(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file for easy comparison
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: Baseline - Logistic Regression\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print("\nResults saved to models/model_info.json and results/metrics.txt")

if __name__ == "__main__":
    main()
```

---

### Step 1.3: Run Baseline Experiment and Commit

```bash
# Run training
python src/train.py

# Check the results
cat models/model_info.json
cat results/metrics.txt

# Stage and commit all files
git add .
git commit -m "Initial commit: Baseline Logistic Regression model"

# View commit history
git log --oneline
```

**Explanation:**
- Trains the baseline Logistic Regression model
- Saves metrics for comparison
- Creates the first commit on the main branch

---

## 📝 Task 2: Create Random Forest Experiment Branch

### Step 2.1: Create and Switch to Experiment Branch

```bash
# Create new branch for Random Forest experiment
git checkout -b exp/random-forest

# Verify current branch
git branch
echo "Current branch: $(git branch --show-current)"
```

**Explanation:**
- `git checkout -b exp/random-forest`: Creates and switches to a new experiment branch
- Branch naming convention `exp/` helps identify experimental branches

---

### Step 2.2: Modify Training Script for Random Forest

**Replace the content of `src/train.py`** with the following code:

```python
"""
Training script for ML experiments - Random Forest Version
"""
import json
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model, {
        'model_type': 'RandomForestClassifier',
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5
    }

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Random Forest Classifier")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_random_forest(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Hyperparameters:")
    for key, value in model_info.items():
        if key != 'model_type':
            print(f"  {key}: {value}")
    print(f"\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: Random Forest Classifier\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Hyperparameters:\n")
        for key, value in model_info.items():
            if key != 'model_type':
                f.write(f"  {key}: {value}\n")
        f.write(f"\nMetrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value}\n")
    
    print("\nResults saved!")

if __name__ == "__main__":
    main()
```

---

### Step 2.3: Run Experiment and Commit

```bash
# Run training
python src/train.py

# View results
cat results/metrics.txt

# Commit changes
git add .
git commit -m "Experiment: Random Forest with n_estimators=100, max_depth=10"

# View branch history
git log --oneline
```

---

### Step 2.4: Tune Hyperparameters (Second Commit)

**Replace the content of `src/train.py`** with the following tuned version (note the changed hyperparameters: `n_estimators=200` and `max_depth=15`):

```python
"""
Training script for ML experiments - Random Forest Version (Tuned)
"""
import json
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model, {
        'model_type': 'RandomForestClassifier',
        'n_estimators': 200,
        'max_depth': 15,
        'min_samples_split': 5
    }

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Random Forest Classifier (Tuned)")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_random_forest(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Hyperparameters:")
    for key, value in model_info.items():
        if key != 'model_type':
            print(f"  {key}: {value}")
    print(f"\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: Random Forest Classifier (Tuned)\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Hyperparameters:\n")
        for key, value in model_info.items():
            if key != 'model_type':
                f.write(f"  {key}: {value}\n")
        f.write(f"\nMetrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value}\n")
    
    print("\nResults saved!")

if __name__ == "__main__":
    main()
```

Then run and commit:

```bash
# Run training again
python src/train.py

# View updated results
cat results/metrics.txt

# Commit the tuned version
git add .
git commit -m "Tune: Random Forest n_estimators=200, max_depth=15"

# View commit history
git log --oneline
```

**Explanation:**
- Demonstrates iterative experiment tracking
- Each hyperparameter change is tracked as a separate commit
- Changes made: `n_estimators` increased from 100 to 200, `max_depth` increased from 10 to 15

---

## 📝 Task 3: Create SVM Experiment Branch

### Step 3.1: Switch to Main and Create New Branch

```bash
# Switch back to main
git checkout main

# Verify we're on main
cat results/metrics.txt  # Should show Logistic Regression results

# Create SVM experiment branch
git checkout -b exp/svm-model

# Verify branch
git branch --show-current
```

---

### Step 3.2: Create SVM Training Script

**Replace the content of `src/train.py`** with the following code:

```python
"""
Training script for ML experiments - SVM Version
"""
import json
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_svm(X_train, y_train):
    """Train SVM model with preprocessing pipeline"""
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42))
    ])
    model.fit(X_train, y_train)
    return model, {
        'model_type': 'SVC',
        'kernel': 'rbf',
        'C': 1.0,
        'gamma': 'scale',
        'preprocessing': 'StandardScaler'
    }

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Support Vector Machine (SVM)")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_svm(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Hyperparameters:")
    for key, value in model_info.items():
        if key != 'model_type':
            print(f"  {key}: {value}")
    print(f"\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: SVM Classifier\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Hyperparameters:\n")
        for key, value in model_info.items():
            if key != 'model_type':
                f.write(f"  {key}: {value}\n")
        f.write(f"\nMetrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value}\n")
    
    print("\nResults saved!")

if __name__ == "__main__":
    main()
```

Then run and commit:

```bash
# Run training
python src/train.py

# Commit
git add .
git commit -m "Experiment: SVM with RBF kernel, C=1.0"
```

---

### Step 3.3: Tune SVM Hyperparameters

**Replace the content of `src/train.py`** with the following tuned version (note the changed hyperparameter: `C=10.0`):

```python
"""
Training script for ML experiments - SVM Version (Tuned)
"""
import json
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_svm(X_train, y_train):
    """Train SVM model with preprocessing pipeline"""
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel='rbf', C=10.0, gamma='scale', random_state=42))
    ])
    model.fit(X_train, y_train)
    return model, {
        'model_type': 'SVC',
        'kernel': 'rbf',
        'C': 10.0,
        'gamma': 'scale',
        'preprocessing': 'StandardScaler'
    }

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Support Vector Machine (SVM) - Tuned")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_svm(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Hyperparameters:")
    for key, value in model_info.items():
        if key != 'model_type':
            print(f"  {key}: {value}")
    print(f"\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: SVM Classifier (Tuned)\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Hyperparameters:\n")
        for key, value in model_info.items():
            if key != 'model_type':
                f.write(f"  {key}: {value}\n")
        f.write(f"\nMetrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value}\n")
    
    print("\nResults saved!")

if __name__ == "__main__":
    main()
```

Then run and commit:

```bash
# Run training
python src/train.py

# Commit
git add .
git commit -m "Tune: SVM with C=10.0"

# View branch history
git log --oneline
```

**Explanation:**
- The regularization parameter `C` was increased from 1.0 to 10.0
- Higher C values mean less regularization, allowing the model to fit the training data more closely

---

## 📝 Task 4: Create Ensemble Experiment Branch

### Step 4.1: Create Ensemble Branch from Main

```bash
# Switch to main
git checkout main

# Create ensemble branch
git checkout -b exp/ensemble

# Verify
git branch --show-current
```

---

### Step 4.2: Create Ensemble Model

**Replace the content of `src/train.py`** with the following code:

```python
"""
Training script for ML experiments - Ensemble Version
"""
import json
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def load_data(filepath='data/dataset.csv'):
    """Load dataset from CSV"""
    df = pd.read_csv(filepath)
    X = df.drop('target', axis=1)
    y = df['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_ensemble(X_train, y_train):
    """Train Voting Ensemble model"""
    # Define base models
    lr = LogisticRegression(max_iter=1000, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    svm = Pipeline([
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel='rbf', C=1.0, probability=True, random_state=42))
    ])
    
    # Create ensemble
    model = VotingClassifier(
        estimators=[
            ('lr', lr),
            ('rf', rf),
            ('svm', svm)
        ],
        voting='soft'
    )
    model.fit(X_train, y_train)
    
    return model, {
        'model_type': 'VotingClassifier',
        'voting': 'soft',
        'base_models': ['LogisticRegression', 'RandomForest', 'SVM'],
        'n_models': 3
    }

def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics"""
    y_pred = model.predict(X_test)
    return {
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4)
    }

def save_results(model_info, metrics, filepath='models/model_info.json'):
    """Save model information and metrics"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'model_info': model_info,
        'metrics': metrics
    }
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    return results

def main():
    print("=" * 50)
    print("TRAINING: Voting Ensemble (LR + RF + SVM)")
    print("=" * 50)
    
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    model, model_info = train_ensemble(X_train, y_train)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save results
    results = save_results(model_info, metrics)
    
    # Print results
    print(f"\nModel: {model_info['model_type']}")
    print(f"Configuration:")
    for key, value in model_info.items():
        if key != 'model_type':
            print(f"  {key}: {value}")
    print(f"\nMetrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Save metrics to text file
    with open('results/metrics.txt', 'w') as f:
        f.write(f"Experiment: Voting Ensemble\n")
        f.write(f"Timestamp: {results['timestamp']}\n")
        f.write(f"{'='*40}\n")
        f.write(f"Configuration:\n")
        for key, value in model_info.items():
            if key != 'model_type':
                f.write(f"  {key}: {value}\n")
        f.write(f"\nMetrics:\n")
        for key, value in metrics.items():
            f.write(f"  {key}: {value}\n")
    
    print("\nResults saved!")

if __name__ == "__main__":
    main()
```

Then run and commit:

```bash
# Run training
python src/train.py

# Commit
git add .
git commit -m "Experiment: Voting Ensemble (LR + RF + SVM)"

# View history
git log --oneline
```

---

## 📝 Task 5: Compare All Experiments

### Step 5.1: Create Comparison Script

```bash
# Switch to main branch
git checkout main
```

**Create a file named `compare_experiments.py`** inside the `src/` directory with the following content:

```python
"""
Compare experiments across different branches
"""
import subprocess
import json

def get_metrics_from_branch(branch_name):
    """Checkout branch and read metrics"""
    # Checkout branch
    subprocess.run(['git', 'checkout', branch_name], 
                   capture_output=True, text=True)
    
    # Read metrics
    try:
        with open('models/model_info.json', 'r') as f:
            data = json.load(f)
        return {
            'branch': branch_name,
            'model': data['model_info'].get('model_type', 'Unknown'),
            'accuracy': data['metrics']['accuracy'],
            'precision': data['metrics']['precision'],
            'recall': data['metrics']['recall'],
            'f1_score': data['metrics']['f1_score']
        }
    except Exception as e:
        return {'branch': branch_name, 'error': str(e)}

def main():
    # Get list of experiment branches
    result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
    branches = [b.strip().replace('* ', '') for b in result.stdout.split('\n') if b.strip()]
    
    print("=" * 70)
    print("EXPERIMENT COMPARISON")
    print("=" * 70)
    
    results = []
    for branch in branches:
        metrics = get_metrics_from_branch(branch)
        results.append(metrics)
    
    # Print comparison table
    print(f"\n{'Branch':<20} {'Model':<25} {'Accuracy':<10} {'F1-Score':<10}")
    print("-" * 70)
    
    for r in results:
        if 'error' not in r:
            print(f"{r['branch']:<20} {r['model']:<25} {r['accuracy']:<10} {r['f1_score']:<10}")
    
    # Find best model
    valid_results = [r for r in results if 'accuracy' in r]
    if valid_results:
        best = max(valid_results, key=lambda x: x['accuracy'])
        print(f"\n{'='*70}")
        print(f"BEST MODEL: {best['model']} (Branch: {best['branch']})")
        print(f"Accuracy: {best['accuracy']}")
        print(f"{'='*70}")
    
    # Return to main
    subprocess.run(['git', 'checkout', 'main'], capture_output=True)

if __name__ == "__main__":
    main()
```

Then commit:

```bash
git add src/compare_experiments.py
git commit -m "Add experiment comparison script"
```

---

### Step 5.2: View Branch Structure

```bash
# View all branches
git branch -a

# View commit graph across all branches
git log --oneline --graph --all

# View differences between branches
git diff main exp/random-forest -- results/metrics.txt
```

---

## 📝 Task 6: Merge Best Experiment to Main

### Step 6.1: Merge Ensemble Branch (Best Performing)

```bash
# Ensure we're on main
git checkout main

# View current state
cat results/metrics.txt

# Merge ensemble branch
git merge exp/ensemble

# This will create a merge conflict in results/metrics.txt and train.py
# Check status
git status
```

---

### Step 6.2: Resolve Merge Conflicts

When conflicts occur, the files will contain conflict markers:

```bash
# View conflict in train.py
cat src/train.py

# The conflict will look like:
# <<<<<<< HEAD
# (Logistic Regression version)
# =======
# (Ensemble version)
# >>>>>>> exp/ensemble
```

**Resolve the conflict manually:**

```bash
# For this lab, we want to keep the ensemble version
# Open train.py and keep the ensemble code (remove conflict markers)

# Or use git checkout to accept one version entirely:
git checkout --theirs src/train.py
git checkout --theirs models/model_info.json
git checkout --theirs results/metrics.txt

# Stage resolved files
git add .

# Complete the merge
git commit -m "Merge ensemble experiment - best performing model (accuracy improvement)"
```

---

### Step 6.3: Verify Merge

```bash
# View final results
cat results/metrics.txt

# View merged history
git log --oneline --graph

# Run the final model
python src/train.py
```

---

## 📝 Task 7: Clean Up and Documentation

### Step 7.1: Delete Merged Branches

```bash
# Delete merged experiment branches
git branch -d exp/ensemble

# View remaining branches
git branch

# Force delete unmerged branches (if needed)
git branch -D exp/random-forest
git branch -D exp/svm-model
```

---

### Step 7.2: Create Final Documentation

**Create a file named `EXPERIMENT_LOG.md`** in the project root directory with the following content:

```markdown
# Experiment Log

## Summary

| Experiment | Model | Accuracy | F1-Score | Status |
|------------|-------|----------|----------|--------|
| Baseline | Logistic Regression | 0.85 | 0.84 | Completed |
| exp/random-forest | Random Forest | 0.89 | 0.88 | Merged |
| exp/svm-model | SVM (RBF) | 0.87 | 0.86 | Closed |
| exp/ensemble | Voting Ensemble | 0.91 | 0.90 | **SELECTED** |

## Best Model

**Voting Ensemble** combining Logistic Regression, Random Forest, and SVM achieved the best performance with:
- Accuracy: 0.91
- F1-Score: 0.90

## Reproduction Steps

1. Clone repository
2. Create virtual environment: `python -m venv mlops-env`
3. Activate: `source mlops-env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run training: `python src/train.py`

## Git Commands Used

- `git init` - Initialize repository
- `git checkout -b <branch>` - Create experiment branch
- `git commit -m "<message>"` - Track experiment changes
- `git merge <branch>` - Merge successful experiments
- `git diff <branch1> <branch2>` - Compare experiments
- `git log --graph --all` - Visualize experiment history
```

Then commit:

```bash
git add EXPERIMENT_LOG.md
git commit -m "Add experiment documentation"
```

---

### Step 7.3: View Final Project State

```bash
# Final commit history
git log --oneline

# Project structure
ls -la

# Deactivate virtual environment (when done)
deactivate
```

---

## ✅ Learning Outcomes

After completing this lab, students will understand:

1. **Environment Management**: Using Python virtual environments for isolated ML projects
2. **Experiment Tracking**: Using Git branches to manage different model experiments
3. **Version Control**: Committing model changes with descriptive messages
4. **Comparison**: Comparing model performance across branches
5. **Conflict Resolution**: Handling merge conflicts when combining experiments
6. **Documentation**: Maintaining experiment logs and reproducibility
7. **MLOps Best Practices**: Structuring ML projects for collaboration

---

## 📋 Quick Reference: File Creation Summary

Throughout this lab, you will create the following files manually:

| File | Location | Task |
|------|----------|------|
| `requirements.txt` | Project root | Step 3 |
| `.gitignore` | Project root | Step 4 |
| `create_dataset.py` | `src/` | Task 1.1 |
| `train.py` | `src/` | Task 1.2 |
| `train.py` (RF version) | `src/` | Task 2.2 |
| `train.py` (RF tuned) | `src/` | Task 2.4 |
| `train.py` (SVM version) | `src/` | Task 3.2 |
| `train.py` (SVM tuned) | `src/` | Task 3.3 |
| `train.py` (Ensemble) | `src/` | Task 4.2 |
| `compare_experiments.py` | `src/` | Task 5.1 |
| `EXPERIMENT_LOG.md` | Project root | Task 7.2 |

---

## 📝 Hyperparameter Changes Summary

| Task | Model | Parameter | Before | After |
|------|-------|-----------|--------|-------|
| 2.4 | Random Forest | n_estimators | 100 | 200 |
| 2.4 | Random Forest | max_depth | 10 | 15 |
| 3.3 | SVM | C | 1.0 | 10.0 |

**Tip:** Use any text editor you're comfortable with (VS Code, nano, vim, etc.) to create and edit these files.