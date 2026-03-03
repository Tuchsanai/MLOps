# Lab: Docker Container Management 🐳

## วัตถุประสงค์ (Objectives)

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. สร้างและตั้งชื่อ Container ด้วย `docker run`
2. ตรวจสอบสถานะของ Container ด้วย `docker ps`
3. หยุด (Stop), ลบ (Remove), และจัดการ Container ได้อย่างถูกต้อง
4. เข้าใจความแตกต่างระหว่าง Running, Stopped, และ Removed Container
5. ใช้คำสั่งจัดการ Container หลายตัวพร้อมกันได้

---

## ความรู้เบื้องต้น (Background)

### Container Lifecycle

Container ใน Docker มี Lifecycle ดังนี้:

```
Created → Running → Stopped → Removed
   ↑         |         |
   └─────────┘         |
     (restart)         ↓
                   (ถูกลบออก)
```

| สถานะ | คำอธิบาย |
|--------|----------|
| **Created** | Container ถูกสร้างแล้วแต่ยังไม่ Start |
| **Running** | Container กำลังทำงานอยู่ |
| **Stopped (Exited)** | Container หยุดทำงานแต่ยังคงอยู่ในระบบ (ข้อมูลยังอยู่) |
| **Removed** | Container ถูกลบออกจากระบบอย่างถาวร |

### คำสั่งสำคัญ (Key Commands Summary)

| คำสั่ง | หน้าที่ |
|--------|---------|
| `docker run` | สร้างและ Start Container ใหม่ |
| `docker ps` | แสดง Container ที่กำลัง Running |
| `docker ps -a` | แสดง Container ทั้งหมด (รวม Stopped) |
| `docker stop` | หยุด Container (Graceful Shutdown) |
| `docker rm` | ลบ Container |
| `docker start` | Start Container ที่ Stopped อยู่ |
| `docker inspect` | แสดงรายละเอียดของ Container |
| `docker logs` | แสดง Log ของ Container |

---

## Part 1: สร้าง Container (Creating Containers)

### Step 1.1 — สร้าง Container 3 ตัว

เราจะสร้าง Container จาก Image ที่แตกต่างกัน โดยตั้งชื่อให้แต่ละตัว:

```bash
docker run -d --name mycontainer1 nginx:latest
docker run -d --name mycontainer2 httpd:latest
docker run -d --name mycontainer3 redis:latest
```

**อธิบายแต่ละ Flag:**

| Flag | ความหมาย |
|------|----------|
| `-d` | Detached mode — รัน Container แบบ Background ไม่ block Terminal |
| `--name` | กำหนดชื่อให้ Container (ถ้าไม่ใส่ Docker จะ Random ชื่อให้) |

**อธิบายแต่ละ Image:**

| Image | คำอธิบาย | Default Port |
|-------|----------|-------------|
| `nginx:latest` | Web Server ยอดนิยม | 80 |
| `httpd:latest` | Apache HTTP Server | 80 |
| `redis:latest` | In-memory Database สำหรับ Caching | 6379 |

> 💡 **หมายเหตุ:** เราเลือกใช้ `httpd` แทน `mysql` เนื่องจาก MySQL ต้องการ Environment Variable (`MYSQL_ROOT_PASSWORD`) จึงจะ Start ได้สำเร็จ ถ้าไม่ใส่ Container จะ Exit ทันที

### Step 1.2 — ตรวจสอบว่า Container ทำงานอยู่

```bash
docker ps
```

**ตัวอย่าง Output:**

```
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS     NAMES
a1b2c3d4e5f6   nginx:latest   "/docker-entrypoint.…"   10 seconds ago   Up 9 seconds    80/tcp    mycontainer1
f6e5d4c3b2a1   httpd:latest   "httpd-foreground"       8 seconds ago    Up 7 seconds    80/tcp    mycontainer2
1a2b3c4d5e6f   redis:latest   "docker-entrypoint.s…"   5 seconds ago    Up 4 seconds    6379/tcp  mycontainer3
```

> 📝 **สังเกต:** แต่ละ Column ให้ข้อมูลสำคัญ:
> - **CONTAINER ID** — ID ย่อ (12 ตัวอักษร) ใช้อ้างอิงแทนชื่อได้
> - **STATUS** — สถานะปัจจุบัน (Up = กำลังทำงาน)
> - **PORTS** — Port ที่ Container เปิดใช้งาน (ยังไม่ได้ Map ออกมา)
> - **NAMES** — ชื่อที่เราตั้งไว้

---

## Part 2: ดู Log และข้อมูลของ Container

### Step 2.1 — ดู Log ของ Container

```bash
docker logs mycontainer1
```

### Step 2.2 — ดู Log แบบ Real-time (Follow)

```bash
docker logs -f mycontainer3
```

กด `Ctrl+C` เพื่อออกจากโหมด Follow

### Step 2.3 — ดูรายละเอียด Container ด้วย inspect

```bash
docker inspect mycontainer1 --format '{{.State.Status}}'
```

ผลลัพธ์จะแสดง: `running`

---

## Part 3: หยุด Container (Stopping Containers)

### Step 3.1 — หยุด Container ตัวเดียว

```bash
docker stop mycontainer1
```

**สิ่งที่เกิดขึ้น:**
1. Docker ส่ง `SIGTERM` signal ไปยัง Process หลักใน Container
2. รอ 10 วินาที (Grace Period) เพื่อให้ Process ปิดตัวเอง
3. ถ้ายังไม่หยุด Docker จะส่ง `SIGKILL` เพื่อบังคับหยุด

