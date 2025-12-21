# 🌿 LAB: Git Branch - การจัดการ Branch ใน Git

## 📋 วัตถุประสงค์การเรียนรู้

หลังจากทำ LAB นี้เสร็จ นักศึกษาจะสามารถ:
- ✅ เข้าใจแนวคิดของ Git Branch
- ✅ ใช้งาน `git branch`, `git switch`, และ `git checkout`
- ✅ เข้าใจสถานะ Detached HEAD
- ✅ ทำงานกับ Remote Branch
- ✅ สร้าง, ลบ, และเปลี่ยนชื่อ Branch ทั้งใน Local และ Remote
- ✅ ใช้คำสั่ง `tree` ตรวจสอบโครงสร้างไฟล์และโฟลเดอร์
- ✅ ใช้คำสั่ง `cat` และ Here Document สร้างไฟล์
- ✅ เข้าใจการใช้ Pipeline (`|`) ใน Linux
- ✅ ใช้คำสั่ง Git พื้นฐานอื่น ๆ เพื่อช่วยในการทำงาน

---

## 📚 ความรู้พื้นฐาน

### Branch คืออะไร?

**Branch** คือ "กิ่ง" ของโปรเจกต์ที่แยกออกมาจากเส้นหลัก ช่วยให้เราสามารถ:
- พัฒนา Feature ใหม่โดยไม่กระทบ Code หลัก
- ทดลองไอเดียใหม่ ๆ อย่างปลอดภัย
- ทำงานร่วมกันหลายคนโดยไม่ชนกัน

```
          feature-login
              ↓
    A---B---C---D
   /             
main---E---F---G
              ↑
          เส้นหลัก
```

### ประเภทของ Branch

| ประเภท | คำอธิบาย |
|--------|----------|
| **Local Branch** | Branch ที่อยู่บนเครื่องของเรา |
| **Remote Branch** | Branch ที่อยู่บน Server (เช่น GitHub, GitLab) |
| **Tracking Branch** | Local Branch ที่เชื่อมต่อกับ Remote Branch |

---

## 🔧 ความรู้เบื้องต้น: Pipeline ใน Linux

### Pipeline (`|`) คืออะไร?

**Pipeline** คือการส่งผลลัพธ์จากคำสั่งหนึ่งไปเป็น input ของอีกคำสั่งหนึ่ง โดยใช้เครื่องหมาย `|` (pipe)

```
คำสั่งที่ 1  |  คำสั่งที่ 2  |  คำสั่งที่ 3
    ↓              ↓              ↓
  output    →    input     →   output
            →              →    input
                           →   output (สุดท้าย)
```

### ตัวอย่างการใช้ Pipeline

```bash
# ตัวอย่างที่ 1: นับจำนวนไฟล์ในโฟลเดอร์
ls | wc -l
```

**อธิบายทีละขั้นตอน:**
```
ls              →  แสดงรายชื่อไฟล์ทั้งหมด
                   file1.txt
                   file2.txt
                   file3.txt
        |
        ↓
wc -l           →  นับจำนวนบรรทัด (line count)
                   ผลลัพธ์: 3
```

```bash
# ตัวอย่างที่ 2: ค้นหาไฟล์ .py
ls | grep ".py"
```

**อธิบายทีละขั้นตอน:**
```
ls              →  แสดงรายชื่อไฟล์ทั้งหมด
                   main.py
                   README.md
                   utils.py
                   config.json
        |
        ↓
grep ".py"      →  กรองเฉพาะบรรทัดที่มี ".py"
                   ผลลัพธ์:
                   main.py
                   utils.py
```

```bash
# ตัวอย่างที่ 3: ดู commit ล่าสุด 5 อัน และค้นหาคำว่า "fix"
git log --oneline | head -5 | grep "fix"
```

**อธิบายทีละขั้นตอน:**
```
git log --oneline    →  แสดง commit ทั้งหมด (บรรทัดเดียวต่อ commit)
                        abc1234 feat: add login
                        def5678 fix: bug in navbar
                        ghi9012 feat: add register
                        jkl3456 fix: typo in readme
                        mno7890 initial commit
                        ...
        |
        ↓
head -5              →  เอาแค่ 5 บรรทัดแรก
                        abc1234 feat: add login
                        def5678 fix: bug in navbar
                        ghi9012 feat: add register
                        jkl3456 fix: typo in readme
                        mno7890 initial commit
        |
        ↓
grep "fix"           →  กรองเฉพาะบรรทัดที่มีคำว่า "fix"
                        ผลลัพธ์:
                        def5678 fix: bug in navbar
                        jkl3456 fix: typo in readme
```

```bash
# ตัวอย่างที่ 4: นับจำนวน branch ทั้งหมด
git branch | wc -l
```

**อธิบายทีละขั้นตอน:**
```
git branch      →  แสดงรายชื่อ branch
                   * main
                     feature-login
                     feature-register
        |
        ↓
wc -l           →  นับจำนวนบรรทัด
                   ผลลัพธ์: 3
```

```bash
# ตัวอย่างที่ 5: ค้นหา branch ที่มีคำว่า "feature"
git branch | grep "feature"
```

**อธิบายทีละขั้นตอน:**
```
git branch      →  แสดงรายชื่อ branch
                   * main
                     feature-login
                     feature-register
                     bugfix-navbar
        |
        ↓
grep "feature"  →  กรองเฉพาะบรรทัดที่มี "feature"
                   ผลลัพธ์:
                     feature-login
                     feature-register
```

### สรุปคำสั่งที่ใช้บ่อยกับ Pipeline

| คำสั่ง | หน้าที่ | ตัวอย่าง |
|--------|--------|----------|
| `grep "text"` | กรองบรรทัดที่มีข้อความ | `cat file | grep "error"` |
| `wc -l` | นับจำนวนบรรทัด | `ls | wc -l` |
| `head -n` | เอา n บรรทัดแรก | `cat file | head -10` |
| `tail -n` | เอา n บรรทัดสุดท้าย | `cat file | tail -5` |
| `sort` | เรียงลำดับ | `cat file | sort` |
| `uniq` | ลบบรรทัดซ้ำ | `cat file | sort | uniq` |

