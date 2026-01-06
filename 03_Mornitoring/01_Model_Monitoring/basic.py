# %% [markdown]
# # 📚 LAB 1.1: Introduction to Evidently AI
# ## แนะนำ Evidently AI สำหรับการ Monitor โมเดล Machine Learning
#
# ---
#
# ## 🎯 วัตถุประสงค์การเรียนรู้
# หลังจากจบ LAB นี้ นักศึกษาจะสามารถ:
# 1. เข้าใจความสำคัญของ Model Monitoring
# 2. ติดตั้งและตั้งค่า Evidently AI
# 3. เข้าใจโครงสร้างของ Report และ Test Suite
# 4. สร้าง Report แรกจาก dataset ตัวอย่าง
#
# ---
#
# ## 📖 ทฤษฎีพื้นฐาน
#
# ### ทำไมต้อง Monitor โมเดล?
#
# เมื่อโมเดล ML ถูก deploy ไปใช้งานจริง มันอาจเกิดปัญหาหลายอย่าง:
#
# | ปัญหา | คำอธิบาย | ผลกระทบ |
# |-------|----------|---------|
# | **Data Drift** | ข้อมูล input เปลี่ยนแปลงไปจากตอน train | โมเดลทำนายผิดพลาด |
# | **Concept Drift** | ความสัมพันธ์ระหว่าง feature กับ target เปลี่ยน | โมเดลล้าสมัย |
# | **Model Decay** | Performance ลดลงตามเวลา | ความแม่นยำต่ำลง |
# | **Data Quality Issues** | ข้อมูลมี missing, outliers | ผลลัพธ์ไม่น่าเชื่อถือ |
#
# ### Evidently AI คืออะไร?
#
# **Evidently** เป็น open-source Python library สำหรับ:
# - 📊 สร้าง **Reports** - รายงานวิเคราะห์ข้อมูลและโมเดล
# - ✅ สร้าง **Test Suites** - ชุดทดสอบอัตโนมัติ
# - 🔍 ตรวจจับ **Data Drift** และ **Model Drift**
# - 📈 ติดตาม **Model Performance**
#
# ### โครงสร้างหลักของ Evidently
#
# ```
# Evidently
# ├── Reports (รายงาน)
# │   ├── Metrics (ตัววัดแต่ละตัว)
# │   └── Metric Presets (ชุดตัววัดสำเร็จรูป)
# │
# └── Test Suites (ชุดทดสอบ)
#     ├── Tests (การทดสอบแต่ละตัว)
#     └── Test Presets (ชุดทดสอบสำเร็จรูป)
# ```

# %% [markdown]
# ## 🔧 ขั้นตอนที่ 1: ติดตั้ง Library ที่จำเป็น

# %%
# ติดตั้ง Evidently และ libraries ที่เกี่ยวข้อง
# รันคำสั่งนี้ใน terminal หรือ uncomment บรรทัดด้านล่าง

# !pip install evidently pandas scikit-learn numpy matplotlib seaborn

# %%
# Import libraries ที่จำเป็น
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, load_wine, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Import Evidently
import evidently
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metric_preset import ClassificationPreset, RegressionPreset
from evidently.metrics import *

# แสดง version
print(f"📦 Evidently version: {evidently.__version__}")
print("✅ Import สำเร็จ!")

# %% [markdown]
# ## 📊 ขั้นตอนที่ 2: เตรียมข้อมูลตัวอย่าง
#
# เราจะใช้ **Iris Dataset** เป็นข้อมูลตัวอย่างแรก
# - เป็น classification problem
# - มี 4 features และ 3 classes
# - เข้าใจง่ายและเหมาะสำหรับการเรียนรู้

# %%
# โหลด Iris dataset
print("📥 กำลังโหลด Iris Dataset...")
iris = load_iris()

# สร้าง DataFrame
df_iris = pd.DataFrame(
    data=iris.data,
    columns=iris.feature_names
)
df_iris['target'] = iris.target
df_iris['target_name'] = df_iris['target'].map({
    0: 'setosa', 
    1: 'versicolor', 
    2: 'virginica'
})

print(f"\n📋 ข้อมูลทั้งหมด: {len(df_iris)} แถว")
print(f"📊 จำนวน Features: {len(iris.feature_names)}")
print(f"🎯 จำนวน Classes: {len(iris.target_names)}")

