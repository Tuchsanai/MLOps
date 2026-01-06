# %% [markdown]
# # LAB: Model Monitoring with Evidently AI
# ## Section 1: Foundation & Model Performance Monitoring
#
# **วัตถุประสงค์การเรียนรู้:**
# - เข้าใจหลักการ Model Monitoring และความสำคัญในการ deploy โมเดล
# - ใช้งาน Evidently AI สำหรับการติดตามคุณภาพข้อมูลและประสิทธิภาพโมเดล
# - ตรวจจับ Data Drift และ Target Drift
# - สร้าง Report และ Test Suite สำหรับ monitoring

# %% [markdown]
# ---
# # LAB 1.1: Introduction to Evidently AI
#
# ## วัตถุประสงค์
# - ติดตั้งและตั้งค่า Evidently
# - ทำความเข้าใจโครงสร้าง Report และ Test Suite
# - สร้าง Report แรกจาก dataset ตัวอย่าง

# %% [markdown]
# ### 1.1.1 ติดตั้ง Evidently AI
#
# Evidently เป็น open-source Python library สำหรับ ML model monitoring
# ช่วยตรวจสอบคุณภาพข้อมูล, ประสิทธิภาพโมเดล, และ data drift

# %%
# ติดตั้ง library ที่จำเป็น
# !pip install evidently scikit-learn pandas numpy

# %%
# Import libraries ที่จำเป็น
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_breast_cancer, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Evidently imports
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metric_preset import ClassificationPreset, RegressionPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset, DataQualityTestPreset
from evidently.tests import *

import warnings
warnings.filterwarnings('ignore')

print("✅ Import libraries สำเร็จ!")

# %% [markdown]
# ### 1.1.2 ทำความเข้าใจแนวคิด Model Monitoring
#
# **ทำไมต้องทำ Model Monitoring?**
#
# 1. **Data Drift**: ข้อมูล production เปลี่ยนแปลงไปจากข้อมูลที่ใช้ train
# 2. **Model Degradation**: ประสิทธิภาพโมเดลลดลงเมื่อเวลาผ่านไป
# 3. **Data Quality Issues**: ข้อมูลมีปัญหา missing values, outliers
# 4. **Concept Drift**: ความสัมพันธ์ระหว่าง features และ target เปลี่ยนไป

# %%
# โหลด dataset ตัวอย่าง - Breast Cancer Dataset
print("=" * 60)
print("📊 โหลด Breast Cancer Dataset")
print("=" * 60)

# โหลดข้อมูล
cancer = load_breast_cancer()
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df['target'] = cancer.target

print(f"\n📌 ขนาดข้อมูล: {df.shape}")
print(f"📌 จำนวน Features: {len(cancer.feature_names)}")
print(f"📌 Classes: {cancer.target_names}")
print(f"\n📌 การกระจายของ Target:")
print(df['target'].value_counts())

# %%
# แสดงตัวอย่างข้อมูล
print("\n📋 ตัวอย่างข้อมูล 5 แถวแรก:")
df.head()

# %% [markdown]
# ### 1.1.3 แบ่งข้อมูลเป็น Reference และ Current
#
# ใน Model Monitoring เราจะแบ่งข้อมูลเป็น:
# - **Reference Data**: ข้อมูลที่ใช้ train โมเดล (baseline)
# - **Current Data**: ข้อมูลใหม่ที่ต้องการตรวจสอบ (production data)

# %%
# แบ่งข้อมูลเป็น Reference และ Current
# สมมติ 70% แรกเป็น reference, 30% หลังเป็น current
split_index = int(len(df) * 0.7)

reference_data = df.iloc[:split_index].copy()
current_data = df.iloc[split_index:].copy()

print("=" * 60)
print("📊 การแบ่งข้อมูล Reference vs Current")
print("=" * 60)
print(f"\n📌 Reference Data: {reference_data.shape[0]} rows")
print(f"📌 Current Data: {current_data.shape[0]} rows")

# %% [markdown]
# ### 1.1.4 สร้าง Report แรกด้วย Evidently
#
# Evidently มี 2 components หลัก:
# 1. **Report**: สร้าง visualization และ metrics
# 2. **Test Suite**: ตรวจสอบเงื่อนไขและ pass/fail

# %%
# สร้าง Data Drift Report
print("=" * 60)
print("📊 สร้าง Data Drift Report")
print("=" * 60)

# กำหนด column mapping
column_mapping = ColumnMapping(
    target='target',
    numerical_features=cancer.feature_names.tolist()
)

# สร้าง Report ด้วย DataDriftPreset
data_drift_report = Report(metrics=[
    DataDriftPreset()
])

# รัน report
data_drift_report.run(
    reference_data=reference_data,
    current_data=current_data,
    column_mapping=column_mapping
)

print("✅ สร้าง Data Drift Report สำเร็จ!")

# %%
# แสดงผล Report ในรูปแบบ dictionary
drift_results = data_drift_report.as_dict()

print("\n📋 สรุปผล Data Drift:")
print("-" * 40)

# ดึงข้อมูล dataset drift
dataset_drift = drift_results['metrics'][0]['result']
print(f"📌 Dataset Drift Detected: {dataset_drift['dataset_drift']}")
print(f"📌 Number of Drifted Features: {dataset_drift['number_of_drifted_columns']}")
print(f"📌 Share of Drifted Features: {dataset_drift['share_of_drifted_columns']:.2%}")

# %%
# บันทึก Report เป็น HTML file
data_drift_report.save_html("report_data_drift.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_data_drift.html' สำเร็จ!")

# %% [markdown]
# ### 1.1.5 สร้าง Test Suite
#
# Test Suite ใช้สำหรับตรวจสอบเงื่อนไขอัตโนมัติ
# เหมาะสำหรับใช้ใน CI/CD pipeline

# %%
# สร้าง Test Suite สำหรับ Data Drift
print("=" * 60)
print("🧪 สร้าง Test Suite สำหรับ Data Drift")
print("=" * 60)

data_drift_test_suite = TestSuite(tests=[
    DataDriftTestPreset()
])

data_drift_test_suite.run(
    reference_data=reference_data,
    current_data=current_data,
    column_mapping=column_mapping
)

print("✅ รัน Test Suite สำเร็จ!")

# %%
# แสดงผล Test Suite
test_results = data_drift_test_suite.as_dict()

print("\n📋 สรุปผล Test Suite:")
print("-" * 40)

# นับจำนวน tests ที่ pass/fail
summary = test_results['summary']
print(f"📌 Total Tests: {summary['total_tests']}")
print(f"✅ Passed: {summary['success_tests']}")
print(f"❌ Failed: {summary['failed_tests']}")

# %%
# บันทึก Test Suite เป็น HTML
data_drift_test_suite.save_html("test_suite_data_drift.html")
print("\n💾 บันทึก Test Suite เป็นไฟล์ 'test_suite_data_drift.html' สำเร็จ!")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 1.1
#
# 1. ลองเปลี่ยน dataset เป็น Iris dataset และสร้าง Data Drift Report
# 2. ลองปรับ split ratio เป็น 80:20 และสังเกตผลลัพธ์
# 3. สำรวจ metrics อื่นๆ ใน drift_results

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 1.2: Data Quality Monitoring
#
# ## วัตถุประสงค์
# - ตรวจสอบ missing values, duplicates
# - วิเคราะห์ data integrity และ consistency
# - สร้าง Data Quality Report และตั้ง threshold alerts

# %% [markdown]
# ### 1.2.1 ทำความเข้าใจ Data Quality
#
# **Data Quality Dimensions:**
# - **Completeness**: ข้อมูลครบถ้วน (ไม่มี missing values)
# - **Uniqueness**: ไม่มีข้อมูลซ้ำ (duplicates)
# - **Validity**: ข้อมูลอยู่ในช่วงที่ถูกต้อง
# - **Consistency**: ข้อมูลสอดคล้องกัน

# %%
# สร้าง dataset ที่มีปัญหา Data Quality
print("=" * 60)
print("📊 สร้าง Dataset ที่มีปัญหา Data Quality")
print("=" * 60)

# ใช้ข้อมูล reference เดิม
df_quality = reference_data.copy()

# เพิ่ม missing values
np.random.seed(42)
missing_indices = np.random.choice(df_quality.index, size=20, replace=False)
df_quality.loc[missing_indices, 'mean radius'] = np.nan

# เพิ่ม duplicate rows
duplicates = df_quality.sample(10, random_state=42)
df_quality = pd.concat([df_quality, duplicates], ignore_index=True)

# เพิ่ม outliers
outlier_indices = np.random.choice(df_quality.index, size=5, replace=False)
df_quality.loc[outlier_indices, 'mean area'] = df_quality['mean area'].max() * 10

print(f"📌 ขนาดข้อมูลหลังเพิ่มปัญหา: {df_quality.shape}")
print(f"📌 Missing values in 'mean radius': {df_quality['mean radius'].isna().sum()}")
print(f"📌 Duplicate rows: {df_quality.duplicated().sum()}")

# %%
# สร้าง Data Quality Report
print("\n" + "=" * 60)
print("📊 สร้าง Data Quality Report")
print("=" * 60)

# อัพเดท column mapping
quality_column_mapping = ColumnMapping(
    target='target',
    numerical_features=[col for col in df_quality.columns if col != 'target']
)

# สร้าง Report
data_quality_report = Report(metrics=[
    DataQualityPreset()
])

data_quality_report.run(
    current_data=df_quality,
    reference_data=reference_data,
    column_mapping=quality_column_mapping
)

print("✅ สร้าง Data Quality Report สำเร็จ!")

