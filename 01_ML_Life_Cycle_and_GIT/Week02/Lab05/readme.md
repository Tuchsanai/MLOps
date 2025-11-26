# 🧪 Lab: Git for Machine Learning Development

---

## 📋 Lab Overview

In this lab, you will learn how to use Git commands to track changes in a Machine Learning project. You will build a complete ML pipeline step-by-step, committing your work at each stage.

**What you will learn:**

| Git Command | Description |
|-------------|-------------|
| `git init` | Initialize a new repository |
| `git status` | Check current state of files |
| `git add` | Stage changes for commit |
| `git commit` | Save changes with descriptive message |
| `git log` | View commit history |
| `git push` | Upload commits to remote repository |
| `git pull` | Download commits from remote repository |

**ML Skills Applied:**

- Data loading with Pandas
- Data preprocessing and splitting
- Model training with Scikit-learn
- Model evaluation with metrics
- Model comparison and selection


## 📝 Git Workflow Summary in Each Step

### **Step 1: Initialize Repository**
```
git init
     ↓
Create empty .git folder
     ↓
Repository ready for tracking
```

---

### **Steps 2-7: Develop & Commit (Repeat for each feature)**

Each step follows the same Git workflow pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Add Data Loading                                       │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Create load_data() function                       │
│  Test:         python train.py ✓                                 │
│  Git Status:   untracked files (train.py)                        │
│  Git Add:      git add train.py                                  │
│  Git Commit:   git commit -m "Step 2: Add data loading..."       │
│  Result:       ✓ 1st commit saved                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Add Data Preprocessing                                 │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Add preprocess_data() + train_test_split          │
│  Test:         python train.py ✓                                 │
│  Git Status:   modified (train.py)                               │
│  Git Add:      git add train.py                                  │
│  Git Commit:   git commit -m "Step 3: Add preprocessing..."      │
│  Result:       ✓ 2nd commit saved                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Add Model Training                                     │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Add train_model() + DecisionTreeClassifier        │
│  Test:         python train.py ✓                                 │
│  Git Status:   modified (train.py)                               │
│  Git Add:      git add train.py                                  │
│  Git Commit:   git commit -m "Step 4: Add model training..."     │
│  Result:       ✓ 3rd commit saved                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Add Model Evaluation                                   │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Add evaluate_model() + metrics                    │
│  Test:         python train.py ✓                                 │
│  Git Status:   modified (train.py)                               │
│  Git Add:      git add train.py                                  │
│  Git Commit:   git commit -m "Step 5: Add model evaluation..."   │
│  Result:       ✓ 4th commit saved                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Add Model Comparison                                   │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Add train_random_forest() + compare models        │
│  Test:         python train.py ✓                                 │
│  Git Status:   modified (train.py)                               │
│  Git Add:      git add train.py                                  │
│  Git Commit:   git commit -m "Step 6: Compare models..."         │
│  Result:       ✓ 5th commit saved                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: Add Model Saving & Loading                             │
├─────────────────────────────────────────────────────────────────┤
│  Code Change:  Add save_model() + load_model()                   │
│  New Files:    .gitignore, best_model.joblib                     │
│  Test:         python train.py ✓                                 │
│  Git Status:   modified (train.py), untracked (.gitignore, etc.) │
│  Git Add:      git add train.py .gitignore best_model.joblib     │
│  Git Commit:   git commit -m "Step 7: Add model saving..."       │
│  Result:       ✓ 6th commit saved                                │
└─────────────────────────────────────────────────────────────────┘
```

---

### **Step 8: Push to Remote (GitHub)**
```
git remote add origin https://github.com/YOUR_USERNAME/repo.git
     ↓
git push -u origin main
     ↓