---

## 🔧 ความรู้เบื้องต้น: Here Document (Heredoc)

### Here Document คืออะไร?

**Here Document** คือวิธีการเขียนข้อความหลายบรรทัดลงไฟล์โดยไม่ต้องกด Ctrl+D

```bash
cat > ชื่อไฟล์ << 'EOF'
เนื้อหาบรรทัดที่ 1
เนื้อหาบรรทัดที่ 2
เนื้อหาบรรทัดที่ 3
EOF
```

**อธิบาย:**
- `cat > ชื่อไฟล์` = สร้างไฟล์ใหม่
- `<< 'EOF'` = เริ่มต้น Here Document (EOF = End Of File, ใช้คำอื่นก็ได้)
- `EOF` = สิ้นสุด Here Document

### เปรียบเทียบวิธีสร้างไฟล์

| วิธี | ข้อดี | ข้อเสีย |
|------|-------|---------|
| `echo "text" > file` | ง่าย รวดเร็ว | เขียนได้แค่บรรทัดเดียว |
| `cat > file` แล้ว Ctrl+D | เขียนได้หลายบรรทัด | ต้องจำกด Ctrl+D |
| `cat > file << 'EOF'` | เขียนได้หลายบรรทัด, ชัดเจน | พิมพ์ยาวกว่า |

---

## 🛠️ เตรียมความพร้อม

### ขั้นตอนที่ 1: ตั้งค่า Git (ถ้ายังไม่เคยตั้ง)

```bash
# ตั้งค่าชื่อผู้ใช้
git config --global user.name "ชื่อของคุณ"

# ตั้งค่าอีเมล
git config --global user.email "your.email@example.com"

# ตรวจสอบการตั้งค่า
git config --list
```

### ขั้นตอนที่ 2: สร้างโปรเจกต์สำหรับฝึก

```bash
# สร้างโฟลเดอร์ใหม่
mkdir git-branch-lab
cd git-branch-lab

# เริ่มต้น Git repository
git init

# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in /path/to/git-branch-lab/.git/
```

### ขั้นตอนที่ 3: ใช้ tree ดูโครงสร้างโปรเจกต์

```bash
# ดูโครงสร้างโฟลเดอร์ (รวม hidden files)
tree -a
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
└── .git
    ├── HEAD
    ├── config
    ├── description
    ├── hooks
    │   └── ...
    ├── info
    │   └── exclude
    ├── objects
    │   ├── info
    │   └── pack
    └── refs
        ├── heads
        └── tags
```

> 💡 คำสั่ง `tree -a` แสดงไฟล์ที่ซ่อน (hidden files) ด้วย ทำให้เห็นโฟลเดอร์ `.git`

---

## 📝 แบบฝึกหัดที่ 0: การใช้ Here Document สร้างไฟล์

### 0.1 สร้างไฟล์ README.md

```bash
cat > README.md << 'EOF'
# My Git Branch Lab
โปรเจกต์สำหรับเรียนรู้ Git Branch

## วัตถุประสงค์
- เรียนรู้การใช้งาน Git Branch
- ฝึกการสลับ Branch
- เข้าใจ Remote Branch

## ผู้จัดทำ
- นักศึกษา: [ชื่อของคุณ]
- รหัส: [รหัสนักศึกษา]
EOF
```

```bash
# ตรวจสอบไฟล์ที่สร้าง
cat README.md
```

**ผลลัพธ์ที่คาดหวัง:**
```
# My Git Branch Lab
โปรเจกต์สำหรับเรียนรู้ Git Branch

## วัตถุประสงค์
- เรียนรู้การใช้งาน Git Branch
- ฝึกการสลับ Branch
- เข้าใจ Remote Branch

## ผู้จัดทำ
- นักศึกษา: [ชื่อของคุณ]
- รหัส: [รหัสนักศึกษา]
```

### 0.2 ใช้ tree ดูโครงสร้างหลังสร้างไฟล์

```bash
# ดูโครงสร้าง (ไม่รวม .git)
tree

# ดูโครงสร้างพร้อม hidden files
tree -a

# ดูเฉพาะ 1 level
tree -L 1
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
└── README.md

0 directories, 1 file
```

### 0.3 สร้างไฟล์ Python ด้วย Here Document

```bash
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application file
Git Branch Lab Project
"""

def main():
    print("Welcome to Git Branch Lab!")
    print("Let's learn about branches!")

if __name__ == "__main__":
    main()
EOF
```

```bash
# ตรวจสอบไฟล์
cat main.py

# ดูโครงสร้างโปรเจกต์
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
└── main.py

0 directories, 2 files
```

### 0.4 สร้างโฟลเดอร์และไฟล์หลายไฟล์

```bash
# สร้างโฟลเดอร์ src
mkdir src

# สร้างไฟล์ __init__.py
cat > src/__init__.py << 'EOF'
# Package initialization
__version__ = "1.0.0"
EOF
```

```bash
# สร้างไฟล์ utils.py
cat > src/utils.py << 'EOF'
"""Utility functions"""

def greet(name):
    """Greet a user"""
    return f"Hello, {name}!"

def add(a, b):
    """Add two numbers"""
    return a + b
EOF
```

```bash
# สร้างโฟลเดอร์ tests
mkdir tests

# สร้างไฟล์ test
cat > tests/test_utils.py << 'EOF'
"""Unit tests for utils module"""
import sys
sys.path.insert(0, '..')
from src.utils import greet, add

def test_greet():
    assert greet("World") == "Hello, World!"

def test_add():
    assert add(2, 3) == 5

if __name__ == "__main__":
    test_greet()
    test_add()
    print("All tests passed!")
EOF
```

### 0.5 ใช้ tree ดูโครงสร้างโปรเจกต์ทั้งหมด

```bash
# ดูโครงสร้างทั้งหมด
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── main.py
├── src
│   ├── __init__.py
│   └── utils.py
└── tests
    └── test_utils.py

2 directories, 5 files
```

