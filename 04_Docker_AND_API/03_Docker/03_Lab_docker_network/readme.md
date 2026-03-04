# Lab: Docker Network with Subnet

## วัตถุประสงค์ของ Lab

Lab นี้จะสอนเกี่ยวกับการจัดการ **Docker Network** ซึ่งเป็นระบบเครือข่ายเสมือน (Virtual Network) ที่ Docker ใช้ในการเชื่อมต่อ Container ต่าง ๆ เข้าด้วยกัน โดยในบทเรียนนี้ นักศึกษาจะได้เรียนรู้:

- การสร้าง Docker Network แบบกำหนด Subnet เอง
- การตรวจสอบรายละเอียดของ Network
- การเชื่อมต่อ Container เข้ากับ Network
- การตรวจสอบ IP Address ของ Container
- การตัดการเชื่อมต่อ (Disconnect) และเชื่อมต่อใหม่ (Reconnect)
- การลบ Network เมื่อไม่ต้องการใช้งานแล้ว

## ความรู้พื้นฐานที่ควรรู้

### Docker Network คืออะไร?

Docker Network คือระบบเครือข่ายเสมือนที่ Docker สร้างขึ้นเพื่อให้ Container สามารถสื่อสารกันได้ เปรียบเสมือนการสร้าง LAN (Local Area Network) ภายใน Docker Engine โดยปกติ Docker จะมี Network เริ่มต้น 3 แบบ:

| ประเภท | คำอธิบาย |
|--------|----------|
| **bridge** | Network เริ่มต้น ใช้สำหรับ Container ที่ทำงานบนเครื่องเดียวกัน |
| **host** | ใช้ Network ของเครื่อง Host โดยตรง ไม่มีการแยก Network |
| **none** | ไม่มี Network เลย Container จะถูกแยกออกจากเครือข่ายทั้งหมด |

### Subnet คืออะไร?

**Subnet (Subnetwork)** คือการแบ่งเครือข่ายใหญ่ออกเป็นเครือข่ายย่อย ๆ เช่น `192.168.100.0/24` หมายความว่า:

- **192.168.100.0** = ที่อยู่เครือข่าย (Network Address)
- **/24** = Subnet Mask (255.255.255.0) หมายความว่ามี IP ที่ใช้งานได้ 254 ตัว ตั้งแต่ `192.168.100.1` ถึง `192.168.100.254`

### BusyBox คืออะไร?

**BusyBox** คือ Docker Image ขนาดเล็กมาก (ประมาณ 1-5 MB) ที่รวมเครื่องมือ Linux พื้นฐานไว้ในไฟล์เดียว เหมาะสำหรับการทดสอบและเรียนรู้เพราะดาวน์โหลดเร็วและใช้ทรัพยากรน้อย

---

## ขั้นตอนการทำ Lab

---

### ขั้นตอนที่ 1: สำรวจ Docker Network ที่มีอยู่ในระบบ

ก่อนสร้าง Network ใหม่ ให้ตรวจสอบว่าในระบบมี Network อะไรอยู่บ้าง

```bash
docker network ls
```

**คำอธิบายคำสั่ง:**
- `docker network ls` — แสดงรายการ Docker Network ทั้งหมดที่มีอยู่ในระบบ

**ผลลัพธ์ที่คาดหวัง:**
```
NETWORK ID     NAME      DRIVER    SCOPE
xxxxxxxxxxxx   bridge    bridge    local
xxxxxxxxxxxx   host      host      local
xxxxxxxxxxxx   none      null      local
```

จะเห็น Network เริ่มต้น 3 ตัว คือ `bridge`, `host`, และ `none` ซึ่ง Docker สร้างให้อัตโนมัติ

---

### ขั้นตอนที่ 2: สร้าง Docker Network ใหม่พร้อมกำหนด Subnet

สร้าง Network ชื่อ `lab_network` พร้อมกำหนด Subnet เป็น `192.168.100.0/24`

```bash
docker network create --subnet 192.168.100.0/24 lab_network
```

**คำอธิบายคำสั่ง:**
- `docker network create` — คำสั่งสร้าง Docker Network ใหม่
- `--subnet 192.168.100.0/24` — กำหนดช่วง IP Address ที่จะใช้ในเครือข่ายนี้ โดยจะมี IP ใช้ได้ตั้งแต่ `192.168.100.1` ถึง `192.168.100.254`
- `lab_network` — ชื่อของ Network ที่จะสร้าง (ตั้งชื่อเองได้)

**ผลลัพธ์ที่คาดหวัง:**

Docker จะแสดง Network ID (เลขยาว ๆ) กลับมา แสดงว่าสร้างสำเร็จ

---

