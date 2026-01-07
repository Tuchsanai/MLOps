# 🔄 Lab: Git Restore ใน MLOps Application

## 📚 ภาพรวมของ Lab

Lab นี้จะสอนการใช้คำสั่ง `git restore` ในบริบทของการพัฒนา Machine Learning Pipeline โดยจำลองสถานการณ์จริงที่เกิดขึ้นระหว่างการทำงาน เช่น การแก้ไขโค้ดผิดพลาด การทดลองที่ไม่สำเร็จ และการต้องการย้อนกลับไปใช้เวอร์ชันก่อนหน้า

---

## 🎯 วัตถุประสงค์การเรียนรู้

เมื่อจบ Lab นี้ นักศึกษาจะสามารถ:

1. เข้าใจแนวคิดและความสำคัญของ `git restore` ใน MLOps workflow
2. ใช้ `git restore` เพื่อยกเลิกการเปลี่ยนแปลงไฟล์ใน Working Directory
3. ใช้ `git restore --staged` เพื่อยกเลิกไฟล์ที่อยู่ใน Staging Area
4. ใช้ `git restore --source` เพื่อกู้คืนไฟล์จาก commit เฉพาะ
5. ประยุกต์ใช้ `git restore` ในสถานการณ์จริงของการพัฒนา ML Pipeline

---

## 📖 ทฤษฎี: Git Restore คืออะไร?

### 🔑 แนวคิดหลัก

ลองนึกภาพว่าคุณกำลังเขียนรายงานด้วย Microsoft Word ถ้าคุณพิมพ์ผิดหรือลบข้อความไปโดยไม่ตั้งใจ คุณจะกด **Ctrl+Z** เพื่อย้อนกลับ ใช่ไหม?

`git restore` ก็ทำหน้าที่คล้ายๆ กัน แต่ทรงพลังกว่ามาก เพราะมันสามารถย้อนกลับไปหาเวอร์ชันใดก็ได้ในประวัติการทำงานของคุณ ไม่ใช่แค่ขั้นตอนก่อนหน้า

### 📜 ความเป็นมา

ก่อนหน้านี้ Git ใช้คำสั่ง `git checkout` ทำหลายอย่างพร้อมกัน ทั้งสลับ branch และกู้คืนไฟล์ ซึ่งทำให้สับสน ในเดือนสิงหาคม 2019 (Git 2.23) จึงแยกออกมาเป็น 2 คำสั่งที่ชัดเจน:

| คำสั่งเดิม | คำสั่งใหม่ | หน้าที่ |
|-----------|-----------|---------|
| `git checkout <branch>` | `git switch <branch>` | สลับ branch |
| `git checkout -- <file>` | `git restore <file>` | กู้คืนไฟล์ |

### 🏠 ทำความเข้าใจ "บ้าน" ของ Git (Git Areas)

ก่อนจะใช้ `git restore` ได้อย่างมั่นใจ คุณต้องเข้าใจว่า Git แบ่งพื้นที่ทำงานออกเป็น 3 ส่วน เปรียบเหมือน "บ้าน" ที่มี 3 ห้อง:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      🏠 บ้านของ Git (Git Areas)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐ │
│  │  🛠️ ห้องทำงาน      │   │  📦 ห้องจัดเตรียม   │   │  🏛️ ห้องเก็บของถาวร │ │
│  │  (Working         │   │  (Staging Area    │   │  (Repository)     │ │
│  │   Directory)      │   │   / Index)        │   │                   │ │
│  │                   │   │                   │   │                   │ │
│  │  • ไฟล์ที่คุณ      │   │  • ไฟล์ที่เลือกแล้ว │   │  • ประวัติที่บันทึก  │ │
│  │    กำลังแก้ไข      │   │    ว่าจะ commit   │   │    ถาวรแล้ว        │ │
│  │  • ยังไม่ได้เลือก   │   │  • รอการ commit   │   │  • กู้คืนได้เสมอ    │ │
│  │    ว่าจะเก็บ       │   │                   │   │                   │ │
│  └───────────────────┘   └───────────────────┘   └───────────────────┘ │
│           │                       │                       │            │
│           │    git add ───────▶   │    git commit ─────▶  │            │
│           │                       │                       │            │
│           │   ◀─── git restore    │  ◀── git restore      │            │
│           │        --staged       │      --source         │            │
│           │                       │                       │            │
│           └───────────────────────┴───────────────────────┘            │
│                            ▲                                           │
│                            │                                           │
│                   git restore (กู้คืนจาก commit ล่าสุด)                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**อธิบายแต่ละห้อง:**

| ห้อง | ชื่อภาษาอังกฤษ | คำอธิบาย | เปรียบเทียบ |
|------|---------------|----------|------------|
| 🛠️ ห้องทำงาน | Working Directory | ไฟล์ที่คุณเห็นและแก้ไขได้ในโฟลเดอร์โปรเจกต์ | โต๊ะทำงานที่มีเอกสารกระจัดกระจาย |
| 📦 ห้องจัดเตรียม | Staging Area (Index) | ไฟล์ที่คุณเลือกแล้วว่าจะ commit ในรอบถัดไป | กล่องที่ใส่เอกสารที่จัดเรียบร้อยแล้ว รอส่งไปเก็บ |
| 🏛️ ห้องเก็บของถาวร | Repository | ประวัติ commit ทั้งหมด เก็บถาวรอย่างปลอดภัย | ตู้เซฟเก็บเอกสารสำคัญ ล็อคกุญแจไว้ |