### Step 3.2 — ตรวจสอบสถานะหลัง Stop

```bash
docker ps
```

ตอนนี้ `mycontainer1` จะ **ไม่แสดง** เพราะ `docker ps` แสดงเฉพาะ Container ที่ Running

```bash
docker ps -a
```

ตอนนี้จะเห็น `mycontainer1` มี Status เป็น `Exited`

**ตัวอย่าง Output:**

```
CONTAINER ID   IMAGE          STATUS                     NAMES
a1b2c3d4e5f6   nginx:latest   Exited (0) 5 seconds ago   mycontainer1
f6e5d4c3b2a1   httpd:latest   Up 2 minutes               mycontainer2
1a2b3c4d5e6f   redis:latest   Up 2 minutes               mycontainer3
```

### Step 3.3 — Restart Container ที่ Stopped

```bash
docker start mycontainer1
```

ตรวจสอบว่า Container กลับมา Running:

```bash
docker ps
```

---

## Part 4: ลบ Container (Removing Containers)

### Step 4.1 — ลบ Container ที่ Stopped แล้ว

```bash
docker stop mycontainer1
docker rm mycontainer1
```

> ⚠️ **สำคัญ:** ต้อง Stop ก่อน Remove ถ้าพยายามลบ Container ที่ Running อยู่จะเกิด Error

**ลองทดสอบ:**

```bash
docker rm mycontainer2
```

จะเห็น Error:

```
Error response from daemon: cannot remove container "mycontainer2": container is running:
stop the container before removing or force remove
```

### Step 4.2 — Force Remove (ลบโดยไม่ต้อง Stop ก่อน)

```bash
docker rm -f mycontainer2
```

Flag `-f` (force) จะ Stop และ Remove ในขั้นตอนเดียว

### Step 4.3 — ตรวจสอบว่า Container ถูกลบแล้ว

```bash
docker ps -a
```

ตอนนี้ควรเหลือแค่ `mycontainer3`

---

## Part 5: จัดการ Container หลายตัวพร้อมกัน (Bulk Operations)

### Step 5.1 — สร้าง Container ใหม่สำหรับทดสอบ

```bash
docker run -d --name web1 nginx:latest
docker run -d --name web2 nginx:latest
docker run -d --name web3 nginx:latest
docker run -d --name cache1 redis:latest
```

### Step 5.2 — หยุดทุก Container พร้อมกัน

```bash
docker stop $(docker ps -q)
```

**อธิบาย:**
- `docker ps -q` → แสดงเฉพาะ CONTAINER ID ของ Container ที่ Running (Quiet mode)
- `$(...)` → Command Substitution — นำผลลัพธ์มาเป็น Argument ของ `docker stop`

ตรวจสอบ:

```bash
docker ps -a
```

ทุก Container จะมี Status เป็น `Exited`

### Step 5.3 — ลบทุก Container พร้อมกัน

```bash
docker rm $(docker ps -aq)
```

**อธิบาย:**
- `docker ps -aq` → แสดง ID ของ Container **ทั้งหมด** (รวม Stopped)
- ใช้ `-a` เพิ่มเพราะต้องการลบ Container ที่ Stopped ด้วย

### Step 5.4 — ลบทุก Container แบบรวดเร็ว (Force)

ถ้าต้องการ Stop + Remove ทุกตัวในคำสั่งเดียว:

```bash
docker rm -f $(docker ps -aq)
```

### Step 5.5 — ใช้ docker container prune (วิธีที่แนะนำ)

```bash
docker container prune
```

คำสั่งนี้จะลบเฉพาะ **Stopped Container** ทั้งหมด และถามยืนยันก่อนลบ ถือเป็นวิธีที่ปลอดภัยกว่า

เพิ่ม `-f` เพื่อข้ามการยืนยัน:

```bash
docker container prune -f
```

---

## Part 6: เทคนิคเพิ่มเติม (Bonus)

### 6.1 — Filter Container ด้วย `--filter`

```bash
# แสดงเฉพาะ Container ที่มีสถานะ exited
docker ps -a --filter "status=exited"

# แสดงเฉพาะ Container ที่ใช้ image nginx
docker ps -a --filter "ancestor=nginx:latest"

# แสดงเฉพาะ Container ที่ชื่อขึ้นต้นด้วย web
docker ps -a --filter "name=web"
```

### 6.2 — ตั้งค่า Auto-Remove ด้วย `--rm`

```bash
docker run -d --rm --name temp_container nginx:latest
```

เมื่อ Container นี้ Stop ระบบจะลบ Container ออกโดยอัตโนมัติ เหมาะสำหรับงานทดสอบชั่วคราว

### 6.3 — Rename Container

```bash
docker run -d --name old_name nginx:latest
docker rename old_name new_name
docker ps
```

---

## สรุป (Summary)

| การกระทำ | คำสั่ง |
|----------|--------|
| สร้าง Container | `docker run -d --name <name> <image>` |
| ดู Container ที่ Running | `docker ps` |
| ดู Container ทั้งหมด | `docker ps -a` |
| หยุด Container | `docker stop <name>` |
| Start Container ที่หยุดอยู่ | `docker start <name>` |
| ลบ Container (ต้อง Stop ก่อน) | `docker rm <name>` |
| Force ลบ Container | `docker rm -f <name>` |
| หยุดทุก Container | `docker stop $(docker ps -q)` |
| ลบทุก Container | `docker rm -f $(docker ps -aq)` |
| ลบ Stopped Container ทั้งหมด | `docker container prune` |

---