### 0.6 ใช้ Pipeline กับ tree

```bash
# นับจำนวนไฟล์ Python
tree | grep ".py" | wc -l
```

**อธิบายทีละขั้นตอน:**
```
tree            →  แสดงโครงสร้างไฟล์ทั้งหมด
        |
        ↓
grep ".py"      →  กรองเฉพาะบรรทัดที่มี ".py"
                   ├── main.py
                   ├── __init__.py
                   └── utils.py
                   └── test_utils.py
        |
        ↓
wc -l           →  นับจำนวนบรรทัด
                   ผลลัพธ์: 4
```

### 0.7 ตัวเลือกที่มีประโยชน์ของ tree

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `tree` | ดูโครงสร้างพื้นฐาน |
| `tree -a` | แสดง hidden files |
| `tree -L 2` | แสดงแค่ 2 ระดับ |
| `tree -d` | แสดงเฉพาะโฟลเดอร์ |
| `tree -f` | แสดง full path |
| `tree -h` | แสดงขนาดไฟล์ |
| `tree -I "node_modules"` | ไม่แสดงโฟลเดอร์ที่ระบุ |
| `tree --du` | แสดงขนาดรวมของโฟลเดอร์ |
| `tree -P "*.py"` | แสดงเฉพาะไฟล์ .py |

### 0.8 เปรียบเทียบวิธีสร้างไฟล์

| คำสั่ง | การทำงาน | ตัวอย่าง |
|--------|----------|----------|
| `cat > file << 'EOF'` | สร้างไฟล์หลายบรรทัด (ทับ) | ดูตัวอย่างด้านบน |
| `cat >> file << 'EOF'` | เพิ่มต่อท้ายไฟล์ (หลายบรรทัด) | เพิ่มเนื้อหาต่อท้าย |
| `echo "text" > file` | สร้างไฟล์บรรทัดเดียว (ทับ) | `echo "hello" > test.txt` |
| `echo "text" >> file` | เพิ่มต่อท้าย (บรรทัดเดียว) | `echo "world" >> test.txt` |

---

## 📝 แบบฝึกหัดที่ 1: Commit ไฟล์ที่สร้าง

### 1.1 เพิ่มไฟล์ทั้งหมดและ Commit

```bash
# ดูสถานะ
git status

# เพิ่มไฟล์ทั้งหมด
git add .

# ดูสถานะอีกครั้ง
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
        new file:   main.py
        new file:   src/__init__.py
        new file:   src/utils.py
        new file:   tests/test_utils.py
```

```bash
# Commit ครั้งแรก
git commit -m "Initial commit: สร้างโครงสร้างโปรเจกต์"

# ดู log
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
abc1234 Initial commit: สร้างโครงสร้างโปรเจกต์
```

---

## 📝 แบบฝึกหัดที่ 2: การสร้างและดู Branch

### 2.1 ดูรายชื่อ Branch ทั้งหมด

```bash
# ดู local branch ทั้งหมด
git branch

# ดู local และ remote branch ทั้งหมด
git branch -a

# ดูพร้อมรายละเอียด (commit ล่าสุด)
git branch -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
* main
```
> 💡 เครื่องหมาย `*` แสดงว่าเราอยู่ที่ branch ไหน

### 2.2 สร้าง Branch ใหม่

```bash
# วิธีที่ 1: สร้าง branch แต่ไม่ย้ายไป
git branch feature-login

# ตรวจสอบว่า branch ถูกสร้างแล้ว
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
* main
```

### 2.3 สร้าง Branch เพิ่มเติม

```bash
# สร้าง branch อีกหลาย ๆ อัน
git branch feature-register
git branch bugfix-navbar
git branch hotfix-security

# ดูรายการ branch ทั้งหมด
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  bugfix-navbar
  feature-login
  feature-register
  hotfix-security
* main
```

### 2.4 ใช้ Pipeline นับจำนวน Branch

```bash
# นับจำนวน branch ทั้งหมด
git branch | wc -l
```

**อธิบายทีละขั้นตอน:**
```
git branch      →  แสดงรายชื่อ branch
                   * main
                     feature-login
                     feature-register
                     bugfix-navbar
                     hotfix-security
        |
        ↓
wc -l           →  นับจำนวนบรรทัด
                   ผลลัพธ์: 5
```

```bash
# ค้นหา branch ที่มีคำว่า "feature"
git branch | grep "feature"
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
  feature-register
```

### 2.5 ใช้ tree ดูโครงสร้าง .git/refs

```bash
# ดูว่า Git เก็บ branch ไว้ที่ไหน
tree .git/refs
```

**ผลลัพธ์ที่คาดหวัง:**
```
.git/refs
├── heads
│   ├── bugfix-navbar
│   ├── feature-login
│   ├── feature-register
│   ├── hotfix-security
│   └── main
└── tags

2 directories, 5 files
```

> 💡 Git เก็บ branch ไว้เป็นไฟล์ใน `.git/refs/heads/` โดยแต่ละไฟล์เก็บ commit hash

```bash
# ดู commit hash ที่แต่ละ branch ชี้ไป
cat .git/refs/heads/main
cat .git/refs/heads/feature-login
```

---

## 📝 แบบฝึกหัดที่ 3: การสลับ Branch ด้วย git switch และ git checkout

### 3.1 การใช้ git switch (วิธีใหม่ - แนะนำ)

```bash
# สลับไป branch feature-login
git switch feature-login

# ตรวจสอบว่าอยู่ branch ไหน
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  bugfix-navbar
* feature-login
  feature-register
  hotfix-security
  main
```

### 3.2 การใช้ git checkout (วิธีเก่า - ยังใช้ได้)

```bash
# สลับไป branch main ด้วย checkout
git checkout main

# ตรวจสอบ
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  bugfix-navbar
  feature-login
  feature-register
  hotfix-security
* main
```

### 3.3 สร้าง Branch และสลับไปพร้อมกัน