### 🎮 คำสั่ง git restore ที่สำคัญ

| คำสั่ง | ทำอะไร | เมื่อไหร่ใช้ |
|--------|--------|------------|
| `git restore <file>` | ยกเลิกการแก้ไขใน Working Directory | เมื่อแก้ไขผิด ยังไม่ได้ `git add` |
| `git restore --staged <file>` | เอาไฟล์ออกจาก Staging Area | เมื่อ `git add` ไปแล้ว แต่ยังไม่อยาก commit |
| `git restore --source=<commit> <file>` | กู้คืนไฟล์จาก commit ที่ระบุ | เมื่อต้องการเวอร์ชันเก่าจากประวัติ |
| `git restore .` | ยกเลิกการแก้ไขทุกไฟล์ | เมื่อทุกอย่างพังหมด ต้องการเริ่มใหม่ |

### 🤖 ทำไม Git Restore ถึงสำคัญใน MLOps?

ในการพัฒนา Machine Learning เราทำการทดลองบ่อยมาก และบ่อยครั้งที่ผลลัพธ์ไม่เป็นไปตามที่หวัง:

| สถานการณ์ | ปัญหาที่เกิด | วิธีแก้ด้วย git restore |
|-----------|-------------|------------------------|
| ปรับ hyperparameters | Accuracy ลดลง | กู้คืนค่า parameters เดิม |
| เปลี่ยน preprocessing | Data pipeline พัง | ย้อนกลับไปใช้โค้ดเดิม |
| ลอง model architecture ใหม่ | Training ช้าลง 10 เท่า | กู้คืน model เดิม |
| แก้ไข evaluation metrics | ผลลัพธ์คำนวณผิด | กลับไปใช้สูตรที่ถูกต้อง |

**ข้อดีของการใช้ git restore:**
- ⚡ กู้คืนได้ทันที ไม่ต้อง copy-paste จากที่อื่น
- 🛡️ ปลอดภัย ไม่มีทางทำให้ประวัติ commit เสียหาย
- 🎯 เลือกกู้คืนเฉพาะไฟล์ที่ต้องการได้

---

## 🎬 สถานการณ์จำลอง: เรื่องราวของ Lab นี้

### 📋 บทบาทของคุณ

คุณคือ **ML Engineer** ที่เพิ่งเข้าทำงานที่บริษัท DataTech ได้ 1 เดือน หัวหน้าทีมมอบหมายให้คุณพัฒนา **Classification Pipeline** สำหรับจำแนกพันธุ์ดอกไอริส (Iris) ซึ่งเป็นโปรเจกต์ฝึกหัดก่อนจะได้ทำโปรเจกต์จริง

### 🎯 เป้าหมายของโปรเจกต์

สร้าง ML Pipeline ที่ประกอบด้วย 3 ส่วนหลัก:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  📊 data_prep   │───▶│  🤖 train       │───▶│  📈 evaluate    │
│                 │    │                 │    │                 │
│  โหลด & เตรียม   │    │  Train โมเดล    │    │  วัดผล & รายงาน │
│  ข้อมูล         │    │  Random Forest  │    │  Accuracy, F1   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📅 ไทม์ไลน์ของเหตุการณ์: สัปดาห์แรกของ ML Engineer

