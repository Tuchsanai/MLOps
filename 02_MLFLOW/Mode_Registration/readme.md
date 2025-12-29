# 🧪 Lab: การลงทะเบียนโมเดล (Model Registration) ด้วย MLflow

## 📋 ภาพรวม

ใน Lab นี้ นักศึกษาจะได้เรียนรู้วิธีการจัดการโมเดล Machine Learning อย่างเป็นระบบด้วย **MLflow Model Registry** ซึ่งเป็นเครื่องมือสำคัญในการทำ MLOps

---

## 🎯 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. เข้าใจแนวคิดของ Model Registry และความสำคัญใน MLOps
2. ลงทะเบียนโมเดลเข้าสู่ MLflow Model Registry
3. จัดการเวอร์ชันของโมเดล (Model Versioning)
4. เปลี่ยนสถานะของโมเดล (Model Stage Transitions)
5. โหลดโมเดลจาก Registry มาใช้งาน

---

## 📚 ความรู้พื้นฐานที่ต้องมี

- Python เบื้องต้น
- การใช้งาน Command Line / Terminal
- ความเข้าใจเรื่อง Virtual Environment
- ผ่าน Lab การติดตั้งและใช้งาน MLflow เบื้องต้นมาแล้ว

---

## 📦 ข้อกำหนดเบื้องต้น (Prerequisites)

| รายการ | รายละเอียด |
|--------|------------|
| Python | เวอร์ชัน 3.9 - 3.12 |
| pip | ตัวจัดการ Package ของ Python |
| ระบบปฏิบัติการ | Linux หรือ macOS |
| Port ที่ต้องใช้ | 8080 (สำหรับ MLflow Tracking Server และ UI) |

---

## 📚 ทฤษฎีพื้นฐาน

### 🔄 Machine Learning Lifecycle คืออะไร?

ก่อนที่เราจะเข้าใจ Model Registry เราต้องเข้าใจ **Machine Learning Lifecycle** ก่อน

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

**แต่ละขั้นตอนมีความสำคัญดังนี้:**

| ขั้นตอน | คำอธิบาย | ปัญหาที่พบบ่อย |
|---------|----------|---------------|
| Data Collection | รวบรวมข้อมูลจากแหล่งต่างๆ | ข้อมูลไม่สอดคล้องกัน, ขาดการติดตาม |
| Model Training | ฝึกโมเดลด้วย Algorithm ต่างๆ | ไม่รู้ว่าใช้ hyperparameters อะไร |
| Model Evaluation | ประเมินประสิทธิภาพโมเดล | เปรียบเทียบโมเดลยาก |
| Model Deployment | นำโมเดลไปใช้งานจริง | ไม่รู้ว่าโมเดลไหนใช้งานอยู่ |

---

### 🤔 ปัญหาที่เกิดขึ้นเมื่อไม่มี Model Registry

ลองนึกภาพสถานการณ์นี้:

```
📁 โฟลเดอร์โปรเจกต์ของคุณ (ไม่มี Model Registry)
├── model_v1.pkl
├── model_v2.pkl
├── model_v2_fixed.pkl
├── model_v2_fixed_final.pkl
├── model_v2_fixed_final_REAL.pkl      ← 😱 อันไหนดีที่สุด?
├── model_best.pkl
├── model_best_new.pkl
└── model_production_maybe.pkl          ← 😵 งง!
```

**ปัญหาที่พบบ่อย:**

| ปัญหา | ผลกระทบ |
|-------|---------|
| 🔍 **หาโมเดลไม่เจอ** | ไม่รู้ว่าโมเดลไหนดีที่สุด ต้องฝึกใหม่ |
| 📊 **ไม่รู้ Hyperparameters** | จำไม่ได้ว่าใช้ค่าอะไรฝึก |
| 🔄 **ไม่มี Version Control** | ไม่สามารถย้อนกลับไปใช้โมเดลเก่าได้ |
| 👥 **ทำงานเป็นทีมยาก** | ไม่รู้ว่าใครแก้ไขอะไร เมื่อไหร่ |
| 🚀 **Deploy ยาก** | ไม่มั่นใจว่าโมเดลไหนพร้อม Production |
| 📝 **ไม่มี Audit Trail** | ไม่สามารถตรวจสอบย้อนหลังได้ |

---

### 🏛️ Model Registry คืออะไร?

**Model Registry** คือระบบจัดการโมเดลแบบรวมศูนย์ (Centralized Model Management) ที่ช่วยแก้ปัญหาทั้งหมดข้างต้น

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
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  📦 Registered Model: "sales-predictor"                              │    │
│  │  ├── 📋 Description: โมเดลพยากรณ์ยอดขาย                               │    │
│  │  └── ... (versions)                                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 🎯 ประโยชน์ของ Model Registry

| ประโยชน์ | คำอธิบาย | ตัวอย่าง |
|----------|----------|----------|
| **🔢 Version Control** | ติดตามทุกเวอร์ชันของโมเดล | ย้อนกลับไปใช้ Version 2 ได้ทันที |
| **📊 Metadata Tracking** | เก็บข้อมูลที่เกี่ยวข้องทั้งหมด | Parameters, Metrics, Artifacts |
| **🚦 Stage Management** | จัดการสถานะการใช้งาน | Staging → Production |
| **👥 Collaboration** | ทำงานร่วมกันเป็นทีม | ทุกคนเห็นโมเดลเดียวกัน |
| **📝 Audit Trail** | ติดตามการเปลี่ยนแปลง | ใครเปลี่ยนอะไร เมื่อไหร่ |
| **🔗 Lineage** | เชื่อมโยงกับ Experiment | รู้ว่าโมเดลมาจาก Run ไหน |

---

### 🚦 Model Stages (สถานะของโมเดล)