df_iris.head(10)

# %%
# สำรวจข้อมูลเบื้องต้น
print("=" * 50)
print("📊 สถิติเบื้องต้นของข้อมูล")
print("=" * 50)
df_iris.describe()

# %%
# ดูการกระจายของ target
print("\n🎯 การกระจายของ Target Classes:")
print(df_iris['target_name'].value_counts())

# %% [markdown]
# ## 🔀 ขั้นตอนที่ 3: แบ่งข้อมูล Reference และ Current
#
# ### แนวคิดสำคัญ:
# - **Reference Data** = ข้อมูลที่ใช้ตอน train (baseline)
# - **Current Data** = ข้อมูลใหม่ที่เข้ามา (production)
#
# Evidently จะเปรียบเทียบ Current กับ Reference เพื่อตรวจจับความเปลี่ยนแปลง

# %%
# แบ่งข้อมูลเป็น Reference และ Current
# สมมติว่า:
# - Reference = ข้อมูล 70% แรก (ข้อมูลเก่าที่ใช้ train)
# - Current = ข้อมูล 30% หลัง (ข้อมูลใหม่ที่เข้ามา)

# เลือกเฉพาะ feature columns (ไม่รวม target_name)
feature_columns = iris.feature_names

# สร้าง DataFrame สำหรับ Evidently (ใช้เฉพาะ features)
df_reference = df_iris.iloc[:105][feature_columns + ['target']].copy()
df_current = df_iris.iloc[105:][feature_columns + ['target']].copy()

print("📦 ข้อมูล Reference:")
print(f"   - จำนวนแถว: {len(df_reference)}")
print(f"   - Columns: {list(df_reference.columns)}")

print("\n📦 ข้อมูล Current:")
print(f"   - จำนวนแถว: {len(df_current)}")
print(f"   - Columns: {list(df_current.columns)}")

# %% [markdown]
# ## 📈 ขั้นตอนที่ 4: สร้าง Report แรกด้วย Evidently
#
# ### Report คืออะไร?
# Report เป็นการรวมรวม **Metrics** หลายตัวมาแสดงผลด้วยกัน
#
# ### Metric Preset คืออะไร?
# Metric Preset เป็น "ชุดสำเร็จรูป" ของ Metrics ที่เกี่ยวข้องกัน เช่น:
# - `DataDriftPreset` - ตรวจจับ Data Drift
# - `DataQualityPreset` - ตรวจสอบคุณภาพข้อมูล
# - `ClassificationPreset` - วัด performance ของ classification model

# %%
# สร้าง Data Drift Report
print("🔄 กำลังสร้าง Data Drift Report...")

# สร้าง Report object พร้อม DataDriftPreset
data_drift_report = Report(metrics=[
    DataDriftPreset()  # ใช้ preset สำเร็จรูปสำหรับตรวจจับ drift
])

# รัน Report โดยเปรียบเทียบ reference กับ current
data_drift_report.run(
    reference_data=df_reference,
    current_data=df_current
)

print("✅ สร้าง Report สำเร็จ!")

# %%
# แสดงผล Report ใน Notebook
# Report จะแสดงเป็น interactive HTML
data_drift_report

# %% [markdown]
# ### 💡 อธิบายผลลัพธ์:
#
# จาก Report ด้านบน คุณจะเห็น:
# 1. **Dataset Drift** - สรุปว่ามี drift หรือไม่
# 2. **Drift per Feature** - แต่ละ feature มี drift มากน้อยแค่ไหน
# 3. **Distribution Plots** - กราฟเปรียบเทียบการกระจายของข้อมูล

# %%
# บันทึก Report เป็นไฟล์ HTML
data_drift_report.save_html("reports/lab1_1_data_drift_report.html")
print("💾 บันทึก Report เป็นไฟล์ HTML สำเร็จ!")
print("📂 ไฟล์: reports/lab1_1_data_drift_report.html")

# %% [markdown]
# ## 📊 ขั้นตอนที่ 5: สร้าง Data Quality Report

# %%
# สร้าง Data Quality Report
print("🔍 กำลังสร้าง Data Quality Report...")