### ขั้นตอนที่ 3: ตรวจสอบรายละเอียดของ Network ที่สร้าง

ใช้คำสั่ง `inspect` เพื่อดูรายละเอียดทั้งหมดของ `lab_network`

```bash
docker network inspect lab_network
```

**คำอธิบายคำสั่ง:**
- `docker network inspect` — แสดงข้อมูลรายละเอียดของ Network ในรูปแบบ JSON
- `lab_network` — ชื่อ Network ที่ต้องการดูข้อมูล

**ผลลัพธ์ที่คาดหวัง:**
```json
[
    {
        "Name": "lab_network",
        "Driver": "bridge",
        "IPAM": {
            "Config": [
                {
                    "Subnet": "192.168.100.0/24"
                }
            ]
        },
        "Containers": {}
    }
]
```

**สิ่งที่ควรสังเกต:**
- `"Subnet": "192.168.100.0/24"` — แสดงว่า Subnet ถูกกำหนดตามที่เราต้องการ
- `"Containers": {}` — ยังไม่มี Container เชื่อมต่ออยู่ (ว่างเปล่า)
- `"Driver": "bridge"` — ใช้ Driver แบบ bridge เป็นค่าเริ่มต้น

---

### ขั้นตอนที่ 4: สร้าง Container และเชื่อมต่อเข้ากับ Network

สร้าง Container จาก BusyBox Image และเชื่อมต่อเข้ากับ `lab_network`

```bash
docker run -d --name busybox_container --network lab_network busybox sleep 360000
```

**คำอธิบายคำสั่ง:**
- `docker run` — สร้างและรัน Container ใหม่
- `-d` — รันแบบ **Detached Mode** (ทำงานอยู่เบื้องหลัง ไม่ยึดหน้า Terminal)
- `--name busybox_container` — ตั้งชื่อ Container ว่า `busybox_container` เพื่อให้อ้างอิงได้ง่าย
- `--network lab_network` — เชื่อมต่อ Container นี้เข้ากับ `lab_network` ที่สร้างไว้ในขั้นตอนที่ 2
- `busybox` — ชื่อ Docker Image ที่ใช้สร้าง Container
- `sleep 360000` — คำสั่งที่ให้ Container ทำงาน คือ "นอนรอ" 360,000 วินาที (ประมาณ 100 ชั่วโมง) เพื่อให้ Container ไม่หยุดทำงานและเราสามารถเข้าไปทดสอบได้

---

### ขั้นตอนที่ 5: ตรวจสอบ IP Address ของ Container

เข้าไปใน Container เพื่อดู IP Address ที่ได้รับจาก `lab_network`

**5.1 เข้าไปใน Container:**

```bash
docker exec -it busybox_container sh
```

**คำอธิบายคำสั่ง:**
- `docker exec` — รันคำสั่งภายใน Container ที่กำลังทำงานอยู่
- `-it` — เปิดโหมด Interactive Terminal (`-i` = interactive, `-t` = allocate pseudo-TTY) เพื่อให้เราพิมพ์คำสั่งได้
- `busybox_container` — ชื่อ Container ที่ต้องการเข้าไป
- `sh` — เปิด Shell (command line) ภายใน Container

**5.2 ตรวจสอบ IP Address:**

เมื่ออยู่ภายใน Container แล้ว ให้พิมพ์คำสั่ง:

```bash
ip addr
```

**คำอธิบายคำสั่ง:**
- `ip addr` — แสดงข้อมูล Network Interface และ IP Address ทั้งหมดของ Container

**ผลลัพธ์ที่คาดหวัง:**

จะเห็น IP Address อยู่ในช่วง `192.168.100.x/24` (เช่น `192.168.100.2/24`) ซึ่งเป็น IP ที่ Docker กำหนดให้จาก Subnet ที่เราตั้งไว้

**5.3 ออกจาก Container:**

```bash
exit
```

คำสั่ง `exit` จะออกจาก Shell ของ Container กลับมาที่ Terminal ของเครื่อง Host

---

### ขั้นตอนที่ 6: ทดสอบ Disconnect และ Reconnect

ในขั้นตอนนี้ เราจะทดสอบการตัดการเชื่อมต่อ Container ออกจาก Network และเชื่อมต่อกลับ

**6.1 ตัดการเชื่อมต่อ Container ออกจาก Network:**

```bash
docker network disconnect lab_network busybox_container
```

**คำอธิบายคำสั่ง:**
- `docker network disconnect` — ตัดการเชื่อมต่อ Container ออกจาก Network
- `lab_network` — ชื่อ Network ที่ต้องการตัดการเชื่อมต่อ
- `busybox_container` — ชื่อ Container ที่ต้องการตัดออก

