# 🌿 LAB: Git Branch & Merge - การจัดการ Branch และ Merge ใน Git

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
- ✅ **เข้าใจและใช้งาน Git Merge ได้อย่างถูกต้อง**
- ✅ **แก้ไข Merge Conflict ได้**

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
          main line
```

### ประเภทของ Branch

| ประเภท | คำอธิบาย |
|--------|----------|
| **Local Branch** | Branch ที่อยู่บนเครื่องของเรา |
| **Remote Branch** | Branch ที่อยู่บน Server (เช่น GitHub, GitLab) |
| **Tracking Branch** | Local Branch ที่เชื่อมต่อกับ Remote Branch |

### ทำไมต้องมีหลาย Commits ใน main ก่อนสร้าง Branch?

การมีหลาย commits ใน main ก่อนสร้าง branch ใหม่มีประโยชน์:
- เห็นภาพชัดเจนว่า branch ใหม่แยกออกมาจากจุดไหน
- ฝึกการใช้ `git log` ดูประวัติ commits
- เข้าใจการทำงานของ HEAD pointer
- เตรียมพร้อมสำหรับการ merge ในอนาคต

```
main:    A---B---C  (3 commits before creating branch)
                 \
feature:          D---E  (new commits in branch)
```

---

## 🔧 ความรู้เบื้องต้น: Pipeline ใน Linux

### Pipeline (`|`) คืออะไร?

**Pipeline** คือการส่งผลลัพธ์จากคำสั่งหนึ่งไปเป็น input ของอีกคำสั่งหนึ่ง โดยใช้เครื่องหมาย `|` (pipe)

```
command 1  |  command 2  |  command 3
    ↓              ↓              ↓
  output    →    input     →   output
            →              →    input
                           →   output (final)
```

### ตัวอย่างการใช้ Pipeline

| คำสั่ง | หน้าที่ | ตัวอย่าง |
|--------|--------|----------|
| `grep "text"` | กรองบรรทัดที่มีข้อความ | `cat file \| grep "error"` |
| `wc -l` | นับจำนวนบรรทัด | `ls \| wc -l` |
| `head -n` | เอา n บรรทัดแรก | `cat file \| head -10` |
| `tail -n` | เอา n บรรทัดสุดท้าย | `cat file \| tail -5` |
| `sort` | เรียงลำดับ | `cat file \| sort` |

---

## 🔧 ความรู้เบื้องต้น: Here Document (Heredoc)

### Here Document คืออะไร?

**Here Document** คือวิธีการเขียนข้อความหลายบรรทัดลงไฟล์โดยไม่ต้องกด Ctrl+D

```bash
cat > filename << 'EOF'
content line 1
content line 2
content line 3
EOF
```

**อธิบาย:**
- `cat > filename` = สร้างไฟล์ใหม่
- `<< 'EOF'` = เริ่มต้น Here Document (EOF = End Of File, ใช้คำอื่นก็ได้)
- `EOF` = สิ้นสุด Here Document

---

## 🛠️ เตรียมความพร้อม

### ขั้นตอนที่ 1: ตั้งค่า Git (ถ้ายังไม่เคยตั้ง)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

> 💡 **หมายเหตุ:** การตั้ง `init.defaultBranch main` จะทำให้ทุกครั้งที่สร้าง repository ใหม่ด้วย `git init` จะใช้ชื่อ `main` แทน `master`

### ขั้นตอนที่ 2: สร้างโปรเจกต์สำหรับฝึก

```bash
mkdir git-branch-lab && cd git-branch-lab
git init
```

**ผลลัพธ์ที่คาดหวัง:**
```
Initialized empty Git repository in /path/to/git-branch-lab/.git/
```

---

## 📝 แบบฝึกหัดที่ 0: การใช้ Here Document สร้างไฟล์และ Commit แรก

### 0.1 สร้างไฟล์ README.md และ Commit แรก

```bash
cat > README.md << 'EOF'
# My Git Branch Lab
A project for learning Git Branch

## Objectives
- Learn how to use Git Branch
- Practice switching branches
- Understand Remote Branch

## Author
- Student: [Your Name]
- ID: [Student ID]
EOF

git add README.md
git commit -m "docs: add README.md with project description"
```

**ผลลัพธ์ที่คาดหวัง:**
```
[main (root-commit) 721e631] docs: add README.md with project description
 1 file changed, 11 insertions(+)
 create mode 100644 README.md
