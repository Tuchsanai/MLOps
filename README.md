# 📘 Machine Learning Operations (MLOps)

## 📝 Course Description

กระบวนการทำเอ็มแอลอีอพ กระบวนการสร้างแบบจำลอง เช่น การนำเข้าข้อมูล การสอนแบบจำลอง การเตรียมแบบจำลองเพื่อสำหรับนำไปใช้งาน กระบวนการสำหรับการนำแบบจำลองไปใช้งาน เช่น การทดสอบโปรแกรม กระบวนการตรวจสอบแบบจำลอง เช่น การตรวจสอบแบบจำลอง การวิเคราะห์ประสิทธิภาพของแบบจำลอง การกำกับควบคุมการใช้แบบจำลอง

**MLOps Lifecycle:** Build Pipeline → Deploy Pipeline → Monitoring Pipeline

---

## 🎯 Course Learning Outcomes (CLOs)

| CLO | รายละเอียด |
|-----|------------|
| **CLO1** | อธิบายแนวคิด MLOps Lifecycle และกระบวนการทำงานของ ML Pipeline ได้ |
| **CLO2** | ใช้ระบบควบคุมเวอร์ชัน (Git และ DVC) ในการจัดการโค้ดและข้อมูลของ ML Projects ได้ |
| **CLO3** | ออกแบบและสร้าง Build Pipeline สำหรับนำเข้าข้อมูล สอนแบบจำลอง และทดสอบแบบจำลองได้ |
| **CLO4** | บันทึกและจัดการ Experiment รวมถึงลงทะเบียนแบบจำลองด้วย MLflow ได้ |
| **CLO5** | สร้าง Container ด้วย Docker และพัฒนา REST API สำหรับ Deploy แบบจำลองได้ |
| **CLO6** | ตรวจสอบและวิเคราะห์ประสิทธิภาพของแบบจำลองที่ Deploy แล้วได้ |
| **CLO7** | ตรวจจับ Data Drift และ Model Drift เพื่อกำกับควบคุมการใช้แบบจำลองได้ |

---

## 📅 Course Schedule (15 Weeks)

---

# 🔹 Module 1: ML Life Cycle และ Git (Week 1-4)

---

## Week 01: บทนำ MLOps และ Git พื้นฐาน

> **วัตถุประสงค์:** เข้าใจภาพรวมของ MLOps และเริ่มต้นใช้งาน Git

### 1. MLOps คืออะไร?
- แนวคิด Machine Learning Operations
- ML Lifecycle Overview
- การผสมผสาน ML + DevOps + Data Engineering

### 2. Git พื้นฐาน
- การตั้งค่า Git Configuration (`user.name`, `user.email`)
- คำสั่งพื้นฐาน: `git init`, `git add`, `git commit`
- การสร้าง Private Repository บน GitHub

### 3. Git กับ ML Projects
- การ Clone ด้วย Token
- การ Train Model บน Cloud
- การ Push ผลลัพธ์กลับ GitHub

### 4. Data Ingestion Concepts ⭐
- แนวคิดการนำเข้าข้อมูลสำหรับ ML
- Data Sources และ Data Formats
- การจัดการ Data Pipeline เบื้องต้น

**📌 CLO ที่เกี่ยวข้อง:** CLO1, CLO2, CLO3

---

## Week 02: Git สำหรับ ML Projects

> **วัตถุประสงค์:** จัดการโครงสร้างโปรเจกต์ ML และติดตามการเปลี่ยนแปลง

### 1. Git Fundamentals for MLOps
- การใช้ `.gitignore` สำหรับ ML Projects
- การ Track ไฟล์ที่ควร/ไม่ควร Track
- โครงสร้าง ML Project ที่เหมาะสม

### 2. คำสั่ง Git ขั้นสูง
- `git diff` - ดูการเปลี่ยนแปลง
- `git log` - ดูประวัติ Commits
- `git status` - ตรวจสอบสถานะ

### 3. ML Project Structure
- การจัดโครงสร้างโฟลเดอร์: `src/`, `config/`, `data/`, `models/`, `results/`
- สิ่งที่ควร Track vs ไม่ควร Track
- การเขียน Commit Message ที่ดี

**📌 CLO ที่เกี่ยวข้อง:** CLO2, CLO3

---

## Week 03: Git Branch และ Merge

> **วัตถุประสงค์:** จัดการ Branch และ Merge สำหรับการทดลอง ML

### 1. Git Branch Workflow
- การสร้าง/ลบ/เปลี่ยนชื่อ Branch
- `git switch` vs `git checkout`
- Branch Naming Convention สำหรับ ML

### 2. Branch Strategy สำหรับ ML
- `experiment/` branches สำหรับทดลอง Model
- `feature/` branches สำหรับ Feature Engineering
- `tune/` branches สำหรับ Hyperparameter Tuning
- `fix/` branches สำหรับแก้ไข Bug

