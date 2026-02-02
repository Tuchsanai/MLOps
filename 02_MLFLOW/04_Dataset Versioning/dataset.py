# %%
# MLflow Dataset Versioning and Tracking Lab

```python
# %% [markdown]
# # 🧪 MLflow Dataset Versioning and Tracking Lab
#
# ## Learning Objectives
# By the end of this lab, you will be able to:
# - Understand MLflow's dataset tracking capabilities
# - Version different types of datasets (CSV, Images, JSON, Parquet)
# - Track dataset metadata and lineage
# - Compare dataset versions across experiments
#
# ## Prerequisites
# - Python 3.8+
# - MLflow installed
# - Basic understanding of machine learning workflows

# %% [markdown]
# ## 📦 Step 1: Environment Setup
#
# First, let's install and import all necessary libraries.
# Run the cell below to set up your environment.

# %%
# Install required packages (uncomment if needed)
# #!pip install mlflow pandas numpy scikit-learn pillow pyarrow boto3

# %%
# Import required libraries
import mlflow
from mlflow.data.pandas_dataset import PandasDataset
from mlflow.data.numpy_dataset import NumpyDataset
import mlflow.data as mlflow_data

import pandas as pd
import numpy as np
import json
import os
import shutil
from datetime import datetime
from PIL import Image
import hashlib
from sklearn.datasets import load_iris, load_wine, fetch_california_housing
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

print("✅ All libraries imported successfully!")
print(f"MLflow version: {mlflow.__version__}")

# %% [markdown]
# ## 🔧 Step 2: MLflow Configuration
#
# Configure MLflow to connect to your tracking server.
#
# **Important:** Make sure your MLflow server is running at the specified URI.
#
# To start a local MLflow server, run in terminal:
# ```bash
# mlflow server --host 0.0.0.0 --port 5000
# ```

# %%
# MLflow Configuration
MLFLOW_TRACKING_URI = "http://localhost:5000"

# Set the tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Verify connection
try:
    client = mlflow.tracking.MlflowClient()
    experiments = client.search_experiments()
    print(f"✅ Successfully connected to MLflow at: {MLFLOW_TRACKING_URI}")
    print(f"📊 Number of existing experiments: {len(experiments)}")
except Exception as e:
    print(f"❌ Failed to connect to MLflow: {e}")
    print("💡 Tip: Make sure MLflow server is running!")

# %% [markdown]
# ## 📁 Step 3: Create Working Directories
#
# We'll create directories to store our sample datasets.

# %%
# Create directories for datasets
DATASET_DIR = "./mlflow_datasets_lab"
CSV_DIR = os.path.join(DATASET_DIR, "csv")
IMAGE_DIR = os.path.join(DATASET_DIR, "images")
JSON_DIR = os.path.join(DATASET_DIR, "json")
PARQUET_DIR = os.path.join(DATASET_DIR, "parquet")

# Create all directories
for directory in [DATASET_DIR, CSV_DIR, IMAGE_DIR, JSON_DIR, PARQUET_DIR]:
    os.makedirs(directory, exist_ok=True)
    print(f"📂 Created directory: {directory}")

print("\n✅ All directories created successfully!")

# %% [markdown]
# ---
# # 📊 PART 1: CSV Dataset Versioning
# ---
#
# ## Step 4: Create and Version CSV Datasets
#
# In this section, we'll learn how to:
# 1. Create sample CSV datasets
# 2. Track them with MLflow
# 3. Create multiple versions
# 4. Compare versions

# %% [markdown]
# ### 4.1 Create Sample CSV Datasets
#
# We'll create a customer dataset with multiple versions simulating
# data updates over time.

# %%
def create_customer_dataset_v1():
    """
    Create Version 1 of customer dataset.
    This represents our initial data collection.
    """
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 70, n_samples),
        'income': np.random.normal(50000, 15000, n_samples).astype(int),
        'spending_score': np.random.randint(1, 100, n_samples),
        'membership_years': np.random.randint(0, 10, n_samples),
        'churn': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    }
    
    df = pd.DataFrame(data)
    return df

def create_customer_dataset_v2():
    """
    Create Version 2 of customer dataset.
    Simulates data update with:
    - More samples
    - New feature (region)
    - Updated values
    """
    np.random.seed(43)
    n_samples = 1500  # More data collected
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 75, n_samples),
        'income': np.random.normal(55000, 18000, n_samples).astype(int),
        'spending_score': np.random.randint(1, 100, n_samples),
        'membership_years': np.random.randint(0, 15, n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
        'churn': np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
    }
    
    df = pd.DataFrame(data)
    return df

# Create datasets
df_v1 = create_customer_dataset_v1()
df_v2 = create_customer_dataset_v2()

# Save to CSV files
csv_path_v1 = os.path.join(CSV_DIR, "customers_v1.csv")
csv_path_v2 = os.path.join(CSV_DIR, "customers_v2.csv")

df_v1.to_csv(csv_path_v1, index=False)
df_v2.to_csv(csv_path_v2, index=False)

print("📊 Customer Dataset Version 1:")
print(f"   Shape: {df_v1.shape}")
print(f"   Columns: {list(df_v1.columns)}")
print(f"   Saved to: {csv_path_v1}")