```

### 0.2 สร้างไฟล์ main.py และ Commit ที่สอง

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

git add main.py
git commit -m "feat: add main.py entry point"
```

**ผลลัพธ์ที่คาดหวัง:**
```
[main cfe1851] feat: add main.py entry point
 1 file changed, 12 insertions(+)
 create mode 100644 main.py
```

### 0.3 สร้างโครงสร้างโปรเจกต์และ Commit ที่สาม

```bash
mkdir -p src tests

cat > src/__init__.py << 'EOF'
# Package initialization
__version__ = "1.0.0"
EOF

cat > src/utils.py << 'EOF'
"""Utility functions"""

def greet(name):
    """Greet a user"""
    return f"Hello, {name}!"

def add(a, b):
    """Add two numbers"""
    return a + b
EOF

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

git add .
git commit -m "feat: add project structure with src and tests"
```

**ผลลัพธ์ที่คาดหวัง:**
```
[main 29a6460] feat: add project structure with src and tests
 3 files changed, 26 insertions(+)
 create mode 100644 src/__init__.py
 create mode 100644 src/utils.py
 create mode 100644 tests/test_utils.py
```

### 0.4 ตรวจสอบโครงสร้างและ Log

```bash
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

```bash
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
29a6460 feat: add project structure with src and tests
cfe1851 feat: add main.py entry point
721e631 docs: add README.md with project description
```

> 🎉 **main มี 3 commits แล้ว! พร้อมสำหรับสร้าง Branch ใหม่!**

---

## 📝 แบบฝึกหัดที่ 1: การสร้างและดู Branch

### 1.1 ดูรายชื่อ Branch ทั้งหมด

```bash
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
* main
```

> 💡 เครื่องหมาย `*` แสดงว่าเราอยู่ที่ branch ไหน

### 1.2 สร้าง Branch ใหม่

```bash
git branch feature-login
git branch feature-register
git branch bugfix-navbar
git branch hotfix-security

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

### 1.3 ดู Branch พร้อม Commit Info

```bash
git branch -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
  bugfix-navbar    29a6460 feat: add project structure with src and tests
  feature-login    29a6460 feat: add project structure with src and tests
  feature-register 29a6460 feat: add project structure with src and tests
  hotfix-security  29a6460 feat: add project structure with src and tests
* main             29a6460 feat: add project structure with src and tests
```

> 💡 **สังเกต:** ทุก branch ชี้ไปที่ commit เดียวกัน เพราะเพิ่งสร้างจาก main

### 1.4 ใช้ Pipeline นับจำนวน Branch

```bash
git branch | wc -l
```

**ผลลัพธ์ที่คาดหวัง:**
```
5
```

```bash
git branch | grep "feature"
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
  feature-register
```

---

## 📝 แบบฝึกหัดที่ 2: การสลับ Branch ด้วย git switch และ git checkout

### 2.1 การใช้ git switch (วิธีใหม่ - แนะนำ)

```bash
git switch feature-login
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'feature-login'
  bugfix-navbar
* feature-login
  feature-register
  hotfix-security
  main
```

### 2.2 การใช้ git checkout (วิธีเก่า - ยังใช้ได้)

```bash
git checkout main
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
  bugfix-navbar
  feature-login
  feature-register
  hotfix-security
* main
```

### 2.3 สร้าง Branch และสลับไปพร้อมกัน

**วิธีที่ 1: ใช้ git switch -c (แนะนำ)**

```bash
git switch -c feature-dashboard
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to a new branch 'feature-dashboard'
  bugfix-navbar
* feature-dashboard
  feature-login
  feature-register
  hotfix-security
  main
```

**วิธีที่ 2: ใช้ git checkout -b**

```bash
git switch main
git checkout -b feature-profile
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
Switched to a new branch 'feature-profile'
  bugfix-navbar
  feature-dashboard
  feature-login
* feature-profile
  feature-register
  hotfix-security
  main
```

### 2.4 เปรียบเทียบ git switch vs git checkout

| คำสั่ง | การใช้งาน | หมายเหตุ |
|--------|----------|----------|
| `git switch <branch>` | สลับ branch | วิธีใหม่ ปลอดภัยกว่า |
| `git switch -c <branch>` | สร้างและสลับ | เหมือน checkout -b |
| `git checkout <branch>` | สลับ branch | วิธีเก่า ยังใช้ได้ |
| `git checkout -b <branch>` | สร้างและสลับ | วิธีเก่า |