### 🗓️ วันศุกร์ก่อนหน้า - รับมอบหมายโปรเจกต์

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏢 ห้องประชุมทีม ML - 15:00 น.                                         │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  👨‍💼 หัวหน้าทีม: "ยินดีต้อนรับ! เรามีโปรเจกต์ฝึกหัดให้คุณ"              │
│                                                                        │
│  📋 รายละเอียดโปรเจกต์:                                                 │
│  ├── ชื่อ: Iris Classification Pipeline                                │
│  ├── Dataset: Iris (150 samples, 3 classes)                           │
│  ├── เป้าหมาย: สร้าง Pipeline ครบวงจร                                   │
│  └── กำหนดส่ง: วันศุกร์หน้า (7 วัน)                                      │
│                                                                        │
│  💭 ความรู้สึก: ตื่นเต้น พร้อมลุย!                                       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 🗓️ วันเสาร์-อาทิตย์ - เตรียมตัวและวางแผน

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏠 บ้าน - วันหยุดสุดสัปดาห์                                            │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  📚 สิ่งที่ทำ:                                                          │
│  ├── ศึกษา requirements และวางแผนการทำงาน                               │
│  ├── ออกแบบโครงสร้าง: data_prep.py → train.py → evaluate.py            │
│  ├── ศึกษา Iris Dataset                                                │
│  └── ตั้งค่า Git และ Virtual Environment                               │
│                                                                        │
│  📝 แผนการทำงานสัปดาห์หน้า:                                             │
│  ├── จันทร์: สร้าง Pipeline ทั้ง 3 ไฟล์                                 │
│  ├── อังคาร: เพิ่ม Feature Engineering                                 │
│  ├── พุธ: ปรับปรุงและ Refactor                                         │
│  ├── พฤหัส: ทดสอบและแก้ไข                                              │
│  └── ศุกร์: ส่งงาน                                                      │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🗓️ วันจันทร์ (Day 1) - สร้าง Pipeline & เกิดปัญหาแรก

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📆 วันจันทร์ - สร้าง ML Pipeline                                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⏰ 09:00 - เริ่มทำงาน                                                      │
│  ├── ☕ ดื่มกาแฟ เปิด VS Code                                               │
│  ├── 📂 cd ~/mlops-git-restore-lab                                         │
│  └── 💻 เริ่มเขียน data_prep.py                                            │
│                                                                            │
│  ⏰ 10:30 - Commit #1: Data Preparation ✅                                  │
│  ├── git add data_prep.py                                                  │
│  └── git commit -m "feat: add data preparation module"                     │
│                                                                            │
│  ⏰ 11:00 - พักเบรก 🍵                                                      │
│                                                                            │
│  ⏰ 11:30 - กลับมาทำงาน                                                     │
│  └── 💻 เริ่มเขียน train.py                                                │
│                                                                            │
│  ⏰ 13:00 - Commit #2: Model Training ✅                                    │
│  ├── git add train.py                                                      │
│  └── git commit -m "feat: add model training module"                       │
│                                                                            │
│  ⏰ 13:30 - พักกลางวัน 🍜                                                   │
│                                                                            │
│  ⏰ 14:30 - กลับมาทำงาน                                                     │
│  └── 💻 เริ่มเขียน evaluate.py                                             │
│                                                                            │
│  ⏰ 16:00 - Commit #3: Model Evaluation ✅                                  │
│  ├── git add evaluate.py                                                   │
│  └── git commit -m "feat: add model evaluation module"                     │
│                                                                            │
│  ⏰ 16:30 - ทดสอบ Pipeline                                                  │
│  ├── 🎉 ทุกอย่างทำงานได้!                                                  │
│  └── 📊 Accuracy: 96.67%                                                   │
│                                                                            │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⏰ 17:00 - 🆘 สถานการณ์ที่ 1 เกิดขึ้น!                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                            │
│  💭 "ลองเปลี่ยน hyperparameters ดูดีกว่า"                                   │
│                                                                            │
│  ✏️ แก้ไข train.py:                                                        │
│  ├── ตั้งใจจะเปลี่ยน n_estimators=200                                      │
│  ├── แต่พิมพ์ผิด: n_estimators=-999                                        │
│  └── และ: max_depth="invalid"                                              │
│                                                                            │
│  ⏰ 17:10 - ลองรันโค้ด                                                      │
│  ├── python train.py                                                       │
│  └── ❌ ERROR! ValueError: Invalid parameter value                         │
│                                                                            │
│  😰 "โค้ดพังหมดแล้ว! ทำไงดี?"                                               │
│                                                                            │
│  ⏰ 17:15 - 💡 นึกได้! ยังไม่ได้ commit ที่แก้ไข!                           │
│  ├── git status → modified: train.py                                       │
│  ├── 💡 "ใช้ git restore ได้!"                                             │
│  ├── ✅ git restore train.py                                               │
│  └── 🎉 โค้ดกลับมาใช้งานได้!                                               │
│                                                                            │
│  ⏰ 17:30 - เลิกงาน 🏠                                                      │
│  └── 📝 บทเรียนวันนี้: git restore ช่วยกู้คืนจากความผิดพลาดได้             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### 🗓️ วันอังคาร (Day 2) - Feature Engineering & Add ผิดไฟล์

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📆 วันอังคาร - Feature Engineering                                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⏰ 09:00 - เริ่มทำงาน                                                      │
│  ├── 💭 "วันนี้จะเพิ่ม feature engineering"                                 │
│  └── 📝 แผน: แก้ไข data_prep.py และ evaluate.py                            │
│                                                                            │
│  ⏰ 10:00 - แก้ไขไฟล์                                                       │
│  ├── ✏️ data_prep.py: เพิ่ม add_features() function                        │
│  │   ├── sepal_ratio = sepal_length / sepal_width                         │
│  │   ├── petal_ratio = petal_length / petal_width                         │
│  │   ├── sepal_area = sepal_length * sepal_width                          │
│  │   └── petal_area = petal_length * petal_width                          │
│  │                                                                         │
│  └── ✏️ evaluate.py: เพิ่ม experimental features                           │
│      ├── timestamp tracking                                                │
│      ├── save_metrics_to_file()                                            │
│      └── ⚠️ ยังไม่ได้ทดสอบ!                                                │
│                                                                            │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⏰ 11:00 - 🆘 สถานการณ์ที่ 2 เกิดขึ้น!                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                            │
│  💨 รีบทำ ใช้ git add . โดยไม่ได้คิด                                        │
│                                                                            │
│  📋 git status:                                                            │
│  ├── Changes to be committed:                                              │
│  │   ├── modified: data_prep.py  ✅ พร้อม                                  │
│  │   └── modified: evaluate.py   ⚠️ ยังไม่พร้อม!                           │
│                                                                            │
│  😬 "เดี๋ยว! evaluate.py มี experimental code ยังไม่ได้ทดสอบ!"             │
│  💭 "ถ้า commit ไปอาจทำให้ production พัง"                                  │
│                                                                            │
│  ⏰ 11:15 - 💡 แก้ไข!                                                       │
│  ├── git restore --staged evaluate.py                                      │
│  └── 📋 git status:                                                        │
│      ├── Changes to be committed:                                          │
│      │   └── modified: data_prep.py  ✅                                    │
│      └── Changes not staged:                                               │
│          └── modified: evaluate.py  (กลับมา working directory)             │
│                                                                            │
│  ⏰ 11:30 - Commit เฉพาะที่พร้อม                                            │
│  ├── git commit -m "feat: add feature engineering to data_prep"            │
│  └── 🎉 Commit สำเร็จ!                                                     │
│                                                                            │
│  ⏰ 11:45 - ตัดสินใจเรื่อง evaluate.py                                      │
│  ├── 💭 "ยังไม่พร้อม ขอกู้คืนเวอร์ชันเดิมก่อน"                               │
│  ├── git restore evaluate.py                                               │
│  └── 📋 git status → clean                                                 │
│                                                                            │
│  ⏰ 12:00-17:00 - ทำงานต่อ 🍔                                               │
│  └── 📝 บทเรียน: ตรวจสอบก่อน add และใช้ --staged เพื่อ unstage             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### 🗓️ วันพุธ (Day 3) - Over-Engineering & ต้องกลับเวอร์ชันเก่า

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📆 วันพุธ - Refactoring                                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⏰ 09:00 - ประชุมกับหัวหน้าทีม                                             │
│  ├── 👨‍💼 หัวหน้า: "ความคืบหน้าเป็นอย่างไรบ้าง?"                             │
│  ├── 📊 แสดง Pipeline: data_prep → train → evaluate                        │
│  ├── 👍 หัวหน้าพอใจ                                                        │
│  └── 📋 หัวหน้า: "ลองเพิ่ม logging หน่อยนะ"                                 │
│                                                                            │
│  ⏰ 10:00-12:00 - Over-engineering เริ่มต้น! 🔧                             │
│  ├── 💭 "งั้นทำให้เต็มที่เลย!"                                             │
│  ├── ✏️ evaluate.py:                                                       │
│  │   ├── เพิ่ม logging module (DEBUG, INFO, WARNING, ERROR)               │
│  │   ├── สร้าง ModelEvaluator class                                        │
│  │   ├── เพิ่ม metrics_history list                                        │
│  │   ├── เพิ่ม file handlers                                               │
│  │   └── เพิ่ม JSON export                                                 │
│  │                                                                         │
│  ├── git add evaluate.py                                                   │
│  └── git commit -m "refactor: over-engineer evaluation module"             │
│                                                                            │
│  ⏰ 13:00 - พักกลางวัน 🍲                                                   │
│  └── 💭 คิดว่าทำได้ดีมาก                                                    │
│                                                                            │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⏰ 14:00 - 🆘 สถานการณ์ที่ 3 เกิดขึ้น!                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                            │
│  👨‍💼 หัวหน้า Review โค้ด:                                                   │
│  ├── 😐 "ทำไมซับซ้อนขนาดนี้?"                                              │
│  ├── 📋 "Class ไม่จำเป็น ขอแค่ functions ธรรมดา"                            │
│  ├── 📋 "Logging ก็เกินไป ขอแค่ print ก็พอ"                                 │
│  └── 📋 "กลับไปใช้เวอร์ชันเรียบง่ายเถอะ"                                    │
│                                                                            │
│  😰 "แต่... commit ไปแล้วนี่!"                                              │
│                                                                            │
│  ⏰ 14:30 - 💡 แก้ไขด้วย git restore --source                               │
│  ├── git log --oneline                                                     │
│  │   ├── pqr4567 refactor: over-engineer evaluation module  ← ปัจจุบัน     │
│  │   ├── xyz7890 feat: add feature engineering to data_prep                │
│  │   ├── abc1234 feat: add model evaluation module  ← ต้องการ!             │
│  │   ├── def5678 feat: add model training module                           │
│  │   └── ghi9012 feat: add data preparation module                         │
│  │                                                                         │
│  ├── git restore --source=abc1234 evaluate.py                              │
│  └── 🎉 โค้ดกลับมาเป็นเวอร์ชันเรียบง่าย!                                    │
│                                                                            │
│  ⏰ 15:00 - Commit การแก้ไข                                                │
│  ├── git add evaluate.py                                                   │
│  └── git commit -m "revert: restore simple evaluation module"              │
│                                                                            │
│  ⏰ 15:30 - หัวหน้า Review อีกครั้ง                                         │
│  ├── 👍 "ดีมาก เรียบง่าย เข้าใจง่าย"                                        │
│  └── 💡 "จำไว้นะ KISS - Keep It Simple, Stupid"                            │
│                                                                            │
│  ⏰ 17:00 - เลิกงาน 🏠                                                      │
│  └── 📝 บทเรียน: Simple is better than complex                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### 🗓️ วันพฤหัส (Day 4) - อุบัติเหตุครั้งใหญ่

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📆 วันพฤหัส - Testing & Bug Fixing                                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⏰ 09:00 - เริ่มทำงานตามปกติ ☕                                            │
│                                                                            │
│  ⏰ 09:30 - ทดลอง script ใหม่                                              │
│  ├── 💭 "ลองเขียน script สำหรับ cleanup"                                   │
│  └── ✏️ เริ่มเขียน cleanup.sh                                              │
│                                                                            │
│  ⏰ 10:00 - ประชุมด่วน! 📞                                                  │
│  ├── หัวหน้าเรียกประชุม                                                    │
│  ├── ⏰ ประชุมเริ่ม 10:30                                                   │
│  └── 😰 รีบ! ต้องทำให้เสร็จก่อน                                            │
│                                                                            │
│  ════════════════════════════════════════════════════════════════════════  │
│  ⏰ 10:15 - 🆘 สถานการณ์ที่ 4 เกิดขึ้น! 💥                                  │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                            │
│  💨 รีบเกินไป พิมพ์คำสั่งผิด!                                               │
│                                                                            │
│  ⌨️ ตั้งใจพิมพ์:                                                            │
│      echo "# Clean script" > cleanup.sh                                    │
│                                                                            │
│  ⌨️ พิมพ์จริง (ผิด!):                                                       │
│      echo "# BROKEN!" > data_prep.py                                       │
│      echo "# BROKEN!" > train.py                                           │
│                                                                            │
│  😱 ไฟล์หลักถูกเขียนทับ!                                                    │
│                                                                            │
│  📋 git status:                                                            │
│  ├── modified: data_prep.py                                                │
│  └── modified: train.py                                                    │
│                                                                            │
│  📄 cat data_prep.py:                                                      │
│      # BROKEN!                                                             │
│                                                                            │
│  📄 cat train.py:                                                          │
│      # BROKEN!                                                             │
│                                                                            │
│  😰 "โค้ดหลายร้อยบรรทัดหายหมด! ทำไงดี?!"                                    │
│                                                                            │
│  ⏰ 10:20 - 💡 สงบสติ นึกได้!                                               │
│  ├── 💭 "ยังไม่ได้ commit!"                                                │
│  ├── 💭 "ใช้ git restore . ได้!"                                           │
│  ├── ✅ git restore .                                                      │
│  └── 🎉 ทุกไฟล์กลับมา!                                                     │
│                                                                            │
│  ⏰ 10:25 - ตรวจสอบ                                                        │
│  ├── git status → clean                                                    │
│  ├── python train.py → สำเร็จ!                                             │
│  └── 👍 ทุกอย่างปกติ                                                       │
│                                                                            │
│  ⏰ 10:30 - เข้าประชุม (ทันพอดี!) 📞                                        │
│  └── 😌 ไม่มีใครรู้เรื่องอุบัติเหตุ                                          │
│                                                                            │
│  ⏰ 12:00-17:00 - ทำงานต่อ                                                  │
│  └── 📝 บทเรียน: git restore . คือเพื่อนที่ดีที่สุดยามคับขัน               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### 🗓️ วันศุกร์ (Day 5) - ส่งงานสำเร็จ 🎉

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📆 วันศุกร์ - Delivery Day!                                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ⏰ 09:00 - ตรวจสอบทุกอย่างครั้งสุดท้าย                                     │
│  ├── 🧪 python data_prep.py → ✅                                           │
│  ├── 🧪 python train.py → ✅                                               │
│  ├── 🧪 python evaluate.py → ✅                                            │
│  └── 📊 Accuracy: 96.67%                                                   │
│                                                                            │
│  ⏰ 10:00 - นำเสนอผลงาน 🎤                                                  │
│  ├── 👨‍💼 หัวหน้าและทีม                                                     │
│  ├── 📊 Demo Pipeline ทั้งหมด                                              │
│  └── 👏 ทุกคนพอใจ!                                                         │
│                                                                            │
│  ⏰ 11:00 - Feedback จากหัวหน้า                                             │
│  ├── 👍 "ดีมาก! Pipeline ใช้งานได้จริง"                                    │
│  ├── 👍 "โค้ดเรียบง่าย เข้าใจง่าย"                                          │
│  ├── 👍 "Git workflow เป็นระเบียบ"                                         │
│  └── 🎁 "พร้อมรับโปรเจกต์จริงแล้ว!"                                         │
│                                                                            │
│  ⏰ 12:00 - ฉลองความสำเร็จ 🍕                                               │
│  └── กินพิซซ่ากับทีม                                                       │
│                                                                            │
│  ⏰ 17:00 - เลิกงาน                                                        │
│  └── 🎉 จบสัปดาห์ด้วยความสำเร็จ!                                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ สรุปภาพรวม 4 สถานการณ์

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     🗺️ สรุป 4 สถานการณ์ที่จะพบใน Lab                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ╔════════════════════════════════════════════════════════════════════════╗ │
│  ║ 📆 วันจันทร์ 17:00                                                      ║ │
│  ║ ┌───────────────────────────────────────────────────────────────────┐  ║ │
│  ║ │ 🆘 สถานการณ์ที่ 1: แก้ไขโค้ดผิดพลาดใน Working Directory            │  ║ │
│  ║ │                                                                   │  ║ │
│  ║ │ ❌ ปัญหา: แก้ไข train.py ผิด (n_estimators=-999)                   │  ║ │
│  ║ │ 💡 วิธีแก้: git restore train.py                                  │  ║ │
│  ║ │ ✅ ผลลัพธ์: โค้ดกลับมาใช้งานได้                                     │  ║ │
│  ║ └───────────────────────────────────────────────────────────────────┘  ║ │
│  ╚════════════════════════════════════════════════════════════════════════╝ │
│                              │                                               │
│                              ▼                                               │
│  ╔════════════════════════════════════════════════════════════════════════╗ │
│  ║ 📆 วันอังคาร 11:00                                                      ║ │
│  ║ ┌───────────────────────────────────────────────────────────────────┐  ║ │
│  ║ │ 🆘 สถานการณ์ที่ 2: Add ไฟล์ผิด (Staged)                            │  ║ │
│  ║ │                                                                   │  ║ │
│  ║ │ ❌ ปัญหา: git add . แล้ว evaluate.py ยังไม่พร้อม commit            │  ║ │
│  ║ │ 💡 วิธีแก้: git restore --staged evaluate.py                      │  ║ │
│  ║ │ ✅ ผลลัพธ์: evaluate.py กลับไป Working Directory                  │  ║ │
│  ║ └───────────────────────────────────────────────────────────────────┘  ║ │
│  ╚════════════════════════════════════════════════════════════════════════╝ │
│                              │                                               │
│                              ▼                                               │
│  ╔════════════════════════════════════════════════════════════════════════╗ │
│  ║ 📆 วันพุธ 14:30                                                         ║ │
│  ║ ┌───────────────────────────────────────────────────────────────────┐  ║ │
│  ║ │ 🆘 สถานการณ์ที่ 3: ต้องกลับไปเวอร์ชันเก่า (Over-engineered)        │  ║ │
│  ║ │                                                                   │  ║ │
│  ║ │ ❌ ปัญหา: evaluate.py ซับซ้อนเกินไป และ commit ไปแล้ว             │  ║ │
│  ║ │ 💡 วิธีแก้: git restore --source=<commit> evaluate.py             │  ║ │
│  ║ │ ✅ ผลลัพธ์: โค้ดกลับมาเป็นเวอร์ชันเรียบง่าย                         │  ║ │
│  ║ └───────────────────────────────────────────────────────────────────┘  ║ │
│  ╚════════════════════════════════════════════════════════════════════════╝ │
│                              │                                               │
│                              ▼                                               │
│  ╔════════════════════════════════════════════════════════════════════════╗ │
│  ║ 📆 วันพฤหัส 10:15                                                       ║ │
│  ║ ┌───────────────────────────────────────────────────────────────────┐  ║ │
│  ║ │ 🆘 สถานการณ์ที่ 4: หลายไฟล์พังพร้อมกัน (อุบัติเหตุ)                │  ║ │
│  ║ │                                                                   │  ║ │
│  ║ │ ❌ ปัญหา: พิมพ์คำสั่งผิด เขียนทับหลายไฟล์                          │  ║ │
│  ║ │ 💡 วิธีแก้: git restore .                                         │  ║ │
│  ║ │ ✅ ผลลัพธ์: ทุกไฟล์กลับมาเป็นปกติ                                   │  ║ │
│  ║ └───────────────────────────────────────────────────────────────────┘  ║ │
│  ╚════════════════════════════════════════════════════════════════════════╝ │
│                              │                                               │
│                              ▼                                               │
│                        🎉 วันศุกร์                                           │
│                      ส่งงานสำเร็จ!                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Part 1: การเตรียมความพร้อม