MLflow Model Registry มี 4 สถานะหลัก:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Model Stage Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     ┌────────────┐                                                          │
│     │            │                                                          │
│     │    None    │  ← โมเดลเพิ่งลงทะเบียน ยังไม่กำหนดสถานะ                    │
│     │    ⚪      │                                                          │
│     └─────┬──────┘                                                          │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │            │                                                          │
│     │  Staging   │  ← กำลังทดสอบ (QA/Testing Environment)                    │
│     │    🟡      │    - ทดสอบ Performance                                    │
│     │            │    - ทดสอบ Integration                                    │
│     └─────┬──────┘    - ทดสอบ Edge Cases                                    │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │            │                                                          │
│     │ Production │  ← ใช้งานจริง (Live Environment)                          │
│     │    🟢      │    - ให้บริการ Users จริง                                 │
│     │            │    - ต้องมี Monitoring                                    │
│     └─────┬──────┘    - ต้องมี Alerting                                     │
│           │                                                                  │
│           ▼                                                                  │
│     ┌────────────┐                                                          │
│     │            │                                                          │
│     │  Archived  │  ← เก็บถาวร (ไม่ใช้งานแล้ว แต่ยังเข้าถึงได้)               │
│     │    ⚫      │    - เก็บไว้ Reference                                    │
│     │            │    - สามารถ Rollback ได้                                  │
│     └────────────┘                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**รายละเอียดแต่ละ Stage:**

| Stage | สัญลักษณ์ | คำอธิบาย | ใครใช้งาน | ตัวอย่าง Use Case |
|-------|----------|----------|----------|------------------|
| **None** | ⚪ | สถานะเริ่มต้น | Data Scientists | เพิ่งฝึกเสร็จ กำลังประเมินผล |
| **Staging** | 🟡 | ทดสอบก่อน Production | QA Team, ML Engineers | ทดสอบกับข้อมูลจริงในสภาพแวดล้อมทดสอบ |
| **Production** | 🟢 | ใช้งานจริง | End Users | ให้บริการผ่าน API |
| **Archived** | ⚫ | เก็บถาวร | ทุกคน (อ่านอย่างเดียว) | เก็บโมเดลเก่าไว้ Reference |

---

### 🔗 ความสัมพันธ์ระหว่าง Components ใน MLflow

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
│  │  │  │   ├── Parameters: {n_estimators: 50, max_depth: 5}       │    │    │
│  │  │  │   ├── Metrics: {accuracy: 0.92, f1: 0.91}                │    │    │
│  │  │  │   └── Artifacts: [model.pkl, confusion_matrix.png]       │    │    │
│  │  │  │                           │                               │    │    │
│  │  │  │                           │  register_model()             │    │    │
│  │  │  │                           ▼                               │    │    │
│  │  │  ├── 🏃 Run 2: random-forest-v2  ─────────────────────────┐  │    │    │
│  │  │  │   ├── Parameters: {n_estimators: 100, max_depth: 10}   │  │    │    │
│  │  │  │   └── Metrics: {accuracy: 0.95, f1: 0.94}              │  │    │    │
│  │  │  │                           │                             │  │    │    │
│  │  │  │                           ▼                             │  │    │    │
│  │  │  └── 🏃 Run 3: gradient-boosting  ───────────────────────┐│  │    │    │
│  │  │      ├── Parameters: {n_estimators: 100, lr: 0.1}        ││  │    │    │
│  │  │      └── Metrics: {accuracy: 0.97, f1: 0.96}             ││  │    │    │
│  │  │                           │                               ││  │    │    │
│  │  └───────────────────────────│───────────────────────────────┘│  │    │    │
│  └──────────────────────────────│────────────────────────────────┘  │    │    │
│                                 │                                    │    │    │
│                                 ▼                                    ▼    │    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    🏛️ MLflow Model Registry                         │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  📦 Registered Model: "iris-classifier"                      │    │    │
│  │  │  ├── Version 1 ← from Run 1 (Stage: Archived)               │    │    │
│  │  │  ├── Version 2 ← from Run 2 (Stage: Staging)                │    │    │
│  │  │  └── Version 3 ← from Run 3 (Stage: Production)             │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                 │                                            │
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    🚀 MLflow Model Serving                          │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  🌐 REST API Endpoint                                        │    │    │
│  │  │  └── POST /invocations                                       │    │    │
│  │  │      └── Uses: models:/iris-classifier@production            │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 📋 Model URI Formats

เมื่อต้องการโหลดโมเดลจาก Registry สามารถใช้ URI ได้หลายรูปแบบ:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Model URI Formats                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📌 โหลดด้วย Version Number                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  models:/<model_name>/<version>                                      │    │
│  │                                                                      │    │
│  │  ตัวอย่าง:                                                            │    │
│  │  • models:/iris-classifier/1     → โหลด Version 1                    │    │
│  │  • models:/iris-classifier/3     → โหลด Version 3                    │    │
│  │  • models:/sales-predictor/5     → โหลด Version 5                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  📌 โหลดด้วย Stage (แนะนำ ⭐)                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  models:/<model_name>@<stage>                                        │    │
│  │                                                                      │    │
│  │  ตัวอย่าง:                                                            │    │
│  │  • models:/iris-classifier@production  → โหลดโมเดลที่ใช้งานจริง       │    │
│  │  • models:/iris-classifier@staging     → โหลดโมเดลที่กำลังทดสอบ       │    │
│  │  • models:/sales-predictor@production  → โหลดโมเดล Production        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  📌 โหลด Version ล่าสุด                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  models:/<model_name>/latest                                         │    │
│  │                                                                      │    │
│  │  ตัวอย่าง:                                                            │    │
│  │  • models:/iris-classifier/latest    → โหลด Version ล่าสุด           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  💡 ทำไมควรใช้ @stage?                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ✅ ไม่ต้องแก้ Code เมื่อมี Version ใหม่                               │    │
│  │  ✅ แค่เปลี่ยน Stage ของ Version ที่ต้องการ                           │    │
│  │  ✅ Code ที่ใช้ @production จะโหลดโมเดลใหม่อัตโนมัติ                    │    │
│  │  ✅ ลด Human Error จากการใส่ Version ผิด                             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ Lab Pipeline Overview