---

## 📝 แบบฝึกหัดที่ 3: ทำงานกับ Branch และสร้างไฟล์

### 3.1 สร้างการเปลี่ยนแปลงใน feature-login

```bash
git switch feature-login
mkdir -p src/auth

cat > src/auth/__init__.py << 'EOF'
# Authentication module
__all__ = ['login', 'logout', 'validate_user']
EOF

cat > src/auth/login.py << 'EOF'
"""
Login Module
User login system
"""

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_logged_in = False
    
    def __repr__(self):
        return f"User({self.username})"

def login(username, password):
    """Login function"""
    print(f"Attempting to login: {username}")
    if username and password:
        print("Login successful!")
        return True
    return False

def logout(user):
    """Logout function"""
    print(f"Logging out: {user.username}")
    user.is_logged_in = False
    return True

def validate_user(username):
    """Validate username"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not username.isalnum():
        return False, "Username must contain only letters and numbers"
    return True, "Valid username"
EOF

cat > tests/test_login.py << 'EOF'
"""Unit Tests for Login Module"""
import sys
sys.path.insert(0, '..')
from src.auth.login import login, logout, validate_user, User

def test_login_success():
    result = login("testuser", "password123")
    assert result == True
    print("test_login_success passed")

def test_login_empty_username():
    result = login("", "password123")
    assert result == False
    print("test_login_empty_username passed")

def test_validate_user_short():
    valid, msg = validate_user("ab")
    assert valid == False
    print("test_validate_user_short passed")

def test_validate_user_valid():
    valid, msg = validate_user("testuser")
    assert valid == True
    print("test_validate_user_valid passed")

if __name__ == "__main__":
    test_login_success()
    test_login_empty_username()
    test_validate_user_short()
    test_validate_user_valid()
    print("\nAll login tests passed!")
EOF
```

### 3.2 ตรวจสอบโครงสร้างและ Commit

```bash
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
git add .
git commit -m "feat: add login system with tests"
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
[feature-login 5d5a623] feat: add login system with tests
 3 files changed, 77 insertions(+)
 create mode 100644 src/auth/__init__.py
 create mode 100644 src/auth/login.py
 create mode 100644 tests/test_login.py

5d5a623 feat: add login system with tests
29a6460 feat: add project structure with src and tests
cfe1851 feat: add main.py entry point
721e631 docs: add README.md with project description
```

> 💡 **สังเกต:** feature-login มี 4 commits (3 จาก main + 1 ใหม่)

### 3.3 เปรียบเทียบโครงสร้างระหว่าง Branch

```bash
git switch main
tree
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
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

## 📝 แบบฝึกหัดที่ 4: สร้าง Feature อีก Branch

### 4.1 สร้าง Feature Register

```bash
git switch feature-register
mkdir -p src/auth

cat > src/auth/register.py << 'EOF'
"""
Register Module
New user registration system
"""

import re
from datetime import datetime

class RegistrationError(Exception):
    """Exception for registration errors"""
    pass

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True, "Email valid"
    return False, "Invalid email format"

def validate_password(password):
    """Validate password strength"""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain uppercase letter")
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain a number")
    
    if errors:
        return False, errors
    return True, ["Password valid"]

def register(username, email, password):
    """Register new user"""
    email_valid, email_msg = validate_email(email)
    if not email_valid:
        raise RegistrationError(email_msg)
    
    pass_valid, pass_msgs = validate_password(password)
    if not pass_valid:
        raise RegistrationError(", ".join(pass_msgs))
    
    user = {
        'username': username,
        'email': email,
        'created_at': datetime.now().isoformat(),
        'is_active': True
    }
    
    print(f"Registration successful: {username}")
    return user
EOF

cat > tests/test_register.py << 'EOF'
"""Unit Tests for Register Module"""
import sys
sys.path.insert(0, '..')
from src.auth.register import validate_email, validate_password, register, RegistrationError

def test_validate_email_valid():
    valid, msg = validate_email("test@example.com")
    assert valid == True
    print("test_validate_email_valid passed")

def test_validate_email_invalid():
    valid, msg = validate_email("invalid-email")
    assert valid == False
    print("test_validate_email_invalid passed")

