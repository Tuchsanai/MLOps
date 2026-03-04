# 🐳 Docker Compose

## 📌 ภาพรวม (Overview)

**Docker Compose** คือเครื่องมือสำหรับ **กำหนดและจัดการ multi-container Docker applications** โดยใช้ไฟล์ YAML เพียงไฟล์เดียว (`docker-compose.yml`) แทนที่จะต้องรันคำสั่ง `docker run` หลายครั้งสำหรับแต่ละ container

---

## 🤔 ปัญหา: ถ้าไม่มี Docker Compose

สมมติว่าเราต้องการรัน application ที่ประกอบด้วยหลาย services เราจะต้องรันคำสั่ง `docker run` แยกกันทีละตัว:

```bash
docker run yourname/simple-webapp
docker run mongodb
docker run redis:alpine
docker run ansible
```

### ❌ ข้อเสียของวิธีนี้

- ต้องรันคำสั่งหลายครั้ง ทีละ container
- จัดการลำดับการเริ่มต้น (startup order) ได้ยาก
- ไม่มี network เชื่อมต่อระหว่าง containers โดยอัตโนมัติ
- ยากต่อการ reproduce environment ให้เหมือนกันทุกครั้ง

---

## ✅ วิธีแก้: ใช้ Docker Compose

เราสามารถรวมทุก services ไว้ในไฟล์ `docker-compose.yml` เพียงไฟล์เดียว:

```yaml
services:
  web:
    image: "yourname/simple-webapp"
  database:
    image: "mongodb"
  messaging:
    image: "redis:alpine"
  orchestration:
    image: "ansible"
```

### 🔍 อธิบายแต่ละ Service

| Service | Image | หน้าที่ |
|---------|-------|---------|
| **web** | `yourname/simple-webapp` | Web Application หลัก |
| **database** | `mongodb` | ฐานข้อมูล NoSQL (MongoDB) |
| **messaging** | `redis:alpine` | ระบบ Message Queue / Caching (Redis) |
| **orchestration** | `ansible` | เครื่องมือจัดการ Configuration / Automation |

> 💡 **หมายเหตุ:** Docker images ทั้งหมดจะถูก pull มาจาก **Public Docker Registry (Docker Hub)** โดยอัตโนมัติ หากยังไม่มีใน local machine

---

## 🚀 การใช้งาน

เพียงรันคำสั่งเดียว ทุก services จะเริ่มต้นทำงานพร้อมกัน:

```bash
docker-compose up
```

### คำสั่งที่ใช้บ่อย

```bash
# เริ่มต้นทุก services (foreground)
docker-compose up

# เริ่มต้นทุก services (background / detached mode)
docker-compose up -d

# หยุดทุก services
docker-compose down

# ดู logs ของทุก services
docker-compose logs

# ดูสถานะของ services
docker-compose ps
```

---

## 🔄 เปรียบเทียบ: ก่อน vs หลัง ใช้ Docker Compose

| | ❌ ไม่ใช้ Docker Compose | ✅ ใช้ Docker Compose |
|---|---|---|
| **วิธีรัน** | รัน `docker run` หลายครั้ง | รัน `docker-compose up` ครั้งเดียว |
| **การตั้งค่า** | จำคำสั่งและ options ทั้งหมด | เขียนไว้ในไฟล์ `docker-compose.yml` |
| **Network** | ต้องสร้างและจัดการเอง | สร้าง default network ให้อัตโนมัติ |
| **การจัดการ** | ต้องจัดการแต่ละ container แยกกัน | จัดการทุก services พร้อมกัน |

---

## 📁 โครงสร้างโปรเจกต์ตัวอย่าง

```
my-project/
├── docker-compose.yml      # ไฟล์กำหนด services ทั้งหมด
├── webapp/
│   ├── Dockerfile          # สร้าง image สำหรับ web app
│   └── app.py
└── README.md
```

---

## 📚 สรุป

Docker Compose ช่วยให้เราสามารถ:

1. **กำหนด** ทุก services ไว้ในไฟล์เดียว (`docker-compose.yml`)
2. **จัดการ** multi-container applications ได้ง่าย
3. **เริ่มต้น** ทุกอย่างด้วยคำสั่งเดียว (`docker-compose up`)
4. **สร้าง network** เชื่อมต่อระหว่าง containers โดยอัตโนมัติ
5. **Pull images** จาก Docker Hub (Public Docker Registry) อัตโนมัติ

> 🐋 **"Define and run multi-container applications with ease!"**