# %%
# วิเคราะห์ผลลัพธ์ Data Quality
quality_results = data_quality_report.as_dict()

print("\n📋 สรุปผล Data Quality:")
print("-" * 40)

# แสดงข้อมูลเบื้องต้น
for metric in quality_results['metrics']:
    metric_id = metric['metric']
    if 'DatasetSummaryMetric' in metric_id:
        result = metric['result']['current']
        print(f"📌 จำนวนแถว: {result['number_of_rows']}")
        print(f"📌 จำนวน columns: {result['number_of_columns']}")
        print(f"📌 Missing values: {result['number_of_missing_values']}")
        print(f"📌 Duplicate rows: {result['number_of_duplicated_rows']}")

# %%
# บันทึก Report
data_quality_report.save_html("report_data_quality.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_data_quality.html' สำเร็จ!")

# %% [markdown]
# ### 1.2.2 ตรวจสอบ Missing Values แบบละเอียด

# %%
# สร้าง Report เฉพาะ Missing Values
print("=" * 60)
print("📊 วิเคราะห์ Missing Values")
print("=" * 60)

missing_report = Report(metrics=[
    DatasetMissingValuesMetric()
])

missing_report.run(
    current_data=df_quality,
    reference_data=reference_data,
    column_mapping=quality_column_mapping
)

missing_results = missing_report.as_dict()

print("\n📋 สรุป Missing Values:")
print("-" * 40)

missing_data = missing_results['metrics'][0]['result']['current']
print(f"📌 Total Missing Values: {missing_data['number_of_missing_values']}")
print(f"📌 Share of Missing Values: {missing_data['share_of_missing_values']:.2%}")
print(f"📌 Columns with Missing: {missing_data['number_of_columns_with_missing_values']}")

# %% [markdown]
# ### 1.2.3 ตรวจสอบ Duplicates

# %%
# สร้าง Report เฉพาะ Duplicates
print("=" * 60)
print("📊 วิเคราะห์ Duplicate Rows")
print("=" * 60)

duplicates_report = Report(metrics=[
    DatasetDuplicatedRowsMetric()
])

duplicates_report.run(
    current_data=df_quality,
    reference_data=reference_data,
    column_mapping=quality_column_mapping
)

dup_results = duplicates_report.as_dict()

print("\n📋 สรุป Duplicates:")
print("-" * 40)

dup_data = dup_results['metrics'][0]['result']['current']
print(f"📌 Duplicate Rows: {dup_data['number_of_duplicated_rows']}")
print(f"📌 Share of Duplicates: {dup_data['share_of_duplicated_rows']:.2%}")

# %% [markdown]
# ### 1.2.4 สร้าง Test Suite สำหรับ Data Quality

# %%
# สร้าง Test Suite พร้อม threshold
print("=" * 60)
print("🧪 สร้าง Test Suite สำหรับ Data Quality")
print("=" * 60)

data_quality_test = TestSuite(tests=[
    # ตรวจสอบ missing values ไม่เกิน 5%
    TestShareOfMissingValues(lte=0.05),

    # ตรวจสอบ duplicate rows ไม่เกิน 2%
    TestNumberOfDuplicatedRows(lte=10),

    # ตรวจสอบ columns ที่มี missing values
    TestNumberOfColumnsWithMissingValues(lte=2),

    # ตรวจสอบจำนวนแถว
    TestNumberOfRows(gte=100),
])

data_quality_test.run(
    current_data=df_quality,
    reference_data=reference_data,
    column_mapping=quality_column_mapping
)

print("✅ รัน Test Suite สำเร็จ!")

# %%
# แสดงผล Test Suite
quality_test_results = data_quality_test.as_dict()

print("\n📋 ผลการทดสอบ Data Quality:")
print("-" * 40)

for test in quality_test_results['tests']:
    test_name = test['name']
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    print(f"{status}: {test_name}")

# %%
# บันทึก Test Suite
data_quality_test.save_html("test_suite_data_quality.html")
print("\n💾 บันทึก Test Suite เป็นไฟล์ 'test_suite_data_quality.html' สำเร็จ!")

# %% [markdown]
# ### 1.2.5 สร้าง Custom Data Quality Checks

# %%
# สร้าง Test Suite แบบ Custom
print("=" * 60)
print("🧪 Custom Data Quality Tests")
print("=" * 60)

custom_quality_test = TestSuite(tests=[
    # ตรวจสอบค่าใน column เฉพาะ
    TestColumnShareOfMissingValues(column_name='mean radius', lte=0.1),

    # ตรวจสอบค่า mean อยู่ในช่วง
    TestColumnMean(column_name='mean area', gt=0),

    # ตรวจสอบค่า min/max
    TestColumnMin(column_name='mean radius', gt=0),
])

custom_quality_test.run(
    current_data=df_quality,
    reference_data=reference_data,
    column_mapping=quality_column_mapping
)

# แสดงผล
custom_results = custom_quality_test.as_dict()
print("\n📋 ผลการทดสอบ Custom:")
print("-" * 40)

for test in custom_results['tests']:
    test_name = test['name']
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    print(f"{status}: {test_name}")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 1.2
#
# 1. สร้าง Test Suite ที่ตรวจสอบว่า missing values ในแต่ละ column ไม่เกิน 3%
# 2. เพิ่ม outliers ให้กับ column อื่นๆ และใช้ Evidently ตรวจจับ
# 3. สร้าง alert เมื่อพบ duplicate rows เกิน 5%

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 1.3: Model Performance Tracking
#
# ## วัตถุประสงค์
# - ติดตาม classification metrics (Accuracy, Precision, Recall, F1)
# - ติดตาม regression metrics (MAE, RMSE, R²)
# - เปรียบเทียบ performance ระหว่าง reference vs current data

# %% [markdown]
# ### 1.3.1 เตรียมโมเดล Classification

# %%
# เตรียมข้อมูลสำหรับ Classification
print("=" * 60)
print("📊 เตรียมโมเดล Classification")
print("=" * 60)

# โหลด Breast Cancer Dataset
cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = pd.Series(cancer.target, name='target')

# แบ่งข้อมูล train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"📌 Training set: {X_train.shape[0]} samples")
print(f"📌 Test set: {X_test.shape[0]} samples")

# %%
# Train โมเดล
print("\n" + "=" * 60)
print("🤖 Training Random Forest Classifier")
print("=" * 60)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict
y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)

# คำนวณ probability
y_train_proba = clf.predict_proba(X_train)[:, 1]
y_test_proba = clf.predict_proba(X_test)[:, 1]

print("✅ Training สำเร็จ!")

# %%
# คำนวณ metrics แบบ manual
print("\n📋 Performance Metrics (Manual Calculation):")
print("-" * 40)
print(f"📌 Training Accuracy: {accuracy_score(y_train, y_train_pred):.4f}")
print(f"📌 Test Accuracy: {accuracy_score(y_test, y_test_pred):.4f}")
print(f"📌 Test Precision: {precision_score(y_test, y_test_pred):.4f}")
print(f"📌 Test Recall: {recall_score(y_test, y_test_pred):.4f}")
print(f"📌 Test F1-Score: {f1_score(y_test, y_test_pred):.4f}")

# %% [markdown]
# ### 1.3.2 สร้าง Classification Performance Report

# %%
# เตรียมข้อมูลสำหรับ Evidently
print("=" * 60)
print("📊 สร้าง Classification Performance Report")
print("=" * 60)

# สร้าง DataFrame สำหรับ reference (training)
reference_clf = X_train.copy()
reference_clf['target'] = y_train.values
reference_clf['prediction'] = y_train_pred

# สร้าง DataFrame สำหรับ current (test)
current_clf = X_test.copy()
current_clf['target'] = y_test.values
current_clf['prediction'] = y_test_pred

print(f"📌 Reference data shape: {reference_clf.shape}")
print(f"📌 Current data shape: {current_clf.shape}")

# %%
# กำหนด Column Mapping
clf_column_mapping = ColumnMapping(
    target='target',
    prediction='prediction',
    numerical_features=cancer.feature_names.tolist()
)

# สร้าง Classification Report
clf_report = Report(metrics=[
    ClassificationPreset()
])

clf_report.run(
    reference_data=reference_clf,
    current_data=current_clf,
    column_mapping=clf_column_mapping
)

print("✅ สร้าง Classification Report สำเร็จ!")

# %%
# วิเคราะห์ผลลัพธ์
clf_results = clf_report.as_dict()

print("\n📋 Classification Metrics จาก Evidently:")
print("-" * 40)

for metric in clf_results['metrics']:
    metric_id = metric['metric']
    if 'ClassificationQualityMetric' in metric_id:
        current = metric['result']['current']
        reference = metric['result']['reference']

        print("\n🔹 Current Data (Test Set):")
        print(f"   Accuracy: {current['accuracy']:.4f}")
        print(f"   Precision: {current['precision']:.4f}")
        print(f"   Recall: {current['recall']:.4f}")
        print(f"   F1: {current['f1']:.4f}")

        print("\n🔹 Reference Data (Training Set):")
        print(f"   Accuracy: {reference['accuracy']:.4f}")
        print(f"   Precision: {reference['precision']:.4f}")
        print(f"   Recall: {reference['recall']:.4f}")
        print(f"   F1: {reference['f1']:.4f}")

# %%
# บันทึก Report
clf_report.save_html("report_classification_performance.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_classification_performance.html' สำเร็จ!")

# %% [markdown]
# ### 1.3.3 เตรียมโมเดล Regression

# %%
# โหลด California Housing Dataset
print("=" * 60)
print("📊 เตรียมโมเดล Regression")
print("=" * 60)

