# 🎓 LAB: Git Branch, Merge และ Conflict Resolution

## 📋 สารบัญ
- [ภาพรวม Pipeline](#-ภาพรวม-pipeline)
- [วัตถุประสงค์การเรียนรู้](#-วัตถุประสงค์การเรียนรู้)
- [ความรู้พื้นฐานที่ต้องมี](#-ความรู้พื้นฐานที่ต้องมี)
- [Part 1: เตรียมสภาพแวดล้อม](#-part-1-เตรียมสภาพแวดล้อม)
- [Part 2: Git Branch พื้นฐาน](#-part-2-git-branch-พื้นฐาน)
- [Part 3: Git Merge แบบ Fast-Forward](#-part-3-git-merge-แบบ-fast-forward)
- [Part 4: Git Merge แบบ 3-Way Merge](#-part-4-git-merge-แบบ-3-way-merge)
- [Part 5: Merge Conflict และการแก้ไข](#-part-5-merge-conflict-และการแก้ไข)
- [Part 6: Remote Branch](#-part-6-remote-branch)
- [Part 7: แบบฝึกหัดรวม](#-part-7-แบบฝึกหัดรวม)
- [สรุปคำสั่งที่ใช้](#-สรุปคำสั่งที่ใช้)

---

## 🗺️ ภาพรวม Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🎯 LAB Git Branch & Merge Pipeline                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Part 1    │    │   Part 2    │    │   Part 3    │    │   Part 4    │
│  เตรียม     │───▶│  Branch     │───▶│ Fast-Forward│───▶│  3-Way      │
│ สภาพแวดล้อม │    │  พื้นฐาน    │    │   Merge     │    │   Merge     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                               │
     ┌─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Part 5    │    │   Part 6    │    │   Part 7    │
│   Merge     │───▶│   Remote    │───▶│ แบบฝึกหัด  │
│  Conflict   │    │   Branch    │    │    รวม     │
└─────────────┘    └─────────────┘    └─────────────┘


╔═════════════════════════════════════════════════════════════════════════════════╗
║                           📊 รายละเอียด Pipeline                                ║
╠═════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║  Part 1: เตรียมสภาพแวดล้อม                                                      ║
║  ├── สร้างโปรเจค                                                                ║
║  ├── ตั้งค่า Git config                                                         ║
║  └── สร้างไฟล์เริ่มต้น                                                          ║
║                                                                                 ║
║  Part 2: Git Branch พื้นฐาน                                                     ║
║  ├── git branch (สร้าง/ดู branch)                                               ║
║  ├── git switch (สลับ branch)                                                   ║
║  ├── git checkout (วิธีดั้งเดิม)                                                ║
║  └── git branch -d (ลบ branch)                                                  ║
║                                                                                 ║
║  Part 3: Fast-Forward Merge                                                     ║
║  ├── สร้าง feature branch                                                       ║
║  ├── ทำงานบน feature branch                                                     ║
║  └── merge กลับ main (ไม่มี diverge)                                            ║
║                                                                                 ║
║  Part 4: 3-Way Merge                                                            ║
║  ├── สร้าง 2 branches ที่ diverge                                               ║
║  ├── แก้ไขไฟล์คนละส่วน                                                          ║
║  └── merge โดยไม่มี conflict                                                    ║
║                                                                                 ║
║  Part 5: Merge Conflict ⭐ (เน้น)                                                ║
║  ├── Conflict แบบ Single File                                                   ║
║  ├── Conflict แบบ Multiple Files                                                ║
║  ├── วิธีแก้ไข Conflict ด้วยมือ                                                 ║
║  ├── ใช้ git mergetool                                                          ║
║  └── Abort merge ด้วย git merge --abort                                         ║
║                                                                                 ║
║  Part 6: Remote Branch                                                          ║
║  ├── git remote (เชื่อมต่อ remote)                                              ║
║  ├── git push (ส่งขึ้น remote)                                                  ║
║  ├── git fetch vs git pull                                                      ║
║  └── Tracking branch                                                            ║
║                                                                                 ║
║  Part 7: แบบฝึกหัดรวม                                                           ║
║  └── จำลองการทำงานเป็นทีม                                                       ║
║                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════╝
```

### 🔄 Flow การทำงานของ Branch และ Merge

```
                    ┌─────────────────────────────────────────────────────┐
                    │              Git Branch & Merge Flow                │
                    └─────────────────────────────────────────────────────┘

    main           feature-A        feature-B         ผลลัพธ์หลัง merge
      │                │                │                    │
      │                │                │                    │
    [C1]───────────────┼────────────────┼──────────────────[C1]
      │                │                │                    │
      │    สร้าง branch│                │                    │
      ├───────────────▶●                │                    │
      │               [C2]              │                    │
      │                │                │                    │
      │                │    สร้าง branch│                    │
      ├────────────────┼───────────────▶●                    │
      │                │               [C3]                  │
      │                │                │                    │
      │               [C4]              │                    │
      │                │               [C5]                  │
      │                │                │                    │
      │◀───────────────┤                │         Fast-Forward
      │    merge       │                │         หรือ 3-Way
    [C4]               │                │                [C4]
      │                │                │                    │
      │◀───────────────┼────────────────┤                    │
      │                     merge                      Merge Commit
    [C6]─────────────────────────────────────────────────[C6]
      │                                                      │
      ▼                                                      ▼


    Legend:
    ● = Commit
    ─▶ = Branch creation
    ◀─ = Merge
```

---

## 🎯 วัตถุประสงค์การเรียนรู้

หลังจากทำ LAB นี้เสร็จ นักศึกษาจะสามารถ:

| ลำดับ | ทักษะ | รายละเอียด |
|-------|-------|------------|
| 1 | **Git Branch** | สร้าง, ดู, ลบ และจัดการ branch ได้ |
| 2 | **Git Switch/Checkout** | สลับไปมาระหว่าง branch ได้อย่างคล่องแคล่ว |
| 3 | **Fast-Forward Merge** | เข้าใจและทำ merge แบบ fast-forward |
| 4 | **3-Way Merge** | เข้าใจและทำ merge เมื่อมี diverging branches |
| 5 | **Merge Conflict** | ระบุ, เข้าใจ และแก้ไข conflict ได้ |
| 6 | **Local vs Remote** | เข้าใจความแตกต่างและจัดการทั้งสองแบบ |
| 7 | **Team Workflow** | ประยุกต์ใช้ในการทำงานเป็นทีม |

---

## 📚 ความรู้พื้นฐานที่ต้องมี

- ✅ เข้าใจ Git basics (`git init`, `git add`, `git commit`)
- ✅ ใช้งาน Command Line ได้
- ✅ มี Git ติดตั้งในเครื่องแล้ว

---

## 🔧 Part 1: เตรียมสภาพแวดล้อม

### Step 1.1: สร้างโฟลเดอร์โปรเจค

```bash
# สร้างโฟลเดอร์สำหรับ LAB
mkdir -p ~/git-lab-branch-merge
cd ~/git-lab-branch-merge

# ตรวจสอบตำแหน่งปัจจุบัน
pwd
```

**ผลลัพธ์ที่คาดหวัง:**
```
/home/<username>/git-lab-branch-merge
```

### Step 1.2: ตั้งค่า Git Config

```bash
# ตั้งค่าชื่อและอีเมล (ถ้ายังไม่ได้ตั้ง)
git config --global user.name "ชื่อ-นามสกุล"
git config --global user.email "your-email@example.com"

# ตรวจสอบการตั้งค่า
git config --list | grep user
```

**ผลลัพธ์ที่คาดหวัง:**
```
user.name=ชื่อ-นามสกุล
user.email=your-email@example.com
```

### Step 1.3: Initialize Git Repository

```bash
# สร้าง Git repository
git init

# ตรวจสอบสถานะ
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in /home/<username>/git-lab-branch-merge/.git/
```

### Step 1.4: สร้างโครงสร้างโปรเจคเริ่มต้น

```bash
# สร้างโฟลเดอร์โครงสร้าง
mkdir -p src docs tests

# ใช้ tree ดูโครงสร้าง
tree -a -L 2
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── .git
│   ├── HEAD
│   ├── config
│   ├── ...
├── docs
├── src
└── tests
```

### Step 1.5: สร้างไฟล์เริ่มต้นด้วย cat และ EOF

```bash
# สร้างไฟล์ README.md
cat > README.md << 'EOF'
# My Project

โปรเจคนี้สร้างขึ้นเพื่อเรียนรู้ Git Branch และ Merge

## Features
- Feature A
- Feature B

## การติดตั้ง
```bash
git clone <repository-url>
```

## ผู้พัฒนา
- นักศึกษา KMITL
EOF

# ตรวจสอบไฟล์ที่สร้าง
cat README.md
```

### Step 1.6: สร้างไฟล์ Source Code

```bash
# สร้างไฟล์ main.py
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application file
Version: 1.0.0
"""

def main():
    """Main function"""
    print("Hello, Git!")
    print("Welcome to Branch & Merge Lab")

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def calculate_product(a, b):
    """Calculate product of two numbers"""
    return a * b

if __name__ == "__main__":
    main()
EOF

# สร้างไฟล์ utils.py
cat > src/utils.py << 'EOF'
#!/usr/bin/env python3
"""
Utility functions
"""

def format_output(message):
    """Format output message"""
    return f">>> {message} <<<"

def validate_input(value):
    """Validate input value"""
    if value is None:
        return False
    return True
EOF

# สร้างไฟล์ config
cat > src/config.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration settings
"""

# Application settings
APP_NAME = "GitLabProject"
VERSION = "1.0.0"
DEBUG = False

# Database settings
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "mydb"
EOF
```

### Step 1.7: ตรวจสอบโครงสร้างโปรเจค

```bash
# ดูโครงสร้างไฟล์ทั้งหมด
tree -a -I '.git'
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── docs
├── src
│   ├── config.py
│   ├── main.py
│   └── utils.py
└── tests

3 directories, 4 files
```

### Step 1.8: Commit ครั้งแรก

```bash
# เพิ่มไฟล์ทั้งหมด
git add .

# ตรวจสอบสถานะ
git status

# Commit
git commit -m "Initial commit: Add project structure and basic files"

# ดูประวัติ
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
abc1234 (HEAD -> main) Initial commit: Add project structure and basic files
```

---

## 🌿 Part 2: Git Branch พื้นฐาน

### 📖 ทฤษฎี: Branch คืออะไร?

```
Branch = pointer ที่ชี้ไปยัง commit

                     HEAD
                       │
                       ▼
    main ──────▶ [Commit C1]
                       │
                       ▼
               [Commit C0 - Initial]

เมื่อสร้าง branch ใหม่:

                     HEAD (อยู่ที่ main)
                       │
                       ▼
    main ──────▶ [Commit C1] ◀────── feature (branch ใหม่)
                       │
                       ▼
               [Commit C0 - Initial]
```

### Step 2.1: ดู Branch ปัจจุบัน

```bash
# ดู branch ทั้งหมด
git branch

# ดูพร้อม commit ล่าสุด
git branch -v

# ดูทุก branch รวม remote
git branch -a
```

**ผลลัพธ์ที่คาดหวัง:**
```
* main
```

> 💡 **หมายเหตุ:** เครื่องหมาย `*` แสดง branch ที่เราอยู่ปัจจุบัน

### Step 2.2: สร้าง Branch ใหม่

```bash
# สร้าง branch ชื่อ feature-login
git branch feature-login

# ตรวจสอบ branch ทั้งหมด
git branch

# ดูรายละเอียดเพิ่มเติม
git branch -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
* main
```

### Step 2.3: สลับ Branch ด้วย git switch (แนะนำ)

```bash
# สลับไป feature-login
git switch feature-login

# ตรวจสอบว่าอยู่ branch ไหน
git branch

# ดู HEAD ชี้ไปที่ไหน
cat .git/HEAD
```

**ผลลัพธ์ที่คาดหวัง:**
```
* feature-login
  main
```

```
ref: refs/heads/feature-login
```

### Step 2.4: สลับ Branch ด้วย git checkout (วิธีดั้งเดิม)

```bash
# กลับไป main ด้วย checkout
git checkout main

# ตรวจสอบ
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
* main
```

### Step 2.5: สร้างและสลับ Branch ในคำสั่งเดียว

```bash
# วิธีใหม่ (แนะนำ)
git switch -c feature-register

# ตรวจสอบ
git branch

# กลับ main
git switch main

# วิธีเก่า
git checkout -b feature-dashboard

# ตรวจสอบ
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-dashboard
  feature-login
  feature-register
* main
```

### Step 2.6: ลบ Branch

```bash
# ลบ branch ที่ไม่ต้องการ
git branch -d feature-dashboard
git branch -d feature-register

# ตรวจสอบ
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Deleted branch feature-dashboard (was abc1234).
Deleted branch feature-register (was abc1234).
```

```
  feature-login
* main
```

### Step 2.7: ดูโครงสร้าง Branch ด้วย git log

```bash
# ดู branch ทั้งหมดในรูปแบบ graph
git log --oneline --graph --all

# ดูแบบละเอียด
git log --oneline --graph --all --decorate
```

**ผลลัพธ์ที่คาดหวัง:**
```
* abc1234 (HEAD -> main, feature-login) Initial commit: Add project structure and basic files
```

---

## 🔀 Part 3: Git Merge แบบ Fast-Forward

### 📖 ทฤษฎี: Fast-Forward Merge คืออะไร?

```
Fast-Forward Merge เกิดขึ้นเมื่อ:
- Branch ที่จะ merge ไม่มี commits ใหม่
- Git แค่ย้าย pointer ไปข้างหน้า

ก่อน Merge:
                            HEAD
                              │
    main ────────────────────▶●
                              │
                              │     feature-login
                              │          │
                              │          ▼
                              └────●────●────●
                                  C2   C3   C4

หลัง Fast-Forward Merge:
                                              HEAD
                                                │
    main ──────────────────────────────────────▶●
                                                │
                                          feature-login
                                                │
    ●────●────●────●                            │
   C1   C2   C3   C4 ◀──────────────────────────┘

(Git แค่ย้าย main pointer มาที่ C4)
```

### Step 3.1: เตรียม Branch สำหรับ Fast-Forward

```bash
# ตรวจสอบว่าอยู่ที่ main
git switch main

# ดูสถานะปัจจุบัน
git log --oneline --graph --all
```

### Step 3.2: สลับไป feature-login และเพิ่มไฟล์

```bash
# สลับไป feature-login
git switch feature-login

# สร้างไฟล์ login
cat > src/login.py << 'EOF'
#!/usr/bin/env python3
"""
Login module
"""

class LoginManager:
    """Manage user login"""
    
    def __init__(self):
        self.logged_in_users = []
    
    def login(self, username, password):
        """Login user"""
        # Simple validation
        if username and password:
            self.logged_in_users.append(username)
            return True
        return False
    
    def logout(self, username):
        """Logout user"""
        if username in self.logged_in_users:
            self.logged_in_users.remove(username)
            return True
        return False
    
    def is_logged_in(self, username):
        """Check if user is logged in"""
        return username in self.logged_in_users

# Testing
if __name__ == "__main__":
    manager = LoginManager()
    print(manager.login("admin", "password123"))
    print(manager.is_logged_in("admin"))
EOF

# ตรวจสอบไฟล์
tree src/
```

**ผลลัพธ์ที่คาดหวัง:**
```
src/
├── config.py
├── login.py
├── main.py
└── utils.py
```

### Step 3.3: Commit การเปลี่ยนแปลง

```bash
# Add และ commit
git add src/login.py
git commit -m "Add login module with LoginManager class"

# ดูประวัติ
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
* def5678 (HEAD -> feature-login) Add login module with LoginManager class
* abc1234 (main) Initial commit: Add project structure and basic files
```

### Step 3.4: เพิ่ม Commit อีกหนึ่ง

```bash
# เพิ่มฟังก์ชันใน login.py
cat >> src/login.py << 'EOF'

def validate_password(password):
    """
    Validate password strength
    - At least 8 characters
    - Contains number
    """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
EOF

# Commit
git add src/login.py
git commit -m "Add password validation function"

# ดูประวัติ
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
* ghi9012 (HEAD -> feature-login) Add password validation function
* def5678 Add login module with LoginManager class
* abc1234 (main) Initial commit: Add project structure and basic files
```

### Step 3.5: ทำ Fast-Forward Merge

```bash
# กลับไป main
git switch main

# ตรวจสอบว่า main ยังอยู่ที่ commit เดิม
git log --oneline -1

# Merge feature-login เข้า main
git merge feature-login

# ดูผลลัพธ์
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
Updating abc1234..ghi9012
Fast-forward
 src/login.py | 45 +++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 45 insertions(+)
 create mode 100644 src/login.py
```

```
* ghi9012 (HEAD -> main, feature-login) Add password validation function
* def5678 Add login module with LoginManager class
* abc1234 Initial commit: Add project structure and basic files
```

> 💡 **สังเกต:** Git บอกว่า "Fast-forward" และ main ถูกย้ายมาที่ commit เดียวกับ feature-login

### Step 3.6: ตรวจสอบโครงสร้างไฟล์

```bash
# ดูโครงสร้างไฟล์
tree -I '.git'

# ตรวจสอบไฟล์ login.py
cat src/login.py | head -20
```

---

## 🔀 Part 4: Git Merge แบบ 3-Way Merge

### 📖 ทฤษฎี: 3-Way Merge คืออะไร?

```
3-Way Merge เกิดขึ้นเมื่อ:
- ทั้งสอง branch มี commits ที่แยกออกจากกัน (diverged)
- Git ต้องสร้าง merge commit ใหม่

ก่อน Merge:
                    ●────●  (feature-api)
                   /   C3  C4
                  /
    ●────●────●────●────●  (main)
   C0   C1  (base)  C5   C6

หลัง 3-Way Merge:
                    ●────●
                   /       \
                  /         \
    ●────●────●────●────●────●  (main + feature-api merged)
   C0   C1  base  C5   C6  (Merge Commit)
                            │
                            └── รวมการเปลี่ยนแปลงจากทั้งสอง branch
```

### Step 4.1: สร้าง Branch ใหม่สำหรับ API

```bash
# ตรวจสอบว่าอยู่ที่ main
git switch main

# สร้าง branch ใหม่
git switch -c feature-api

# ตรวจสอบ
git branch
```

### Step 4.2: เพิ่มไฟล์ API ใน feature-api

```bash
# สร้างไฟล์ api.py
cat > src/api.py << 'EOF'
#!/usr/bin/env python3
"""
API module for handling HTTP requests
"""

import json

class APIHandler:
    """Handle API requests"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    def get(self, endpoint):
        """GET request"""
        url = f"{self.base_url}/{endpoint}"
        return {"method": "GET", "url": url}
    
    def post(self, endpoint, data):
        """POST request"""
        url = f"{self.base_url}/{endpoint}"
        return {"method": "POST", "url": url, "data": data}
    
    def format_response(self, response):
        """Format API response"""
        return json.dumps(response, indent=2)

if __name__ == "__main__":
    api = APIHandler()
    print(api.get("users"))
    print(api.post("users", {"name": "John"}))
EOF

# Commit
git add src/api.py
git commit -m "Add API handler module"

# ดูประวัติ
git log --oneline --graph --all
```

### Step 4.3: เพิ่ม Commit อีกใน feature-api

```bash
# สร้างไฟล์ tests
cat > tests/test_api.py << 'EOF'
#!/usr/bin/env python3
"""
Tests for API module
"""

import sys
sys.path.insert(0, '../src')

from api import APIHandler

def test_get():
    """Test GET request"""
    api = APIHandler()
    result = api.get("users")
    assert result["method"] == "GET"
    print("✓ test_get passed")

def test_post():
    """Test POST request"""
    api = APIHandler()
    result = api.post("users", {"name": "Test"})
    assert result["method"] == "POST"
    assert result["data"]["name"] == "Test"
    print("✓ test_post passed")

if __name__ == "__main__":
    test_get()
    test_post()
    print("\nAll tests passed!")
EOF

# Commit
git add tests/test_api.py
git commit -m "Add tests for API handler"
```

### Step 4.4: กลับไป main และเพิ่ม commits

```bash
# กลับไป main
git switch main

# ดูว่า main ไม่มีไฟล์ api.py
tree src/

# สร้างไฟล์ใหม่ใน main
cat > docs/README_DEV.md << 'EOF'
# Developer Guide

## การติดตั้ง Development Environment

1. Clone repository
```bash
git clone <repo-url>
cd <project>
```

2. สร้าง Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

## การรัน Tests
```bash
python -m pytest tests/
```

## Code Style
- ใช้ PEP 8
- ใช้ type hints
- เขียน docstrings
EOF

# Commit
git add docs/README_DEV.md
git commit -m "Add developer documentation"

# ดูประวัติ - สังเกตว่า branches diverged
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
* jkl3456 (HEAD -> main) Add developer documentation
| * mno7890 (feature-api) Add tests for API handler
| * pqr1234 Add API handler module
|/
* ghi9012 (feature-login) Add password validation function
* def5678 Add login module with LoginManager class
* abc1234 Initial commit: Add project structure and basic files
```

### Step 4.5: ทำ 3-Way Merge

```bash
# Merge feature-api เข้า main
git merge feature-api -m "Merge feature-api: Add API functionality"

# ดูผลลัพธ์
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
*   stu5678 (HEAD -> main) Merge feature-api: Add API functionality
|\
| * mno7890 (feature-api) Add tests for API handler
| * pqr1234 Add API handler module
* | jkl3456 Add developer documentation
|/
* ghi9012 (feature-login) Add password validation function
* def5678 Add login module with LoginManager class
* abc1234 Initial commit: Add project structure and basic files
```

> 💡 **สังเกต:** มี merge commit ใหม่เกิดขึ้น และ graph แสดงการรวม branches

### Step 4.6: ตรวจสอบผลลัพธ์

```bash
# ดูโครงสร้างไฟล์
tree -I '.git'

# ตรวจสอบว่ามีไฟล์จากทั้งสอง branch
ls -la src/
ls -la docs/
ls -la tests/
```

**ผลลัพธ์ที่คาดหวัง:**
```
.
├── README.md
├── docs
│   └── README_DEV.md
├── src
│   ├── api.py
│   ├── config.py
│   ├── login.py
│   ├── main.py
│   └── utils.py
└── tests
    └── test_api.py
```

---

## ⚠️ Part 5: Merge Conflict และการแก้ไข

### 📖 ทฤษฎี: Merge Conflict คืออะไร?

```
Merge Conflict เกิดขึ้นเมื่อ:
- ทั้งสอง branch แก้ไขไฟล์เดียวกัน ในบรรทัดเดียวกัน
- Git ไม่สามารถตัดสินใจได้ว่าจะเลือกเวอร์ชันไหน

         main                    feature-x
           │                         │
           ▼                         ▼
    ┌─────────────┐          ┌─────────────┐
    │ config.py   │          │ config.py   │
    │             │          │             │
    │ DEBUG=False │          │ DEBUG=True  │
    │             │          │             │
    └─────────────┘          └─────────────┘
           │                         │
           └──────────┬──────────────┘
                      │
                      ▼
              ❌ CONFLICT!
              ต้องเลือกว่าจะใช้
              DEBUG=False หรือ DEBUG=True


Conflict Markers ที่ Git ใส่ในไฟล์:
┌─────────────────────────────────────┐
│ <<<<<<< HEAD                        │  ← เริ่มต้น conflict (เวอร์ชันปัจจุบัน)
│ DEBUG = False                       │  ← โค้ดจาก branch ปัจจุบัน (main)
│ =======                             │  ← แบ่งระหว่างสอง versions
│ DEBUG = True                        │  ← โค้ดจาก branch ที่ merge เข้ามา
│ >>>>>>> feature-x                   │  ← สิ้นสุด conflict
└─────────────────────────────────────┘
```

### Step 5.1: เตรียม Scenario สำหรับ Conflict

```bash
# ตรวจสอบว่าอยู่ที่ main
git switch main

# ดูเนื้อหา config.py ปัจจุบัน
cat src/config.py
```

### Step 5.2: สร้าง Branch สำหรับ Development

```bash
# สร้าง branch สำหรับ development settings
git switch -c feature-dev-config

# แก้ไข config.py สำหรับ development
cat > src/config.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration settings
Updated for DEVELOPMENT environment
"""

# Application settings
APP_NAME = "GitLabProject"
VERSION = "1.1.0-dev"
DEBUG = True  # Enable debug for development

# Database settings - Development
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "mydb_dev"

# Development specific
LOG_LEVEL = "DEBUG"
CACHE_ENABLED = False
EOF

# Commit
git add src/config.py
git commit -m "Update config for development environment"
```

### Step 5.3: กลับไป main และแก้ไข config ต่างออกไป

```bash
# กลับไป main
git switch main

# แก้ไข config.py สำหรับ production
cat > src/config.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration settings
Updated for PRODUCTION environment
"""

# Application settings
APP_NAME = "GitLabProject"
VERSION = "1.1.0"
DEBUG = False  # Disable debug for production

# Database settings - Production
DB_HOST = "db.production.server"
DB_PORT = 5432
DB_NAME = "mydb_prod"

# Production specific
LOG_LEVEL = "ERROR"
CACHE_ENABLED = True
EOF

# Commit
git add src/config.py
git commit -m "Update config for production environment"

# ดูประวัติ
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
* vwx9012 (HEAD -> main) Update config for production environment
| * yza3456 (feature-dev-config) Update config for development environment
|/
*   stu5678 Merge feature-api: Add API functionality
...
```

### Step 5.4: พยายาม Merge และเจอ Conflict

```bash
# พยายาม merge feature-dev-config
git merge feature-dev-config
```

**ผลลัพธ์ที่คาดหวัง:**
```
Auto-merging src/config.py
CONFLICT (content): Merge conflict in src/config.py
Automatic merge failed; fix conflicts and then commit the result.
```

### Step 5.5: ตรวจสอบ Conflict

```bash
# ดูสถานะ
git status

# ดูเนื้อหาไฟล์ที่มี conflict
cat src/config.py
```

**ผลลัพธ์ที่คาดหวัง (git status):**
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   src/config.py
```

**ผลลัพธ์ที่คาดหวัง (cat src/config.py):**
```python
#!/usr/bin/env python3
"""
Configuration settings
<<<<<<< HEAD
Updated for PRODUCTION environment
=======
Updated for DEVELOPMENT environment
>>>>>>> feature-dev-config
"""

# Application settings
APP_NAME = "GitLabProject"
<<<<<<< HEAD
VERSION = "1.1.0"
DEBUG = False  # Disable debug for production
=======
VERSION = "1.1.0-dev"
DEBUG = True  # Enable debug for development
>>>>>>> feature-dev-config

# Database settings - Production
DB_HOST = "db.production.server"
...
```

### Step 5.6: วิธีที่ 1 - แก้ไข Conflict ด้วยมือ

```bash
# แก้ไขไฟล์ด้วย text editor หรือใช้ cat
cat > src/config.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration settings
Supports both DEVELOPMENT and PRODUCTION environments
"""
import os

# Environment detection
ENVIRONMENT = os.getenv("APP_ENV", "development")

# Application settings
APP_NAME = "GitLabProject"
VERSION = "1.1.0"

# Environment-specific settings
if ENVIRONMENT == "production":
    DEBUG = False
    DB_HOST = "db.production.server"
    DB_NAME = "mydb_prod"
    LOG_LEVEL = "ERROR"
    CACHE_ENABLED = True
else:
    DEBUG = True
    DB_HOST = "localhost"
    DB_NAME = "mydb_dev"
    LOG_LEVEL = "DEBUG"
    CACHE_ENABLED = False

# Common settings
DB_PORT = 5432
EOF

# ตรวจสอบไฟล์ที่แก้ไข
cat src/config.py
```

### Step 5.7: Complete the Merge

```bash
# Mark conflict as resolved
git add src/config.py

# ตรวจสอบสถานะ
git status

# Commit การแก้ไข conflict
git commit -m "Merge feature-dev-config: Combine dev and prod configs with environment detection"

# ดูประวัติ
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
*   bcd7890 (HEAD -> main) Merge feature-dev-config: Combine dev and prod configs
|\
| * yza3456 (feature-dev-config) Update config for development environment
* | vwx9012 Update config for production environment
|/
*   stu5678 Merge feature-api: Add API functionality
...
```

### Step 5.8: สร้าง Conflict แบบหลายไฟล์

```bash
# สร้าง branch ใหม่
git switch -c feature-ui

# แก้ไขหลายไฟล์
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application file
Version: 2.0.0 - With UI Support
"""

from ui import UserInterface

def main():
    """Main function with UI"""
    ui = UserInterface()
    ui.show_welcome()
    ui.show_menu()

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def calculate_product(a, b):
    """Calculate product of two numbers"""
    return a * b

if __name__ == "__main__":
    main()
EOF

cat > src/utils.py << 'EOF'
#!/usr/bin/env python3
"""
Utility functions - UI Edition
"""

def format_output(message):
    """Format output message with UI styling"""
    return f"┌{'─'*50}┐\n│ {message:^48} │\n└{'─'*50}┘"

def validate_input(value):
    """Validate input value"""
    if value is None:
        return False
    return True

def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
EOF

# Commit
git add .
git commit -m "Update main and utils for UI support"
```

```bash
# กลับไป main
git switch main

# แก้ไขไฟล์เดียวกันแต่ต่างออกไป
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application file
Version: 2.0.0 - With API Support
"""

from api import APIHandler

def main():
    """Main function with API"""
    api = APIHandler()
    print("Starting API server...")
    api.start()

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def calculate_product(a, b):
    """Calculate product of two numbers"""
    return a * b

def calculate_average(numbers):
    """Calculate average - New function"""
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    main()
EOF

cat > src/utils.py << 'EOF'
#!/usr/bin/env python3
"""
Utility functions - API Edition
"""

import json

def format_output(message):
    """Format output message as JSON"""
    return json.dumps({"message": message})

def validate_input(value):
    """Validate input value with type checking"""
    if value is None:
        return False, "Value cannot be None"
    if not isinstance(value, (str, int, float)):
        return False, "Invalid type"
    return True, "Valid"

def parse_json(data):
    """Parse JSON string"""
    return json.loads(data)
EOF

# Commit
git add .
git commit -m "Update main and utils for API support"
```

### Step 5.9: Merge และแก้ Conflict หลายไฟล์

```bash
# พยายาม merge
git merge feature-ui
```

**ผลลัพธ์ที่คาดหวัง:**
```
Auto-merging src/utils.py
CONFLICT (content): Merge conflict in src/utils.py
Auto-merging src/main.py
CONFLICT (content): Merge conflict in src/main.py
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
# ดูไฟล์ที่มี conflict
git status

# ดูรายการไฟล์ที่ conflict
git diff --name-only --diff-filter=U
```

### Step 5.10: แก้ไข Conflict ทีละไฟล์

```bash
# แก้ไข main.py - รวมทั้ง UI และ API
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main application file
Version: 2.0.0 - Full Featured (UI + API)
"""

from api import APIHandler

def main():
    """Main function with both UI and API support"""
    print("┌" + "─"*50 + "┐")
    print("│" + " Welcome to GitLabProject ".center(50) + "│")
    print("└" + "─"*50 + "┘")
    
    print("\nStarting services...")
    api = APIHandler()
    print("API ready!")

def calculate_sum(a, b):
    """Calculate sum of two numbers"""
    return a + b

def calculate_product(a, b):
    """Calculate product of two numbers"""
    return a * b

def calculate_average(numbers):
    """Calculate average"""
    return sum(numbers) / len(numbers)

def show_menu():
    """Show application menu"""
    print("\n1. API Mode")
    print("2. UI Mode")
    print("3. Exit")

if __name__ == "__main__":
    main()
    show_menu()
EOF

# Mark as resolved
git add src/main.py
```

```bash
# แก้ไข utils.py
cat > src/utils.py << 'EOF'
#!/usr/bin/env python3
"""
Utility functions - Combined Edition
"""

import json

def format_output(message, style="json"):
    """Format output message
    
    Args:
        message: The message to format
        style: 'json' or 'box'
    """
    if style == "json":
        return json.dumps({"message": message})
    else:
        return f"┌{'─'*50}┐\n│ {message:^48} │\n└{'─'*50}┘"

def validate_input(value, strict=False):
    """Validate input value
    
    Args:
        value: Value to validate
        strict: If True, also check type
    """
    if value is None:
        return (False, "Value cannot be None") if strict else False
    if strict and not isinstance(value, (str, int, float)):
        return False, "Invalid type"
    return (True, "Valid") if strict else True

def parse_json(data):
    """Parse JSON string"""
    return json.loads(data)

def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
EOF

# Mark as resolved
git add src/utils.py
```

### Step 5.11: Complete Multi-file Merge

```bash
# ตรวจสอบสถานะ
git status

# Commit
git commit -m "Merge feature-ui: Combine UI and API functionality"

# ดูประวัติ
git log --oneline --graph --all
```

### Step 5.12: ใช้ git merge --abort

```bash
# สร้าง scenario ใหม่สำหรับแสดง abort
git switch -c feature-test

# แก้ไขไฟล์
echo "# Test file" > tests/test_main.py
git add .
git commit -m "Add test main file"

# กลับ main และแก้ไขไฟล์เดียวกัน
git switch main
echo "# Main test file" > tests/test_main.py
git add .
git commit -m "Add main test file"

# Merge และเจอ conflict
git merge feature-test

# ถ้าไม่ต้องการ merge ต่อ สามารถ abort ได้
git merge --abort

# ตรวจสอบสถานะ - กลับมาเหมือนก่อน merge
git status
```

### Step 5.13: ใช้ git diff เพื่อดู Conflict

```bash
# สร้าง conflict ใหม่
git merge feature-test

# ดู conflict แบบละเอียด
git diff

# ดูเฉพาะชื่อไฟล์ที่ conflict
git diff --name-only --diff-filter=U

# ดูว่าแต่ละ side เปลี่ยนอะไร
git diff --ours    # ดูว่า our side (main) เปลี่ยนอะไร
git diff --theirs  # ดูว่า their side (feature-test) เปลี่ยนอะไร
```

### Step 5.14: แก้และ Commit

```bash
# แก้ไขไฟล์
cat > tests/test_main.py << 'EOF'
#!/usr/bin/env python3
"""
Test cases for main module
Combined from both branches
"""

import sys
sys.path.insert(0, '../src')

from main import calculate_sum, calculate_product, calculate_average

def test_calculate_sum():
    """Test sum function"""
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(-1, 1) == 0
    print("✓ test_calculate_sum passed")

def test_calculate_product():
    """Test product function"""
    assert calculate_product(2, 3) == 6
    assert calculate_product(0, 5) == 0
    print("✓ test_calculate_product passed")

def test_calculate_average():
    """Test average function"""
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0
    print("✓ test_calculate_average passed")

if __name__ == "__main__":
    test_calculate_sum()
    test_calculate_product()
    test_calculate_average()
    print("\n✅ All tests passed!")
EOF

# Complete merge
git add tests/test_main.py
git commit -m "Merge feature-test: Add comprehensive test cases"

# ดูประวัติ
git log --oneline --graph --all
```

---

## 🌐 Part 6: Remote Branch

### 📖 ทฤษฎี: Local vs Remote Branch

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Local vs Remote Branches                          │
└─────────────────────────────────────────────────────────────────────┘

Local Repository                     Remote Repository (GitHub/GitLab)
(เครื่องของเรา)                            (Server)
                                    
┌─────────────────────┐             ┌─────────────────────┐
│                     │   git push  │                     │
│  main ●────●────●   │ ─────────▶  │  main ●────●────●   │
│                     │             │                     │
│  feature-x ●────●   │             │  feature-x ●────●   │
│                     │             │                     │
│  (local branches)   │   git pull  │  (remote branches)  │
│                     │ ◀─────────  │                     │
└─────────────────────┘             └─────────────────────┘

Tracking Branches (origin/main, origin/feature-x):
- เป็น "snapshot" ของ remote branches
- อัพเดทเมื่อ git fetch/pull
- ใช้เปรียบเทียบกับ local branches


git fetch vs git pull:
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  git fetch:                                                      │
│  ┌───────┐         ┌───────────┐                                │
│  │Remote │ ──────▶ │origin/main│  (อัพเดท tracking branch)       │
│  │ main  │         └───────────┘                                │
│  └───────┘               │                                       │
│                          │  (local main ไม่เปลี่ยน)             │
│                          ▼                                       │
│                    ┌───────┐                                     │
│                    │ main  │  (ยังเหมือนเดิม)                    │
│                    └───────┘                                     │
│                                                                  │
│  git pull = git fetch + git merge:                               │
│  ┌───────┐         ┌───────────┐         ┌───────┐             │
│  │Remote │ ──────▶ │origin/main│ ──────▶ │ main  │             │
│  │ main  │         └───────────┘         └───────┘             │
│  └───────┘                                (merged!)              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Step 6.1: ดู Remote ที่เชื่อมต่อ

```bash
# ดู remote (ยังไม่มี)
git remote -v

# ดู remote branches
git branch -r

# ดูทุก branches (local + remote)
git branch -a
```

### Step 6.2: จำลอง Remote Repository (ใช้ local bare repo)

```bash
# สร้าง bare repository เพื่อจำลอง remote
cd ~
mkdir -p git-remote-simulation/my-project.git
cd git-remote-simulation/my-project.git
git init --bare

# กลับไปโปรเจคหลัก
cd ~/git-lab-branch-merge

# เพิ่ม remote
git remote add origin ~/git-remote-simulation/my-project.git

# ตรวจสอบ
git remote -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
origin  /home/<username>/git-remote-simulation/my-project.git (fetch)
origin  /home/<username>/git-remote-simulation/my-project.git (push)
```

### Step 6.3: Push Branch ไป Remote

```bash
# Push main branch
git push -u origin main

# ดู remote branches
git branch -r

# ดูทุก branches
git branch -a
```

**ผลลัพธ์ที่คาดหวัง:**
```
  remotes/origin/main
```

### Step 6.4: Push Branch อื่นไป Remote

```bash
# Push feature-login
git push -u origin feature-login

# Push feature-api
git push -u origin feature-api

# ดู remote branches
git branch -r
```

**ผลลัพธ์ที่คาดหวัง:**
```
  origin/feature-api
  origin/feature-login
  origin/main
```

### Step 6.5: สร้าง Branch จาก Remote

```bash
# สร้าง local branch ที่ track remote branch
git switch -c feature-from-remote origin/feature-login

# หรือใช้วิธีลัด
git switch --track origin/feature-api

# ดูการ tracking
git branch -vv
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-api          pqr1234 [origin/feature-api] Add API handler module
  feature-from-remote  ghi9012 [origin/feature-login] Add password validation function
  feature-login        ghi9012 [origin/feature-login] Add password validation function
* main                 xxx1234 [origin/main] Merge feature-test: Add comprehensive test cases
```

### Step 6.6: เข้าใจ git fetch

```bash
# กลับไป main
git switch main

# จำลองการเปลี่ยนแปลงบน remote
# (ปกติคนอื่นจะ push แต่เราจะจำลองเอง)
cd ~/git-remote-simulation/my-project.git

# ดู branches บน bare repo
git branch

# กลับไปโปรเจค
cd ~/git-lab-branch-merge

# ดู status ของ remote tracking
git status

# Fetch updates จาก remote
git fetch origin

# ดูความแตกต่าง
git log main..origin/main --oneline
```

### Step 6.7: เข้าใจ git pull

```bash
# git pull = git fetch + git merge
# ใช้เมื่อต้องการ fetch และ merge ในคำสั่งเดียว

# ดู help
git pull --help | head -20

# Pull จาก remote (ถ้ามีการเปลี่ยนแปลง)
git pull origin main
```

### Step 6.8: ลบ Remote Branch

```bash
# ลบ branch บน remote
git push origin --delete feature-from-remote

# ตรวจสอบ
git branch -r

# Clean up stale remote-tracking branches
git fetch --prune
```

### Step 6.9: ดูข้อมูล Remote แบบละเอียด

```bash
# ดูข้อมูล remote
git remote show origin

# ดู configuration
cat .git/config
```

---

## 🏋️ Part 7: แบบฝึกหัดรวม

### 📝 แบบฝึกหัดที่ 1: Feature Branch Workflow

**สถานการณ์:** ทีม 2 คนทำงานบน feature ต่างกัน

```bash
# เตรียมพื้นที่ทำงาน
cd ~/git-lab-branch-merge
git switch main

# === Developer A ===
git switch -c feature-user-profile

cat > src/profile.py << 'EOF'
#!/usr/bin/env python3
"""
User Profile Module
"""

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {}
    
    def set_name(self, name):
        self.data['name'] = name
    
    def set_email(self, email):
        self.data['email'] = email
    
    def get_profile(self):
        return self.data
EOF

git add src/profile.py
git commit -m "Add user profile module"

# === Developer B ===
git switch main
git switch -c feature-notification

cat > src/notification.py << 'EOF'
#!/usr/bin/env python3
"""
Notification Module
"""

class NotificationService:
    def __init__(self):
        self.notifications = []
    
    def send_email(self, to, subject, body):
        self.notifications.append({
            'type': 'email',
            'to': to,
            'subject': subject,
            'body': body
        })
        return True
    
    def send_sms(self, to, message):
        self.notifications.append({
            'type': 'sms',
            'to': to,
            'message': message
        })
        return True
EOF

git add src/notification.py
git commit -m "Add notification service"

# === Merge ทั้งสอง features ===
git switch main
git merge feature-user-profile -m "Merge: Add user profile feature"
git merge feature-notification -m "Merge: Add notification feature"

# ดูผลลัพธ์
git log --oneline --graph --all
tree src/
```

### 📝 แบบฝึกหัดที่ 2: แก้ Conflict แบบซับซ้อน

**สถานการณ์:** ทั้งสองคนแก้ไฟล์เดียวกัน

```bash
# === Developer A ===
git switch main
git switch -c feature-logging-v1

cat > src/logger.py << 'EOF'
#!/usr/bin/env python3
"""
Logging Module - Version A
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('app')

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_warning(message):
    logger.warning(message)
EOF

git add src/logger.py
git commit -m "Add logging module v1"

# === Developer B ===
git switch main
git switch -c feature-logging-v2

cat > src/logger.py << 'EOF'
#!/usr/bin/env python3
"""
Logging Module - Version B with file output
"""
import logging
from datetime import datetime

# Create logs directory
import os
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s: %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)

def log_debug(msg):
    logger.debug(msg)
EOF

git add src/logger.py
git commit -m "Add logging module v2 with file output"

# === Merge และแก้ Conflict ===
git switch main
git merge feature-logging-v1 -m "Merge logging v1"
git merge feature-logging-v2  # จะเกิด conflict!

# ตรวจสอบ conflict
git status
cat src/logger.py

# แก้ไข conflict - รวมทั้งสอง version
cat > src/logger.py << 'EOF'
#!/usr/bin/env python3
"""
Logging Module - Combined Version
Supports both console and file logging
"""
import logging
from datetime import datetime
import os

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')

def log_info(message):
    """Log info level message"""
    logger.info(message)

def log_error(message):
    """Log error level message"""
    logger.error(message)

def log_warning(message):
    """Log warning level message"""
    logger.warning(message)

def log_debug(message):
    """Log debug level message"""
    logger.debug(message)

def set_log_level(level):
    """Set logging level"""
    logger.setLevel(level)
EOF

git add src/logger.py
git commit -m "Merge logging v2: Combined console and file logging"

# ตรวจสอบผลลัพธ์
git log --oneline --graph
```

### 📝 แบบฝึกหัดที่ 3: Self-Practice

**ทำด้วยตัวเอง:**

1. สร้าง branch ชื่อ `feature-database`
2. เพิ่มไฟล์ `src/database.py` ที่มี class `DatabaseConnection`
3. กลับไป main และสร้าง branch `feature-cache`
4. เพิ่มไฟล์ `src/cache.py` ที่มี class `CacheManager`
5. Merge ทั้งสอง branches เข้า main
6. ตรวจสอบ history ด้วย `git log --graph`

**Template สำหรับ database.py:**
```bash
cat > src/database.py << 'EOF'
#!/usr/bin/env python3
"""
Database Module
TODO: Implement by student
"""

class DatabaseConnection:
    def __init__(self):
        # TODO: Initialize connection
        pass
    
    def connect(self):
        # TODO: Connect to database
        pass
    
    def disconnect(self):
        # TODO: Disconnect
        pass
    
    def execute(self, query):
        # TODO: Execute query
        pass
EOF
```

---

## 📋 สรุปคำสั่งที่ใช้

### Branch Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch` | ดู branch ทั้งหมด |
| `git branch <name>` | สร้าง branch ใหม่ |
| `git branch -d <name>` | ลบ branch |
| `git branch -D <name>` | บังคับลบ branch |
| `git branch -v` | ดู branch พร้อม commit ล่าสุด |
| `git branch -vv` | ดู branch พร้อม tracking info |
| `git branch -a` | ดูทุก branch (local + remote) |
| `git branch -r` | ดูเฉพาะ remote branches |

### Switch/Checkout Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git switch <branch>` | สลับไป branch |
| `git switch -c <name>` | สร้างและสลับไป branch ใหม่ |
| `git checkout <branch>` | สลับไป branch (วิธีเก่า) |
| `git checkout -b <name>` | สร้างและสลับ (วิธีเก่า) |

### Merge Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git merge <branch>` | Merge branch เข้ามา |
| `git merge --abort` | ยกเลิก merge |
| `git merge --continue` | ดำเนินการ merge ต่อ |

### Remote Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git remote -v` | ดู remote ทั้งหมด |
| `git remote add <name> <url>` | เพิ่ม remote |
| `git push -u origin <branch>` | Push และตั้ง upstream |
| `git fetch origin` | ดึงข้อมูลจาก remote |
| `git pull origin <branch>` | Fetch และ merge |

### Utility Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git status` | ดูสถานะ |
| `git log --oneline --graph --all` | ดูประวัติแบบ graph |
| `git diff` | ดูความแตกต่าง |
| `tree -a -I '.git'` | ดูโครงสร้างไฟล์ |

---

## 🎉 สรุป

เมื่อทำ LAB นี้เสร็จสมบูรณ์ นักศึกษาจะ:

✅ เข้าใจและใช้งาน Git Branch ได้คล่อง  
✅ สลับ branch ด้วย `git switch` และ `git checkout`  
✅ เข้าใจความแตกต่างระหว่าง Fast-Forward และ 3-Way Merge  
✅ แก้ไข Merge Conflict ได้อย่างมั่นใจ  
✅ จัดการ Local และ Remote Branch ได้  
✅ พร้อมทำงานเป็นทีมด้วย Git  

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Git Official Documentation](https://git-scm.com/doc)
- [Pro Git Book (Free)](https://git-scm.com/book/en/v2)
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---