### ขั้นตอนที่ 0.1: ตั้งค่า Git (ทำครั้งแรกครั้งเดียว)

> ⚠️ **หมายเหตุ**: ถ้าเคยตั้งค่า Git แล้ว ให้ข้ามไปขั้นตอนที่ 0.2 ได้เลย

**ทำไมต้องตั้งค่า?** Git ต้องรู้ว่า "ใคร" เป็นคนทำการเปลี่ยนแปลง เพื่อบันทึกในประวัติ commit

```bash
# ตรวจสอบว่าตั้งค่าไว้แล้วหรือยัง
git config --global user.name
git config --global user.email
```

ถ้ายังไม่มีค่า ให้ตั้งค่าดังนี้:

```bash
# ตั้งค่าชื่อผู้ใช้ (ใส่ชื่อจริงของนักศึกษา)
git config --global user.name "Student Name"

# ตั้งค่าอีเมล (ใส่อีเมลจริงของนักศึกษา)
git config --global user.email "student@example.com"
```

### ขั้นตอนที่ 0.2: เตรียม Project Environment

```bash
# สร้างโฟลเดอร์สำหรับ Lab
mkdir -p ~/mlops-git-restore-lab
cd ~/mlops-git-restore-lab

# สร้าง Git repository ใหม่
git init

# สร้าง virtual environment (แนะนำ)
python3 -m venv venv
source venv/bin/activate

# ติดตั้ง dependencies
pip install scikit-learn pandas numpy
```

