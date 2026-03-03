# Docker CMD vs ENTRYPOINT

## วัตถุประสงค์ของบทเรียน


บทเรียนนี้จะช่วยให้นักศึกษาเข้าใจ:

- คำสั่ง `CMD` และ `ENTRYPOINT` ใน Dockerfile คืออะไร และต่างกันอย่างไร
- พฤติกรรมของแต่ละคำสั่งเมื่อใช้แยกกัน และเมื่อใช้ร่วมกัน
- วิธี Override (แทนที่) พฤติกรรม default ของ Container
- แนวทางปฏิบัติที่ดี (Best Practices) ในการเลือกใช้งาน

---

## ความรู้พื้นฐาน: Container ทำงานอย่างไร?

เมื่อเรา `docker run` สิ่งที่เกิดขึ้นคือ Docker จะสร้าง Container จาก Image แล้ว **รันคำสั่ง (process) หนึ่งคำสั่ง** ภายใน Container นั้น

คำถามคือ: **คำสั่งนั้นถูกกำหนดจากที่ไหน?**

คำตอบคือ: จาก `CMD` และ/หรือ `ENTRYPOINT` ที่เราเขียนไว้ใน Dockerfile

---

## 1. CMD — คำสั่ง Default ที่ถูก Override ได้ทั้งหมด

### แนวคิด

`CMD` ใช้กำหนด **คำสั่ง default** ที่จะรันเมื่อ Container เริ่มทำงาน
แต่สิ่งสำคัญคือ: **`CMD` จะถูกแทนที่ (override) ทั้งหมด** หากผู้ใช้ระบุคำสั่งเองตอน `docker run`

### รูปแบบการเขียน (Syntax)

```dockerfile
# Exec Form (แนะนำ) — ใช้ JSON array
CMD ["executable", "param1", "param2"]

# Shell Form — รันผ่าน /bin/sh -c
CMD command param1 param2
```

> **Exec Form vs Shell Form:**
> - **Exec Form** `["echo", "hello"]` — รัน process โดยตรง ไม่ผ่าน shell, เป็น PID 1, รับ signal ได้ถูกต้อง
> - **Shell Form** `echo hello` — รันผ่าน `/bin/sh -c`, shell เป็น PID 1, process จริงเป็น child process

### ไฟล์ตัวอย่าง: `Dockerfile-CMD`

```dockerfile
FROM ubuntu
CMD ["echo", "Hello from CMD!"]
```

### ขั้นตอนทดลอง

**Step 1: Build Image**
```bash
docker build -t cmd-example -f Dockerfile-CMD .
```

**Step 2: Run แบบไม่ใส่ argument (ใช้ค่า default จาก CMD)**
```bash
docker run cmd-example
```
**Output:**
```
Hello from CMD!
```
> Container รันคำสั่ง `echo "Hello from CMD!"` ตามที่ `CMD` กำหนดไว้

**Step 3: Run แบบใส่ argument (Override CMD ทั้งหมด)**
```bash
docker run cmd-example echo "CMD with custom message"
```
**Output:**
```
CMD with custom message
```
> คำสั่ง `echo "CMD with custom message"` ที่ใส่ตอน `docker run` ได้ **แทนที่ CMD เดิมทั้งหมด**

**Step 4: ทดลอง Override ด้วยคำสั่งอื่นที่ไม่ใช่ echo**
```bash
docker run cmd-example ls /
```
**Output:**
```
bin  boot  dev  etc  home  lib  ...
```
> `CMD` ถูก override ด้วย `ls /` ทั้งหมด — แสดงว่า CMD ไม่ได้ lock executable ไว้

### สรุป CMD

| สถานการณ์ | คำสั่งที่รันจริง |
|---|---|
| `docker run cmd-example` | `echo "Hello from CMD!"` |
| `docker run cmd-example echo "Custom"` | `echo "Custom"` (CMD ถูก override) |
| `docker run cmd-example ls /` | `ls /` (CMD ถูก override ด้วยคำสั่งอื่น) |

---

## 2. ENTRYPOINT — คำสั่งที่ตายตัว (Fixed Executable)

### แนวคิด

`ENTRYPOINT` ใช้กำหนด **executable ที่ตายตัว** ของ Container
เมื่อผู้ใช้ใส่ argument ตอน `docker run` argument เหล่านั้นจะถูก **ต่อท้าย (append)** หลัง ENTRYPOINT ไม่ใช่แทนที่

### รูปแบบการเขียน (Syntax)

```dockerfile
# Exec Form (แนะนำ)
ENTRYPOINT ["executable", "param1", "param2"]

# Shell Form
ENTRYPOINT command param1 param2
```