### 3. Git Merge
- Fast-Forward Merge
- 3-Way Merge
- การแก้ไข Merge Conflicts

### 4. Remote Repository
- การ Push/Pull จาก Remote
- การจัดการ Remote Branches
- การตั้ง Upstream Tracking

**📌 CLO ที่เกี่ยวข้อง:** CLO2, CLO3

---

## Week 04: Git Recovery Operations

> **วัตถุประสงค์:** กู้คืนและจัดการ Pipeline ที่ผิดพลาด

### 1. Git Restore
- กู้คืนไฟล์ใน Working Directory
- กู้คืนไฟล์จาก Staging Area
- กู้คืนไฟล์จาก Commit เฉพาะ

### 2. Git Reset
- `--soft`: ย้าย HEAD เก็บ Staging และ Working Directory
- `--hard`: ลบทุกอย่าง ย้อนกลับสมบูรณ์
- การใช้ `HEAD~n` อ้างอิง Commit

### 3. การจัดการ ML Pipeline ที่ผิดพลาด
- สถานการณ์: Model เปลี่ยนแล้วผลแย่ลง
- การ Rollback ไปใช้ Model Version เดิม
- Git Reflog สำหรับกู้คืน Commit ที่หาย

### 4. Model Testing with Git ⭐
- การทดสอบ Model ก่อน Commit
- การใช้ Pre-commit Hooks
- Automated Testing Concepts

**📌 CLO ที่เกี่ยวข้อง:** CLO2, CLO3

---

# 🔹 Module 2: MLflow (Week 5-7)

---

## Week 05: MLflow Basics & Tracking

> **วัตถุประสงค์:** ติดตั้งและใช้งาน MLflow สำหรับ Experiment Tracking

### 1. MLflow Overview
- 4 Components หลัก: Tracking, Projects, Models, Registry
- การติดตั้งและตั้งค่า MLflow Server
- Backend Store (SQLite) vs Artifact Store

### 2. MLflow Server Setup
- การรัน MLflow Server บน Docker
- การตั้งค่า Port และ Host
- การเข้าถึง MLflow UI

### 3. Experiment และ Run
- การสร้าง Experiment
- การสร้างและจัดการ Runs
- Experiment Naming Convention

### 4. Parameters Logging
- `mlflow.log_param()` - บันทึกทีละค่า
- `mlflow.log_params()` - บันทึกหลายค่า
- ประเภท Parameters: Hyperparameters, Data Parameters, Architecture

### 5. Metrics Logging
- `mlflow.log_metric()` - บันทึก Metric ทีละค่า
- `mlflow.log_metrics()` - บันทึกหลายค่า
- การบันทึก Metrics พร้อม Step (Training Loop)

### 6. Artifacts Logging
- `mlflow.log_artifact()` - บันทึกไฟล์เดี่ยว
- `mlflow.log_artifacts()` - บันทึกทั้งโฟลเดอร์
- การบันทึก Plots, Configs, Models

### 7. Model Logging
- `mlflow.sklearn.log_model()`
- `mlflow.pytorch.log_model()`
- Model Signature และ Input Example

### 8. Autolog
- `mlflow.sklearn.autolog()`
- `mlflow.pytorch.autolog()`
- สิ่งที่ Autolog บันทึกให้อัตโนมัติ

**📌 CLO ที่เกี่ยวข้อง:** CLO3, CLO4

---

## Week 06: MLflow Model Registry

> **วัตถุประสงค์:** จัดการเวอร์ชันและ Lifecycle ของ Model

### 1. Model Registry Concepts
- Registered Model vs Model Version
- Model Stages: None → Staging → Production → Archived
- Model Aliases และ Tags

### 2. การลงทะเบียน Model
- `mlflow.register_model()`
- การลงทะเบียนพร้อม Log
- การจัดการ Model Versions

### 3. Model Lifecycle Management
- Stage Transitions
- การใช้ Aliases (champion, challenger, baseline)
- Model Lineage และ Audit Trail

### 4. Best Practices
- การตั้งชื่อ Model
- การใช้ Tags อย่างเหมาะสม
- Workflow แนะนำสำหรับ Model Promotion

### 5. Model Governance ⭐
- การกำกับควบคุมการใช้แบบจำลอง
- Access Control และ Permissions
- Audit Logging และ Compliance

**📌 CLO ที่เกี่ยวข้อง:** CLO4, CLO7

---

## Week 07: MLflow Model Deployment

> **วัตถุประสงค์:** Deploy Model เป็น REST API

### 1. Model Serving Architecture
- MLflow Models Format
- Model Flavors (sklearn, pytorch, tensorflow, etc.)
- REST API Endpoints