### ภาพรวมของ Lab ทั้งหมด

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         🗺️ Lab Pipeline Overview                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🛠️ SETUP: เตรียมสภาพแวดล้อม                                         │    │
│  │  ├── สร้างโฟลเดอร์ mlflowserver-lab                                  │    │
│  │  ├── สร้าง Virtual Environment                                       │    │
│  │  ├── ติดตั้ง Packages                                                │    │
│  │  └── เปิด MLflow Server                                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 1: ฝึกและลงทะเบียนโมเดล                                       │    │
│  │  ├── 📊 เตรียมข้อมูล Iris Dataset                                    │    │
│  │  ├── 🎯 ฝึก RandomForest Model                                       │    │
│  │  ├── 📈 บันทึก Parameters & Metrics                                  │    │
│  │  └── 📦 ลงทะเบียนโมเดลเป็น Version 1                                  │    │
│  │                                                                      │    │
│  │  Output: iris-classifier (Version 1)                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 2: สร้างหลาย Versions                                         │    │
│  │  ├── 🔄 ปรับ Hyperparameters → Version 2                             │    │
│  │  ├── 🔄 เปลี่ยน Algorithm → Version 3                                │    │
│  │  └── 📋 ดูรายการ Versions ทั้งหมด                                     │    │
│  │                                                                      │    │
│  │  Output: iris-classifier (Version 1, 2, 3)                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 3: จัดการสถานะโมเดล                                           │    │
│  │  ├── ⚫ Version 1 → Archived                                         │    │
│  │  ├── 🟡 Version 2 → Staging                                          │    │
│  │  ├── 🟢 Version 3 → Production                                       │    │
│  │  └── 📝 เพิ่ม Description                                            │    │
│  │                                                                      │    │
│  │  Output: โมเดลพร้อม Stages และ Descriptions                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 4: โหลดโมเดลจาก Registry                                      │    │
│  │  ├── 📥 โหลดด้วย Version Number                                      │    │
│  │  ├── 📥 โหลดด้วย Stage (@production, @staging)                       │    │
│  │  ├── 📥 โหลดเป็น PyFunc Model                                        │    │
│  │  └── 🔮 ทดสอบ Prediction                                             │    │
│  │                                                                      │    │
│  │  Output: เข้าใจวิธีโหลดโมเดลหลายรูปแบบ                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 5: สร้าง REST API                                             │    │
│  │  ├── 🌐 สร้าง Flask Application                                      │    │
│  │  ├── 🔌 Endpoints: /health, /predict, /model-info                    │    │
│  │  └── 🧪 ทดสอบด้วย curl                                               │    │
│  │                                                                      │    │
│  │  Output: REST API พร้อมใช้งาน                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                              │                                               │
│                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  🔬 LAB 6: Automated Pipeline (Advanced)                             │    │
│  │  ├── 🔄 Auto-compare Staging vs Production                           │    │
│  │  ├── 🚀 Auto-promote ถ้า Staging ดีกว่า                               │    │
│  │  └── 📊 Generate Comparison Report                                   │    │
│  │                                                                      │    │
│  │  Output: Automated Model Promotion Pipeline                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Flow Diagram                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐                                                          │
│   │              │                                                          │
│   │  Iris Data   │                                                          │
│   │   Dataset    │                                                          │
│   │              │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │              │    │              │    │              │                  │
│   │    Train     │───▶│   Evaluate   │───▶│   Register   │                  │
│   │    Model     │    │    Model     │    │    Model     │                  │
│   │              │    │              │    │              │                  │
│   └──────────────┘    └──────────────┘    └──────┬───────┘                  │
│                                                   │                          │
│          ┌────────────────────────────────────────┘                          │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────────────────────────────────────────────────┐              │
│   │                                                          │              │
│   │                   MLflow Model Registry                  │              │
│   │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │              │
│   │  │ Version 1  │  │ Version 2  │  │ Version 3  │         │              │
│   │  │  Archived  │  │  Staging   │  │ Production │         │              │
│   │  └────────────┘  └─────┬──────┘  └─────┬──────┘         │              │
│   │                        │               │                 │              │
│   └────────────────────────│───────────────│─────────────────┘              │
│                            │               │                                 │
│          ┌─────────────────┘               └─────────────────┐              │
│          │                                                   │              │
│          ▼                                                   ▼              │
│   ┌──────────────┐                                    ┌──────────────┐      │
│   │              │                                    │              │      │
│   │   Testing    │                                    │  Production  │      │
│   │ Environment  │                                    │     API      │      │
│   │              │                                    │              │      │
│   └──────────────┘                                    └──────┬───────┘      │
│                                                              │              │
│                                                              ▼              │
│                                                       ┌──────────────┐      │
│                                                       │              │      │
│                                                       │    Users     │      │
│                                                       │              │      │
│                                                       └──────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ การเตรียมสภาพแวดล้อม

### ขั้นตอนที่ 1: สร้างโฟลเดอร์สำหรับ Lab

```bash
# สร้างโฟลเดอร์สำหรับเก็บไฟล์ Lab
mkdir -p mlflowserver-lab

# เข้าไปในโฟลเดอร์
cd mlflowserver-lab
```

---

### ขั้นตอนที่ 2: สร้าง Virtual Environment

> 💡 **ทำไมต้องใช้ Virtual Environment?**
> 
> Virtual Environment ช่วยแยก Package ของแต่ละโปรเจกต์ออกจากกัน ป้องกันปัญหา Package Version ขัดแย้งกัน

```bash
# 2.1 สร้าง Virtual Environment ชื่อ .venv
python -m venv .venv

# 2.2 เปิดใช้งาน Virtual Environment
source .venv/bin/activate

# 2.3 อัพเดท pip ให้เป็นเวอร์ชันล่าสุด
python -m pip install --upgrade pip
```

✅ **ตรวจสอบ:** เมื่อเปิดใช้งานสำเร็จ จะเห็น `(.venv)` นำหน้า prompt

---

### ขั้นตอนที่ 3: ติดตั้ง Package ที่จำเป็น

```bash
pip install mlflow[extras] scikit-learn pandas numpy
```

**รายละเอียด Package:**

| Package | หน้าที่ |
|---------|--------|
| `mlflow[extras]` | MLflow เวอร์ชันสมบูรณ์ รวม Model Serving, SQL Storage และ Dependencies ทั้งหมด |
| `scikit-learn` | Library สำหรับ Machine Learning |
| `pandas` | จัดการข้อมูลแบบ DataFrame |
| `numpy` | คำนวณทางคณิตศาสตร์ |

✅ **ตรวจสอบ:** รันคำสั่งนี้เพื่อยืนยันการติดตั้ง:

```bash
python -c "import mlflow; print('MLflow version:', mlflow.__version__)"
```

---