def test_validate_password_weak():
    valid, msgs = validate_password("short")
    assert valid == False
    print("test_validate_password_weak passed")

def test_validate_password_strong():
    valid, msgs = validate_password("StrongPass123")
    assert valid == True
    print("test_validate_password_strong passed")

if __name__ == "__main__":
    test_validate_email_valid()
    test_validate_email_invalid()
    test_validate_password_weak()
    test_validate_password_strong()
    print("\nAll register tests passed!")
EOF

git add .
git commit -m "feat: add register system with validation"
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
[feature-register 72e31c0] feat: add register system with validation
 2 files changed, 83 insertions(+)
 create mode 100644 src/auth/register.py
 create mode 100644 tests/test_register.py

72e31c0 feat: add register system with validation
29a6460 feat: add project structure with src and tests
cfe1851 feat: add main.py entry point
721e631 docs: add README.md with project description
```

---

## 📝 แบบฝึกหัดที่ 5: Detached HEAD State

### 5.1 ทำความเข้าใจ HEAD

**HEAD** คือตัวชี้ที่บอกว่าเราอยู่ที่ไหนใน Git history

```bash
git switch main
git log --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
29a6460 feat: add project structure with src and tests
cfe1851 feat: add main.py entry point
721e631 docs: add README.md with project description
```

### 5.2 เข้าสู่สถานะ Detached HEAD

```bash
# checkout ไปที่ commit แรก (ใช้ hash จริงจาก log ของคุณ)
git checkout 721e631
```

**ผลลัพธ์ที่คาดหวัง:**
```
Note: switching to '721e631'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

HEAD is now at 721e631 docs: add README.md with project description
```

### 5.3 ดูสถานะใน Detached HEAD

```bash
git status
ls -la
```

**ผลลัพธ์ที่คาดหวัง:**
```
HEAD detached at 721e631
nothing to commit, working tree clean

total 13
drwxr-xr-x 3 root root 4096 ...
-rw-r--r-- 1 root root  209 ... README.md
```

> 💡 **สังเกต:** ที่ commit แรก มีแค่ไฟล์ README.md เท่านั้น!

### 5.4 ออกจาก Detached HEAD

```bash
git switch main
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
On branch main
nothing to commit, working tree clean
```

> ⚠️ **คำเตือน:** ถ้าคุณ commit ใน Detached HEAD แล้วสลับออกไป commits เหล่านั้นอาจหายได้!

---

## 📝 แบบฝึกหัดที่ 6: การเปลี่ยนชื่อ Branch

### 6.1 เปลี่ยนชื่อ Branch ปัจจุบัน

```bash
git switch bugfix-navbar
git branch -m fix-navbar
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'bugfix-navbar'
  feature-dashboard
  feature-login
  feature-profile
  feature-register
* fix-navbar
  hotfix-security
  main
```

### 6.2 เปลี่ยนชื่อ Branch อื่น (ไม่ต้องไปอยู่ที่ branch นั้น)

```bash
git switch main
git branch -m hotfix-security security-patch
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
  feature-dashboard
  feature-login
  feature-profile
  feature-register
  fix-navbar
* main
  security-patch
```

---

## 📝 แบบฝึกหัดที่ 7: การลบ Branch

### 7.1 ลบ Branch ที่ไม่มี Commit ใหม่

```bash
git branch -d fix-navbar
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Deleted branch fix-navbar (was 29a6460).
  feature-dashboard
  feature-login
  feature-profile
  feature-register
* main
  security-patch
```

### 7.2 ลบ Branch ที่มี Commit ยังไม่ได้ Merge (บังคับลบ)

```bash
git switch feature-dashboard
cat > src/dashboard.py << 'EOF'
"""Dashboard Module"""

def show_dashboard():
    print("================================")
    print("          DASHBOARD             ")
    print("================================")

def get_stats():
    return {'users': 100, 'active': 50}
EOF

git add .
git commit -m "feat: add dashboard module"
```

**ผลลัพธ์ที่คาดหวัง:**
```
[feature-dashboard ab22cce] feat: add dashboard module
 1 file changed, 9 insertions(+)
 create mode 100644 src/dashboard.py
```

```bash
git switch main
git branch -d feature-dashboard
```

**ผลลัพธ์ที่คาดหวัง (Error):**
```
error: the branch 'feature-dashboard' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature-dashboard'
```

```bash
git branch -D feature-dashboard
git branch
```

**ผลลัพธ์ที่คาดหวัง:**
```
Deleted branch feature-dashboard (was ab22cce).
  feature-login
  feature-profile
  feature-register