---

## 📝 Part 2: สร้าง ML Pipeline

### ขั้นตอนที่ 1: สร้างไฟล์ Data Preparation

**📍 ไทม์ไลน์:** วันจันทร์ 09:00-10:30

```bash
cat > data_prep.py << 'EOF'
"""
Data Preparation Module
สำหรับโหลดและเตรียมข้อมูล Iris Dataset
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_data():
    """โหลด Iris dataset และแปลงเป็น DataFrame"""
    iris = load_iris()
    df = pd.DataFrame(
        data=iris.data,
        columns=iris.feature_names
    )
    df['target'] = iris.target
    df['target_name'] = df['target'].map({
        0: 'setosa',
        1: 'versicolor', 
        2: 'virginica'
    })
    return df

def prepare_data(df, test_size=0.2, random_state=42):
    """แบ่งข้อมูลเป็น train/test sets"""
    X = df.drop(['target', 'target_name'], axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df = load_data()
    print("Dataset Info:")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())
    
    X_train, X_test, y_train, y_test = prepare_data(df)
EOF
```

```bash
# Commit
git add data_prep.py
git commit -m "feat: add data preparation module"
```

### ขั้นตอนที่ 2: สร้างไฟล์ Training

**📍 ไทม์ไลน์:** วันจันทร์ 11:30-13:00