housing = fetch_california_housing()
X_reg = pd.DataFrame(housing.data, columns=housing.feature_names)
y_reg = pd.Series(housing.target, name='target')

# แบ่งข้อมูล
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.3, random_state=42
)

print(f"📌 Training set: {X_train_reg.shape[0]} samples")
print(f"📌 Test set: {X_test_reg.shape[0]} samples")

# %%
# Train โมเดล Regression
print("\n" + "=" * 60)
print("🤖 Training Random Forest Regressor")
print("=" * 60)

reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
reg.fit(X_train_reg, y_train_reg)

# Predict
y_train_reg_pred = reg.predict(X_train_reg)
y_test_reg_pred = reg.predict(X_test_reg)

print("✅ Training สำเร็จ!")

# %%
# คำนวณ Regression metrics แบบ manual
print("\n📋 Regression Metrics (Manual Calculation):")
print("-" * 40)
print(f"📌 Training MAE: {mean_absolute_error(y_train_reg, y_train_reg_pred):.4f}")
print(f"📌 Test MAE: {mean_absolute_error(y_test_reg, y_test_reg_pred):.4f}")
print(f"📌 Test RMSE: {np.sqrt(mean_squared_error(y_test_reg, y_test_reg_pred)):.4f}")
print(f"📌 Test R²: {r2_score(y_test_reg, y_test_reg_pred):.4f}")

# %% [markdown]
# ### 1.3.4 สร้าง Regression Performance Report

# %%
# เตรียมข้อมูลสำหรับ Evidently
print("=" * 60)
print("📊 สร้าง Regression Performance Report")
print("=" * 60)

# สร้าง DataFrame
reference_reg = X_train_reg.copy()
reference_reg['target'] = y_train_reg.values
reference_reg['prediction'] = y_train_reg_pred

current_reg = X_test_reg.copy()
current_reg['target'] = y_test_reg.values
current_reg['prediction'] = y_test_reg_pred

# Column Mapping
reg_column_mapping = ColumnMapping(
    target='target',
    prediction='prediction',
    numerical_features=housing.feature_names.tolist()
)

# สร้าง Regression Report
reg_report = Report(metrics=[
    RegressionPreset()
])

reg_report.run(
    reference_data=reference_reg,
    current_data=current_reg,
    column_mapping=reg_column_mapping
)

print("✅ สร้าง Regression Report สำเร็จ!")

# %%
# วิเคราะห์ผลลัพธ์
reg_results = reg_report.as_dict()

print("\n📋 Regression Metrics จาก Evidently:")
print("-" * 40)

for metric in reg_results['metrics']:
    metric_id = metric['metric']
    if 'RegressionQualityMetric' in metric_id:
        current = metric['result']['current']
        reference = metric['result']['reference']

        print("\n🔹 Current Data (Test Set):")
        print(f"   MAE: {current['mean_abs_error']:.4f}")
        print(f"   RMSE: {np.sqrt(current['mean_error']**2 + current['error_std']**2):.4f}")
        print(f"   R²: {current['r2_score']:.4f}")

        print("\n🔹 Reference Data (Training Set):")
        print(f"   MAE: {reference['mean_abs_error']:.4f}")
        print(f"   R²: {reference['r2_score']:.4f}")

# %%
# บันทึก Report
reg_report.save_html("report_regression_performance.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_regression_performance.html' สำเร็จ!")

# %% [markdown]
# ### 1.3.5 สร้าง Test Suite สำหรับ Model Performance

# %%
# Classification Performance Tests
print("=" * 60)
print("🧪 Classification Performance Tests")
print("=" * 60)

clf_perf_test = TestSuite(tests=[
    # ตรวจสอบ Accuracy ไม่ต่ำกว่า 90%
    TestAccuracyScore(gte=0.90),

    # ตรวจสอบ Precision ไม่ต่ำกว่า 85%
    TestPrecisionScore(gte=0.85),

    # ตรวจสอบ Recall ไม่ต่ำกว่า 85%
    TestRecallScore(gte=0.85),

    # ตรวจสอบ F1 ไม่ต่ำกว่า 85%
    TestF1Score(gte=0.85),
])

clf_perf_test.run(
    reference_data=reference_clf,
    current_data=current_clf,
    column_mapping=clf_column_mapping
)

# แสดงผล
clf_test_results = clf_perf_test.as_dict()
print("\n📋 ผลการทดสอบ Classification Performance:")
print("-" * 40)

for test in clf_test_results['tests']:
    test_name = test['name']
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    print(f"{status}: {test_name}")

# %%
# Regression Performance Tests
print("\n" + "=" * 60)
print("🧪 Regression Performance Tests")
print("=" * 60)

reg_perf_test = TestSuite(tests=[
    # ตรวจสอบ MAE ไม่เกิน 0.5
    TestValueMAE(lte=0.5),

    # ตรวจสอบ RMSE ไม่เกิน 0.7
    TestValueRMSE(lte=0.7),

    # ตรวจสอบ R² ไม่ต่ำกว่า 0.7
    TestValueR2Score(gte=0.7),
])

reg_perf_test.run(
    reference_data=reference_reg,
    current_data=current_reg,
    column_mapping=reg_column_mapping
)

# แสดงผล
reg_test_results = reg_perf_test.as_dict()
print("\n📋 ผลการทดสอบ Regression Performance:")
print("-" * 40)

for test in reg_test_results['tests']:
    test_name = test['name']
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    print(f"{status}: {test_name}")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 1.3
#
# 1. ลองเปลี่ยนโมเดลเป็น LogisticRegression และเปรียบเทียบ metrics
# 2. สร้าง Test Suite ที่ตรวจสอบว่า performance ของ current ไม่ต่ำกว่า reference เกิน 5%
# 3. ทดลอง train โมเดลด้วย hyperparameters ที่แตกต่างกันและเปรียบเทียบผล

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 1.4: Target Drift Detection
#
# ## วัตถุประสงค์
# - ตรวจจับการเปลี่ยนแปลงของ target distribution
# - วิเคราะห์ prediction drift
# - สร้าง alerts เมื่อ target drift เกินค่าที่กำหนด

# %% [markdown]
# ### 1.4.1 ทำความเข้าใจ Target Drift
#
# **Target Drift** เกิดขึ้นเมื่อ:
# - การกระจายของ target variable เปลี่ยนแปลง
# - Prediction ของโมเดลเปลี่ยนแปลงไปจาก reference
#
# **สาเหตุที่พบบ่อย:**
# - ฤดูกาล (seasonality)
# - เปลี่ยนแปลงพฤติกรรมผู้ใช้
# - External factors (เศรษฐกิจ, การแข่งขัน)

# %%
# สร้างข้อมูลที่มี Target Drift
print("=" * 60)
print("📊 สร้างข้อมูลที่มี Target Drift")
print("=" * 60)

# ใช้ข้อมูล Classification จากก่อนหน้า
# สร้าง current data ที่มี target distribution เปลี่ยนไป

# Reference: สัดส่วน target ปกติ
reference_target_drift = reference_clf.copy()

# Current: เปลี่ยนสัดส่วน target (เพิ่ม class 1)
current_target_drift = current_clf.copy()

# เปลี่ยน target บางส่วนจาก 0 เป็น 1 เพื่อจำลอง drift
np.random.seed(42)
change_indices = current_target_drift[current_target_drift['target'] == 0].sample(
    frac=0.3, random_state=42
).index
current_target_drift.loc[change_indices, 'target'] = 1

print("\n📋 การกระจายของ Target:")
print("-" * 40)
print("\n🔹 Reference Data:")
print(reference_target_drift['target'].value_counts(normalize=True))
print("\n🔹 Current Data (with drift):")
print(current_target_drift['target'].value_counts(normalize=True))

# %% [markdown]
# ### 1.4.2 ตรวจจับ Target Drift

# %%
# สร้าง Target Drift Report
print("=" * 60)
print("📊 สร้าง Target Drift Report")
print("=" * 60)

target_drift_report = Report(metrics=[
    TargetDriftMetric()
])

target_drift_report.run(
    reference_data=reference_target_drift,
    current_data=current_target_drift,
    column_mapping=clf_column_mapping
)

print("✅ สร้าง Target Drift Report สำเร็จ!")

# %%
# วิเคราะห์ผลลัพธ์
target_drift_results = target_drift_report.as_dict()

print("\n📋 ผลการตรวจจับ Target Drift:")
print("-" * 40)

for metric in target_drift_results['metrics']:
    if 'TargetDriftMetric' in metric['metric']:
        result = metric['result']
        print(f"📌 Drift Detected: {result['drift_detected']}")
        print(f"📌 Drift Score (p-value): {result['drift_score']:.6f}")
        print(f"📌 Statistical Test: {result['stattest_name']}")

# %%
# บันทึก Report
target_drift_report.save_html("report_target_drift.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_target_drift.html' สำเร็จ!")

# %% [markdown]
# ### 1.4.3 ตรวจจับ Prediction Drift

# %%
# สร้าง Prediction Drift
print("=" * 60)
print("📊 สร้าง Prediction Drift Report")
print("=" * 60)

# สร้าง prediction ใหม่สำหรับ current data ที่มี drift
# (ในกรณีจริง prediction อาจเปลี่ยนเมื่อ input data เปลี่ยน)

# จำลองการเปลี่ยนแปลงของ prediction
current_pred_drift = current_target_drift.copy()
np.random.seed(42)
flip_indices = np.random.choice(
    current_pred_drift.index,
    size=int(len(current_pred_drift) * 0.2),
    replace=False
)
current_pred_drift.loc[flip_indices, 'prediction'] = 1 - current_pred_drift.loc[flip_indices, 'prediction']