data_quality_report = Report(metrics=[
    DataQualityPreset()  # ตรวจสอบคุณภาพข้อมูล
])

data_quality_report.run(
    reference_data=df_reference,
    current_data=df_current
)

print("✅ สร้าง Data Quality Report สำเร็จ!")

# %%
# แสดงผล Data Quality Report
data_quality_report

# %% [markdown]
# ## 🧪 ขั้นตอนที่ 6: ทำความเข้าใจ Test Suite
#
# ### Test Suite vs Report
# | Report | Test Suite |
# |--------|------------|
# | แสดงผลเป็นรายงานวิเคราะห์ | แสดงผลเป็น Pass/Fail |
# | เหมาะสำหรับ exploration | เหมาะสำหรับ automation |
# | ไม่มี threshold | กำหนด threshold ได้ |

# %%
# Import Test Suite และ Test Presets
from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset, DataQualityTestPreset

# สร้าง Test Suite สำหรับ Data Drift
print("🧪 กำลังสร้าง Data Drift Test Suite...")

data_drift_test_suite = TestSuite(tests=[
    DataDriftTestPreset()
])

data_drift_test_suite.run(
    reference_data=df_reference,
    current_data=df_current
)

print("✅ รัน Test Suite สำเร็จ!")

# %%
# แสดงผล Test Suite
data_drift_test_suite

# %% [markdown]
# ### 💡 อธิบายผลลัพธ์ Test Suite:
#
# - ✅ **PASS** = ผ่านการทดสอบ (ไม่มีปัญหา)
# - ❌ **FAIL** = ไม่ผ่านการทดสอบ (มีปัญหา)
# - ⚠️ **WARNING** = มีข้อควรระวัง

# %%
# ดูผลลัพธ์แบบ dictionary
test_results = data_drift_test_suite.as_dict()
print("📋 สรุปผลการทดสอบ:")
print(f"   - จำนวน Tests ทั้งหมด: {test_results['summary']['total_tests']}")
print(f"   - ผ่าน (Success): {test_results['summary']['success_tests']}")
print(f"   - ไม่ผ่าน (Failed): {test_results['summary']['failed_tests']}")

# %% [markdown]
# ## 📝 ขั้นตอนที่ 7: สร้าง Report แบบกำหนดเอง (Custom Metrics)

# %%
# สร้าง Report แบบเลือก Metrics เอง
print("🎨 กำลังสร้าง Custom Report...")

custom_report = Report(metrics=[
    # Dataset-level metrics
    DatasetSummaryMetric(),           # สรุปข้อมูลทั้งหมด
    DatasetDriftMetric(),             # ตรวจจับ drift ระดับ dataset
    
    # Column-level metrics
    ColumnDriftMetric(column_name='sepal length (cm)'),  # drift ของ column เฉพาะ
    ColumnSummaryMetric(column_name='sepal width (cm)'), # สรุป column เฉพาะ
])

custom_report.run(
    reference_data=df_reference,
    current_data=df_current
)

print("✅ สร้าง Custom Report สำเร็จ!")

# %%
# แสดงผล Custom Report
custom_report

# %% [markdown]
# ## 🎯 สรุป LAB 1.1
#
# ### สิ่งที่เรียนรู้ในบทนี้:
#
# 1. **ความสำคัญของ Model Monitoring**
#    - ป้องกัน Model Decay
#    - ตรวจจับ Data Drift
#    - รักษาคุณภาพของโมเดลใน Production
#
# 2. **โครงสร้างของ Evidently**
#    - Report = รายงานวิเคราะห์
#    - Test Suite = ชุดทดสอบอัตโนมัติ
#    - Metric Preset = ชุดตัววัดสำเร็จรูป
#
# 3. **การใช้งานเบื้องต้น**
#    - สร้าง Report ด้วย Metric Preset
#    - สร้าง Test Suite
#    - บันทึก Report เป็น HTML
#
# ### 📚 แบบฝึกหัด:
# 1. ลองเปลี่ยน dataset เป็น Wine หรือ California Housing
# 2. สร้าง Report ด้วย Metric Preset อื่นๆ
# 3. ลองบันทึก Test Suite เป็นไฟล์ HTML

# %%
print("🎉 จบ LAB 1.1: Introduction to Evidently AI")
print("=" * 50)