```bash
cat > train.py << 'EOF'
"""
Model Training Module
สำหรับ train โมเดล Classification
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from data_prep import load_data, prepare_data

def train_model(X_train, y_train, n_estimators=100, max_depth=5):
    """Train Random Forest Classifier"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train_scaled, y_train)
    
    print(f"Model trained with {n_estimators} trees, max_depth={max_depth}")
    
    return model, scaler

def save_model(model, scaler, model_path="model.pkl", scaler_path="scaler.pkl"):
    """บันทึกโมเดลและ scaler"""
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")

if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    model, scaler = train_model(X_train, y_train)
    save_model(model, scaler)
EOF
```

```bash
# Commit
git add train.py
git commit -m "feat: add model training module"
```

### ขั้นตอนที่ 3: สร้างไฟล์ Evaluation

**📍 ไทม์ไลน์:** วันจันทร์ 14:30-16:00

```bash
cat > evaluate.py << 'EOF'
"""
Model Evaluation Module
สำหรับประเมินผลโมเดล Classification
"""
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import pickle
import numpy as np
from data_prep import load_data, prepare_data

def load_model(model_path="model.pkl", scaler_path="scaler.pkl"):
    """โหลดโมเดลและ scaler"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

def evaluate_model(model, scaler, X_test, y_test):
    """ประเมินผลโมเดล"""
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    return metrics, y_pred

def print_evaluation_report(metrics, y_test, y_pred):
    """พิมพ์รายงานการประเมินผล"""
    print("=" * 50)
    print("MODEL EVALUATION REPORT")
    print("=" * 50)
    
    print("\n📊 Performance Metrics:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1-Score:  {metrics['f1_score']:.4f}")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, 
          target_names=['setosa', 'versicolor', 'virginica']))
    
    print("🔢 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    model, scaler = load_model()
    metrics, y_pred = evaluate_model(model, scaler, X_test, y_test)
    print_evaluation_report(metrics, y_test, y_pred)
EOF
```

