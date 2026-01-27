# 🧪 Lab: การติดตั้งและใช้งาน MLflow เบื้องต้น

## 📋 คำอธิบาย Lab

**MLflow** คือ Open-source Platform สำหรับจัดการ Machine Learning Lifecycle ทั้งหมด ตั้งแต่การทดลอง (Experiment Tracking) การจัดการโมเดล (Model Registry) ไปจนถึงการ Deploy โมเดล

### 🎯 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. ติดตั้งและตั้งค่า MLflow บนเครื่องของตนเองได้
2. เข้าใจองค์ประกอบหลักของ MLflow (Tracking Server, Backend Store, Artifact Store)
3. เปิดใช้งาน MLflow Tracking Server แบบ Persistent ได้
4. เชื่อมต่อ Python Client กับ MLflow Server ได้

### 📚 ความรู้พื้นฐานที่ต้องมี

- Python เบื้องต้น
- การใช้งาน Command Line / Terminal

---

## 📦 ข้อกำหนดเบื้องต้น (Prerequisites)

| รายการ | รายละเอียด |
|--------|------------|
| Python | เวอร์ชัน 3.9 - 3.12 |
| pip | ตัวจัดการ Package ของ Python |
| ระบบปฏิบัติการ | Linux หรือ macOS |
| Port ที่ต้องใช้ | 5000 (สำหรับ Tracking Server และ UI) |

---

## 🐳 การใช้งาน LAB ผ่าน Docker

### 🧹 ขั้นตอนที่ 0: ลบ Container เก่า (กรณีต้องการเริ่มต้นใหม่)

หากเคยรัน Lab นี้มาก่อนและต้องการ clear ของเก่าทั้งหมด ให้รันคำสั่งต่อไปนี้:

**สำหรับ Linux / macOS / Git Bash:**

```bash
# หยุด container ทั้งหมด
docker stop $(docker ps -aq)

# ลบ container ทั้งหมด
docker rm $(docker ps -aq)
```

**สำหรับ Windows (Command Prompt):**

```cmd
# หยุด container ทั้งหมด
for /f "tokens=*" %i in ('docker ps -aq') do docker stop %i

# ลบ container ทั้งหมด
for /f "tokens=*" %i in ('docker ps -aq') do docker rm %i
```

**สำหรับ Windows (PowerShell):**

```powershell
# หยุด container ทั้งหมด
docker ps -aq | ForEach-Object { docker stop $_ }

# ลบ container ทั้งหมด
docker ps -aq | ForEach-Object { docker rm $_ }
```

---

### 🚀 ขั้นตอนที่ 1: รัน Docker Container

สำหรับผู้ที่ต้องการใช้งานผ่าน Docker Container ที่ติดตั้ง Library พื้นฐานไว้ครบถ้วนแล้ว สามารถรันคำสั่งดังนี้:

```bash
docker run -d -p 5000:5000 -p 8888:8888 --name mlops-container tuchsanai/mlops_2568_2:latest
```

**อธิบาย Port ที่ใช้งาน:**

| Port | Service | URL |
|------|---------|-----|
| 5000 | MLflow Tracking Server | http://127.0.0.1:5000 |
| 8888 | Jupyter Notebook | http://127.0.0.1:8888 |

---

## 🚀 ขั้นตอนการทำ Lab

### ขั้นตอนที่ 2: สร้างโฟลเดอร์และเปิดใช้งาน MLflow Tracking Server

```bash
# 2.1 สร้างโฟลเดอร์สำหรับเก็บไฟล์ Lab
mkdir -p /home/student/workspace/mlflowserver-lab

# 2.2 เข้าไปในโฟลเดอร์
cd /home/student/workspace/mlflowserver-lab

# 2.3 สร้างโฟลเดอร์เก็บข้อมูล
mkdir -p /home/student/workspace/mlflowserver-lab/mlruns_db
mkdir -p /home/student/workspace/mlflowserver-lab/mlartifacts

# 2.4 เปิด Server ให้เข้าถึงได้จากทุก IP
nohup mlflow server \
  --host 0.0.0.0 --port 5000 \
  --backend-store-uri sqlite:////home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db \
  --artifacts-destination /home/student/workspace/mlflowserver-lab/mlartifacts \
  --serve-artifacts > mlflow.log 2>&1 &
```

**🗂️ อธิบายโครงสร้างไฟล์:**

```
/home/student/workspace/mlflowserver-lab/
├── mlruns_db/
│   └── mlflow.db          # ฐานข้อมูล SQLite เก็บ Experiment และ Run Metadata
├── mlartifacts/           # โฟลเดอร์เก็บ Model Files และ Artifacts
```

| ส่วนประกอบ | หน้าที่ | Full Path |
|-----------|--------|-----------|
| Backend Store (SQLite) | เก็บข้อมูล Experiment, Run, Parameters, Metrics | `/home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db` |
| Artifact Store | เก็บไฟล์โมเดล, กราฟ, ไฟล์ผลลัพธ์อื่นๆ | `/home/student/workspace/mlflowserver-lab/mlartifacts/` |

---

### ขั้นตอนที่ 3: ตรวจสอบ MLflow UI

1. เปิด Web Browser
2. ไปที่ URL: **http://127.0.0.1:5000**
3. จะเห็นหน้า MLflow UI ดังรูป:

![MLflow UI](./img/1.png)

---

## 📊 สรุปสิ่งที่ได้เรียนรู้

| หัวข้อ | สิ่งที่ได้เรียนรู้ |
|--------|------------------|
| Tracking Server | การเปิดใช้งาน Server แบบ Persistent |
| Storage Architecture | เข้าใจ Backend Store และ Artifact Store |

---

## ❓ คำถามทบทวน

1. MLflow Tracking Server มีหน้าที่อะไร?
2. Backend Store และ Artifact Store ต่างกันอย่างไร?
3. ทำไมการใช้ Persistent Storage ถึงดีกว่า In-memory สำหรับงานจริง?

---

## 🔗 แหล่งเรียนรู้เพิ่มเติม

- [MLflow Official Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Tracking Guide](https://mlflow.org/docs/latest/tracking.html)
- [MLflow GitHub Repository](https://github.com/mlflow/mlflow)

---

## 🛠️ การแก้ปัญหาที่พบบ่อย (Troubleshooting)

### ปัญหา: Port 5000 ถูกใช้งานอยู่แล้ว

**วิธีแก้:** เปลี่ยนไปใช้ Port อื่น เช่น 5001

```bash
nohup mlflow server \
  --host 0.0.0.0 --port 5001 \
  --backend-store-uri sqlite:////home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db \
  --artifacts-destination /home/student/workspace/mlflowserver-lab/mlartifacts \
  --serve-artifacts > mlflow.log 2>&1 &
```

### ปัญหา: ไม่สามารถเชื่อมต่อกับ Server ได้

**ตรวจสอบ:**

1. Server กำลังทำงานอยู่หรือไม่ (ดูใน Terminal ที่รัน Server)
2. URL ถูกต้องหรือไม่
3. Firewall ไม่ได้บล็อก Port

---

**📝 หมายเหตุ:** Lab นี้เป็นพื้นฐานสำหรับการใช้งาน MLflow ใน Lab ถัดไปจะเรียนรู้การ Log Experiments และ Track Models