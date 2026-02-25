# LAB 3: Docker - Node.js Bulletin Board Application

## Overview

LAB นี้เป็นการฝึกปฏิบัติการใช้ **Docker** ในการ containerize แอปพลิเคชัน **Node.js Bulletin Board** ซึ่งเป็นเว็บแอปพลิเคชันสำหรับจัดการกระดานข่าวกิจกรรม (Event Bulletin Board) โดยผู้เรียนจะได้เรียนรู้การเขียน Dockerfile, การ build Docker Image และการ run Docker Container

![Demo](./demo3.jpg)

---

## Learning Objectives

- เข้าใจโครงสร้างของ Dockerfile และคำสั่งพื้นฐาน (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`)
- สามารถ build Docker Image จาก Dockerfile ได้
- สามารถ run Docker Container พร้อม port mapping ได้
- เข้าใจการทำงานร่วมกันระหว่าง Docker กับ Node.js Application

---

## Tech Stack

| Component   | Technology             |
|-------------|------------------------|
| Backend     | Node.js + Express      |
| Frontend    | Vue.js + Bootstrap     |
| Template    | EJS                    |
| Container   | Docker                 |
| Port        | 8080 (container)       |

---

## Project Structure

```
LAB3_node-bulletin-board-master/
├── readme.md
├── demo3.jpg
├── LICENSE
└── bulletin-board-app/
    ├── Dockerfile           # Docker configuration
    ├── package.json         # Node.js dependencies
    ├── server.js            # Express server (port 8080)
    ├── app.js               # Vue.js frontend logic
    ├── index.html           # Main HTML page
    ├── site.css             # Custom styles
    ├── LICENSE
    └── backend/
        ├── index.js         # Route handler (render index)
        ├── api.js           # REST API endpoints
        └── events.js        # Sample event data
```

---

## Application Features

แอปพลิเคชัน Bulletin Board มีความสามารถดังนี้:

- **เพิ่มกิจกรรม (Add Event):** กรอก Title, Detail และ Date แล้วกดปุ่ม Submit
- **แสดงรายการกิจกรรม (View Events):** แสดงรายการกิจกรรมทั้งหมดทางด้านขวา
- **ลบกิจกรรม (Delete Event):** กดปุ่ม Delete เพื่อลบกิจกรรมที่ไม่ต้องการ

### API Endpoints

| Method   | Endpoint              | Description          |
|----------|-----------------------|----------------------|
| `GET`    | `/`                   | แสดงหน้าเว็บหลัก      |
| `GET`    | `/api/events`         | ดึงรายการกิจกรรมทั้งหมด |
| `POST`   | `/api/events`         | เพิ่มกิจกรรมใหม่       |
| `DELETE` | `/api/events/:eventId`| ลบกิจกรรมตาม ID      |

---

## Dockerfile Explained

```dockerfile
FROM node:current-slim        # ใช้ Node.js image ขนาดเล็ก

WORKDIR /usr/src/app           # กำหนด working directory ภายใน container
COPY package.json .            # คัดลอก package.json เข้า container
RUN npm install                # ติดตั้ง dependencies

EXPOSE 8080                    # เปิด port 8080
CMD [ "npm", "start" ]         # คำสั่งเริ่มต้นเมื่อ run container

COPY . .                       # คัดลอกไฟล์ทั้งหมดเข้า container
```

> **หมายเหตุ:** การ `COPY package.json` ก่อนแล้วค่อย `RUN npm install` เป็นเทคนิค **Docker layer caching** ช่วยให้ไม่ต้อง install dependencies ใหม่ทุกครั้งที่ code เปลี่ยนแปลง

---

## Lab Instructions

### Step 1: Clone Repository

```bash
git clone https://github.com/Tuchsanai/MLOps.git
```

### Step 2: Navigate to Project Directory

```bash
cd MLOps/04_Docker_AND_API/01_Docker/LAB3_node-bulletin-board-master/bulletin-board-app
```

### Step 3: Build Docker Image

```bash
docker build -t bulletinboard:1.0 .
```

- `-t bulletinboard:1.0` : ตั้งชื่อ image เป็น `bulletinboard` พร้อม tag `1.0`
- `.` : ใช้ Dockerfile จาก directory ปัจจุบัน

### Step 4: Run Docker Container

```bash
docker run -p 8085:8080 -d --name bb bulletinboard:1.0
```

| Flag            | Description                                          |
|-----------------|------------------------------------------------------|
| `-p 8085:8080`  | Map port 8085 ของ host ไปยัง port 8080 ของ container  |
| `-d`            | Run container แบบ detached (background)              |
| `--name bb`     | ตั้งชื่อ container เป็น `bb`                           |

### Step 5: Access the Application

เปิดเว็บเบราว์เซอร์แล้วไปที่:

```
http://localhost:8085
```

---

## Useful Docker Commands

```bash
# ดู container ที่กำลังทำงาน
docker ps

# ดู logs ของ container
docker logs bb

# หยุด container
docker stop bb

# ลบ container
docker rm bb

# ลบ image
docker rmi bulletinboard:1.0
```

---

## License

Apache License 2.0