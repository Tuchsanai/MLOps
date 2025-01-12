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