### ไฟล์ตัวอย่าง: `Dockerfile-ENTRYPOINT`

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo", "Hello from ENTRYPOINT!"]
```

### ขั้นตอนทดลอง

**Step 1: Build Image**
```bash
docker build -t entrypoint-example -f Dockerfile-ENTRYPOINT .
```

**Step 2: Run แบบไม่ใส่ argument**
```bash
docker run entrypoint-example
```
**Output:**
```
Hello from ENTRYPOINT!
```

**Step 3: Run แบบใส่ argument (Argument จะถูกต่อท้าย)**
```bash
docker run entrypoint-example "ENTRYPOINT with custom message"
```
**Output:**
```
Hello from ENTRYPOINT! ENTRYPOINT with custom message
```
> สังเกตว่า argument ใหม่ถูก **ต่อท้าย** หลัง ENTRYPOINT เดิม ไม่ได้แทนที่
> คำสั่งจริงที่รันคือ: `echo "Hello from ENTRYPOINT!" "ENTRYPOINT with custom message"`

### สรุป ENTRYPOINT

| สถานการณ์ | คำสั่งที่รันจริง |
|---|---|
| `docker run entrypoint-example` | `echo "Hello from ENTRYPOINT!"` |
| `docker run entrypoint-example "Custom"` | `echo "Hello from ENTRYPOINT!" "Custom"` (ต่อท้าย) |

---

## 3. CMD + ENTRYPOINT — ใช้ร่วมกัน (Best Practice)

### แนวคิด

เมื่อใช้ `ENTRYPOINT` และ `CMD` ร่วมกัน:

- **`ENTRYPOINT`** กำหนด executable ที่ตายตัว (เปลี่ยนไม่ได้ง่ายๆ)
- **`CMD`** กำหนด **default arguments** ให้กับ ENTRYPOINT (เปลี่ยนได้ง่ายตอน run)

นี่คือ **Pattern ที่แนะนำ** เพราะให้ความยืดหยุ่นสูงสุด

### ไฟล์ตัวอย่าง: `Dockerfile-CMD-ENTRYPOINT`

```dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
CMD ["Hello from both CMD and ENTRYPOINT!"]
```

### ขั้นตอนทดลอง

**Step 1: Build Image**
```bash
docker build -t cmd-entrypoint-example -f Dockerfile-CMD-ENTRYPOINT .
```

**Step 2: Run แบบไม่ใส่ argument (ใช้ CMD เป็น default argument)**
```bash
docker run cmd-entrypoint-example
```
**Output:**
```
Hello from both CMD and ENTRYPOINT!
```
> Docker รัน: `ENTRYPOINT + CMD` = `echo "Hello from both CMD and ENTRYPOINT!"`

**Step 3: Run แบบใส่ argument (Override เฉพาะ CMD)**
```bash
docker run cmd-entrypoint-example "Custom message with both CMD and ENTRYPOINT"
```
**Output:**
```
Custom message with both CMD and ENTRYPOINT
```
> Docker รัน: `ENTRYPOINT + user args` = `echo "Custom message with both CMD and ENTRYPOINT"`
> **เฉพาะส่วน CMD ถูก override** ตัว ENTRYPOINT (`echo`) ยังคงอยู่

### สรุป CMD + ENTRYPOINT

| สถานการณ์ | ENTRYPOINT | CMD / Args | คำสั่งที่รันจริง |
|---|---|---|---|
| ไม่ใส่ argument | `echo` | `"Hello from both..."` (default) | `echo "Hello from both..."` |
| ใส่ argument | `echo` | `"Custom message"` (override) | `echo "Custom message"` |

---

## 4. ตารางเปรียบเทียบ CMD vs ENTRYPOINT

| คุณสมบัติ | `CMD` | `ENTRYPOINT` |
|---|---|---|
| **หน้าที่** | กำหนด default command/arguments | กำหนด fixed executable |
| **Override ตอน `docker run`** | ถูก override **ทั้งหมด** | argument ถูก **ต่อท้าย** |
| **เปลี่ยน executable ได้ไหม** | ได้ (ถูก override ทั้งคำสั่ง) | ไม่ได้ (ต้องใช้ `--entrypoint` flag) |
| **ใช้ร่วมกัน** | เป็น default arguments ให้ ENTRYPOINT | เป็น fixed executable |
| **เหมาะกับ** | Container ที่ต้องการความยืดหยุ่นสูง | Container ที่ต้องการ lock executable ไว้ |

---

## 5. แผนภาพการทำงาน (Flow)

```
docker run <image> [user_args]
        │
        ▼
   มี user_args ไหม?
        │
   ┌────┴────┐
   │ ไม่มี    │ มี
   ▼         ▼
  ┌──────────────────────────────┐
  │  มี ENTRYPOINT ไหม?         │
  │                              │
  │  ไม่มี:                      │
  │    รัน CMD ทั้งหมด            │  ← docker run cmd-example
  │    หรือ user_args ทั้งหมด     │  ← docker run cmd-example ls /
  │                              │
  │  มี:                         │
  │    ไม่มี user_args:           │
  │      รัน ENTRYPOINT + CMD    │  ← docker run cmd-entrypoint-example
  │                              │
  │    มี user_args:             │
  │      รัน ENTRYPOINT + args   │  ← docker run cmd-entrypoint-example "Hi"
  │      (CMD ถูก override)      │
  └──────────────────────────────┘