All commits uploaded to GitHub ✓
```


---

### **Key Files Modified/Created at Each Step**

| Step | Files Changed | git add | git commit |
|------|---------------|---------|-----------|
| 2 | train.py (created) | `git add train.py` | "Step 2: Add data loading..." |
| 3 | train.py (modified) | `git add train.py` | "Step 3: Add preprocessing..." |
| 4 | train.py (modified) | `git add train.py` | "Step 4: Add training..." |
| 5 | train.py (modified) | `git add train.py` | "Step 5: Add evaluation..." |
| 6 | train.py (modified) | `git add train.py` | "Step 6: Add comparison..." |
| 7 | train.py, .gitignore, best_model.joblib | `git add .` | "Step 7: Add saving..." |
| 8 | None | N/A | `git push -u origin main` |

---

## 🚀 Let's Begin!

---

# Step 1: Initialize Git Repository

## 1.1 Create Project Folder

Open your terminal and run:

```bash
# Create project folder
mkdir ml-iris-classifier
cd ml-iris-classifier
```

## 1.2 Initialize Git

```bash
# Initialize empty Git repository
git init
```

**Expected output:**

```
Initialized empty Git repository in /path/to/ml-iris-classifier/.git/
```

## 1.3 Check Git Status

```bash
# Check repository status
git status
```

**Expected output:**

```
On branch main
No commits yet
nothing to commit (create or copy files and use "git add" to track)
```

✅ **Checkpoint:** You have created a new Git repository!

---

# Step 2: Create Project Structure & Load Data

## 2.1 Create Python File

Create a new file named `train.py`:

```python
# train.py
# Step 2: Load and explore the Iris dataset

import pandas as pd
from sklearn.datasets import load_iris

def load_data():
    """Load Iris dataset and return as DataFrame"""
    # Load built-in Iris dataset
    iris = load_iris()
    
    # Create DataFrame
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    
    # Add target column
    df['target'] = iris.target
    
    return df

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    
    # Show basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
```

## 2.2 What Changed in train.py?

### 📌 New Additions:
- **Imports:** Added `pandas` for data manipulation and `load_iris` from scikit-learn
- **New Function:** `load_data()` - loads the Iris dataset and converts it to a Pandas DataFrame
  - Fetches the built-in Iris dataset (150 samples, 4 features)
  - Creates a DataFrame with feature names as column headers
  - Adds a 'target' column containing the class labels (0, 1, 2)
- **Main Section:** Loads data and displays basic information (shape, first 5 rows, data types)

### 🎯 Purpose:
This is the **first building block** of the ML pipeline. We start by loading and exploring the data to understand its structure before proceeding to preprocessing.

---

## 2.3 Test Your Code

```bash
# Run the script
python train.py
```

**Expected output:**

```
Loading Iris dataset...

Dataset shape: (150, 5)

First 5 rows:
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  target
0                5.1               3.5                1.4               0.2       0
1                4.9               3.0                1.4               0.2       0
...
```

## 2.4 Stage and Commit Changes

```bash
# Check what files are untracked
git status
```

**Output:**

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        train.py
```

```bash
# Stage the file
git add train.py

# Check status again
git status
```

**Output:**

```
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   train.py
```

```bash
# Commit with descriptive message
git commit -m "Step 2: Add data loading function for Iris dataset"
```

## 2.5 View Commit History

```bash
# View commit log
git log --oneline
```

**Output:**

```
abc1234 (HEAD -> main) Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** First commit completed! Your data loading code is saved.

---

# Step 3: Add Data Preprocessing

## 3.1 Update train.py - Add Preprocessing

Edit `train.py` to add data splitting:

```python
# train.py
# Step 3: Add data preprocessing and splitting

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    # Separate features (X) and target (y)
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42  # For reproducibility
    )
    
    return X_train, X_test, y_train, y_test

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\nSplitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
```

## 3.2 What Changed in train.py?

### 📌 New Additions:
- **New Import:** `train_test_split` from scikit-learn
- **New Function:** `preprocess_data()` - prepares data for model training
  - Separates the dataset into features (X) and target labels (y)
  - Splits the data: 80% for training, 20% for testing
  - Uses `random_state=42` to ensure reproducible results
- **Updated Main Section:** Now calls both `load_data()` and `preprocess_data()` and displays dataset sizes

### 🎯 Purpose:
This step **splits the data** into training and test sets. This is essential because we use the training set to teach the model and the test set to evaluate if it can predict on unseen data.

### 📊 Data Breakdown:
- Original: 150 samples
- Training set: ~120 samples (80%)
- Test set: ~30 samples (20%)

---

## 3.3 Test Your Code

```bash
python train.py
```

**Expected output:**

```
Loading Iris dataset...
Dataset shape: (150, 5)

