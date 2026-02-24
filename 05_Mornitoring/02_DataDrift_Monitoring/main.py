# %%
# Complete MLOps Labs: Understanding Data Drift Concepts with sklearn

## LAB 1: Understanding Data Drift Concepts


# %% [markdown]
# # LAB 1: Understanding Data Drift Concepts
# ## ทำความเข้าใจแนวคิดพื้นฐานของ Data Drift
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. เข้าใจความแตกต่างระหว่าง Covariate Shift และ Concept Drift
# 2. เรียนรู้ Statistical tests สำหรับ drift detection (KS, PSI, Wasserstein)
# 3. สามารถเลือก drift detection method ที่เหมาะสมกับสถานการณ์ต่างๆ
#
# ### ทฤษฎีพื้นฐาน:
# **Data Drift** คือ การเปลี่ยนแปลงของข้อมูลเมื่อเวลาผ่านไป ซึ่งอาจส่งผลกระทบต่อประสิทธิภาพของ ML Model
#
# มี 2 ประเภทหลัก:
# - **Covariate Shift**: การเปลี่ยนแปลงของ input features P(X) โดยที่ความสัมพันธ์ P(Y|X) ยังคงเดิม
# - **Concept Drift**: การเปลี่ยนแปลงของความสัมพันธ์ระหว่าง input และ output P(Y|X)

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment และ Import Libraries
#
# ก่อนเริ่มต้น เราจะ import libraries ที่จำเป็นทั้งหมด

# %%
# Import libraries ที่จำเป็น
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# ตั้งค่า random seed เพื่อให้ผลลัพธ์สามารถทำซ้ำได้
np.random.seed(42)

# ตั้งค่า matplotlib สำหรับการแสดงผลภาษาไทย
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("✅ Libraries imported successfully!")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")

# %% [markdown]
# ## ส่วนที่ 2: ทำความเข้าใจ Covariate Shift
#
# ### ทฤษฎี Covariate Shift:
# - เกิดขึ้นเมื่อ distribution ของ input features เปลี่ยนแปลง
# - ตัวอย่าง: โมเดลทำนายราคาบ้านที่ train กับบ้านในเมือง แต่ต้องทำนายบ้านในชนบท
# - ความสัมพันธ์ระหว่าง features กับ target ยังคงเหมือนเดิม
#
# สูตรทางคณิตศาสตร์:
# - Training: P_train(X) ≠ P_test(X)
# - แต่: P(Y|X) คงที่

# %%
def generate_covariate_shift_data():
    """
    สร้างข้อมูลที่แสดง Covariate Shift
    
    ในตัวอย่างนี้:
    - Training data: อายุลูกค้า 20-40 ปี
    - Production data: อายุลูกค้า 40-60 ปี
    - ความสัมพันธ์ระหว่างอายุกับพฤติกรรมการซื้อยังคงเดิม
    """
    
    # Training data: ลูกค้าอายุน้อย (20-40)
    np.random.seed(42)
    n_train = 1000
    age_train = np.random.normal(30, 5, n_train)
    income_train = age_train * 1500 + np.random.normal(0, 5000, n_train)
    
    # กฎการซื้อ: ซื้อถ้า income > 40000 + age * 500
    threshold_train = 40000 + age_train * 500
    purchase_train = (income_train > threshold_train).astype(int)
    
    train_df = pd.DataFrame({
        'age': age_train,
        'income': income_train,
        'purchase': purchase_train
    })
    
    # Production data: ลูกค้าอายุมากขึ้น (40-60) - Covariate Shift!
    n_prod = 1000
    age_prod = np.random.normal(50, 5, n_prod)  # อายุเปลี่ยน!
    income_prod = age_prod * 1500 + np.random.normal(0, 5000, n_prod)
    
    # กฎการซื้อเหมือนเดิม (ไม่มี Concept Drift)
    threshold_prod = 40000 + age_prod * 500
    purchase_prod = (income_prod > threshold_prod).astype(int)
    
    prod_df = pd.DataFrame({
        'age': age_prod,
        'income': income_prod,
        'purchase': purchase_prod
    })
    
    return train_df, prod_df

# สร้างข้อมูล
train_covariate, prod_covariate = generate_covariate_shift_data()

print("📊 Training Data Summary:")
print(train_covariate.describe())
print("\n📊 Production Data Summary:")
print(prod_covariate.describe())

# %%
# Visualize Covariate Shift
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Plot 1: Age Distribution
axes[0].hist(train_covariate['age'], bins=30, alpha=0.7, label='Training', color='blue')
axes[0].hist(prod_covariate['age'], bins=30, alpha=0.7, label='Production', color='red')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Covariate Shift: Age Distribution\n(Training vs Production)')
axes[0].legend()
axes[0].axvline(train_covariate['age'].mean(), color='blue', linestyle='--', label='Train Mean')
axes[0].axvline(prod_covariate['age'].mean(), color='red', linestyle='--', label='Prod Mean')

# Plot 2: Income Distribution
axes[1].hist(train_covariate['income'], bins=30, alpha=0.7, label='Training', color='blue')
axes[1].hist(prod_covariate['income'], bins=30, alpha=0.7, label='Production', color='red')
axes[1].set_xlabel('Income')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Covariate Shift: Income Distribution\n(Training vs Production)')
axes[1].legend()

# Plot 3: Relationship P(Y|X) ยังคงเดิม
axes[2].scatter(train_covariate['age'], train_covariate['income'], 
                c=train_covariate['purchase'], alpha=0.3, cmap='coolwarm', label='Training')
axes[2].set_xlabel('Age')
axes[2].set_ylabel('Income')
axes[2].set_title('P(Y|X) Relationship\n(Decision boundary ยังคงเดิม)')