print(f"📌 จำนวน predictions ที่เปลี่ยน: {len(flip_indices)}")

# %%
# สร้าง Report สำหรับ Prediction Drift
prediction_drift_report = Report(metrics=[
    ColumnDriftMetric(column_name='prediction')
])

prediction_drift_report.run(
    reference_data=reference_target_drift,
    current_data=current_pred_drift,
    column_mapping=clf_column_mapping
)

# วิเคราะห์ผล
pred_drift_results = prediction_drift_report.as_dict()

print("\n📋 ผลการตรวจจับ Prediction Drift:")
print("-" * 40)

for metric in pred_drift_results['metrics']:
    if 'ColumnDriftMetric' in metric['metric']:
        result = metric['result']
        print(f"📌 Column: {result['column_name']}")
        print(f"📌 Drift Detected: {result['drift_detected']}")
        print(f"📌 Drift Score: {result['drift_score']:.6f}")

# %% [markdown]
# ### 1.4.4 สร้าง Test Suite สำหรับ Target Drift

# %%
# Test Suite สำหรับ Target Drift
print("=" * 60)
print("🧪 Target Drift Test Suite")
print("=" * 60)

target_drift_test = TestSuite(tests=[
    # ตรวจสอบว่าไม่มี target drift
    TestColumnDrift(column_name='target'),

    # ตรวจสอบว่าไม่มี prediction drift
    TestColumnDrift(column_name='prediction'),
])

target_drift_test.run(
    reference_data=reference_target_drift,
    current_data=current_pred_drift,
    column_mapping=clf_column_mapping
)

# แสดงผล
target_test_results = target_drift_test.as_dict()
print("\n📋 ผลการทดสอบ Target Drift:")
print("-" * 40)

for test in target_test_results['tests']:
    test_name = test['name']
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    desc = test.get('description', '')
    print(f"{status}: {test_name}")

# %%
# บันทึก Test Suite
target_drift_test.save_html("test_suite_target_drift.html")
print("\n💾 บันทึก Test Suite เป็นไฟล์ 'test_suite_target_drift.html' สำเร็จ!")

# %% [markdown]
# ### 1.4.5 สร้าง Comprehensive Drift Report

# %%
# รวมทุก metrics ใน Report เดียว
print("=" * 60)
print("📊 สร้าง Comprehensive Drift Report")
print("=" * 60)

comprehensive_report = Report(metrics=[
    DataDriftPreset(),
    TargetDriftMetric(),
    ColumnDriftMetric(column_name='prediction'),
])

comprehensive_report.run(
    reference_data=reference_target_drift,
    current_data=current_pred_drift,
    column_mapping=clf_column_mapping
)

print("✅ สร้าง Comprehensive Report สำเร็จ!")

# %%
# บันทึก Report
comprehensive_report.save_html("report_comprehensive_drift.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_comprehensive_drift.html' สำเร็จ!")

# %% [markdown]
# ### 1.4.6 สร้าง Alert System

# %%
# สร้างฟังก์ชันสำหรับ Alert
def check_drift_alerts(reference_data, current_data, column_mapping, thresholds=None):
    """
    ตรวจสอบ drift และส่ง alerts

    Parameters:
    - reference_data: DataFrame ข้อมูล reference
    - current_data: DataFrame ข้อมูล current
    - column_mapping: ColumnMapping object
    - thresholds: dict กำหนด threshold สำหรับ alerts

    Returns:
    - dict: ผลการตรวจสอบและ alerts
    """
    if thresholds is None:
        thresholds = {
            'drift_share': 0.3,  # แจ้งเตือนถ้า drift features เกิน 30%
            'target_drift_pvalue': 0.05,  # แจ้งเตือนถ้า p-value < 0.05
        }

    alerts = []

    # ตรวจสอบ Data Drift
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_data, current_data=current_data,
                     column_mapping=column_mapping)
    drift_results = drift_report.as_dict()

    dataset_drift = drift_results['metrics'][0]['result']
    drift_share = dataset_drift['share_of_drifted_columns']

    if drift_share > thresholds['drift_share']:
        alerts.append({
            'type': 'DATA_DRIFT',
            'severity': 'HIGH',
            'message': f"⚠️ Data drift detected! {drift_share:.1%} of features have drifted (threshold: {thresholds['drift_share']:.1%})"
        })

    # ตรวจสอบ Target Drift
    target_report = Report(metrics=[TargetDriftMetric()])
    target_report.run(reference_data=reference_data, current_data=current_data,
                      column_mapping=column_mapping)
    target_results = target_report.as_dict()

    target_drift = target_results['metrics'][0]['result']

    if target_drift['drift_detected']:
        alerts.append({
            'type': 'TARGET_DRIFT',
            'severity': 'CRITICAL',
            'message': f"🚨 Target drift detected! p-value: {target_drift['drift_score']:.6f}"
        })

    return {
        'data_drift_share': drift_share,
        'target_drift_detected': target_drift['drift_detected'],
        'target_drift_pvalue': target_drift['drift_score'],
        'alerts': alerts
    }

# %%
# ทดสอบ Alert System
print("=" * 60)
print("🔔 Alert System")
print("=" * 60)

alert_results = check_drift_alerts(
    reference_data=reference_target_drift,
    current_data=current_pred_drift,
    column_mapping=clf_column_mapping
)

print("\n📋 สรุปผลการตรวจสอบ:")
print("-" * 40)
print(f"📌 Data Drift Share: {alert_results['data_drift_share']:.1%}")
print(f"📌 Target Drift Detected: {alert_results['target_drift_detected']}")
print(f"📌 Target Drift p-value: {alert_results['target_drift_pvalue']:.6f}")

print("\n📋 Alerts:")
print("-" * 40)
if alert_results['alerts']:
    for alert in alert_results['alerts']:
        print(f"[{alert['severity']}] {alert['type']}: {alert['message']}")
else:
    print("✅ ไม่มี alerts")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 1.4
#
# 1. ทดลองสร้าง drift ด้วยการเปลี่ยน target distribution ในระดับต่างๆ (10%, 20%, 50%)
# 2. สร้าง Alert System ที่ส่ง notification เมื่อตรวจพบ drift
# 3. ทดลองใช้ statistical test อื่นๆ ใน Evidently (chi-square, KS test, etc.)

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # สรุป Section 1
#
# ## สิ่งที่ได้เรียนรู้
#
# ### LAB 1.1: Introduction to Evidently AI
# - ติดตั้งและใช้งาน Evidently เบื้องต้น
# - เข้าใจ Report และ Test Suite
# - สร้าง Data Drift Report
#
# ### LAB 1.2: Data Quality Monitoring
# - ตรวจสอบ missing values และ duplicates
# - สร้าง Data Quality Report
# - ตั้งค่า threshold alerts
#
# ### LAB 1.3: Model Performance Tracking
# - ติดตาม Classification metrics (Accuracy, Precision, Recall, F1)
# - ติดตาม Regression metrics (MAE, RMSE, R²)
# - เปรียบเทียบ performance ระหว่าง reference vs current
#
# ### LAB 1.4: Target Drift Detection
# - ตรวจจับ Target Drift
# - ตรวจจับ Prediction Drift
# - สร้าง Alert System

# %% [markdown]
# ## Best Practices สำหรับ Model Monitoring
#
# 1. **กำหนด Baseline ที่ชัดเจน**: เก็บ reference data ที่มีคุณภาพ
# 2. **Monitor สม่ำเสมอ**: ตั้ง schedule สำหรับการตรวจสอบ
# 3. **ตั้ง Threshold ที่เหมาะสม**: ปรับตามบริบทของ business
# 4. **สร้าง Alert System**: แจ้งเตือนทันทีเมื่อพบปัญหา
# 5. **เก็บ Log และ History**: เพื่อวิเคราะห์ trend

# %%
# สรุป files ที่สร้าง
print("=" * 60)
print("📁 Files ที่สร้างจาก Lab นี้")
print("=" * 60)
print("""
1. report_data_drift.html - Data Drift Report
2. test_suite_data_drift.html - Data Drift Test Suite
3. report_data_quality.html - Data Quality Report
4. test_suite_data_quality.html - Data Quality Test Suite
5. report_classification_performance.html - Classification Performance Report
6. report_regression_performance.html - Regression Performance Report
7. report_target_drift.html - Target Drift Report
8. test_suite_target_drift.html - Target Drift Test Suite
9. report_comprehensive_drift.html - Comprehensive Drift Report
""")
print("✅ Lab Section 1 เสร็จสมบูรณ์!")

# %% [markdown]
# ---
# ---
# # Section 2: Feature Drift & Data Drift
#
# **วัตถุประสงค์การเรียนรู้:**
# - เข้าใจความแตกต่างระหว่าง Data Drift และ Feature Drift
# - ใช้ Statistical Tests ต่างๆ ในการตรวจจับ Drift
# - วิเคราะห์ Drift ในระดับ Feature แต่ละตัว
# - สร้างกลยุทธ์ในการจัดการกับ Drift

# %% [markdown]
# ---
# # LAB 2.1: Understanding Data Drift
#
# ## วัตถุประสงค์
# - เข้าใจแนวคิดและประเภทของ Data Drift
# - สร้างข้อมูลจำลองที่มี Drift แบบต่างๆ
# - ตรวจจับ Dataset-level Drift