Splitting data into train/test sets...
Training set size: 120
Test set size: 30
```

## 3.4 Stage and Commit Changes

```bash
# Check what changed
git status
```

**Output:**

```
Changes not staged for commit:
        modified:   train.py
```

```bash
# Stage changes
git add train.py

# Commit with message
git commit -m "Step 3: Add data preprocessing and train/test split"
```

## 3.5 View Updated History

```bash
git log --oneline
```

**Output:**

```
def5678 (HEAD -> main) Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** You now have 2 commits tracking your progress!

---

# Step 4: Train Initial Model

## 4.1 Update train.py - Add Model Training

Edit `train.py` to add a simple model:

```python
# train.py
# Step 4: Add model training with Decision Tree

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Train a Decision Tree classifier"""
    # Create model
    model = DecisionTreeClassifier(random_state=42)
    
    # Train model
    model.fit(X_train, y_train)
    
    return model

# Main execution
if __name__ == "__main__":
    # Load data
    print("Loading Iris dataset...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\nSplitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    print("\nTraining Decision Tree model...")
    model = train_model(X_train, y_train)
    print("Model training completed!")
    print(f"Model type: {type(model).__name__}")
```

## 4.2 What Changed in train.py?

### 📌 New Additions:
- **New Import:** `DecisionTreeClassifier` from scikit-learn
- **New Function:** `train_model()` - creates and trains a Decision Tree classifier
  - Instantiates a DecisionTreeClassifier with `random_state=42` for reproducibility
  - Fits (trains) the model using training data
- **Updated Main Section:** Now includes a training step after data preprocessing

### 🎯 Purpose:
This step **trains the machine learning model**. The Decision Tree learns patterns from the training data, creating a tree structure that can predict flower species based on measurements.

### 🌳 How it Works:
The Decision Tree algorithm learns decision rules from the training data:
- Example: "If sepal length > 5.5, predict class 1"
- These rules form a tree structure the model uses for predictions

---

## 4.3 Test Your Code

```bash
python train.py
```

**Expected output:**

```
Loading Iris dataset...
Dataset shape: (150, 5)

Splitting data into train/test sets...
Training set size: 120
Test set size: 30

Training Decision Tree model...
Model training completed!
Model type: DecisionTreeClassifier
```

## 4.4 Stage and Commit

```bash
# Check status
git status

# Stage and commit
git add train.py
git commit -m "Step 4: Add Decision Tree model training"

# View history
git log --oneline
```

**Output:**

```
ghi9012 (HEAD -> main) Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Model training step committed!

---

# Step 5: Add Model Evaluation

## 5.1 Update train.py - Add Evaluation

Edit `train.py` to add evaluation metrics:

```python
# train.py
# Step 5: Add model evaluation

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Generate classification report
    report = classification_report(y_test, y_pred)
    
    return accuracy, report, y_pred