```bash
# วิธีที่ 1: ใช้ git switch -c (แนะนำ)
git switch -c feature-dashboard

# ตรวจสอบ
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  bugfix-navbar
* feature-dashboard
  feature-login
  feature-register
  hotfix-security
  main
```

```bash
# กลับไป main ก่อน
git switch main

# วิธีที่ 2: ใช้ git checkout -b
git checkout -b feature-profile

# ตรวจสอบ
git branch
```

### 3.4 เปรียบเทียบ git switch vs git checkout

| คำสั่ง | การใช้งาน | หมายเหตุ |
|--------|----------|----------|
| `git switch <branch>` | สลับ branch | วิธีใหม่ ปลอดภัยกว่า |
| `git switch -c <branch>` | สร้างและสลับ | เหมือน checkout -b |
| `git checkout <branch>` | สลับ branch | วิธีเก่า ยังใช้ได้ |
| `git checkout -b <branch>` | สร้างและสลับ | วิธีเก่า |
| `git checkout <file>` | กู้ไฟล์ | ⚠️ checkout ทำได้หลายอย่าง |

> 💡 **แนะนำ:** ใช้ `git switch` สำหรับสลับ branch และ `git restore` สำหรับกู้ไฟล์ เพื่อความชัดเจน

---

## 📝 แบบฝึกหัดที่ 4: ทำงานกับ Branch และใช้ tree ตรวจสอบ

### 4.1 สร้างการเปลี่ยนแปลงใน Branch

```bash
# ไปที่ feature-login
git switch feature-login

# ดูโครงสร้างปัจจุบัน
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── main.py
├── src
│   ├── __init__.py
│   └── utils.py
└── tests
    └── test_utils.py

2 directories, 5 files
```

### 4.2 สร้างไฟล์ใหม่สำหรับ Login Feature

```bash
# สร้างโฟลเดอร์ auth
mkdir -p src/auth

# สร้างไฟล์ __init__.py สำหรับ auth module
cat > src/auth/__init__.py << 'EOF'
# Authentication module
__all__ = ['login', 'logout', 'validate_user']
EOF
```

```bash
# สร้างไฟล์ login.py
cat > src/auth/login.py << 'EOF'
"""
Login Module
ระบบ Login สำหรับผู้ใช้งาน
"""

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged_in = False
    
    def __repr__(self):
        return f"User({self.username})"

def login(username, password):
    """
    ฟังก์ชันสำหรับ Login
    
    Args:
        username: ชื่อผู้ใช้
        password: รหัสผ่าน
    
    Returns:
        bool: True ถ้า login สำเร็จ
    """
    print(f"Attempting to login: {username}")
    # TODO: เพิ่มการตรวจสอบจริง
    if username and password:
        print("Login successful!")
        return True
    return False

def logout(user):
    """ฟังก์ชันสำหรับ Logout"""
    print(f"Logging out: {user.username}")
    user.is_logged_in = False
    return True

def validate_user(username):
    """ตรวจสอบความถูกต้องของ username"""
    if len(username) < 3:
        return False, "Username ต้องมีอย่างน้อย 3 ตัวอักษร"
    if not username.isalnum():
        return False, "Username ต้องเป็นตัวอักษรหรือตัวเลขเท่านั้น"
    return True, "Valid username"
EOF
```

### 4.3 สร้างไฟล์ Test สำหรับ Login

```bash
cat > tests/test_login.py << 'EOF'
"""
Unit Tests for Login Module
"""
import sys
sys.path.insert(0, '..')
from src.auth.login import login, logout, validate_user, User

def test_login_success():
    """ทดสอบ login สำเร็จ"""
    result = login("testuser", "password123")
    assert result == True
    print("✓ test_login_success passed")

def test_login_empty_username():
    """ทดสอบ login ด้วย username ว่าง"""
    result = login("", "password123")
    assert result == False
    print("✓ test_login_empty_username passed")

def test_validate_user_short():
    """ทดสอบ username สั้นเกินไป"""
    valid, msg = validate_user("ab")
    assert valid == False
    print("✓ test_validate_user_short passed")

def test_validate_user_valid():
    """ทดสอบ username ถูกต้อง"""
    valid, msg = validate_user("testuser")
    assert valid == True
    print("✓ test_validate_user_valid passed")

def test_user_class():
    """ทดสอบ User class"""
    user = User("john", "secret")
    assert user.username == "john"
    assert user.is_logged_in == False
    print("✓ test_user_class passed")

if __name__ == "__main__":
    test_login_success()
    test_login_empty_username()
    test_validate_user_short()
    test_validate_user_valid()
    test_user_class()
    print("\n🎉 All login tests passed!")
EOF
```

### 4.4 ใช้ tree ตรวจสอบโครงสร้างที่เปลี่ยนแปลง

```bash
# ดูโครงสร้างทั้งหมด
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── main.py
├── src
│   ├── __init__.py
│   ├── auth
│   │   ├── __init__.py
│   │   └── login.py
│   └── utils.py
└── tests
    ├── test_login.py
    └── test_utils.py

3 directories, 8 files
```

```bash
# ดูเฉพาะโฟลเดอร์ src
tree src
```

**ผลลัพธ์ที่คาดหวัง:**
```
src
├── __init__.py
├── auth
│   ├── __init__.py
│   └── login.py
└── utils.py

1 directory, 4 files
```

```bash
# ใช้ Pipeline นับไฟล์ Python ใน src
tree src | grep ".py" | wc -l
```

### 4.5 ดูสถานะและ Commit

```bash
# ดูสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch feature-login
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/auth/
        tests/test_login.py
```

```bash
# เพิ่มและ commit
git add .
git commit -m "feat: เพิ่มระบบ Login พร้อม tests"

# ดู log
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
def5678 feat: เพิ่มระบบ Login พร้อม tests
abc1234 Initial commit: สร้างโครงสร้างโปรเจกต์
```

### 4.6 เปรียบเทียบโครงสร้างระหว่าง Branch

```bash
# ดูโครงสร้างใน feature-login
echo "=== feature-login ==="
tree

# สลับไป main
git switch main

# ดูโครงสร้างใน main
echo "=== main ==="
tree
```