# %% [markdown]
# ### 2.1.1 ประเภทของ Data Drift
#
# **Data Drift** คือการเปลี่ยนแปลงของ distribution ข้อมูล ซึ่งแบ่งเป็น:
#
# 1. **Covariate Shift**: Input features เปลี่ยนแปลง แต่ความสัมพันธ์กับ target คงที่
# 2. **Prior Probability Shift**: Target distribution เปลี่ยนแปลง
# 3. **Concept Drift**: ความสัมพันธ์ระหว่าง features และ target เปลี่ยนไป
#
# **สาเหตุของ Data Drift:**
# - การเปลี่ยนแปลงตามฤดูกาล (Seasonality)
# - การเปลี่ยนแปลงพฤติกรรมผู้ใช้
# - การเปลี่ยนแปลงของ data collection process
# - External events (เศรษฐกิจ, สังคม, การแข่งขัน)

# %%
# Import libraries สำหรับ Section 2
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer, make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset
from evidently.tests import *

import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("📚 Section 2: Feature Drift & Data Drift")
print("=" * 60)

# %%
# โหลดข้อมูลพื้นฐาน
print("\n📊 โหลด Breast Cancer Dataset")
print("-" * 40)

cancer = load_breast_cancer()
df_base = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df_base['target'] = cancer.target

# เลือกเฉพาะ features หลักๆ เพื่อให้ง่ายต่อการศึกษา
selected_features = [
    'mean radius', 'mean texture', 'mean perimeter', 'mean area',
    'mean smoothness', 'mean compactness', 'mean concavity',
    'mean symmetry', 'mean fractal dimension'
]

df_selected = df_base[selected_features + ['target']].copy()

print(f"📌 ขนาดข้อมูล: {df_selected.shape}")
print(f"📌 Features ที่เลือก: {len(selected_features)} features")

# %% [markdown]
# ### 2.1.2 สร้างข้อมูลที่มี Drift แบบต่างๆ

# %%
# แบ่งข้อมูลเป็น Reference
reference_data = df_selected.iloc[:400].copy()

print("=" * 60)
print("📊 สร้างข้อมูลที่มี Drift แบบต่างๆ")
print("=" * 60)

# %%
# 1. Gradual Drift - การเปลี่ยนแปลงแบบค่อยเป็นค่อยไป
print("\n🔹 1. Gradual Drift")
print("-" * 40)

gradual_drift_data = df_selected.iloc[400:].copy()

# เพิ่มค่าทีละน้อยให้กับ features
np.random.seed(42)
drift_factor = 0.1  # 10% shift

for col in selected_features[:5]:  # drift 5 features แรก
    original_std = gradual_drift_data[col].std()
    gradual_drift_data[col] = gradual_drift_data[col] + (drift_factor * original_std)

print(f"📌 สร้าง Gradual Drift ใน 5 features")
print(f"📌 Drift factor: {drift_factor:.0%}")

# %%
# 2. Sudden Drift - การเปลี่ยนแปลงแบบกะทันหัน
print("\n🔹 2. Sudden Drift")
print("-" * 40)

sudden_drift_data = df_selected.iloc[400:].copy()

# เปลี่ยนค่าแบบกะทันหัน
for col in ['mean radius', 'mean area']:
    sudden_drift_data[col] = sudden_drift_data[col] * 1.5  # เพิ่ม 50%

print(f"📌 สร้าง Sudden Drift ใน 'mean radius' และ 'mean area'")
print(f"📌 เพิ่มค่า 50%")

# %%
# 3. Seasonal Drift - การเปลี่ยนแปลงตามฤดูกาล
print("\n🔹 3. Seasonal Drift (Simulated)")
print("-" * 40)

seasonal_drift_data = df_selected.iloc[400:].copy()

# จำลอง seasonal pattern ด้วย sine wave
n_samples = len(seasonal_drift_data)
seasonal_factor = np.sin(np.linspace(0, 2*np.pi, n_samples))

for col in ['mean texture', 'mean smoothness']:
    original_std = seasonal_drift_data[col].std()
    seasonal_drift_data[col] = seasonal_drift_data[col] + (seasonal_factor * original_std * 0.3)

print(f"📌 สร้าง Seasonal Drift ใน 'mean texture' และ 'mean smoothness'")

# %%
# 4. Incremental Drift - การเปลี่ยนแปลงแบบสะสม
print("\n🔹 4. Incremental Drift")
print("-" * 40)

incremental_drift_data = df_selected.iloc[400:].copy()

# สร้าง incremental drift - ค่าเพิ่มขึ้นเรื่อยๆ ตามลำดับ
n_samples = len(incremental_drift_data)
increment = np.linspace(0, 1, n_samples)

for col in ['mean compactness', 'mean concavity']:
    original_std = incremental_drift_data[col].std()
    incremental_drift_data.loc[:, col] = incremental_drift_data[col].values + (increment * original_std * 0.5)

print(f"📌 สร้าง Incremental Drift ใน 'mean compactness' และ 'mean concavity'")

# %% [markdown]
# ### 2.1.3 ตรวจจับ Dataset-level Drift

# %%
# ตรวจจับ Drift ในแต่ละประเภท
print("=" * 60)
print("📊 ตรวจจับ Dataset-level Drift")
print("=" * 60)

# Column Mapping
column_mapping = ColumnMapping(
    target='target',
    numerical_features=selected_features
)

# สร้างฟังก์ชันสำหรับตรวจจับ drift
def detect_dataset_drift(reference, current, name, column_mapping):
    """ตรวจจับ dataset-level drift"""
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current, column_mapping=column_mapping)
    results = report.as_dict()

    drift_info = results['metrics'][0]['result']
    return {
        'name': name,
        'dataset_drift': drift_info['dataset_drift'],
        'drift_share': drift_info['share_of_drifted_columns'],
        'n_drifted': drift_info['number_of_drifted_columns']
    }

# %%
# ตรวจจับ drift ทุกประเภท
drift_types = [
    ('Gradual Drift', gradual_drift_data),
    ('Sudden Drift', sudden_drift_data),
    ('Seasonal Drift', seasonal_drift_data),
    ('Incremental Drift', incremental_drift_data),
]

print("\n📋 สรุปผลการตรวจจับ Dataset Drift:")
print("-" * 60)
print(f"{'Drift Type':<20} {'Detected':<12} {'Drift Share':<15} {'N Drifted'}")
print("-" * 60)

drift_results = []
for name, data in drift_types:
    result = detect_dataset_drift(reference_data, data, name, column_mapping)
    drift_results.append(result)
    detected = "✅ Yes" if result['dataset_drift'] else "❌ No"
    print(f"{result['name']:<20} {detected:<12} {result['drift_share']:.1%}{'':>10} {result['n_drifted']}")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 2.1
#
# 1. ลองปรับ drift_factor ให้มากขึ้น/น้อยลง และสังเกตผล
# 2. สร้าง drift แบบใหม่ที่รวม gradual + sudden drift
# 3. ทดลองกับ dataset อื่นและเปรียบเทียบผล

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 2.2: Feature Drift Detection
#
# ## วัตถุประสงค์
# - ตรวจจับ Drift ในระดับ Feature แต่ละตัว
# - วิเคราะห์ว่า Feature ใดมี Drift
# - สร้าง Feature-level Drift Report

# %% [markdown]
# ### 2.2.1 ตรวจจับ Drift ในแต่ละ Feature

# %%
# สร้าง Feature Drift Report
print("=" * 60)
print("📊 Feature-level Drift Detection")
print("=" * 60)

# ใช้ Sudden Drift data เพื่อให้เห็นผลชัดเจน
feature_drift_report = Report(metrics=[
    DataDriftPreset()
])

feature_drift_report.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

print("✅ สร้าง Feature Drift Report สำเร็จ!")

# %%
# วิเคราะห์ Drift ในแต่ละ Feature
feature_results = feature_drift_report.as_dict()

print("\n📋 Feature-level Drift Analysis:")
print("-" * 70)
print(f"{'Feature':<25} {'Drift Detected':<15} {'Drift Score':<15} {'Stat Test'}")
print("-" * 70)

drift_by_columns = feature_results['metrics'][0]['result']['drift_by_columns']

for feature, info in drift_by_columns.items():
    if feature != 'target':
        detected = "✅ Yes" if info['drift_detected'] else "❌ No"
        score = f"{info['drift_score']:.4f}"
        test = info['stattest_name']
        print(f"{feature:<25} {detected:<15} {score:<15} {test}")

# %%
# บันทึก Report
feature_drift_report.save_html("report_feature_drift.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_feature_drift.html' สำเร็จ!")

# %% [markdown]
# ### 2.2.2 ตรวจจับ Drift แบบเจาะจง Feature

# %%
# ตรวจจับ Drift เฉพาะ Feature ที่สนใจ
print("=" * 60)
print("📊 Single Feature Drift Detection")
print("=" * 60)

# สร้าง Report สำหรับ features เฉพาะ
single_feature_report = Report(metrics=[
    ColumnDriftMetric(column_name='mean radius'),
    ColumnDriftMetric(column_name='mean area'),
    ColumnDriftMetric(column_name='mean texture'),
])

single_feature_report.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

# แสดงผล
single_results = single_feature_report.as_dict()

print("\n📋 Single Feature Drift Results:")
print("-" * 50)

for metric in single_results['metrics']:
    result = metric['result']
    feature = result['column_name']
    detected = "✅ Yes" if result['drift_detected'] else "❌ No"
    score = result['drift_score']
    print(f"📌 {feature}: Drift={detected}, Score={score:.4f}")

# %% [markdown]
# ### 2.2.3 เปรียบเทียบ Distribution ก่อน-หลัง Drift

# %%
# วิเคราะห์ Distribution ของ Feature ที่มี Drift
print("=" * 60)
print("📊 Distribution Comparison")
print("=" * 60)