```bash
# Commit
git add evaluate.py
git commit -m "feat: add model evaluation module"
```

### ✅ ตรวจสอบประวัติ Commits

```bash
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
abc1234 feat: add model evaluation module
def5678 feat: add model training module  
ghi9012 feat: add data preparation module
```

---

## 🚨 Part 3: สถานการณ์ปัญหาและการแก้ไข

### 📍 สถานการณ์ที่ 1: แก้ไขโค้ดผิดพลาดใน Working Directory

**📆 วันจันทร์ 17:00**

#### ขั้นตอน 1.1: สร้างปัญหา (จำลองความผิดพลาด)

```bash
cat > train.py << 'EOF'
"""
Model Training Module - BROKEN VERSION
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
from data_prep import load_data, prepare_data

def train_model(X_train, y_train, n_estimators=100, max_depth=5):
    model = RandomForestClassifier(
        n_estimators=-999,  # BUG: ค่าติดลบ!
        max_depth="invalid",  # BUG: ชนิดข้อมูลผิด!
        random_state=42
    )
    model.fit(X_train, y_train)
    return model  # BUG: ไม่ได้ return scaler!

def save_model(model, scaler, model_path="model.pkl", scaler_path="scaler.pkl"):
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == "__main__":
    df = load_data()
    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train)
    save_model(model, None)
EOF
```

#### ขั้นตอน 1.2: ตรวจสอบและแก้ไข

```bash
# ดูสถานะ
git status

# ลองรัน - จะเกิด Error
python train.py

# 💡 กู้คืนไฟล์
git restore train.py

# ตรวจสอบ
python train.py  # ควรทำงานได้
```

---

### 📍 สถานการณ์ที่ 2: ยกเลิกไฟล์ที่ add ไปแล้ว (Staged)