**ผลลัพธ์ที่คาดหวังใน main:**
```
=== main ===
.
├── README.md
├── main.py
├── src
│   ├── __init__.py
│   └── utils.py
└── tests
    └── test_utils.py

2 directories, 5 files
```

> 💡 สังเกตว่าโฟลเดอร์ `src/auth` และไฟล์ `tests/test_login.py` ไม่มีใน main เพราะมันอยู่ใน feature-login

---

## 📝 แบบฝึกหัดที่ 5: สร้าง Feature อีก Branch พร้อมไฟล์

### 5.1 สร้าง Feature Register

```bash
# สลับไป feature-register
git switch feature-register

# ดูโครงสร้างปัจจุบัน (ควรเหมือน main)
tree

# สร้างโฟลเดอร์
mkdir -p src/auth
```

### 5.2 สร้างไฟล์ register.py

```bash
cat > src/auth/register.py << 'EOF'
"""
Register Module
ระบบลงทะเบียนผู้ใช้ใหม่
"""

import re
from datetime import datetime

class RegistrationError(Exception):
    """Exception สำหรับข้อผิดพลาดในการลงทะเบียน"""
    pass

def validate_email(email):
    """
    ตรวจสอบรูปแบบ email
    
    Args:
        email: อีเมลที่ต้องการตรวจสอบ
    
    Returns:
        tuple: (is_valid, message)
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True, "Email valid"
    return False, "รูปแบบ email ไม่ถูกต้อง"

def validate_password(password):
    """
    ตรวจสอบความแข็งแรงของ password
    
    Requirements:
    - อย่างน้อย 8 ตัวอักษร
    - มีตัวพิมพ์ใหญ่
    - มีตัวเลข
    """
    errors = []
    if len(password) < 8:
        errors.append("Password ต้องมีอย่างน้อย 8 ตัวอักษร")
    if not any(c.isupper() for c in password):
        errors.append("Password ต้องมีตัวพิมพ์ใหญ่")
    if not any(c.isdigit() for c in password):
        errors.append("Password ต้องมีตัวเลข")
    
    if errors:
        return False, errors
    return True, ["Password valid"]

def register(username, email, password):
    """
    ลงทะเบียนผู้ใช้ใหม่
    
    Args:
        username: ชื่อผู้ใช้
        email: อีเมล
        password: รหัสผ่าน
    
    Returns:
        dict: ข้อมูลผู้ใช้ที่ลงทะเบียน
    """
    # Validate email
    email_valid, email_msg = validate_email(email)
    if not email_valid:
        raise RegistrationError(email_msg)
    
    # Validate password
    pass_valid, pass_msgs = validate_password(password)
    if not pass_valid:
        raise RegistrationError(", ".join(pass_msgs))
    
    # สร้างผู้ใช้ใหม่
    user = {
        'username': username,
        'email': email,
        'created_at': datetime.now().isoformat(),
        'is_active': True
    }
    
    print(f"✓ ลงทะเบียนสำเร็จ: {username}")
    return user
EOF
```

### 5.3 สร้าง Test สำหรับ Register

```bash
cat > tests/test_register.py << 'EOF'
"""
Unit Tests for Register Module
"""
import sys
sys.path.insert(0, '..')
from src.auth.register import (
    validate_email, 
    validate_password, 
    register,
    RegistrationError
)

def test_validate_email_valid():
    """ทดสอบ email ถูกต้อง"""
    valid, msg = validate_email("test@example.com")
    assert valid == True
    print("✓ test_validate_email_valid passed")

def test_validate_email_invalid():
    """ทดสอบ email ไม่ถูกต้อง"""
    valid, msg = validate_email("invalid-email")
    assert valid == False
    print("✓ test_validate_email_invalid passed")

def test_validate_password_weak():
    """ทดสอบ password อ่อนแอ"""
    valid, msgs = validate_password("short")
    assert valid == False
    print("✓ test_validate_password_weak passed")

def test_validate_password_strong():
    """ทดสอบ password แข็งแรง"""
    valid, msgs = validate_password("StrongPass123")
    assert valid == True
    print("✓ test_validate_password_strong passed")

def test_register_success():
    """ทดสอบลงทะเบียนสำเร็จ"""
    user = register("newuser", "new@example.com", "SecurePass123")
    assert user['username'] == "newuser"
    assert user['is_active'] == True
    print("✓ test_register_success passed")

def test_register_invalid_email():
    """ทดสอบลงทะเบียนด้วย email ไม่ถูกต้อง"""
    try:
        register("user", "bad-email", "Pass123456")
        assert False, "Should have raised error"
    except RegistrationError:
        print("✓ test_register_invalid_email passed")

if __name__ == "__main__":
    test_validate_email_valid()
    test_validate_email_invalid()
    test_validate_password_weak()
    test_validate_password_strong()
    test_register_success()
    test_register_invalid_email()
    print("\n🎉 All register tests passed!")
EOF
```

### 5.4 ตรวจสอบโครงสร้างและ Commit

```bash
# ดูโครงสร้าง
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── main.py
├── src
│   ├── __init__.py
│   ├── auth
│   │   └── register.py
│   └── utils.py
└── tests
    ├── test_register.py
    └── test_utils.py

3 directories, 7 files
```

```bash
# Commit
git add .
git commit -m "feat: เพิ่มระบบ Register พร้อม validation"

# ดู log
git log --oneline
```

---

## 📝 แบบฝึกหัดที่ 6: Detached HEAD State

### 6.1 ทำความเข้าใจ HEAD

**HEAD** คือตัวชี้ที่บอกว่าเราอยู่ที่ไหนใน Git history

```
       HEAD
        ↓
       main
        ↓
A---B---C---D
```

```bash
# ดูว่า HEAD ชี้ไปที่ไหน
cat .git/HEAD
```

**ผลลัพธ์ที่คาดหวัง:**
```
ref: refs/heads/feature-register
```

### 6.2 เข้าสู่สถานะ Detached HEAD