print("\n📊 Customer Dataset Version 2:")
print(f"   Shape: {df_v2.shape}")
print(f"   Columns: {list(df_v2.columns)}")
print(f"   Saved to: {csv_path_v2}")

# %% [markdown]
# ### 4.2 Track CSV Dataset with MLflow
#
# Now let's create an MLflow experiment and log our CSV datasets
# with proper versioning and metadata.

# %%
def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file for versioning."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_dataset_stats(df):
    """Generate statistics for a DataFrame."""
    stats = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
    }
    
    # Add numeric column statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        stats["numeric_stats"] = df[numeric_cols].describe().to_dict()
    
    return stats

print("✅ Helper functions created!")

# %%
# Create experiment for CSV datasets
EXPERIMENT_NAME_CSV = "CSV_Dataset_Versioning_Lab"

# Set or create experiment
mlflow.set_experiment(EXPERIMENT_NAME_CSV)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME_CSV)
print(f"📁 Experiment: {EXPERIMENT_NAME_CSV}")
print(f"   Experiment ID: {experiment.experiment_id}")

# %%
# Log CSV Dataset Version 1
print("🔄 Logging CSV Dataset Version 1...")

with mlflow.start_run(run_name="customer_dataset_v1") as run:
    # Load the dataset for MLflow
    df = pd.read_csv(csv_path_v1)
    
    # Create MLflow dataset
    dataset = mlflow.data.from_pandas(
        df, 
        source=csv_path_v1,
        name="customer_churn_dataset",
        targets="churn"
    )
    
    # Log the dataset
    mlflow.log_input(dataset, context="training")
    
    # Log dataset metadata as parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "customer_churn")
    mlflow.log_param("data_source", "synthetic")
    mlflow.log_param("creation_date", datetime.now().isoformat())
    
    # Log dataset statistics as metrics
    stats = get_dataset_stats(df)
    mlflow.log_metric("num_rows", stats["num_rows"])
    mlflow.log_metric("num_columns", stats["num_columns"])
    mlflow.log_metric("memory_mb", stats["memory_usage_mb"])
    mlflow.log_metric("missing_total", sum(stats["missing_values"].values()))
    mlflow.log_metric("churn_rate", df['churn'].mean())
    
    # Log the actual CSV file as artifact
    mlflow.log_artifact(csv_path_v1, artifact_path="datasets")
    
    # Log schema information
    schema_info = {
        "columns": stats["columns"],
        "dtypes": stats["dtypes"],
        "version": "1.0.0"
    }
    schema_path = os.path.join(CSV_DIR, "schema_v1.json")
    with open(schema_path, 'w') as f:
        json.dump(schema_info, f, indent=2)
    mlflow.log_artifact(schema_path, artifact_path="schema")
    
    # Log file hash for integrity
    file_hash = calculate_file_hash(csv_path_v1)
    mlflow.log_param("file_hash_md5", file_hash)
    
    run_id_v1 = run.info.run_id
    print(f"✅ Dataset v1 logged successfully!")
    print(f"   Run ID: {run_id_v1}")
    print(f"   File Hash: {file_hash}")

# %%
# Log CSV Dataset Version 2
print("🔄 Logging CSV Dataset Version 2...")

with mlflow.start_run(run_name="customer_dataset_v2") as run:
    # Load the dataset
    df = pd.read_csv(csv_path_v2)
    
    # Create MLflow dataset
    dataset = mlflow.data.from_pandas(
        df, 
        source=csv_path_v2,
        name="customer_churn_dataset",
        targets="churn"
    )
    
    # Log the dataset
    mlflow.log_input(dataset, context="training")
    
    # Log dataset metadata
    mlflow.log_param("dataset_version", "2.0.0")
    mlflow.log_param("dataset_name", "customer_churn")
    mlflow.log_param("data_source", "synthetic")
    mlflow.log_param("creation_date", datetime.now().isoformat())
    mlflow.log_param("changes_from_v1", "Added region column, more samples")
    
    # Log statistics
    stats = get_dataset_stats(df)
    mlflow.log_metric("num_rows", stats["num_rows"])
    mlflow.log_metric("num_columns", stats["num_columns"])
    mlflow.log_metric("memory_mb", stats["memory_usage_mb"])
    mlflow.log_metric("missing_total", sum(stats["missing_values"].values()))
    mlflow.log_metric("churn_rate", df['churn'].mean())
    
    # Log artifact
    mlflow.log_artifact(csv_path_v2, artifact_path="datasets")
    
    # Log schema
    schema_info = {
        "columns": stats["columns"],
        "dtypes": stats["dtypes"],
        "version": "2.0.0"
    }
    schema_path = os.path.join(CSV_DIR, "schema_v2.json")
    with open(schema_path, 'w') as f:
        json.dump(schema_info, f, indent=2)
    mlflow.log_artifact(schema_path, artifact_path="schema")
    
    file_hash = calculate_file_hash(csv_path_v2)
    mlflow.log_param("file_hash_md5", file_hash)
    
    run_id_v2 = run.info.run_id
    print(f"✅ Dataset v2 logged successfully!")
    print(f"   Run ID: {run_id_v2}")
    print(f"   File Hash: {file_hash}")