### ขั้นตอนที่ 4: เปิดใช้งาน MLflow Tracking Server

> ⚠️ **สำคัญ:** ให้นักศึกษา **เลือกทำเพียงแบบเดียว** (แบบที่ 1 หรือ แบบที่ 2) ไม่ต้องทำทั้ง 2 แบบ

| แบบ | ข้อดี | ข้อเสีย | เหมาะสำหรับ |
|-----|-------|---------|-------------|
| แบบที่ 1: In-Memory | เริ่มต้นเร็ว ไม่ต้องตั้งค่า | ข้อมูลหายเมื่อปิด Server | ทดลองใช้งานเร็วๆ |
| แบบที่ 2: Persistent | ข้อมูลไม่หาย | ต้องสร้างโฟลเดอร์เพิ่ม | ใช้งานจริง ⭐ |

---

#### 📌 แบบที่ 1: In-Memory (สำหรับทดลองใช้งานเร็ว)

```bash
mlflow server --host 127.0.0.1 --port 8080
```

**ข้อดี:** เริ่มต้นได้เร็ว ไม่ต้องตั้งค่าอะไรเพิ่ม  
**ข้อเสีย:** ข้อมูลหายเมื่อปิด Server

**ผลลัพธ์ที่คาดหวัง:**

```
INFO:     Started server process [28550]
INFO:     Application startup complete.
Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

---

#### 📌 แบบที่ 2: Persistent Storage (แนะนำสำหรับใช้งานจริง) ⭐

```bash
# 4.1 สร้างโฟลเดอร์เก็บข้อมูล
mkdir -p mlruns_db mlartifacts

# 4.2 เปิด Server พร้อม SQLite Backend
mlflow server \
  --host 127.0.0.1 --port 8080 \
  --backend-store-uri sqlite:///mlruns_db/mlflow.db \
  --artifacts-destination ./mlartifacts \
  --serve-artifacts
```

**🗂️ โครงสร้างไฟล์หลังจากสร้าง:**

```
mlflowserver-lab/
├── mlruns_db/
│   └── mlflow.db          # ฐานข้อมูล SQLite เก็บ Experiment และ Run Metadata
├── mlartifacts/           # โฟลเดอร์เก็บ Model Files และ Artifacts
└── .venv/                 # Virtual Environment
```

> 💡 **หมายเหตุ:** เปิด Terminal นี้ทิ้งไว้ แล้วทำงานใน **Terminal ใหม่**

---

### ขั้นตอนที่ 5: ตรวจสอบการทำงาน

เปิด Browser แล้วไปที่: `http://127.0.0.1:8080`

✅ **ผลลัพธ์ที่คาดหวัง:** เห็นหน้า MLflow UI

---

## 🔬 แบบฝึกหัดที่ 1: การฝึกและลงทะเบียนโมเดล

### 🎯 เป้าหมาย

- ฝึกโมเดล RandomForest
- บันทึก Parameters และ Metrics
- ลงทะเบียนโมเดลเข้า Model Registry

> ⚠️ **สำคัญ:** เปิด **Terminal ใหม่** และอย่าลืม activate virtual environment ก่อน!

```bash
cd mlflowserver-lab
source .venv/bin/activate
```

### สร้างไฟล์ `train_and_register.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 1 - การฝึกและลงทะเบียนโมเดล
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

# ==========================================
# ขั้นตอนที่ 1: ตั้งค่า MLflow
# ==========================================

# กำหนด Tracking URI (ที่อยู่ของ MLflow Server)
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# สร้างหรือเลือก Experiment
mlflow.set_experiment("model-registration-lab")

print("✅ ตั้งค่า MLflow เรียบร้อย")

# ==========================================
# ขั้นตอนที่ 2: เตรียมข้อมูล
# ==========================================

# โหลด Iris Dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

# แบ่งข้อมูล Train/Test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42
)

print(f"✅ เตรียมข้อมูลเรียบร้อย")
print(f"   - Training samples: {len(X_train)}")
print(f"   - Test samples: {len(X_test)}")

# ==========================================
# ขั้นตอนที่ 3: ฝึกโมเดลและลงทะเบียน
# ==========================================

# ชื่อโมเดลที่จะลงทะเบียน
MODEL_NAME = "iris-classifier"

# เริ่ม MLflow Run
with mlflow.start_run(run_name="random-forest-v1") as run:
    
    # --- กำหนด Hyperparameters ---
    n_estimators = 100
    max_depth = 5
    random_state = 42
    
    # --- บันทึก Parameters ---
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("random_state", random_state)
    
    print("\n📊 Parameters:")
    print(f"   - n_estimators: {n_estimators}")
    print(f"   - max_depth: {max_depth}")
    
    # --- สร้างและฝึกโมเดล ---
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    print("\n🎯 ฝึกโมเดลเรียบร้อย!")
    
    # --- ประเมินผล ---
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # --- บันทึก Metrics ---
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    
    print(f"\n📈 Metrics:")
    print(f"   - Accuracy: {accuracy:.4f}")
    print(f"   - F1 Score: {f1:.4f}")
    
    # ==========================================
    # ⭐ ขั้นตอนสำคัญ: ลงทะเบียนโมเดล
    # ==========================================
    
    # วิธีที่ 1: ลงทะเบียนพร้อมกับ log_model
    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MODEL_NAME,  # ← ชื่อที่จะลงทะเบียน
        input_example=X_train.iloc[:5]
    )
    
    print(f"\n✅ ลงทะเบียนโมเดลเรียบร้อย!")
    print(f"   - Model Name: {MODEL_NAME}")
    print(f"   - Model URI: {model_info.model_uri}")
    print(f"   - Run ID: {run.info.run_id}")

print("\n" + "="*50)
print("🎉 เสร็จสิ้น! ไปดูผลลัพธ์ที่ MLflow UI")
print("   http://127.0.0.1:8080")
print("="*50)
```

### รันโปรแกรม

```bash
python train_and_register.py
```

### ✅ ตรวจสอบผลลัพธ์

1. เปิด MLflow UI ที่ `http://127.0.0.1:8080`
2. คลิกที่แท็บ **"Models"** (ด้านบน)
3. จะเห็นโมเดล `iris-classifier` ที่ลงทะเบียนไว้

---