### 2. Model Deployment
- `mlflow models serve` command
- การ Deploy เป็น REST API
- Input Format: dataframe_split, dataframe_records, instances

### 3. การเรียกใช้ Model ผ่าน API
- HTTP POST requests
- JSON Input/Output Format
- Batch Prediction

### 4. Application Testing Basics ⭐
- การทดสอบ API Endpoint
- Unit Testing สำหรับ Model Service
- Integration Testing Concepts

**📌 CLO ที่เกี่ยวข้อง:** CLO4, CLO5

---

# 🔹 Module 3: Model Monitoring (Week 8-9)

---

## Week 08: Foundation & Model Performance Monitoring

> **วัตถุประสงค์:** ตรวจสอบคุณภาพข้อมูลและประสิทธิภาพ Model

### 1. Introduction to Monitoring
- ความสำคัญของ Model Monitoring
- การติดตั้งและตั้งค่า Evidently AI
- โครงสร้าง Report และ Test Suite

### 2. Data Quality Monitoring
- Missing Values Detection
- Duplicate Detection
- Outlier Detection
- Data Quality Reports และ Alerts

### 3. Model Performance Tracking
- **Classification Metrics:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix, AUC-ROC
- **Regression Metrics:** MAE, RMSE, R²
- การเปรียบเทียบ Reference vs Current Performance

### 4. Target Drift Detection
- การตรวจจับการเปลี่ยนแปลงของ Target Distribution
- Prediction Drift
- การสร้าง Alerts

### 5. Monitoring Dashboard
- Interactive HTML Reports
- การรวม Multiple Metrics
- Export และ Share Reports

**📌 CLO ที่เกี่ยวข้อง:** CLO6, CLO7

---

## Week 09: Data Drift & Advanced Monitoring

> **วัตถุประสงค์:** ตรวจจับ Data Drift และวิเคราะห์ขั้นสูง

### 1. Data Drift Concepts (LAB 1)
- **Covariate Shift:** การเปลี่ยนแปลงของ Input Distribution
- **Concept Drift:** การเปลี่ยนแปลงความสัมพันธ์ระหว่าง Input และ Output
- **Prior Probability Shift:** การเปลี่ยนแปลงของ Target Distribution

### 2. Statistical Tests for Drift Detection
- **KS Test (Kolmogorov-Smirnov):** สำหรับ Numerical Features
- **Chi-Square Test:** สำหรับ Categorical Features
- **PSI (Population Stability Index):** วัดความเสถียรของ Distribution
- **Wasserstein Distance:** วัดระยะห่างระหว่าง Distributions

### 3. Feature Drift Detection (LAB 2)
- Per-Feature Analysis
- Numerical vs Categorical Feature Drift
- Feature Distribution Visualization

### 4. Multivariate Drift Analysis (LAB 3)
- Correlation Analysis
- PCA-based Drift Detection
- Mahalanobis Distance
- Dataset-level Drift

**📌 CLO ที่เกี่ยวข้อง:** CLO6, CLO7

---

# 🔹 Module 4: Cloud Computing & Deployment (Week 10-14)

---

## Week 10: Google Cloud Platform และ DVC สำหรับ MLOps

> **วัตถุประสงค์:** ใช้งาน Google Cloud Platform และ DVC สำหรับ ML Workloads

### 1. GCP Overview
- แนะนำ Google Cloud Platform
- การสร้าง Project และตั้งค่า Billing
- Cloud Console และ Cloud Shell

### 2. Compute Engine
- การสร้าง VM Instance
- การเลือก Machine Type สำหรับ ML
- SSH และการจัดการ Instance

### 3. Cloud Storage
- การสร้างและจัดการ Buckets
- การ Upload/Download ข้อมูล
- gsutil Commands

### 4. DVC (Data Version Control)
- แนวคิด Data Versioning
- ข้อจำกัดของ Git กับไฟล์ขนาดใหญ่
- การติดตั้งและตั้งค่า DVC
- คำสั่งพื้นฐาน: `dvc init`, `dvc add`, `dvc push/pull`

### 5. DVC กับ Google Cloud Storage
- การเชื่อมต่อ DVC กับ GCS
- การสร้าง DVC Pipeline ด้วย `dvc.yaml`
- การกำหนด Stages และ Dependencies
- `dvc repro` สำหรับ Reproduce Pipeline

**📌 CLO ที่เกี่ยวข้อง:** CLO2, CLO3

---

## Week 11: Docker Fundamentals สำหรับ ML

> **วัตถุประสงค์:** สร้าง Container สำหรับ ML Applications

### 1. Docker Basics
- Container vs Virtual Machine
- Docker Architecture (Images, Containers, Registry)
- การติดตั้ง Docker