```

---

## 6. Use Case ในงาน MLOps จริง

### ตัวอย่าง: สร้าง Container สำหรับ Inference ML Model

```dockerfile
FROM python:3.11-slim

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy โค้ด
COPY app/ /app/
WORKDIR /app

# ENTRYPOINT = executable ตายตัว (python)
# CMD = default script ที่เปลี่ยนได้
ENTRYPOINT ["python"]
CMD ["serve.py"]
```

**การใช้งาน:**
```bash
# รัน default: python serve.py
docker run ml-model

# เปลี่ยนไปรัน training แทน: python train.py
docker run ml-model train.py

# รัน evaluation: python evaluate.py --data test.csv
docker run ml-model evaluate.py --data test.csv
```

> ENTRYPOINT lock ไว้ว่าต้องรัน `python` เสมอ
> CMD กำหนด default เป็น `serve.py` แต่เปลี่ยนเป็น script อื่นได้ตอน run

---

### ตัวอย่าง: Container สำหรับ API Server

```dockerfile
FROM python:3.11-slim

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
CMD ["--port", "8000"]
```

**การใช้งาน:**
```bash
# รัน default ที่ port 8000
docker run api-server

# เปลี่ยน port เป็น 9000
docker run api-server --port 9000
```

---

## 7. วิธี Override ENTRYPOINT ตอน Runtime

ในกรณีที่ต้องการ override ENTRYPOINT จริงๆ สามารถใช้ flag `--entrypoint`:

```bash
# override ENTRYPOINT เพื่อเข้า shell แทน
docker run --entrypoint /bin/bash entrypoint-example

# override ENTRYPOINT เพื่อรันคำสั่งอื่น
docker run --entrypoint ls entrypoint-example /app
```

> ควรใช้เฉพาะกรณี debug เท่านั้น ไม่ควรใช้ในงาน production

---

## 8. ข้อควรระวังและ Best Practices

| หัวข้อ | คำแนะนำ |
|---|---|
| **ใช้ Exec Form เสมอ** | เขียนเป็น `["cmd", "arg"]` ไม่ใช่ `cmd arg` เพื่อให้ process เป็น PID 1 และรับ signal ได้ถูกต้อง |
| **CMD มีได้แค่ 1 ตัว** | ถ้าเขียน `CMD` หลายบรรทัด จะใช้แค่ **ตัวสุดท้าย** เท่านั้น |
| **ENTRYPOINT มีได้แค่ 1 ตัว** | เช่นเดียวกับ CMD ถ้าเขียนหลายบรรทัด ใช้แค่ตัวสุดท้าย |
| **ใช้ร่วมกันเป็น Best Practice** | `ENTRYPOINT` = executable, `CMD` = default arguments |
| **Shell Form กับ ENTRYPOINT** | หลีกเลี่ยง Shell Form กับ ENTRYPOINT เพราะจะทำให้ `CMD` และ user args ไม่ทำงาน |

---

## 9. แบบฝึกหัด

1. **สร้าง Dockerfile** ที่ใช้ `ENTRYPOINT` เป็น `curl` และ `CMD` เป็น `https://google.com` จากนั้นทดลอง override URL ตอน `docker run`

2. **อธิบายผลลัพธ์** ของคำสั่งต่อไปนี้:
   ```bash
   # Dockerfile:
   # FROM ubuntu
   # ENTRYPOINT ["echo", "A"]
   # CMD ["B", "C"]

   docker run myimage         # Output = ?
   docker run myimage D E     # Output = ?
   ```

3. **จงเปรียบเทียบ** ว่าถ้าใช้ Shell Form กับ ENTRYPOINT จะเกิดอะไรขึ้น:
   ```dockerfile
   # แบบ A (Exec Form)
   ENTRYPOINT ["echo", "hello"]
   CMD ["world"]

   # แบบ B (Shell Form)
   ENTRYPOINT echo hello
   CMD ["world"]
   ```

---

## Lab Setup

### Prerequisites
- Docker installed on your machine

### Clone Repository

```bash
git clone https://github.com/Tuchsanai/MLOps.git
cd MLOps/04_Docker_AND_API/03_Docker/01_LAB_CMD_Entrypoint/
```

### Quick Start — รันทุก Lab ต่อเนื่อง

```bash
# Lab 1: CMD
docker build -t cmd-example -f Dockerfile-CMD .
docker run cmd-example
docker run cmd-example echo "CMD with custom message"

# Lab 2: ENTRYPOINT
docker build -t entrypoint-example -f Dockerfile-ENTRYPOINT .
docker run entrypoint-example
docker run entrypoint-example "ENTRYPOINT with custom message"

# Lab 3: CMD + ENTRYPOINT
docker build -t cmd-entrypoint-example -f Dockerfile-CMD-ENTRYPOINT .
docker run cmd-entrypoint-example
docker run cmd-entrypoint-example "Custom message with both CMD and ENTRYPOINT"
```
