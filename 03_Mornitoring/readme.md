# แนวคิดหัวข้อ LAB: Model Monitoring 

## Section 1: Foundation & Model Performance Monitoring

### LAB 1.1: Introduction to Evidently AI
- ติดตั้งและตั้งค่า Evidently
- ทำความเข้าใจโครงสร้าง Report และ Test Suite
- สร้าง Report แรกจาก dataset ตัวอย่าง

### LAB 1.2: Data Quality Monitoring
- ตรวจสอบ missing values, duplicates
- วิเคราะห์ data integrity และ consistency
- สร้าง Data Quality Report และตั้ง threshold alerts

### LAB 1.3: Model Performance Tracking
- ติดตาม classification metrics (Accuracy, Precision, Recall, F1)
- ติดตาม regression metrics (MAE, RMSE, R²)
- เปรียบเทียบ performance ระหว่าง reference vs current data

### LAB 1.4: Target Drift Detection
- ตรวจจับการเปลี่ยนแปลงของ target distribution
- วิเคราะห์ prediction drift
- สร้าง alerts เมื่อ target drift เกินค่าที่กำหนด

### LAB 1.5: Building Monitoring Dashboard
- สร้าง interactive HTML reports
- รวม multiple metrics ใน single dashboard
- Export และ share reports

### LAB 1.6: Automated Testing with Test Suites
- สร้าง Test Suite สำหรับ model validation
- กำหนด pass/fail conditions
- Integrate testing เข้ากับ CI/CD pipeline concept

---

## Section 2: Data Drift & Advanced Monitoring

### LAB 2.1: Understanding Data Drift Concepts
- ทฤษฎี Covariate Shift vs Concept Drift
- Statistical tests สำหรับ drift detection (KS, PSI, Wasserstein)
- เลือก drift detection method ที่เหมาะสม

### LAB 2.2: Feature Drift Detection
- ตรวจจับ drift ในแต่ละ feature
- วิเคราะห์ numerical vs categorical feature drift
- Visualize feature distributions over time

### LAB 2.3: Multivariate Drift Analysis
- ตรวจจับ drift ที่เกิดจากความสัมพันธ์ระหว่าง features
- Dataset-level drift detection
- Correlation analysis between features

### LAB 2.4: Drift Detection in Production Simulation
- สร้าง simulated data stream ที่มี gradual drift
- Detect sudden vs gradual drift
- Implement sliding window monitoring

### LAB 2.5: Custom Metrics & Drift Thresholds
- สร้าง custom drift metrics
- ปรับ threshold ตาม business requirements
- Handle false positives/negatives ใน drift detection

### LAB 2.6: End-to-End Monitoring Pipeline
- รวมทุก components เข้าด้วยกัน
- สร้าง automated monitoring workflow
- Integrate กับ MLflow สำหรับ experiment tracking

---

## ตัวอย่าง Dataset ที่แนะนำ

| Dataset | Use Case | เหมาะกับ LAB |
|---------|----------|--------------|
| Credit Card Fraud | Classification + Imbalanced | Performance, Target Drift |
| House Prices | Regression | Feature Drift, Performance |
| Bike Sharing | Time-series regression | Gradual Drift, Seasonality |
| Adult Income | Classification + Mixed features | Data Quality, Feature Drift |

---

## Progression Flow

```
Section 1 (Foundation)          Section 2 (Advanced)
        │                               │
   Setup → Data Quality            Drift Theory
        │                               │
   Performance Metrics         Feature-level Drift
        │                               │
   Target Drift                Multivariate Drift
        │                               │
   Dashboard                   Production Simulation
        │                               │
   Test Suites                 Custom Metrics
        │                               │
        └──────────> Final Integration <─┘
```

---