# สร้าง Report แสดง distribution
distribution_report = Report(metrics=[
    ColumnSummaryMetric(column_name='mean radius'),
    ColumnSummaryMetric(column_name='mean area'),
    ColumnValueRangeMetric(column_name='mean radius'),
    ColumnValueRangeMetric(column_name='mean area'),
])

distribution_report.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

dist_results = distribution_report.as_dict()

print("\n📋 Distribution Statistics Comparison:")
print("-" * 70)

for metric in dist_results['metrics']:
    if 'ColumnSummaryMetric' in metric['metric']:
        result = metric['result']
        col = result['column_name']
        ref = result['reference_characteristics']
        cur = result['current_characteristics']

        print(f"\n🔹 {col}:")
        print(f"   Reference: mean={ref['mean']:.2f}, std={ref['std']:.2f}, min={ref['min']:.2f}, max={ref['max']:.2f}")
        print(f"   Current:   mean={cur['mean']:.2f}, std={cur['std']:.2f}, min={cur['min']:.2f}, max={cur['max']:.2f}")

# %%
# บันทึก Distribution Report
distribution_report.save_html("report_distribution_comparison.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_distribution_comparison.html' สำเร็จ!")

# %% [markdown]
# ### 2.2.4 สร้าง Feature Drift Test Suite

# %%
# Test Suite สำหรับ Feature Drift
print("=" * 60)
print("🧪 Feature Drift Test Suite")
print("=" * 60)

feature_drift_test = TestSuite(tests=[
    # ตรวจสอบ drift ในแต่ละ feature
    TestColumnDrift(column_name='mean radius'),
    TestColumnDrift(column_name='mean area'),
    TestColumnDrift(column_name='mean texture'),
    TestColumnDrift(column_name='mean perimeter'),
    TestColumnDrift(column_name='mean smoothness'),

    # ตรวจสอบจำนวน features ที่ drift
    TestShareOfDriftedColumns(lte=0.3),  # ไม่เกิน 30%

    # ตรวจสอบ dataset drift
    TestNumberOfDriftedColumns(lte=3),  # ไม่เกิน 3 columns
])

feature_drift_test.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

# แสดงผล
test_results = feature_drift_test.as_dict()

print("\n📋 Feature Drift Test Results:")
print("-" * 60)

passed = 0
failed = 0
for test in test_results['tests']:
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    if test['status'] == 'SUCCESS':
        passed += 1
    else:
        failed += 1
    print(f"{status}: {test['name']}")

print(f"\n📊 Summary: {passed} passed, {failed} failed")

# %%
# บันทึก Test Suite
feature_drift_test.save_html("test_suite_feature_drift.html")
print("\n💾 บันทึก Test Suite เป็นไฟล์ 'test_suite_feature_drift.html' สำเร็จ!")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 2.2
#
# 1. สร้าง drift ให้กับ features อื่นๆ และตรวจจับ
# 2. ปรับ threshold ของ TestShareOfDriftedColumns และสังเกตผล
# 3. เปรียบเทียบ distribution ของ features ที่ drift vs ไม่ drift

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 2.3: Drift Detection Methods
#
# ## วัตถุประสงค์
# - เข้าใจ Statistical Tests ที่ใช้ตรวจจับ Drift
# - เปรียบเทียบ methods ต่างๆ
# - เลือก method ที่เหมาะสมกับข้อมูล

# %% [markdown]
# ### 2.3.1 Statistical Tests สำหรับ Drift Detection
#
# **Evidently รองรับ Statistical Tests หลายแบบ:**
#
# | Test | ใช้กับ | ลักษณะ |
# |------|--------|--------|
# | **Kolmogorov-Smirnov (KS)** | Numerical | เปรียบเทียบ CDF |
# | **Wasserstein Distance** | Numerical | Earth Mover's Distance |
# | **Jensen-Shannon Divergence** | Both | Information-theoretic |
# | **Chi-Square** | Categorical | Frequency comparison |
# | **Z-test** | Numerical | Mean comparison |
# | **Population Stability Index (PSI)** | Both | Banking/Credit risk |

# %%
# Import stattest options
from evidently.calculations.stattests import StatTest

print("=" * 60)
print("📊 Statistical Tests สำหรับ Drift Detection")
print("=" * 60)

# แสดง Statistical Tests ที่ใช้ได้
available_tests = [
    ('ks', 'Kolmogorov-Smirnov', 'numerical'),
    ('wasserstein', 'Wasserstein Distance', 'numerical'),
    ('jensenshannon', 'Jensen-Shannon Divergence', 'both'),
    ('psi', 'Population Stability Index', 'both'),
    ('kl_div', 'Kullback-Leibler Divergence', 'both'),
    ('chisquare', 'Chi-Square', 'categorical'),
    ('z', 'Z-test', 'numerical'),
    ('t_test', 'T-test', 'numerical'),
]

print("\n📋 Available Statistical Tests:")
print("-" * 60)
print(f"{'Test ID':<15} {'Name':<30} {'Data Type'}")
print("-" * 60)
for test_id, name, dtype in available_tests:
    print(f"{test_id:<15} {name:<30} {dtype}")

# %% [markdown]
# ### 2.3.2 เปรียบเทียบ Statistical Tests

# %%
# ทดสอบ methods ต่างๆ กับข้อมูลเดียวกัน
print("=" * 60)
print("📊 เปรียบเทียบ Statistical Tests")
print("=" * 60)

# เลือก feature ที่จะทดสอบ
test_feature = 'mean radius'

# สร้างข้อมูลที่มี drift ระดับต่างๆ
np.random.seed(42)
original_values = reference_data[test_feature].values

# Mild drift (5% shift)
mild_drift = sudden_drift_data.copy()
mild_drift[test_feature] = original_values[:len(mild_drift)] * 1.05

# Moderate drift (15% shift)
moderate_drift = sudden_drift_data.copy()
moderate_drift[test_feature] = original_values[:len(moderate_drift)] * 1.15

# Severe drift (30% shift)
severe_drift = sudden_drift_data.copy()
severe_drift[test_feature] = original_values[:len(severe_drift)] * 1.30

print(f"📌 Testing feature: {test_feature}")
print(f"📌 Mild drift: 5% shift")
print(f"📌 Moderate drift: 15% shift")
print(f"📌 Severe drift: 30% shift")

# %%
# ทดสอบแต่ละ method
stat_tests = ['ks', 'wasserstein', 'jensenshannon', 'psi']
drift_levels = [
    ('No Drift', reference_data.iloc[200:]),
    ('Mild (5%)', mild_drift),
    ('Moderate (15%)', moderate_drift),
    ('Severe (30%)', severe_drift),
]

print("\n📋 Comparison Results:")
print("-" * 80)
print(f"{'Test':<15} {'No Drift':<15} {'Mild (5%)':<15} {'Moderate (15%)':<15} {'Severe (30%)':<15}")
print("-" * 80)

for stat_test in stat_tests:
    results = []
    for level_name, data in drift_levels:
        try:
            report = Report(metrics=[
                ColumnDriftMetric(column_name=test_feature, stattest=stat_test)
            ])
            report.run(
                reference_data=reference_data,
                current_data=data,
                column_mapping=column_mapping
            )
            result = report.as_dict()
            drift_score = result['metrics'][0]['result']['drift_score']
            detected = result['metrics'][0]['result']['drift_detected']
            mark = "⚠️" if detected else "✓"
            results.append(f"{drift_score:.4f} {mark}")
        except Exception as e:
            results.append("N/A")

    print(f"{stat_test:<15} {results[0]:<15} {results[1]:<15} {results[2]:<15} {results[3]:<15}")

# %% [markdown]
# ### 2.3.3 กำหนด Custom Statistical Test

# %%
# ใช้ Statistical Test ที่กำหนดเอง
print("=" * 60)
print("📊 Custom Statistical Test Configuration")
print("=" * 60)

# สร้าง Report ด้วย custom stattest
custom_stattest_report = Report(metrics=[
    # ใช้ KS test กับ threshold ที่กำหนดเอง
    ColumnDriftMetric(
        column_name='mean radius',
        stattest='ks',
        stattest_threshold=0.1  # กำหนด threshold เอง
    ),
    # ใช้ Wasserstein distance
    ColumnDriftMetric(
        column_name='mean area',
        stattest='wasserstein',
        stattest_threshold=0.1
    ),
    # ใช้ PSI
    ColumnDriftMetric(
        column_name='mean texture',
        stattest='psi',
        stattest_threshold=0.2
    ),
])

custom_stattest_report.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

# แสดงผล
custom_results = custom_stattest_report.as_dict()

print("\n📋 Custom Statistical Test Results:")
print("-" * 70)

for metric in custom_results['metrics']:
    result = metric['result']
    col = result['column_name']
    test = result['stattest_name']
    threshold = result['stattest_threshold']
    score = result['drift_score']
    detected = "✅ Drift" if result['drift_detected'] else "❌ No Drift"

    print(f"📌 {col}:")
    print(f"   Test: {test}, Threshold: {threshold}, Score: {score:.4f}")
    print(f"   Result: {detected}")
    print()

# %%
# บันทึก Report
custom_stattest_report.save_html("report_custom_stattest.html")
print("💾 บันทึก Report เป็นไฟล์ 'report_custom_stattest.html' สำเร็จ!")

# %% [markdown]
# ### 2.3.4 เลือก Method ที่เหมาะสม

# %%
# คำแนะนำในการเลือก Statistical Test
print("=" * 60)
print("📚 คำแนะนำในการเลือก Statistical Test")
print("=" * 60)