```bash
# กลับไป main ก่อน
git switch main

# ดู log เพื่อหา commit hash
git log --oneline

# checkout ไปที่ commit ใด commit หนึ่ง (ใช้ hash จาก log ของคุณ)
git checkout abc1234
```

**ผลลัพธ์ที่คาดหวัง:**
```
Note: switching to 'abc1234'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

...
```

### 6.3 ทำความเข้าใจ Detached HEAD

```
            main
              ↓
A---B---C---D
    ↑
   HEAD (detached)
```

```bash
# ดู HEAD ตอนนี้
cat .git/HEAD
```

**ผลลัพธ์ที่คาดหวัง:**
```
abc1234567890...  (commit hash โดยตรง ไม่ใช่ reference)
```

```bash
# ดูสถานะ
git status

# ดูโครงสร้างไฟล์ ณ จุดนั้น
tree
```

### 6.4 สิ่งที่ทำได้ใน Detached HEAD

```bash
# ดูไฟล์ในเวอร์ชันเก่า
cat README.md

# สร้าง branch จากจุดนี้ถ้าต้องการ
git switch -c old-version-branch

# หรือกลับไป branch เดิม
git switch main
```

### 6.5 ออกจาก Detached HEAD

```bash
# กลับไป branch main
git switch main

# ตรวจสอบสถานะ
git status

# ดูโครงสร้าง
tree
```

> ⚠️ **คำเตือน:** ถ้าคุณ commit ใน Detached HEAD แล้วสลับออกไป commits เหล่านั้นอาจหายได้ ควรสร้าง branch ก่อน

---

## 📝 แบบฝึกหัดที่ 7: การเปลี่ยนชื่อ Branch

### 7.1 เปลี่ยนชื่อ Branch ปัจจุบัน

```bash
# ไปที่ branch ที่ต้องการเปลี่ยนชื่อ
git switch bugfix-navbar

# เปลี่ยนชื่อ branch ปัจจุบัน
git branch -m fix-navbar

# ตรวจสอบ
git branch

# ดูการเปลี่ยนแปลงใน .git/refs/heads
tree .git/refs/heads
```

**ผลลัพธ์ที่คาดหวัง:**
```
.git/refs/heads
├── feature-dashboard
├── feature-login
├── feature-profile
├── feature-register
├── fix-navbar          <-- ชื่อใหม่
├── hotfix-security
└── main
```

### 7.2 เปลี่ยนชื่อ Branch อื่น (ไม่ต้องไปอยู่ที่ branch นั้น)

```bash
# กลับไป main
git switch main

# เปลี่ยนชื่อ hotfix-security เป็น security-patch
git branch -m hotfix-security security-patch

# ตรวจสอบ
git branch

# ดูการเปลี่ยนแปลง
tree .git/refs/heads
```

---

## 📝 แบบฝึกหัดที่ 8: การลบ Branch

### 8.1 ลบ Branch ที่ไม่มี Commit ใหม่

```bash
# ใช้ -d (delete) สำหรับ branch ที่ไม่มี commit ใหม่
git branch -d fix-navbar

# ตรวจสอบ
git branch

# ดู refs ว่าหายไปแล้ว
tree .git/refs/heads
```

**ผลลัพธ์ที่คาดหวัง:**
```
Deleted branch fix-navbar (was abc1234).
```

### 8.2 ลบ Branch ที่มี Commit ยังไม่ได้ Merge (บังคับลบ)

```bash
# ลอง commit อะไรบางอย่างใน feature-dashboard
git switch feature-dashboard

# สร้างไฟล์ใหม่ด้วย heredoc
cat > src/dashboard.py << 'EOF'
"""
Dashboard Module
หน้า Dashboard สำหรับแสดงข้อมูลสรุป
"""

def show_dashboard():
    """แสดง Dashboard หลัก"""
    print("╔════════════════════════════╗")
    print("║       DASHBOARD            ║")
    print("╠════════════════════════════╣")
    print("║  Welcome to the dashboard! ║")
    print("╚════════════════════════════╝")

def get_stats():
    """ดึงข้อมูลสถิติ"""
    return {
        'users': 100,
        'active': 50,
        'revenue': 5000,
        'growth': '15%'
    }

def display_stats():
    """แสดงสถิติ"""
    stats = get_stats()
    print("\n📊 Statistics:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

if __name__ == "__main__":
    show_dashboard()
    display_stats()
EOF
```

```bash
# ดูโครงสร้าง
tree src

# Commit
git add .
git commit -m "feat: เพิ่ม dashboard module"

# กลับไป main
git switch main

# ลองลบด้วย -d (จะ error เพราะยังไม่ merge)
git branch -d feature-dashboard
```

**ผลลัพธ์ที่คาดหวัง:**
```
error: The branch 'feature-dashboard' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature-dashboard'.
```

```bash
# ใช้ -D (force delete) ถ้าแน่ใจว่าต้องการลบ
git branch -D feature-dashboard

# ตรวจสอบ
git branch
```

> ⚠️ **คำเตือน:** ใช้ `-D` ด้วยความระมัดระวัง เพราะจะลบ commits ที่ยังไม่ได้ merge ไปด้วย

---

## 📝 แบบฝึกหัดที่ 9: Remote Branch

### 9.1 เตรียม Remote Repository

สำหรับแบบฝึกหัดนี้ คุณต้องมี GitHub account และสร้าง repository ใหม่

```bash
# เพิ่ม remote (แทนที่ URL ด้วยของคุณ)
git remote add origin https://github.com/YOUR_USERNAME/git-branch-lab.git

# ตรวจสอบ remote
git remote -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
origin  https://github.com/YOUR_USERNAME/git-branch-lab.git (fetch)
origin  https://github.com/YOUR_USERNAME/git-branch-lab.git (push)
```

### 9.2 Push Branch ไป Remote

```bash
# Push main ไป remote
git push -u origin main
```

**ผลลัพธ์ที่คาดหวัง:**
```
Enumerating objects: 3, done.
...
To https://github.com/YOUR_USERNAME/git-branch-lab.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

```bash
# Push feature-login ไป remote
git push -u origin feature-login

