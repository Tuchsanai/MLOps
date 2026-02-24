# 📚 Data Drift Detection: Complete Guide for MLOps

## สารบัญ
1. [บทนำ: ทำความเข้าใจ Data Drift](#บทนำ-ทำความเข้าใจ-data-drift)
2. [LAB 1: Understanding Data Drift Concepts](#lab-1-understanding-data-drift-concepts)
3. [LAB 2: Feature Drift Detection](#lab-2-feature-drift-detection)
4. [LAB 3: Multivariate Drift Analysis](#lab-3-multivariate-drift-analysis)
5. [LAB 4: Drift Detection in Production Simulation](#lab-4-drift-detection-in-production-simulation)
6. [LAB 5: Custom Metrics & Drift Thresholds](#lab-5-custom-metrics--drift-thresholds)
7. [LAB 6: End-to-End Monitoring Pipeline](#lab-6-end-to-end-monitoring-pipeline)
8. [สรุปและ Best Practices](#สรุปและ-best-practices)

---

## บทนำ: ทำความเข้าใจ Data Drift

### Data Drift คืออะไร?

**Data Drift** (หรือ Dataset Shift) คือปรากฏการณ์ที่ข้อมูลในระบบ production มีการเปลี่ยนแปลงไปจากข้อมูลที่ใช้ train โมเดล ซึ่งเป็นหนึ่งในสาเหตุหลักที่ทำให้ ML Model มีประสิทธิภาพลดลงเมื่อเวลาผ่านไป

```
Training Time                    Production Time
     │                                │
     ▼                                ▼
┌─────────────┐               ┌─────────────┐
│ Training    │               │ Production  │
│ Data        │──── Drift ───▶│ Data        │
│ P(X,Y)_train│               │ P(X,Y)_prod │
└─────────────┘               └─────────────┘
     │                                │
     ▼                                ▼
┌─────────────┐               ┌─────────────┐
│ Good Model  │               │ Degraded    │
│ Performance │               │ Performance │
└─────────────┘               └─────────────┘
```

### ทำไม Drift Detection ถึงสำคัญ?

1. **Model Degradation**: โมเดลที่ train ด้วยข้อมูลเก่าอาจทำนายผิดพลาดกับข้อมูลใหม่
2. **Business Impact**: การตัดสินใจผิดพลาดส่งผลต่อธุรกิจโดยตรง
3. **Regulatory Compliance**: หลายอุตสาหกรรมต้องการ monitoring อย่างต่อเนื่อง
4. **Resource Optimization**: รู้เวลาที่ต้อง retrain ช่วยประหยัดทรัพยากร

---

## LAB 1: Understanding Data Drift Concepts

### 🎯 วัตถุประสงค์
- เข้าใจความแตกต่างระหว่าง Covariate Shift และ Concept Drift
- เรียนรู้ Statistical tests สำหรับ drift detection
- สามารถเลือก drift detection method ที่เหมาะสม

### ทฤษฎี: ประเภทของ Data Drift

#### 1. Covariate Shift (Feature Drift)

**นิยาม**: การเปลี่ยนแปลงของ distribution ของ input features P(X) โดยที่ความสัมพันธ์ P(Y|X) ยังคงเดิม

```
Covariate Shift:
├── P(X)_train ≠ P(X)_prod     ← Distribution เปลี่ยน
└── P(Y|X)_train = P(Y|X)_prod  ← Relationship คงเดิม
```

**ตัวอย่างในชีวิตจริง**:
- โมเดลทำนายราคาบ้านที่ train กับบ้านในเมือง แต่ต้องทำนายบ้านในชนบท
- โมเดลอายุลูกค้าที่ train กับกลุ่มอายุ 20-40 ปี แต่ production มีลูกค้าอายุ 40-60 ปี

**Code Reference** - การสร้างข้อมูล Covariate Shift:
```python
def generate_covariate_shift_data():
    # Training data: ลูกค้าอายุน้อย (20-40)
    age_train = np.random.normal(30, 5, n_train)
    
    # Production data: ลูกค้าอายุมากขึ้น (40-60) - Covariate Shift!
    age_prod = np.random.normal(50, 5, n_prod)
    
    # กฎการซื้อเหมือนเดิม (ไม่มี Concept Drift)
    # P(Y|X) ยังคงเดิม
```

#### 2. Concept Drift (Label Drift)

**นิยาม**: การเปลี่ยนแปลงของความสัมพันธ์ระหว่าง input และ output P(Y|X)

```
Concept Drift:
├── P(X) อาจคงที่หรือเปลี่ยนก็ได้
└── P(Y|X)_train ≠ P(Y|X)_prod  ← Relationship เปลี่ยน!
```

**ตัวอย่างในชีวิตจริง**:
- พฤติกรรมการซื้อของลูกค้าเปลี่ยนหลัง COVID-19
- ความหมายของ "spam email" เปลี่ยนไปตามเวลา

**Code Reference** - การสร้างข้อมูล Concept Drift:
```python
def generate_concept_drift_data():
    # Training: กฎการซื้อเดิม - ซื้อถ้า income > 45000
    purchase_train = (income_train > 45000).astype(int)
    
    # Production: กฎการซื้อเปลี่ยน - ซื้อถ้า income > 55000
    # Threshold เปลี่ยน = Concept Drift!
    purchase_prod = (income_prod > 55000).astype(int)
```

#### เปรียบเทียบ Covariate Shift vs Concept Drift

| ลักษณะ | Covariate Shift | Concept Drift |
|--------|-----------------|---------------|
| สิ่งที่เปลี่ยน | P(X) | P(Y\|X) |
| ตัวอย่าง | กลุ่มลูกค้าเปลี่ยน | พฤติกรรมเปลี่ยน |
| การตรวจจับ | เปรียบเทียบ feature distributions | ต้องมี labels หรือ performance |
| วิธีแก้ | Sample weighting, Retrain | Retrain with new data |

---

### Statistical Tests สำหรับ Drift Detection

#### 1. Kolmogorov-Smirnov (KS) Test

**ทฤษฎี**:
- เปรียบเทียบ Cumulative Distribution Function (CDF) ของ 2 samples
- วัดความแตกต่างสูงสุดระหว่าง 2 CDFs

```
KS Statistic = max|F₁(x) - F₂(x)|

โดยที่:
- F₁(x) = CDF ของ reference data
- F₂(x) = CDF ของ current data
```

**การตีความ**:
- KS Statistic: 0-1 (ยิ่งสูง = ยิ่งแตกต่าง)
- p-value < 0.05: reject null hypothesis → มี drift

**ข้อดี**:
- ไม่ต้องสมมติ distribution (non-parametric)
- Sensitive ต่อการเปลี่ยนแปลง

**ข้อเสีย**:
- ใช้ได้กับ continuous variables เท่านั้น

**Code Reference**:
```python
def kolmogorov_smirnov_test(data1, data2, feature_name="feature"):
    statistic, p_value = stats.ks_2samp(data1, data2)
    drift_detected = p_value < 0.05
    
    return {
        'statistic': statistic,
        'p_value': p_value,
        'drift_detected': drift_detected
    }
```

#### 2. Population Stability Index (PSI)

**ทฤษฎี**:
- วัดการเปลี่ยนแปลงของ distribution โดยเปรียบเทียบ proportions ในแต่ละ bin
- นิยมใช้ใน credit scoring และ financial models

**สูตร**:
```
PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)

โดยที่:
- Expected% = proportion ใน reference data
- Actual% = proportion ใน current data
```

**การตีความ PSI**:

| ค่า PSI | ความหมาย | Action |
|---------|----------|--------|
| < 0.1 | ไม่มีการเปลี่ยนแปลงสำคัญ | ปกติ |
| 0.1 - 0.25 | การเปลี่ยนแปลงปานกลาง | ตรวจสอบเพิ่ม |
| ≥ 0.25 | การเปลี่ยนแปลงมาก | ต้องดำเนินการ |

**Code Reference**:
```python
def calculate_psi(expected, actual, bins=10, eps=1e-6):
    # สร้าง bins จาก expected data
    breakpoints = np.percentile(expected, np.linspace(0, 100, bins + 1))
    
    # นับจำนวนในแต่ละ bin
    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)
    
    # คำนวณ proportions
    expected_props = expected_counts / len(expected) + eps
    actual_props = actual_counts / len(actual) + eps
    
    # คำนวณ PSI
    psi = np.sum((actual_props - expected_props) * np.log(actual_props / expected_props))
    return psi
```

#### 3. Wasserstein Distance (Earth Mover's Distance)

**ทฤษฎี**:
- วัด "งาน" ที่ต้องใช้ในการเปลี่ยน distribution หนึ่งไปเป็นอีก distribution
- คล้ายกับการคำนวณต้นทุนในการขนย้ายดิน

```
Wasserstein Distance = inf ∫|F₁⁻¹(u) - F₂⁻¹(u)| du

เปรียบเสมือน:
┌─────────────┐         ┌─────────────┐
│   Pile A    │  move   │   Pile B    │
│   (sand)    │ ──────▶ │   (sand)    │
└─────────────┘  cost   └─────────────┘
```

**ข้อดี**:
- คำนึงถึง distance ระหว่าง bins
- Sensitive ต่อ shift ในตำแหน่ง

**Code Reference**:
```python
def wasserstein_distance_test(data1, data2, feature_name="feature"):
    distance = stats.wasserstein_distance(data1, data2)
    
    # Normalize โดยใช้ standard deviation
    std_ref = np.std(data1)
    normalized_distance = distance / std_ref if std_ref > 0 else distance
    
    return {
        'distance': distance,
        'normalized_distance': normalized_distance
    }
```

### การเลือก Drift Detection Method

```
Decision Tree:

1. Data Type?
   ├── Continuous → ไปข้อ 2
   └── Categorical → Chi-squared หรือ PSI

2. ต้องการ Statistical Significance?
   ├── ใช่ → KS Test
   └── ไม่จำเป็น → PSI หรือ Wasserstein

3. Industry Requirement?
   ├── Finance/Credit → PSI (regulatory standards)
   └── อื่นๆ → เลือกตามความเหมาะสม

4. ต้องการ Sensitivity สูง?
   ├── ใช่ → Wasserstein
   └── ปกติ → KS หรือ PSI
```

---

## LAB 2: Feature Drift Detection

### 🎯 วัตถุประสงค์
- ตรวจจับ drift ในแต่ละ feature อย่างเป็นระบบ
- วิเคราะห์ numerical vs categorical feature drift
- สร้าง visualization สำหรับ feature distributions

### ทฤษฎี: Per-Feature Analysis

การวิเคราะห์ drift ในแต่ละ feature มีความสำคัญเพราะ:
1. ช่วยระบุ root cause ของ model performance degradation
2. ทำให้เข้าใจว่า feature ไหนเปลี่ยนแปลงมากที่สุด
3. สามารถ prioritize การแก้ไขได้

### Numerical Features vs Categorical Features

#### Numerical Features
```
Methods ที่ใช้:
├── KS Test - compare CDFs
├── PSI - compare bin proportions
└── Wasserstein - measure distribution distance
```

#### Categorical Features
```
Methods ที่ใช้:
├── Chi-squared Test - compare frequency distributions
└── PSI (category-based) - compare category proportions
```

### Feature Drift Detector Class

**Architecture**:
```
FeatureDriftDetector
├── __init__()
│   ├── reference_data
│   ├── current_data
│   ├── numerical_features
│   └── categorical_features
│
├── Numerical Methods
│   ├── ks_test()
│   ├── calculate_psi()
│   └── wasserstein_test()
│
├── Categorical Methods
│   ├── chi_squared_test()
│   └── categorical_psi()
│
└── Analysis
    ├── analyze_numerical_feature()
    ├── analyze_categorical_feature()
    ├── analyze_all_features()
    └── get_summary_report()
```

**Code Reference**:
```python
class FeatureDriftDetector:
    def __init__(self, reference_data, current_data, 
                 numerical_features=None, categorical_features=None):
        self.reference = reference_data
        self.current = current_data
        self.numerical_features = numerical_features
        self.categorical_features = categorical_features
    
    def analyze_numerical_feature(self, feature):
        results = {
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
        return results
```

### Feature Drift Ranking

จัดลำดับ features ตามความรุนแรงของ drift เพื่อ prioritization:

```
Ranking Algorithm:
1. คำนวณ PSI สำหรับทุก features
2. เรียงลำดับจากมากไปน้อย
3. กำหนด severity level (none/mild/severe)
4. Focus แก้ไข features ที่มี severe drift ก่อน
```

### Time-based Distribution Analysis

การติดตาม drift เมื่อเวลาผ่านไป:

```
Period 0 (Reference)
    │
    ▼
Period 1 ──── PSI = 0.02 (none)
    │
    ▼
Period 2 ──── PSI = 0.08 (none)
    │
    ▼
Period 3 ──── PSI = 0.15 (mild) ⚠️
    │
    ▼
Period 4 ──── PSI = 0.28 (severe) 🔴
```

---

## LAB 3: Multivariate Drift Analysis

### 🎯 วัตถุประสงค์
- ตรวจจับ drift ที่เกิดจากความสัมพันธ์ระหว่าง features
- ใช้ Dataset-level drift detection
- วิเคราะห์ Correlation changes

### ทฤษฎี: Multivariate Drift

**ปัญหา**: Univariate methods อาจพลาด drift ที่เกิดจากการเปลี่ยนแปลงของความสัมพันธ์ระหว่าง features

```
ตัวอย่าง:
Reference:                    Current:
- Age mean = 35              - Age mean = 35      (เหมือนเดิม)
- Income mean = 50000        - Income mean = 50000 (เหมือนเดิม)
- Corr(Age, Income) = 0.8    - Corr(Age, Income) = 0.1 ← เปลี่ยน!

Univariate test: ไม่พบ drift
Multivariate test: พบ drift ในความสัมพันธ์
```

### Methods สำหรับ Multivariate Drift

#### 1. Correlation-based Analysis

**ทฤษฎี**: เปรียบเทียบ correlation matrix ระหว่าง reference และ current data

**Fisher's Z Transformation** สำหรับเปรียบเทียบ correlations:
```
Z = arctanh(r)

Z-test statistic = (Z_ref - Z_cur) / SE
where SE = sqrt(1/(n₁-3) + 1/(n₂-3))
```

**Code Reference**:
```python
def correlation_drift_test(ref_df, cur_df, significance_level=0.05):
    ref_corr = ref_df.corr()
    cur_corr = cur_df.corr()
    
    for col1, col2 in feature_pairs:
        r_ref = ref_corr.loc[col1, col2]
        r_cur = cur_corr.loc[col1, col2]
        
        # Fisher's Z transformation
        z_ref = np.arctanh(r_ref)
        z_cur = np.arctanh(r_cur)
        
        # Z-test
        se = np.sqrt(1/(n_ref-3) + 1/(n_cur-3))
        z_stat = (z_ref - z_cur) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
```

#### 2. PCA-based Analysis

**ทฤษฎี**: ใช้ Principal Component Analysis เพื่อตรวจจับการเปลี่ยนแปลงของ multivariate structure

```
PCA Drift Detection:
├── Explained Variance Ratio - variance ที่แต่ละ PC อธิบายได้
├── Component Similarity - ทิศทางของ PC เหมือนเดิมหรือไม่
└── Reconstruction Error - error เมื่อ reconstruct data
```

**Metrics ที่ใช้**:
1. **Explained Variance Comparison**: เปรียบเทียบว่าแต่ละ PC อธิบาย variance เท่าเดิมหรือไม่
2. **Component Similarity (Cosine Similarity)**: ดูว่า PC directions เหมือนเดิมหรือไม่
3. **Reconstruction Error**: ใช้ reference PCA กับ current data แล้วดู error

**Code Reference**:
```python
def pca_drift_detection(ref_df, cur_df, n_components=None):
    # Standardize
    scaler = StandardScaler()
    ref_scaled = scaler.fit_transform(ref_df)
    cur_scaled = scaler.transform(cur_df)
    
    # Fit PCA on reference
    pca_ref = PCA(n_components=n_components)
    pca_ref.fit(ref_scaled)
    
    # Component similarities (using cosine similarity)
    for i in range(n_components):
        cos_sim = abs(np.dot(pca_ref.components_[i], pca_cur.components_[i]))
        # ถ้า cos_sim < 0.9 = structure เปลี่ยน
```

#### 3. Mahalanobis Distance

**ทฤษฎี**: วัดว่าข้อมูลใหม่อยู่ห่างจาก distribution ของ reference data เท่าไร โดยคำนึงถึง covariance

```
Mahalanobis Distance = √((x - μ)ᵀ Σ⁻¹ (x - μ))

โดยที่:
- x = data point
- μ = mean ของ reference
- Σ = covariance matrix ของ reference
```

**การใช้งาน**:
1. Fit covariance บน reference data
2. คำนวณ Mahalanobis distance สำหรับทุก points
3. เปรียบเทียบ distribution ของ distances

**Code Reference**:
```python
def mahalanobis_drift_detection(ref_df, cur_df, threshold_percentile=95):
    # Fit covariance on reference
    cov = EmpiricalCovariance().fit(ref_scaled)
    
    # Calculate distances
    ref_distances = cov.mahalanobis(ref_scaled)
    cur_distances = cov.mahalanobis(cur_scaled)
    
    # Compare distributions
    ks_stat, ks_pval = stats.ks_2samp(ref_distances, cur_distances)
    drift_detected = ks_pval < 0.05
```

### Comprehensive Multivariate Analysis

```
MultivariateriftDetector
├── Correlation Analysis
│   └── ตรวจจับ pairwise correlation changes
├── PCA Analysis
│   └── ตรวจจับ structure changes
├── Mahalanobis Analysis
│   └── ตรวจจับ distribution shift
└── Consensus
    └── รวมผลจากทุก methods
```

---

## LAB 4: Drift Detection in Production Simulation

### 🎯 วัตถุประสงค์
- สร้าง simulated data stream ที่มี drift
- ตรวจจับ sudden vs gradual drift
- Implement sliding window monitoring

### ทฤษฎี: Drift Patterns ใน Production

#### Types of Drift

```
1. Sudden Drift (Abrupt)
   ────────────┬────────────
               │
               ▼ Drift Point
   เปลี่ยนทันที

2. Gradual Drift
   ────────────╱────────────
   เปลี่ยนช้าๆ ตามเวลา

3. Incremental Drift
   ────┬───┬───┬───┬────────
       │   │   │   │
   เปลี่ยนเป็นขั้นบันได

4. Seasonal/Recurring Drift
   ────╲╱────╲╱────╲╱────
   เปลี่ยนตาม pattern ซ้ำ
```

**Code Reference** - Data Stream Simulator:
```python
class DataStreamSimulator:
    def generate_stream(self, n_samples, drift_type='no_drift', drift_params=None):
        if drift_type == 'sudden':
            # เปลี่ยนทันทีที่ drift_point
            data[:drift_point] = np.random.normal(base_mean, ...)
            data[drift_point:] = np.random.normal(new_mean, ...)
            
        elif drift_type == 'gradual':
            # Linear interpolation
            for i in range(n_samples):
                if drift_start <= i <= drift_end:
                    progress = (i - drift_start) / (drift_end - drift_start)
                    current_mean = base_mean + progress * (final_mean - base_mean)
```

### Sliding Window Drift Detection

**หลักการ**:
```
Time ────────────────────────────────────────────▶

Reference Window          Test Window
[═══════════════════]     [═════════]
        ▲                      ▲
        │                      │
   Fixed/Slow moving    Current data
```

**Architecture**:
```
SlidingWindowDriftDetector
├── reference_buffer (deque with maxlen)
├── test_buffer (deque with maxlen)
├── update(value)
│   ├── Add to buffer
│   ├── Check if ready
│   └── Run drift detection
├── Detection Methods
│   ├── KS Test
│   └── PSI
└── Output
    ├── drift_detected
    ├── metrics
    └── history
```

**Code Reference**:
```python
class SlidingWindowDriftDetector:
    def __init__(self, reference_window_size=200, test_window_size=100):
        self.reference_buffer = deque(maxlen=reference_window_size)
        self.test_buffer = deque(maxlen=test_window_size)
    
    def update(self, value, timestamp=None):
        # เพิ่มค่าใน buffers
        if not self.is_initialized:
            self.reference_buffer.append(value)
            return {'status': 'initializing'}
        
        self.test_buffer.append(value)
        
        if len(self.test_buffer) < self.test_window_size:
            return {'status': 'collecting'}
        
        # ทำ drift detection
        ref_array = np.array(self.reference_buffer)
        test_array = np.array(self.test_buffer)
        
        psi = self.calculate_psi(ref_array, test_array)
        drift_detected = psi > self.psi_threshold
        
        return {
            'drift_detected': drift_detected,
            'psi': psi
        }
```

### Adaptive Reference Window

**ปัญหาของ Fixed Reference**:
- Gradual drift อาจตรวจไม่เจอ เพราะ reference เก่าเกินไป
- ต้อง adapt reference เมื่อ detect drift

**วิธีแก้**:
```python
class AdaptiveDriftDetector:
    def adapt_reference(self):
        """ปรับ reference window เมื่อ confirm drift"""
        # ผสม old reference กับ new data
        old_weight = 0.5
        
        # เพิ่มบางส่วนจาก old reference
        for val in old_ref[-n_old:]:
            self.reference_buffer.append(val)
        
        # เพิ่ม new data
        for val in new_data:
            self.reference_buffer.append(val)
```

### Page-Hinkley Test

**ทฤษฎี**: Algorithm สำหรับ detect mean shift ใน streaming data

```
Algorithm:
1. Update running mean: μ_t = α·μ_{t-1} + (1-α)·x_t
2. Update cumulative sum: S_t = S_{t-1} + (x_t - μ_t - δ)
3. Track min/max of S_t
4. Detect if S_t - min(S) > λ (upward shift)
         หรือ max(S) - S_t > λ (downward shift)
```

**Code Reference**:
```python
class PageHinkleyDetector:
    def update(self, value):
        # Update mean (exponential moving average)
        self.mean = self.alpha * self.mean + (1 - self.alpha) * value
        
        # Update cumulative sum
        self.sum += value - self.mean - self.delta
        
        # Update min/max
        self.min_sum = min(self.min_sum, self.sum)
        self.max_sum = max(self.max_sum, self.sum)
        
        # Detection
        ph_positive = self.sum - self.min_sum  # Upward shift
        ph_negative = self.max_sum - self.sum  # Downward shift
        
        drift_detected = (ph_positive > self.lambda_) or (ph_negative > self.lambda_)
```

### Comparison of Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| Sliding Window | Simple, intuitive | Fixed reference | Sudden drift |
| Adaptive | Handles gradual drift | More complex | Production |
| Page-Hinkley | Low memory, fast | Mean shift only | Real-time |

---

## LAB 5: Custom Metrics & Drift Thresholds

### 🎯 วัตถุประสงค์
- สร้าง custom drift metrics
- ปรับ threshold ตาม business requirements
- Handle false positives/negatives

### ทฤษฎี: Threshold Selection

**ปัญหา**: Default thresholds อาจไม่เหมาะกับทุก use case

```
Trade-off:
                    Threshold
           Low ◄─────────────────▶ High
           
Sensitivity: High                    Low
False Positive: High                 Low
False Negative: Low                  High
```

### Custom Drift Metrics

#### 1. Combined Score
```python
def combined_score(reference, current, weights=None):
    """รวมหลาย metrics เข้าด้วยกัน"""
    if weights is None:
        weights = {
            'psi': 0.3,
            'wasserstein': 0.3,
            'mean_shift': 0.2,
            'percentile': 0.2
        }
    
    # Normalize แต่ละ metric ให้อยู่ในช่วง 0-1
    psi = min(calculate_psi(reference, current), 1.0)
    wasserstein = min(normalized_wasserstein(reference, current) / 3, 1.0)
    mean_shift = min(mean_shift_ratio(reference, current) / 3, 1.0)
    percentile = min(percentile_shift(reference, current) / 3, 1.0)
    
    score = (weights['psi'] * psi + 
             weights['wasserstein'] * wasserstein +
             weights['mean_shift'] * mean_shift +
             weights['percentile'] * percentile)
    
    return score
```

#### 2. Jensen-Shannon Divergence
```python
def jensen_shannon_divergence(reference, current, bins=10):
    """Symmetric version of KL Divergence"""
    # สร้าง normalized histograms
    ref_hist = np.histogram(reference, bins=bins, density=True)[0]
    cur_hist = np.histogram(current, bins=bins, density=True)[0]
    
    # Average distribution
    m = 0.5 * (ref_hist + cur_hist)
    
    # JS Divergence = 0.5 * (KL(P||M) + KL(Q||M))
    js = 0.5 * (kl_divergence(ref_hist, m) + kl_divergence(cur_hist, m))
    return js
```

### Threshold Optimization

#### F1-based Optimization

```python
def find_optimal_threshold(scenarios, metric_func, thresholds, optimize_for='f1'):
    """หา threshold ที่ให้ F1 score สูงสุด"""
    results = []
    
    for t in thresholds:
        y_true = [s['has_drift'] for s in scenarios]
        y_pred = [metric_func(s['reference'], s['current']) > t for s in scenarios]
        
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        results.append({'threshold': t, 'f1': f1})
    
    # หา optimal
    optimal = max(results, key=lambda x: x['f1'])
    return optimal
```

#### Cost-based Optimization

**ทฤษฎี**: ปรับ threshold ตาม cost ของ false positive vs false negative

```
Total Cost = FP_count × FP_cost + FN_count × FN_cost

Scenarios:
├── High FN cost (เช่น fraud detection)
│   └── ใช้ Low threshold → detect more, accept false alarms
├── High FP cost (เช่น expensive retraining)
│   └── ใช้ High threshold → conservative detection
└── Balanced cost
    └── Optimize for F1
```

**Code Reference**:
```python
class BusinessDriftThreshold:
    def __init__(self, false_positive_cost=1, false_negative_cost=10):
        self.fp_cost = false_positive_cost
        self.fn_cost = false_negative_cost
    
    def calculate_total_cost(self, y_true, y_pred):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return fp * self.fp_cost + fn * self.fn_cost
    
    def find_cost_optimal_threshold(self, scenarios, metric_func, thresholds):
        costs = []
        for t in thresholds:
            y_pred = [metric_func(s['reference'], s['current']) > t 
                     for s in scenarios]
            cost = self.calculate_total_cost(y_true, y_pred)
            costs.append({'threshold': t, 'cost': cost})
        
        optimal = min(costs, key=lambda x: x['cost'])
        return optimal
```

### Handling False Positives/Negatives

#### Ensemble Approach
```python
class RobustDriftDetector:
    """ใช้หลาย methods ร่วมกัน"""
    
    def detect(self, reference, current):
        all_metrics = self._calculate_all_metrics(reference, current)
        
        # Majority voting
        drift_votes = sum(
            1 for m, v in all_metrics.items() 
            if v > self.thresholds[m]
        )
        
        # ต้อง 3/4 methods agree
        ensemble_drift = drift_votes >= 3
        
        return ensemble_drift
```

#### Confirmation Mechanism
```python
def detect_with_confirmation(self, reference, current):
    """ต้อง detect หลายครั้งติดกันถึงยืนยัน"""
    
    potential_drift = self.primary_metric(reference, current) > threshold
    
    if potential_drift:
        self.consecutive_count += 1
    else:
        self.consecutive_count = 0
    
    # Confirmed ถ้า detect 3 ครั้งติดกัน
    confirmed = self.consecutive_count >= 3
    return confirmed
```

### Best Practices สำหรับ Threshold Setting

```
1️⃣ DOMAIN-SPECIFIC THRESHOLDS
   - ไม่ใช้ default โดยไม่ validate
   - ทดสอบกับ labeled data
   - ปรึกษา domain experts

2️⃣ COST-BASED OPTIMIZATION
   - พิจารณา cost ของ FP vs FN
   - FN แพง → Lower threshold
   - FP แพง → Higher threshold

3️⃣ ENSEMBLE APPROACH
   - ใช้หลาย metrics ร่วมกัน
   - Voting mechanism ลด false positives

4️⃣ CONFIRMATION MECHANISM
   - Require consecutive detections
   - ป้องกัน temporary spikes

5️⃣ PERIODIC REVIEW
   - Review thresholds เป็นระยะ
   - Business requirements อาจเปลี่ยน
```

---

## LAB 6: End-to-End Monitoring Pipeline

### 🎯 วัตถุประสงค์
- รวมทุก components เข้าด้วยกัน
- สร้าง automated monitoring workflow
- Integrate กับ MLflow

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 Drift Monitoring Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐    ┌────────────────┐                   │
│  │  Data Source   │───▶│  Data Buffer   │                   │
│  └────────────────┘    └───────┬────────┘                   │
│                                │                             │
│                    ┌───────────▼───────────┐                │
│                    │   Drift Calculator    │                │
│                    └───────────┬───────────┘                │
│                                │                             │
│           ┌────────────────────┼────────────────────┐       │
│           │                    │                    │       │
│           ▼                    ▼                    ▼       │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │   Alert     │      │   Report    │      │   MLflow    │ │
│  │   Manager   │      │   Generator │      │   Tracker   │ │
│  └─────────────┘      └─────────────┘      └─────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Data Classes

```python
from dataclasses import dataclass
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
    timestamp: datetime
    feature: str
    drift_detected: bool
    drift_type: DriftType
    psi: float
    ks_statistic: float
    ks_pvalue: float
    reference_mean: float
    current_mean: float

@dataclass
class Alert:
    timestamp: datetime
    severity: AlertSeverity
    message: str
    details: Dict
    acknowledged: bool = False
```

#### 2. Configuration

```python
@dataclass
class MonitoringConfig:
    reference_window_size: int = 1000
    current_window_size: int = 200
    psi_mild_threshold: float = 0.1
    psi_moderate_threshold: float = 0.2
    psi_severe_threshold: float = 0.25
    ks_significance: float = 0.05
    check_interval_seconds: int = 60
    alert_cooldown_minutes: int = 30
    features_to_monitor: List[str] = field(default_factory=list)
```

#### 3. Data Buffer

```python
class DataBuffer:
    """Buffer สำหรับเก็บ reference และ current data"""
    
    def __init__(self, config: MonitoringConfig):
        self.reference_data: Dict[str, deque] = {}
        self.current_data: Dict[str, deque] = {}
    
    def initialize(self, reference_df: pd.DataFrame):
        """Initialize with reference data"""
        for feature in self.config.features_to_monitor:
            self.reference_data[feature] = deque(
                reference_df[feature].values,
                maxlen=self.config.reference_window_size
            )
    
    def add_data(self, data: Dict[str, float]):
        """Add new data point"""
        for feature, value in data.items():
            self.current_data[feature].append(value)
```

#### 4. Alert Manager

```python
class AlertManager:
    """จัดการ alerts พร้อม cooldown"""
    
    def __init__(self, config: MonitoringConfig):
        self.alerts: List[Alert] = []
        self.last_alert_time: Dict[str, datetime] = {}
    
    def should_alert(self, feature: str) -> bool:
        """Check cooldown"""
        if feature not in self.last_alert_time:
            return True
        elapsed = datetime.now() - self.last_alert_time[feature]
        return elapsed > timedelta(minutes=self.config.alert_cooldown_minutes)
    
    def create_alert(self, drift_result: DriftResult) -> Optional[Alert]:
        if not drift_result.drift_detected:
            return None
        
        if not self.should_alert(drift_result.feature):
            return None
        
        # Determine severity
        severity = self._determine_severity(drift_result.drift_type)
        
        alert = Alert(
            timestamp=drift_result.timestamp,
            severity=severity,
            message=f"Drift detected in {drift_result.feature}",
            details=drift_result.to_dict()
        )
        
        self.alerts.append(alert)
        self.last_alert_time[drift_result.feature] = datetime.now()
        
        return alert
```

#### 5. Main Pipeline

```python
class DriftMonitoringPipeline:
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.data_buffer = DataBuffer(config)
        self.alert_manager = AlertManager(config)
        self.drift_calculator = DriftCalculator()
        self.results_history: List[DriftResult] = []
    
    def initialize(self, reference_data: pd.DataFrame):
        self.data_buffer.initialize(reference_data)
    
    def process_batch(self, batch_data: pd.DataFrame) -> List[DriftResult]:
        results = []
        
        # Add data to buffer
        for idx, row in batch_data.iterrows():
            self.data_buffer.add_data(row.to_dict())
        
        # Check if ready
        if not self.data_buffer.is_current_ready():
            return results
        
        # Detect drift for each feature
        for feature in self.config.features_to_monitor:
            result = self._detect_drift_for_feature(feature)
            if result:
                results.append(result)
                
                # Create alert if needed
                if result.drift_detected:
                    self.alert_manager.create_alert(result)
        
        return results
```

### Report Generation

```python
class ReportGenerator:
    def generate_html_report(self, output_path: str):
        """Generate HTML report"""
        summary = self.pipeline.get_summary_report()
        
        html_content = f"""
        <html>
        <head><title>Drift Monitoring Report</title></head>
        <body>
            <h1>Drift Monitoring Report</h1>
            <p>Generated: {datetime.now()}</p>
            
            <h2>Summary</h2>
            <p>Total Checks: {summary['total_checks']}</p>
            <p>Drifts Detected: {summary['total_drifts_detected']}</p>
            
            <h2>Feature Summary</h2>
            <table>
                <tr><th>Feature</th><th>PSI</th><th>Status</th></tr>
                {self._generate_feature_rows(summary)}
            </table>
            
            <h2>Active Alerts</h2>
            {self._generate_alerts_section()}
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
```

### MLflow Integration

```python
class MLflowDriftTracker:
    def __init__(self, experiment_name: str = "drift_monitoring"):
        mlflow.set_experiment(experiment_name)
    
    def log_drift_result(self, result: DriftResult):
        mlflow.log_metric(f"{result.feature}_psi", result.psi)
        mlflow.log_metric(f"{result.feature}_drift", 1 if result.drift_detected else 0)
        mlflow.log_param(f"{result.feature}_drift_type", result.drift_type.value)
    
    def log_summary(self, summary: Dict):
        mlflow.log_metric("total_drifts", summary.get('total_drifts_detected', 0))
        for feature, data in summary.get('feature_summary', {}).items():
            mlflow.log_metric(f"{feature}_drift_rate", data['drift_rate'])
    
    def log_artifact(self, artifact_path: str):
        mlflow.log_artifact(artifact_path)
```

---

## สรุปและ Best Practices

### Summary Table

| Lab | หัวข้อ | Key Concepts |
|-----|--------|--------------|
| 1 | Understanding Data Drift | Covariate/Concept Shift, KS/PSI/Wasserstein |
| 2 | Feature Drift Detection | Per-feature analysis, Numerical vs Categorical |
| 3 | Multivariate Drift | Correlation, PCA, Mahalanobis Distance |
| 4 | Production Simulation | Streaming, Sliding Window, Page-Hinkley |
| 5 | Custom Metrics & Thresholds | Optimization, Cost-based, Ensemble |
| 6 | End-to-End Pipeline | Architecture, Alerting, Reporting, MLflow |

### Decision Framework

```
เมื่อพบ Drift ควรทำอย่างไร?

1. Assess Severity
   ├── MILD → Monitor closely
   ├── MODERATE → Investigate root cause
   └── SEVERE → Immediate action required

2. Investigate Root Cause
   ├── Data collection issue?
   ├── Upstream data change?
   ├── Real-world change?
   └── Seasonal pattern?

3. Decide Action
   ├── Retrain model
   ├── Update feature engineering
   ├── Adjust thresholds
   └── Business process change
```

### Production Checklist

```
□ Define monitoring strategy
  □ Which features to monitor?
  □ What thresholds to use?
  □ How often to check?

□ Implement detection
  □ Choose appropriate methods
  □ Handle both numerical and categorical
  □ Consider multivariate drift

□ Set up alerting
  □ Define severity levels
  □ Configure notification channels
  □ Set cooldown periods

□ Create reporting
  □ Automated dashboards
  □ Periodic reports
  □ Historical analysis

□ Plan remediation
  □ When to retrain?
  □ How to validate new model?
  □ Rollback procedures
```

### Final Thoughts

การทำ Drift Detection ที่ดีต้อง:

1. **เข้าใจ Business Context**: Drift ที่สำคัญใน domain หนึ่งอาจไม่สำคัญใน domain อื่น

2. **ใช้หลาย Methods**: ไม่มี method ใดที่สมบูรณ์แบบ ควรใช้หลาย methods ร่วมกัน

3. **Tune Thresholds**: Default thresholds มักไม่เหมาะ ต้องปรับตาม use case

4. **Automate**: การทำ manual monitoring ไม่ยั่งยืน ต้องมี automated pipeline

5. **Monitor the Monitor**: ตรวจสอบว่า monitoring system ทำงานถูกต้อง

---

## แหล่งเรียนรู้เพิ่มเติม

- [Evidently AI Documentation](https://docs.evidentlyai.com/)
- [NannyML Documentation](https://docs.nannyml.com/)
- [Alibi Detect](https://docs.seldon.io/projects/alibi-detect/)
- [Great Expectations](https://docs.greatexpectations.io/)

---

*เอกสารนี้จัดทำเพื่อประกอบการเรียนการสอนวิชา MLOps*