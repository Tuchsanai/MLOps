# 📚 Model Monitoring with Scikit-Learn: Theory & Practice Guide

## สารบัญ (Table of Contents)
1. [บทนำ: Model Monitoring คืออะไร?](#1-บทนำ-model-monitoring-คืออะไร)
2. [Section 1: Data Quality Monitoring](#section-1-data-quality-monitoring)
3. [Section 2: Model Performance Tracking](#section-2-model-performance-tracking)
4. [Section 3: Target Drift Detection](#section-3-target-drift-detection)
5. [Section 4: Building Monitoring Dashboard](#section-4-building-monitoring-dashboard)
6. [Best Practices และแนวทางปฏิบัติ](#best-practices-และแนวทางปฏิบัติ)

---

## 1. บทนำ: Model Monitoring คืออะไร?

### 1.1 ความหมายและความสำคัญ

**Model Monitoring** คือกระบวนการติดตามและเฝ้าระวังประสิทธิภาพของโมเดล Machine Learning หลังจากที่ได้ Deploy ไปใช้งานจริง (Production) เพื่อให้มั่นใจว่าโมเดลยังคงทำงานได้อย่างถูกต้องและน่าเชื่อถือ

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML Model Lifecycle                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Training → Validation → Deployment → [MONITORING] → Retrain   │
│                                            ↑                    │
│                                            │                    │
│                              ┌─────────────┴─────────────┐      │
│                              │   • Data Quality          │      │
│                              │   • Performance Metrics   │      │
│                              │   • Drift Detection       │      │
│                              │   • Alerts & Actions      │      │
│                              └───────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 ทำไมต้อง Monitor โมเดล?

| ปัญหา | คำอธิบาย | ผลกระทบ |
|-------|----------|---------|
| **Data Drift** | ข้อมูลในโลกจริงเปลี่ยนแปลงตลอดเวลา | โมเดลทำนายผิดพลาดมากขึ้น |
| **Concept Drift** | ความสัมพันธ์ระหว่าง features และ target เปลี่ยนไป | โมเดลไม่สามารถเรียนรู้ pattern ใหม่ |
| **Model Degradation** | ประสิทธิภาพโมเดลลดลงเมื่อเวลาผ่านไป | Business Impact สูง |
| **Data Quality Issues** | ปัญหา missing values, outliers, duplicates | Garbage In, Garbage Out |

### 1.3 องค์ประกอบหลักของ Model Monitoring

```python
# โครงสร้างหลักของ Monitoring System
monitoring_components = {
    "Data Quality": ["Missing Values", "Duplicates", "Outliers", "Schema Validation"],
    "Performance": ["Accuracy", "Precision", "Recall", "F1", "AUC-ROC"],
    "Drift Detection": ["Feature Drift", "Target Drift", "Prediction Drift"],
    "Alerting": ["Threshold Alerts", "Anomaly Alerts", "Trend Alerts"]
}
```

---

## Section 1: Data Quality Monitoring

### 1.1 ทฤษฎี: Data Quality คืออะไร?

**Data Quality** หมายถึงระดับความถูกต้อง ครบถ้วน และเชื่อถือได้ของข้อมูล หลักการสำคัญคือ **"Garbage In, Garbage Out"** - ถ้าข้อมูลไม่ดี โมเดลก็ไม่สามารถทำนายได้ดี

#### มิติของ Data Quality (Data Quality Dimensions)

```
┌────────────────────────────────────────────────────────────┐
│                   DATA QUALITY DIMENSIONS                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Completeness│  │  Accuracy   │  │ Consistency │        │
│  │ (ครบถ้วน)   │  │ (ถูกต้อง)   │  │ (สอดคล้อง)  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Timeliness │  │   Validity  │  │  Uniqueness │        │
│  │ (ทันเวลา)   │  │ (ถูกรูปแบบ) │  │ (ไม่ซ้ำซ้อน)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────────────────────────────────────────┘
```

### 1.2 การตรวจสอบ Missing Values

**Missing Values** คือค่าที่หายไปหรือไม่มีการบันทึกในข้อมูล สามารถแบ่งได้ 3 ประเภท:

| ประเภท | คำอธิบาย | ตัวอย่าง |
|--------|----------|----------|
| **MCAR** (Missing Completely at Random) | ข้อมูลหายไปแบบสุ่มทั้งหมด | เซ็นเซอร์เสียแบบสุ่ม |
| **MAR** (Missing at Random) | ข้อมูลหายขึ้นกับตัวแปรอื่น | รายได้หายเฉพาะกลุ่มอายุน้อย |
| **MNAR** (Missing Not at Random) | ข้อมูลหายขึ้นกับค่าตัวเอง | คนรายได้สูงไม่กรอกรายได้ |

#### Code Implementation:

```python
class DataQualityMonitor:
    def check_missing_values(self):
        """ตรวจสอบ missing values"""
        missing = self.data.isnull().sum()
        missing_pct = (missing / len(self.data) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'column': missing.index,
            'missing_count': missing.values,
            'missing_percentage': missing_pct.values
        })
        # กรองเฉพาะ columns ที่มี missing
        missing_df = missing_df[missing_df['missing_count'] > 0].sort_values(
            'missing_percentage', ascending=False
        )
        return missing_df
```

**หลักการ:**
- ใช้ `isnull().sum()` นับจำนวน missing ในแต่ละ column
- คำนวณ % โดยหารด้วยจำนวน rows ทั้งหมด
- เรียงลำดับจากมากไปน้อยเพื่อให้เห็นปัญหาหลักก่อน

### 1.3 การตรวจสอบ Duplicates

**Duplicates** คือข้อมูลที่ซ้ำกัน อาจเกิดจาก:
- Data entry ซ้ำ
- ETL process มีปัญหา
- System integration ผิดพลาด

```python
def check_duplicates(self):
    """ตรวจสอบข้อมูลซ้ำ"""
    # ตรวจสอบ duplicate rows ทั้งหมด
    duplicate_rows = self.data.duplicated().sum()
    
    # ตรวจสอบ duplicate ตาม ID (ถ้ามี)
    id_columns = [col for col in self.data.columns if 'id' in col.lower()]
    duplicate_ids = {}
    
    for id_col in id_columns:
        dup_count = self.data[id_col].duplicated().sum()
        if dup_count > 0:
            duplicate_ids[id_col] = int(dup_count)
    
    return {
        'duplicate_rows': int(duplicate_rows),
        'duplicate_percentage': round(duplicate_rows / len(self.data) * 100, 2),
        'duplicate_ids': duplicate_ids
    }
```

### 1.4 การตรวจหา Outliers

**Outliers** คือค่าที่ผิดปกติหรืออยู่ห่างจากค่าส่วนใหญ่ มี 2 วิธีหลักในการตรวจจับ:

#### วิธีที่ 1: IQR Method (Interquartile Range)

```
                    IQR Method
    ◄───────────────────────────────────────────►
    
    Lower Bound                      Upper Bound
         │                                │
         ▼                                ▼
    Q1 - 1.5×IQR                   Q3 + 1.5×IQR
         │                                │
    ─────┴────────┬────────┬────────┬─────┴─────
                  Q1       Q2       Q3
                  │        │        │
                  ◄────────┴────────►
                        IQR
```

**สูตร:**
- IQR = Q3 - Q1
- Lower Bound = Q1 - 1.5 × IQR
- Upper Bound = Q3 + 1.5 × IQR

#### วิธีที่ 2: Z-Score Method

```python
# Z-score = (x - μ) / σ
# ถ้า |Z-score| > 3 → Outlier
```

#### Code Implementation:

```python
def detect_outliers(self, method='iqr', threshold=1.5):
    """ตรวจหา outliers"""
    numeric_cols = self.data.select_dtypes(include=[np.number]).columns
    outlier_info = []
    
    for col in numeric_cols:
        if method == 'iqr':
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = self.data[(self.data[col] < lower_bound) | 
                                 (self.data[col] > upper_bound)]
        else:  # z-score
            z_scores = np.abs(stats.zscore(self.data[col].dropna()))
            outliers = self.data[z_scores > threshold]
        
        outlier_info.append({
            'column': col,
            'outlier_count': len(outliers),
            'outlier_percentage': round(len(outliers) / len(self.data) * 100, 2)
        })
    
    return pd.DataFrame(outlier_info)
```

### 1.5 Data Quality Alert System

ระบบแจ้งเตือนใช้ **Threshold-based Approach** โดยกำหนดค่า threshold สำหรับแต่ละ metric:

```python
class DataQualityAlert:
    def __init__(self):
        self.thresholds = {
            'missing_rate': 0.05,      # ไม่เกิน 5% missing
            'duplicate_rate': 0.01,    # ไม่เกิน 1% duplicates
            'outlier_rate': 0.05       # ไม่เกิน 5% outliers
        }
```

```
┌─────────────────────────────────────────────────────────┐
│                 ALERT SEVERITY LEVELS                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🟢 HEALTHY    │  All metrics within threshold         │
│                                                         │
│  🟡 WARNING    │  Some metrics slightly above threshold│
│                │  (1x - 2x threshold)                  │
│                                                         │
│  🔴 CRITICAL   │  Metrics significantly above threshold│
│                │  (> 2x threshold)                     │
└─────────────────────────────────────────────────────────┘
```

---

## Section 2: Model Performance Tracking

### 2.1 ทฤษฎี: Classification Metrics

สำหรับ **Classification Problems** เราใช้ metrics ดังนี้:

#### Confusion Matrix

```
                    PREDICTED
                 │  Negative  │  Positive
         ────────┼────────────┼───────────
         Negative│     TN     │    FP     
  ACTUAL ────────┼────────────┼───────────
         Positive│     FN     │    TP     
```

| Metric | สูตร | ความหมาย |
|--------|------|----------|
| **Accuracy** | (TP + TN) / Total | ความถูกต้องโดยรวม |
| **Precision** | TP / (TP + FP) | จากที่ทำนาย Positive มีกี่ % ที่ถูก |
| **Recall** | TP / (TP + FN) | จาก Positive จริง ทำนายถูกกี่ % |
| **F1-Score** | 2 × (P × R) / (P + R) | Harmonic Mean ของ Precision และ Recall |
| **Specificity** | TN / (TN + FP) | จาก Negative จริง ทำนายถูกกี่ % |

#### เมื่อไหร่ใช้ Metric ไหน?

```
┌────────────────────────────────────────────────────────────────┐
│                    METRIC SELECTION GUIDE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Use Case                    │  Primary Metric                 │
│  ────────────────────────────┼────────────────────────────────│
│  Balanced Dataset            │  Accuracy, F1-Score            │
│  Imbalanced Dataset          │  F1-Score, AUC-ROC             │
│  Cost of FP is high          │  Precision                     │
│  Cost of FN is high          │  Recall                        │
│  Fraud Detection             │  Recall, F1-Score              │
│  Medical Diagnosis           │  Recall (Sensitivity)          │
│  Spam Detection              │  Precision                     │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 Code Implementation: Performance Monitor

```python
class ModelPerformanceMonitor:
    def calculate_classification_metrics(self, y_true, y_pred, y_prob=None):
        """คำนวณ metrics สำหรับ classification"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
        }
        
        # Confusion matrix values
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        metrics['true_positive'] = int(tp)
        metrics['true_negative'] = int(tn)
        metrics['false_positive'] = int(fp)
        metrics['false_negative'] = int(fn)
        
        # Specificity
        metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        return metrics
```

### 2.3 ทฤษฎี: Regression Metrics

สำหรับ **Regression Problems**:

| Metric | สูตร | คุณสมบัติ |
|--------|------|----------|
| **MAE** | Σ\|yᵢ - ŷᵢ\| / n | ค่าเฉลี่ยความคลาดเคลื่อนสัมบูรณ์, robust ต่อ outliers |
| **MSE** | Σ(yᵢ - ŷᵢ)² / n | ลงโทษ error ใหญ่มากกว่า |
| **RMSE** | √MSE | อยู่ในหน่วยเดียวกับ target |
| **R²** | 1 - (SS_res / SS_tot) | สัดส่วนความแปรปรวนที่อธิบายได้ (0-1) |
| **MAPE** | Σ\|(yᵢ - ŷᵢ)/yᵢ\| × 100 / n | % error, ระวัง division by zero |

```python
def calculate_regression_metrics(self, y_true, y_pred):
    """คำนวณ metrics สำหรับ regression"""
    return {
        'mae': mean_absolute_error(y_true, y_pred),
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score(y_true, y_pred),
        'mape': np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
    }
```

### 2.4 Baseline Comparison

การเปรียบเทียบกับ **Baseline** คือหัวใจของ Performance Monitoring:

```
┌─────────────────────────────────────────────────────────────┐
│              PERFORMANCE COMPARISON FRAMEWORK               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   BASELINE                      CURRENT                     │
│   (Training/Validation)         (Production)                │
│   ┌───────────────┐             ┌───────────────┐           │
│   │ Accuracy: 0.92│ ─────────►  │ Accuracy: 0.87│           │
│   │ F1: 0.89      │  Compare    │ F1: 0.82      │           │
│   └───────────────┘             └───────────────┘           │
│                                                             │
│   Degradation = (0.92 - 0.87) / 0.92 × 100 = 5.4%          │
│                                                             │
│   Status: 🟡 WARNING (degradation > 5%)                     │
└─────────────────────────────────────────────────────────────┘
```

```python
def _compare_with_baseline(self, current_metrics, task):
    """เปรียบเทียบกับ baseline"""
    comparison = {}
    
    for metric in key_metrics:
        baseline_val = self.baseline_metrics.get(metric, 0)
        current_val = current_metrics.get(metric, 0)
        
        change = current_val - baseline_val
        change_pct = (change / baseline_val * 100) if baseline_val != 0 else 0
        
        comparison[metric] = {
            'baseline': baseline_val,
            'current': current_val,
            'change': change,
            'change_pct': change_pct,
            'status': 'improved' if change > 0 else 'degraded' if change < 0 else 'stable'
        }
    
    return comparison
```

### 2.5 Performance Degradation Alerts

```
┌─────────────────────────────────────────────────────────────┐
│             PERFORMANCE DEGRADATION THRESHOLDS              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Degradation %      │  Status    │  Action                 │
│   ───────────────────┼────────────┼────────────────────────│
│   < 5%               │  🟢 OK     │  Continue monitoring    │
│   5% - 10%           │  🟡 WARN   │  Investigate cause      │
│   > 10%              │  🔴 CRIT   │  Consider retraining    │
│   > 20%              │  ⚫ FATAL  │  Immediate retrain      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 3: Target Drift Detection

### 3.1 ทฤษฎี: Types of Drift

**Drift** คือการเปลี่ยนแปลงของ data distribution ตามเวลา แบ่งได้ 3 ประเภทหลัก:

```
┌─────────────────────────────────────────────────────────────────┐
│                      TYPES OF DRIFT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. DATA DRIFT (Covariate Drift)                               │
│     P(X) changes, but P(Y|X) remains the same                  │
│     ตัวอย่าง: ลูกค้ากลุ่มใหม่เข้ามา แต่ pattern ยังเหมือนเดิม   │
│                                                                 │
│  2. CONCEPT DRIFT                                               │
│     P(Y|X) changes                                              │
│     ตัวอย่าง: พฤติกรรมการผิดนัดชำระเปลี่ยนไป                   │
│                                                                 │
│  3. TARGET DRIFT (Label Drift)                                  │
│     P(Y) changes                                                │
│     ตัวอย่าง: อัตราการ default เพิ่มขึ้นในช่วง recession       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Drift Patterns Over Time

```
1. SUDDEN DRIFT                2. GRADUAL DRIFT
   │                              │
   │    ┌────────                 │         ╱────
   │    │                         │       ╱
   │────┘                         │     ╱
   │                              │   ╱
   └────────────►                 └──────────────►
        time                           time

3. INCREMENTAL DRIFT           4. RECURRING DRIFT
   │                              │
   │          ╱──                 │  ╱╲    ╱╲
   │        ╱                     │ ╱  ╲  ╱  ╲
   │      ╱                       │╱    ╲╱    ╲
   │────╱                         │
   └────────────►                 └──────────────►
        time                           time
```

### 3.2 Statistical Tests สำหรับ Drift Detection

#### 3.2.1 Kolmogorov-Smirnov Test (KS Test)

ใช้สำหรับ **continuous variables**

**หลักการ:**
- เปรียบเทียบ Cumulative Distribution Function (CDF) ของสอง samples
- H₀: ทั้งสอง distributions มาจากประชากรเดียวกัน
- ถ้า p-value < 0.05 → Reject H₀ → มี drift

```python
def ks_test(self, reference_col, current_col):
    """Kolmogorov-Smirnov Test"""
    statistic, p_value = ks_2samp(reference_col.dropna(), current_col.dropna())
    return {
        'test': 'Kolmogorov-Smirnov',
        'statistic': statistic,  # Max difference between CDFs
        'p_value': p_value,
        'drift_detected': p_value < 0.05
    }
```

```
KS Test Visualization:

     CDF
     1.0 ┤          ●●●●●●●●●●●●
         │       ●●●       ○○○○○○
         │    ●●●      ○○○○
     0.5 ┤  ●●●    ○○○○  ← D = max difference
         │ ●●   ○○○
         │●  ○○○
     0.0 ┼○○○─────────────────────►
                Value
         
         ● Reference  ○ Current
```

#### 3.2.2 Chi-Square Test

ใช้สำหรับ **categorical variables**

```python
def chi_square_test(self, reference_col, current_col):
    """Chi-Square Test สำหรับ categorical variables"""
    # สร้าง contingency table
    ref_counts = reference_col.value_counts()
    curr_counts = current_col.value_counts()
    
    all_categories = set(ref_counts.index) | set(curr_counts.index)
    
    ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
    curr_freq = [curr_counts.get(cat, 0) for cat in all_categories]
    
    contingency = np.array([ref_freq, curr_freq])
    
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    
    return {
        'test': 'Chi-Square',
        'statistic': chi2,
        'p_value': p_value,
        'drift_detected': p_value < 0.05
    }
```

#### 3.2.3 Population Stability Index (PSI)

**PSI** เป็น metric ที่นิยมใช้ในอุตสาหกรรมการเงิน

**สูตร:**
```
PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)
```

**การแปลผล:**

| PSI Value | Interpretation | Action |
|-----------|----------------|--------|
| < 0.10 | No significant change | Continue monitoring |
| 0.10 - 0.25 | Slight change | Minor investigation |
| ≥ 0.25 | Significant change | Major investigation/retrain |

```python
def calculate_psi(self, reference_col, current_col, bins=10):
    """Population Stability Index"""
    # สร้าง bins จาก reference
    bin_edges = np.linspace(reference_col.min(), reference_col.max(), bins + 1)
    
    # คำนวณ % ในแต่ละ bin
    ref_hist, _ = np.histogram(reference_col, bins=bin_edges)
    curr_hist, _ = np.histogram(current_col, bins=bin_edges)
    
    ref_pct = ref_hist / len(reference_col)
    curr_pct = curr_hist / len(current_col)
    
    # หลีกเลี่ยง log(0)
    ref_pct = np.where(ref_pct == 0, 0.0001, ref_pct)
    curr_pct = np.where(curr_pct == 0, 0.0001, curr_pct)
    
    # คำนวณ PSI
    psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
    
    return {
        'psi': psi,
        'interpretation': 'No Drift' if psi < 0.1 else 
                         'Slight Drift' if psi < 0.25 else 
                         'Significant Drift'
    }
```

#### 3.2.4 Wasserstein Distance (Earth Mover's Distance)

**Wasserstein Distance** วัดระยะห่างระหว่างสอง distributions โดยคิดจากปริมาณ "work" ที่ต้องใช้ในการเปลี่ยน distribution หนึ่งไปเป็นอีก distribution หนึ่ง

```python
def wasserstein_distance_test(self, reference_col, current_col):
    """Wasserstein Distance"""
    distance = wasserstein_distance(reference_col.dropna(), current_col.dropna())
    
    # Normalize by reference std
    ref_std = reference_col.std()
    normalized_distance = distance / ref_std if ref_std > 0 else distance
    
    return {
        'distance': distance,
        'normalized_distance': normalized_distance,
        'drift_detected': normalized_distance > 0.1
    }
```

### 3.3 Prediction Drift Detection

นอกจากตรวจจับ drift ของ input data และ target แล้ว ยังต้องตรวจจับ **Prediction Drift** ด้วย:

```python
def detect_prediction_drift(model, scaler, reference_data, current_data):
    """ตรวจจับ Prediction Drift"""
    # ทำนาย probability
    ref_proba = model.predict_proba(X_ref_scaled)[:, 1]
    curr_proba = model.predict_proba(X_curr_scaled)[:, 1]
    
    # Statistical tests
    ks_stat, ks_pval = ks_2samp(ref_proba, curr_proba)
    wasserstein = wasserstein_distance(ref_proba, curr_proba)
    
    return {
        'ks_statistic': ks_stat,
        'ks_pvalue': ks_pval,
        'wasserstein_distance': wasserstein,
        'drift_detected': ks_pval < 0.05
    }
```

### 3.4 Drift Detection Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                 DRIFT DETECTION DECISION MATRIX                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Variable Type    │  Recommended Test   │  Alternative           │
│  ─────────────────┼─────────────────────┼────────────────────────│
│  Continuous       │  KS Test + PSI      │  Wasserstein Distance  │
│  Categorical      │  Chi-Square Test    │  Jensen-Shannon Div    │
│  Binary Target    │  Chi-Square Test    │  Proportion Z-test     │
│  Predictions      │  KS Test            │  Wasserstein Distance  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Section 4: Building Monitoring Dashboard

### 4.1 ทฤษฎี: Dashboard Design Principles

**Monitoring Dashboard** ที่ดีควรมีคุณสมบัติดังนี้:

```
┌─────────────────────────────────────────────────────────────────┐
│                   DASHBOARD DESIGN PRINCIPLES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. VISIBILITY (เห็นภาพรวม)                                    │
│     - Overall status at a glance                                │
│     - Key metrics prominently displayed                         │
│                                                                 │
│  2. ACTIONABLE (นำไปปฏิบัติได้)                                │
│     - Clear alerts with severity levels                         │
│     - Recommended actions                                       │
│                                                                 │
│  3. HISTORICAL (มีประวัติ)                                     │
│     - Trend visualization                                       │
│     - Comparison with baseline                                  │
│                                                                 │
│  4. DRILL-DOWN (ดูรายละเอียดได้)                               │
│     - From summary to detail                                    │
│     - Root cause investigation                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Dashboard Components

```
┌──────────────────────────────────────────────────────────────────┐
│                    MODEL MONITORING DASHBOARD                    │
├──────────┬────────────────────────────────────────┬──────────────┤
│          │                                        │              │
│  STATUS  │        PERFORMANCE METRICS             │   ALERTS     │
│  🟢/🟡/🔴 │    ┌────────────────────────┐         │  ┌────────┐  │
│          │    │  Accuracy  ████████ 92% │         │  │ 0 CRIT │  │
│          │    │  Precision ███████  89% │         │  │ 2 WARN │  │
│          │    │  Recall    ██████   85% │         │  └────────┘  │
│          │    │  F1-Score  ███████  87% │         │              │
│          │    └────────────────────────┘         │              │
├──────────┴────────────────────────────────────────┴──────────────┤
│                                                                  │
│  DATA QUALITY                    │  DRIFT DETECTION              │
│  ┌────────────────────┐          │  ┌────────────────────┐      │
│  │ Missing:   ▓▓ 2%   │          │  │ Feature Drift: 3/10│      │
│  │ Duplicate: ▓ 0.5%  │          │  │ Target Drift: NO   │      │
│  │ Outliers:  ▓▓▓ 4%  │          │  │ Pred Drift: YES    │      │
│  └────────────────────┘          │  └────────────────────┘      │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                        TREND OVER TIME                           │
│     100% ┤                                                       │
│          │  ●──●──●──●──●                                       │
│      80% ┤           ╲──●──●──●                                 │
│          │                                                       │
│      60% ┤                                                       │
│          └──┬──┬──┬──┬──┬──┬──┬──►                              │
│             W1 W2 W3 W4 W5 W6 W7 W8                              │
└──────────────────────────────────────────────────────────────────┘
```

### 4.3 Comprehensive Dashboard Class

```python
class ModelMonitoringDashboard:
    """Dashboard สำหรับ Model Monitoring"""
    
    def __init__(self, model, model_name="ML Model"):
        self.model = model
        self.model_name = model_name
        self.reports = {
            'data_quality': {},
            'performance': {},
            'drift': {},
            'alerts': []
        }
    
    def run_full_monitoring(self, reference_data, current_data, target_col, scaler=None):
        """รัน monitoring ทั้งหมด"""
        
        # 1. Data Quality Monitoring
        print("📊 [1/4] Running Data Quality Check...")
        dq_monitor = DataQualityMonitor(current_data)
        self.reports['data_quality'] = {
            'missing': dq_monitor.check_missing_values(),
            'duplicates': dq_monitor.check_duplicates(),
            'outliers': dq_monitor.detect_outliers()
        }
        
        # 2. Performance Monitoring
        print("📈 [2/4] Running Performance Evaluation...")
        # ... คำนวณ metrics ...
        
        # 3. Drift Detection
        print("🔍 [3/4] Running Drift Detection...")
        drift_detector = DriftDetector(reference_data)
        # ... ตรวจจับ drift ...
        
        # 4. Generate Alerts
        print("🚨 [4/4] Generating Alerts...")
        self._generate_alerts()
        
        return self.reports
```

### 4.4 Alert Generation Logic

```python
def _generate_alerts(self):
    """สร้าง alerts จากผลการ monitoring"""
    self.reports['alerts'] = []
    
    # Data Quality Alerts
    if missing_count > 0:
        self.reports['alerts'].append({
            'type': 'WARNING',
            'category': 'Data Quality',
            'message': 'พบ missing values ในข้อมูล'
        })
    
    # Performance Alerts
    degradation = (baseline_acc - current_acc) / baseline_acc * 100
    if degradation > 10:
        self.reports['alerts'].append({
            'type': 'CRITICAL',
            'category': 'Performance',
            'message': f"Accuracy ลดลง {degradation:.1f}%"
        })
    
    # Drift Alerts
    if target_drift_detected:
        self.reports['alerts'].append({
            'type': 'CRITICAL',
            'category': 'Drift',
            'message': 'ตรวจพบ Target Drift'
        })
```

### 4.5 Report Export

การ export report เพื่อแชร์กับ stakeholders:

```python
def export_report(self, filename=None):
    """Export report เป็น dictionary/JSON"""
    return {
        'model_name': self.model_name,
        'timestamp': datetime.now().isoformat(),
        'data_quality': {...},
        'performance': {...},
        'drift': {...},
        'alerts': self.reports['alerts'],
        'overall_status': 'CRITICAL' if any_critical else 
                         'WARNING' if any_warning else 
                         'HEALTHY'
    }
```

---

## Best Practices และแนวทางปฏิบัติ

### 1. กำหนด Baseline ที่ชัดเจน

```
┌─────────────────────────────────────────────────────────────────┐
│                     BASELINE ESTABLISHMENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✓ บันทึก performance metrics เมื่อ deploy                     │
│  ✓ เก็บ reference data distribution                            │
│  ✓ กำหนด threshold สำหรับแต่ละ metric                          │
│  ✓ Document assumptions และ limitations                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Monitor อย่างสม่ำเสมอ

| Metric Type | Recommended Frequency |
|-------------|----------------------|
| Data Quality | Real-time / Daily |
| Model Performance | Daily / Weekly |
| Drift Detection | Weekly / Monthly |
| Full Dashboard Review | Weekly |

### 3. ตั้ง Threshold ที่เหมาะสม

```python
# Example threshold configuration
thresholds = {
    # Data Quality
    'missing_rate': {'warning': 0.05, 'critical': 0.10},
    'duplicate_rate': {'warning': 0.01, 'critical': 0.05},
    
    # Performance
    'accuracy_degradation': {'warning': 0.05, 'critical': 0.10},
    'f1_degradation': {'warning': 0.05, 'critical': 0.10},
    
    # Drift
    'psi': {'warning': 0.10, 'critical': 0.25},
    'ks_pvalue': {'threshold': 0.05}
}
```

### 4. มี Action Plan

```
┌─────────────────────────────────────────────────────────────────┐
│                     ALERT RESPONSE MATRIX                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Alert Level   │  Response Time  │  Action                      │
│  ─────────────┼─────────────────┼──────────────────────────────│
│  🟢 HEALTHY   │  -              │  Continue monitoring         │
│  🟡 WARNING   │  < 24 hours     │  Investigate, prepare retrain│
│  🔴 CRITICAL  │  < 4 hours      │  Immediate investigation     │
│  ⚫ FATAL     │  Immediate      │  Rollback / Emergency retrain│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Document Everything

```python
# Monitoring log structure
monitoring_log = {
    'timestamp': '2024-01-15T10:30:00',
    'model_version': 'v1.2.3',
    'data_period': '2024-01-08 to 2024-01-14',
    'metrics': {...},
    'alerts': [...],
    'actions_taken': 'None required',
    'reviewed_by': 'ML Engineer'
}
```

---

## Quick Reference: Monitoring Checklist

```
□ Data Quality
  □ Missing values < 5%
  □ Duplicates < 1%
  □ Outliers investigated
  □ Schema validation passed

□ Model Performance
  □ Accuracy within acceptable range
  □ Precision/Recall balanced
  □ F1-Score stable
  □ Confusion matrix reviewed

□ Drift Detection
  □ Feature distributions checked
  □ Target drift assessed
  □ Prediction drift analyzed
  □ PSI < 0.10 for all features

□ Alerts & Actions
  □ All critical alerts addressed
  □ Warning alerts investigated
  □ Action plan documented
  □ Stakeholders notified
```

---

## สรุป

Model Monitoring เป็นส่วนสำคัญของ MLOps ที่ช่วยให้มั่นใจว่าโมเดลทำงานได้อย่างถูกต้องหลัง deploy:

1. **Data Quality Monitoring** - ตรวจสอบคุณภาพข้อมูลก่อนเข้าโมเดล
2. **Performance Tracking** - ติดตามประสิทธิภาพโมเดลเทียบกับ baseline
3. **Drift Detection** - ตรวจจับการเปลี่ยนแปลงของ data/target distribution
4. **Dashboard & Alerts** - รวมทุกอย่างใน single view พร้อมระบบแจ้งเตือน

การทำ monitoring ที่ดีช่วยให้ทีมสามารถตอบสนองต่อปัญหาได้รวดเร็ว และรักษา business value ของ ML models ไว้ได้อย่างต่อเนื่อง