# Main execution
if __name__ == "__main__":
    # Load data
    print("=" * 50)
    print("IRIS CLASSIFICATION PIPELINE")
    print("=" * 50)
    
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train model
    print("\n[3] Training Decision Tree model...")
    model = train_model(X_train, y_train)
    print("    Model training completed!")
    
    # Evaluate model
    print("\n[4] Evaluating model...")
    accuracy, report, y_pred = evaluate_model(model, X_test, y_test)
    
    print(f"\n{'=' * 50}")
    print("EVALUATION RESULTS")
    print(f"{'=' * 50}")
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nClassification Report:\n{report}")
```

## 5.2 What Changed in train.py?

### 📌 New Additions:
- **New Imports:** `accuracy_score` and `classification_report` from scikit-learn.metrics
- **New Function:** `evaluate_model()` - assesses how well the trained model performs
  - Makes predictions on the test set
  - Calculates accuracy (percentage of correct predictions)
  - Generates a detailed classification report showing precision, recall, and F1-score for each class
- **Updated Main Section:** Much better formatting with numbered steps and evaluation results displayed clearly

### 🎯 Purpose:
This step **measures model performance** using metrics that tell us how good our model is at predicting on unseen data.

### 📈 Key Metrics Explained:
- **Accuracy:** Overall correctness (out of 100%)
- **Precision:** Of the flowers we predicted as class X, how many were correct?
- **Recall:** Of all actual class X flowers, how many did we identify?
- **F1-Score:** Balanced combination of precision and recall

---

## 5.3 Test Your Code

```bash
python train.py
```

**Expected output:**

```
==================================================
IRIS CLASSIFICATION PIPELINE
==================================================

[1] Loading Iris dataset...
    Dataset shape: (150, 5)

[2] Splitting data into train/test sets...
    Training set size: 120
    Test set size: 30

[3] Training Decision Tree model...
    Model training completed!

[4] Evaluating model...

==================================================
EVALUATION RESULTS
==================================================

Accuracy: 1.0000 (100.00%)

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00        10
           1       1.00      1.00      1.00         9
           2       1.00      1.00      1.00        11

    accuracy                           1.00        30
   macro avg       1.00      1.00      1.00        30
weighted avg       1.00      1.00      1.00        30
```

## 5.4 Stage and Commit

```bash
git add train.py
git commit -m "Step 5: Add model evaluation with accuracy and classification report"

# View full history
git log --oneline
```

**Output:**

```
jkl3456 (HEAD -> main) Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Complete ML pipeline committed!

---

# Step 6: Improve Model (Try Different Algorithm)

## 6.1 Update train.py - Add Random Forest

Edit `train.py` to compare two models:

```python
# train.py
# Step 6: Compare Decision Tree vs Random Forest

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_decision_tree(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier"""
    model = RandomForestClassifier(
        n_estimators=100,  # Number of trees
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report, y_pred

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("IRIS CLASSIFICATION - MODEL COMPARISON")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train and evaluate Decision Tree
    print("\n" + "=" * 60)
    print("MODEL 1: Decision Tree")
    print("=" * 60)
    dt_model = train_decision_tree(X_train, y_train)
    dt_accuracy, dt_report, _ = evaluate_model(dt_model, X_test, y_test)
    print(f"Accuracy: {dt_accuracy:.4f} ({dt_accuracy*100:.2f}%)")
    
    # Train and evaluate Random Forest
    print("\n" + "=" * 60)
    print("MODEL 2: Random Forest")
    print("=" * 60)
    rf_model = train_random_forest(X_train, y_train)
    rf_accuracy, rf_report, _ = evaluate_model(rf_model, X_test, y_test)
    print(f"Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
    print(f"Random Forest Accuracy: {rf_accuracy*100:.2f}%")
    
    if rf_accuracy > dt_accuracy:
        print("\n✓ Random Forest performs better!")
    elif dt_accuracy > rf_accuracy:
        print("\n✓ Decision Tree performs better!")
    else:
        print("\n✓ Both models perform equally!")
```

## 6.2 What Changed in train.py?

### 📌 New Additions:
- **New Import:** `RandomForestClassifier` from scikit-learn.ensemble
- **New Function:** `train_random_forest()` - trains a Random Forest classifier with 100 trees
- **Renamed/Separated:** Previous `train_model()` is now specifically `train_decision_tree()`
- **Updated Main Section:**
  - Now trains BOTH Decision Tree and Random Forest models
  - Evaluates each model separately
  - Compares their accuracies side-by-side
  - Shows which model performs better

### 🎯 Purpose:
This step **introduces model comparison**. Instead of using just one algorithm, we train multiple models and compare their performance to choose the best one.