recommendations = """
📌 Kolmogorov-Smirnov (ks):
   - เหมาะกับ: Numerical data ทั่วไป
   - ข้อดี: ไม่ต้องสมมติ distribution, sensitive ต่อ shape changes
   - ข้อเสีย: อาจไม่ sensitive กับ tail differences

📌 Wasserstein Distance:
   - เหมาะกับ: ต้องการวัด "ระยะทาง" ระหว่าง distributions
   - ข้อดี: Interpretable, ไม่มีปัญหากับ zero probabilities
   - ข้อเสีย: อาจ sensitive กับ outliers

📌 Jensen-Shannon Divergence:
   - เหมาะกับ: Probability distributions
   - ข้อดี: Symmetric, bounded (0-1)
   - ข้อเสีย: ต้อง discretize continuous data

📌 Population Stability Index (PSI):
   - เหมาะกับ: Credit scoring, Risk management
   - ข้อดี: Industry standard, interpretable thresholds
   - ข้อเสีย: Sensitive to bin selection

📌 Chi-Square:
   - เหมาะกับ: Categorical data
   - ข้อดี: Well-understood, works with frequencies
   - ข้อเสีย: Requires sufficient sample size per category

📋 General Guidelines:
   PSI < 0.1: No drift
   PSI 0.1-0.2: Slight drift (monitor)
   PSI > 0.2: Significant drift (action needed)
"""

print(recommendations)

# %% [markdown]
# ### 2.3.5 Test Suite ด้วย Multiple Methods

# %%
# สร้าง Test Suite ที่ใช้หลาย methods
print("=" * 60)
print("🧪 Multi-Method Test Suite")
print("=" * 60)

multi_method_test = TestSuite(tests=[
    # ใช้ KS test
    TestColumnDrift(column_name='mean radius', stattest='ks'),

    # ใช้ PSI
    TestColumnDrift(column_name='mean area', stattest='psi'),

    # ใช้ Wasserstein
    TestColumnDrift(column_name='mean texture', stattest='wasserstein'),

    # Overall dataset drift
    TestShareOfDriftedColumns(lte=0.5),
])

multi_method_test.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

# แสดงผล
multi_results = multi_method_test.as_dict()

print("\n📋 Multi-Method Test Results:")
print("-" * 60)

for test in multi_results['tests']:
    status = "✅ PASS" if test['status'] == 'SUCCESS' else "❌ FAIL"
    print(f"{status}: {test['name']}")

# %%
# บันทึก Test Suite
multi_method_test.save_html("test_suite_multi_method.html")
print("\n💾 บันทึก Test Suite เป็นไฟล์ 'test_suite_multi_method.html' สำเร็จ!")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 2.3
#
# 1. ทดลองใช้ statistical tests อื่นๆ ที่ยังไม่ได้ใช้
# 2. ปรับ threshold ของแต่ละ test และสังเกตผลกระทบ
# 3. สร้างข้อมูล categorical และใช้ Chi-Square test

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # LAB 2.4: Handling and Mitigating Drift
#
# ## วัตถุประสงค์
# - เรียนรู้กลยุทธ์ในการจัดการกับ Drift
# - สร้าง Monitoring Pipeline
# - Implement Drift Alert System

# %% [markdown]
# ### 2.4.1 กลยุทธ์ในการจัดการกับ Drift
#
# **เมื่อตรวจพบ Drift สามารถดำเนินการได้หลายวิธี:**
#
# 1. **Retrain Model**: Train โมเดลใหม่ด้วยข้อมูลล่าสุด
# 2. **Update Reference Data**: อัพเดท baseline data
# 3. **Feature Engineering**: ปรับปรุง features
# 4. **Ensemble Methods**: ใช้หลายโมเดลร่วมกัน
# 5. **Online Learning**: อัพเดทโมเดลแบบ incremental

# %%
# สร้างระบบ Drift Monitoring Pipeline
print("=" * 60)
print("📊 Drift Monitoring Pipeline")
print("=" * 60)

class DriftMonitor:
    """Class สำหรับ monitoring drift อย่างเป็นระบบ"""

    def __init__(self, reference_data, column_mapping, thresholds=None):
        self.reference_data = reference_data
        self.column_mapping = column_mapping
        self.thresholds = thresholds or {
            'dataset_drift_share': 0.3,
            'feature_drift_pvalue': 0.05,
            'psi_threshold': 0.2,
        }
        self.history = []

    def check_drift(self, current_data, batch_id=None):
        """ตรวจสอบ drift และบันทึกผล"""
        # Dataset-level drift
        dataset_report = Report(metrics=[DataDriftPreset()])
        dataset_report.run(
            reference_data=self.reference_data,
            current_data=current_data,
            column_mapping=self.column_mapping
        )
        dataset_results = dataset_report.as_dict()
        drift_info = dataset_results['metrics'][0]['result']

        # สร้าง result object
        result = {
            'batch_id': batch_id,
            'timestamp': pd.Timestamp.now(),
            'dataset_drift': drift_info['dataset_drift'],
            'drift_share': drift_info['share_of_drifted_columns'],
            'n_drifted_columns': drift_info['number_of_drifted_columns'],
            'drifted_features': [],
            'alerts': []
        }

        # หา features ที่ drift
        for feature, info in drift_info['drift_by_columns'].items():
            if info['drift_detected']:
                result['drifted_features'].append({
                    'feature': feature,
                    'drift_score': info['drift_score'],
                    'stattest': info['stattest_name']
                })

        # สร้าง alerts
        result['alerts'] = self._generate_alerts(result)

        # บันทึก history
        self.history.append(result)

        return result

    def _generate_alerts(self, result):
        """สร้าง alerts ตาม thresholds"""
        alerts = []

        if result['dataset_drift']:
            alerts.append({
                'level': 'CRITICAL',
                'type': 'DATASET_DRIFT',
                'message': f"🚨 Dataset drift detected! {result['drift_share']:.1%} of features drifted"
            })

        if result['drift_share'] > self.thresholds['dataset_drift_share']:
            alerts.append({
                'level': 'HIGH',
                'type': 'HIGH_DRIFT_SHARE',
                'message': f"⚠️ High drift share: {result['drift_share']:.1%} (threshold: {self.thresholds['dataset_drift_share']:.1%})"
            })

        return alerts

    def get_summary(self):
        """สรุปผล monitoring"""
        if not self.history:
            return "No monitoring data available"

        total_checks = len(self.history)
        drift_detected = sum(1 for h in self.history if h['dataset_drift'])

        summary = {
            'total_checks': total_checks,
            'drift_detected_count': drift_detected,
            'drift_rate': drift_detected / total_checks if total_checks > 0 else 0,
            'most_drifted_features': self._get_most_drifted_features()
        }

        return summary

    def _get_most_drifted_features(self):
        """หา features ที่ drift บ่อยที่สุด"""
        feature_counts = {}
        for h in self.history:
            for f in h['drifted_features']:
                feature = f['feature']
                feature_counts[feature] = feature_counts.get(feature, 0) + 1

        return sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)[:5]


print("✅ สร้าง DriftMonitor class สำเร็จ!")

# %%
# ทดสอบ Drift Monitor
print("\n" + "=" * 60)
print("🔍 ทดสอบ Drift Monitor")
print("=" * 60)

# สร้าง monitor
monitor = DriftMonitor(
    reference_data=reference_data,
    column_mapping=column_mapping
)

# จำลองการตรวจสอบ batches หลายๆ รอบ
batches = [
    ('batch_001', reference_data.iloc[200:]),  # No drift
    ('batch_002', gradual_drift_data),          # Gradual drift
    ('batch_003', sudden_drift_data),           # Sudden drift
    ('batch_004', seasonal_drift_data),         # Seasonal drift
]

print("\n📋 Monitoring Results:")
print("-" * 70)

for batch_id, data in batches:
    result = monitor.check_drift(data, batch_id=batch_id)
    drift_status = "🚨 DRIFT" if result['dataset_drift'] else "✅ OK"
    print(f"\n{batch_id}: {drift_status}")
    print(f"   Drift Share: {result['drift_share']:.1%}")
    print(f"   Drifted Features: {result['n_drifted_columns']}")

    if result['alerts']:
        for alert in result['alerts']:
            print(f"   [{alert['level']}] {alert['message']}")

# %%
# แสดง Summary
print("\n" + "=" * 60)
print("📊 Monitoring Summary")
print("=" * 60)

summary = monitor.get_summary()

print(f"\n📌 Total Checks: {summary['total_checks']}")
print(f"📌 Drift Detected: {summary['drift_detected_count']} times")
print(f"📌 Drift Rate: {summary['drift_rate']:.1%}")

print("\n📌 Most Frequently Drifted Features:")
for feature, count in summary['most_drifted_features']:
    print(f"   - {feature}: {count} times")

# %% [markdown]
# ### 2.4.2 สร้าง Drift Response Actions

# %%
# สร้างฟังก์ชันสำหรับ response actions
print("=" * 60)
print("📊 Drift Response Actions")
print("=" * 60)