* main
  security-patch
```

> ⚠️ **คำเตือน:** ใช้ `-D` ด้วยความระมัดระวัง เพราะจะลบ commits ที่ยังไม่ได้ merge ไปด้วย

---

## 📝 แบบฝึกหัดที่ 8: Remote Branch

### 8.1 เตรียม Remote Repository

```bash
git remote add origin https://github.com/YOUR_USERNAME/git-branch-lab.git
git remote -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
origin  https://github.com/YOUR_USERNAME/git-branch-lab.git (fetch)
origin  https://github.com/YOUR_USERNAME/git-branch-lab.git (push)
```

### 8.2 Push Branch ไป Remote

```bash
git push -u origin main
git push -u origin feature-login
git branch -a
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login
  feature-profile
  feature-register
* main
  security-patch
  remotes/origin/feature-login
  remotes/origin/main
```

### 8.3 ลบ Remote Branch

```bash
git push origin --delete feature-login
git fetch --prune
git branch -a
```

**ผลลัพธ์ที่คาดหวัง:**
```
To https://github.com/YOUR_USERNAME/git-branch-lab.git
 - [deleted]         feature-login
  feature-login
  feature-profile
  feature-register
* main
  security-patch
  remotes/origin/main
```

---

## 📝 แบบฝึกหัดที่ 9: Git Merge และคำสั่งที่มีประโยชน์

### 🔀 ความรู้พื้นฐาน: Git Merge คืออะไร?

**Git Merge** คือการรวม commits จาก branch หนึ่งเข้ากับอีก branch หนึ่ง เป็นวิธีที่ใช้บ่อยที่สุดในการนำ feature ที่พัฒนาเสร็จแล้วกลับเข้า main branch

```
Before merge:
main:     A---B---C
               \
feature:        D---E

After merge:
main:     A---B---C-------F (merge commit)
               \         /
feature:        D---E---+
```

### ประเภทของ Merge

| ประเภท | คำอธิบาย | เมื่อไหร่เกิด |
|--------|----------|--------------|
| **Fast-forward** | เลื่อน pointer ไปข้างหน้า ไม่สร้าง merge commit | เมื่อ main ไม่มี commit ใหม่หลังแยก branch |
| **3-way merge** | สร้าง merge commit ใหม่ | เมื่อทั้งสอง branch มี commit ใหม่ |
| **Merge conflict** | ต้องแก้ไข conflict ด้วยมือ | เมื่อแก้ไขไฟล์เดียวกันในตำแหน่งเดียวกัน |

---

### 9.1 เตรียมสถานะ Branch สำหรับ Merge

```bash
git switch main
git branch -v
```

**ผลลัพธ์ที่คาดหวัง:**
```
  feature-login    5d5a623 feat: add login system with tests
  feature-profile  29a6460 feat: add project structure with src and tests
  feature-register 72e31c0 feat: add register system with validation
* main             29a6460 feat: add project structure with src and tests
  security-patch   29a6460 feat: add project structure with src and tests
```

```bash
git log --oneline --graph --all
```

**ผลลัพธ์ที่คาดหวัง:**
```
* 72e31c0 feat: add register system with validation
| * 5d5a623 feat: add login system with tests
|/  
* 29a6460 feat: add project structure with src and tests
* cfe1851 feat: add main.py entry point
* 721e631 docs: add README.md with project description
```

---

### 9.2 Fast-Forward Merge

**Fast-forward merge** เกิดขึ้นเมื่อ branch ปลายทางไม่มี commits ใหม่หลังจากที่แยก branch ออกไป

```bash
git switch -c feature-quick-fix

cat > src/quick_fix.py << 'EOF'
"""Quick Fix Module"""

def fix_typo(text):
    fixes = {'teh': 'the', 'adn': 'and', 'waht': 'what'}
    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)
    return text

def sanitize_input(text):
    return text.strip().replace('<', '').replace('>', '')
EOF

git add .
git commit -m "fix: add quick fix utilities"
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to a new branch 'feature-quick-fix'
[feature-quick-fix f7eb4f2] fix: add quick fix utilities
 1 file changed, 10 insertions(+)
 create mode 100644 src/quick_fix.py