**6.2 ตรวจสอบว่า Container ถูกตัดออกจาก Network แล้ว:**

```bash
docker network inspect lab_network
```

**สิ่งที่ควรสังเกต:**
- `"Containers": {}` — จะเห็นว่าส่วน Containers ว่างเปล่า แสดงว่าไม่มี Container เชื่อมต่ออยู่แล้ว

**6.3 เชื่อมต่อ Container กลับเข้าสู่ Network:**

```bash
docker network connect lab_network busybox_container
```

**คำอธิบายคำสั่ง:**
- `docker network connect` — เชื่อมต่อ Container เข้ากับ Network
- `lab_network` — ชื่อ Network ที่ต้องการเชื่อมต่อ
- `busybox_container` — ชื่อ Container ที่ต้องการเชื่อมต่อ

**6.4 ตรวจสอบว่า Container เชื่อมต่อกลับสำเร็จ:**

```bash
docker network inspect lab_network
```

**สิ่งที่ควรสังเกต:**
- ส่วน `"Containers"` จะแสดงข้อมูลของ `busybox_container` กลับมา พร้อม IP Address ใหม่ที่ได้รับ (อาจเป็น IP เดิมหรือ IP ใหม่ก็ได้ ขึ้นอยู่กับว่ามี Container อื่นใช้ IP เดิมอยู่หรือไม่)

---

### ขั้นตอนที่ 7: ลบ Network เมื่อไม่ต้องการใช้งานแล้ว

ก่อนลบ Network ต้องตัดการเชื่อมต่อ Container ออกจาก Network ก่อน เพราะ Docker ไม่อนุญาตให้ลบ Network ที่ยังมี Container เชื่อมต่ออยู่

**7.1 ตัดการเชื่อมต่อ Container ออกจาก Network:**

```bash
docker network disconnect lab_network busybox_container
```

**7.2 ลบ Network:**

```bash
docker network rm lab_network
```

**คำอธิบายคำสั่ง:**
- `docker network rm` — ลบ Docker Network
- `lab_network` — ชื่อ Network ที่ต้องการลบ

**หมายเหตุ:** หากยังมี Container เชื่อมต่ออยู่ คำสั่งนี้จะ Error และแจ้งว่าต้อง Disconnect Container ออกก่อน

---

### ขั้นตอนที่ 8: ทำความสะอาดระบบ (Cleanup)

เมื่อทำ Lab เสร็จแล้ว ให้ลบ Container, Image, Volume และ Network ที่ไม่ใช้งานทั้งหมด

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network prune -f
```

**คำอธิบายแต่ละคำสั่ง:**

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `docker stop $(docker ps -a -q)` | หยุดการทำงานของ Container ทั้งหมด โดย `docker ps -a -q` จะแสดง ID ของ Container ทั้งหมด |
| `docker rm $(docker ps -a -q)` | ลบ Container ทั้งหมดที่หยุดทำงานแล้ว |
| `docker rmi $(docker images -q)` | ลบ Docker Image ทั้งหมด โดย `docker images -q` จะแสดง ID ของ Image ทั้งหมด |
| `docker volume rm $(docker volume ls -q)` | ลบ Docker Volume ทั้งหมด |
| `docker network prune -f` | ลบ Network ที่ไม่มี Container ใช้งาน โดย `-f` คือ force (ไม่ถามยืนยัน) |

> **คำเตือน:** คำสั่งเหล่านี้จะลบทรัพยากร Docker **ทั้งหมด** ในเครื่อง ควรใช้ด้วยความระมัดระวัง และตรวจสอบให้แน่ใจว่าไม่มี Container หรือ Image ที่ยังต้องการใช้งานอยู่

---

## สรุปคำสั่งที่ใช้ใน Lab

| คำสั่ง | หน้าที่ |
|--------|---------|
| `docker network ls` | แสดงรายการ Network ทั้งหมด |
| `docker network create --subnet <CIDR> <name>` | สร้าง Network ใหม่พร้อมกำหนด Subnet |
| `docker network inspect <name>` | ดูรายละเอียดของ Network |
| `docker network connect <network> <container>` | เชื่อมต่อ Container เข้ากับ Network |
| `docker network disconnect <network> <container>` | ตัดการเชื่อมต่อ Container ออกจาก Network |
| `docker network rm <name>` | ลบ Network |
| `docker network prune -f` | ลบ Network ที่ไม่ใช้งานทั้งหมด |
| `docker run -d --name <name> --network <network> <image> <cmd>` | สร้างและรัน Container พร้อมเชื่อมต่อ Network |
| `docker exec -it <container> sh` | เข้าไปใช้งาน Shell ภายใน Container |