def recommend_actions(drift_result, model_performance=None):
    """แนะนำ actions ตามผล drift"""
    actions = []

    drift_share = drift_result['drift_share']
    n_drifted = drift_result['n_drifted_columns']

    # กำหนด actions ตามระดับ drift
    if drift_share < 0.1:
        actions.append({
            'priority': 'LOW',
            'action': 'MONITOR',
            'description': 'Continue monitoring, no immediate action required'
        })

    elif drift_share < 0.3:
        actions.append({
            'priority': 'MEDIUM',
            'action': 'INVESTIGATE',
            'description': 'Investigate drifted features and assess impact'
        })
        actions.append({
            'priority': 'MEDIUM',
            'action': 'UPDATE_REFERENCE',
            'description': 'Consider updating reference data window'
        })

    else:
        actions.append({
            'priority': 'HIGH',
            'action': 'RETRAIN',
            'description': 'Retrain model with recent data'
        })
        actions.append({
            'priority': 'HIGH',
            'action': 'ALERT_STAKEHOLDERS',
            'description': 'Notify data science team and stakeholders'
        })

    # ถ้ามีข้อมูล performance
    if model_performance and model_performance.get('accuracy_drop', 0) > 0.05:
        actions.append({
            'priority': 'CRITICAL',
            'action': 'IMMEDIATE_RETRAIN',
            'description': f"Model accuracy dropped by {model_performance['accuracy_drop']:.1%}"
        })

    return actions

# %%
# ทดสอบ action recommendations
print("\n📋 Action Recommendations for Each Batch:")
print("-" * 70)

for batch_id, data in batches:
    result = monitor.history[batches.index((batch_id, data))]
    actions = recommend_actions(result)

    print(f"\n🔹 {batch_id} (Drift Share: {result['drift_share']:.1%}):")
    for action in actions:
        print(f"   [{action['priority']}] {action['action']}: {action['description']}")

# %% [markdown]
# ### 2.4.3 สร้าง Comprehensive Monitoring Report

# %%
# สร้าง Comprehensive Report
print("=" * 60)
print("📊 Comprehensive Drift Monitoring Report")
print("=" * 60)

# ใช้ข้อมูล sudden drift สำหรับ demo
comprehensive_monitor_report = Report(metrics=[
    # Dataset overview
    DatasetSummaryMetric(),

    # Data Drift
    DataDriftPreset(),

    # Data Quality
    DatasetMissingValuesMetric(),
    DatasetDuplicatedRowsMetric(),

    # Feature-level details
    ColumnSummaryMetric(column_name='mean radius'),
    ColumnSummaryMetric(column_name='mean area'),
    ColumnDriftMetric(column_name='mean radius'),
    ColumnDriftMetric(column_name='mean area'),
])

comprehensive_monitor_report.run(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping
)

print("✅ สร้าง Comprehensive Report สำเร็จ!")

# %%
# บันทึก Comprehensive Report
comprehensive_monitor_report.save_html("report_comprehensive_monitoring.html")
print("\n💾 บันทึก Report เป็นไฟล์ 'report_comprehensive_monitoring.html' สำเร็จ!")

# %% [markdown]
# ### 2.4.4 Automated Drift Detection Pipeline

# %%
# สร้าง Automated Pipeline
print("=" * 60)
print("📊 Automated Drift Detection Pipeline")
print("=" * 60)

def run_drift_pipeline(reference_data, current_data, column_mapping,
                       thresholds=None, save_report=True, report_name=None):
    """
    รัน drift detection pipeline แบบอัตโนมัติ

    Returns:
    - dict: ผลการตรวจจับ drift และ recommendations
    """
    if thresholds is None:
        thresholds = {
            'drift_share': 0.3,
            'psi': 0.2,
        }

    results = {
        'status': 'OK',
        'drift_detected': False,
        'metrics': {},
        'alerts': [],
        'recommendations': []
    }

    # 1. ตรวจสอบ Data Quality
    quality_report = Report(metrics=[
        DatasetMissingValuesMetric(),
        DatasetDuplicatedRowsMetric()
    ])
    quality_report.run(current_data=current_data, reference_data=reference_data,
                       column_mapping=column_mapping)
    quality_results = quality_report.as_dict()

    missing_share = quality_results['metrics'][0]['result']['current']['share_of_missing_values']
    dup_share = quality_results['metrics'][1]['result']['current']['share_of_duplicated_rows']

    results['metrics']['missing_values_share'] = missing_share
    results['metrics']['duplicates_share'] = dup_share

    # 2. ตรวจสอบ Data Drift
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_data, current_data=current_data,
                     column_mapping=column_mapping)
    drift_results = drift_report.as_dict()

    drift_info = drift_results['metrics'][0]['result']
    results['metrics']['drift_share'] = drift_info['share_of_drifted_columns']
    results['metrics']['n_drifted_columns'] = drift_info['number_of_drifted_columns']
    results['drift_detected'] = drift_info['dataset_drift']

    # 3. สร้าง Alerts
    if results['drift_detected']:
        results['status'] = 'WARNING'
        results['alerts'].append({
            'level': 'HIGH',
            'message': f"Dataset drift detected: {drift_info['share_of_drifted_columns']:.1%} features drifted"
        })

    if missing_share > 0.05:
        results['alerts'].append({
            'level': 'MEDIUM',
            'message': f"High missing values: {missing_share:.1%}"
        })

    # 4. สร้าง Recommendations
    if drift_info['share_of_drifted_columns'] > thresholds['drift_share']:
        results['status'] = 'CRITICAL'
        results['recommendations'].append("Retrain model with recent data")
        results['recommendations'].append("Update reference dataset")
    elif drift_info['share_of_drifted_columns'] > 0.1:
        results['recommendations'].append("Monitor closely")
        results['recommendations'].append("Investigate drifted features")

    # 5. บันทึก Report (optional)
    if save_report:
        filename = report_name or f"pipeline_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html"
        comprehensive_report = Report(metrics=[
            DatasetSummaryMetric(),
            DataDriftPreset(),
            DatasetMissingValuesMetric(),
        ])
        comprehensive_report.run(reference_data=reference_data, current_data=current_data,
                                column_mapping=column_mapping)
        comprehensive_report.save_html(filename)
        results['report_file'] = filename

    return results

# %%
# ทดสอบ Pipeline
print("\n🔄 Running Automated Pipeline...")
print("-" * 60)

pipeline_result = run_drift_pipeline(
    reference_data=reference_data,
    current_data=sudden_drift_data,
    column_mapping=column_mapping,
    report_name="report_pipeline_output.html"
)

print(f"\n📋 Pipeline Results:")
print(f"   Status: {pipeline_result['status']}")
print(f"   Drift Detected: {pipeline_result['drift_detected']}")
print(f"\n📊 Metrics:")
for key, value in pipeline_result['metrics'].items():
    if isinstance(value, float):
        print(f"   {key}: {value:.4f}")
    else:
        print(f"   {key}: {value}")

print(f"\n⚠️ Alerts:")
for alert in pipeline_result['alerts']:
    print(f"   [{alert['level']}] {alert['message']}")

print(f"\n💡 Recommendations:")
for rec in pipeline_result['recommendations']:
    print(f"   - {rec}")

print(f"\n📁 Report saved: {pipeline_result.get('report_file', 'N/A')}")

# %% [markdown]
# ### 📝 แบบฝึกหัด LAB 2.4
#
# 1. ปรับปรุง DriftMonitor class ให้เก็บ history ลง file
# 2. สร้างระบบ notification (email, Slack) เมื่อตรวจพบ drift
# 3. Implement online learning approach เมื่อตรวจพบ gradual drift
# 4. สร้าง dashboard สำหรับ monitoring ด้วย Streamlit หรือ Dash

# %%
# พื้นที่สำหรับทำแบบฝึกหัด
# TODO: เขียนโค้ดของคุณที่นี่




# %% [markdown]
# ---
# # สรุป Section 2
#
# ## สิ่งที่ได้เรียนรู้
#
# ### LAB 2.1: Understanding Data Drift
# - ประเภทของ Data Drift (Gradual, Sudden, Seasonal, Incremental)
# - สร้างข้อมูลจำลองที่มี Drift แบบต่างๆ
# - ตรวจจับ Dataset-level Drift
#
# ### LAB 2.2: Feature Drift Detection
# - ตรวจจับ Drift ในระดับ Feature
# - เปรียบเทียบ Distribution ก่อน-หลัง Drift
# - สร้าง Feature Drift Test Suite
#
# ### LAB 2.3: Drift Detection Methods
# - Statistical Tests ต่างๆ (KS, Wasserstein, PSI, Chi-Square)
# - เลือก method ที่เหมาะสมกับข้อมูล
# - กำหนด Custom Statistical Test
#
# ### LAB 2.4: Handling and Mitigating Drift
# - กลยุทธ์จัดการกับ Drift
# - สร้าง Drift Monitoring Pipeline
# - Automated Drift Detection

# %% [markdown]
# ## Best Practices สำหรับ Drift Management
#
# 1. **Monitor สม่ำเสมอ**: ตั้ง schedule การตรวจสอบ (daily, weekly)
# 2. **กำหนด Threshold ที่เหมาะสม**: ปรับตาม business context
# 3. **เก็บ Historical Data**: เพื่อวิเคราะห์ trend และ pattern
# 4. **Automate Response**: สร้างระบบ auto-retrain เมื่อจำเป็น
# 5. **Document Everything**: บันทึกเหตุการณ์และ actions ที่ทำ

# %%
# สรุป files ที่สร้างจาก Section 2
print("=" * 60)
print("📁 Files ที่สร้างจาก Section 2")
print("=" * 60)
print("""
1. report_feature_drift.html - Feature Drift Report
2. report_distribution_comparison.html - Distribution Comparison Report
3. test_suite_feature_drift.html - Feature Drift Test Suite
4. report_custom_stattest.html - Custom Statistical Test Report
5. test_suite_multi_method.html - Multi-Method Test Suite
6. report_comprehensive_monitoring.html - Comprehensive Monitoring Report
7. report_pipeline_output.html - Pipeline Output Report
""")
print("✅ Lab Section 2 เสร็จสมบูรณ์!")