## 🔬 แบบฝึกหัดที่ 2: การจัดการเวอร์ชันโมเดล

### 🎯 เป้าหมาย

- สร้างหลาย Versions ของโมเดล
- เปรียบเทียบผลลัพธ์ระหว่าง Versions
- เรียนรู้ว่า MLflow จัดการ Versions อย่างไร

### สร้างไฟล์ `model_versioning.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 2 - การจัดการเวอร์ชันโมเดล
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_experiment("model-registration-lab")

# เตรียมข้อมูล
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

MODEL_NAME = "iris-classifier"

# ==========================================
# Version 2: ลองปรับ Hyperparameters
# ==========================================

print("="*50)
print("🔄 สร้าง Version 2: Random Forest (ปรับ params)")
print("="*50)

with mlflow.start_run(run_name="random-forest-v2"):
    
    # Hyperparameters ใหม่
    n_estimators = 200  # เพิ่มจาก 100
    max_depth = 10      # เพิ่มจาก 5
    
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("model_type", "RandomForest")
    
    # ฝึกโมเดล
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # ประเมินผล
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    
    print(f"📈 Accuracy: {accuracy:.4f}")
    
    # ลงทะเบียนเป็น Version ใหม่
    mlflow.sklearn.log_model(
        model, 
        "model",
        registered_model_name=MODEL_NAME
    )
    
    print("✅ ลงทะเบียน Version 2 เรียบร้อย!")

# ==========================================
# Version 3: ลองใช้ Algorithm อื่น
# ==========================================

print("\n" + "="*50)
print("🔄 สร้าง Version 3: Gradient Boosting")
print("="*50)

with mlflow.start_run(run_name="gradient-boosting-v1"):
    
    n_estimators = 100
    max_depth = 3
    learning_rate = 0.1
    
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("model_type", "GradientBoosting")
    
    # ฝึกโมเดล
    model = GradientBoostingClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # ประเมินผล
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    
    print(f"📈 Accuracy: {accuracy:.4f}")
    
    # ลงทะเบียนเป็น Version ใหม่
    mlflow.sklearn.log_model(
        model, 
        "model",
        registered_model_name=MODEL_NAME
    )
    
    print("✅ ลงทะเบียน Version 3 เรียบร้อย!")

# ==========================================
# ดูรายการ Versions ทั้งหมด
# ==========================================

print("\n" + "="*50)
print("📋 รายการ Versions ทั้งหมด")
print("="*50)

from mlflow.tracking import MlflowClient

client = MlflowClient()

# ดึงข้อมูลโมเดลที่ลงทะเบียน
model_versions = client.search_model_versions(f"name='{MODEL_NAME}'")

print(f"\n📦 Model: {MODEL_NAME}")
print("-"*40)

for mv in model_versions:
    print(f"\n   📌 Version {mv.version}")
    print(f"      - Run ID: {mv.run_id[:8]}...")
    print(f"      - Stage: {mv.current_stage}")
    print(f"      - Status: {mv.status}")
```

### รันโปรแกรม

```bash
python model_versioning.py
```

### ✅ ตรวจสอบผลลัพธ์

1. ไปที่ MLflow UI → Models → iris-classifier
2. จะเห็น 3 Versions พร้อมรายละเอียดของแต่ละ Version

---

## 🔬 แบบฝึกหัดที่ 3: การเปลี่ยนสถานะโมเดล (Stage Transitions)

### 🎯 เป้าหมาย

- เรียนรู้การเปลี่ยน Stage ของโมเดล
- เข้าใจ Workflow การ Promote โมเดล
- เพิ่ม Description ให้โมเดล

### สร้างไฟล์ `stage_transitions.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 3 - การเปลี่ยนสถานะโมเดล
"""

from mlflow.tracking import MlflowClient
import mlflow

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# สร้าง MLflow Client
client = MlflowClient()

MODEL_NAME = "iris-classifier"

print("="*60)
print("🔄 การจัดการสถานะโมเดล (Stage Transitions)")
print("="*60)

# ==========================================
# ดูสถานะปัจจุบันของทุก Versions
# ==========================================

print("\n📋 สถานะปัจจุบัน:")
print("-"*40)

versions = client.search_model_versions(f"name='{MODEL_NAME}'")
for v in versions:
    print(f"   Version {v.version}: {v.current_stage}")

# ==========================================
# เปลี่ยนสถานะโมเดล
# ==========================================

# --- 1. ย้าย Version 1 ไป Archived ---
print("\n🔸 ย้าย Version 1 → Archived")

client.transition_model_version_stage(
    name=MODEL_NAME,
    version="1",
    stage="Archived",
    archive_existing_versions=False  # ไม่ย้าย versions อื่น
)
print("   ✅ สำเร็จ!")

# --- 2. ย้าย Version 2 ไป Staging ---
print("\n🔸 ย้าย Version 2 → Staging")

client.transition_model_version_stage(
    name=MODEL_NAME,
    version="2",
    stage="Staging"
)
print("   ✅ สำเร็จ!")

# --- 3. ย้าย Version 3 ไป Production ---
print("\n🔸 ย้าย Version 3 → Production")

client.transition_model_version_stage(
    name=MODEL_NAME,
    version="3",
    stage="Production"
)
print("   ✅ สำเร็จ!")

# ==========================================
# ดูสถานะหลังการเปลี่ยน
# ==========================================

print("\n" + "="*60)
print("📋 สถานะหลังการเปลี่ยน:")
print("-"*40)

# ดึงข้อมูลใหม่
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
for v in versions:
    stage_emoji = {
        "None": "⚪",
        "Staging": "🟡",
        "Production": "🟢",
        "Archived": "⚫"
    }.get(v.current_stage, "❓")
    
    print(f"   {stage_emoji} Version {v.version}: {v.current_stage}")

# ==========================================
# เพิ่มคำอธิบายให้ Version
# ==========================================

print("\n🔸 เพิ่มคำอธิบายให้ Version 3")

client.update_model_version(
    name=MODEL_NAME,
    version="3",
    description="โมเดล Gradient Boosting ที่ผ่านการทดสอบแล้ว ใช้งานจริง"
)
print("   ✅ เพิ่มคำอธิบายเรียบร้อย!")

# ==========================================
# เพิ่มคำอธิบายให้ Registered Model
# ==========================================

print("\n🔸 เพิ่มคำอธิบายให้ Registered Model")

client.update_registered_model(
    name=MODEL_NAME,
    description="โมเดลสำหรับจำแนกประเภทดอกไอริส (Iris Classification)"
)
print("   ✅ เพิ่มคำอธิบายเรียบร้อย!")

print("\n" + "="*60)
print("🎉 เสร็จสิ้น! ไปดูผลลัพธ์ที่ MLflow UI")
print("   http://127.0.0.1:8080")
print("="*60)
```

### รันโปรแกรม

```bash
python stage_transitions.py
```

### ✅ ตรวจสอบผลลัพธ์

1. ไปที่ MLflow UI → Models → iris-classifier
2. จะเห็น Stages ที่เปลี่ยนไปของแต่ละ Version
3. สังเกตสีที่แตกต่างกันของแต่ละ Stage

---

## 🔬 แบบฝึกหัดที่ 4: การโหลดโมเดลจาก Registry

### 🎯 เป้าหมาย

- เรียนรู้วิธีโหลดโมเดลหลายรูปแบบ
- เข้าใจ Model URI Formats
- ทดสอบ Prediction กับโมเดลต่างๆ

### สร้างไฟล์ `load_model.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 4 - การโหลดโมเดลจาก Registry
"""