```

```bash
git switch main
git merge feature-quick-fix
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
Updating 29a6460..f7eb4f2
Fast-forward
 src/quick_fix.py | 10 ++++++++++
 1 file changed, 10 insertions(+)
 create mode 100644 src/quick_fix.py
```

> 💡 **สังเกต:** Git บอกว่าเป็น "Fast-forward" เพราะ main ไม่มี commit ใหม่หลังจากสร้าง feature-quick-fix

```bash
git log --oneline -4
```

**ผลลัพธ์ที่คาดหวัง:**
```
f7eb4f2 fix: add quick fix utilities
29a6460 feat: add project structure with src and tests
cfe1851 feat: add main.py entry point
721e631 docs: add README.md with project description
```

```bash
# ลบ branch ที่ merge แล้ว
git branch -d feature-quick-fix
```

---

### 9.3 3-Way Merge (Merge Commit)

**3-way merge** เกิดขึ้นเมื่อทั้งสอง branch มี commits ใหม่ Git จะสร้าง "merge commit" ใหม่

```bash
# ดู commits ที่จะ merge เข้ามา
git log main..feature-login --oneline
```

**ผลลัพธ์ที่คาดหวัง:**
```
5d5a623 feat: add login system with tests
```

```bash
git merge feature-login -m "Merge branch 'feature-login' into main"
```

**ผลลัพธ์ที่คาดหวัง:**
```
Merge made by the 'ort' strategy.
 src/auth/__init__.py |  2 ++
 src/auth/login.py    | 44 ++++++++++++++++++++++++++++++++++++++++++++
 tests/test_login.py  | 31 +++++++++++++++++++++++++++++++
 3 files changed, 77 insertions(+)
 create mode 100644 src/auth/__init__.py
 create mode 100644 src/auth/login.py
 create mode 100644 tests/test_login.py
```

```bash
git log --oneline --graph -8
```

**ผลลัพธ์ที่คาดหวัง:**
```
*   f8fb191 Merge branch 'feature-login' into main
|\  
| * 5d5a623 feat: add login system with tests
* | f7eb4f2 fix: add quick fix utilities
|/  
* 29a6460 feat: add project structure with src and tests
* cfe1851 feat: add main.py entry point
* 721e631 docs: add README.md with project description
```

> 💡 **สังเกต:** Git สร้าง merge commit ใหม่ (f8fb191) ที่รวม commits จากทั้งสอง branch

---

### 9.4 Merge พร้อมดู Diff ก่อน

```bash
# ดูไฟล์ที่จะเปลี่ยนแปลง
git diff --name-only main..feature-register
```

**ผลลัพธ์ที่คาดหวัง:**
```
src/auth/register.py
tests/test_register.py
```

```bash
# ดูสถิติการเปลี่ยนแปลง
git diff --stat main..feature-register
```

**ผลลัพธ์ที่คาดหวัง:**
```
 src/auth/register.py   | 52 ++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_register.py | 31 ++++++++++++++++++++++++++++
 2 files changed, 83 insertions(+)
```

```bash
git merge feature-register -m "Merge branch 'feature-register' - add registration system"
```

**ผลลัพธ์ที่คาดหวัง:**
```
Merge made by the 'ort' strategy.
 src/auth/register.py   | 52 ++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_register.py | 31 ++++++++++++++++++++++++++++
 2 files changed, 83 insertions(+)
 create mode 100644 src/auth/register.py
 create mode 100644 tests/test_register.py
```

```bash
tree src/auth
```

**ผลลัพธ์ที่คาดหวัง:**
```
src/auth
├── __init__.py
├── login.py
└── register.py

0 directories, 3 files
```

---

### 9.5 การแก้ไข Merge Conflict

**Merge conflict** เกิดขึ้นเมื่อทั้งสอง branch แก้ไขไฟล์เดียวกันในตำแหน่งเดียวกัน

**สร้างสถานการณ์ conflict:**

```bash
git switch -c feature-update-readme

cat > README.md << 'EOF'
# My Git Branch Lab
A comprehensive project for learning Git Branch and Merge

## Objectives
- Learn how to use Git Branch
- Practice switching branches
- Understand Remote Branch
- Master Git Merge techniques

## Features
- Login System
- Registration System
- Quick Fix Utilities

## Author
- Student: [Your Name]
- Updated by: Feature Team
EOF