**📆 วันอังคาร 11:00**

#### ขั้นตอน 2.1: แก้ไขหลายไฟล์และ add ทั้งหมด

```bash
# แก้ไข data_prep.py (เพิ่ม feature engineering)
# แก้ไข evaluate.py (เพิ่ม experimental features)

git add .
git status
```

#### ขั้นตอน 2.2: Unstage เฉพาะไฟล์ที่ยังไม่พร้อม

```bash
# Unstage evaluate.py
git restore --staged evaluate.py

# Commit เฉพาะ data_prep.py
git commit -m "feat: add feature engineering to data_prep"

# กู้คืน evaluate.py กลับเป็นเวอร์ชันเดิม
git restore evaluate.py
```

---

### 📍 สถานการณ์ที่ 3: กู้คืนไฟล์จาก Commit เฉพาะ

**📆 วันพุธ 14:30**

#### ขั้นตอน 3.1: ดูประวัติ commits

```bash
git log --oneline
```

#### ขั้นตอน 3.2: กู้คืนจาก commit เดิม

```bash
# หา commit hash ของเวอร์ชันที่ต้องการ
# แล้วกู้คืน
git restore --source=<commit_hash> evaluate.py

# หรือใช้ HEAD~N
git restore --source=HEAD~2 evaluate.py

# Commit การเปลี่ยนแปลง
git add evaluate.py
git commit -m "revert: restore simple evaluation module"
```

---

### 📍 สถานการณ์ที่ 4: กู้คืนหลายไฟล์พร้อมกัน

**📆 วันพฤหัส 10:15**

#### ขั้นตอน 4.1: สร้างปัญหา (จำลองอุบัติเหตุ)

```bash
# เขียนทับไฟล์หลายไฟล์ (อุบัติเหตุ!)
echo "# BROKEN!" > data_prep.py
echo "# BROKEN!" > train.py

# ตรวจสอบ
git status
cat data_prep.py
```

#### ขั้นตอน 4.2: กู้คืนทุกไฟล์

```bash
# กู้คืนทุกไฟล์พร้อมกัน
git restore .

# ตรวจสอบ
git status  # ควรเป็น clean
python train.py  # ควรทำงานได้
```

---

## 📊 สรุปคำสั่ง Git Restore

| คำสั่ง | ทำอะไร | เมื่อไหร่ใช้ |
|--------|--------|------------|
| `git restore <file>` | ยกเลิกการแก้ไขใน Working Directory | แก้ไขผิด ยังไม่ได้ add |
| `git restore --staged <file>` | เอาไฟล์ออกจาก Staging Area | add ไปแล้ว ไม่อยาก commit |
| `git restore --source=<commit> <file>` | กู้คืนจาก commit ที่ระบุ | ต้องการเวอร์ชันเก่า |
| `git restore .` | กู้คืนทุกไฟล์ | ทุกอย่างพัง! |

---

## ✅ แบบฝึกหัดเพิ่มเติม

### แบบฝึกหัดที่ 1: Basic Restore
1. แก้ไข `train.py` โดยเปลี่ยน `n_estimators=100` เป็น `n_estimators=10`
2. ใช้ `git diff` ดูความแตกต่าง
3. ใช้ `git restore train.py` กู้คืนไฟล์

### แบบฝึกหัดที่ 2: Staged Restore
1. แก้ไข `evaluate.py` เพิ่ม comment
2. ใช้ `git add evaluate.py`
3. ใช้ `git restore --staged evaluate.py`
4. ใช้ `git restore evaluate.py`

### แบบฝึกหัดที่ 3: Source Restore
1. ดู commit history ด้วย `git log --oneline`
2. กู้คืน `data_prep.py` จาก commit แรก
3. ตรวจสอบความแตกต่างด้วย `git diff`

---

## 🎓 บทสรุป

### สิ่งที่ได้เรียนรู้

1. **git restore** เป็นเครื่องมือสำคัญในการจัดการกับความผิดพลาด
2. การแยกแยะระหว่าง **Working Directory**, **Staging Area**, และ **Repository**
3. ใน MLOps การทดลองและย้อนกลับเป็นเรื่องปกติ
4. **`--source`** ช่วยให้กู้คืนไฟล์จาก commit ใดก็ได้

### Best Practices

| Practice | เหตุผล |
|----------|--------|
| Commit บ่อยๆ | มี restore points มากขึ้น |
| เขียน commit message ชัดเจน | หา commit ได้ง่าย |
| ใช้ `git status` บ่อยๆ | รู้ว่าอยู่สถานะไหน |
| ทดสอบก่อน commit | ลดโอกาสต้อง restore |

### ⚠️ ข้อควรระวัง

- `git restore <file>` - การเปลี่ยนแปลงที่ไม่ได้ commit จะหายถาวร!
- `git restore .` - ทุกไฟล์จะถูกกู้คืน ตรวจสอบให้ดีก่อนใช้

---

## 📚 อ้างอิง

- [Git Documentation - git restore](https://git-scm.com/docs/git-restore)
- [Pro Git Book](https://git-scm.com/book)
- [MLOps Best Practices](https://ml-ops.org/)