import mlflow
import pandas as pd
from sklearn.datasets import load_iris

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")

MODEL_NAME = "iris-classifier"

print("="*60)
print("📥 การโหลดโมเดลจาก Model Registry")
print("="*60)

# เตรียมข้อมูลสำหรับทดสอบ
iris = load_iris()
sample_data = pd.DataFrame(
    iris.data[:5], 
    columns=iris.feature_names
)

print("\n📊 ข้อมูลตัวอย่างสำหรับ Prediction:")
print(sample_data)
print(f"\n🎯 คำตอบที่ถูกต้อง: {iris.target[:5]}")

# ==========================================
# วิธีที่ 1: โหลดด้วย Version Number
# ==========================================

print("\n" + "-"*60)
print("🔹 วิธีที่ 1: โหลดด้วย Version Number")
print("-"*60)

# โหลด Version 1
model_v1 = mlflow.sklearn.load_model(
    model_uri=f"models:/{MODEL_NAME}/1"
)

predictions_v1 = model_v1.predict(sample_data)
print(f"\n📦 Version 1 predictions: {predictions_v1}")

# โหลด Version 3
model_v3 = mlflow.sklearn.load_model(
    model_uri=f"models:/{MODEL_NAME}/3"
)

predictions_v3 = model_v3.predict(sample_data)
print(f"📦 Version 3 predictions: {predictions_v3}")

# ==========================================
# วิธีที่ 2: โหลดด้วย Stage
# ==========================================

print("\n" + "-"*60)
print("🔹 วิธีที่ 2: โหลดด้วย Stage (แนะนำ ⭐)")
print("-"*60)

# โหลดโมเดลที่อยู่ใน Production
print("\n🟢 โหลดโมเดล Production:")

model_prod = mlflow.sklearn.load_model(
    model_uri=f"models:/{MODEL_NAME}@production"
)

predictions_prod = model_prod.predict(sample_data)
print(f"   Predictions: {predictions_prod}")

# โหลดโมเดลที่อยู่ใน Staging
print("\n🟡 โหลดโมเดล Staging:")

model_staging = mlflow.sklearn.load_model(
    model_uri=f"models:/{MODEL_NAME}@staging"
)

predictions_staging = model_staging.predict(sample_data)
print(f"   Predictions: {predictions_staging}")

# ==========================================
# วิธีที่ 3: โหลดเป็น PyFunc Model
# ==========================================

print("\n" + "-"*60)
print("🔹 วิธีที่ 3: โหลดเป็น PyFunc (Generic)")
print("-"*60)

# โหลดเป็น PyFunc (ใช้ได้กับทุก ML Framework)
model_pyfunc = mlflow.pyfunc.load_model(
    model_uri=f"models:/{MODEL_NAME}@production"
)

predictions_pyfunc = model_pyfunc.predict(sample_data)
print(f"\n📦 PyFunc predictions: {predictions_pyfunc}")

# ==========================================
# สรุป
# ==========================================

print("\n" + "="*60)
print("📝 สรุป Model URI Formats")
print("="*60)