# ดู branch ทั้งหมด (local และ remote)
git branch -a

# ดูโครงสร้าง refs รวม remote
tree .git/refs
```

**ผลลัพธ์ที่คาดหวัง:**
```
.git/refs
├── heads
│   ├── feature-login
│   ├── feature-register
│   └── main
├── remotes
│   └── origin
│       ├── feature-login
│       └── main
└── tags
```

### 9.3 ดึง Remote Branch มาทำงาน

```bash
# ดึงข้อมูลจาก remote
git fetch origin

# ดู remote branch ทั้งหมด
git branch -r

# ใช้ Pipeline กรอง remote branch
git branch -r | grep "feature"
```

**ผลลัพธ์ที่คาดหวัง:**
```
  origin/feature-login
```

```bash
# สร้าง local branch จาก remote branch
git switch -c feature-from-remote origin/feature-login

# หรือใช้วิธีสั้น ๆ (Git จะหา remote branch ให้อัตโนมัติ)
git switch feature-login
```

### 9.4 Push Branch ใหม่ไป Remote

```bash
# ไปที่ branch ที่ต้องการ push
git switch feature-register

# Push ไป remote
git push -u origin feature-register

# ตรวจสอบ
git branch -a

# ดู refs
tree .git/refs/remotes
```

### 9.5 เปลี่ยนชื่อ Remote Branch

```bash
# ไปที่ branch นั้นก่อน
git switch feature-register

# ขั้นตอนที่ 1: เปลี่ยนชื่อ local branch
git branch -m feature-signup

# ขั้นตอนที่ 2: ลบ remote branch เก่า
git push origin --delete feature-register

# ขั้นตอนที่ 3: Push branch ใหม่
git push -u origin feature-signup

# ดูผลลัพธ์
tree .git/refs/remotes/origin
```

### 9.6 ลบ Remote Branch

```bash
# วิธีที่ 1
git push origin --delete feature-login

# วิธีที่ 2 (ใช้ : หน้าชื่อ branch)
git push origin :feature-login

# อัพเดท remote tracking branches
git fetch --prune

# ตรวจสอบ
tree .git/refs/remotes/origin
```

---

## 📝 แบบฝึกหัดที่ 10: คำสั่งที่มีประโยชน์อื่น ๆ

### 10.1 ดู Branch พร้อม Commit ล่าสุด

```bash
git branch -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login   def5678 feat: เพิ่มระบบ Login พร้อม tests
  feature-signup  ghi9012 feat: เพิ่มระบบ Register พร้อม validation
* main            abc1234 Initial commit: สร้างโครงสร้างโปรเจกต์
```

### 10.2 ดู Branch ที่ Merge แล้ว/ยังไม่ Merge

```bash
# Branch ที่ merge เข้า main แล้ว
git branch --merged main

# Branch ที่ยังไม่ได้ merge
git branch --no-merged main
```

### 10.3 ดู Branch Tracking

```bash
git branch -vv
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login   def5678 [origin/feature-login] feat: เพิ่มระบบ Login
* main            abc1234 [origin/main] Initial commit
```

### 10.4 ดู Log แบบ Graph

```bash
# ดู log ทุก branch แบบ graph
git log --oneline --graph --all

# ดูแบบสวยงาม
git log --oneline --graph --all --decorate
```

**ผลลัพธ์ที่คาดหวัง:**
```
* def5678 (feature-login) feat: เพิ่มระบบ Login พร้อม tests
| * ghi9012 (feature-signup) feat: เพิ่มระบบ Register พร้อม validation
|/
* abc1234 (HEAD -> main, origin/main) Initial commit: สร้างโครงสร้างโปรเจกต์
```

### 10.5 ใช้ Pipeline กับ Git Log

```bash
# นับจำนวน commit ทั้งหมด
git log --oneline | wc -l

# ค้นหา commit ที่มีคำว่า "feat"
git log --oneline | grep "feat"

# ดู 5 commit ล่าสุดที่เป็น feature
git log --oneline | grep "feat" | head -5
```

**อธิบายตัวอย่างสุดท้าย:**
```
git log --oneline    →  แสดง commit ทั้งหมด
        |
        ↓
grep "feat"          →  กรองเฉพาะ commit ที่มี "feat"
        |
        ↓
head -5              →  เอาแค่ 5 อันแรก
```

### 10.6 สร้างไฟล์ .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
venv/
.env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/
EOF
```

```bash
# ตรวจสอบ
cat .gitignore

# Commit
git add .gitignore
git commit -m "chore: เพิ่ม .gitignore"
```

### 10.7 ใช้ tree ร่วมกับ .gitignore

```bash
# ดูโครงสร้างโดยไม่รวมไฟล์ที่อยู่ใน .gitignore
tree -I '__pycache__|*.pyc|.git|venv|.env'

# หรือดูเฉพาะไฟล์ที่ git track
git ls-files | head -20
```

---

## 📋 สรุปคำสั่งสำคัญ

### คำสั่ง Linux พื้นฐาน

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `cat > file << 'EOF'` | สร้างไฟล์หลายบรรทัด (heredoc) |
| `cat >> file << 'EOF'` | เพิ่มต่อท้ายไฟล์ (heredoc) |
| `cat file` | อ่านเนื้อหาไฟล์ |
| `echo "text" > file` | เขียนบรรทัดเดียว (ทับ) |
| `echo "text" >> file` | เขียนบรรทัดเดียว (ต่อท้าย) |
| `tree` | ดูโครงสร้างไฟล์และโฟลเดอร์ |
| `tree -a` | ดูรวม hidden files |
| `tree -L 2` | ดูแค่ 2 ระดับ |
| `cmd1 \| cmd2` | Pipeline: ส่ง output ไปเป็น input |
| `grep "text"` | กรองบรรทัดที่มีข้อความ |
| `wc -l` | นับจำนวนบรรทัด |
| `head -n` | เอา n บรรทัดแรก |
| `tail -n` | เอา n บรรทัดสุดท้าย |