git add README.md
git commit -m "docs: update README with feature list"
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to a new branch 'feature-update-readme'
[feature-update-readme 4d46521] docs: update README with feature list
 1 file changed, 8 insertions(+), 2 deletions(-)
```

```bash
git switch main

cat > README.md << 'EOF'
# My Git Branch Lab
A project for learning Git Branch - Version 2.0

## Objectives
- Learn how to use Git Branch
- Practice switching branches
- Understand Remote Branch
- Learn Git Merge and Conflict Resolution

## Status
- Project: Active
- Version: 2.0

## Author
- Student: [Your Name]
- Maintained by: Main Team
EOF

git add README.md
git commit -m "docs: update README with version info"
```

**ผลลัพธ์ที่คาดหวัง:**
```
Switched to branch 'main'
[main 6e61edd] docs: update README with version info
 1 file changed, 7 insertions(+), 2 deletions(-)
```

```bash
git merge feature-update-readme
```

**ผลลัพธ์ที่คาดหวัง (Conflict!):**
```
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
git status
```

**ผลลัพธ์ที่คาดหวัง:**
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

```bash
cat README.md
```

**ผลลัพธ์ที่คาดหวัง (Conflict Markers):**
```
# My Git Branch Lab
<<<<<<< HEAD
A project for learning Git Branch - Version 2.0
=======
A comprehensive project for learning Git Branch and Merge
>>>>>>> feature-update-readme

## Objectives
- Learn how to use Git Branch
- Practice switching branches
- Understand Remote Branch
<<<<<<< HEAD
- Learn Git Merge and Conflict Resolution

## Status
- Project: Active
- Version: 2.0

## Author
- Student: [Your Name]
- Maintained by: Main Team
=======
- Master Git Merge techniques

## Features
- Login System
- Registration System
- Quick Fix Utilities

## Author
- Student: [Your Name]
- Updated by: Feature Team
>>>>>>> feature-update-readme
```

> 💡 **อธิบาย Conflict Markers:**
> - `<<<<<<< HEAD` = เริ่มต้นส่วนของ branch ปัจจุบัน (main)
> - `=======` = แบ่งระหว่างสอง versions
> - `>>>>>>> feature-update-readme` = สิ้นสุดส่วนของ branch ที่ merge เข้ามา

---

### 9.6 แก้ไข Conflict

**แก้ไขไฟล์โดยรวมเนื้อหาจากทั้งสองส่วน:**

```bash
cat > README.md << 'EOF'
# My Git Branch Lab
A comprehensive project for learning Git Branch and Merge - Version 2.0

## Objectives
- Learn how to use Git Branch
- Practice switching branches
- Understand Remote Branch
- Master Git Merge techniques
- Learn Git Merge and Conflict Resolution

## Features
- Login System
- Registration System
- Quick Fix Utilities

## Status
- Project: Active
- Version: 2.0

## Author
- Student: [Your Name]
- Maintained by: Main Team & Feature Team
EOF

git add README.md
git commit -m "Merge branch 'feature-update-readme' - resolve conflicts"
```

**ผลลัพธ์ที่คาดหวัง:**
```
[main 1ddc2a4] Merge branch 'feature-update-readme' - resolve conflicts
```

```bash
git log --oneline --graph -6
```

**ผลลัพธ์ที่คาดหวัง:**
```
*   1ddc2a4 Merge branch 'feature-update-readme' - resolve conflicts
|\  
| * 4d46521 docs: update README with feature list
* | 6e61edd docs: update README with version info
|/  
*   ce7f4e9 Merge branch 'feature-register' - add registration system
...
```


---

## 📋 สรุปคำสั่ง Git Merge

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git merge <branch>` | Merge branch เข้า branch ปัจจุบัน |
| `git merge <branch> -m "msg"` | Merge พร้อมกำหนด commit message |
| `git merge --no-ff <branch>` | บังคับสร้าง merge commit |
| `git merge --squash <branch>` | รวม commits ทั้งหมดเป็น 1 |
| `git merge --abort` | ยกเลิก merge ระหว่างมี conflict |
| `git diff main..<branch>` | ดูความแตกต่างก่อน merge |
| `git log main..<branch>` | ดู commits ที่จะ merge เข้ามา |
| `git branch --merged` | ดู branch ที่ merge แล้ว |
| `git branch --no-merged` | ดู branch ที่ยังไม่ merge |

