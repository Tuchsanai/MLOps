# 🐳 LAB 4: Nginx with Volume & Port Mapping

> เรียนรู้การใช้ Docker เพื่อ deploy เว็บไซต์ด้วย Nginx พร้อม **Port Mapping** และ **Volume Mounting**
> โดยใช้ Google Cloud VM Instance เป็น host

---

## 📋 Overview

ใน LAB นี้ เราจะ:

1. สร้าง VM Instance บน **Google Cloud Platform** และใช้ **External IP** ในการเข้าถึงเว็บไซต์
2. Clone โปรเจกต์จาก GitHub
3. รัน **Nginx Container** พร้อม map port `8083 → 80` และ mount โฟลเดอร์ `web_demo` เป็น volume
4. เข้าถึงเว็บไซต์ผ่าน browser ด้วย `http://<EXTERNAL_IP>:8083`

---

## 🖼️ ตัวอย่างผลลัพธ์ (Screenshots)

| Google Cloud Console — External IP | ผลลัพธ์บน Browser |
|:---:|:---:|
| ![gpc](./gpc.jpg) | ![web](./web.jpg) |
| คัดลอก **External IP** จาก VM Instance | เปิด `http://<EXTERNAL_IP>:8083` บน Browser |

---

## 🚀 ขั้นตอนการทำ LAB

### Step 1: สร้าง Working Directory

```bash
mkdir LAB4_Nginx_Volume_Port_Mapping
cd LAB4_Nginx_Volume_Port_Mapping
```

### Step 2: Clone โปรเจกต์จาก GitHub

```bash
git clone https://github.com/Tuchsanai/MLOps.git
```

จากนั้นเข้าไปยังโฟลเดอร์ LAB:

```bash
cd MLOps/04_Docker_AND_API/01_Docker/LAB2_Nginx_Volume_Port_Mapping
```

### Step 3: รัน Nginx Container ด้วย Port Mapping และ Volume Mounting

```bash
docker run -d -p 8083:80 -v ${PWD}/web_demo:/usr/share/nginx/html:ro nginx
```

**อธิบายคำสั่ง:**

| Flag | ความหมาย |
|------|----------|
| `-d` | รันแบบ detached (background) |
| `-p 8083:80` | Map port **8083** ของ host ไปยัง port **80** ของ container (Nginx) |
| `-v ${PWD}/web_demo:/usr/share/nginx/html:ro` | Mount โฟลเดอร์ `web_demo` เข้าไปเป็น document root ของ Nginx แบบ **read-only** |
| `nginx` | ใช้ official Nginx image จาก Docker Hub |

### Step 4: เข้าถึงเว็บไซต์

เปิด Browser แล้วไปที่:

```
http://<EXTERNAL_IP>:8083
```

> 💡 แทนที่ `<EXTERNAL_IP>` ด้วย External IP ของ VM Instance ที่คัดลอกมาจาก Google Cloud Console
> (ดังตัวอย่างในรูป: `34.142.254.39`)

---

## ✅ ผลลัพธ์ที่คาดหวัง

เมื่อเปิด browser จะเห็นหน้า **"Welcome to Demo nginx Website"** ซึ่งเป็นไฟล์ HTML ที่อยู่ในโฟลเดอร์ `web_demo` ที่ถูก mount เข้าไปใน container

---

## 📝 สิ่งที่ได้เรียนรู้

- **Port Mapping** (`-p`): เชื่อมต่อ port ของ host กับ port ของ container
- **Volume Mounting** (`-v`): แชร์ไฟล์ระหว่าง host กับ container โดยไม่ต้อง rebuild image
- การใช้ **External IP** ของ Google Cloud VM เพื่อเข้าถึง service ที่รันอยู่ใน container