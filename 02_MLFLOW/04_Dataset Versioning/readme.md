# 📚 MLflow Dataset Versioning and Tracking

## คู่มือประกอบการเรียนรู้ - ทฤษฎีและปฏิบัติ

---

## 📋 สารบัญ

1. [บทนำ: ความสำคัญของ Dataset Versioning](#1-บทนำ-ความสำคัญของ-dataset-versioning)
2. [ทฤษฎี: Data Pipeline ใน MLOps](#2-ทฤษฎี-data-pipeline-ใน-mlops)
3. [MLflow Dataset Tracking Architecture](#3-mlflow-dataset-tracking-architecture)
4. [การ Version ข้อมูลประเภทต่างๆ](#4-การ-version-ข้อมูลประเภทต่างๆ)
5. [Best Practices และ Design Patterns](#5-best-practices-และ-design-patterns)
6. [แบบฝึกหัด](#6-แบบฝึกหัด)

---

## 1. บทนำ: ความสำคัญของ Dataset Versioning

### 1.1 ปัญหาที่พบบ่อยในการจัดการข้อมูล ML

ในโปรเจกต์ Machine Learning ทั่วไป ทีมมักประสบปัญหาเหล่านี้:

```
❌ "Model ทำงานได้ดีเมื่อวานนี้ แต่วันนี้ Accuracy ตก ไม่รู้ว่าเปลี่ยนอะไรไป"
❌ "ใช้ Data ชุดไหนในการ Train Model version ที่ deploy อยู่?"
❌ "ใครแก้ไข Dataset? เมื่อไหร่? แก้อะไร?"
❌ "ต้องการกลับไปใช้ Data version เดิม แต่ไม่มี backup"
```

### 1.2 Dataset Versioning คืออะไร?

**Dataset Versioning** คือกระบวนการติดตามและจัดการการเปลี่ยนแปลงของชุดข้อมูลอย่างเป็นระบบ คล้ายกับที่ Git ทำกับ Source Code

```
┌─────────────────────────────────────────────────────────────┐
│                    Dataset Versioning                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Dataset v1.0  ──►  Dataset v1.1  ──►  Dataset v2.0        │
│   (1000 rows)        (+500 rows)        (+new column)        │
│       │                  │                   │               │
│       ▼                  ▼                   ▼               │
│   Model v1           Model v2            Model v3            │
│   (Acc: 85%)        (Acc: 87%)          (Acc: 91%)          │
│                                                              │
│   ✓ Traceability: ติดตามได้ว่า Model ใช้ Data version ไหน   │
│   ✓ Reproducibility: สามารถ reproduce ผลลัพธ์ได้            │
│   ✓ Rollback: กลับไป version เดิมได้เมื่อเกิดปัญหา          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 ทำไมต้องใช้ MLflow สำหรับ Dataset Tracking?

| คุณสมบัติ | ประโยชน์ |
|-----------|---------|
| **Centralized Tracking** | เก็บข้อมูลทุกอย่างไว้ที่เดียว |
| **Metadata Logging** | บันทึก schema, statistics, hash |
| **Artifact Storage** | เก็บ Dataset files พร้อม versioning |
| **UI Dashboard** | ดูและเปรียบเทียบ versions ได้ง่าย |
| **API Access** | เข้าถึงข้อมูลผ่าน Python API |

---

## 2. ทฤษฎี: Data Pipeline ใน MLOps

### 2.1 ML Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        ML Data Pipeline                               │
└──────────────────────────────────────────────────────────────────────┘

     ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
     │  Raw    │    │  Data   │    │ Feature │    │ Model   │
     │  Data   │───►│ Process │───►│  Store  │───►│Training │
     └─────────┘    └─────────┘    └─────────┘    └─────────┘
          │              │              │              │
          ▼              ▼              ▼              ▼
     ┌─────────────────────────────────────────────────────┐
     │              MLflow Tracking Server                  │
     │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
     │  │Dataset  │ │ Process │ │Feature  │ │ Model   │   │
     │  │Metadata │ │  Logs   │ │Metadata │ │Metrics  │   │
     │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
     └─────────────────────────────────────────────────────┘
```

### 2.2 Data Lineage (สายพันธุ์ข้อมูล)

**Data Lineage** คือการติดตามที่มาและการเปลี่ยนแปลงของข้อมูลตลอด Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│                      Data Lineage Example                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                              │
│  │ Raw CSV      │ ◄── Source: Customer Database                │
│  │ v1.0         │     Date: 2024-01-01                         │
│  │ 1000 rows    │     Hash: abc123...                          │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼ Transformation: Remove nulls, normalize              │
│  ┌──────────────┐                                              │
│  │ Cleaned CSV  │ ◄── Process: clean_data.py                   │
│  │ v1.1         │     Date: 2024-01-02                         │
│  │ 950 rows     │     Parent: v1.0                             │
│  └──────┬───────┘                                              │
│         │                                                       │
│         ▼ Transformation: Feature engineering                   │
│  ┌──────────────┐                                              │
│  │ Feature Set  │ ◄── Process: feature_eng.py                  │
│  │ v1.0         │     Date: 2024-01-03                         │
│  │ 950 rows     │     Parent: cleaned v1.1                     │
│  │ 15 features  │                                              │
│  └──────────────┘                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### 2.3 Dataset Versioning Strategies

#### Strategy 1: Semantic Versioning (MAJOR.MINOR.PATCH)

```python
# Version Number Meaning:
# MAJOR: Breaking changes (schema change, column removal)
# MINOR: Backward compatible additions (new rows, new columns)
# PATCH: Bug fixes (data corrections)

version_examples = {
    "1.0.0": "Initial dataset",
    "1.1.0": "Added 500 new samples",        # Minor: more data
    "1.1.1": "Fixed typos in labels",        # Patch: corrections
    "2.0.0": "Added 'region' column",        # Major: schema change
}
```

#### Strategy 2: Date-based Versioning

```python
# Format: YYYY-MM-DD or YYYYMMDD
version_examples = {
    "2024-01-01": "January snapshot",
    "2024-02-01": "February snapshot",
    "2024-02-15": "Mid-month update",
}
```

#### Strategy 3: Hash-based Versioning

```python
# ใช้ Content Hash เป็น Version Identifier
import hashlib

def get_dataset_version(filepath):
    """สร้าง version จาก file content hash"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()[:8]  # ใช้ 8 characters แรก

# ผลลัพธ์: "a1b2c3d4"
```

---

## 3. MLflow Dataset Tracking Architecture

### 3.1 MLflow Components สำหรับ Dataset Tracking

```
┌─────────────────────────────────────────────────────────────────┐
│                   MLflow Dataset Tracking                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Experiments   │  │      Runs       │  │    Artifacts    │ │
│  │─────────────────│  │─────────────────│  │─────────────────│ │
│  │ • CSV_Dataset   │  │ • Parameters    │  │ • Dataset files │ │
│  │ • Image_Dataset │  │ • Metrics       │  │ • Schema JSON   │ │
│  │ • JSON_Dataset  │  │ • Tags          │  │ • Samples       │ │
│  │ • Parquet_Data  │  │ • Dataset Input │  │ • Metadata      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                    │                    │           │
│           └────────────────────┼────────────────────┘           │
│                                ▼                                 │
│                    ┌───────────────────┐                        │
│                    │  Tracking Server  │                        │
│                    │   (SQLite/DB)     │                        │
│                    └───────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 MLflow Dataset Types

MLflow รองรับ Dataset หลายประเภท:

```python
from mlflow.data.pandas_dataset import PandasDataset
from mlflow.data.numpy_dataset import NumpyDataset
from mlflow.data.spark_dataset import SparkDataset

# 1. Pandas Dataset
dataset = mlflow.data.from_pandas(
    df,                          # DataFrame
    source="path/to/file.csv",   # แหล่งที่มา
    name="my_dataset",           # ชื่อ dataset
    targets="label_column"       # target column (optional)
)

# 2. NumPy Dataset
dataset = mlflow.data.from_numpy(
    features=X,                  # feature array
    targets=y,                   # target array
    source="sklearn.datasets"
)
```

### 3.3 Logging Dataset to MLflow

```python
# โครงสร้างการ Log Dataset แบบสมบูรณ์

with mlflow.start_run(run_name="dataset_v1"):
    
    # 1. สร้าง MLflow Dataset object
    dataset = mlflow.data.from_pandas(df, source=filepath)
    
    # 2. Log Dataset Input (สำคัญ!)
    mlflow.log_input(dataset, context="training")
    
    # 3. Log Parameters (Metadata)
    mlflow.log_param("dataset_version", "1.0.0")
    mlflow.log_param("dataset_name", "customer_data")
    mlflow.log_param("source_type", "csv")
    mlflow.log_param("creation_date", "2024-01-01")
    
    # 4. Log Metrics (Statistics)
    mlflow.log_metric("num_rows", len(df))
    mlflow.log_metric("num_columns", len(df.columns))
    mlflow.log_metric("missing_values", df.isnull().sum().sum())
    
    # 5. Log Artifacts (Files)
    mlflow.log_artifact(filepath, artifact_path="datasets")
```

### 3.4 Dataset Statistics ที่ควร Track

```python
def get_comprehensive_dataset_stats(df):
    """
    คำนวณ Statistics ที่สำคัญสำหรับ Dataset
    """
    stats = {
        # Basic Info
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024**2),
        
        # Data Quality
        "missing_total": df.isnull().sum().sum(),
        "missing_percentage": (df.isnull().sum().sum() / df.size) * 100,
        "duplicate_rows": df.duplicated().sum(),
        
        # Column Types
        "numeric_columns": len(df.select_dtypes(include=['number']).columns),
        "categorical_columns": len(df.select_dtypes(include=['object']).columns),
        "datetime_columns": len(df.select_dtypes(include=['datetime']).columns),
    }
    
    # Target Distribution (ถ้ามี target column)
    if 'target' in df.columns:
        stats["target_distribution"] = df['target'].value_counts().to_dict()
        stats["class_balance_ratio"] = df['target'].value_counts().min() / df['target'].value_counts().max()
    
    return stats
```

---

## 4. การ Version ข้อมูลประเภทต่างๆ

### 4.1 CSV Dataset Versioning

**Use Cases:** Tabular data, Customer data, Transaction logs

```
┌────────────────────────────────────────────────────────────┐
│                    CSV Dataset Workflow                     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌────────────┐ │
│  │  Read CSV   │ ───► │  Validate   │ ───► │  Log to    │ │
│  │             │      │  Schema     │      │  MLflow    │ │
│  └─────────────┘      └─────────────┘      └────────────┘ │
│         │                    │                    │        │
│         ▼                    ▼                    ▼        │
│   pd.read_csv()      Check columns,       log_input(),    │
│                      dtypes, nulls        log_artifact()  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Key Tracking Elements:**

```python
# สิ่งที่ควร Track สำหรับ CSV Dataset
tracking_elements = {
    "parameters": [
        "dataset_version",
        "file_hash_md5",      # สำหรับ integrity check
        "schema_version",
        "encoding",           # e.g., "utf-8"
        "delimiter",          # e.g., ","
    ],
    "metrics": [
        "num_rows",
        "num_columns", 
        "missing_values",
        "memory_mb",
        "target_distribution",  # สำหรับ classification
    ],
    "artifacts": [
        "dataset.csv",
        "schema.json",
        "statistics.json",
    ]
}
```

### 4.2 Image Dataset Versioning

**Use Cases:** Computer Vision, Image Classification, Object Detection

```
┌─────────────────────────────────────────────────────────────┐
│                  Image Dataset Structure                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  dataset/                                                    │
│  ├── v1/                                                    │
│  │   ├── class_a/                                           │
│  │   │   ├── img_0001.png                                   │
│  │   │   ├── img_0002.png                                   │
│  │   │   └── ...                                            │
│  │   ├── class_b/                                           │
│  │   │   ├── img_0001.png                                   │
│  │   │   └── ...                                            │
│  │   └── dataset_info.json                                  │
│  └── v2/                                                    │
│      ├── class_a/                                           │
│      ├── class_b/                                           │
│      ├── class_c/           ◄── New class added             │
│      └── dataset_info.json                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Tracking Elements:**

```python
# สิ่งที่ควร Track สำหรับ Image Dataset
tracking_elements = {
    "parameters": [
        "dataset_version",
        "image_format",         # PNG, JPEG
        "image_size",           # "64x64", "224x224"
        "num_classes",
        "class_names",
        "augmentation_applied", # True/False
    ],
    "metrics": [
        "total_images",
        "images_per_class",     # แต่ละ class
        "class_balance_ratio",
        "total_size_mb",
    ],
    "artifacts": [
        "samples/",             # ตัวอย่างรูปจากแต่ละ class
        "dataset_info.json",
        "class_distribution.png",
    ]
}
```

### 4.3 JSON Dataset Versioning

**Use Cases:** NLP data, API responses, Semi-structured data

```
┌─────────────────────────────────────────────────────────────┐
│                  JSON Dataset Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  // text_classification_v1.json                             │
│  [                                                          │
│    {                                                        │
│      "id": 1,                                               │
│      "text": "The team won the championship",               │
│      "label": "sports",                                     │
│      "metadata": {                                          │
│        "source": "synthetic",                               │
│        "confidence": 0.95                                   │
│      }                                                      │
│    },                                                       │
│    ...                                                      │
│  ]                                                          │
│                                                              │
│  // Changes in v2:                                          │
│  // - More samples (100 → 200)                              │
│  // - Added "timestamp" field                               │
│  // - Added new label categories                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Tracking Elements:**

```python
# สิ่งที่ควร Track สำหรับ JSON Dataset
tracking_elements = {
    "parameters": [
        "dataset_version",
        "task_type",           # classification, NER, etc.
        "num_classes",
        "text_field",          # field ที่เก็บ text
        "label_field",
    ],
    "metrics": [
        "total_samples",
        "avg_text_length",
        "max_text_length",
        "vocabulary_size",
        "label_distribution",
    ],
    "artifacts": [
        "dataset.json",
        "label_stats.json",
        "vocabulary.txt",
    ]
}
```

### 4.4 Parquet Dataset Versioning

**Use Cases:** Big data, Data warehousing, Columnar analytics

```
┌─────────────────────────────────────────────────────────────┐
│              Parquet vs CSV Comparison                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Feature              │    CSV    │   Parquet               │
│  ─────────────────────┼───────────┼────────────────         │
│  Storage Format       │    Row    │   Columnar              │
│  Compression          │    No     │   Built-in              │
│  Schema               │    No     │   Embedded              │
│  Read Speed           │   Slow    │   Fast                  │
│  Write Speed          │   Fast    │   Moderate              │
│  File Size            │   Large   │   Small                 │
│  Column Selection     │   Full    │   Selective             │
│  Data Types           │   Text    │   Native                │
│                                                              │
│  Best For:                                                  │
│  - CSV: Small data, interchange, human-readable             │
│  - Parquet: Large data, analytics, ML pipelines             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Tracking Elements:**

```python
# สิ่งที่ควร Track สำหรับ Parquet Dataset
tracking_elements = {
    "parameters": [
        "dataset_version",
        "compression",         # snappy, gzip, etc.
        "row_group_size",
        "partitioning",        # partition columns
    ],
    "metrics": [
        "num_records",
        "num_columns",
        "file_size_mb",
        "compression_ratio",
        "row_groups",
    ],
    "artifacts": [
        "dataset.parquet",
        "schema.json",
        "statistics.json",
    ]
}
```

---

## 5. Best Practices และ Design Patterns

### 5.1 Dataset Versioning Best Practices

```
┌─────────────────────────────────────────────────────────────┐
│              ✅ Best Practices Checklist                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. VERSION CONTROL                                         │
│     □ ใช้ Semantic Versioning (MAJOR.MINOR.PATCH)           │
│     □ บันทึก version ทุกครั้งที่ data เปลี่ยน               │
│     □ Document การเปลี่ยนแปลงใน changelog                   │
│                                                              │
│  2. DATA INTEGRITY                                          │
│     □ คำนวณและบันทึก file hash (MD5/SHA256)                │
│     □ Validate schema ก่อน log                              │
│     □ Check data quality metrics                            │
│                                                              │
│  3. METADATA                                                │
│     □ บันทึก creation date                                  │
│     □ บันทึก source/origin                                  │
│     □ บันทึก processing steps                               │
│     □ บันทึก owner/responsible person                       │
│                                                              │
│  4. ARTIFACTS                                               │
│     □ Log sample data สำหรับ quick preview                  │
│     □ Log schema information                                │
│     □ Log statistics summary                                │
│                                                              │
│  5. NAMING CONVENTION                                       │
│     □ ใช้ meaningful run names                              │
│     □ ใช้ consistent experiment naming                      │
│     □ ใช้ descriptive parameter names                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 File Integrity Verification

```python
import hashlib

def calculate_file_hash(filepath, algorithm='md5'):
    """
    คำนวณ Hash ของไฟล์สำหรับ integrity verification
    
    ใช้สำหรับ:
    1. ตรวจสอบว่าไฟล์ไม่ถูกแก้ไข
    2. ระบุ unique version ของ dataset
    3. Detect duplicate datasets
    """
    if algorithm == 'md5':
        hash_obj = hashlib.md5()
    elif algorithm == 'sha256':
        hash_obj = hashlib.sha256()
    
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

# ตัวอย่างการใช้งาน
file_hash = calculate_file_hash("data/customers.csv")
mlflow.log_param("file_hash_md5", file_hash)
```

### 5.3 Schema Management

```python
def log_schema_info(df, version):
    """
    บันทึก Schema Information ของ DataFrame
    """
    schema = {
        "version": version,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "nullable": {col: df[col].isnull().any() for col in df.columns},
        "unique_counts": {col: df[col].nunique() for col in df.columns},
    }
    return schema

# Schema Change Detection
def detect_schema_changes(schema_v1, schema_v2):
    """
    ตรวจจับการเปลี่ยนแปลง Schema ระหว่าง 2 versions
    """
    changes = {
        "added_columns": set(schema_v2["columns"]) - set(schema_v1["columns"]),
        "removed_columns": set(schema_v1["columns"]) - set(schema_v2["columns"]),
        "dtype_changes": {},
    }
    
    # Check dtype changes
    common_cols = set(schema_v1["columns"]) & set(schema_v2["columns"])
    for col in common_cols:
        if schema_v1["dtypes"][col] != schema_v2["dtypes"][col]:
            changes["dtype_changes"][col] = {
                "from": schema_v1["dtypes"][col],
                "to": schema_v2["dtypes"][col]
            }
    
    return changes
```

### 5.4 Dataset Comparison Pattern

```python
def compare_dataset_versions(run_id_v1, run_id_v2):
    """
    เปรียบเทียบ 2 versions ของ dataset
    """
    client = mlflow.tracking.MlflowClient()
    
    run_v1 = client.get_run(run_id_v1)
    run_v2 = client.get_run(run_id_v2)
    
    comparison = {
        "v1": {
            "version": run_v1.data.params.get("dataset_version"),
            "rows": run_v1.data.metrics.get("num_rows"),
            "columns": run_v1.data.metrics.get("num_columns"),
        },
        "v2": {
            "version": run_v2.data.params.get("dataset_version"),
            "rows": run_v2.data.metrics.get("num_rows"),
            "columns": run_v2.data.metrics.get("num_columns"),
        },
        "diff": {
            "rows_change": run_v2.data.metrics.get("num_rows", 0) - 
                          run_v1.data.metrics.get("num_rows", 0),
            "columns_change": run_v2.data.metrics.get("num_columns", 0) - 
                             run_v1.data.metrics.get("num_columns", 0),
        }
    }
    
    return comparison
```

---

## 6. แบบฝึกหัด

### แบบฝึกหัดที่ 1: Basic Dataset Versioning

**วัตถุประสงค์:** ฝึกการสร้างและ version CSV dataset

```python
# TODO: Complete the following tasks

# Task 1.1: สร้าง Customer Dataset Version 3
# - เพิ่ม column: "loyalty_points" (integer)
# - เพิ่ม column: "last_purchase_date" (datetime)
# - เพิ่มจำนวน samples เป็น 2000 rows

def create_customer_dataset_v3():
    """
    สร้าง Version 3 ของ customer dataset
    """
    # Your code here
    pass

# Task 1.2: Log ไปยัง MLflow พร้อม metadata ที่ครบถ้วน
def log_dataset_v3(df, filepath):
    """
    Log dataset v3 ไปยัง MLflow
    """
    # Your code here
    pass
```

### แบบฝึกหัดที่ 2: Image Dataset Augmentation Tracking

**วัตถุประสงค์:** ฝึกการ track augmented image dataset

```python
# TODO: Complete the following tasks

# Task 2.1: สร้าง Augmented Image Dataset
# - Apply rotation (90°, 180°, 270°)
# - Apply horizontal flip
# - Track augmentation parameters

def create_augmented_dataset(original_dir, output_dir):
    """
    สร้าง augmented version ของ image dataset
    """
    # Your code here
    pass

# Task 2.2: Log augmentation metadata
def log_augmented_dataset(dataset_dir, augmentation_params):
    """
    Log augmented dataset พร้อม augmentation parameters
    """
    # Your code here
    pass
```

### แบบฝึกหัดที่ 3: Dataset Lineage Tracking

**วัตถุประสงค์:** ฝึกการ track ความสัมพันธ์ระหว่าง raw และ processed data

```python
# TODO: Complete the following tasks

# Task 3.1: สร้าง Raw → Cleaned → Featured pipeline
def track_data_pipeline():
    """
    Track dataset transformations:
    1. Raw data → Log as "raw_v1"
    2. Cleaned data → Log as "cleaned_v1" with parent="raw_v1"
    3. Featured data → Log as "featured_v1" with parent="cleaned_v1"
    """
    # Your code here
    pass

# Task 3.2: Query lineage information
def get_dataset_lineage(run_id):
    """
    ดึงข้อมูล lineage ของ dataset จาก run_id
    """
    # Your code here
    pass
```

### แบบฝึกหัดที่ 4: Multi-format Dataset Comparison

**วัตถุประสงค์:** เปรียบเทียบ dataset format ต่างๆ

```python
# TODO: Complete the following tasks

# Task 4.1: สร้าง same dataset ใน 3 formats
# - CSV
# - Parquet  
# - JSON

# Task 4.2: Log แต่ละ format และเปรียบเทียบ
# - File size
# - Read time
# - Write time

def compare_dataset_formats(df):
    """
    เปรียบเทียบ performance ของ format ต่างๆ
    """
    # Your code here
    pass
```

---

## 📖 เอกสารอ้างอิง

1. [MLflow Documentation - Dataset Tracking](https://mlflow.org/docs/latest/tracking.html#datasets)
2. [MLflow Data Module API](https://mlflow.org/docs/latest/python_api/mlflow.data.html)
3. [Data Version Control Best Practices](https://dvc.org/doc)
4. [Apache Parquet Documentation](https://parquet.apache.org/docs/)

---

## 🎯 สรุป

หลังจากศึกษาเนื้อหานี้แล้ว นักศึกษาควรสามารถ:

1. ✅ อธิบายความสำคัญของ Dataset Versioning ใน ML Pipeline
2. ✅ ใช้ MLflow ในการ track และ version datasets ประเภทต่างๆ
3. ✅ ออกแบบ metadata schema สำหรับ dataset tracking
4. ✅ เปรียบเทียบ dataset versions และ track lineage
5. ✅ ประยุกต์ใช้ best practices ในโปรเจกต์จริง

---

**Happy Learning! 🚀**