### การจัดการ Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch` | ดูรายการ local branch |
| `git branch -a` | ดูรายการ local และ remote branch |
| `git branch -v` | ดู branch พร้อม commit ล่าสุด |
| `git branch <n>` | สร้าง branch ใหม่ |
| `git branch -d <n>` | ลบ branch (ที่ merge แล้ว) |
| `git branch -D <n>` | บังคับลบ branch |
| `git branch -m <new-name>` | เปลี่ยนชื่อ branch ปัจจุบัน |
| `git branch -m <old> <new>` | เปลี่ยนชื่อ branch อื่น |

### การสลับ Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git switch <branch>` | สลับไป branch (แนะนำ) |
| `git switch -c <branch>` | สร้างและสลับไป branch ใหม่ |
| `git checkout <branch>` | สลับไป branch (วิธีเก่า) |
| `git checkout -b <branch>` | สร้างและสลับไป branch ใหม่ |

### Remote Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch -r` | ดู remote branch |
| `git fetch origin` | ดึงข้อมูล remote |
| `git push -u origin <branch>` | Push branch ไป remote |
| `git push origin --delete <branch>` | ลบ remote branch |
| `git fetch --prune` | ลบ remote tracking ที่ไม่มีอยู่แล้ว |

---

## 🧪 แบบทดสอบความเข้าใจ

ลองตอบคำถามเหล่านี้:

1. **คำสั่งใดใช้สร้าง branch ใหม่และสลับไปพร้อมกัน?**

2. **Detached HEAD คืออะไร? และเกิดขึ้นเมื่อไหร่?**

3. **ความแตกต่างระหว่าง `git branch -d` และ `git branch -D` คืออะไร?**

4. **จะลบ remote branch ได้อย่างไร?**

5. **`git switch` ต่างจาก `git checkout` อย่างไร?**

6. **Pipeline (`|`) ทำหน้าที่อะไร?**

7. **คำสั่ง `git branch | grep "feature" | wc -l` ทำอะไร?**

8. **Git เก็บข้อมูล branch ไว้ที่ไหน?**

<details>
<summary>💡 คลิกเพื่อดูเฉลย</summary>

1. `git switch -c <branch-name>` หรือ `git checkout -b <branch-name>`

2. Detached HEAD คือสถานะที่ HEAD ชี้ไปที่ commit โดยตรง ไม่ได้ชี้ผ่าน branch เกิดขึ้นเมื่อ checkout ไปที่ commit hash โดยตรง

3. `-d` ลบได้เฉพาะ branch ที่ merge แล้วหรือไม่มี commit ใหม่ ส่วน `-D` บังคับลบแม้ยังไม่ได้ merge

4. `git push origin --delete <branch-name>` หรือ `git push origin :<branch-name>`

5. `git switch` ใช้สำหรับสลับ branch เท่านั้น ปลอดภัยกว่า ส่วน `git checkout` ทำได้หลายอย่าง (สลับ branch, กู้ไฟล์) อาจทำให้สับสน

6. Pipeline ส่ง output จากคำสั่งซ้ายไปเป็น input ของคำสั่งขวา

7. นับจำนวน branch ที่มีคำว่า "feature" ในชื่อ
   - `git branch` แสดงรายชื่อ branch ทั้งหมด
   - `grep "feature"` กรองเฉพาะบรรทัดที่มี "feature"
   - `wc -l` นับจำนวนบรรทัด

8. Git เก็บ branch ไว้ใน `.git/refs/heads/` โดยแต่ละไฟล์เก็บ commit hash ที่ branch นั้นชี้ไป

</details>

---

## 🎯 แบบฝึกหัดเพิ่มเติม

### Challenge 1: สร้างโครงสร้างโปรเจกต์

ลองสร้างโครงสร้างต่อไปนี้ด้วย `mkdir` และ `cat > file << 'EOF'`:

```
my-web-app/
├── README.md
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   └── models/
│       ├── __init__.py
│       └── user.py
├── static/
│   └── css/
│       └── style.css
└── tests/
    └── test_app.py
```

### Challenge 2: Branch Workflow

1. สร้าง branch ใหม่ชื่อ `feature-api`
2. เพิ่มไฟล์ `src/api.py` ด้วย heredoc
3. Commit การเปลี่ยนแปลง
4. เปลี่ยนชื่อ branch เป็น `feature-rest-api`
5. กลับไป main
6. ลบ branch นั้น (ใช้ -D)

### Challenge 3: Pipeline Challenge

เขียนคำสั่ง Pipeline เพื่อ:
1. นับจำนวนไฟล์ `.py` ในโปรเจกต์
2. หา commit ที่มีคำว่า "fix" ใน 10 commit ล่าสุด
3. นับจำนวน branch ที่ชื่อขึ้นต้นด้วย "feature"

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (Interactive)](https://learngitbranching.js.org/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Linux Pipe Tutorial](https://www.geeksforgeeks.org/piping-in-unix-or-linux/)

---

## ✅ Checklist ก่อนจบ LAB

- [ ] เข้าใจการใช้ Pipeline (`|`) และสามารถใช้งานได้
- [ ] ใช้ Here Document (`cat > file << 'EOF'`) สร้างไฟล์ได้
- [ ] ใช้ `tree` ตรวจสอบโครงสร้างโปรเจกต์ได้
- [ ] ใช้ `tree .git/refs` ดูโครงสร้าง branch ของ Git ได้
- [ ] สร้าง branch ใหม่ได้
- [ ] สลับ branch ด้วย `git switch` และ `git checkout` ได้
- [ ] เข้าใจ Detached HEAD และรู้วิธีออก
- [ ] เปลี่ยนชื่อ branch ได้
- [ ] ลบ branch ได้ทั้ง local และ remote
- [ ] Push และ track remote branch ได้
- [ ] ใช้ `git log --graph` ดูโครงสร้าง branch ได้
- [ ] ใช้ Pipeline กับคำสั่ง git ได้ (เช่น `git branch | grep "feature"`)

---