print("""
┌────────────────────────────────────────────────────────────┐
│  Format                          │  ตัวอย่าง               │
├──────────────────────────────────┼─────────────────────────┤
│  models:/<name>/<version>        │  models:/iris-clf/1     │
│  models:/<name>@<stage>          │  models:/iris-clf@prod  │
│  models:/<name>/latest           │  models:/iris-clf/latest│
└──────────────────────────────────┴─────────────────────────┘

💡 แนะนำใช้ @stage เพราะ:
   ✅ ไม่ต้องเปลี่ยน code เมื่อมี version ใหม่
   ✅ แค่เปลี่ยน stage ของ version ที่ต้องการ
   ✅ code ที่ใช้ @production จะโหลดโมเดลใหม่อัตโนมัติ
""")
```

### รันโปรแกรม

```bash
python load_model.py
```

---

## 🔬 แบบฝึกหัดที่ 5: สร้าง REST API สำหรับ Serve โมเดล

### 🎯 เป้าหมาย

- สร้าง REST API ด้วย Flask
- โหลดโมเดลจาก Production
- ทดสอบด้วย curl

### ติดตั้ง Flask

```bash
pip install flask
```

### สร้างไฟล์ `serve_model.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 5 - สร้าง API สำหรับ Serve โมเดล
"""

from flask import Flask, request, jsonify
import mlflow
import pandas as pd

# ตั้งค่า MLflow
mlflow.set_tracking_uri("http://127.0.0.1:8080")

# โหลดโมเดลจาก Production
MODEL_NAME = "iris-classifier"
print(f"📥 กำลังโหลดโมเดล {MODEL_NAME}@production...")
model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@production")
print("✅ โหลดโมเดลเรียบร้อย!")

# สร้าง Flask App
app = Flask(__name__)

# Feature names สำหรับ Iris dataset
FEATURE_NAMES = [
    'sepal length (cm)', 
    'sepal width (cm)', 
    'petal length (cm)', 
    'petal width (cm)'
]

# Class names
CLASS_NAMES = ['setosa', 'versicolor', 'virginica']

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "stage": "production"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    
    Input JSON format:
    {
        "data": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]
    }
    """
    try:
        # รับข้อมูลจาก request
        input_data = request.json
        
        # แปลงเป็น DataFrame
        df = pd.DataFrame(input_data['data'], columns=FEATURE_NAMES)
        
        # ทำนาย
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)
        
        # สร้าง response
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "prediction": int(pred),
                "class_name": CLASS_NAMES[pred],
                "probabilities": {
                    CLASS_NAMES[j]: round(float(prob), 4)
                    for j, prob in enumerate(probabilities[i])
                }
            })
        
        return jsonify({
            "success": True,
            "results": results
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/model-info', methods=['GET'])
def model_info():
    """ดูข้อมูลโมเดล"""
    from mlflow.tracking import MlflowClient
    client = MlflowClient()
    
    # ดึงข้อมูล Production version
    versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    
    if versions:
        v = versions[0]
        return jsonify({
            "model_name": MODEL_NAME,
            "version": v.version,
            "stage": v.current_stage,
            "description": v.description,
            "run_id": v.run_id
        })
    
    return jsonify({"error": "No production model found"}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Starting Model Serving API")
    print("="*50)
    print(f"\n📦 Model: {MODEL_NAME}")
    print(f"🌐 API URL: http://127.0.0.1:9000")
    print("\n📝 Endpoints:")
    print("   - GET  /health     : Health check")
    print("   - POST /predict    : Make predictions")
    print("   - GET  /model-info : Model information")
    print("\n" + "="*50 + "\n")
    
    app.run(host='127.0.0.1', port=9000, debug=True)
```

### รัน API Server

> ⚠️ **หมายเหตุ:** เปิด Terminal ใหม่ (Terminal ที่ 3) เพราะ Terminal ที่ 1 รัน MLflow Server อยู่

```bash
cd mlflowserver-lab
source .venv/bin/activate
python serve_model.py
```

### ทดสอบ API

เปิด **Terminal ที่ 4** แล้วรันคำสั่ง:

```bash
# ตรวจสอบสถานะ
curl http://127.0.0.1:9000/health

# ดูข้อมูลโมเดล
curl http://127.0.0.1:9000/model-info

# ทดสอบ Prediction
curl -X POST http://127.0.0.1:9000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]}'
```

---

## 🔬 แบบฝึกหัดที่ 6: Automated Model Promotion Pipeline (Advanced)

### 🎯 เป้าหมาย

- สร้าง Pipeline อัตโนมัติสำหรับเปรียบเทียบโมเดล
- Auto-promote โมเดลจาก Staging → Production
- สร้าง Comparison Report

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Automated Model Promotion Pipeline                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐                                                          │
│   │   Staging    │                                                          │
│   │    Model     │                                                          │
│   │     🟡       │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────────────────────────────────────────────────────────┐      │
│   │                      Compare Performance                          │      │
│   │  ┌────────────────────────────────────────────────────────────┐  │      │
│   │  │  Staging Accuracy vs Production Accuracy                    │  │      │
│   │  │                                                             │  │      │
│   │  │  if staging_acc > production_acc:                           │  │      │
│   │  │      promote staging → production                           │  │      │
│   │  │      archive old production                                 │  │      │
│   │  │  else:                                                      │  │      │
│   │  │      keep current production                                │  │      │
│   │  └────────────────────────────────────────────────────────────┘  │      │
│   └──────────────────────────────────────────────────────────────────┘      │
│          │                                                                   │
│          ▼                                                                   │
│   ┌──────────────┐         ┌──────────────┐                                 │
│   │  Production  │   OR    │    Keep      │                                 │
│   │   (Updated)  │         │   Current    │                                 │
│   │     🟢       │         │     🟢       │                                 │
│   └──────────────┘         └──────────────┘                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### สร้างไฟล์ `auto_promote.py`

```python
"""
Lab: Model Registration with MLflow
แบบฝึกหัดที่ 6 - Automated Model Promotion Pipeline
"""

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime

# ==========================================
# Configuration
# ==========================================

mlflow.set_tracking_uri("http://127.0.0.1:8080")
client = MlflowClient()

MODEL_NAME = "iris-classifier"
METRIC_NAME = "accuracy"
THRESHOLD = 0.0  # Staging ต้องดีกว่า Production อย่างน้อย 0%

# ==========================================
# Prepare Test Data
# ==========================================

print("="*70)
print("🤖 Automated Model Promotion Pipeline")
print("="*70)

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# Get Models from Registry
# ==========================================

print("\n📋 ดึงข้อมูลโมเดลจาก Registry...")

def get_model_by_stage(model_name, stage):
    """Get model version by stage"""
    versions = client.get_latest_versions(model_name, stages=[stage])
    return versions[0] if versions else None

staging_model = get_model_by_stage(MODEL_NAME, "Staging")
production_model = get_model_by_stage(MODEL_NAME, "Production")

if not staging_model:
    print("❌ ไม่พบโมเดลใน Staging")
    exit(1)

if not production_model:
    print("⚠️ ไม่พบโมเดลใน Production - จะ promote Staging ไป Production โดยตรง")
    
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=staging_model.version,
        stage="Production"
    )
    print(f"✅ Promote Version {staging_model.version} → Production")
    exit(0)

print(f"\n   🟡 Staging:    Version {staging_model.version}")
print(f"   🟢 Production: Version {production_model.version}")

# ==========================================
# Load and Evaluate Models
# ==========================================

print("\n📊 ประเมินประสิทธิภาพโมเดล...")

def evaluate_model(model_uri, X_test, y_test):
    """Load and evaluate model"""
    model = mlflow.sklearn.load_model(model_uri)
    predictions = model.predict(X_test)
    accuracy = (predictions == y_test).mean()
    return accuracy

staging_uri = f"models:/{MODEL_NAME}@staging"
production_uri = f"models:/{MODEL_NAME}@production"

staging_accuracy = evaluate_model(staging_uri, X_test, y_test)
production_accuracy = evaluate_model(production_uri, X_test, y_test)

print(f"\n   🟡 Staging Accuracy:    {staging_accuracy:.4f}")
print(f"   🟢 Production Accuracy: {production_accuracy:.4f}")
print(f"   📈 Difference:          {staging_accuracy - production_accuracy:+.4f}")

# ==========================================
# Decision: Promote or Keep
# ==========================================

print("\n" + "="*70)
print("🔍 ตัดสินใจ...")
print("="*70)

if staging_accuracy > production_accuracy + THRESHOLD:
    print(f"\n✅ Staging ({staging_accuracy:.4f}) ดีกว่า Production ({production_accuracy:.4f})")
    print("   → จะ Promote Staging ไป Production")
    
    # Archive current production
    print(f"\n🔸 Archive Production Version {production_model.version}...")
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=production_model.version,
        stage="Archived"
    )
    
    # Promote staging to production
    print(f"🔸 Promote Staging Version {staging_model.version} → Production...")
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=staging_model.version,
        stage="Production"
    )
    
    # Add description
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client.update_model_version(
        name=MODEL_NAME,
        version=staging_model.version,
        description=f"Auto-promoted on {timestamp}. Accuracy: {staging_accuracy:.4f}"
    )
    
    print("\n🎉 Promotion สำเร็จ!")
    