# %% [markdown]
# ### 4.3 Compare CSV Dataset Versions
#
# Let's retrieve and compare the two versions we logged.

# %%
# Compare dataset versions
print("📊 Comparing Dataset Versions:")
print("=" * 60)

client = mlflow.tracking.MlflowClient()

# Get runs from the experiment
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"]
)

comparison_data = []
for run in runs:
    if "customer_dataset" in run.info.run_name:
        version_info = {
            "Run Name": run.info.run_name,
            "Version": run.data.params.get("dataset_version", "N/A"),
            "Rows": run.data.metrics.get("num_rows", "N/A"),
            "Columns": run.data.metrics.get("num_columns", "N/A"),
            "Churn Rate": f"{run.data.metrics.get('churn_rate', 0):.2%}",
            "Memory (MB)": f"{run.data.metrics.get('memory_mb', 0):.2f}"
        }
        comparison_data.append(version_info)

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# %% [markdown]
# ---
# # 🖼️ PART 2: Image Dataset Versioning
# ---
#
# ## Step 5: Create and Version Image Datasets
#
# In this section, we'll learn how to:
# 1. Generate synthetic image datasets
# 2. Track image datasets with metadata
# 3. Log image statistics and samples

# %% [markdown]
# ### 5.1 Create Synthetic Image Dataset
#
# We'll create a simple image classification dataset with
# geometric shapes (circles, squares, triangles).

# %%
def create_shape_image(shape, size=64, color=None):
    """Create an image with a specific shape."""
    if color is None:
        color = tuple(np.random.randint(100, 255, 3))
    
    # Create a white background
    img = Image.new('RGB', (size, size), color=(255, 255, 255))
    pixels = img.load()
    
    center = size // 2
    radius = size // 3
    
    if shape == 'circle':
        for x in range(size):
            for y in range(size):
                if (x - center) ** 2 + (y - center) ** 2 <= radius ** 2:
                    pixels[x, y] = color
                    
    elif shape == 'square':
        for x in range(center - radius, center + radius):
            for y in range(center - radius, center + radius):
                if 0 <= x < size and 0 <= y < size:
                    pixels[x, y] = color
                    
    elif shape == 'triangle':
        for y in range(center - radius, center + radius):
            width = int((y - (center - radius)) * radius / radius)
            for x in range(center - width, center + width):
                if 0 <= x < size and 0 <= y < size:
                    pixels[x, y] = color
    
    return img

def create_image_dataset(version, num_per_class=50):
    """Create a complete image dataset with multiple classes."""
    shapes = ['circle', 'square', 'triangle']
    dataset_info = {
        'version': version,
        'classes': shapes,
        'images_per_class': num_per_class,
        'total_images': num_per_class * len(shapes),
        'image_size': 64,
        'files': []
    }
    
    version_dir = os.path.join(IMAGE_DIR, f"v{version}")
    os.makedirs(version_dir, exist_ok=True)
    
    for shape in shapes:
        class_dir = os.path.join(version_dir, shape)
        os.makedirs(class_dir, exist_ok=True)
        
        for i in range(num_per_class):
            img = create_shape_image(shape)
            filename = f"{shape}_{i:04d}.png"
            filepath = os.path.join(class_dir, filename)
            img.save(filepath)
            dataset_info['files'].append({
                'path': filepath,
                'class': shape,
                'filename': filename
            })
    
    return dataset_info, version_dir

print("✅ Image generation functions created!")

# %%
# Create Image Dataset Version 1 (smaller dataset)
print("🖼️ Creating Image Dataset Version 1...")
image_info_v1, image_dir_v1 = create_image_dataset(version=1, num_per_class=30)
print(f"   Total images: {image_info_v1['total_images']}")
print(f"   Classes: {image_info_v1['classes']}")
print(f"   Location: {image_dir_v1}")

# Create Image Dataset Version 2 (larger dataset)
print("\n🖼️ Creating Image Dataset Version 2...")
image_info_v2, image_dir_v2 = create_image_dataset(version=2, num_per_class=50)
print(f"   Total images: {image_info_v2['total_images']}")
print(f"   Classes: {image_info_v2['classes']}")
print(f"   Location: {image_dir_v2}")

# %% [markdown]
# ### 5.2 Track Image Dataset with MLflow
#
# Now let's log our image datasets with proper tracking and metadata.