plt.tight_layout()
plt.savefig('covariate_shift_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 สังเกต: Distribution ของ Age และ Income เปลี่ยนไป แต่ความสัมพันธ์ในการตัดสินใจซื้อยังเหมือนเดิม")

# %% [markdown]
# ## ส่วนที่ 3: ทำความเข้าใจ Concept Drift
#
# ### ทฤษฎี Concept Drift:
# - เกิดขึ้นเมื่อความสัมพันธ์ระหว่าง input และ output เปลี่ยนแปลง
# - ตัวอย่าง: พฤติกรรมการซื้อของลูกค้าเปลี่ยนหลัง COVID-19
# - แม้ input distribution จะเหมือนเดิม แต่ output เปลี่ยน
#
# สูตรทางคณิตศาสตร์:
# - P(X) อาจคงที่หรือเปลี่ยนก็ได้
# - แต่: P(Y|X) เปลี่ยนแปลง

# %%
def generate_concept_drift_data():
    """
    สร้างข้อมูลที่แสดง Concept Drift
    
    ในตัวอย่างนี้:
    - Training data: ลูกค้าซื้อเมื่อ income สูงกว่า threshold
    - Production data: threshold เปลี่ยน (พฤติกรรมเปลี่ยน)
    """
    
    np.random.seed(42)
    n_samples = 1000
    
    # Training data
    age_train = np.random.normal(35, 10, n_samples)
    income_train = np.random.normal(50000, 15000, n_samples)
    
    # กฎการซื้อเดิม: ซื้อถ้า income > 45000
    purchase_train = (income_train > 45000).astype(int)
    
    train_df = pd.DataFrame({
        'age': age_train,
        'income': income_train,
        'purchase': purchase_train
    })
    
    # Production data: distribution เหมือนเดิม
    age_prod = np.random.normal(35, 10, n_samples)
    income_prod = np.random.normal(50000, 15000, n_samples)
    
    # กฎการซื้อเปลี่ยน: ซื้อถ้า income > 55000 (Concept Drift!)
    # อาจเกิดจากเศรษฐกิจตกต่ำ ลูกค้าต้องการรายได้สูงขึ้นถึงจะซื้อ
    purchase_prod = (income_prod > 55000).astype(int)
    
    prod_df = pd.DataFrame({
        'age': age_prod,
        'income': income_prod,
        'purchase': purchase_prod
    })
    
    return train_df, prod_df

# สร้างข้อมูล
train_concept, prod_concept = generate_concept_drift_data()

print("📊 Training Data Summary:")
print(f"Purchase Rate: {train_concept['purchase'].mean():.2%}")
print(train_concept.describe())

print("\n📊 Production Data Summary:")
print(f"Purchase Rate: {prod_concept['purchase'].mean():.2%}")
print(prod_concept.describe())

# %%
# Visualize Concept Drift
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Plot 1: Income Distribution (เหมือนกัน)
axes[0].hist(train_concept['income'], bins=30, alpha=0.7, label='Training', color='blue')
axes[0].hist(prod_concept['income'], bins=30, alpha=0.7, label='Production', color='red')
axes[0].set_xlabel('Income')
axes[0].set_ylabel('Frequency')
axes[0].set_title('No Covariate Shift: Income Distribution\n(Training ≈ Production)')
axes[0].legend()

# Plot 2: Purchase Rate by Income Bin
income_bins = np.linspace(20000, 80000, 10)

train_purchase_rate = []
prod_purchase_rate = []
bin_centers = []

for i in range(len(income_bins)-1):
    mask_train = (train_concept['income'] >= income_bins[i]) & (train_concept['income'] < income_bins[i+1])
    mask_prod = (prod_concept['income'] >= income_bins[i]) & (prod_concept['income'] < income_bins[i+1])
    
    if mask_train.sum() > 0:
        train_purchase_rate.append(train_concept[mask_train]['purchase'].mean())
    else:
        train_purchase_rate.append(0)
        
    if mask_prod.sum() > 0:
        prod_purchase_rate.append(prod_concept[mask_prod]['purchase'].mean())
    else:
        prod_purchase_rate.append(0)
    
    bin_centers.append((income_bins[i] + income_bins[i+1]) / 2)

axes[1].plot(bin_centers, train_purchase_rate, 'b-o', label='Training P(Y|X)', linewidth=2)
axes[1].plot(bin_centers, prod_purchase_rate, 'r-o', label='Production P(Y|X)', linewidth=2)
axes[1].set_xlabel('Income')
axes[1].set_ylabel('Purchase Probability')
axes[1].set_title('Concept Drift: P(Y|X) Changed!\n(Decision boundary moved)')
axes[1].legend()
axes[1].axhline(0.5, color='gray', linestyle='--', alpha=0.5)

# Plot 3: Decision Boundary Comparison
axes[2].scatter(train_concept['income'], train_concept['purchase'] + np.random.normal(0, 0.05, len(train_concept)), 
                alpha=0.3, color='blue', label='Training')
axes[2].scatter(prod_concept['income'], prod_concept['purchase'] + np.random.normal(0, 0.05, len(prod_concept)), 
                alpha=0.3, color='red', label='Production')
axes[2].axvline(45000, color='blue', linestyle='--', linewidth=2, label='Train Threshold (45k)')
axes[2].axvline(55000, color='red', linestyle='--', linewidth=2, label='Prod Threshold (55k)')
axes[2].set_xlabel('Income')
axes[2].set_ylabel('Purchase (with jitter)')
axes[2].set_title('Concept Drift Visualization\n(Threshold shifted from 45k to 55k)')
axes[2].legend()

plt.tight_layout()
plt.savefig('concept_drift_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 สังเกต: Distribution ของ Income เหมือนเดิม แต่ความสัมพันธ์กับ Purchase เปลี่ยนไป!")
print("   - Training: ซื้อเมื่อ income > 45,000")
print("   - Production: ซื้อเมื่อ income > 55,000")

# %% [markdown]
# ## ส่วนที่ 4: Statistical Tests สำหรับ Drift Detection
#
# ### 4.1 Kolmogorov-Smirnov (KS) Test
#
# **ทฤษฎี:**
# - เปรียบเทียบ cumulative distribution function (CDF) ของ 2 samples
# - วัดความแตกต่างสูงสุดระหว่าง 2 CDFs
# - ข้อดี: ไม่ต้องสมมติ distribution, sensitive ต่อการเปลี่ยนแปลง
# - ข้อเสีย: ใช้ได้กับ continuous variables เท่านั้น
#
# **การตีความ:**
# - KS Statistic: 0-1 (ยิ่งสูง = ยิ่งต่าง)
# - p-value < 0.05: reject null hypothesis → มี drift

# %%
def kolmogorov_smirnov_test(data1, data2, feature_name="feature"):
    """
    ทำ KS Test เพื่อตรวจจับ drift
    
    Parameters:
    -----------
    data1 : array-like - ข้อมูลชุดแรก (reference/training)
    data2 : array-like - ข้อมูลชุดที่สอง (current/production)
    feature_name : str - ชื่อ feature
    
    Returns:
    --------
    dict : ผลลัพธ์ของ KS test
    """
    statistic, p_value = stats.ks_2samp(data1, data2)
    
    # กำหนด threshold สำหรับ drift
    drift_detected = p_value < 0.05
    
    result = {
        'feature': feature_name,
        'test': 'Kolmogorov-Smirnov',
        'statistic': statistic,
        'p_value': p_value,
        'drift_detected': drift_detected,
        'interpretation': 'DRIFT DETECTED!' if drift_detected else 'No significant drift'
    }
    
    return result

# ทดสอบ KS Test กับข้อมูล Covariate Shift
print("=" * 60)
print("🔍 KS Test Results for Covariate Shift Data")
print("=" * 60)

ks_age = kolmogorov_smirnov_test(train_covariate['age'], prod_covariate['age'], 'age')
ks_income = kolmogorov_smirnov_test(train_covariate['income'], prod_covariate['income'], 'income')

for result in [ks_age, ks_income]:
    print(f"\nFeature: {result['feature']}")
    print(f"  KS Statistic: {result['statistic']:.4f}")
    print(f"  P-value: {result['p_value']:.6f}")
    print(f"  Result: {result['interpretation']}")

# %%
# Visualize KS Test
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for idx, (feature, ax) in enumerate(zip(['age', 'income'], axes)):
    # คำนวณ CDF
    sorted_train = np.sort(train_covariate[feature])
    sorted_prod = np.sort(prod_covariate[feature])
    
    cdf_train = np.arange(1, len(sorted_train) + 1) / len(sorted_train)
    cdf_prod = np.arange(1, len(sorted_prod) + 1) / len(sorted_prod)
    
    ax.plot(sorted_train, cdf_train, 'b-', linewidth=2, label='Training CDF')
    ax.plot(sorted_prod, cdf_prod, 'r-', linewidth=2, label='Production CDF')
    
    # แสดง KS statistic (maximum distance)
    ks_result = kolmogorov_smirnov_test(train_covariate[feature], prod_covariate[feature], feature)
    
    ax.set_xlabel(feature.capitalize())
    ax.set_ylabel('Cumulative Probability')
    ax.set_title(f'KS Test: {feature.capitalize()}\nKS Statistic = {ks_result["statistic"]:.4f}, p-value = {ks_result["p_value"]:.4f}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ks_test_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ### 4.2 Population Stability Index (PSI)
#
# **ทฤษฎี:**
# - วัดการเปลี่ยนแปลงของ distribution โดยเปรียบเทียบ proportions ในแต่ละ bin
# - นิยมใช้ใน credit scoring และ financial models
# - สูตร: PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)
#
# **การตีความ PSI:**
# - PSI < 0.1: ไม่มีการเปลี่ยนแปลงที่สำคัญ
# - 0.1 ≤ PSI < 0.25: มีการเปลี่ยนแปลงปานกลาง ควรตรวจสอบ
# - PSI ≥ 0.25: มีการเปลี่ยนแปลงมาก ต้องดำเนินการ

# %%
def calculate_psi(expected, actual, bins=10, eps=1e-6):
    """
    คำนวณ Population Stability Index (PSI)
    
    Parameters:
    -----------
    expected : array-like - ข้อมูล reference (training)
    actual : array-like - ข้อมูล current (production)
    bins : int - จำนวน bins สำหรับ discretize
    eps : float - ค่าเล็กๆ เพื่อป้องกัน division by zero
    
    Returns:
    --------
    float : ค่า PSI
    dict : รายละเอียดการคำนวณ
    """
    # สร้าง bins จาก expected data
    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
    breakpoints = np.unique(breakpoints)  # ลบ duplicates
    
    # นับจำนวนในแต่ละ bin
    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)
    
    # คำนวณ proportions
    expected_props = expected_counts / len(expected) + eps
    actual_props = actual_counts / len(actual) + eps
    
    # คำนวณ PSI
    psi_values = (actual_props - expected_props) * np.log(actual_props / expected_props)
    psi = np.sum(psi_values)
    
    # ตีความผลลัพธ์
    if psi < 0.1:
        interpretation = "No significant change (PSI < 0.1)"
        severity = "LOW"
    elif psi < 0.25:
        interpretation = "Moderate change - monitor closely (0.1 ≤ PSI < 0.25)"
        severity = "MEDIUM"
    else:
        interpretation = "Significant change - action required (PSI ≥ 0.25)"
        severity = "HIGH"
    
    return {
        'psi': psi,
        'interpretation': interpretation,
        'severity': severity,
        'bin_psi_values': psi_values,
        'expected_props': expected_props,
        'actual_props': actual_props,
        'breakpoints': breakpoints
    }

# คำนวณ PSI สำหรับแต่ละ feature
print("=" * 60)
print("📊 PSI Results for Covariate Shift Data")
print("=" * 60)

for feature in ['age', 'income']:
    psi_result = calculate_psi(train_covariate[feature], prod_covariate[feature])
    print(f"\nFeature: {feature}")
    print(f"  PSI Value: {psi_result['psi']:.4f}")
    print(f"  Severity: {psi_result['severity']}")
    print(f"  Interpretation: {psi_result['interpretation']}")

# %%
# Visualize PSI
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for idx, feature in enumerate(['age', 'income']):
    psi_result = calculate_psi(train_covariate[feature], prod_covariate[feature])
    
    x = np.arange(len(psi_result['expected_props']))
    width = 0.35
    
    axes[idx].bar(x - width/2, psi_result['expected_props'], width, label='Expected (Train)', color='blue', alpha=0.7)
    axes[idx].bar(x + width/2, psi_result['actual_props'], width, label='Actual (Prod)', color='red', alpha=0.7)
    
    axes[idx].set_xlabel('Bin')
    axes[idx].set_ylabel('Proportion')
    axes[idx].set_title(f'PSI Analysis: {feature.capitalize()}\nPSI = {psi_result["psi"]:.4f} ({psi_result["severity"]})')
    axes[idx].legend()
    axes[idx].set_xticks(x)

plt.tight_layout()
plt.savefig('psi_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ### 4.3 Wasserstein Distance (Earth Mover's Distance)
#
# **ทฤษฎี:**
# - วัด "งาน" ที่ต้องใช้ในการเปลี่ยน distribution หนึ่งไปเป็นอีก distribution
# - เหมือนการคำนวณต้นทุนในการขนย้ายดิน (Earth Mover)
# - ข้อดี: คำนึงถึง distance ระหว่าง bins, sensitive ต่อ shift ในตำแหน่ง
# - ข้อเสีย: ต้อง normalize ข้อมูลเพื่อให้เปรียบเทียบได้

# %%
def wasserstein_distance_test(data1, data2, feature_name="feature"):
    """
    คำนวณ Wasserstein Distance สำหรับ drift detection
    
    Parameters:
    -----------
    data1 : array-like - ข้อมูลชุดแรก (reference)
    data2 : array-like - ข้อมูลชุดที่สอง (current)
    feature_name : str - ชื่อ feature
    
    Returns:
    --------
    dict : ผลลัพธ์ของ Wasserstein distance
    """
    # คำนวณ Wasserstein distance
    distance = stats.wasserstein_distance(data1, data2)
    
    # Normalize โดยใช้ standard deviation ของ reference data
    std_ref = np.std(data1)
    normalized_distance = distance / std_ref if std_ref > 0 else distance
    
    # กำหนด threshold (ปรับได้ตาม domain)
    if normalized_distance < 0.1:
        severity = "LOW"
        interpretation = "No significant drift"
    elif normalized_distance < 0.5:
        severity = "MEDIUM"
        interpretation = "Moderate drift detected"
    else:
        severity = "HIGH"
        interpretation = "Significant drift detected"
    
    return {
        'feature': feature_name,
        'distance': distance,
        'normalized_distance': normalized_distance,
        'severity': severity,
        'interpretation': interpretation
    }

# คำนวณ Wasserstein Distance
print("=" * 60)
print("📏 Wasserstein Distance Results for Covariate Shift Data")
print("=" * 60)

for feature in ['age', 'income']:
    wd_result = wasserstein_distance_test(train_covariate[feature], prod_covariate[feature], feature)
    print(f"\nFeature: {feature}")
    print(f"  Wasserstein Distance: {wd_result['distance']:.4f}")
    print(f"  Normalized Distance: {wd_result['normalized_distance']:.4f}")
    print(f"  Severity: {wd_result['severity']}")
    print(f"  Interpretation: {wd_result['interpretation']}")

# %%
# Visualize Wasserstein Distance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for idx, feature in enumerate(['age', 'income']):
    ax = axes[idx]
    
    # แสดง histogram และ KDE
    ax.hist(train_covariate[feature], bins=30, alpha=0.5, density=True, label='Training', color='blue')
    ax.hist(prod_covariate[feature], bins=30, alpha=0.5, density=True, label='Production', color='red')
    
    # คำนวณ Wasserstein distance
    wd_result = wasserstein_distance_test(train_covariate[feature], prod_covariate[feature], feature)
    
    # แสดง mean และ "การขนย้าย"
    mean_train = train_covariate[feature].mean()
    mean_prod = prod_covariate[feature].mean()
    
    ax.axvline(mean_train, color='blue', linestyle='--', linewidth=2, label=f'Train Mean: {mean_train:.1f}')
    ax.axvline(mean_prod, color='red', linestyle='--', linewidth=2, label=f'Prod Mean: {mean_prod:.1f}')
    
    # แสดง arrow สำหรับ "earth moving"
    ax.annotate('', xy=(mean_prod, 0.01), xytext=(mean_train, 0.01),
                arrowprops=dict(arrowstyle='->', color='green', lw=3))
    
    ax.set_xlabel(feature.capitalize())
    ax.set_ylabel('Density')
    ax.set_title(f'Wasserstein Distance: {feature.capitalize()}\nDistance = {wd_result["distance"]:.2f} ({wd_result["severity"]})')
    ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('wasserstein_visualization.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 ลูกศรสีเขียวแสดงทิศทางของ 'การขนย้าย' จาก Training ไป Production")

# %% [markdown]
# ## ส่วนที่ 5: เปรียบเทียบและเลือก Drift Detection Method
#
# ### สรุปข้อดี-ข้อเสียของแต่ละ method:
#
# | Method | ข้อดี | ข้อเสีย | ใช้เมื่อ |
# |--------|-------|---------|---------|
# | KS Test | ไม่สมมติ distribution, sensitive | ใช้กับ continuous เท่านั้น | ต้องการ statistical significance |
# | PSI | มี threshold ชัดเจน, industry standard | ต้อง binning | Credit scoring, Risk models |
# | Wasserstein | คำนึงถึง distance, เข้าใจง่าย | ต้อง normalize | เปรียบเทียบ shift ในตำแหน่ง |

# %%
def comprehensive_drift_analysis(reference_data, current_data, feature_name):
    """
    วิเคราะห์ drift โดยใช้ทุก methods และเปรียบเทียบผลลัพธ์
    """
    results = {
        'feature': feature_name,
        'ks': kolmogorov_smirnov_test(reference_data, current_data, feature_name),
        'psi': calculate_psi(reference_data, current_data),
        'wasserstein': wasserstein_distance_test(reference_data, current_data, feature_name)
    }
    
    # สรุปผล
    drift_votes = 0
    if results['ks']['drift_detected']:
        drift_votes += 1
    if results['psi']['severity'] in ['MEDIUM', 'HIGH']:
        drift_votes += 1
    if results['wasserstein']['severity'] in ['MEDIUM', 'HIGH']:
        drift_votes += 1
    
    results['consensus'] = 'DRIFT' if drift_votes >= 2 else 'NO DRIFT'
    results['drift_votes'] = drift_votes
    
    return results

# เปรียบเทียบผลลัพธ์
print("=" * 80)
print("📊 COMPREHENSIVE DRIFT ANALYSIS COMPARISON")
print("=" * 80)

comparison_results = []

for feature in ['age', 'income']:
    result = comprehensive_drift_analysis(
        train_covariate[feature], 
        prod_covariate[feature], 
        feature
    )
    comparison_results.append(result)
    
    print(f"\n🔍 Feature: {feature.upper()}")
    print("-" * 40)
    print(f"  KS Test: stat={result['ks']['statistic']:.4f}, p={result['ks']['p_value']:.4f} → {result['ks']['interpretation']}")
    print(f"  PSI: {result['psi']['psi']:.4f} → {result['psi']['severity']}")
    print(f"  Wasserstein: {result['wasserstein']['normalized_distance']:.4f} → {result['wasserstein']['severity']}")
    print(f"  📋 CONSENSUS ({result['drift_votes']}/3 votes): {result['consensus']}")

# %%
# สร้าง comparison table
comparison_df = pd.DataFrame([
    {
        'Feature': r['feature'],
        'KS Statistic': f"{r['ks']['statistic']:.4f}",
        'KS p-value': f"{r['ks']['p_value']:.4f}",
        'KS Drift': '✓' if r['ks']['drift_detected'] else '✗',
        'PSI': f"{r['psi']['psi']:.4f}",
        'PSI Severity': r['psi']['severity'],
        'Wasserstein': f"{r['wasserstein']['normalized_distance']:.4f}",
        'WD Severity': r['wasserstein']['severity'],
        'Consensus': r['consensus']
    }
    for r in comparison_results
])

print("\n" + "=" * 80)
print("📊 SUMMARY TABLE")
print("=" * 80)
print(comparison_df.to_string(index=False))

# %% [markdown]
# ## ส่วนที่ 6: แนวทางการเลือก Drift Detection Method
#
# ### Decision Tree สำหรับเลือก Method:
#
# ```
# 1. Data Type?
#    ├── Continuous → ไปข้อ 2
#    └── Categorical → ใช้ Chi-squared test หรือ PSI
#
# 2. ต้องการ Statistical Significance?
#    ├── ใช่ → KS Test หรือ Chi-squared
#    └── ไม่จำเป็น → PSI หรือ Wasserstein
#
# 3. Industry Requirement?
#    ├── Finance/Credit → PSI (มี regulatory standards)
#    └── อื่นๆ → เลือกตามความเหมาะสม
#
# 4. ต้องการความ sensitive สูง?
#    ├── ใช่ → Wasserstein (detect small shifts)
#    └── ปกติ → KS หรือ PSI
# ```

# %%
def recommend_drift_method(data_type, needs_significance, industry, high_sensitivity):
    """
    แนะนำ drift detection method ที่เหมาะสม
    
    Parameters:
    -----------
    data_type : str - 'continuous' หรือ 'categorical'
    needs_significance : bool - ต้องการ statistical significance หรือไม่
    industry : str - 'finance', 'healthcare', 'general'
    high_sensitivity : bool - ต้องการ sensitivity สูงหรือไม่
    
    Returns:
    --------
    str : recommended method พร้อมเหตุผล
    """
    recommendations = []
    
    if data_type == 'categorical':
        recommendations.append({
            'method': 'Chi-squared Test',
            'reason': 'เหมาะกับ categorical data',
            'priority': 1
        })
        recommendations.append({
            'method': 'PSI (binned)',
            'reason': 'สามารถใช้กับ categorical ได้โดยใช้ category เป็น bins',
            'priority': 2
        })
    else:  # continuous
        if industry == 'finance':
            recommendations.append({
                'method': 'PSI',
                'reason': 'Industry standard ใน finance, มี regulatory requirements',
                'priority': 1
            })
        
        if needs_significance:
            recommendations.append({
                'method': 'KS Test',
                'reason': 'ให้ p-value สำหรับ statistical significance',
                'priority': 1 if industry != 'finance' else 2
            })
        
        if high_sensitivity:
            recommendations.append({
                'method': 'Wasserstein Distance',
                'reason': 'Sensitive ต่อ small shifts และ location changes',
                'priority': 2
            })
        
        # Default recommendation
        if not recommendations:
            recommendations.append({
                'method': 'PSI + KS Test',
                'reason': 'ใช้ทั้งสองเพื่อ cross-validate',
                'priority': 1
            })
    
    # เรียงตาม priority
    recommendations.sort(key=lambda x: x['priority'])
    
    return recommendations

# ตัวอย่างการใช้งาน
print("=" * 60)
print("🎯 DRIFT METHOD RECOMMENDATION EXAMPLES")
print("=" * 60)

scenarios = [
    {'data_type': 'continuous', 'needs_significance': True, 'industry': 'finance', 'high_sensitivity': False},
    {'data_type': 'continuous', 'needs_significance': False, 'industry': 'general', 'high_sensitivity': True},
    {'data_type': 'categorical', 'needs_significance': True, 'industry': 'healthcare', 'high_sensitivity': False},
]

for i, scenario in enumerate(scenarios, 1):
    print(f"\n📋 Scenario {i}:")
    print(f"   Data Type: {scenario['data_type']}")
    print(f"   Needs Significance: {scenario['needs_significance']}")
    print(f"   Industry: {scenario['industry']}")
    print(f"   High Sensitivity: {scenario['high_sensitivity']}")
    
    recs = recommend_drift_method(**scenario)
    print("   Recommendations:")
    for j, rec in enumerate(recs, 1):
        print(f"   {j}. {rec['method']} - {rec['reason']}")

# %% [markdown]
# ## สรุป LAB 1
#
# ### สิ่งที่เรียนรู้:
# 1. **Covariate Shift**: P(X) เปลี่ยน แต่ P(Y|X) คงที่
# 2. **Concept Drift**: P(Y|X) เปลี่ยน (relationship เปลี่ยน)
# 3. **KS Test**: วัด maximum distance ระหว่าง CDFs, ให้ p-value
# 4. **PSI**: วัดการเปลี่ยนแปลงของ proportions, มี threshold ชัดเจน
# 5. **Wasserstein**: วัด "งาน" ในการเปลี่ยน distribution
#
# ### Best Practices:
# - ใช้หลาย methods เพื่อ cross-validate
# - เลือก method ตาม data type และ business requirements
# - ตั้ง threshold ที่เหมาะสมกับ context

# %%
print("=" * 60)
print("✅ LAB 1 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Covariate Shift vs Concept Drift - เข้าใจความแตกต่าง
2. KS Test - ใช้เมื่อต้องการ statistical significance
3. PSI - Industry standard สำหรับ finance
4. Wasserstein - Sensitive ต่อ location shifts

🔜 Next: LAB 2 - Feature Drift Detection
""")

## LAB 2: Feature Drift Detection


# %% [markdown]
# # LAB 2: Feature Drift Detection
# ## การตรวจจับ Drift ในแต่ละ Feature
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. ตรวจจับ drift ในแต่ละ feature อย่างเป็นระบบ
# 2. วิเคราะห์ numerical vs categorical feature drift
# 3. สร้าง visualization สำหรับ feature distributions over time
#
# ### ทฤษฎี:
# การตรวจจับ drift ในแต่ละ feature มีความสำคัญเพราะ:
# - ช่วยระบุ root cause ของ model performance degradation
# - ทำให้เข้าใจว่า feature ไหนเปลี่ยนแปลงมากที่สุด
# - สามารถ prioritize การแก้ไขได้

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
plt.rcParams['figure.figsize'] = (14, 8)

print("✅ Libraries imported successfully!")

# %% [markdown]
# ## ส่วนที่ 2: สร้าง Dataset ที่มีหลาย Features
#
# เราจะสร้าง dataset ที่จำลองสถานการณ์จริง:
# - มีทั้ง numerical และ categorical features
# - บาง features มี drift บาง features ไม่มี
# - มี drift ในระดับต่างๆ

# %%
def create_multi_feature_dataset(n_samples=2000, drift_level='mixed'):
    """
    สร้าง dataset ที่มีหลาย features พร้อม simulated drift
    
    Parameters:
    -----------
    n_samples : int - จำนวน samples ต่อ dataset
    drift_level : str - 'none', 'mild', 'severe', 'mixed'
    
    Returns:
    --------
    tuple : (reference_df, current_df, feature_info)
    """
    
    np.random.seed(42)
    
    # === Reference Data (Training) ===
    reference_data = {
        # Numerical Features
        'age': np.random.normal(35, 10, n_samples),
        'income': np.random.normal(50000, 15000, n_samples),
        'credit_score': np.random.normal(650, 80, n_samples),
        'account_balance': np.random.exponential(10000, n_samples),
        'transaction_count': np.random.poisson(20, n_samples),
        
        # Categorical Features (encoded as integers)
        'region': np.random.choice([0, 1, 2, 3], n_samples, p=[0.3, 0.3, 0.25, 0.15]),
        'customer_type': np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.35, 0.15]),
        'product_category': np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.2, 0.2, 0.2, 0.2, 0.2])
    }
    
    # === Current Data (Production) with various drift levels ===
    if drift_level == 'none':
        current_data = {k: v.copy() for k, v in reference_data.items()}
        # เพิ่ม random noise เล็กน้อย
        for key in ['age', 'income', 'credit_score']:
            current_data[key] = np.random.normal(
                reference_data[key].mean(),
                reference_data[key].std(),
                n_samples
            )
    
    elif drift_level == 'mixed':
        current_data = {
            # No drift
            'age': np.random.normal(35, 10, n_samples),  # เหมือนเดิม
            'credit_score': np.random.normal(650, 80, n_samples),  # เหมือนเดิม
            
            # Mild drift
            'income': np.random.normal(55000, 15000, n_samples),  # mean shift เล็กน้อย
            'transaction_count': np.random.poisson(25, n_samples),  # เพิ่มขึ้นเล็กน้อย
            
            # Severe drift
            'account_balance': np.random.exponential(20000, n_samples),  # scale เปลี่ยนมาก
            
            # Categorical drift
            'region': np.random.choice([0, 1, 2, 3], n_samples, p=[0.15, 0.15, 0.35, 0.35]),  # distribution เปลี่ยน
            'customer_type': np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.35, 0.15]),  # เหมือนเดิม
            'product_category': np.random.choice([0, 1, 2, 3, 4], n_samples, p=[0.4, 0.1, 0.1, 0.2, 0.2])  # เปลี่ยนบ้าง
        }
    
    reference_df = pd.DataFrame(reference_data)
    current_df = pd.DataFrame(current_data)
    
    # Feature info
    feature_info = {
        'numerical': ['age', 'income', 'credit_score', 'account_balance', 'transaction_count'],
        'categorical': ['region', 'customer_type', 'product_category'],
        'expected_drift': {
            'age': 'none',
            'income': 'mild',
            'credit_score': 'none',
            'account_balance': 'severe',
            'transaction_count': 'mild',
            'region': 'severe',
            'customer_type': 'none',
            'product_category': 'mild'
        }
    }
    
    return reference_df, current_df, feature_info

# สร้าง dataset
reference_df, current_df, feature_info = create_multi_feature_dataset(drift_level='mixed')

print("📊 Reference Data Shape:", reference_df.shape)
print("📊 Current Data Shape:", current_df.shape)
print("\n📋 Feature Types:")
print(f"  Numerical: {feature_info['numerical']}")
print(f"  Categorical: {feature_info['categorical']}")

print("\n📋 Expected Drift Levels:")
for feature, level in feature_info['expected_drift'].items():
    print(f"  {feature}: {level}")

# %%
# แสดง summary statistics
print("\n" + "=" * 60)
print("REFERENCE DATA SUMMARY")
print("=" * 60)
print(reference_df.describe())

print("\n" + "=" * 60)
print("CURRENT DATA SUMMARY")
print("=" * 60)
print(current_df.describe())

# %% [markdown]
# ## ส่วนที่ 3: สร้าง Feature Drift Detector Class
#
# เราจะสร้าง class ที่รวมทุก drift detection methods เพื่อใช้งานได้สะดวก

# %%
class FeatureDriftDetector:
    """
    Class สำหรับตรวจจับ drift ในแต่ละ feature
    
    รองรับทั้ง numerical และ categorical features
    ใช้หลาย statistical tests เพื่อ comprehensive analysis
    """
    
    def __init__(self, reference_data, current_data, numerical_features=None, categorical_features=None):
        """
        Initialize detector
        
        Parameters:
        -----------
        reference_data : pd.DataFrame - ข้อมูล reference (training)
        current_data : pd.DataFrame - ข้อมูล current (production)
        numerical_features : list - รายชื่อ numerical features
        categorical_features : list - รายชื่อ categorical features
        """
        self.reference = reference_data
        self.current = current_data
        
        # Auto-detect feature types if not provided
        if numerical_features is None:
            self.numerical_features = reference_data.select_dtypes(include=[np.number]).columns.tolist()
        else:
            self.numerical_features = numerical_features
            
        if categorical_features is None:
            self.categorical_features = []
        else:
            self.categorical_features = categorical_features
        
        self.results = {}
    
    def ks_test(self, feature):
        """Kolmogorov-Smirnov test สำหรับ numerical features"""
        stat, p_value = stats.ks_2samp(
            self.reference[feature].dropna(),
            self.current[feature].dropna()
        )
        return {'statistic': stat, 'p_value': p_value}
    
    def calculate_psi(self, feature, bins=10):
        """Population Stability Index"""
        ref_data = self.reference[feature].dropna()
        cur_data = self.current[feature].dropna()
        
        # สร้าง bins
        breakpoints = np.percentile(ref_data, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        ref_counts, _ = np.histogram(ref_data, bins=breakpoints)
        cur_counts, _ = np.histogram(cur_data, bins=breakpoints)
        
        # คำนวณ proportions
        eps = 1e-6
        ref_props = ref_counts / len(ref_data) + eps
        cur_props = cur_counts / len(cur_data) + eps
        
        # คำนวณ PSI
        psi = np.sum((cur_props - ref_props) * np.log(cur_props / ref_props))
        
        return {'psi': psi}
    
    def wasserstein_test(self, feature):
        """Wasserstein Distance"""
        ref_data = self.reference[feature].dropna()
        cur_data = self.current[feature].dropna()
        
        distance = stats.wasserstein_distance(ref_data, cur_data)
        
        # Normalize by std of reference
        std = ref_data.std()
        normalized = distance / std if std > 0 else distance
        
        return {'distance': distance, 'normalized_distance': normalized}
    
    def chi_squared_test(self, feature):
        """Chi-squared test สำหรับ categorical features"""
        # นับ frequency ของแต่ละ category
        ref_counts = self.reference[feature].value_counts()
        cur_counts = self.current[feature].value_counts()
        
        # รวม categories ให้เท่ากัน
        all_categories = set(ref_counts.index) | set(cur_counts.index)
        ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
        cur_freq = [cur_counts.get(cat, 0) for cat in all_categories]
        
        # Normalize to expected frequencies
        total_ref = sum(ref_freq)
        total_cur = sum(cur_freq)
        expected = [(r / total_ref) * total_cur for r in ref_freq]
        
        # Chi-squared test
        try:
            stat, p_value = stats.chisquare(cur_freq, expected)
        except:
            stat, p_value = 0, 1.0
        
        return {'statistic': stat, 'p_value': p_value}
    
    def analyze_numerical_feature(self, feature):
        """วิเคราะห์ drift สำหรับ numerical feature"""
        results = {
            'feature': feature,
            'type': 'numerical',
            'ks_test': self.ks_test(feature),
            'psi': self.calculate_psi(feature),
            'wasserstein': self.wasserstein_test(feature)
        }
        
        # สรุปผล
        ks_drift = results['ks_test']['p_value'] < 0.05
        psi_value = results['psi']['psi']
        
        if psi_value < 0.1:
            psi_severity = 'none'
        elif psi_value < 0.25:
            psi_severity = 'mild'
        else:
            psi_severity = 'severe'
        
        results['drift_detected'] = ks_drift or psi_severity != 'none'
        results['severity'] = psi_severity
        
        return results
    
    def analyze_categorical_feature(self, feature):
        """วิเคราะห์ drift สำหรับ categorical feature"""
        chi2_result = self.chi_squared_test(feature)
        
        # คำนวณ PSI สำหรับ categorical
        ref_props = self.reference[feature].value_counts(normalize=True)
        cur_props = self.current[feature].value_counts(normalize=True)
        
        all_cats = set(ref_props.index) | set(cur_props.index)
        eps = 1e-6
        psi = 0
        for cat in all_cats:
            ref_p = ref_props.get(cat, 0) + eps
            cur_p = cur_props.get(cat, 0) + eps
            psi += (cur_p - ref_p) * np.log(cur_p / ref_p)
        
        results = {
            'feature': feature,
            'type': 'categorical',
            'chi_squared': chi2_result,
            'psi': {'psi': psi}
        }
        
        # สรุปผล
        chi2_drift = chi2_result['p_value'] < 0.05
        
        if psi < 0.1:
            psi_severity = 'none'
        elif psi < 0.25:
            psi_severity = 'mild'
        else:
            psi_severity = 'severe'
        
        results['drift_detected'] = chi2_drift or psi_severity != 'none'
        results['severity'] = psi_severity
        
        return results
    
    def analyze_all_features(self):
        """วิเคราะห์ drift สำหรับทุก features"""
        all_results = {}
        
        # Numerical features
        for feature in self.numerical_features:
            all_results[feature] = self.analyze_numerical_feature(feature)
        
        # Categorical features
        for feature in self.categorical_features:
            all_results[feature] = self.analyze_categorical_feature(feature)
        
        self.results = all_results
        return all_results
    
    def get_summary_report(self):
        """สร้าง summary report"""
        if not self.results:
            self.analyze_all_features()
        
        summary = []
        for feature, result in self.results.items():
            row = {
                'Feature': feature,
                'Type': result['type'],
                'Drift Detected': '✓' if result['drift_detected'] else '✗',
                'Severity': result['severity'].upper(),
                'PSI': f"{result['psi']['psi']:.4f}"
            }
            
            if result['type'] == 'numerical':
                row['KS p-value'] = f"{result['ks_test']['p_value']:.4f}"
            else:
                row['Chi2 p-value'] = f"{result['chi_squared']['p_value']:.4f}"
            
            summary.append(row)
        
        return pd.DataFrame(summary)

# %%
# ใช้งาน FeatureDriftDetector
detector = FeatureDriftDetector(
    reference_data=reference_df,
    current_data=current_df,
    numerical_features=feature_info['numerical'],
    categorical_features=feature_info['categorical']
)

# วิเคราะห์ทุก features
all_results = detector.analyze_all_features()

# แสดง summary report
print("=" * 80)
print("📊 FEATURE DRIFT DETECTION REPORT")
print("=" * 80)
summary_df = detector.get_summary_report()
print(summary_df.to_string(index=False))

# %% [markdown]
# ## ส่วนที่ 4: Visualize Feature Distributions
#
# การ visualize ช่วยให้เข้าใจ drift ได้ดีขึ้น

# %%
def plot_numerical_feature_drift(reference, current, feature_name, ax=None):
    """
    สร้าง visualization สำหรับ numerical feature drift
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))
    
    # Histogram
    ax.hist(reference[feature_name], bins=30, alpha=0.5, label='Reference', color='blue', density=True)
    ax.hist(current[feature_name], bins=30, alpha=0.5, label='Current', color='red', density=True)
    
    # Statistics
    ref_mean = reference[feature_name].mean()
    cur_mean = current[feature_name].mean()
    
    ax.axvline(ref_mean, color='blue', linestyle='--', linewidth=2)
    ax.axvline(cur_mean, color='red', linestyle='--', linewidth=2)
    
    # Calculate PSI for title
    detector_temp = FeatureDriftDetector(reference, current, [feature_name], [])
    result = detector_temp.analyze_numerical_feature(feature_name)
    
    ax.set_title(f'{feature_name}\nPSI: {result["psi"]["psi"]:.4f} | Severity: {result["severity"].upper()}')
    ax.set_xlabel(feature_name)
    ax.set_ylabel('Density')
    ax.legend()
    
    return ax

def plot_categorical_feature_drift(reference, current, feature_name, ax=None):
    """
    สร้าง visualization สำหรับ categorical feature drift
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))
    
    # Calculate proportions
    ref_props = reference[feature_name].value_counts(normalize=True).sort_index()
    cur_props = current[feature_name].value_counts(normalize=True).sort_index()
    
    # Align categories
    all_cats = sorted(set(ref_props.index) | set(cur_props.index))
    ref_values = [ref_props.get(cat, 0) for cat in all_cats]
    cur_values = [cur_props.get(cat, 0) for cat in all_cats]
    
    x = np.arange(len(all_cats))
    width = 0.35
    
    ax.bar(x - width/2, ref_values, width, label='Reference', color='blue', alpha=0.7)
    ax.bar(x + width/2, cur_values, width, label='Current', color='red', alpha=0.7)
    
    ax.set_xticks(x)
    ax.set_xticklabels([f'Cat {c}' for c in all_cats])
    
    # Calculate PSI for title
    detector_temp = FeatureDriftDetector(reference, current, [], [feature_name])
    result = detector_temp.analyze_categorical_feature(feature_name)
    
    ax.set_title(f'{feature_name}\nPSI: {result["psi"]["psi"]:.4f} | Severity: {result["severity"].upper()}')
    ax.set_xlabel('Category')
    ax.set_ylabel('Proportion')
    ax.legend()
    
    return ax

# %%
# Plot all numerical features
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, feature in enumerate(feature_info['numerical']):
    plot_numerical_feature_drift(reference_df, current_df, feature, axes[idx])

# Remove empty subplot
if len(feature_info['numerical']) < 6:
    axes[-1].set_visible(False)

plt.suptitle('Numerical Features: Distribution Comparison\n(Reference vs Current)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('numerical_features_drift.png', dpi=150, bbox_inches='tight')
plt.show()

# %%
# Plot all categorical features
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for idx, feature in enumerate(feature_info['categorical']):
    plot_categorical_feature_drift(reference_df, current_df, feature, axes[idx])

plt.suptitle('Categorical Features: Distribution Comparison\n(Reference vs Current)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('categorical_features_drift.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 5: Feature Drift Ranking และ Prioritization
#
# จัดลำดับ features ตามความรุนแรงของ drift

# %%
def rank_features_by_drift(detector):
    """
    จัดลำดับ features ตาม drift severity
    """
    if not detector.results:
        detector.analyze_all_features()
    
    rankings = []
    for feature, result in detector.results.items():
        rankings.append({
            'feature': feature,
            'psi': result['psi']['psi'],
            'drift_detected': result['drift_detected'],
            'severity': result['severity'],
            'type': result['type']
        })
    
    # เรียงตาม PSI (มากไปน้อย)
    rankings.sort(key=lambda x: x['psi'], reverse=True)
    
    return rankings

# จัดลำดับ features
rankings = rank_features_by_drift(detector)

print("=" * 60)
print("📊 FEATURE DRIFT RANKING (Sorted by PSI)")
print("=" * 60)

for rank, item in enumerate(rankings, 1):
    severity_emoji = {'none': '🟢', 'mild': '🟡', 'severe': '🔴'}[item['severity']]
    print(f"{rank}. {item['feature']:<20} | PSI: {item['psi']:.4f} | {severity_emoji} {item['severity'].upper()}")

# %%
# สร้าง Drift Ranking Visualization
fig, ax = plt.subplots(figsize=(12, 6))

features = [r['feature'] for r in rankings]
psi_values = [r['psi'] for r in rankings]
colors = ['red' if r['severity'] == 'severe' else 'orange' if r['severity'] == 'mild' else 'green' for r in rankings]

bars = ax.barh(features, psi_values, color=colors, alpha=0.7, edgecolor='black')

# Add threshold lines
ax.axvline(0.1, color='orange', linestyle='--', label='Mild Threshold (0.1)')
ax.axvline(0.25, color='red', linestyle='--', label='Severe Threshold (0.25)')

ax.set_xlabel('PSI Value')
ax.set_ylabel('Feature')
ax.set_title('Feature Drift Ranking by PSI\n(Red=Severe, Orange=Mild, Green=None)')
ax.legend()

# Add value labels
for bar, psi in zip(bars, psi_values):
    ax.text(psi + 0.01, bar.get_y() + bar.get_height()/2, f'{psi:.3f}', va='center')

plt.tight_layout()
plt.savefig('feature_drift_ranking.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 6: Time-based Distribution Analysis
#
# วิเคราะห์ว่า distribution เปลี่ยนแปลงอย่างไรเมื่อเวลาผ่านไป

# %%
def simulate_time_series_data(n_periods=6, samples_per_period=500):
    """
    จำลองข้อมูลที่เปลี่ยนแปลงตามเวลา
    """
    all_data = []
    
    for period in range(n_periods):
        np.random.seed(42 + period)
        
        # Gradual drift: mean เพิ่มขึ้นทีละน้อย
        age_mean = 35 + period * 2  # drift ใน age
        income_mean = 50000  # ไม่มี drift
        
        data = pd.DataFrame({
            'period': period,
            'age': np.random.normal(age_mean, 10, samples_per_period),
            'income': np.random.normal(income_mean, 15000, samples_per_period),
            'credit_score': np.random.normal(650, 80, samples_per_period)
        })
        all_data.append(data)
    
    return pd.concat(all_data, ignore_index=True)

# สร้างข้อมูล time series
time_series_data = simulate_time_series_data()
print(f"📊 Time Series Data Shape: {time_series_data.shape}")
print(f"📋 Periods: {time_series_data['period'].unique()}")

# %%
# Visualize distribution over time
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

features_to_plot = ['age', 'income', 'credit_score']
colors = plt.cm.viridis(np.linspace(0, 1, 6))

for idx, feature in enumerate(features_to_plot):
    ax = axes[idx]
    
    for period in range(6):
        period_data = time_series_data[time_series_data['period'] == period][feature]
        ax.hist(period_data, bins=20, alpha=0.3, color=colors[period], label=f'Period {period}')
        ax.axvline(period_data.mean(), color=colors[period], linestyle='--', alpha=0.8)
    
    ax.set_title(f'{feature.capitalize()} Distribution Over Time')
    ax.set_xlabel(feature)
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=8)

plt.suptitle('Feature Distributions Across Time Periods\n(Dashed lines = Mean per period)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('time_series_distributions.png', dpi=150, bbox_inches='tight')
plt.show()

# %%
# Calculate PSI over time (comparing each period to Period 0)
def calculate_psi_over_time(data, feature, reference_period=0):
    """
    คำนวณ PSI เมื่อเทียบกับ reference period
    """
    ref_data = data[data['period'] == reference_period][feature]
    
    results = []
    for period in data['period'].unique():
        if period == reference_period:
            results.append({'period': period, 'psi': 0})
        else:
            cur_data = data[data['period'] == period][feature]
            
            # Calculate PSI
            breakpoints = np.percentile(ref_data, np.linspace(0, 100, 11))
            breakpoints = np.unique(breakpoints)
            
            ref_counts, _ = np.histogram(ref_data, bins=breakpoints)
            cur_counts, _ = np.histogram(cur_data, bins=breakpoints)
            
            eps = 1e-6
            ref_props = ref_counts / len(ref_data) + eps
            cur_props = cur_counts / len(cur_data) + eps
            
            psi = np.sum((cur_props - ref_props) * np.log(cur_props / ref_props))
            results.append({'period': period, 'psi': psi})
    
    return pd.DataFrame(results)

# คำนวณ PSI สำหรับแต่ละ feature
fig, ax = plt.subplots(figsize=(10, 6))

for feature in ['age', 'income', 'credit_score']:
    psi_over_time = calculate_psi_over_time(time_series_data, feature)
    ax.plot(psi_over_time['period'], psi_over_time['psi'], marker='o', label=feature, linewidth=2)

ax.axhline(0.1, color='orange', linestyle='--', alpha=0.7, label='Mild Threshold')
ax.axhline(0.25, color='red', linestyle='--', alpha=0.7, label='Severe Threshold')

ax.set_xlabel('Time Period')
ax.set_ylabel('PSI (compared to Period 0)')
ax.set_title('PSI Trend Over Time\n(Reference: Period 0)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('psi_over_time.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 สังเกต: Age แสดง gradual drift (PSI เพิ่มขึ้นเรื่อยๆ)")
print("   ในขณะที่ Income และ Credit Score ค่อนข้าง stable")

# %% [markdown]
# ## สรุป LAB 2
#
# ### สิ่งที่เรียนรู้:
# 1. **FeatureDriftDetector Class**: เครื่องมือสำหรับวิเคราะห์ drift ทุก features
# 2. **Numerical vs Categorical**: ใช้ methods ที่เหมาะสมกับแต่ละ type
# 3. **Visualization**: ช่วยให้เห็น drift ได้ชัดเจน
# 4. **Ranking**: จัดลำดับ features ตาม severity เพื่อ prioritization
# 5. **Time-based Analysis**: ติดตาม drift เมื่อเวลาผ่านไป

# %%
print("=" * 60)
print("✅ LAB 2 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Numerical features: ใช้ KS Test + PSI + Wasserstein
2. Categorical features: ใช้ Chi-squared + PSI
3. Visualization สำคัญสำหรับการทำความเข้าใจ drift
4. Track PSI over time เพื่อ detect gradual drift

🔜 Next: LAB 3 - Multivariate Drift Analysis
""")




## LAB 3: Multivariate Drift Analysis


# %% [markdown]
# # LAB 3: Multivariate Drift Analysis
# ## การวิเคราะห์ Drift ที่เกิดจากความสัมพันธ์ระหว่าง Features
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. ตรวจจับ drift ที่เกิดจากความสัมพันธ์ระหว่าง features
# 2. ใช้ Dataset-level drift detection
# 3. วิเคราะห์ Correlation changes ระหว่าง features
#
# ### ทฤษฎี:
# **Multivariate Drift** เกิดขึ้นเมื่อ:
# - แต่ละ feature ดูปกติเมื่อวิเคราะห์แยก
# - แต่ความสัมพันธ์ระหว่าง features เปลี่ยนไป
# - ตัวอย่าง: correlation ระหว่าง age และ income เปลี่ยน

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import EmpiricalCovariance
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
plt.rcParams['figure.figsize'] = (12, 8)

print("✅ Libraries imported successfully!")

# %% [markdown]
# ## ส่วนที่ 2: สร้าง Dataset ที่มี Multivariate Drift
#
# เราจะสร้างข้อมูลที่:
# - Marginal distributions เหมือนกัน (ไม่มี univariate drift)
# - แต่ correlation structure เปลี่ยน (multivariate drift)

# %%
def create_multivariate_drift_data(n_samples=2000):
    """
    สร้างข้อมูลที่มี multivariate drift
    - Marginal distributions คล้ายกัน
    - Correlation structure ต่างกัน
    """
    np.random.seed(42)
    
    # === Reference Data ===
    # Correlated features: age และ income มี positive correlation สูง
    mean_ref = [35, 50000, 650]  # age, income, credit_score
    cov_ref = [
        [100, 3000, 50],      # age variance และ covariance
        [3000, 225000000, 100000],  # income variance และ covariance
        [50, 100000, 6400]    # credit_score variance และ covariance
    ]
    
    ref_data = np.random.multivariate_normal(mean_ref, cov_ref, n_samples)
    reference_df = pd.DataFrame(ref_data, columns=['age', 'income', 'credit_score'])
    
    # === Current Data (Multivariate Drift) ===
    # Same marginals but different correlation structure
    mean_cur = [35, 50000, 650]  # means เหมือนเดิม
    
    # Correlation structure เปลี่ยน: age และ income correlation ลดลง
    cov_cur = [
        [100, 500, 50],       # correlation ระหว่าง age-income ลดลงมาก!
        [500, 225000000, 100000],
        [50, 100000, 6400]
    ]
    
    cur_data = np.random.multivariate_normal(mean_cur, cov_cur, n_samples)
    current_df = pd.DataFrame(cur_data, columns=['age', 'income', 'credit_score'])
    
    return reference_df, current_df

# สร้างข้อมูล
ref_multi, cur_multi = create_multivariate_drift_data()

print("📊 Reference Data:")
print(ref_multi.describe())
print("\n📊 Current Data:")
print(cur_multi.describe())

# %%
# แสดง correlation matrix comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Reference correlation matrix
corr_ref = ref_multi.corr()
sns.heatmap(corr_ref, annot=True, cmap='coolwarm', center=0, ax=axes[0], 
            vmin=-1, vmax=1, fmt='.3f')
axes[0].set_title('Reference Correlation Matrix')

# Current correlation matrix
corr_cur = cur_multi.corr()
sns.heatmap(corr_cur, annot=True, cmap='coolwarm', center=0, ax=axes[1],
            vmin=-1, vmax=1, fmt='.3f')
axes[1].set_title('Current Correlation Matrix')

# Difference
corr_diff = corr_cur - corr_ref
sns.heatmap(corr_diff, annot=True, cmap='RdBu', center=0, ax=axes[2],
            vmin=-1, vmax=1, fmt='.3f')
axes[2].set_title('Correlation Difference\n(Current - Reference)')

plt.tight_layout()
plt.savefig('correlation_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 สังเกต: Correlation ระหว่าง Age-Income เปลี่ยนจาก ~0.6 เป็น ~0.03")

# %% [markdown]
# ## ส่วนที่ 3: Univariate vs Multivariate Drift Detection
#
# เปรียบเทียบว่า univariate methods พลาดอะไรไป

# %%
from scipy import stats

def univariate_drift_check(ref_df, cur_df):
    """ตรวจจับ drift ด้วย univariate methods"""
    results = []
    
    for col in ref_df.columns:
        # KS Test
        ks_stat, ks_pval = stats.ks_2samp(ref_df[col], cur_df[col])
        
        # Mean comparison
        ref_mean = ref_df[col].mean()
        cur_mean = cur_df[col].mean()
        mean_diff_pct = abs(cur_mean - ref_mean) / ref_mean * 100
        
        # Std comparison
        ref_std = ref_df[col].std()
        cur_std = cur_df[col].std()
        std_diff_pct = abs(cur_std - ref_std) / ref_std * 100
        
        results.append({
            'feature': col,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_pval,
            'drift_detected': ks_pval < 0.05,
            'mean_diff_%': mean_diff_pct,
            'std_diff_%': std_diff_pct
        })
    
    return pd.DataFrame(results)

# ตรวจจับ univariate drift
univariate_results = univariate_drift_check(ref_multi, cur_multi)
print("=" * 60)
print("📊 UNIVARIATE DRIFT DETECTION RESULTS")
print("=" * 60)
print(univariate_results.to_string(index=False))

print("\n💡 สังเกต: Univariate methods ไม่พบ drift ที่สำคัญ!")
print("   แต่เรารู้ว่า correlation structure เปลี่ยนไป")

# %% [markdown]
# ## ส่วนที่ 4: Correlation-based Drift Detection
#
# ตรวจจับการเปลี่ยนแปลงของ correlation structure

# %%
def correlation_drift_test(ref_df, cur_df, significance_level=0.05):
    """
    ตรวจจับ drift ใน correlation structure
    
    ใช้ Fisher's Z transformation เพื่อเปรียบเทียบ correlations
    """
    results = []
    
    # คำนวณ correlation matrices
    ref_corr = ref_df.corr()
    cur_corr = cur_df.corr()
    
    n_ref = len(ref_df)
    n_cur = len(cur_df)
    
    # เปรียบเทียบแต่ละ pair
    for i, col1 in enumerate(ref_df.columns):
        for j, col2 in enumerate(ref_df.columns):
            if i >= j:  # ข้าม diagonal และ lower triangle
                continue
            
            r_ref = ref_corr.loc[col1, col2]
            r_cur = cur_corr.loc[col1, col2]
            
            # Fisher's Z transformation
            z_ref = np.arctanh(r_ref)
            z_cur = np.arctanh(r_cur)
            
            # Standard error
            se = np.sqrt(1/(n_ref-3) + 1/(n_cur-3))
            
            # Z-test statistic
            z_stat = (z_ref - z_cur) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            
            results.append({
                'feature_pair': f'{col1} - {col2}',
                'ref_correlation': r_ref,
                'cur_correlation': r_cur,
                'correlation_change': r_cur - r_ref,
                'z_statistic': z_stat,
                'p_value': p_value,
                'significant_change': p_value < significance_level
            })
    
    return pd.DataFrame(results)

# ตรวจจับ correlation drift
corr_drift_results = correlation_drift_test(ref_multi, cur_multi)
print("=" * 60)
print("📊 CORRELATION DRIFT DETECTION RESULTS")
print("=" * 60)
print(corr_drift_results.to_string(index=False))

# %%
# Visualize correlation changes
fig, ax = plt.subplots(figsize=(10, 6))

x = range(len(corr_drift_results))
colors = ['red' if sig else 'green' for sig in corr_drift_results['significant_change']]

bars = ax.bar(x, corr_drift_results['correlation_change'], color=colors, alpha=0.7, edgecolor='black')

ax.set_xticks(x)
ax.set_xticklabels(corr_drift_results['feature_pair'], rotation=45, ha='right')
ax.set_ylabel('Correlation Change')
ax.set_title('Correlation Changes Between Reference and Current Data\n(Red = Statistically Significant)')
ax.axhline(0, color='black', linestyle='-', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, corr_drift_results['correlation_change']):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{val:.3f}',
            ha='center', va='bottom' if height > 0 else 'top')

plt.tight_layout()
plt.savefig('correlation_drift.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 5: PCA-based Multivariate Drift Detection
#
# ใช้ PCA เพื่อตรวจจับ drift ใน multivariate structure

# %%
def pca_drift_detection(ref_df, cur_df, n_components=None):
    """
    ใช้ PCA เพื่อตรวจจับ multivariate drift
    
    เปรียบเทียบ:
    1. Explained variance ratios
    2. Principal component directions
    3. Reconstruction errors
    """
    if n_components is None:
        n_components = min(len(ref_df.columns), 3)
    
    # Standardize data
    scaler = StandardScaler()
    ref_scaled = scaler.fit_transform(ref_df)
    cur_scaled = scaler.transform(cur_df)
    
    # Fit PCA on reference data
    pca_ref = PCA(n_components=n_components)
    pca_ref.fit(ref_scaled)
    
    # Transform both datasets using reference PCA
    ref_transformed = pca_ref.transform(ref_scaled)
    cur_transformed = pca_ref.transform(cur_scaled)
    
    # 1. Compare explained variance
    ref_explained_var = pca_ref.explained_variance_ratio_
    
    # Fit PCA on current data for comparison
    pca_cur = PCA(n_components=n_components)
    pca_cur.fit(cur_scaled)
    cur_explained_var = pca_cur.explained_variance_ratio_
    
    # 2. Compare principal components (using cosine similarity)
    component_similarities = []
    for i in range(n_components):
        cos_sim = np.dot(pca_ref.components_[i], pca_cur.components_[i])
        cos_sim = abs(cos_sim)  # Absolute value เพราะ sign อาจ flip
        component_similarities.append(cos_sim)
    
    # 3. Reconstruction error on current data using reference PCA
    ref_reconstructed = pca_ref.inverse_transform(ref_transformed)
    cur_reconstructed = pca_ref.inverse_transform(cur_transformed)
    
    ref_recon_error = np.mean((ref_scaled - ref_reconstructed) ** 2)
    cur_recon_error = np.mean((cur_scaled - cur_reconstructed) ** 2)
    
    results = {
        'ref_explained_variance': ref_explained_var,
        'cur_explained_variance': cur_explained_var,
        'component_similarities': component_similarities,
        'ref_reconstruction_error': ref_recon_error,
        'cur_reconstruction_error': cur_recon_error,
        'reconstruction_error_ratio': cur_recon_error / ref_recon_error if ref_recon_error > 0 else 1,
        'ref_components': pca_ref.components_,
        'cur_components': pca_cur.components_,
        'pca_ref': pca_ref,
        'ref_transformed': ref_transformed,
        'cur_transformed': cur_transformed
    }
    
    return results

# ทำ PCA drift detection
pca_results = pca_drift_detection(ref_multi, cur_multi)

print("=" * 60)
print("📊 PCA-BASED DRIFT DETECTION RESULTS")
print("=" * 60)

print("\n1. Explained Variance Comparison:")
for i in range(len(pca_results['ref_explained_variance'])):
    ref_ev = pca_results['ref_explained_variance'][i]
    cur_ev = pca_results['cur_explained_variance'][i]
    print(f"   PC{i+1}: Reference = {ref_ev:.4f}, Current = {cur_ev:.4f}, Diff = {cur_ev - ref_ev:.4f}")

print("\n2. Component Similarities (1.0 = identical):")
for i, sim in enumerate(pca_results['component_similarities']):
    status = "✓ Similar" if sim > 0.9 else "⚠️ Changed!"
    print(f"   PC{i+1}: Cosine Similarity = {sim:.4f} {status}")

print("\n3. Reconstruction Error:")
print(f"   Reference: {pca_results['ref_reconstruction_error']:.6f}")
print(f"   Current: {pca_results['cur_reconstruction_error']:.6f}")
print(f"   Ratio: {pca_results['reconstruction_error_ratio']:.4f}x")

# %%
# Visualize PCA results
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Explained variance comparison
ax1 = axes[0, 0]
x = range(1, len(pca_results['ref_explained_variance']) + 1)
width = 0.35
ax1.bar([i - width/2 for i in x], pca_results['ref_explained_variance'], 
        width, label='Reference', color='blue', alpha=0.7)
ax1.bar([i + width/2 for i in x], pca_results['cur_explained_variance'], 
        width, label='Current', color='red', alpha=0.7)
ax1.set_xlabel('Principal Component')
ax1.set_ylabel('Explained Variance Ratio')
ax1.set_title('Explained Variance Comparison')
ax1.legend()
ax1.set_xticks(x)

# Plot 2: Component similarities
ax2 = axes[0, 1]
colors = ['green' if s > 0.9 else 'red' for s in pca_results['component_similarities']]
ax2.bar(x, pca_results['component_similarities'], color=colors, alpha=0.7, edgecolor='black')
ax2.axhline(0.9, color='orange', linestyle='--', label='Similarity Threshold (0.9)')
ax2.set_xlabel('Principal Component')
ax2.set_ylabel('Cosine Similarity')
ax2.set_title('Principal Component Similarity\n(Reference vs Current)')
ax2.set_xticks(x)
ax2.legend()

# Plot 3: Scatter plot in PC space (Reference)
ax3 = axes[1, 0]
ax3.scatter(pca_results['ref_transformed'][:, 0], pca_results['ref_transformed'][:, 1], 
            alpha=0.3, label='Reference', color='blue')
ax3.scatter(pca_results['cur_transformed'][:, 0], pca_results['cur_transformed'][:, 1], 
            alpha=0.3, label='Current', color='red')
ax3.set_xlabel('PC1')
ax3.set_ylabel('PC2')
ax3.set_title('Data in PCA Space\n(Using Reference PCA)')
ax3.legend()

# Plot 4: Component loadings comparison
ax4 = axes[1, 1]
features = ref_multi.columns.tolist()
x = np.arange(len(features))
width = 0.35

for i in range(2):  # แสดง PC1 และ PC2
    ref_loadings = pca_results['ref_components'][i]
    cur_loadings = pca_results['cur_components'][i]
    
    ax4.barh([f'PC{i+1} Ref' for f in features] if i == 0 else [f'PC{i+1} Cur' for f in features], 
             ref_loadings if i == 0 else cur_loadings)

ax4.set_xlabel('Loading')
ax4.set_title('PC Loadings (First 2 Components)')

plt.tight_layout()
plt.savefig('pca_drift_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 6: Mahalanobis Distance for Dataset-level Drift
#
# ใช้ Mahalanobis distance เพื่อวัด multivariate drift

# %%
def mahalanobis_drift_detection(ref_df, cur_df, threshold_percentile=95):
    """
    ใช้ Mahalanobis distance เพื่อตรวจจับ multivariate drift
    
    วัดว่าข้อมูลใหม่อยู่ห่างจาก distribution ของ reference data เท่าไร
    """
    # Standardize features
    scaler = StandardScaler()
    ref_scaled = scaler.fit_transform(ref_df)
    cur_scaled = scaler.transform(cur_df)
    
    # Fit covariance on reference data
    cov = EmpiricalCovariance().fit(ref_scaled)
    
    # Calculate Mahalanobis distances
    ref_distances = cov.mahalanobis(ref_scaled)
    cur_distances = cov.mahalanobis(cur_scaled)
    
    # Determine threshold from reference data
    threshold = np.percentile(ref_distances, threshold_percentile)
    
    # Count outliers
    ref_outliers = np.sum(ref_distances > threshold) / len(ref_distances) * 100
    cur_outliers = np.sum(cur_distances > threshold) / len(cur_distances) * 100
    
    # Statistical comparison
    ks_stat, ks_pval = stats.ks_2samp(ref_distances, cur_distances)
    
    results = {
        'ref_distances': ref_distances,
        'cur_distances': cur_distances,
        'threshold': threshold,
        'ref_mean_distance': np.mean(ref_distances),
        'cur_mean_distance': np.mean(cur_distances),
        'ref_outlier_pct': ref_outliers,
        'cur_outlier_pct': cur_outliers,
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pval,
        'drift_detected': ks_pval < 0.05
    }
    
    return results

# ทำ Mahalanobis drift detection
maha_results = mahalanobis_drift_detection(ref_multi, cur_multi)

print("=" * 60)
print("📊 MAHALANOBIS DISTANCE DRIFT DETECTION")
print("=" * 60)
print(f"\nMean Mahalanobis Distance:")
print(f"  Reference: {maha_results['ref_mean_distance']:.4f}")
print(f"  Current: {maha_results['cur_mean_distance']:.4f}")
print(f"\nOutlier Percentage (beyond {maha_results['threshold']:.2f} threshold):")
print(f"  Reference: {maha_results['ref_outlier_pct']:.2f}%")
print(f"  Current: {maha_results['cur_outlier_pct']:.2f}%")
print(f"\nKS Test on Distances:")
print(f"  Statistic: {maha_results['ks_statistic']:.4f}")
print(f"  P-value: {maha_results['ks_pvalue']:.4f}")
print(f"  Drift Detected: {'Yes ✓' if maha_results['drift_detected'] else 'No'}")

# %%
# Visualize Mahalanobis distances
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Distribution of Mahalanobis distances
ax1 = axes[0]
ax1.hist(maha_results['ref_distances'], bins=50, alpha=0.5, label='Reference', color='blue', density=True)
ax1.hist(maha_results['cur_distances'], bins=50, alpha=0.5, label='Current', color='red', density=True)
ax1.axvline(maha_results['threshold'], color='orange', linestyle='--', linewidth=2, 
            label=f'95th percentile threshold ({maha_results["threshold"]:.2f})')
ax1.set_xlabel('Mahalanobis Distance')
ax1.set_ylabel('Density')
ax1.set_title('Distribution of Mahalanobis Distances')
ax1.legend()

# Plot 2: CDF comparison
ax2 = axes[1]
sorted_ref = np.sort(maha_results['ref_distances'])
sorted_cur = np.sort(maha_results['cur_distances'])

ax2.plot(sorted_ref, np.arange(1, len(sorted_ref)+1)/len(sorted_ref), 
         'b-', label='Reference CDF', linewidth=2)
ax2.plot(sorted_cur, np.arange(1, len(sorted_cur)+1)/len(sorted_cur), 
         'r-', label='Current CDF', linewidth=2)
ax2.axvline(maha_results['threshold'], color='orange', linestyle='--', linewidth=2)
ax2.set_xlabel('Mahalanobis Distance')
ax2.set_ylabel('Cumulative Probability')
ax2.set_title(f'CDF Comparison\nKS Statistic = {maha_results["ks_statistic"]:.4f}')
ax2.legend()

plt.tight_layout()
plt.savefig('mahalanobis_drift.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 7: Comprehensive Multivariate Drift Report

# %%
class MultivariateriftDetector:
    """
    Class สำหรับ comprehensive multivariate drift detection
    """
    
    def __init__(self, reference_df, current_df):
        self.reference = reference_df
        self.current = current_df
        self.results = {}
    
    def analyze(self):
        """ทำ comprehensive analysis"""
        
        # 1. Correlation analysis
        corr_results = correlation_drift_test(self.reference, self.current)
        self.results['correlation'] = corr_results
        
        # 2. PCA analysis
        pca_results = pca_drift_detection(self.reference, self.current)
        self.results['pca'] = pca_results
        
        # 3. Mahalanobis analysis
        maha_results = mahalanobis_drift_detection(self.reference, self.current)
        self.results['mahalanobis'] = maha_results
        
        # 4. Overall assessment
        drift_indicators = {
            'correlation_drift': any(corr_results['significant_change']),
            'pca_structure_change': any(sim < 0.9 for sim in pca_results['component_similarities']),
            'mahalanobis_drift': maha_results['drift_detected']
        }
        
        drift_count = sum(drift_indicators.values())
        
        self.results['summary'] = {
            'drift_indicators': drift_indicators,
            'drift_count': drift_count,
            'overall_assessment': 'HIGH' if drift_count >= 2 else 'MEDIUM' if drift_count == 1 else 'LOW'
        }
        
        return self.results
    
    def print_report(self):
        """พิมพ์ report สรุป"""
        if not self.results:
            self.analyze()
        
        print("=" * 70)
        print("📊 COMPREHENSIVE MULTIVARIATE DRIFT REPORT")
        print("=" * 70)
        
        print("\n1️⃣ CORRELATION DRIFT:")
        print("-" * 40)
        corr_df = self.results['correlation']
        significant_pairs = corr_df[corr_df['significant_change']]
        if len(significant_pairs) > 0:
            print("   ⚠️ Significant correlation changes detected:")
            for _, row in significant_pairs.iterrows():
                print(f"      {row['feature_pair']}: {row['ref_correlation']:.3f} → {row['cur_correlation']:.3f}")
        else:
            print("   ✓ No significant correlation changes")
        
        print("\n2️⃣ PCA STRUCTURE ANALYSIS:")
        print("-" * 40)
        pca_res = self.results['pca']
        for i, sim in enumerate(pca_res['component_similarities']):
            status = "✓" if sim > 0.9 else "⚠️ Changed"
            print(f"   PC{i+1} similarity: {sim:.4f} {status}")
        print(f"   Reconstruction error ratio: {pca_res['reconstruction_error_ratio']:.4f}x")
        
        print("\n3️⃣ MAHALANOBIS DISTANCE ANALYSIS:")
        print("-" * 40)
        maha_res = self.results['mahalanobis']
        print(f"   Mean distance ratio: {maha_res['cur_mean_distance']/maha_res['ref_mean_distance']:.4f}x")
        print(f"   Outlier % (Reference): {maha_res['ref_outlier_pct']:.2f}%")
        print(f"   Outlier % (Current): {maha_res['cur_outlier_pct']:.2f}%")
        print(f"   KS Test p-value: {maha_res['ks_pvalue']:.4f}")
        
        print("\n" + "=" * 70)
        print("📋 OVERALL ASSESSMENT")
        print("=" * 70)
        summary = self.results['summary']
        print(f"   Drift Indicators Triggered: {summary['drift_count']}/3")
        for indicator, triggered in summary['drift_indicators'].items():
            status = "⚠️" if triggered else "✓"
            print(f"      {status} {indicator}: {'Yes' if triggered else 'No'}")
        
        severity_emoji = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🔴'}
        print(f"\n   🎯 OVERALL MULTIVARIATE DRIFT: {severity_emoji[summary['overall_assessment']]} {summary['overall_assessment']}")

# ใช้งาน
detector = MultivariateriftDetector(ref_multi, cur_multi)
detector.analyze()
detector.print_report()

# %% [markdown]
# ## สรุป LAB 3
#
# ### สิ่งที่เรียนรู้:
# 1. **Multivariate Drift**: เกิดขึ้นเมื่อ relationship ระหว่าง features เปลี่ยน
# 2. **Correlation Analysis**: ตรวจจับการเปลี่ยนแปลงของ pairwise correlations
# 3. **PCA Analysis**: ตรวจจับการเปลี่ยนแปลงของ multivariate structure
# 4. **Mahalanobis Distance**: วัด dataset-level drift
#
# ### Key Insights:
# - Univariate methods อาจพลาด multivariate drift
# - ใช้หลาย methods ร่วมกันเพื่อความครอบคลุม
# - Monitor ทั้ง individual features และ relationships

# %%
print("=" * 60)
print("✅ LAB 3 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Multivariate drift ตรวจจับด้วย univariate methods ไม่ได้
2. Correlation drift analysis ใช้ Fisher's Z transformation
3. PCA structure comparison ดู component similarities
4. Mahalanobis distance วัด overall distribution shift

🔜 Next: LAB 4 - Drift Detection in Production Simulation
""")
```

---

## LAB 4: Drift Detection in Production Simulation

```python
# %% [markdown]
# # LAB 4: Drift Detection in Production Simulation
# ## การจำลองการตรวจจับ Drift ใน Production Environment
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. สร้าง simulated data stream ที่มี gradual drift
# 2. ตรวจจับ sudden vs gradual drift
# 3. Implement sliding window monitoring
#
# ### ทฤษฎี:
# ใน production environment:
# - ข้อมูลมาเป็น stream ไม่ใช่ batch
# - Drift อาจเกิดแบบ sudden หรือ gradual
# - ต้องมี monitoring strategy ที่เหมาะสม

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from collections import deque
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
plt.rcParams['figure.figsize'] = (14, 6)

print("✅ Libraries imported successfully!")

# %% [markdown]
# ## ส่วนที่ 2: สร้าง Data Stream Simulator
#
# จำลอง data stream ที่มี drift หลายรูปแบบ

# %%
class DataStreamSimulator:
    """
    Simulator สำหรับสร้าง data stream ที่มี drift patterns ต่างๆ
    
    Drift Types:
    - sudden: เปลี่ยนทันทีที่จุดใดจุดหนึ่ง
    - gradual: เปลี่ยนแปลงช้าๆ ตามเวลา
    - incremental: เปลี่ยนเป็นขั้นบันได
    - seasonal: เปลี่ยนตาม pattern ซ้ำ
    - no_drift: ไม่มี drift
    """
    
    def __init__(self, base_mean=50, base_std=10, random_seed=42):
        self.base_mean = base_mean
        self.base_std = base_std
        self.random_seed = random_seed
        np.random.seed(random_seed)
    
    def generate_stream(self, n_samples, drift_type='no_drift', drift_params=None):
        """
        สร้าง data stream
        
        Parameters:
        -----------
        n_samples : int - จำนวน samples
        drift_type : str - ประเภทของ drift
        drift_params : dict - parameters สำหรับ drift
        """
        if drift_params is None:
            drift_params = {}
        
        data = np.zeros(n_samples)
        timestamps = [datetime(2024, 1, 1) + timedelta(hours=i) for i in range(n_samples)]
        
        if drift_type == 'no_drift':
            data = np.random.normal(self.base_mean, self.base_std, n_samples)
        
        elif drift_type == 'sudden':
            drift_point = drift_params.get('drift_point', n_samples // 2)
            new_mean = drift_params.get('new_mean', self.base_mean + 2 * self.base_std)
            
            data[:drift_point] = np.random.normal(self.base_mean, self.base_std, drift_point)
            data[drift_point:] = np.random.normal(new_mean, self.base_std, n_samples - drift_point)
        
        elif drift_type == 'gradual':
            drift_start = drift_params.get('drift_start', n_samples // 4)
            drift_end = drift_params.get('drift_end', 3 * n_samples // 4)
            final_mean = drift_params.get('final_mean', self.base_mean + 2 * self.base_std)
            
            for i in range(n_samples):
                if i < drift_start:
                    current_mean = self.base_mean
                elif i > drift_end:
                    current_mean = final_mean
                else:
                    # Linear interpolation
                    progress = (i - drift_start) / (drift_end - drift_start)
                    current_mean = self.base_mean + progress * (final_mean - self.base_mean)
                
                data[i] = np.random.normal(current_mean, self.base_std)
        
        elif drift_type == 'incremental':
            step_size = drift_params.get('step_size', n_samples // 5)
            step_increase = drift_params.get('step_increase', self.base_std * 0.5)
            
            for i in range(n_samples):
                step = i // step_size
                current_mean = self.base_mean + step * step_increase
                data[i] = np.random.normal(current_mean, self.base_std)
        
        elif drift_type == 'seasonal':
            period = drift_params.get('period', 168)  # 1 week in hours
            amplitude = drift_params.get('amplitude', self.base_std)
            
            for i in range(n_samples):
                seasonal_effect = amplitude * np.sin(2 * np.pi * i / period)
                data[i] = np.random.normal(self.base_mean + seasonal_effect, self.base_std)
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'value': data,
            'index': range(n_samples)
        })

# สร้าง simulator
simulator = DataStreamSimulator(base_mean=50, base_std=10)

print("✅ DataStreamSimulator created")

# %%
# สร้างตัวอย่าง drift patterns
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

drift_types = ['no_drift', 'sudden', 'gradual', 'incremental', 'seasonal']
drift_params_list = [
    {},
    {'drift_point': 500, 'new_mean': 70},
    {'drift_start': 200, 'drift_end': 800, 'final_mean': 70},
    {'step_size': 200, 'step_increase': 5},
    {'period': 200, 'amplitude': 15}
]

streams = {}
for i, (dtype, params) in enumerate(zip(drift_types, drift_params_list)):
    stream = simulator.generate_stream(1000, drift_type=dtype, drift_params=params)
    streams[dtype] = stream
    
    ax = axes[i]
    ax.plot(stream['index'], stream['value'], alpha=0.7, linewidth=0.5)
    
    # Add rolling mean
    rolling_mean = stream['value'].rolling(window=50).mean()
    ax.plot(stream['index'], rolling_mean, 'r-', linewidth=2, label='Rolling Mean (50)')
    
    ax.axhline(50, color='green', linestyle='--', alpha=0.5, label='Original Mean')
    ax.set_title(f'{dtype.replace("_", " ").title()}')
    ax.set_xlabel('Time Index')
    ax.set_ylabel('Value')
    ax.legend(fontsize=8)

# Hide empty subplot
axes[-1].set_visible(False)

plt.suptitle('Different Types of Data Drift', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('drift_types.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 3: Sliding Window Drift Detector
#
# Implement sliding window สำหรับ real-time drift detection

# %%
class SlidingWindowDriftDetector:
    """
    Drift detector ที่ใช้ sliding window approach
    
    เหมาะสำหรับ:
    - Real-time monitoring
    - Streaming data
    - Memory-efficient processing
    """
    
    def __init__(self, reference_window_size=200, test_window_size=100, 
                 ks_threshold=0.05, psi_threshold=0.1):
        """
        Parameters:
        -----------
        reference_window_size : int - ขนาดของ reference window
        test_window_size : int - ขนาดของ test window
        ks_threshold : float - threshold สำหรับ KS test p-value
        psi_threshold : float - threshold สำหรับ PSI
        """
        self.reference_window_size = reference_window_size
        self.test_window_size = test_window_size
        self.ks_threshold = ks_threshold
        self.psi_threshold = psi_threshold
        
        # ใช้ deque สำหรับ efficient sliding window
        self.reference_buffer = deque(maxlen=reference_window_size)
        self.test_buffer = deque(maxlen=test_window_size)
        
        self.history = []
        self.drift_points = []
        self.is_initialized = False
    
    def calculate_psi(self, reference, test, bins=10):
        """คำนวณ PSI"""
        breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        ref_counts, _ = np.histogram(reference, bins=breakpoints)
        test_counts, _ = np.histogram(test, bins=breakpoints)
        
        eps = 1e-6
        ref_props = ref_counts / len(reference) + eps
        test_props = test_counts / len(test) + eps
        
        psi = np.sum((test_props - ref_props) * np.log(test_props / ref_props))
        return psi
    
    def update(self, value, timestamp=None):
        """
        Update detector ด้วยค่าใหม่
        
        Returns:
        --------
        dict : detection result
        """
        # เพิ่มค่าใน buffers
        if not self.is_initialized:
            self.reference_buffer.append(value)
            if len(self.reference_buffer) >= self.reference_window_size:
                self.is_initialized = True
            return {'drift_detected': False, 'status': 'initializing'}
        
        self.test_buffer.append(value)
        
        # รอจนมีข้อมูลพอใน test buffer
        if len(self.test_buffer) < self.test_window_size:
            return {'drift_detected': False, 'status': 'collecting'}
        
        # ทำ drift detection
        ref_array = np.array(self.reference_buffer)
        test_array = np.array(self.test_buffer)
        
        # KS Test
        ks_stat, ks_pval = stats.ks_2samp(ref_array, test_array)
        
        # PSI
        psi = self.calculate_psi(ref_array, test_array)
        
        # Detection logic
        ks_drift = ks_pval < self.ks_threshold
        psi_drift = psi > self.psi_threshold
        drift_detected = ks_drift or psi_drift
        
        result = {
            'timestamp': timestamp,
            'drift_detected': drift_detected,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_pval,
            'psi': psi,
            'ref_mean': np.mean(ref_array),
            'test_mean': np.mean(test_array),
            'status': 'DRIFT' if drift_detected else 'normal'
        }
        
        self.history.append(result)
        
        if drift_detected:
            self.drift_points.append(len(self.history) - 1)
        
        return result
    
    def reset_reference(self):
        """Reset reference window ด้วย test window ปัจจุบัน"""
        self.reference_buffer.clear()
        for val in self.test_buffer:
            self.reference_buffer.append(val)
        self.test_buffer.clear()
        print("📋 Reference window reset with current data")
    
    def get_history_df(self):
        """แปลง history เป็น DataFrame"""
        return pd.DataFrame(self.history)

# %%
# ทดสอบ SlidingWindowDriftDetector กับ sudden drift
print("=" * 60)
print("🔍 Testing Sliding Window Detector with SUDDEN DRIFT")
print("=" * 60)

detector = SlidingWindowDriftDetector(
    reference_window_size=200,
    test_window_size=100,
    ks_threshold=0.05,
    psi_threshold=0.1
)

sudden_stream = streams['sudden']

for idx, row in sudden_stream.iterrows():
    result = detector.update(row['value'], timestamp=row['timestamp'])
    
    # Print only drift events
    if result.get('drift_detected', False):
        print(f"⚠️ DRIFT at index {idx}: KS p-value={result['ks_pvalue']:.4f}, PSI={result['psi']:.4f}")

print(f"\n📊 Total drift points detected: {len(detector.drift_points)}")

# %%
# Visualize detection results
history_df = detector.get_history_df()

fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Plot 1: Original data with drift points
ax1 = axes[0]
ax1.plot(sudden_stream['index'], sudden_stream['value'], alpha=0.5, label='Data')
ax1.plot(sudden_stream['index'], sudden_stream['value'].rolling(50).mean(), 
         'b-', linewidth=2, label='Rolling Mean')

# Mark drift points
for dp in detector.drift_points:
    ax1.axvline(dp + 200 + 100, color='red', alpha=0.5, linestyle='--')  # Offset for initialization

ax1.axvline(500, color='green', linestyle='--', linewidth=2, label='Actual Drift Point')
ax1.set_ylabel('Value')
ax1.set_title('Data Stream with Detected Drift Points')
ax1.legend()

# Plot 2: KS p-value over time
ax2 = axes[1]
ax2.plot(history_df.index + 200 + 100, history_df['ks_pvalue'], 'b-', linewidth=1)
ax2.axhline(0.05, color='red', linestyle='--', label='Threshold (0.05)')
ax2.set_ylabel('KS p-value')
ax2.set_title('KS Test p-value Over Time')
ax2.legend()
ax2.set_yscale('log')

# Plot 3: PSI over time
ax3 = axes[2]
ax3.plot(history_df.index + 200 + 100, history_df['psi'], 'g-', linewidth=1)
ax3.axhline(0.1, color='red', linestyle='--', label='Threshold (0.1)')
ax3.set_ylabel('PSI')
ax3.set_xlabel('Time Index')
ax3.set_title('PSI Over Time')
ax3.legend()

plt.tight_layout()
plt.savefig('sliding_window_detection.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 4: Detecting Gradual Drift
#
# Gradual drift ยากกว่า sudden drift เพราะเปลี่ยนช้าๆ

# %%
print("=" * 60)
print("🔍 Testing Sliding Window Detector with GRADUAL DRIFT")
print("=" * 60)

detector_gradual = SlidingWindowDriftDetector(
    reference_window_size=200,
    test_window_size=100
)

gradual_stream = streams['gradual']

for idx, row in gradual_stream.iterrows():
    result = detector_gradual.update(row['value'], timestamp=row['timestamp'])

history_gradual = detector_gradual.get_history_df()

print(f"\n📊 Total drift points detected: {len(detector_gradual.drift_points)}")
print(f"   First detection at index: {detector_gradual.drift_points[0] + 300 if detector_gradual.drift_points else 'N/A'}")

# %%
# Compare detection of sudden vs gradual drift
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sudden drift
ax1 = axes[0, 0]
ax1.plot(sudden_stream['index'], sudden_stream['value'], alpha=0.3)
ax1.plot(sudden_stream['index'], sudden_stream['value'].rolling(50).mean(), 'b-', linewidth=2)
for dp in detector.drift_points:
    ax1.axvline(dp + 300, color='red', alpha=0.3)
ax1.axvline(500, color='green', linestyle='--', linewidth=2, label='Actual Drift')
ax1.set_title('Sudden Drift Detection')
ax1.legend()

ax2 = axes[0, 1]
history_df = detector.get_history_df()
ax2.plot(history_df.index + 300, history_df['psi'], 'g-')
ax2.axhline(0.1, color='red', linestyle='--')
ax2.set_title('Sudden Drift: PSI')

# Gradual drift
ax3 = axes[1, 0]
ax3.plot(gradual_stream['index'], gradual_stream['value'], alpha=0.3)
ax3.plot(gradual_stream['index'], gradual_stream['value'].rolling(50).mean(), 'b-', linewidth=2)
for dp in detector_gradual.drift_points:
    ax3.axvline(dp + 300, color='red', alpha=0.3)
ax3.axvspan(200, 800, alpha=0.2, color='green', label='Drift Period')
ax3.set_title('Gradual Drift Detection')
ax3.legend()

ax4 = axes[1, 1]
ax4.plot(history_gradual.index + 300, history_gradual['psi'], 'g-')
ax4.axhline(0.1, color='red', linestyle='--')
ax4.set_title('Gradual Drift: PSI')

plt.tight_layout()
plt.savefig('sudden_vs_gradual_detection.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 Observation:")
print("   - Sudden drift: ตรวจจับได้เร็วและชัดเจน")
print("   - Gradual drift: ใช้เวลานานกว่าจะ detect ได้")

# %% [markdown]
# ## ส่วนที่ 5: Adaptive Reference Window
#
# ปรับ reference window เพื่อ handle gradual drift

# %%
class AdaptiveDriftDetector:
    """
    Drift detector ที่ปรับ reference window อัตโนมัติ
    
    Features:
    - ปรับ reference เมื่อตรวจจับ drift
    - ป้องกัน false alarms จาก temporary spikes
    - Track both short-term และ long-term drift
    """
    
    def __init__(self, reference_window_size=200, test_window_size=50,
                 confirmation_window=3, psi_threshold=0.1):
        """
        Parameters:
        -----------
        confirmation_window : int - จำนวนครั้งติดต่อกันที่ต้อง detect ก่อนยืนยัน drift
        """
        self.reference_window_size = reference_window_size
        self.test_window_size = test_window_size
        self.confirmation_window = confirmation_window
        self.psi_threshold = psi_threshold
        
        self.reference_buffer = deque(maxlen=reference_window_size)
        self.test_buffer = deque(maxlen=test_window_size)
        
        self.consecutive_drift_count = 0
        self.confirmed_drifts = []
        self.history = []
        self.adaptation_count = 0
    
    def calculate_psi(self, reference, test, bins=10):
        """คำนวณ PSI"""
        breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        ref_counts, _ = np.histogram(reference, bins=breakpoints)
        test_counts, _ = np.histogram(test, bins=breakpoints)
        
        eps = 1e-6
        ref_props = ref_counts / len(reference) + eps
        test_props = test_counts / len(test) + eps
        
        psi = np.sum((test_props - ref_props) * np.log(test_props / ref_props))
        return psi
    
    def adapt_reference(self):
        """ปรับ reference window"""
        # ผสม old reference กับ new data
        old_weight = 0.5
        old_ref = list(self.reference_buffer)
        new_data = list(self.test_buffer)
        
        # สร้าง new reference
        self.reference_buffer.clear()
        
        # เพิ่มบางส่วนจาก old reference
        n_old = int(len(old_ref) * old_weight)
        for val in old_ref[-n_old:]:
            self.reference_buffer.append(val)
        
        # เพิ่ม new data
        for val in new_data:
            self.reference_buffer.append(val)
        
        self.adaptation_count += 1
        self.consecutive_drift_count = 0
    
    def update(self, value, timestamp=None):
        """Update detector"""
        # Initialize
        if len(self.reference_buffer) < self.reference_window_size:
            self.reference_buffer.append(value)
            return {'status': 'initializing', 'drift_detected': False}
        
        self.test_buffer.append(value)
        
        if len(self.test_buffer) < self.test_window_size:
            return {'status': 'collecting', 'drift_detected': False}
        
        # Drift detection
        ref_array = np.array(self.reference_buffer)
        test_array = np.array(self.test_buffer)
        
        psi = self.calculate_psi(ref_array, test_array)
        potential_drift = psi > self.psi_threshold
        
        if potential_drift:
            self.consecutive_drift_count += 1
        else:
            self.consecutive_drift_count = 0
        
        # Confirmed drift (multiple consecutive detections)
        confirmed = self.consecutive_drift_count >= self.confirmation_window
        
        result = {
            'timestamp': timestamp,
            'psi': psi,
            'potential_drift': potential_drift,
            'confirmed_drift': confirmed,
            'consecutive_count': self.consecutive_drift_count,
            'adaptation_count': self.adaptation_count,
            'ref_mean': np.mean(ref_array),
            'test_mean': np.mean(test_array)
        }
        
        self.history.append(result)
        
        # Adapt if confirmed
        if confirmed:
            self.confirmed_drifts.append(len(self.history) - 1)
            self.adapt_reference()
            result['adapted'] = True
        
        return result
    
    def get_history_df(self):
        return pd.DataFrame(self.history)

# %%
# ทดสอบ Adaptive Detector
print("=" * 60)
print("🔍 Testing ADAPTIVE Drift Detector with GRADUAL DRIFT")
print("=" * 60)

adaptive_detector = AdaptiveDriftDetector(
    reference_window_size=200,
    test_window_size=50,
    confirmation_window=3,
    psi_threshold=0.1
)

for idx, row in gradual_stream.iterrows():
    result = adaptive_detector.update(row['value'], timestamp=row['timestamp'])
    
    if result.get('confirmed_drift', False):
        print(f"✅ CONFIRMED DRIFT at index {idx}: PSI={result['psi']:.4f}, Adapted!")

print(f"\n📊 Total confirmed drifts: {len(adaptive_detector.confirmed_drifts)}")
print(f"📊 Total adaptations: {adaptive_detector.adaptation_count}")

# %%
# Visualize adaptive detection
adaptive_history = adaptive_detector.get_history_df()

fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Plot 1: Data with adaptations
ax1 = axes[0]
ax1.plot(gradual_stream['index'], gradual_stream['value'], alpha=0.3)
ax1.plot(gradual_stream['index'], gradual_stream['value'].rolling(50).mean(), 'b-', linewidth=2)

offset = 200 + 50  # initialization + test window
for drift_idx in adaptive_detector.confirmed_drifts:
    ax1.axvline(drift_idx + offset, color='red', linestyle='--', alpha=0.7, linewidth=2)

ax1.set_title('Gradual Drift with Adaptive Detection')
ax1.set_ylabel('Value')

# Plot 2: PSI with threshold
ax2 = axes[1]
ax2.plot(adaptive_history.index + offset, adaptive_history['psi'], 'g-')
ax2.axhline(0.1, color='red', linestyle='--', label='Threshold')
ax2.set_ylabel('PSI')
ax2.legend()

# Plot 3: Reference vs Test mean
ax3 = axes[2]
ax3.plot(adaptive_history.index + offset, adaptive_history['ref_mean'], 'b-', label='Reference Mean')
ax3.plot(adaptive_history.index + offset, adaptive_history['test_mean'], 'r-', label='Test Mean')
ax3.set_xlabel('Time Index')
ax3.set_ylabel('Mean')
ax3.legend()

plt.tight_layout()
plt.savefig('adaptive_detection.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 Adaptive detector ปรับ reference window เมื่อ detect drift")
print("   ทำให้สามารถติดตาม gradual drift ได้ต่อเนื่อง")

# %% [markdown]
# ## ส่วนที่ 6: Page-Hinkley Test for Change Detection
#
# Algorithm สำหรับ detect mean shift ใน streaming data

# %%
class PageHinkleyDetector:
    """
    Page-Hinkley test สำหรับ detect mean shift
    
    เหมาะสำหรับ:
    - Streaming data
    - Detect upward หรือ downward shifts
    - Low memory footprint
    """
    
    def __init__(self, delta=0.005, lambda_=50, alpha=0.9999):
        """
        Parameters:
        -----------
        delta : float - magnitude ที่ยอมรับได้ของ change
        lambda_ : float - detection threshold
        alpha : float - forgetting factor สำหรับ mean estimation
        """
        self.delta = delta
        self.lambda_ = lambda_
        self.alpha = alpha
        
        self.mean = 0
        self.sum = 0
        self.min_sum = float('inf')
        self.max_sum = float('-inf')
        
        self.n_samples = 0
        self.history = []
        self.drift_points = []
    
    def update(self, value, timestamp=None):
        """
        Update detector ด้วยค่าใหม่
        """
        self.n_samples += 1
        
        # Update mean
        if self.n_samples == 1:
            self.mean = value
        else:
            self.mean = self.alpha * self.mean + (1 - self.alpha) * value
        
        # Update cumulative sum
        self.sum += value - self.mean - self.delta
        
        # Update min/max
        self.min_sum = min(self.min_sum, self.sum)
        self.max_sum = max(self.max_sum, self.sum)
        
        # Calculate test statistics
        ph_positive = self.sum - self.min_sum  # Detect upward shift
        ph_negative = self.max_sum - self.sum  # Detect downward shift
        
        # Detection
        drift_up = ph_positive > self.lambda_
        drift_down = ph_negative > self.lambda_
        drift_detected = drift_up or drift_down
        
        result = {
            'timestamp': timestamp,
            'value': value,
            'mean': self.mean,
            'sum': self.sum,
            'ph_positive': ph_positive,
            'ph_negative': ph_negative,
            'drift_detected': drift_detected,
            'drift_direction': 'up' if drift_up else ('down' if drift_down else None)
        }
        
        self.history.append(result)
        
        if drift_detected:
            self.drift_points.append(self.n_samples - 1)
            self.reset()
        
        return result
    
    def reset(self):
        """Reset statistics หลัง detect drift"""
        self.sum = 0
        self.min_sum = float('inf')
        self.max_sum = float('-inf')
    
    def get_history_df(self):
        return pd.DataFrame(self.history)

# %%
# ทดสอบ Page-Hinkley
print("=" * 60)
print("🔍 Testing PAGE-HINKLEY Detector")
print("=" * 60)

ph_detector = PageHinkleyDetector(delta=0.01, lambda_=30)

# ทดสอบกับ sudden drift
for idx, row in sudden_stream.iterrows():
    result = ph_detector.update(row['value'], timestamp=row['timestamp'])
    
    if result['drift_detected']:
        print(f"⚠️ DRIFT at index {idx}: Direction = {result['drift_direction']}")

print(f"\n📊 Total drifts detected: {len(ph_detector.drift_points)}")

# %%
# Visualize Page-Hinkley results
ph_history = ph_detector.get_history_df()

fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# Plot 1: Data
ax1 = axes[0]
ax1.plot(sudden_stream['index'], sudden_stream['value'], alpha=0.3)
ax1.plot(ph_history.index, ph_history['mean'], 'r-', linewidth=2, label='Estimated Mean')
for dp in ph_detector.drift_points:
    ax1.axvline(dp, color='red', linestyle='--', alpha=0.7)
ax1.set_title('Page-Hinkley Detection')
ax1.set_ylabel('Value')
ax1.legend()

# Plot 2: PH Statistics
ax2 = axes[1]
ax2.plot(ph_history.index, ph_history['ph_positive'], 'g-', label='PH+ (upward)')
ax2.plot(ph_history.index, ph_history['ph_negative'], 'b-', label='PH- (downward)')
ax2.axhline(30, color='red', linestyle='--', label='Threshold')
ax2.set_ylabel('PH Statistics')
ax2.legend()

# Plot 3: Cumulative Sum
ax3 = axes[2]
ax3.plot(ph_history.index, ph_history['sum'], 'purple')
ax3.set_xlabel('Time Index')
ax3.set_ylabel('Cumulative Sum')

plt.tight_layout()
plt.savefig('page_hinkley_detection.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## สรุป LAB 4
#
# ### สิ่งที่เรียนรู้:
# 1. **Data Stream Simulation**: สร้าง streams ที่มี drift patterns ต่างๆ
# 2. **Sliding Window**: วิธีมาตรฐานสำหรับ streaming drift detection
# 3. **Adaptive Detection**: ปรับ reference window เมื่อ detect drift
# 4. **Page-Hinkley**: Algorithm สำหรับ mean shift detection
#
# ### Comparison:
# | Method | Pros | Cons | Best For |
# |--------|------|------|----------|
# | Sliding Window | Simple, intuitive | Fixed reference | Sudden drift |
# | Adaptive | Handles gradual drift | More complex | Production |
# | Page-Hinkley | Low memory, fast | Mean shift only | Real-time |

# %%
print("=" * 60)
print("✅ LAB 4 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Different drift types require different detection strategies
2. Sliding window is fundamental for streaming detection
3. Adaptive reference helps with gradual drift
4. Page-Hinkley is efficient for mean shift detection

🔜 Next: LAB 5 - Custom Metrics & Drift Thresholds
""")
```

---

## LAB 5: Custom Metrics & Drift Thresholds

```python
# %% [markdown]
# # LAB 5: Custom Metrics & Drift Thresholds
# ## การสร้าง Custom Drift Metrics และปรับ Thresholds
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. สร้าง custom drift metrics ที่เหมาะกับ domain
# 2. ปรับ threshold ตาม business requirements
# 3. Handle false positives/negatives ใน drift detection
#
# ### ทฤษฎี:
# Default thresholds อาจไม่เหมาะกับทุก use case:
# - บาง domain ต้องการ sensitivity สูง
# - บาง domain ยอมรับ drift ได้ระดับหนึ่ง
# - Cost of false positive vs false negative ต่างกัน

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
plt.rcParams['figure.figsize'] = (12, 6)

print("✅ Libraries imported successfully!")

# %% [markdown]
# ## ส่วนที่ 2: สร้าง Dataset สำหรับ Threshold Tuning
#
# สร้าง labeled dataset ที่รู้ว่ามี drift หรือไม่

# %%
def create_labeled_drift_dataset(n_scenarios=100):
    """
    สร้าง dataset พร้อม ground truth labels
    
    Returns:
    --------
    list of dicts: แต่ละ scenario มี reference, current, และ label
    """
    scenarios = []
    
    for i in range(n_scenarios):
        np.random.seed(i)
        n_samples = 500
        
        # Reference data
        ref_mean = 50
        ref_std = 10
        reference = np.random.normal(ref_mean, ref_std, n_samples)
        
        # กำหนดว่ามี drift หรือไม่
        has_drift = i < n_scenarios // 2  # 50% มี drift
        
        if has_drift:
            # สร้าง drift ในระดับต่างๆ
            drift_level = (i % 5 + 1) * 0.5  # 0.5, 1.0, 1.5, 2.0, 2.5 std
            current_mean = ref_mean + drift_level * ref_std
            drift_magnitude = drift_level
        else:
            # ไม่มี drift แต่มี noise เล็กน้อย
            current_mean = ref_mean + np.random.uniform(-0.1, 0.1) * ref_std
            drift_magnitude = 0
        
        current = np.random.normal(current_mean, ref_std, n_samples)
        
        scenarios.append({
            'id': i,
            'reference': reference,
            'current': current,
            'has_drift': has_drift,
            'drift_magnitude': drift_magnitude,
            'ref_mean': ref_mean,
            'current_mean': current_mean
        })
    
    return scenarios

# สร้าง dataset
scenarios = create_labeled_drift_dataset(100)

print(f"📊 Created {len(scenarios)} scenarios")
print(f"   With drift: {sum(1 for s in scenarios if s['has_drift'])}")
print(f"   Without drift: {sum(1 for s in scenarios if not s['has_drift'])}")

# %%
# Visualize drift magnitude distribution
drift_mags = [s['drift_magnitude'] for s in scenarios if s['has_drift']]
plt.figure(figsize=(10, 4))
plt.hist(drift_mags, bins=10, edgecolor='black', alpha=0.7)
plt.xlabel('Drift Magnitude (in std)')
plt.ylabel('Count')
plt.title('Distribution of Drift Magnitudes in Scenarios with Drift')
plt.show()

# %% [markdown]
# ## ส่วนที่ 3: สร้าง Custom Drift Metrics

# %%
class CustomDriftMetrics:
    """
    Class สำหรับคำนวณ custom drift metrics
    """
    
    @staticmethod
    def psi(reference, current, bins=10):
        """Population Stability Index"""
        breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        ref_counts, _ = np.histogram(reference, bins=breakpoints)
        cur_counts, _ = np.histogram(current, bins=breakpoints)
        
        eps = 1e-6
        ref_props = ref_counts / len(reference) + eps
        cur_props = cur_counts / len(current) + eps
        
        return np.sum((cur_props - ref_props) * np.log(cur_props / ref_props))
    
    @staticmethod
    def normalized_wasserstein(reference, current):
        """Wasserstein distance normalized by reference std"""
        distance = stats.wasserstein_distance(reference, current)
        return distance / np.std(reference)
    
    @staticmethod
    def mean_shift_ratio(reference, current):
        """Mean shift as ratio of reference std"""
        mean_diff = abs(np.mean(current) - np.mean(reference))
        return mean_diff / np.std(reference)
    
    @staticmethod
    def std_ratio(reference, current):
        """Ratio of standard deviations"""
        return np.std(current) / np.std(reference)
    
    @staticmethod
    def percentile_shift(reference, current, percentiles=[25, 50, 75]):
        """Average shift in percentiles"""
        shifts = []
        ref_std = np.std(reference)
        
        for p in percentiles:
            ref_p = np.percentile(reference, p)
            cur_p = np.percentile(current, p)
            shifts.append(abs(cur_p - ref_p) / ref_std)
        
        return np.mean(shifts)
    
    @staticmethod
    def jensen_shannon_divergence(reference, current, bins=10):
        """Jensen-Shannon divergence"""
        # สร้าง histograms
        all_data = np.concatenate([reference, current])
        bins = np.histogram_bin_edges(all_data, bins=bins)
        
        ref_hist, _ = np.histogram(reference, bins=bins, density=True)
        cur_hist, _ = np.histogram(current, bins=bins, density=True)
        
        # Normalize
        ref_hist = ref_hist / (ref_hist.sum() + 1e-10)
        cur_hist = cur_hist / (cur_hist.sum() + 1e-10)
        
        # Average distribution
        m = 0.5 * (ref_hist + cur_hist)
        
        # KL divergences
        kl_pm = np.sum(ref_hist * np.log((ref_hist + 1e-10) / (m + 1e-10)))
        kl_qm = np.sum(cur_hist * np.log((cur_hist + 1e-10) / (m + 1e-10)))
        
        return 0.5 * (kl_pm + kl_qm)
    
    @staticmethod
    def combined_score(reference, current, weights=None):
        """
        Combined drift score จากหลาย metrics
        
        Default weights: PSI=0.3, Wasserstein=0.3, Mean Shift=0.2, Percentile=0.2
        """
        if weights is None:
            weights = {
                'psi': 0.3,
                'wasserstein': 0.3,
                'mean_shift': 0.2,
                'percentile': 0.2
            }
        
        metrics = CustomDriftMetrics
        
        # Normalize each metric to 0-1 range
        psi = min(metrics.psi(reference, current), 1.0)  # Cap at 1
        wasserstein = min(metrics.normalized_wasserstein(reference, current) / 3, 1.0)  # 3 std = max
        mean_shift = min(metrics.mean_shift_ratio(reference, current) / 3, 1.0)
        percentile = min(metrics.percentile_shift(reference, current) / 3, 1.0)
        
        score = (
            weights['psi'] * psi +
            weights['wasserstein'] * wasserstein +
            weights['mean_shift'] * mean_shift +
            weights['percentile'] * percentile
        )
        
        return score

# %%
# ทดสอบ custom metrics
print("=" * 60)
print("📊 Testing Custom Drift Metrics")
print("=" * 60)

# เลือก scenarios ที่มี drift levels ต่างๆ
test_scenarios = [s for s in scenarios if s['drift_magnitude'] in [0, 0.5, 1.0, 2.0]][:8]

metrics_results = []
for s in test_scenarios:
    result = {
        'id': s['id'],
        'has_drift': s['has_drift'],
        'magnitude': s['drift_magnitude'],
        'psi': CustomDriftMetrics.psi(s['reference'], s['current']),
        'wasserstein': CustomDriftMetrics.normalized_wasserstein(s['reference'], s['current']),
        'mean_shift': CustomDriftMetrics.mean_shift_ratio(s['reference'], s['current']),
        'percentile': CustomDriftMetrics.percentile_shift(s['reference'], s['current']),
        'js_div': CustomDriftMetrics.jensen_shannon_divergence(s['reference'], s['current']),
        'combined': CustomDriftMetrics.combined_score(s['reference'], s['current'])
    }
    metrics_results.append(result)

metrics_df = pd.DataFrame(metrics_results)
print(metrics_df.to_string(index=False))

# %% [markdown]
# ## ส่วนที่ 4: Threshold Optimization
#
# หา optimal threshold โดยใช้ labeled data

# %%
def calculate_metrics_for_threshold(scenarios, metric_func, threshold):
    """
    คำนวณ precision, recall, f1 สำหรับ threshold ที่กำหนด
    """
    y_true = []
    y_pred = []
    
    for s in scenarios:
        y_true.append(1 if s['has_drift'] else 0)
        
        score = metric_func(s['reference'], s['current'])
        y_pred.append(1 if score > threshold else 0)
    
    # Handle edge cases
    if sum(y_pred) == 0:
        return {'precision': 0, 'recall': 0, 'f1': 0}
    
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    return {'precision': precision, 'recall': recall, 'f1': f1}

def find_optimal_threshold(scenarios, metric_func, thresholds, optimize_for='f1'):
    """
    หา optimal threshold
    """
    results = []
    
    for t in thresholds:
        metrics = calculate_metrics_for_threshold(scenarios, metric_func, t)
        metrics['threshold'] = t
        results.append(metrics)
    
    results_df = pd.DataFrame(results)
    
    # หา optimal
    optimal_idx = results_df[optimize_for].idxmax()
    optimal = results_df.iloc[optimal_idx]
    
    return results_df, optimal

# %%
# หา optimal threshold สำหรับ PSI
thresholds = np.linspace(0.01, 0.5, 50)

psi_results, psi_optimal = find_optimal_threshold(
    scenarios, 
    CustomDriftMetrics.psi, 
    thresholds
)

print("=" * 60)
print("📊 PSI Threshold Optimization")
print("=" * 60)
print(f"Optimal threshold: {psi_optimal['threshold']:.3f}")
print(f"Precision: {psi_optimal['precision']:.3f}")
print(f"Recall: {psi_optimal['recall']:.3f}")
print(f"F1 Score: {psi_optimal['f1']:.3f}")

# %%
# Visualize threshold optimization
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

metrics_to_plot = ['precision', 'recall', 'f1']
colors = ['blue', 'green', 'red']

for ax, metric, color in zip(axes, metrics_to_plot, colors):
    ax.plot(psi_results['threshold'], psi_results[metric], f'{color}-', linewidth=2)
    ax.axvline(psi_optimal['threshold'], color='black', linestyle='--', 
               label=f'Optimal ({psi_optimal["threshold"]:.3f})')
    ax.set_xlabel('PSI Threshold')
    ax.set_ylabel(metric.capitalize())
    ax.set_title(f'{metric.capitalize()} vs Threshold')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.suptitle('PSI Threshold Optimization', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('threshold_optimization_psi.png', dpi=150, bbox_inches='tight')
plt.show()

# %%
# เปรียบเทียบ optimal thresholds ของแต่ละ metric
print("=" * 60)
print("📊 Comparing Optimal Thresholds for Different Metrics")
print("=" * 60)

metrics_funcs = {
    'PSI': CustomDriftMetrics.psi,
    'Normalized Wasserstein': CustomDriftMetrics.normalized_wasserstein,
    'Mean Shift Ratio': CustomDriftMetrics.mean_shift_ratio,
    'Combined Score': CustomDriftMetrics.combined_score
}

threshold_ranges = {
    'PSI': np.linspace(0.01, 0.5, 50),
    'Normalized Wasserstein': np.linspace(0.01, 2.0, 50),
    'Mean Shift Ratio': np.linspace(0.01, 2.0, 50),
    'Combined Score': np.linspace(0.01, 0.5, 50)
}

optimal_thresholds = {}
for name, func in metrics_funcs.items():
    results, optimal = find_optimal_threshold(scenarios, func, threshold_ranges[name])
    optimal_thresholds[name] = optimal
    print(f"\n{name}:")
    print(f"  Optimal threshold: {optimal['threshold']:.3f}")
    print(f"  F1 Score: {optimal['f1']:.3f}")

# %% [markdown]
# ## ส่วนที่ 5: Business-driven Threshold Setting
#
# ปรับ threshold ตาม business requirements

# %%
class BusinessDriftThreshold:
    """
    Class สำหรับกำหนด threshold ตาม business context
    """
    
    def __init__(self, false_positive_cost=1, false_negative_cost=10):
        """
        Parameters:
        -----------
        false_positive_cost : float - cost ของ false alarm
        false_negative_cost : float - cost ของ missing drift
        """
        self.fp_cost = false_positive_cost
        self.fn_cost = false_negative_cost
    
    def calculate_total_cost(self, y_true, y_pred):
        """คำนวณ total cost"""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return fp * self.fp_cost + fn * self.fn_cost
    
    def find_cost_optimal_threshold(self, scenarios, metric_func, thresholds):
        """หา threshold ที่ minimize total cost"""
        costs = []
        
        for t in thresholds:
            y_true = [1 if s['has_drift'] else 0 for s in scenarios]
            y_pred = [1 if metric_func(s['reference'], s['current']) > t else 0 for s in scenarios]
            
            cost = self.calculate_total_cost(y_true, y_pred)
            costs.append({'threshold': t, 'cost': cost})
        
        cost_df = pd.DataFrame(costs)
        optimal_idx = cost_df['cost'].idxmin()
        return cost_df, cost_df.iloc[optimal_idx]

# %%
# เปรียบเทียบ threshold สำหรับ scenarios ต่างๆ
print("=" * 60)
print("📊 Business-driven Threshold Optimization")
print("=" * 60)

# Scenario 1: High cost of missing drift (e.g., fraud detection)
print("\n🔴 Scenario 1: High cost of missing drift (FN cost = 10x)")
high_fn_cost = BusinessDriftThreshold(false_positive_cost=1, false_negative_cost=10)
cost_df_1, optimal_1 = high_fn_cost.find_cost_optimal_threshold(
    scenarios, CustomDriftMetrics.psi, thresholds
)
print(f"   Optimal threshold: {optimal_1['threshold']:.3f}")
print(f"   Total cost: {optimal_1['cost']:.0f}")

# Scenario 2: High cost of false alarms (e.g., model retraining is expensive)
print("\n🟡 Scenario 2: High cost of false alarms (FP cost = 10x)")
high_fp_cost = BusinessDriftThreshold(false_positive_cost=10, false_negative_cost=1)
cost_df_2, optimal_2 = high_fp_cost.find_cost_optimal_threshold(
    scenarios, CustomDriftMetrics.psi, thresholds
)
print(f"   Optimal threshold: {optimal_2['threshold']:.3f}")
print(f"   Total cost: {optimal_2['cost']:.0f}")

# Scenario 3: Balanced costs
print("\n🟢 Scenario 3: Balanced costs (FP = FN)")
balanced_cost = BusinessDriftThreshold(false_positive_cost=1, false_negative_cost=1)
cost_df_3, optimal_3 = balanced_cost.find_cost_optimal_threshold(
    scenarios, CustomDriftMetrics.psi, thresholds
)
print(f"   Optimal threshold: {optimal_3['threshold']:.3f}")
print(f"   Total cost: {optimal_3['cost']:.0f}")

# %%
# Visualize cost-based optimization
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

scenarios_data = [
    (cost_df_1, optimal_1, 'High FN Cost (10x)', 'red'),
    (cost_df_2, optimal_2, 'High FP Cost (10x)', 'orange'),
    (cost_df_3, optimal_3, 'Balanced Cost', 'green')
]

for ax, (cost_df, optimal, title, color) in zip(axes, scenarios_data):
    ax.plot(cost_df['threshold'], cost_df['cost'], f'{color[0]}-', linewidth=2)
    ax.axvline(optimal['threshold'], color='black', linestyle='--',
               label=f'Optimal ({optimal["threshold"]:.3f})')
    ax.scatter([optimal['threshold']], [optimal['cost']], color='black', s=100, zorder=5)
    ax.set_xlabel('PSI Threshold')
    ax.set_ylabel('Total Cost')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cost_based_optimization.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n💡 Insight:")
print("   - High FN cost → Lower threshold (detect more, accept false alarms)")
print("   - High FP cost → Higher threshold (be more conservative)")
print("   - Balanced → Somewhere in between")

# %% [markdown]
# ## ส่วนที่ 6: Handling False Positives/Negatives

# %%
class RobustDriftDetector:
    """
    Drift detector ที่มี mechanisms สำหรับ handle FP/FN
    """
    
    def __init__(self, primary_metric='psi', primary_threshold=0.1,
                 confirmation_window=3, use_ensemble=True):
        """
        Parameters:
        -----------
        primary_metric : str - metric หลัก
        primary_threshold : float - threshold หลัก
        confirmation_window : int - ต้อง detect กี่ครั้งติดกัน
        use_ensemble : bool - ใช้หลาย metrics ร่วมกัน
        """
        self.primary_metric = primary_metric
        self.primary_threshold = primary_threshold
        self.confirmation_window = confirmation_window
        self.use_ensemble = use_ensemble
        
        self.metrics = CustomDriftMetrics()
        
        # Thresholds for ensemble
        self.thresholds = {
            'psi': 0.1,
            'wasserstein': 0.5,
            'mean_shift': 0.5,
            'percentile': 0.3
        }
        
        self.consecutive_count = 0
        self.history = []
    
    def _calculate_all_metrics(self, reference, current):
        """คำนวณทุก metrics"""
        return {
            'psi': self.metrics.psi(reference, current),
            'wasserstein': self.metrics.normalized_wasserstein(reference, current),
            'mean_shift': self.metrics.mean_shift_ratio(reference, current),
            'percentile': self.metrics.percentile_shift(reference, current)
        }
    
    def detect(self, reference, current):
        """
        Detect drift with robustness mechanisms
        """
        all_metrics = self._calculate_all_metrics(reference, current)
        
        # Single metric detection
        primary_value = all_metrics[self.primary_metric]
        primary_drift = primary_value > self.primary_threshold
        
        if self.use_ensemble:
            # Ensemble: majority voting
            drift_votes = sum(
                1 for m, v in all_metrics.items() 
                if v > self.thresholds.get(m, 0.5)
            )
            ensemble_drift = drift_votes >= 3  # ต้อง 3/4 metrics agree
        else:
            ensemble_drift = primary_drift
        
        # Confirmation mechanism
        if ensemble_drift:
            self.consecutive_count += 1
        else:
            self.consecutive_count = 0
        
        confirmed_drift = self.consecutive_count >= self.confirmation_window
        
        result = {
            'metrics': all_metrics,
            'primary_drift': primary_drift,
            'ensemble_drift': ensemble_drift,
            'consecutive_count': self.consecutive_count,
            'confirmed_drift': confirmed_drift
        }
        
        self.history.append(result)
        
        return result
    
    def evaluate(self, scenarios):
        """
        Evaluate detector performance on labeled scenarios
        """
        y_true = []
        y_pred_primary = []
        y_pred_ensemble = []
        y_pred_confirmed = []
        
        for s in scenarios:
            y_true.append(1 if s['has_drift'] else 0)
            
            result = self.detect(s['reference'], s['current'])
            y_pred_primary.append(1 if result['primary_drift'] else 0)
            y_pred_ensemble.append(1 if result['ensemble_drift'] else 0)
            y_pred_confirmed.append(1 if result['confirmed_drift'] else 0)
            
            # Reset for next scenario
            self.consecutive_count = 0
        
        evaluations = {}
        for name, y_pred in [
            ('primary', y_pred_primary),
            ('ensemble', y_pred_ensemble),
            ('confirmed', y_pred_confirmed)
        ]:
            evaluations[name] = {
                'precision': precision_score(y_true, y_pred, zero_division=0),
                'recall': recall_score(y_true, y_pred, zero_division=0),
                'f1': f1_score(y_true, y_pred, zero_division=0)
            }
        
        return evaluations

# %%
# ทดสอบ RobustDriftDetector
print("=" * 60)
print("📊 Evaluating Robust Drift Detector")
print("=" * 60)

detector = RobustDriftDetector(
    primary_metric='psi',
    primary_threshold=0.1,
    confirmation_window=1,  # ลดเหลือ 1 สำหรับ single scenario testing
    use_ensemble=True
)

evaluations = detector.evaluate(scenarios)

for method, metrics in evaluations.items():
    print(f"\n{method.upper()} Method:")
    print(f"  Precision: {metrics['precision']:.3f}")
    print(f"  Recall: {metrics['recall']:.3f}")
    print(f"  F1 Score: {metrics['f1']:.3f}")

# %%
# Visualize comparison
fig, ax = plt.subplots(figsize=(10, 6))

methods = list(evaluations.keys())
x = np.arange(len(methods))
width = 0.25

metrics_names = ['precision', 'recall', 'f1']
colors = ['blue', 'green', 'red']

for i, (metric, color) in enumerate(zip(metrics_names, colors)):
    values = [evaluations[m][metric] for m in methods]
    ax.bar(x + i * width, values, width, label=metric.capitalize(), color=color, alpha=0.7)

ax.set_ylabel('Score')
ax.set_xlabel('Detection Method')
ax.set_title('Comparison of Detection Methods')
ax.set_xticks(x + width)
ax.set_xticklabels([m.capitalize() for m in methods])
ax.legend()
ax.set_ylim(0, 1)

for i, (metric, color) in enumerate(zip(metrics_names, colors)):
    values = [evaluations[m][metric] for m in methods]
    for j, v in enumerate(values):
        ax.text(x[j] + i * width, v + 0.02, f'{v:.2f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('detection_methods_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## ส่วนที่ 7: สรุปและ Best Practices

# %%
print("=" * 70)
print("📋 THRESHOLD SETTING BEST PRACTICES")
print("=" * 70)

best_practices = """
1️⃣ DOMAIN-SPECIFIC THRESHOLDS
   - ไม่ใช้ default thresholds โดยไม่ validate
   - ทดสอบกับ labeled data ถ้ามี
   - ปรึกษากับ domain experts

2️⃣ COST-BASED OPTIMIZATION
   - พิจารณา cost ของ FP vs FN
   - FN แพง → Lower threshold (more sensitive)
   - FP แพง → Higher threshold (more conservative)

3️⃣ ENSEMBLE APPROACH
   - ใช้หลาย metrics ร่วมกัน
   - Voting mechanism ลด false positives
   - ถ้า metrics ไม่ agree → investigate further

4️⃣ CONFIRMATION MECHANISM
   - Require consecutive detections
   - ป้องกัน temporary spikes
   - Trade-off: delay detection

5️⃣ PERIODIC REVIEW
   - Review thresholds เป็นระยะ
   - Data patterns อาจเปลี่ยน
   - Business requirements อาจเปลี่ยน

6️⃣ MONITORING & ALERTING
   - Different severity levels
   - Different thresholds for warning vs critical
   - Escalation procedures
"""

print(best_practices)

# %% [markdown]
# ## สรุป LAB 5
#
# ### สิ่งที่เรียนรู้:
# 1. **Custom Metrics**: PSI, Wasserstein, Mean Shift, Combined Score
# 2. **Threshold Optimization**: ใช้ labeled data หา optimal threshold
# 3. **Cost-based Approach**: ปรับ threshold ตาม FP/FN costs
# 4. **Robust Detection**: Ensemble + Confirmation mechanisms

# %%
print("=" * 60)
print("✅ LAB 5 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Default thresholds rarely optimal for your use case
2. Use labeled data to optimize thresholds
3. Consider business costs of FP vs FN
4. Ensemble methods reduce false alarms
5. Confirmation window adds robustness

🔜 Next: LAB 6 - End-to-End Monitoring Pipeline
""")
```

---

## LAB 6: End-to-End Monitoring Pipeline

```python
# %% [markdown]
# # LAB 6: End-to-End Monitoring Pipeline
# ## สร้าง Pipeline สำหรับ Drift Monitoring แบบครบวงจร
#
# ### วัตถุประสงค์การเรียนรู้:
# 1. รวมทุก components เข้าด้วยกัน
# 2. สร้าง automated monitoring workflow
# 3. Integrate กับ MLflow สำหรับ experiment tracking
#
# ### ทฤษฎี:
# Production ML monitoring ต้องการ:
# - Automated data ingestion
# - Real-time drift detection
# - Alerting mechanisms
# - Experiment tracking
# - Dashboard และ reporting

# %% [markdown]
# ## ส่วนที่ 1: เตรียม Environment

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import stats
import json
import os
import logging
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

np.random.seed(42)
plt.rcParams['figure.figsize'] = (14, 6)

print("✅ Libraries imported successfully!")

# สร้าง directory สำหรับ output
os.makedirs('monitoring_output', exist_ok=True)
os.makedirs('monitoring_output/reports', exist_ok=True)
os.makedirs('monitoring_output/alerts', exist_ok=True)

# %% [markdown]
# ## ส่วนที่ 2: สร้าง Data Classes และ Utilities

# %%
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class DriftType(Enum):
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

@dataclass
class DriftResult:
    """ผลลัพธ์การตรวจจับ drift"""
    timestamp: datetime
    feature: str
    drift_detected: bool
    drift_type: DriftType
    psi: float
    ks_statistic: float
    ks_pvalue: float
    reference_mean: float
    current_mean: float
    reference_std: float
    current_std: float
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'feature': self.feature,
            'drift_detected': self.drift_detected,
            'drift_type': self.drift_type.value,
            'psi': self.psi,
            'ks_statistic': self.ks_statistic,
            'ks_pvalue': self.ks_pvalue,
            'reference_mean': self.reference_mean,
            'current_mean': self.current_mean,
            'reference_std': self.reference_std,
            'current_std': self.current_std
        }

@dataclass
class Alert:
    """Alert object"""
    timestamp: datetime
    severity: AlertSeverity
    message: str
    details: Dict
    acknowledged: bool = False
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'severity': self.severity.value,
            'message': self.message,
            'details': self.details,
            'acknowledged': self.acknowledged
        }

@dataclass
class MonitoringConfig:
    """Configuration สำหรับ monitoring"""
    reference_window_size: int = 1000
    current_window_size: int = 200
    psi_mild_threshold: float = 0.1
    psi_moderate_threshold: float = 0.2
    psi_severe_threshold: float = 0.25
    ks_significance: float = 0.05
    check_interval_seconds: int = 60
    alert_cooldown_minutes: int = 30
    features_to_monitor: List[str] = field(default_factory=list)

# %% [markdown]
# ## ส่วนที่ 3: สร้าง Core Monitoring Components

# %%
class DriftCalculator:
    """
    Component สำหรับคำนวณ drift metrics
    """
    
    @staticmethod
    def calculate_psi(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
        """Calculate Population Stability Index"""
        breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
        breakpoints = np.unique(breakpoints)
        
        if len(breakpoints) < 2:
            return 0.0
        
        ref_counts, _ = np.histogram(reference, bins=breakpoints)
        cur_counts, _ = np.histogram(current, bins=breakpoints)
        
        eps = 1e-6
        ref_props = ref_counts / len(reference) + eps
        cur_props = cur_counts / len(current) + eps
        
        psi = np.sum((cur_props - ref_props) * np.log(cur_props / ref_props))
        return float(psi)
    
    @staticmethod
    def calculate_ks_test(reference: np.ndarray, current: np.ndarray) -> tuple:
        """Calculate Kolmogorov-Smirnov test"""
        statistic, pvalue = stats.ks_2samp(reference, current)
        return float(statistic), float(pvalue)
    
    @staticmethod
    def determine_drift_type(psi: float, config: MonitoringConfig) -> DriftType:
        """Determine drift severity based on PSI"""
        if psi >= config.psi_severe_threshold:
            return DriftType.SEVERE
        elif psi >= config.psi_moderate_threshold:
            return DriftType.MODERATE
        elif psi >= config.psi_mild_threshold:
            return DriftType.MILD
        return DriftType.NONE

# %%
class DataBuffer:
    """
    Buffer สำหรับเก็บ reference และ current data
    """
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.reference_data: Dict[str, deque] = {}
        self.current_data: Dict[str, deque] = {}
        self.is_initialized = False
        
    def initialize(self, reference_df: pd.DataFrame):
        """Initialize with reference data"""
        for feature in self.config.features_to_monitor:
            if feature in reference_df.columns:
                self.reference_data[feature] = deque(
                    reference_df[feature].values[-self.config.reference_window_size:],
                    maxlen=self.config.reference_window_size
                )
                self.current_data[feature] = deque(
                    maxlen=self.config.current_window_size
                )
        self.is_initialized = True
        logger.info(f"DataBuffer initialized with {len(self.reference_data)} features")
    
    def add_data(self, data: Dict[str, float]):
        """Add new data point"""
        for feature, value in data.items():
            if feature in self.current_data:
                self.current_data[feature].append(value)
    
    def get_reference(self, feature: str) -> Optional[np.ndarray]:
        """Get reference data for a feature"""
        if feature in self.reference_data:
            return np.array(self.reference_data[feature])
        return None
    
    def get_current(self, feature: str) -> Optional[np.ndarray]:
        """Get current data for a feature"""
        if feature in self.current_data:
            return np.array(self.current_data[feature])
        return None
    
    def is_current_ready(self) -> bool:
        """Check if current buffer has enough data"""
        for feature in self.config.features_to_monitor:
            if feature in self.current_data:
                if len(self.current_data[feature]) < self.config.current_window_size:
                    return False
        return True
    
    def update_reference(self):
        """Update reference with current data"""
        for feature in self.config.features_to_monitor:
            if feature in self.current_data and len(self.current_data[feature]) > 0:
                # Add current data to reference
                for val in self.current_data[feature]:
                    self.reference_data[feature].append(val)
                self.current_data[feature].clear()
        logger.info("Reference data updated with current window")

# %%
class AlertManager:
    """
    Component สำหรับจัดการ alerts
    """
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.alerts: List[Alert] = []
        self.last_alert_time: Dict[str, datetime] = {}
    
    def should_alert(self, feature: str) -> bool:
        """Check if we should send alert (cooldown)"""
        if feature not in self.last_alert_time:
            return True
        
        elapsed = datetime.now() - self.last_alert_time[feature]
        return elapsed > timedelta(minutes=self.config.alert_cooldown_minutes)
    
    def create_alert(self, drift_result: DriftResult) -> Optional[Alert]:
        """Create alert based on drift result"""
        if not drift_result.drift_detected:
            return None
        
        if not self.should_alert(drift_result.feature):
            return None
        
        # Determine severity
        if drift_result.drift_type == DriftType.SEVERE:
            severity = AlertSeverity.CRITICAL
        elif drift_result.drift_type == DriftType.MODERATE:
            severity = AlertSeverity.WARNING
        else:
            severity = AlertSeverity.INFO
        
        message = (
            f"Drift detected in feature '{drift_result.feature}': "
            f"PSI={drift_result.psi:.4f}, Type={drift_result.drift_type.value}"
        )
        
        alert = Alert(
            timestamp=drift_result.timestamp,
            severity=severity,
            message=message,
            details=drift_result.to_dict()
        )
        
        self.alerts.append(alert)
        self.last_alert_time[drift_result.feature] = datetime.now()
        
        # Log based on severity
        if severity == AlertSeverity.CRITICAL:
            logger.critical(message)
        elif severity == AlertSeverity.WARNING:
            logger.warning(message)
        else:
            logger.info(message)
        
        return alert
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unacknowledged alerts"""
        return [a for a in self.alerts if not a.acknowledged]
    
    def acknowledge_alert(self, index: int):
        """Acknowledge an alert"""
        if 0 <= index < len(self.alerts):
            self.alerts[index].acknowledged = True
    
    def save_alerts(self, filepath: str):
        """Save alerts to file"""
        alerts_data = [a.to_dict() for a in self.alerts]
        with open(filepath, 'w') as f:
            json.dump(alerts_data, f, indent=2)

# %% [markdown]
# ## ส่วนที่ 4: สร้าง Main Monitoring Pipeline

# %%
class DriftMonitoringPipeline:
    """
    Main pipeline สำหรับ drift monitoring
    """
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.data_buffer = DataBuffer(config)
        self.alert_manager = AlertManager(config)
        self.drift_calculator = DriftCalculator()
        self.results_history: List[DriftResult] = []
        self.is_running = False
        
    def initialize(self, reference_data: pd.DataFrame):
        """Initialize pipeline with reference data"""
        self.data_buffer.initialize(reference_data)
        logger.info("DriftMonitoringPipeline initialized")
    
    def process_batch(self, batch_data: pd.DataFrame) -> List[DriftResult]:
        """Process a batch of new data"""
        results = []
        
        # Add data to buffer
        for idx, row in batch_data.iterrows():
            data_point = {f: row[f] for f in self.config.features_to_monitor if f in row}
            self.data_buffer.add_data(data_point)
        
        # Check if ready for drift detection
        if not self.data_buffer.is_current_ready():
            logger.debug("Current buffer not ready yet")
            return results
        
        # Perform drift detection for each feature
        for feature in self.config.features_to_monitor:
            result = self._detect_drift_for_feature(feature)
            if result:
                results.append(result)
                self.results_history.append(result)
                
                # Create alert if needed
                if result.drift_detected:
                    self.alert_manager.create_alert(result)
        
        return results
    
    def _detect_drift_for_feature(self, feature: str) -> Optional[DriftResult]:
        """Detect drift for a single feature"""
        reference = self.data_buffer.get_reference(feature)
        current = self.data_buffer.get_current(feature)
        
        if reference is None or current is None:
            return None
        
        if len(current) < 10:  # Need minimum samples
            return None
        
        # Calculate metrics
        psi = self.drift_calculator.calculate_psi(reference, current)
        ks_stat, ks_pval = self.drift_calculator.calculate_ks_test(reference, current)
        
        # Determine drift type
        drift_type = self.drift_calculator.determine_drift_type(psi, self.config)
        drift_detected = drift_type != DriftType.NONE or ks_pval < self.config.ks_significance
        
        return DriftResult(
            timestamp=datetime.now(),
            feature=feature,
            drift_detected=drift_detected,
            drift_type=drift_type,
            psi=psi,
            ks_statistic=ks_stat,
            ks_pvalue=ks_pval,
            reference_mean=float(np.mean(reference)),
            current_mean=float(np.mean(current)),
            reference_std=float(np.std(reference)),
            current_std=float(np.std(current))
        )
    
    def get_summary_report(self) -> Dict:
        """Generate summary report"""
        if not self.results_history:
            return {'status': 'no_data'}
        
        # Group by feature
        feature_summary = {}
        for feature in self.config.features_to_monitor:
            feature_results = [r for r in self.results_history if r.feature == feature]
            if feature_results:
                latest = feature_results[-1]
                drift_count = sum(1 for r in feature_results if r.drift_detected)
                feature_summary[feature] = {
                    'latest_psi': latest.psi,
                    'latest_drift_type': latest.drift_type.value,
                    'drift_count': drift_count,
                    'total_checks': len(feature_results),
                    'drift_rate': drift_count / len(feature_results)
                }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_checks': len(self.results_history),
            'total_drifts_detected': sum(1 for r in self.results_history if r.drift_detected),
            'active_alerts': len(self.alert_manager.get_active_alerts()),
            'feature_summary': feature_summary
        }
    
    def save_results(self, output_dir: str = 'monitoring_output'):
        """Save all results to files"""
        # Save drift results
        results_data = [r.to_dict() for r in self.results_history]
        with open(f'{output_dir}/drift_results.json', 'w') as f:
            json.dump(results_data, f, indent=2)
        
        # Save alerts
        self.alert_manager.save_alerts(f'{output_dir}/alerts/alerts.json')
        
        # Save summary
        summary = self.get_summary_report()
        with open(f'{output_dir}/reports/summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Results saved to {output_dir}")

# %% [markdown]
# ## ส่วนที่ 5: สร้าง Report Generator

# %%
class ReportGenerator:
    """
    Component สำหรับสร้าง reports และ visualizations
    """
    
    def __init__(self, pipeline: DriftMonitoringPipeline):
        self.pipeline = pipeline
    
    def generate_dashboard_data(self) -> Dict:
        """Generate data for dashboard"""
        summary = self.pipeline.get_summary_report()
        
        # Time series data for each feature
        time_series = {}
        for feature in self.pipeline.config.features_to_monitor:
            feature_results = [
                r for r in self.pipeline.results_history 
                if r.feature == feature
            ]
            time_series[feature] = {
                'timestamps': [r.timestamp.isoformat() for r in feature_results],
                'psi_values': [r.psi for r in feature_results],
                'drift_types': [r.drift_type.value for r in feature_results]
            }
        
        return {
            'summary': summary,
            'time_series': time_series,
            'alerts': [a.to_dict() for a in self.pipeline.alert_manager.get_active_alerts()]
        }
    
    def plot_drift_trends(self, save_path: str = None):
        """Plot drift trends for all features"""
        n_features = len(self.pipeline.config.features_to_monitor)
        
        if n_features == 0:
            logger.warning("No features to plot")
            return
        
        fig, axes = plt.subplots(n_features, 1, figsize=(14, 4*n_features), sharex=True)
        
        if n_features == 1:
            axes = [axes]
        
        colors = {'none': 'green', 'mild': 'yellow', 'moderate': 'orange', 'severe': 'red'}
        
        for ax, feature in zip(axes, self.pipeline.config.features_to_monitor):
            feature_results = [
                r for r in self.pipeline.results_history 
                if r.feature == feature
            ]
            
            if not feature_results:
                continue
            
            timestamps = [r.timestamp for r in feature_results]
            psi_values = [r.psi for r in feature_results]
            drift_types = [r.drift_type.value for r in feature_results]
            
            # Plot PSI
            scatter_colors = [colors.get(dt, 'gray') for dt in drift_types]
            ax.scatter(timestamps, psi_values, c=scatter_colors, s=30, alpha=0.7)
            ax.plot(timestamps, psi_values, 'b-', alpha=0.3)
            
            # Add thresholds
            ax.axhline(self.pipeline.config.psi_mild_threshold, 
                      color='yellow', linestyle='--', alpha=0.7, label='Mild')
            ax.axhline(self.pipeline.config.psi_moderate_threshold, 
                      color='orange', linestyle='--', alpha=0.7, label='Moderate')
            ax.axhline(self.pipeline.config.psi_severe_threshold, 
                      color='red', linestyle='--', alpha=0.7, label='Severe')
            
            ax.set_ylabel(f'{feature}\nPSI')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
        
        axes[-1].set_xlabel('Time')
        plt.suptitle('Drift Monitoring Dashboard', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")
        
        plt.show()
    
    def generate_html_report(self, output_path: str):
        """Generate HTML report"""
        summary = self.pipeline.get_summary_report()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Drift Monitoring Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; margin: 10px 0; }}
                .alert-critical {{ background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 5px 0; }}
                .alert-warning {{ background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 5px 0; }}
                .alert-info {{ background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 10px; margin: 5px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #2196F3; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 Drift Monitoring Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total Checks:</strong> {summary.get('total_checks', 0)}</p>
                <p><strong>Total Drifts Detected:</strong> {summary.get('total_drifts_detected', 0)}</p>
                <p><strong>Active Alerts:</strong> {summary.get('active_alerts', 0)}</p>
            </div>
            
            <h2>📈 Feature Summary</h2>
            <table>
                <tr>
                    <th>Feature</th>
                    <th>Latest PSI</th>
                    <th>Drift Type</th>
                    <th>Drift Count</th>
                    <th>Drift Rate</th>
                </tr>
        """
        
        for feature, data in summary.get('feature_summary', {}).items():
            html_content += f"""
                <tr>
                    <td>{feature}</td>
                    <td>{data['latest_psi']:.4f}</td>
                    <td>{data['latest_drift_type']}</td>
                    <td>{data['drift_count']}</td>
                    <td>{data['drift_rate']:.1%}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>⚠️ Active Alerts</h2>
        """
        
        for alert in self.pipeline.alert_manager.get_active_alerts():
            alert_class = f"alert-{alert.severity.value}"
            html_content += f"""
            <div class="{alert_class}">
                <strong>{alert.severity.value.upper()}</strong>: {alert.message}
                <br><small>{alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</small>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved to {output_path}")

# %% [markdown]
# ## ส่วนที่ 6: ทดสอบ Full Pipeline

# %%
# สร้าง test data
def generate_test_data(n_samples=5000):
    """สร้างข้อมูลทดสอบที่มี drift"""
    np.random.seed(42)
    
    data = []
    base_means = {'feature_a': 50, 'feature_b': 100, 'feature_c': 75}
    
    for i in range(n_samples):
        # สร้าง drift ที่ feature_a หลัง sample 3000
        if i < 3000:
            feature_a_mean = base_means['feature_a']
        else:
            # Gradual drift
            progress = (i - 3000) / 2000
            feature_a_mean = base_means['feature_a'] + progress * 20
        
        # สร้าง sudden drift ที่ feature_b ที่ sample 2000
        if i < 2000:
            feature_b_mean = base_means['feature_b']
        else:
            feature_b_mean = base_means['feature_b'] + 30
        
        # feature_c ไม่มี drift
        feature_c_mean = base_means['feature_c']
        
        data.append({
            'timestamp': datetime(2024, 1, 1) + timedelta(hours=i),
            'feature_a': np.random.normal(feature_a_mean, 10),
            'feature_b': np.random.normal(feature_b_mean, 15),
            'feature_c': np.random.normal(feature_c_mean, 12)
        })
    
    return pd.DataFrame(data)

# สร้างข้อมูลทดสอบ
test_data = generate_test_data(5000)
print(f"📊 Test data shape: {test_data.shape}")
print(test_data.head())

# %%
# Visualize test data
fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

for ax, feature in zip(axes, ['feature_a', 'feature_b', 'feature_c']):
    ax.plot(test_data['timestamp'], test_data[feature], alpha=0.3)
    rolling_mean = test_data[feature].rolling(100).mean()
    ax.plot(test_data['timestamp'], rolling_mean, 'r-', linewidth=2, label='Rolling Mean')
    ax.set_ylabel(feature)
    ax.legend()

axes[0].set_title('Test Data with Drift Patterns')
axes[-1].set_xlabel('Time')
plt.tight_layout()
plt.show()

# %%
# Configure และ run pipeline
config = MonitoringConfig(
    reference_window_size=1000,
    current_window_size=200,
    psi_mild_threshold=0.1,
    psi_moderate_threshold=0.2,
    psi_severe_threshold=0.25,
    ks_significance=0.05,
    features_to_monitor=['feature_a', 'feature_b', 'feature_c']
)

# สร้าง pipeline
pipeline = DriftMonitoringPipeline(config)

# ใช้ 1000 samples แรกเป็น reference
reference_data = test_data.iloc[:1000]
pipeline.initialize(reference_data)

print("=" * 60)
print("🚀 Starting Drift Monitoring Pipeline")
print("=" * 60)

# Process data เป็น batches
batch_size = 200
remaining_data = test_data.iloc[1000:]

for i in range(0, len(remaining_data), batch_size):
    batch = remaining_data.iloc[i:i+batch_size]
    results = pipeline.process_batch(batch)
    
    if results and any(r.drift_detected for r in results):
        print(f"\n📍 Batch {i//batch_size + 1} results:")
        for r in results:
            if r.drift_detected:
                print(f"   ⚠️ {r.feature}: PSI={r.psi:.4f}, Type={r.drift_type.value}")

# %%
# Generate summary
print("\n" + "=" * 60)
print("📊 FINAL SUMMARY REPORT")
print("=" * 60)

summary = pipeline.get_summary_report()
print(f"\nTotal Checks: {summary['total_checks']}")
print(f"Total Drifts Detected: {summary['total_drifts_detected']}")
print(f"Active Alerts: {summary['active_alerts']}")

print("\nFeature Summary:")
for feature, data in summary['feature_summary'].items():
    print(f"\n  {feature}:")
    print(f"    Latest PSI: {data['latest_psi']:.4f}")
    print(f"    Drift Type: {data['latest_drift_type']}")
    print(f"    Drift Count: {data['drift_count']}/{data['total_checks']}")
    print(f"    Drift Rate: {data['drift_rate']:.1%}")

# %%
# Generate reports
report_generator = ReportGenerator(pipeline)

# Plot trends
report_generator.plot_drift_trends(save_path='monitoring_output/drift_trends.png')

# Generate HTML report
report_generator.generate_html_report('monitoring_output/reports/drift_report.html')

# Save all results
pipeline.save_results()

print("\n✅ All reports generated and saved to monitoring_output/")

# %% [markdown]
# ## ส่วนที่ 7: Integration กับ MLflow (Optional)

# %%
# Note: ส่วนนี้ต้อง install mlflow ก่อน: pip install mlflow

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("⚠️ MLflow not installed. Skipping MLflow integration.")
    print("   Install with: pip install mlflow")

if MLFLOW_AVAILABLE:
    class MLflowDriftTracker:
        """
        Integration กับ MLflow สำหรับ track drift experiments
        """
        
        def __init__(self, experiment_name: str = "drift_monitoring"):
            mlflow.set_experiment(experiment_name)
            self.active_run = None
        
        def start_run(self, run_name: str = None):
            """Start new MLflow run"""
            self.active_run = mlflow.start_run(run_name=run_name)
            return self.active_run
        
        def log_drift_result(self, result: DriftResult):
            """Log drift result to MLflow"""
            if self.active_run is None:
                return
            
            # Log metrics
            mlflow.log_metric(f"{result.feature}_psi", result.psi)
            mlflow.log_metric(f"{result.feature}_ks_stat", result.ks_statistic)
            mlflow.log_metric(f"{result.feature}_drift", 1 if result.drift_detected else 0)
            
            # Log params
            mlflow.log_param(f"{result.feature}_drift_type", result.drift_type.value)
        
        def log_summary(self, summary: Dict):
            """Log summary to MLflow"""
            if self.active_run is None:
                return
            
            mlflow.log_metric("total_drifts", summary.get('total_drifts_detected', 0))
            mlflow.log_metric("total_checks", summary.get('total_checks', 0))
            
            for feature, data in summary.get('feature_summary', {}).items():
                mlflow.log_metric(f"{feature}_drift_rate", data['drift_rate'])
        
        def log_artifact(self, artifact_path: str):
            """Log artifact to MLflow"""
            if self.active_run is None:
                return
            mlflow.log_artifact(artifact_path)
        
        def end_run(self):
            """End MLflow run"""
            if self.active_run:
                mlflow.end_run()
                self.active_run = None
    
    # Example usage
    print("\n" + "=" * 60)
    print("📊 Logging to MLflow")
    print("=" * 60)
    
    tracker = MLflowDriftTracker("drift_monitoring_lab")
    tracker.start_run(run_name="pipeline_run_1")
    
    # Log summary
    tracker.log_summary(summary)
    
    # Log artifacts
    tracker.log_artifact('monitoring_output/drift_trends.png')
    tracker.log_artifact('monitoring_output/reports/drift_report.html')
    
    tracker.end_run()
    print("✅ Results logged to MLflow")

# %% [markdown]
# ## สรุป LAB 6
#
# ### สิ่งที่เรียนรู้:
# 1. **Pipeline Architecture**: แยก components ชัดเจน
# 2. **Data Classes**: ใช้ dataclasses สำหรับ type safety
# 3. **Alert Management**: จัดการ alerts พร้อม cooldown
# 4. **Report Generation**: HTML reports และ visualizations
# 5. **MLflow Integration**: Track experiments

# %%
print("=" * 60)
print("✅ LAB 6 COMPLETED!")
print("=" * 60)
print("""
📚 Key Takeaways:
1. Modular architecture ทำให้ maintain ง่าย
2. Data buffering ช่วย handle streaming data
3. Alert management ป้องกัน alert fatigue
4. Automated reporting saves time
5. MLflow integration enables experiment tracking

🎉 CONGRATULATIONS! You have completed all 6 labs!

📋 What you've learned:
- LAB 1: Data Drift Concepts (Covariate/Concept Shift)
- LAB 2: Feature Drift Detection (per-feature analysis)
- LAB 3: Multivariate Drift Analysis (correlation/PCA)
- LAB 4: Production Simulation (streaming detection)
- LAB 5: Custom Metrics & Thresholds (optimization)
- LAB 6: End-to-End Pipeline (production-ready)

🚀 Next steps:
- Deploy pipeline to production
- Add more sophisticated alerting (email, Slack)
- Integrate with model retraining triggers
- Add A/B testing capabilities
""")

# %%
# Final cleanup and summary
print("\n📁 Output files created:")
for root, dirs, files in os.walk('monitoring_output'):
    for file in files:
        filepath = os.path.join(root, file)
        print(f"   {filepath}")
```

---

## สรุปรวม

ทั้ง 6 Labs ครอบคลุมเนื้อหาดังนี้:

| Lab | หัวข้อ | สิ่งที่เรียนรู้ |
|-----|--------|----------------|
| 1 | Understanding Data Drift | Covariate/Concept Shift, KS/PSI/Wasserstein |
| 2 | Feature Drift Detection | Per-feature analysis, Numerical vs Categorical |
| 3 | Multivariate Drift | Correlation, PCA, Mahalanobis Distance |
| 4 | Production Simulation | Streaming, Sliding Window, Page-Hinkley |
| 5 | Custom Metrics & Thresholds | Optimization, Cost-based, Ensemble |
| 6 | End-to-End Pipeline | Architecture, Alerting, Reporting, MLflow |