---

## 📋 สรุปคำสั่งสำคัญทั้งหมด

### คำสั่ง Linux พื้นฐาน

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `cat > file << 'EOF'` | สร้างไฟล์หลายบรรทัด (heredoc) |
| `cat file` | อ่านเนื้อหาไฟล์ |
| `tree` | ดูโครงสร้างไฟล์และโฟลเดอร์ |
| `cmd1 \| cmd2` | Pipeline: ส่ง output ไปเป็น input |
| `grep "text"` | กรองบรรทัดที่มีข้อความ |
| `wc -l` | นับจำนวนบรรทัด |

### การจัดการ Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch` | ดูรายการ local branch |
| `git branch -a` | ดูรายการ local และ remote branch |
| `git branch -v` | ดู branch พร้อม commit ล่าสุด |
| `git branch <name>` | สร้าง branch ใหม่ |
| `git branch -d <name>` | ลบ branch (ที่ merge แล้ว) |
| `git branch -D <name>` | บังคับลบ branch |
| `git branch -m <new>` | เปลี่ยนชื่อ branch ปัจจุบัน |
| `git branch --merged` | ดู branch ที่ merge แล้ว |
| `git branch --no-merged` | ดู branch ที่ยังไม่ merge |

### การสลับ Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git switch <branch>` | สลับไป branch (แนะนำ) |
| `git switch -c <branch>` | สร้างและสลับไป branch ใหม่ |
| `git checkout <branch>` | สลับไป branch (วิธีเก่า) |
| `git checkout -b <branch>` | สร้างและสลับไป branch ใหม่ |

### Git Merge

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git merge <branch>` | Merge branch เข้า branch ปัจจุบัน |
| `git merge --no-ff <branch>` | Merge แบบสร้าง merge commit เสมอ |
| `git merge --squash <branch>` | Merge แบบรวม commits เป็น 1 |
| `git merge --abort` | ยกเลิก merge ที่มี conflict |

### Remote Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git push -u origin <branch>` | Push branch ไป remote |
| `git push origin --delete <branch>` | ลบ remote branch |
| `git fetch --prune` | ลบ remote tracking ที่ไม่มีอยู่แล้ว |

---

## 📚 แหล่งเรียนรู้เพิ่มเติม

- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (Interactive)](https://learngitbranching.js.org/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Git Merge Documentation](https://git-scm.com/docs/git-merge)

---

## ✅ Checklist ก่อนจบ LAB

### พื้นฐาน Branch
- [ ] ตั้งค่า `git config --global init.defaultBranch main` แล้ว
- [ ] main มี 3 commits ก่อนสร้าง branch ใหม่
- [ ] เข้าใจการใช้ Pipeline (`|`) และสามารถใช้งานได้
- [ ] ใช้ Here Document (`cat > file << 'EOF'`) สร้างไฟล์ได้
- [ ] ใช้ `tree` ตรวจสอบโครงสร้างโปรเจกต์ได้
- [ ] สร้าง branch ใหม่ได้
- [ ] สลับ branch ด้วย `git switch` และ `git checkout` ได้
- [ ] เข้าใจ Detached HEAD และรู้วิธีออก
- [ ] เปลี่ยนชื่อ branch ได้
- [ ] ลบ branch ได้ทั้ง local และ remote
- [ ] Push และ track remote branch ได้
- [ ] ใช้ `git log --graph` ดูโครงสร้าง branch ได้

### Git Merge
- [ ] **เข้าใจความแตกต่างระหว่าง Fast-Forward และ 3-Way Merge**
- [ ] **ใช้ `git merge` รวม branch ได้**
- [ ] **แก้ไข Merge Conflict ได้**
- [ ] **ใช้ `git merge --no-ff` ได้**
- [ ] **ใช้ `git merge --squash` ได้**
- [ ] **ใช้ `git merge --abort` ยกเลิก merge ได้**
- [ ] **ใช้ `git diff main..<branch>` ดูการเปลี่ยนแปลงก่อน merge**
- [ ] **ใช้ `git branch --merged` ตรวจสอบ branch ที่ merge แล้ว**
- [ ] **ลบ branch ที่ merge แล้วได้อย่างปลอดภัย**

---

## 🎉 ยินดีด้วย!

คุณได้เรียนรู้การจัดการ Git Branch และ Merge เรียบร้อยแล้ว!

---