### 2. Dockerfile สำหรับ ML
- การเขียน Dockerfile
- Base Images สำหรับ ML (python, pytorch, tensorflow)
- Multi-stage Builds

### 3. การจัดการ Dependencies
- requirements.txt vs Conda Environment
- Pip Install Best Practices
- Caching Dependencies

### 4. Building และ Running Containers
- `docker build`
- `docker run`
- Volume Mounting สำหรับ Data และ Models
- Environment Variables

### 5. Docker Compose Basics
- การเขียน docker-compose.yml
- Multi-container Applications
- Networking ระหว่าง Containers

**📌 CLO ที่เกี่ยวข้อง:** CLO5

---

## Week 12: Docker Advanced และ ML Containerization

> **วัตถุประสงค์:** Containerize ML Model สำหรับ Production

### 1. Advanced Dockerfile Techniques
- การ Optimize Docker Image Size
- Layer Caching Strategies
- Security Best Practices

### 2. ML Model Containerization
- การ Package Model กับ Dependencies
- Model Loading ใน Container

### 3. Container Testing
- การทดสอบ Container Image
- Health Checks
- Smoke Testing

### 4. Docker Registry
- การใช้ Docker Hub
- Private Registry
- การ Tag และ Version Images

### 5. Container Orchestration Intro
- แนะนำ Kubernetes Concepts

**📌 CLO ที่เกี่ยวข้อง:** CLO5

---

## Week 13: FastAPI และ Docker สำหรับ ML Model Serving

> **วัตถุประสงค์:** พัฒนา REST API สำหรับ Model Serving ด้วย FastAPI และ Containerize ด้วย Docker

### 1. FastAPI Basics
- การติดตั้งและตั้งค่า FastAPI
- Path Operations (GET, POST)
- Request และ Response Models

### 2. ML Model Integration
- การ Load Model ใน FastAPI

### 3. Dockerize FastAPI Application
- การเขียน Dockerfile สำหรับ FastAPI
- การจัดการ Dependencies ใน Container
- Multi-stage Build สำหรับ Production
- การตั้งค่า Uvicorn ใน Docker

### 4. Docker Compose สำหรับ ML Service
- การเขียน docker-compose.yml
- Volume Mounting สำหรับ Models
- Environment Variables Configuration
- Health Checks สำหรับ API Container

**📌 CLO ที่เกี่ยวข้อง:** CLO5

---

## Week 14: Production Deployment และ Application Testing

> **วัตถุประสงค์:** Deploy Model API สู่ Production พร้อมการทดสอบ

### 1. Production-Ready API
- Gunicorn/Uvicorn Configuration

### 2. Application Testing
- Unit Testing สำหรับ FastAPI

### 3. Containerized Deployment
- การ Dockerize FastAPI App
- Docker Compose สำหรับ ML Service
- Environment Configuration

### 4. End-to-End Pipeline Review
- การรวม Build, Deploy, Monitoring Pipeline

**📌 CLO ที่เกี่ยวข้อง:** CLO1, CLO5

---

# 🔹 Module 5: Project (Week 15)

---

## Week 15: Project Presentation

> **วัตถุประสงค์:** นำเสนอโปรเจกต์ End-to-End MLOps

### 1. Project Presentation
- นำเสนอ End-to-End MLOps Project
- Peer Review และ Feedback
- Q&A Session

**📌 CLO ที่เกี่ยวข้อง:** CLO1-CLO7 (ทุก CLO)

---

## 🛠️ เครื่องมือที่ใช้ในรายวิชา

| Category | Tools |
|----------|-------|
| **Version Control** | Git, GitHub, DVC |
| **Experiment Tracking** | MLflow |
| **Monitoring** | Evidently AI |
| **Cloud Platform** | Google Cloud Platform |
| **Containerization** | Docker, Docker Compose |
| **API Development** | FastAPI, Pydantic |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, Locust |

---

## 📊 CLO-Week Mapping Matrix

| Week | CLO1 | CLO2 | CLO3 | CLO4 | CLO5 | CLO6 | CLO7 |
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| 1 | ✓ | ✓ | ✓ | | | | |
| 2 | | ✓ | ✓ | | | | |
| 3 | | ✓ | | | | | |
| 4 | | ✓ | ✓ | | | | |
| 5 | | | ✓ | ✓ | | | |
| 6 | | | | ✓ | | | ✓ |
| 7 | | | | ✓ | ✓ | | |
| 8 | | | | | | ✓ | ✓ |
| 9 | | | | | | ✓ | ✓ |
| 10 | | ✓ | ✓ | | | | |
| 11 | | | | | ✓ | | |
| 12 | | | | | ✓ | | |
| 13 | | | | | ✓ | | |
| 14 | ✓ | | | | ✓ | | |
| 15 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