else:
    print(f"\n⏸️ Staging ({staging_accuracy:.4f}) ไม่ดีกว่า Production ({production_accuracy:.4f})")
    print("   → คง Production ไว้เหมือนเดิม")

# ==========================================
# Generate Report
# ==========================================

print("\n" + "="*70)
print("📝 Comparison Report")
print("="*70)

report = f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    Model Comparison Report                           │
├─────────────────────────────────────────────────────────────────────┤
│  Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                                       │
│  Model: {MODEL_NAME}                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🟡 Staging (Version {staging_model.version})                                           │
│     - Accuracy: {staging_accuracy:.4f}                                              │
│     - Run ID: {staging_model.run_id[:20]}...                       │
│                                                                      │
│  🟢 Production (Version {production_model.version})                                       │
│     - Accuracy: {production_accuracy:.4f}                                              │
│     - Run ID: {production_model.run_id[:20]}...                       │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  📊 Comparison                                                       │
│     - Accuracy Difference: {staging_accuracy - production_accuracy:+.4f}                                    │
│     - Winner: {"Staging 🏆" if staging_accuracy > production_accuracy else "Production 🏆"}                                                    │
│     - Action Taken: {"Promoted Staging → Production" if staging_accuracy > production_accuracy + THRESHOLD else "Kept Current Production"}                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
"""

print(report)

# Save report to file
with open("promotion_report.txt", "w") as f:
    f.write(report)

print("📁 Report saved to: promotion_report.txt")

# ==========================================
# Final Status
# ==========================================

print("\n" + "="*70)
print("📋 สถานะปัจจุบัน")
print("="*70)

versions = client.search_model_versions(f"name='{MODEL_NAME}'")
for v in sorted(versions, key=lambda x: int(x.version)):
    stage_emoji = {
        "None": "⚪",
        "Staging": "🟡", 
        "Production": "🟢",
        "Archived": "⚫"
    }.get(v.current_stage, "❓")
    print(f"   {stage_emoji} Version {v.version}: {v.current_stage}")
```

### รันโปรแกรม

```bash
python auto_promote.py
```

---

## 📂 โครงสร้างไฟล์หลังจบ Lab

```
mlflowserver-lab/
├── .venv/                      # Virtual Environment
├── mlruns_db/
│   └── mlflow.db               # SQLite Database
├── mlartifacts/                # Model Artifacts
│
├── train_and_register.py       # Lab 1: ฝึกและลงทะเบียนโมเดล
├── model_versioning.py         # Lab 2: จัดการ Versions
├── stage_transitions.py        # Lab 3: เปลี่ยน Stages
├── load_model.py               # Lab 4: โหลดโมเดล
├── serve_model.py              # Lab 5: REST API
├── auto_promote.py             # Lab 6: Automated Pipeline
│
└── promotion_report.txt        # Report จาก Lab 6
```

---

## 📝 สรุป

### สิ่งที่ได้เรียนรู้

| หัวข้อ | คำสั่ง/วิธีการ |
|--------|---------------|
| ลงทะเบียนโมเดล | `mlflow.sklearn.log_model(..., registered_model_name="...")` |
| จัดการ Versions | ทุกครั้งที่ log_model ด้วยชื่อเดิม จะสร้าง version ใหม่ |
| เปลี่ยน Stage | `client.transition_model_version_stage(...)` |
| โหลดด้วย Version | `models:/<name>/<version>` |
| โหลดด้วย Stage | `models:/<name>@<stage>` |
| อัพเดท Description | `client.update_model_version(...)` |

### Best Practices

1. **ใช้ชื่อโมเดลที่สื่อความหมาย** เช่น `iris-classifier`, `sales-predictor`

2. **เพิ่มคำอธิบายให้ทุก Version** เพื่อให้ทีมเข้าใจว่าแต่ละ version ต่างกันอย่างไร

3. **ใช้ @stage แทน version number** ในโค้ดที่ใช้งานจริง เพื่อให้อัปเดตโมเดลได้ง่าย

4. **ทดสอบใน Staging ก่อน Production** เสมอ

5. **สร้าง Automated Pipeline** เพื่อลด Human Error และเพิ่มความเร็วในการ Deploy

---

## 🎯 แบบฝึกหัดเพิ่มเติม

1. **ฝึกโมเดลใหม่** โดยใช้ Dataset อื่น และลงทะเบียนเป็นโมเดลใหม่

2. **เพิ่ม Tags** ให้กับ Registered Model และ Model Versions

3. **สร้าง CI/CD Pipeline** ด้วย GitHub Actions ที่ทดสอบและ Deploy โมเดลอัตโนมัติ

4. **เพิ่ม Model Signature** เพื่อตรวจสอบ Input/Output Schema

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [MLflow Model Registry Documentation](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Python API](https://mlflow.org/docs/latest/python_api/index.html)
- [MLOps Best Practices](https://ml-ops.org/)

---

**🎉 ยินดีด้วย! คุณได้เรียนรู้การจัดการโมเดลด้วย MLflow Model Registry แล้ว**