### 🌲 Random Forest vs Decision Tree:
- **Decision Tree:** One decision tree (simple, fast, can overfit)
- **Random Forest:** 100 decision trees voting together (more robust, better generalization)
- Random Forest typically performs better but is slightly slower

---

## 6.3 Test Your Code

```bash
python train.py
```

## 6.4 Stage and Commit

```bash
git add train.py
git commit -m "Step 6: Add Random Forest and compare with Decision Tree"

# View history
git log --oneline
```

**Output:**

```
mno7890 (HEAD -> main) Step 6: Add Random Forest and compare with Decision Tree
jkl3456 Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Model comparison committed!

---

# Step 7: Save Model to File

## 7.1 Update train.py - Add Model Saving

Edit `train.py` to save the best model:

```python
# train.py
# Step 7: Save the best model to file

import pandas as pd
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def load_data():
    """Load Iris dataset and return as DataFrame"""
    iris = load_iris()
    
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    
    return df

def preprocess_data(df):
    """Split data into features and target, then train/test split"""
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    
    return X_train, X_test, y_train, y_test

def train_decision_tree(X_train, y_train):
    """Train a Decision Tree classifier"""
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def train_random_forest(X_train, y_train):
    """Train a Random Forest classifier"""
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report, y_pred

def save_model(model, filename):
    """Save model to file using joblib"""
    joblib.dump(model, filename)
    print(f"Model saved to: {filename}")

