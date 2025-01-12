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