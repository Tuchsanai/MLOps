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