def load_model(filename):
    """Load model from file"""
    model = joblib.load(filename)
    print(f"Model loaded from: {filename}")
    return model

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("IRIS CLASSIFICATION - TRAIN AND SAVE MODEL")
    print("=" * 60)
    
    # Load data
    print("\n[1] Loading Iris dataset...")
    df = load_data()
    print(f"    Dataset shape: {df.shape}")
    
    # Preprocess data
    print("\n[2] Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    print(f"    Training set size: {len(X_train)}")
    print(f"    Test set size: {len(X_test)}")
    
    # Train models
    print("\n[3] Training models...")
    dt_model = train_decision_tree(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    
    # Evaluate models
    print("\n[4] Evaluating models...")
    dt_accuracy, _, _ = evaluate_model(dt_model, X_test, y_test)
    rf_accuracy, _, _ = evaluate_model(rf_model, X_test, y_test)
    
    print(f"    Decision Tree Accuracy: {dt_accuracy*100:.2f}%")
    print(f"    Random Forest Accuracy: {rf_accuracy*100:.2f}%")
    
    # Select and save best model
    print("\n[5] Saving best model...")
    if rf_accuracy >= dt_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
    else:
        best_model = dt_model
        best_name = "Decision Tree"
    
    save_model(best_model, "best_model.joblib")
    print(f"    Best model: {best_name}")
    
    # Verify saved model works
    print("\n[6] Verifying saved model...")
    loaded_model = load_model("best_model.joblib")
    loaded_accuracy, _, _ = evaluate_model(loaded_model, X_test, y_test)
    print(f"    Loaded model accuracy: {loaded_accuracy*100:.2f}%")
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
```

## 7.2 What Changed in train.py?

### 📌 New Additions:
- **New Import:** `joblib` - used for saving/loading machine learning models as files
- **New Function:** `save_model()` - saves a trained model to a `.joblib` file for later use
- **New Function:** `load_model()` - loads a previously saved model from a `.joblib` file
- **Updated Main Section:**
  - Trains both models
  - Evaluates both models
  - Compares accuracies
  - Selects the BEST model (highest accuracy)
  - Saves the best model to `best_model.joblib`
  - Loads the model back to verify it works correctly
  - Shows completion message

### 🎯 Purpose:
This step **makes the model reusable**. Instead of retraining the model every time we need predictions, we save it as a file. Later, we can load this model in different scripts for making predictions on new data.

### 💾 Why Save Models?
- **Reusability:** Use trained model in production without retraining
- **Efficiency:** Training takes time; loading a saved model is instant
- **Consistency:** Same model produces same results across different runs
- **Sharing:** Send the model file to others for deployment

---

## 7.3 Create .gitignore

Create `.gitignore` to manage which files Git should track:

```bash
# Create .gitignore file
echo "# Python cache files" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "" >> .gitignore
echo "# Optional: Ignore large model files" >> .gitignore
echo "# *.joblib" >> .gitignore
```

### 📌 What is .gitignore?
A `.gitignore` file tells Git which files to ignore (not track). This is important because:
- We don't want to save large model files (like `best_model.joblib`) to Git
- We don't want to track Python cache files (`__pycache__/`, `*.pyc`)
- It keeps the repository clean and reduces storage

---

## 7.4 Stage and Commit All Files

```bash
# Check status - you should see new files
git status

# Add all files
git add train.py
git add .gitignore
git add best_model.joblib

# Commit
git commit -m "Step 7: Add model saving and loading with joblib"

# View complete history
git log --oneline
```

**Output:**

```
pqr1234 (HEAD -> main) Step 7: Add model saving and loading with joblib
mno7890 Step 6: Add Random Forest and compare with Decision Tree
jkl3456 Step 5: Add model evaluation with accuracy and classification report
ghi9012 Step 4: Add Decision Tree model training
def5678 Step 3: Add data preprocessing and train/test split
abc1234 Step 2: Add data loading function for Iris dataset
```

✅ **Checkpoint:** Complete pipeline with model saving!

---

# Step 8: Push to Remote Repository (GitHub)

## 8.1 Create Repository on GitHub

1. Go to https://github.com
2. Click **"New repository"** (green button)
3. Repository name: `ml-iris-classifier`
4. Choose **Public** or **Private**
5. ⚠️ **Do NOT** check "Initialize this repository with a README"
6. Click **"Create repository"**

## 8.2 Connect Local to Remote

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ml-iris-classifier.git

# Verify remote connection
git remote -v
```

**Output:**

```
origin  https://github.com/YOUR_USERNAME/ml-iris-classifier.git (fetch)
origin  https://github.com/YOUR_USERNAME/ml-iris-classifier.git (push)
```

## 8.3 Push to GitHub

```bash
# Push main branch to remote
git push -u origin main
```

You will be prompted for GitHub credentials (username and personal access token).

**Output:**

```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Writing objects: 100% (15/15), 3.45 KiB | 3.45 MiB/s, done.
Total 15 (delta 0), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/ml-iris-classifier.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Checkpoint:** Your code is now on GitHub!

---

# 📊 Git Commands Summary

| Command | Description | When to Use |
|---------|-------------|-------------|
| `git init` | Initialize new repository | Start of project (once) |
| `git status` | Check current state | Before add/commit |
| `git add <file>` | Stage specific file | After modifying code |
| `git add .` | Stage all changed files | After modifying multiple files |
| `git commit -m "msg"` | Save staged changes | After completing a feature |
| `git log` | View full commit history | Review project history |
| `git log --oneline` | View compact history | Quick overview |
| `git remote add` | Connect to GitHub | Setup (once) |
| `git push` | Upload to GitHub | Share your work |

---

# 📈 Summary of Changes Across All Steps

| Step | Added/Changed | Files Modified | Purpose |
|------|---------------|----------------|---------|
| 2 | Data loading function | train.py (created) | Load and explore data |
| 3 | Data preprocessing function | train.py | Split train/test sets (80/20) |
| 4 | Model training function | train.py | Train Decision Tree classifier |
| 5 | Model evaluation function | train.py | Calculate accuracy and metrics |
| 6 | Random Forest model + comparison | train.py | Compare two algorithms |
| 7 | Model saving/loading functions | train.py, .gitignore (created) | Save best model to file |

---

**🎓 Key Takeaways:**
- Each step builds upon the previous one
- Git tracks your progress through commits
- Your train.py grows from simple data loading to a complete ML pipeline
- By Step 7, you have a reusable, production-ready ML model saved as a file