# %%
def get_image_dataset_stats(dataset_dir):
    """Calculate statistics for an image dataset."""
    stats = {
        'total_images': 0,
        'total_size_mb': 0,
        'classes': {},
        'image_dimensions': set()
    }
    
    for class_name in os.listdir(dataset_dir):
        class_path = os.path.join(dataset_dir, class_name)
        if os.path.isdir(class_path):
            class_images = [f for f in os.listdir(class_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            stats['classes'][class_name] = len(class_images)
            stats['total_images'] += len(class_images)
            
            for img_file in class_images[:5]:  # Check first 5 images
                img_path = os.path.join(class_path, img_file)
                stats['total_size_mb'] += os.path.getsize(img_path) / (1024 * 1024)
                
                with Image.open(img_path) as img:
                    stats['image_dimensions'].add(img.size)
    
    stats['image_dimensions'] = list(stats['image_dimensions'])
    return stats

# Create experiment for image datasets
EXPERIMENT_NAME_IMAGES = "Image_Dataset_Versioning_Lab"
mlflow.set_experiment(EXPERIMENT_NAME_IMAGES)

print(f"📁 Experiment: {EXPERIMENT_NAME_IMAGES}")

# %%
# Log Image Dataset Version 1
print("🔄 Logging Image Dataset Version 1...")

with mlflow.start_run(run_name="shapes_dataset_v1") as run:
    # Calculate statistics
    stats = get_image_dataset_stats(image_dir_v1)
    
    # Log parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "geometric_shapes")
    mlflow.log_param("image_format", "PNG")
    mlflow.log_param("image_size", "64x64")
    mlflow.log_param("num_classes", len(stats['classes']))
    mlflow.log_param("class_names", list(stats['classes'].keys()))
    mlflow.log_param("creation_date", datetime.now().isoformat())
    
    # Log metrics
    mlflow.log_metric("total_images", stats['total_images'])
    mlflow.log_metric("total_size_mb", stats['total_size_mb'])
    
    for class_name, count in stats['classes'].items():
        mlflow.log_metric(f"class_{class_name}_count", count)
    
    # Log sample images from each class
    for class_name in stats['classes'].keys():
        class_path = os.path.join(image_dir_v1, class_name)
        sample_images = os.listdir(class_path)[:3]  # Log 3 samples per class
        
        for img_name in sample_images:
            img_path = os.path.join(class_path, img_name)
            mlflow.log_artifact(img_path, artifact_path=f"samples/{class_name}")
    
    # Log dataset info as JSON
    info_path = os.path.join(image_dir_v1, "dataset_info.json")
    with open(info_path, 'w') as f:
        json.dump({
            **image_info_v1,
            'stats': {k: v for k, v in stats.items() if k != 'image_dimensions'}
        }, f, indent=2, default=str)
    mlflow.log_artifact(info_path, artifact_path="metadata")
    
    run_id_img_v1 = run.info.run_id
    print(f"✅ Image Dataset v1 logged!")
    print(f"   Run ID: {run_id_img_v1}")
    print(f"   Total Images: {stats['total_images']}")

# %%
# Log Image Dataset Version 2
print("🔄 Logging Image Dataset Version 2...")

with mlflow.start_run(run_name="shapes_dataset_v2") as run:
    # Calculate statistics
    stats = get_image_dataset_stats(image_dir_v2)
    
    # Log parameters
    mlflow.log_param("dataset_version", "2.0.0")
    mlflow.log_param("dataset_name", "geometric_shapes")
    mlflow.log_param("image_format", "PNG")
    mlflow.log_param("image_size", "64x64")
    mlflow.log_param("num_classes", len(stats['classes']))
    mlflow.log_param("class_names", list(stats['classes'].keys()))
    mlflow.log_param("creation_date", datetime.now().isoformat())
    mlflow.log_param("changes_from_v1", "Increased samples per class")
    
    # Log metrics
    mlflow.log_metric("total_images", stats['total_images'])
    mlflow.log_metric("total_size_mb", stats['total_size_mb'])
    
    for class_name, count in stats['classes'].items():
        mlflow.log_metric(f"class_{class_name}_count", count)
    
    # Log sample images
    for class_name in stats['classes'].keys():
        class_path = os.path.join(image_dir_v2, class_name)
        sample_images = os.listdir(class_path)[:3]
        
        for img_name in sample_images:
            img_path = os.path.join(class_path, img_name)
            mlflow.log_artifact(img_path, artifact_path=f"samples/{class_name}")
    
    # Log dataset info
    info_path = os.path.join(image_dir_v2, "dataset_info.json")
    with open(info_path, 'w') as f:
        json.dump({
            **image_info_v2,
            'stats': {k: v for k, v in stats.items() if k != 'image_dimensions'}
        }, f, indent=2, default=str)
    mlflow.log_artifact(info_path, artifact_path="metadata")
    
    run_id_img_v2 = run.info.run_id
    print(f"✅ Image Dataset v2 logged!")
    print(f"   Run ID: {run_id_img_v2}")
    print(f"   Total Images: {stats['total_images']}")

# %% [markdown]
# ---
# # 📋 PART 3: JSON Dataset Versioning
# ---
#
# ## Step 6: Create and Version JSON Datasets
#
# JSON datasets are common for NLP tasks, configuration data,
# and semi-structured data. Let's learn how to version them.

# %% [markdown]
# ### 6.1 Create Sample JSON Datasets

# %%
def create_text_classification_dataset(version, num_samples=100):
    """Create a text classification dataset in JSON format."""
    
    categories = ['sports', 'technology', 'politics', 'entertainment']
    
    sample_texts = {
        'sports': [
            "The team won the championship game last night",
            "Athletes prepare for the upcoming Olympics",
            "Football season starts next month",
            "The basketball player scored 30 points",
            "Tennis tournament reaches final stages"
        ],
        'technology': [
            "New smartphone features advanced AI capabilities",
            "Tech company releases latest software update",
            "Scientists develop revolutionary battery technology",
            "Cloud computing transforms business operations",
            "Artificial intelligence continues to evolve"
        ],
        'politics': [
            "Government announces new economic policies",
            "Elections scheduled for next year",
            "International summit addresses climate change",
            "New legislation passes in parliament",
            "Diplomatic relations improve between nations"
        ],
        'entertainment': [
            "Movie breaks box office records",
            "Popular singer announces world tour",
            "Streaming service adds new content",
            "Award show celebrates best performances",
            "New video game receives critical acclaim"
        ]
    }
    
    data = []
    for i in range(num_samples):
        category = np.random.choice(categories)
        text = np.random.choice(sample_texts[category])
        
        # Add some variation
        text = text + f" (Sample {i})"
        
        data.append({
            'id': i,
            'text': text,
            'label': category,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'source': 'synthetic',
                'version': version,
                'confidence': round(np.random.uniform(0.7, 1.0), 2)
            }
        })
    
    return data

# Create JSON datasets
json_data_v1 = create_text_classification_dataset(version=1, num_samples=100)
json_data_v2 = create_text_classification_dataset(version=2, num_samples=200)

# Save to files
json_path_v1 = os.path.join(JSON_DIR, "text_classification_v1.json")
json_path_v2 = os.path.join(JSON_DIR, "text_classification_v2.json")

with open(json_path_v1, 'w') as f:
    json.dump(json_data_v1, f, indent=2)

with open(json_path_v2, 'w') as f:
    json.dump(json_data_v2, f, indent=2)

print("📋 JSON Dataset Version 1:")
print(f"   Samples: {len(json_data_v1)}")
print(f"   Saved to: {json_path_v1}")

print("\n📋 JSON Dataset Version 2:")
print(f"   Samples: {len(json_data_v2)}")
print(f"   Saved to: {json_path_v2}")

# %% [markdown]
# ### 6.2 Track JSON Dataset with MLflow

# %%
def get_json_dataset_stats(json_data):
    """Calculate statistics for JSON dataset."""
    df = pd.DataFrame(json_data)
    
    stats = {
        'total_samples': len(json_data),
        'label_distribution': df['label'].value_counts().to_dict(),
        'avg_text_length': df['text'].str.len().mean(),
        'unique_labels': df['label'].nunique()
    }
    
    return stats

# Create experiment for JSON datasets
EXPERIMENT_NAME_JSON = "JSON_Dataset_Versioning_Lab"
mlflow.set_experiment(EXPERIMENT_NAME_JSON)

print(f"📁 Experiment: {EXPERIMENT_NAME_JSON}")

# %%
# Log JSON Dataset Version 1
print("🔄 Logging JSON Dataset Version 1...")

with mlflow.start_run(run_name="text_classification_v1") as run:
    # Load and analyze
    with open(json_path_v1, 'r') as f:
        data = json.load(f)
    
    stats = get_json_dataset_stats(data)
    
    # Log parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "text_classification")
    mlflow.log_param("data_format", "JSON")
    mlflow.log_param("task_type", "multi-class classification")
    mlflow.log_param("num_classes", stats['unique_labels'])
    mlflow.log_param("creation_date", datetime.now().isoformat())
    
    # Log metrics
    mlflow.log_metric("total_samples", stats['total_samples'])
    mlflow.log_metric("avg_text_length", stats['avg_text_length'])
    mlflow.log_metric("num_classes", stats['unique_labels'])
    
    for label, count in stats['label_distribution'].items():
        mlflow.log_metric(f"label_{label}_count", count)
    
    # Log artifact
    mlflow.log_artifact(json_path_v1, artifact_path="datasets")
    
    # Log file hash
    file_hash = calculate_file_hash(json_path_v1)
    mlflow.log_param("file_hash_md5", file_hash)
    
    print(f"✅ JSON Dataset v1 logged!")
    print(f"   Run ID: {run.info.run_id}")

# %%
# Log JSON Dataset Version 2
print("🔄 Logging JSON Dataset Version 2...")

with mlflow.start_run(run_name="text_classification_v2") as run:
    with open(json_path_v2, 'r') as f:
        data = json.load(f)
    
    stats = get_json_dataset_stats(data)
    
    mlflow.log_param("dataset_version", "2.0.0")
    mlflow.log_param("dataset_name", "text_classification")
    mlflow.log_param("data_format", "JSON")
    mlflow.log_param("task_type", "multi-class classification")
    mlflow.log_param("num_classes", stats['unique_labels'])
    mlflow.log_param("creation_date", datetime.now().isoformat())
    mlflow.log_param("changes_from_v1", "Doubled sample size")
    
    mlflow.log_metric("total_samples", stats['total_samples'])
    mlflow.log_metric("avg_text_length", stats['avg_text_length'])
    mlflow.log_metric("num_classes", stats['unique_labels'])
    
    for label, count in stats['label_distribution'].items():
        mlflow.log_metric(f"label_{label}_count", count)
    
    mlflow.log_artifact(json_path_v2, artifact_path="datasets")
    
    file_hash = calculate_file_hash(json_path_v2)
    mlflow.log_param("file_hash_md5", file_hash)
    
    print(f"✅ JSON Dataset v2 logged!")
    print(f"   Run ID: {run.info.run_id}")

# %% [markdown]
# ---
# # 📦 PART 4: Parquet Dataset Versioning
# ---
#
# ## Step 7: Create and Version Parquet Datasets
#
# Parquet is a columnar storage format that's efficient for
# large datasets. It's commonly used in big data pipelines.

# %% [markdown]
# ### 7.1 Create Parquet Datasets

# %%
def create_sales_dataset(version, num_records=10000):
    """Create a sales dataset and save as Parquet."""
    np.random.seed(40 + version)
    
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
    
    data = {
        'transaction_id': range(1, num_records + 1),
        'date': pd.date_range(start='2023-01-01', periods=num_records, freq='H'),
        'product': np.random.choice(products, num_records),
        'region': np.random.choice(regions, num_records),
        'quantity': np.random.randint(1, 20, num_records),
        'unit_price': np.random.uniform(50, 2000, num_records).round(2),
        'discount': np.random.uniform(0, 0.3, num_records).round(2)
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = (df['quantity'] * df['unit_price'] * (1 - df['discount'])).round(2)
    
    return df

# Create Parquet datasets
parquet_df_v1 = create_sales_dataset(version=1, num_records=10000)
parquet_df_v2 = create_sales_dataset(version=2, num_records=25000)

# Save to Parquet
parquet_path_v1 = os.path.join(PARQUET_DIR, "sales_v1.parquet")
parquet_path_v2 = os.path.join(PARQUET_DIR, "sales_v2.parquet")

parquet_df_v1.to_parquet(parquet_path_v1, index=False)
parquet_df_v2.to_parquet(parquet_path_v2, index=False)

print("📦 Parquet Dataset Version 1:")
print(f"   Records: {len(parquet_df_v1)}")
print(f"   Columns: {list(parquet_df_v1.columns)}")
print(f"   File Size: {os.path.getsize(parquet_path_v1) / 1024:.2f} KB")

print("\n📦 Parquet Dataset Version 2:")
print(f"   Records: {len(parquet_df_v2)}")
print(f"   Columns: {list(parquet_df_v2.columns)}")
print(f"   File Size: {os.path.getsize(parquet_path_v2) / 1024:.2f} KB")

# %% [markdown]
# ### 7.2 Track Parquet Dataset with MLflow

# %%
# Create experiment for Parquet datasets
EXPERIMENT_NAME_PARQUET = "Parquet_Dataset_Versioning_Lab"
mlflow.set_experiment(EXPERIMENT_NAME_PARQUET)

print(f"📁 Experiment: {EXPERIMENT_NAME_PARQUET}")

# %%
# Log Parquet Dataset Version 1
print("🔄 Logging Parquet Dataset Version 1...")

with mlflow.start_run(run_name="sales_parquet_v1") as run:
    df = pd.read_parquet(parquet_path_v1)
    
    # Create MLflow dataset from parquet
    dataset = mlflow.data.from_pandas(
        df,
        source=parquet_path_v1,
        name="sales_transactions"
    )
    
    mlflow.log_input(dataset, context="training")
    
    # Log parameters
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "sales_transactions")
    mlflow.log_param("data_format", "Parquet")
    mlflow.log_param("compression", "snappy")
    mlflow.log_param("creation_date", datetime.now().isoformat())
    
    # Log metrics
    mlflow.log_metric("num_records", len(df))
    mlflow.log_metric("num_columns", len(df.columns))
    mlflow.log_metric("file_size_kb", os.path.getsize(parquet_path_v1) / 1024)
    mlflow.log_metric("total_revenue", df['total_amount'].sum())
    mlflow.log_metric("avg_transaction", df['total_amount'].mean())
    mlflow.log_metric("unique_products", df['product'].nunique())
    mlflow.log_metric("unique_regions", df['region'].nunique())
    
    # Log artifact
    mlflow.log_artifact(parquet_path_v1, artifact_path="datasets")
    
    print(f"✅ Parquet Dataset v1 logged!")
    print(f"   Run ID: {run.info.run_id}")

# %%
# Log Parquet Dataset Version 2
print("🔄 Logging Parquet Dataset Version 2...")

with mlflow.start_run(run_name="sales_parquet_v2") as run:
    df = pd.read_parquet(parquet_path_v2)
    
    dataset = mlflow.data.from_pandas(
        df,
        source=parquet_path_v2,
        name="sales_transactions"
    )
    
    mlflow.log_input(dataset, context="training")
    
    mlflow.log_param("dataset_version", "2.0.0")
    mlflow.log_param("dataset_name", "sales_transactions")
    mlflow.log_param("data_format", "Parquet")
    mlflow.log_param("compression", "snappy")
    mlflow.log_param("creation_date", datetime.now().isoformat())
    mlflow.log_param("changes_from_v1", "2.5x more records")
    
    mlflow.log_metric("num_records", len(df))
    mlflow.log_metric("num_columns", len(df.columns))
    mlflow.log_metric("file_size_kb", os.path.getsize(parquet_path_v2) / 1024)
    mlflow.log_metric("total_revenue", df['total_amount'].sum())
    mlflow.log_metric("avg_transaction", df['total_amount'].mean())
    mlflow.log_metric("unique_products", df['product'].nunique())
    mlflow.log_metric("unique_regions", df['region'].nunique())
    
    mlflow.log_artifact(parquet_path_v2, artifact_path="datasets")
    
    print(f"✅ Parquet Dataset v2 logged!")
    print(f"   Run ID: {run.info.run_id}")

# %% [markdown]
# ---
# # 🔬 PART 5: Using Scikit-learn Built-in Datasets
# ---
#
# ## Step 8: Track Standard ML Datasets
#
# MLflow can also track popular datasets from scikit-learn.

# %%
# Create experiment for sklearn datasets
EXPERIMENT_NAME_SKLEARN = "Sklearn_Dataset_Versioning_Lab"
mlflow.set_experiment(EXPERIMENT_NAME_SKLEARN)

print(f"📁 Experiment: {EXPERIMENT_NAME_SKLEARN}")

# %%
# Log Iris Dataset
print("🌸 Logging Iris Dataset...")

with mlflow.start_run(run_name="iris_dataset") as run:
    # Load dataset
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_name'] = df['target'].map({i: name for i, name in enumerate(iris.target_names)})
    
    # Create MLflow dataset
    dataset = mlflow.data.from_pandas(
        df,
        source="sklearn.datasets.load_iris",
        name="iris_dataset",
        targets="target"
    )
    
    mlflow.log_input(dataset, context="training")
    
    # Log parameters
    mlflow.log_param("dataset_name", "iris")
    mlflow.log_param("source", "sklearn.datasets")
    mlflow.log_param("task_type", "classification")
    mlflow.log_param("num_classes", len(iris.target_names))
    mlflow.log_param("class_names", list(iris.target_names))
    mlflow.log_param("feature_names", list(iris.feature_names))
    
    # Log metrics
    mlflow.log_metric("num_samples", len(df))
    mlflow.log_metric("num_features", len(iris.feature_names))
    mlflow.log_metric("num_classes", len(iris.target_names))
    
    # Save and log artifact
    iris_path = os.path.join(CSV_DIR, "iris.csv")
    df.to_csv(iris_path, index=False)
    mlflow.log_artifact(iris_path, artifact_path="datasets")
    
    print(f"✅ Iris Dataset logged!")
    print(f"   Samples: {len(df)}, Features: {len(iris.feature_names)}")

# %%
# Log Wine Dataset
print("🍷 Logging Wine Dataset...")

with mlflow.start_run(run_name="wine_dataset") as run:
    wine = load_wine()
    df = pd.DataFrame(data=wine.data, columns=wine.feature_names)
    df['target'] = wine.target
    
    dataset = mlflow.data.from_pandas(
        df,
        source="sklearn.datasets.load_wine",
        name="wine_dataset",
        targets="target"
    )
    
    mlflow.log_input(dataset, context="training")
    
    mlflow.log_param("dataset_name", "wine")
    mlflow.log_param("source", "sklearn.datasets")
    mlflow.log_param("task_type", "classification")
    mlflow.log_param("num_classes", len(wine.target_names))
    
    mlflow.log_metric("num_samples", len(df))
    mlflow.log_metric("num_features", len(wine.feature_names))
    mlflow.log_metric("num_classes", len(wine.target_names))
    
    wine_path = os.path.join(CSV_DIR, "wine.csv")
    df.to_csv(wine_path, index=False)
    mlflow.log_artifact(wine_path, artifact_path="datasets")
    
    print(f"✅ Wine Dataset logged!")
    print(f"   Samples: {len(df)}, Features: {len(wine.feature_names)}")

# %%
# Log California Housing Dataset
print("🏠 Logging California Housing Dataset...")

with mlflow.start_run(run_name="california_housing_dataset") as run:
    housing = fetch_california_housing()
    df = pd.DataFrame(data=housing.data, columns=housing.feature_names)
    df['target'] = housing.target
    
    dataset = mlflow.data.from_pandas(
        df,
        source="sklearn.datasets.fetch_california_housing",
        name="california_housing",
        targets="target"
    )
    
    mlflow.log_input(dataset, context="training")
    
    mlflow.log_param("dataset_name", "california_housing")
    mlflow.log_param("source", "sklearn.datasets")
    mlflow.log_param("task_type", "regression")
    
    mlflow.log_metric("num_samples", len(df))
    mlflow.log_metric("num_features", len(housing.feature_names))
    mlflow.log_metric("target_mean", df['target'].mean())
    mlflow.log_metric("target_std", df['target'].std())
    
    housing_path = os.path.join(CSV_DIR, "california_housing.csv")
    df.to_csv(housing_path, index=False)
    mlflow.log_artifact(housing_path, artifact_path="datasets")
    
    print(f"✅ California Housing Dataset logged!")
    print(f"   Samples: {len(df)}, Features: {len(housing.feature_names)}")

# %% [markdown]
# ---
# # 📊 PART 6: Dataset Comparison Dashboard
# ---
#
# ## Step 9: Create a Summary of All Tracked Datasets

# %%
def get_all_dataset_runs():
    """Retrieve all dataset runs across experiments."""
    client = mlflow.tracking.MlflowClient()
    experiments = client.search_experiments()
    
    all_runs = []
    for exp in experiments:
        if "Lab" in exp.name:  # Filter our lab experiments
            runs = client.search_runs(experiment_ids=[exp.experiment_id])
            for run in runs:
                run_info = {
                    'experiment': exp.name,
                    'run_name': run.info.run_name,
                    'run_id': run.info.run_id[:8],  # Shortened
                    'status': run.info.status,
                    'dataset_version': run.data.params.get('dataset_version', 'N/A'),
                    'dataset_name': run.data.params.get('dataset_name', 'N/A'),
                    'num_samples': run.data.metrics.get('num_samples', 
                                   run.data.metrics.get('num_rows',
                                   run.data.metrics.get('total_samples',
                                   run.data.metrics.get('num_records',
                                   run.data.metrics.get('total_images', 'N/A'))))),
                }
                all_runs.append(run_info)
    
    return pd.DataFrame(all_runs)

# Get summary
print("📊 Dataset Tracking Summary")
print("=" * 80)

summary_df = get_all_dataset_runs()
if len(summary_df) > 0:
    print(summary_df.to_string(index=False))
else:
    print("No runs found. Make sure MLflow server is running and experiments were logged.")

# %% [markdown]
# ---
# # 🎯 PART 7: Best Practices and Tips
# ---
#
# ## Dataset Versioning Best Practices
#
# 1. **Always include version numbers** in your dataset parameters
# 2. **Calculate and log file hashes** for data integrity verification
# 3. **Log comprehensive metadata** including creation date, source, and changes
# 4. **Use meaningful run names** that reflect the dataset version
# 5. **Log sample artifacts** so you can quickly preview data in the UI
# 6. **Track data statistics** as metrics for easy comparison
# 7. **Document schema changes** between versions

# %% [markdown]
# ## 🧹 Step 10: Cleanup (Optional)
#
# Run this cell to clean up the created directories and files.

# %%
# Cleanup function (uncomment to use)
def cleanup():
    """Remove all created directories and files."""
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
        print(f"🗑️ Removed directory: {DATASET_DIR}")
    print("✅ Cleanup complete!")

# Uncomment the line below to clean up
# cleanup()

print("💡 To clean up, uncomment and run the cleanup() function above.")

# %% [markdown]
# ---
# # 📝 Lab Exercises
# ---
#
# ## Exercise 1: Create Your Own Dataset Version
# Create a new version (v3) of the customer dataset with additional features
# and log it to MLflow.
#
# ## Exercise 2: Image Dataset Augmentation
# Create a v3 of the image dataset with augmented images (rotations, flips)
# and track the augmentation parameters.
#
# ## Exercise 3: Compare Metrics
# Write code to compare the metrics between two dataset versions
# and highlight the differences.
#
# ## Exercise 4: Dataset Lineage
# Create a run that logs the relationship between a raw dataset and
# a processed/cleaned version.

# %% [markdown]
# ---
# # 🎉 Congratulations!
#
# You have completed the MLflow Dataset Versioning and Tracking Lab!
#
# ## What You Learned:
# - ✅ Setting up MLflow tracking
# - ✅ Versioning CSV datasets
# - ✅ Tracking image datasets
# - ✅ Managing JSON datasets
# - ✅ Working with Parquet files
# - ✅ Using sklearn built-in datasets
# - ✅ Comparing dataset versions
#
# ## Next Steps:
# 1. Explore the MLflow UI at http://localhost:5000
# 2. Try connecting datasets to model training runs
# 3. Implement automated dataset validation
# 4. Set up dataset alerts for drift detection
#
# ---
# **Happy Tracking! 🚀**
# ```
#
# # How to Use This Lab
#
# ## Prerequisites
#
# 1. **Start MLflow Server:**
# ```bash
# mlflow server --host 0.0.0.0 --port 5000
# ```
#
# 2. **Install Required Packages:**
# ```bash
# pip install mlflow pandas numpy scikit-learn pillow pyarrow
# ```
#
# ## Running the Lab
#
# 1. Save the code as `mlflow_dataset_lab.py`
# 2. Open in VS Code or JupyterLab
# 3. The `# %%` markers create executable cells
# 4. Run cells sequentially
#
# ## Lab Structure
#
# | Part | Content | Dataset Types |
# |------|---------|---------------|
# | 1 | CSV Dataset Versioning | Customer churn data |
# | 2 | Image Dataset Versioning | Geometric shapes |
# | 3 | JSON Dataset Versioning | Text classification |
# | 4 | Parquet Dataset Versioning | Sales transactions |
# | 5 | Sklearn Datasets | Iris, Wine, Housing |
# | 6 | Comparison Dashboard | All datasets |
# | 7 | Best Practices | Tips & Exercises |
