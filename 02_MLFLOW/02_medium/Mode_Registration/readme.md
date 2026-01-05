# 🏛️ MLflow Model Registry: คู่มือทฤษฎีและแบบฝึกหัดปฏิบัติ

> **วิชา:** MLOps (Machine Learning Operations)  
> **หัวข้อ:** Model Registry และ Model Lifecycle Management  
> **ระดับ:** ปริญญาตรี/บัณฑิตศึกษา

---

## 📋 สารบัญ

1. [บทนำ: ทำไมต้องมี Model Registry?](#1-บทนำ-ทำไมต้องมี-model-registry)
2. [Machine Learning Lifecycle](#2-machine-learning-lifecycle)
3. [ปัญหาที่เกิดขึ้นเมื่อไม่มี Model Registry](#3-ปัญหาที่เกิดขึ้นเมื่อไม่มี-model-registry)
4. [Model Registry คืออะไร?](#4-model-registry-คืออะไร)
5. [องค์ประกอบหลักของ Model Registry](#5-องค์ประกอบหลักของ-model-registry)
6. [Model Stages และ Aliases](#6-model-stages-และ-aliases)
7. [ความสัมพันธ์ระหว่าง Components ใน MLflow](#7-ความสัมพันธ์ระหว่าง-components-ใน-mlflow)
8. [Best Practices](#8-best-practices)
9. [คำอธิบายแบบฝึกหัด](#9-คำอธิบายแบบฝึกหัด)
10. [แหล่งข้อมูลเพิ่มเติม](#10-แหล่งข้อมูลเพิ่มเติม)

---

## 1. บทนำ: ทำไมต้องมี Model Registry?

### 1.1 บริบทของ Machine Learning ในองค์กร

ในยุคปัจจุบัน องค์กรต่างๆ นำ Machine Learning มาใช้งานอย่างแพร่หลาย ตั้งแต่การแนะนำสินค้า (Recommendation Systems) ไปจนถึงการตรวจจับการฉ้อโกง (Fraud Detection) แต่ความท้าทายที่สำคัญคือ **การจัดการ Model ที่มีจำนวนมากและเปลี่ยนแปลงบ่อย**

### 1.2 ความท้าทายในการพัฒนา ML

| ความท้าทาย | คำอธิบาย |
|------------|----------|
| **Model Proliferation** | จำนวน Model เพิ่มขึ้นอย่างรวดเร็ว ทำให้ยากต่อการจัดการ |
| **Reproducibility** | ยากที่จะสร้าง Model เดิมซ้ำได้เหมือนเดิมทุกประการ |
| **Collaboration** | ทีมงานหลายคนทำงานร่วมกันบน Model เดียวกันได้ยาก |
| **Deployment Complexity** | การนำ Model ไปใช้งานจริงมีความซับซ้อน |
| **Governance & Compliance** | ต้องมีการตรวจสอบและอนุมัติก่อนใช้งาน |

### 1.3 Model Registry เป็นคำตอบ

**Model Registry** คือระบบจัดการ Model แบบรวมศูนย์ที่ช่วยแก้ปัญหาเหล่านี้ โดยทำหน้าที่เป็น **"Single Source of Truth"** สำหรับ Model ทั้งหมดในองค์กร

---

## 2. Machine Learning Lifecycle

### 2.1 ภาพรวมของ ML Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Machine Learning Lifecycle                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │   Data   │───▶│  Model   │───▶│  Model   │───▶│  Model   │              │
│   │Collection│    │ Training │    │Evaluation│    │Deployment│              │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
│        │               │               │               │                     │
│        ▼               ▼               ▼               ▼                     │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │   Data   │    │Experiment│    │  Model   │    │Monitoring│              │
│   │Processing│    │ Tracking │    │ Registry │    │& Logging │              │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
│                                                                              │
│                    ◀─────── Feedback Loop ───────▶                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 รายละเอียดแต่ละขั้นตอน

#### 2.2.1 Data Collection & Processing

เป็นขั้นตอนแรกที่รวบรวมและเตรียมข้อมูลสำหรับการฝึก Model โดยมีกิจกรรมหลักดังนี้:

- **Data Ingestion:** รวบรวมข้อมูลจากแหล่งต่างๆ (Database, API, Files)
- **Data Cleaning:** ทำความสะอาดข้อมูล จัดการ Missing Values
- **Feature Engineering:** สร้าง Features ใหม่จากข้อมูลดิบ
- **Data Validation:** ตรวจสอบคุณภาพข้อมูล

#### 2.2.2 Model Training

ขั้นตอนการฝึก Model ด้วย Algorithm ต่างๆ:

- **Algorithm Selection:** เลือก Algorithm ที่เหมาะสม
- **Hyperparameter Tuning:** ปรับค่า Parameters
- **Cross-Validation:** ตรวจสอบความถูกต้อง
- **Experiment Tracking:** บันทึกการทดลอง (MLflow Tracking)

#### 2.2.3 Model Evaluation

ประเมินประสิทธิภาพของ Model:

- **Metrics Calculation:** คำนวณ Accuracy, F1-Score, RMSE ฯลฯ
- **Model Comparison:** เปรียบเทียบ Model หลายตัว
- **Bias Detection:** ตรวจสอบ Bias ใน Model
- **A/B Testing:** ทดสอบเปรียบเทียบกับ Model เดิม

#### 2.2.4 Model Deployment

นำ Model ไปใช้งานจริง:

- **Model Packaging:** เตรียม Model สำหรับ Deploy
- **API Creation:** สร้าง REST API
- **Containerization:** สร้าง Docker Image
- **Scaling:** ขยายระบบรองรับ Load

---

## 3. ปัญหาที่เกิดขึ้นเมื่อไม่มี Model Registry

### 3.1 สถานการณ์จำลอง: โฟลเดอร์ที่วุ่นวาย

ลองนึกภาพโปรเจกต์ ML ที่ไม่มีระบบจัดการ:

```
📁 โปรเจกต์ ML (ไม่มี Model Registry)
├── model_v1.pkl
├── model_v2.pkl
├── model_v2_fixed.pkl
├── model_v2_fixed_final.pkl
├── model_v2_fixed_final_REAL.pkl      ← 😱 อันไหนดีที่สุด?
├── model_best.pkl
├── model_best_new.pkl
├── model_production_maybe.pkl          ← 😵 งง!
├── model_john_test.pkl
├── model_mary_experiment.pkl
└── model_DONT_DELETE.pkl               ← 😰 ใครจะกล้าลบ?
```

### 3.2 ปัญหาที่พบบ่อย

| ปัญหา | คำอธิบาย | ผลกระทบ |
|-------|----------|---------|
| 🔍 **หาโมเดลไม่เจอ** | ไม่รู้ว่าโมเดลไหนดีที่สุด | ต้องฝึกใหม่ เสียเวลาและทรัพยากร |
| 📊 **ไม่รู้ Hyperparameters** | จำไม่ได้ว่าใช้ค่าอะไรฝึก | ไม่สามารถ Reproduce ได้ |
| 🔄 **ไม่มี Version Control** | ไม่สามารถย้อนกลับไปใช้โมเดลเก่าได้ | เสี่ยงต่อการสูญเสียงานที่ทำไว้ |
| 👥 **ทำงานเป็นทีมยาก** | ไม่รู้ว่าใครแก้ไขอะไร เมื่อไหร่ | เกิดความขัดแย้งและความสับสน |
| 🚀 **Deploy ยาก** | ไม่มั่นใจว่าโมเดลไหนพร้อม Production | เสี่ยงต่อการ Deploy Model ที่ไม่ถูกต้อง |
| 📝 **ไม่มี Audit Trail** | ไม่สามารถตรวจสอบย้อนหลังได้ | ปัญหาด้าน Compliance และ Governance |
| 🔗 **ไม่มี Lineage** | ไม่รู้ว่า Model มาจากข้อมูลและการทดลองใด | ยากต่อการ Debug และปรับปรุง |

### 3.3 ผลกระทบทางธุรกิจ

- **เสียเวลา:** ต้องหา Model ที่ถูกต้องนานหลายชั่วโมง
- **เสียเงิน:** ต้องฝึก Model ใหม่เพราะหาของเดิมไม่เจอ
- **เสี่ยง:** Deploy Model ผิดตัวทำให้ผลลัพธ์ไม่ดี
- **Compliance:** ไม่สามารถตอบคำถาม Auditor ได้

---

## 4. Model Registry คืออะไร?

### 4.1 คำนิยาม

**Model Registry** คือระบบจัดการ Machine Learning Model แบบรวมศูนย์ (Centralized Model Management System) ที่ทำหน้าที่:

1. **จัดเก็บ Model** อย่างเป็นระบบ
2. **ติดตาม Version** ทั้งหมด
3. **จัดการ Lifecycle** ของ Model
4. **บันทึก Metadata** ที่เกี่ยวข้อง
5. **ควบคุมการเข้าถึง** และการ Deploy

### 4.2 โครงสร้างของ Model Registry

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         🏛️ MLflow Model Registry                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  📦 Registered Model: "iris-classifier"                              │    │
│  │  ├── 📋 Description: โมเดลจำแนกดอกไอริส                               │    │
│  │  ├── 🏷️ Tags: [classification, sklearn, production-ready]           │    │
│  │  │                                                                   │    │
│  │  ├── 📌 Version 1 ─────────────────────────────────────────────────  │    │
│  │  │   ├── Stage: ⚫ Archived                                          │    │
│  │  │   ├── Created: 2024-01-15 10:30:00                               │    │
│  │  │   ├── Accuracy: 0.92                                             │    │
│  │  │   ├── Algorithm: RandomForest(n_estimators=50)                   │    │
│  │  │   └── Run ID: abc123...                                          │    │
│  │  │                                                                   │    │
│  │  ├── 📌 Version 2 ─────────────────────────────────────────────────  │    │
│  │  │   ├── Stage: 🟡 Staging                                          │    │
│  │  │   ├── Created: 2024-01-20 14:45:00                               │    │
│  │  │   ├── Accuracy: 0.95                                             │    │
│  │  │   ├── Algorithm: RandomForest(n_estimators=100)                  │    │
│  │  │   └── Run ID: def456...                                          │    │
│  │  │                                                                   │    │
│  │  └── 📌 Version 3 ─────────────────────────────────────────────────  │    │
│  │      ├── Stage: 🟢 Production  ← กำลังใช้งานจริง                      │    │
│  │      ├── Created: 2024-01-25 09:00:00                               │    │
│  │      ├── Accuracy: 0.97                                             │    │
│  │      ├── Algorithm: GradientBoosting(n_estimators=100)              │    │
│  │      └── Run ID: ghi789...                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 ประโยชน์ของ Model Registry

| ประโยชน์ | คำอธิบาย | ตัวอย่างการใช้งาน |
|----------|----------|-------------------|
| **🔢 Version Control** | ติดตามทุกเวอร์ชันของโมเดล | ย้อนกลับไปใช้ Version 2 ได้ทันที |
| **📊 Metadata Tracking** | เก็บข้อมูลที่เกี่ยวข้องทั้งหมด | Parameters, Metrics, Artifacts |
| **🚦 Stage Management** | จัดการสถานะการใช้งาน | Staging → Production |
| **👥 Collaboration** | ทำงานร่วมกันเป็นทีม | ทุกคนเห็นโมเดลเดียวกัน |
| **📝 Audit Trail** | ติดตามการเปลี่ยนแปลง | ใครเปลี่ยนอะไร เมื่อไหร่ |
| **🔗 Lineage** | เชื่อมโยงกับ Experiment | รู้ว่าโมเดลมาจาก Run ไหน |
| **🔒 Access Control** | ควบคุมสิทธิ์การเข้าถึง | กำหนดว่าใครสามารถ Deploy ได้ |
| **📦 Standardization** | มาตรฐานการจัดเก็บ | ทุก Model มีโครงสร้างเดียวกัน |

---

## 5. องค์ประกอบหลักของ Model Registry

### 5.1 Registered Model

**Registered Model** คือชื่อที่ใช้เรียก Model ในระบบ เปรียบเสมือน "โปรเจกต์" หนึ่งโปรเจกต์

**คุณสมบัติ:**
- มีชื่อเฉพาะ (Unique Name)
- มี Description อธิบายจุดประสงค์
- มี Tags สำหรับการจัดหมวดหมู่
- มีหลาย Versions ได้

**ตัวอย่าง:**
```
Registered Model: "fraud-detection-xgboost"
├── Description: "ตรวจจับการฉ้อโกงบัตรเครดิต"
├── Tags: [classification, xgboost, fraud, production]
└── Versions: [1, 2, 3, 4, 5]
```

### 5.2 Model Version

**Model Version** คือ Instance หนึ่งของ Registered Model ที่สร้างจากการฝึกครั้งหนึ่ง

**คุณสมบัติ:**
- Version Number (1, 2, 3, ...)
- เชื่อมโยงกับ Run ID
- มี Stage หรือ Alias
- มี Metadata และ Artifacts

**ตัวอย่าง:**
```
Version 3:
├── Run ID: abc123xyz
├── Stage: Production
├── Alias: champion
├── Created: 2024-01-25 09:00:00
├── Metrics: {accuracy: 0.97, f1: 0.96}
└── Parameters: {n_estimators: 100, max_depth: 10}
```

### 5.3 Model Artifacts

**Artifacts** คือไฟล์ที่เกี่ยวข้องกับ Model:

| Artifact | คำอธิบาย |
|----------|----------|
| **MLmodel** | ไฟล์ YAML ที่อธิบายโครงสร้าง Model |
| **model.pkl** | ไฟล์ Model (สำหรับ sklearn) |
| **model.pth** | ไฟล์ Model (สำหรับ PyTorch) |
| **conda.yaml** | Dependencies สำหรับรัน Model |
| **requirements.txt** | Python packages ที่ต้องการ |
| **input_example.json** | ตัวอย่าง Input data |

### 5.4 Metadata

**Metadata** คือข้อมูลที่อธิบาย Model:

```yaml
# ตัวอย่าง Metadata
model_name: iris-classifier
version: 3
created_by: john.doe@company.com
created_at: 2024-01-25T09:00:00Z

parameters:
  algorithm: GradientBoostingClassifier
  n_estimators: 100
  learning_rate: 0.1
  max_depth: 5

metrics:
  accuracy: 0.97
  f1_score: 0.96
  precision: 0.95
  recall: 0.97

tags:
  task: classification
  dataset: iris
  environment: production
  approved_by: ML-Team-Lead
```

---

## 6. Model Stages และ Aliases

### 6.1 Model Stages (Legacy)

MLflow มี 4 Stages หลัก (แบบเดิม):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Model Stage Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     ┌────────────┐                                                          │
│     │    None    │  ← โมเดลเพิ่งลงทะเบียน ยังไม่กำหนดสถานะ                    │
│     │    ⚪      │                                                          │
│     └─────┬──────┘                                                          │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │  Staging   │  ← กำลังทดสอบ (QA/Testing Environment)                    │
│     │    🟡      │    - ทดสอบ Performance                                    │
│     └─────┬──────┘    - ทดสอบ Integration                                    │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │ Production │  ← ใช้งานจริง (Live Environment)                          │
│     │    🟢      │    - ให้บริการ Users จริง                                 │
│     └─────┬──────┘    - ต้องมี Monitoring                                    │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │  Archived  │  ← เก็บถาวร (ไม่ใช้งานแล้ว แต่ยังเข้าถึงได้)               │
│     │    ⚫      │    - เก็บไว้ Reference                                    │
│     └────────────┘    - สามารถ Rollback ได้                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**รายละเอียดแต่ละ Stage:**

| Stage | สัญลักษณ์ | คำอธิบาย | ใครใช้งาน | Use Case |
|-------|----------|----------|----------|----------|
| **None** | ⚪ | สถานะเริ่มต้น | Data Scientists | เพิ่งฝึกเสร็จ กำลังประเมินผล |
| **Staging** | 🟡 | ทดสอบก่อน Production | QA Team, ML Engineers | ทดสอบกับข้อมูลจริงในสภาพแวดล้อมทดสอบ |
| **Production** | 🟢 | ใช้งานจริง | End Users | ให้บริการผ่าน API |
| **Archived** | ⚫ | เก็บถาวร | ทุกคน (อ่านอย่างเดียว) | เก็บโมเดลเก่าไว้ Reference |

### 6.2 Model Aliases (MLflow 2.x - แนะนำ)

ใน MLflow 2.x แนะนำให้ใช้ **Model Aliases** แทน Stages เดิม เนื่องจากมีความยืดหยุ่นมากกว่า

**ข้อดีของ Aliases:**
- กำหนดชื่อได้เอง (ไม่จำกัดแค่ 4 ตัวเลือก)
- สามารถมีหลาย Alias ได้ (เช่น "champion" และ "latest")
- เปลี่ยนแปลงได้ง่าย

**Aliases ที่นิยมใช้:**

| Alias | คำอธิบาย | Use Case |
|-------|----------|----------|
| **champion** | Model ที่ดีที่สุดในปัจจุบัน | ใช้ใน Production |
| **challenger** | Model ที่กำลังทดสอบเพื่อแทน champion | A/B Testing |
| **baseline** | Model แรกสำหรับเปรียบเทียบ | Benchmark |
| **staging** | Model ที่กำลัง QA | Pre-production testing |
| **latest** | Model ล่าสุดที่ฝึก | Development |

**ตัวอย่างการใช้งาน:**

```python
# กำหนด Alias
client.set_registered_model_alias(
    name="fraud-detector",
    alias="champion",
    version="5"
)

# โหลด Model จาก Alias
model = mlflow.pyfunc.load_model("models:/fraud-detector@champion")
```

### 6.3 เปรียบเทียบ Stages vs Aliases

| คุณสมบัติ | Stages (Legacy) | Aliases (แนะนำ) |
|-----------|-----------------|-----------------|
| จำนวนตัวเลือก | 4 ตัว (None, Staging, Production, Archived) | ไม่จำกัด |
| ความยืดหยุ่น | ต่ำ | สูง |
| การเปลี่ยนชื่อ | ไม่ได้ | ได้ |
| Multiple Labels | ไม่ได้ (1 Version = 1 Stage) | ได้ (1 Version = หลาย Aliases) |
| MLflow Version | ทุก Version | 2.x ขึ้นไป |

---

## 7. ความสัมพันธ์ระหว่าง Components ใน MLflow

### 7.1 ภาพรวม

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MLflow Components Relationship                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    🧪 MLflow Tracking                                │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  📁 Experiment: "iris-classification"                        │    │    │
│  │  │  ├── 🏃 Run 1: random-forest-v1                              │    │    │
│  │  │  │   ├── Parameters: {n_estimators: 50}                     │    │    │
│  │  │  │   ├── Metrics: {accuracy: 0.92}                          │    │    │
│  │  │  │   └── Artifacts: [model.pkl]                             │    │    │
│  │  │  │                           │                               │    │    │
│  │  │  │                           │  register_model()             │    │    │
│  │  │  │                           ▼                               │    │    │
│  │  │  ├── 🏃 Run 2: random-forest-v2  ────────────────────────┐   │    │    │
│  │  │  │   └── Metrics: {accuracy: 0.95}                       │   │    │    │
│  │  │  │                           │                            │   │    │    │
│  │  │  │                           ▼                            │   │    │    │
│  │  │  └── 🏃 Run 3: gradient-boosting  ───────────────────────┐│  │    │    │
│  │  │      └── Metrics: {accuracy: 0.97}                       ││  │    │    │
│  │  └──────────────────────────────────────────────────────────┘│  │    │    │
│  └─────────────────────────────────────────────────────────────────┘    │    │
│                                 │                                    │    │    │
│                                 ▼                                    ▼    │    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    🏛️ MLflow Model Registry                         │    │
│  │  ├── Version 1 ← from Run 1 (Alias: baseline)                       │    │
│  │  ├── Version 2 ← from Run 2 (Alias: staging)                        │    │
│  │  └── Version 3 ← from Run 3 (Alias: champion)                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 การไหลของข้อมูล

1. **Experiment** → เป็น Container สำหรับจัดกลุ่ม Runs
2. **Run** → บันทึกการทดลองหนึ่งครั้ง (Parameters, Metrics, Artifacts)
3. **Model Artifact** → ไฟล์ Model ที่บันทึกไว้ใน Run
4. **Registered Model** → Model ที่ลงทะเบียนใน Registry
5. **Model Version** → เวอร์ชันของ Registered Model ที่เชื่อมกับ Run

### 7.3 ความสัมพันธ์แบบละเอียด

| Component A | ความสัมพันธ์ | Component B |
|-------------|-------------|-------------|
| Experiment | มีหลาย | Runs |
| Run | มีหนึ่ง | Model Artifact |
| Run | ลงทะเบียนเป็น | Model Version |
| Registered Model | มีหลาย | Model Versions |
| Model Version | เชื่อมกับ | Run (ผ่าน Run ID) |
| Model Version | มีได้หลาย | Aliases |

---

## 8. Best Practices

### 8.1 การตั้งชื่อ Model

**หลักการ:** ใช้ชื่อที่สื่อความหมาย มีโครงสร้าง และหาได้ง่าย

| ✅ ชื่อที่ดี | ❌ ชื่อที่ควรหลีกเลี่ยง | เหตุผล |
|-------------|------------------------|--------|
| `fraud-detection-xgboost` | `model1` | ไม่สื่อความหมาย |
| `customer-churn-predictor` | `test` | ไม่ชัดเจน |
| `image-classifier-resnet50` | `my_model` | ไม่เฉพาะเจาะจง |
| `nlp-sentiment-bert` | `final_model_v2_REAL` | สับสน |
| `product-recommender-als` | `model_good` | ไม่บอกรายละเอียด |

**รูปแบบแนะนำ:**
```
<use-case>-<algorithm>[-<variant>]

ตัวอย่าง:
- fraud-detection-xgboost
- fraud-detection-xgboost-balanced
- customer-churn-lgbm-v2
```

### 8.2 การใช้ Tags

**Tags สำหรับ Registered Model:**

| Tag Key | ตัวอย่าง Values | วัตถุประสงค์ |
|---------|-----------------|-------------|
| `task` | classification, regression, clustering | ประเภทงาน |
| `framework` | sklearn, pytorch, tensorflow | Framework ที่ใช้ |
| `team` | data-science, ml-engineering | ทีมที่รับผิดชอบ |
| `domain` | fraud, recommendation, nlp | โดเมนธุรกิจ |
| `owner` | john.doe@company.com | เจ้าของ Model |

**Tags สำหรับ Model Version:**

| Tag Key | ตัวอย่าง Values | วัตถุประสงค์ |
|---------|-----------------|-------------|
| `deployment_status` | production, staging, retired | สถานะการ Deploy |
| `approved_by` | ML-Team-Lead, Data-Science-Manager | ผู้อนุมัติ |
| `approval_date` | 2024-01-25 | วันที่อนุมัติ |
| `experiment_type` | baseline, hyperparameter-tuning | ประเภทการทดลอง |
| `data_version` | v2.3, 2024-01-15 | เวอร์ชันข้อมูลที่ใช้ |

### 8.3 การใช้ Aliases

**Aliases ที่แนะนำ:**

| Alias | Use Case | ควรมีกี่ Version |
|-------|----------|-----------------|
| `champion` | Model ที่ใช้ใน Production | 1 |
| `challenger` | Model ที่กำลัง A/B Test | 0-1 |
| `baseline` | Model แรกสำหรับเปรียบเทียบ | 1 |
| `staging` | Model ที่กำลัง QA | 0-1 |
| `shadow` | Model ที่รันคู่กับ champion แต่ไม่ส่งผลลัพธ์ | 0-1 |

### 8.4 Workflow แนะนำ

```
┌─────────────────────────────────────────────────────────────────┐
│                    Model Promotion Workflow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. Train Model                                                │
│      └── บันทึกด้วย MLflow Tracking                              │
│                                                                  │
│   2. Register Model                                             │
│      └── ลงทะเบียนใน Registry (ยังไม่มี Alias)                   │
│                                                                  │
│   3. Internal Testing                                           │
│      └── ทดสอบโดย Data Scientists                                │
│                                                                  │
│   4. Assign "staging" Alias                                     │
│      └── ส่งให้ QA Team ทดสอบ                                    │
│                                                                  │
│   5. QA Testing                                                 │
│      ├── Performance Testing                                    │
│      ├── Integration Testing                                    │
│      └── Load Testing                                           │
│                                                                  │
│   6. Approval                                                   │
│      └── ได้รับการอนุมัติจาก ML Team Lead                        │
│                                                                  │
│   7. Assign "champion" Alias                                    │
│      └── ย้ายจาก staging เป็น champion                          │
│                                                                  │
│   8. Production Deployment                                      │
│      └── Deploy และเริ่มให้บริการ                                 │
│                                                                  │
│   9. Monitoring                                                 │
│      └── ติดตาม Performance ใน Production                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.5 ข้อควรระวัง

| ⚠️ ข้อควรระวัง | 💡 คำแนะนำ |
|----------------|-----------|
| อย่าลบ Model Version ที่เคยใช้ Production | ใช้ Archive หรือลบ Alias แทน |
| อย่าลืมบันทึก Description และ Tags | ทำให้หาและเข้าใจ Model ได้ง่าย |
| อย่ามี Model Version มากเกินไป | ลบหรือ Archive เวอร์ชันที่ไม่ใช้ |
| อย่าใช้ชื่อ Model ที่ซ้ำซ้อน | ใช้ Naming Convention ที่ชัดเจน |
| อย่าลืมทดสอบก่อน Promote | ใช้ staging alias สำหรับ QA |

---

## 9. คำอธิบายแบบฝึกหัด

### 9.1 ภาพรวมแบบฝึกหัด

แบบฝึกหัดนี้ออกแบบมาเพื่อให้นักศึกษาได้ลงมือปฏิบัติจริงกับ MLflow Model Registry ครอบคลุมตั้งแต่พื้นฐานจนถึงการใช้งานขั้นสูง

**วัตถุประสงค์การเรียนรู้:**
1. เข้าใจแนวคิดและประโยชน์ของ Model Registry
2. สามารถลงทะเบียน Model เข้า Registry ได้
3. จัดการ Model Versions และ Aliases ได้
4. โหลด Model จาก Registry มาใช้งานได้
5. เข้าใจ Model Lifecycle Management

### 9.2 โครงสร้างแบบฝึกหัด

แบบฝึกหัดแบ่งเป็น 11 ส่วน:

| ส่วน | หัวข้อ | เนื้อหาสำคัญ |
|------|--------|-------------|
| 1 | การเชื่อมต่อ MLflow Server | ตั้งค่า Tracking URI, สร้าง MLflow Client |
| 2 | การสร้างและลงทะเบียน Model (Scikit-learn) | 2 วิธีลงทะเบียน: พร้อม Train และ ภายหลัง |
| 3 | การดูข้อมูล Registered Models | ค้นหาและดูรายละเอียด Models |
| 4 | การจัดการ Model Stages (Aliases) | กำหนด Alias ให้ Model Versions |
| 5 | การโหลด Model จาก Registry | โหลด Model จาก ARTIFACTS_BASE |
| 6 | การลงทะเบียน PyTorch Model | ทำงานกับ Deep Learning Model |
| 7 | การโหลด PyTorch Model | โหลด PyTorch Model จาก Registry |
| 8 | การค้นหา Models และ Versions | ค้นหาด้วย Filter String |
| 9 | การลบ Model และ Version | Destructive Operations |
| 10 | Best Practices | แนวปฏิบัติที่ดี |
| 11 | การดู Registry ผ่าน UI | ใช้งาน MLflow Web UI |

### 9.3 รายละเอียดแต่ละส่วน

#### ส่วนที่ 1: การเชื่อมต่อ MLflow Server

**ทฤษฎี:**
ก่อนใช้งาน Model Registry ต้องเชื่อมต่อกับ MLflow Server ที่รัน Registry โดยใช้:

```python
import mlflow
from mlflow.tracking import MlflowClient

# เชื่อมต่อ Server
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# สร้าง Client สำหรับจัดการ Registry
client = MlflowClient()
```

**ฟังก์ชันสำคัญ:**
- `mlflow.set_tracking_uri(uri)` - กำหนด URL ของ MLflow Server
- `MlflowClient()` - สร้าง Client สำหรับจัดการ Registry โดยตรง

---

#### ส่วนที่ 2: การสร้างและลงทะเบียน Model (Scikit-learn)

**ทฤษฎี:**
การลงทะเบียน Model มี 2 วิธี:

**วิธีที่ 1: ลงทะเบียนพร้อม Train**
```python
mlflow.sklearn.log_model(
    sk_model=model,
    artifact_path="model",
    registered_model_name="my-model"  # ← ลงทะเบียนทันที
)
```

**วิธีที่ 2: ลงทะเบียนภายหลัง**
```python
# บันทึก Model ก่อน
mlflow.sklearn.log_model(sk_model=model, artifact_path="model")

# ลงทะเบียนภายหลัง
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="my-model"
)
```

**เมื่อไหร่ใช้วิธีไหน:**

| วิธี | Use Case |
|------|----------|
| วิธีที่ 1 | ต้องการลงทะเบียนทันทีหลังฝึก |
| วิธีที่ 2 | ต้องการเลือก Model ที่ดีที่สุดก่อนลงทะเบียน |

**การเพิ่ม Description และ Tags:**
```python
# อัพเดท Description
client.update_registered_model(
    name="my-model",
    description="คำอธิบาย Model"
)

# เพิ่ม Tag ให้ Model
client.set_registered_model_tag("my-model", "task", "classification")

# เพิ่ม Tag ให้ Version
client.set_model_version_tag("my-model", "1", "status", "baseline")
```

---

#### ส่วนที่ 3: การดูข้อมูล Registered Models

**ทฤษฎี:**
MLflow Client มีฟังก์ชันสำหรับดูข้อมูล Models และ Versions:

```python
# ดู Models ทั้งหมด
for rm in client.search_registered_models():
    print(f"Model: {rm.name}")

# ดู Versions ของ Model
versions = client.search_model_versions(f"name='my-model'")
for v in versions:
    print(f"Version {v.version}: {v.current_stage}")

# ดู Model เฉพาะ
model = client.get_registered_model("my-model")

# ดู Version เฉพาะ
version = client.get_model_version("my-model", "1")
```

---

#### ส่วนที่ 4: การจัดการ Model Aliases

**ทฤษฎี:**
Aliases เป็นวิธีกำหนดชื่อให้ Model Version เพื่อง่ายต่อการอ้างอิง

```python
# กำหนด Alias
client.set_registered_model_alias(
    name="my-model",
    alias="champion",
    version="3"
)

# ดู Version จาก Alias
champion = client.get_model_version_by_alias("my-model", "champion")

# ลบ Alias
client.delete_registered_model_alias("my-model", "champion")
```

**ข้อดีของ Aliases:**
- สามารถโหลด Model ด้วยชื่อที่สื่อความหมาย
- เปลี่ยน Version ได้โดยไม่ต้องแก้โค้ด
- รองรับ Workflow เช่น Champion/Challenger

---

#### ส่วนที่ 5: การโหลด Model จาก Registry

**ทฤษฎี:**
มีหลายวิธีในการโหลด Model:

**วิธีที่ 1: โหลดจาก Model URI**
```python
# โหลดจาก Version
model = mlflow.sklearn.load_model("models:/my-model/3")

# โหลดจาก Alias
model = mlflow.sklearn.load_model("models:/my-model@champion")
```

**วิธีที่ 2: โหลดจาก ARTIFACTS_BASE (เร็วที่สุด)**
```python
# สำหรับ Server เดียวกัน
model_path = find_model_path_by_flavor(ARTIFACTS_BASE, experiment_id, "sklearn")
model = mlflow.sklearn.load_model(model_path)
```

**โครงสร้างไฟล์ใน ARTIFACTS_BASE:**
```
mlartifacts/
└── <experiment_id>/
    ├── <run_id>/
    │   └── artifacts/           # Artifacts ทั่วไป
    └── models/                  # Models ถูกเก็บแยก
        └── m-<model_id>/        
            └── artifacts/
                ├── MLmodel
                ├── model.pkl
                └── ...
```

---

#### ส่วนที่ 6-7: การลงทะเบียนและโหลด PyTorch Model

**ทฤษฎี:**
PyTorch Model ใช้วิธีเดียวกับ Scikit-learn แต่ใช้ `mlflow.pytorch`:

```python
# บันทึกและลงทะเบียน
mlflow.pytorch.log_model(
    pytorch_model=model,
    name="model",
    signature=signature,
    registered_model_name="my-pytorch-model"
)

# โหลด
loaded_model = mlflow.pytorch.load_model("models:/my-pytorch-model@champion")
```

**ข้อควรระวัง:**
- ต้องสร้าง Signature ที่ถูกต้อง
- Input ต้องเป็น float32 สำหรับ PyTorch
- ต้องเรียก `model.eval()` ก่อนทำนาย

---

#### ส่วนที่ 8: การค้นหา Models และ Versions

**ทฤษฎี:**
MLflow รองรับ Filter String สำหรับค้นหา:

```python
# ค้นหา Models ที่มี Tag
models = client.search_registered_models(
    filter_string="tags.task = 'classification'"
)

# ค้นหา Versions
versions = client.search_model_versions(
    filter_string="name = 'my-model'"
)

# ค้นหาจาก Run ID
versions = client.search_model_versions(
    filter_string=f"run_id = '{run_id}'"
)
```

---

#### ส่วนที่ 9: การลบ Model และ Version

**ทฤษฎี:**
การลบเป็น Destructive Operation ต้องระวัง:

```python
# ลบ Version
client.delete_model_version(name="my-model", version="1")

# ลบ Alias ก่อนลบ Model
client.delete_registered_model_alias("my-model", "champion")

# ลบ Model ทั้งหมด
client.delete_registered_model(name="my-model")
```

**⚠️ ข้อควรระวัง:**
- การลบไม่สามารถยกเลิกได้
- ต้องลบ Aliases และ Versions ก่อนลบ Model
- แนะนำให้ Archive แทนการลบ

---

### 9.4 สรุปฟังก์ชันสำคัญ

| หมวดหมู่ | ฟังก์ชัน | วัตถุประสงค์ |
|----------|----------|-------------|
| **ลงทะเบียน** | `mlflow.sklearn.log_model(..., registered_model_name)` | บันทึกและลงทะเบียนพร้อมกัน |
| **ลงทะเบียน** | `mlflow.register_model(model_uri, name)` | ลงทะเบียน Model ที่มีอยู่ |
| **โหลด** | `mlflow.sklearn.load_model(model_path)` | โหลด sklearn model |
| **โหลด** | `mlflow.pytorch.load_model(model_path)` | โหลด PyTorch model |
| **Alias** | `client.set_registered_model_alias(name, alias, version)` | กำหนด Alias |
| **Alias** | `client.get_model_version_by_alias(name, alias)` | ดู Version จาก Alias |
| **Metadata** | `client.update_registered_model(name, description)` | อัพเดท Description |
| **Tags** | `client.set_registered_model_tag(name, key, value)` | เพิ่ม Tag ให้ Model |
| **Tags** | `client.set_model_version_tag(name, version, key, value)` | เพิ่ม Tag ให้ Version |
| **ค้นหา** | `client.search_registered_models(filter_string)` | ค้นหา Models |
| **ค้นหา** | `client.search_model_versions(filter_string)` | ค้นหา Versions |
| **ดูข้อมูล** | `client.get_registered_model(name)` | ดู Model |
| **ดูข้อมูล** | `client.get_model_version(name, version)` | ดู Version |

---

## 10. แหล่งข้อมูลเพิ่มเติม

### 10.1 เอกสารอ้างอิง

- [MLflow Model Registry Documentation](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Model Registry Concepts](https://mlflow.org/docs/latest/concepts.html#model-registry)
- [MLflow Python API - Model Registry](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.register_model)
- [Model Aliases and Tags](https://mlflow.org/docs/latest/model-registry.html#model-aliases)

### 10.2 บทความที่แนะนำ

- [Best Practices for Model Registry](https://mlflow.org/docs/latest/model-registry.html#best-practices)
- [Model Lifecycle Management](https://www.databricks.com/blog/2020/07/08/model-registry-best-practices.html)
- [MLOps Maturity Model](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

### 10.3 วิดีโอและ Tutorials

- [MLflow Model Registry Tutorial (YouTube)](https://www.youtube.com/results?search_query=mlflow+model+registry+tutorial)
- [Databricks Model Registry Course](https://www.databricks.com/learn/training)

---

## 📝 หมายเหตุสำหรับผู้สอน

### การเตรียมตัวก่อนสอน

1. **ตรวจสอบ MLflow Server:** ให้แน่ใจว่า Server รันที่ `http://127.0.0.1:5000`
2. **ตรวจสอบ Dependencies:** scikit-learn, pytorch, mlflow
3. **เตรียม Dataset:** Iris dataset (มาพร้อมกับ sklearn)

### คำแนะนำในการสอน

1. เริ่มจากทฤษฎีใน README นี้ก่อน (ประมาณ 30 นาที)
2. ให้นักศึกษาทำแบบฝึกหัดทีละส่วน
3. หยุดอธิบายเพิ่มเติมหลังจบแต่ละส่วน
4. เน้นให้นักศึกษาดู MLflow UI ควบคู่กับการรันโค้ด

### การประเมินผล

- ความเข้าใจแนวคิด Model Registry (30%)
- ความสามารถในการลงทะเบียนและโหลด Model (40%)
- การใช้ Aliases และ Tags อย่างเหมาะสม (20%)
- Best Practices และการนำไปประยุกต์ใช้ (10%)

---

*เอกสารนี้จัดทำขึ้นสำหรับรายวิชา MLOps*  
**MLflow Server URL:** http://127.0.0.1:5000