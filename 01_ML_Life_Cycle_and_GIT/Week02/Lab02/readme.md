# 🎓 Git Lab 02: พื้นฐานการใช้งาน Git และ Remote Repository

## 📋 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Git Workflow Pipeline                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   LOCAL REPOSITORY                              REMOTE REPOSITORY               │
│   ════════════════                              ═════════════════               │
│                                                                                  │
│   ┌──────────────┐                              ┌──────────────┐                │
│   │ Working      │  git add                     │   GitHub/    │                │
│   │ Directory    │ ──────────┐                  │   GitLab     │                │
│   └──────────────┘           │                  └──────────────┘                │
│          │                   ▼                         ▲                        │
│          │           ┌──────────────┐                  │                        │
│          │           │   Staging    │                  │                        │
│          │           │    Area      │                  │                        │
│          │           └──────────────┘                  │                        │
│          │                   │                         │                        │
│          │                   │ git commit              │ git push               │
│          │                   ▼                         │                        │
│          │           ┌──────────────┐                  │                        │
│          │           │    Local     │──────────────────┘                        │
│          │           │  Repository  │                                           │
│          │           └──────────────┘                                           │
│          │                   ▲                         │                        │
│          │                   │                         │ git fetch              │
│          │                   │ git merge               ▼                        │
│          │                   │                  ┌──────────────┐                │
│          │                   └──────────────────│ origin/main  │                │
│          │                                      │ (tracking)   │                │
│          │                                      └──────────────┘                │
│          │                                             │                        │
│          │              git pull = git fetch + git merge                        │
│          │                                                                      │
│          └──────────────── git checkout origin/main ───────────────────────────│
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 โครงสร้างโปรเจคที่จะสร้าง

```
ml-git-lab02_basic/
├── src/
│   ├── main.py
│   └── utils.py
├── config/
│   └── settings.txt
└── data/
    └── sample.txt
```

---

## ⚙️ Git Configuration (ทำครั้งเดียวก่อนเริ่ม Lab)

```bash
# ตั้งค่าชื่อผู้ใช้ (ใช้ชื่อจริงของนักศึกษา)
git config --global user.name "Your Name"

# ตั้งค่าอีเมล (ใช้อีเมลที่ลงทะเบียนกับ GitHub)
git config --global user.email "your.email@example.com"

# ตั้งค่า default branch เป็น main
git config --global init.defaultBranch main

# ตรวจสอบการตั้งค่า
git config --list
```

**ตัวอย่างผลลัพธ์:**
```
user.name=Somchai Student
user.email=somchai@email.com
init.defaultbranch=main
```

---

## 🚀 Part 1: เริ่มต้นสร้างโปรเจค

### Step 1: สร้างโฟลเดอร์โปรเจค

```bash
mkdir ml-git-lab02_basic
cd ml-git-lab02_basic
```

**ตรวจสอบ:**
```bash
pwd
```

**ตัวอย่างผลลัพธ์:**
```
/home/student/ml-git-lab02_basic
```

---

### Step 2: เริ่มต้น Git Repository

```bash
git init
```

**ตัวอย่างผลลัพธ์:**
```
Initialized empty Git repository in /home/student/ml-git-lab02_basic/.git/
```

**ตรวจสอบสถานะ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

---

### Step 3: สร้างโครงสร้างโฟลเดอร์

```bash
mkdir -p src config data
```

**ตรวจสอบ:**
```bash
ls -la
```

**ตัวอย่างผลลัพธ์:**
```
total 20
drwxr-xr-x 6 student student 4096 Dec 16 10:00 .
drwxr-xr-x 3 student student 4096 Dec 16 10:00 ..
drwxr-xr-x 2 student student 4096 Dec 16 10:00 config
drwxr-xr-x 2 student student 4096 Dec 16 10:00 data
drwxr-xr-x 7 student student 4096 Dec 16 10:00 .git
drwxr-xr-x 2 student student 4096 Dec 16 10:00 src
```

---

### Step 4: สร้างไฟล์ main.py

```bash
cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main Application Module
Version: 1.0
"""

def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("Hello from Git Lab 02!")
    print("Learning Git basics...")

if __name__ == "__main__":
    main()
EOF
```

**ตรวจสอบไฟล์ที่สร้าง:**
```bash
cat src/main.py
```

**ตัวอย่างผลลัพธ์:**
```python
#!/usr/bin/env python3
"""
Main Application Module
Version: 1.0
"""

def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("Hello from Git Lab 02!")
    print("Learning Git basics...")

if __name__ == "__main__":
    main()
```

---

### Step 5: ตรวจสอบสถานะ Git (ก่อน add)

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/

nothing added to commit but untracked files present (use "git add" to track)
```

> 📝 **อธิบาย:** Git เห็นว่ามีโฟลเดอร์ `src/` ใหม่ แต่ยังไม่ได้ track (Untracked files)

---

## 🔧 Part 2: การใช้ git add และ git commit

### Step 6: เพิ่มไฟล์เข้า Staging Area ด้วย `git add`

```bash
git add src/main.py
```

**ตรวจสอบสถานะหลัง add:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   src/main.py
```

> 📝 **อธิบาย:** ไฟล์ถูกย้ายไปยัง Staging Area พร้อมสำหรับ commit แล้ว (สีเขียว)

---

### Step 7: Commit ครั้งแรก

```bash
git commit -m "Initial commit: เพิ่ม main.py"
```

**ตัวอย่างผลลัพธ์:**
```
[main (root-commit) a1b2c3d] Initial commit: เพิ่ม main.py
 1 file changed, 12 insertions(+)
 create mode 100644 src/main.py
```

**ตรวจสอบ log:**
```bash
git log --oneline
```

**ตัวอย่างผลลัพธ์:**
```
a1b2c3d (HEAD -> main) Initial commit: เพิ่ม main.py
```

---

### Step 8: สร้างไฟล์เพิ่มเติม - utils.py

```bash
cat > src/utils.py << 'EOF'
"""
Utility Functions Module
"""

def greet(name):
    """ทักทายผู้ใช้"""
    return f"สวัสดี, {name}!"

def calculate_sum(numbers):
    """คำนวณผลรวมของตัวเลข"""
    return sum(numbers)

def calculate_average(numbers):
    """คำนวณค่าเฉลี่ย"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
EOF
```

**ตรวจสอบ:**
```bash
cat src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```python
"""
Utility Functions Module
"""

def greet(name):
    """ทักทายผู้ใช้"""
    return f"สวัสดี, {name}!"

def calculate_sum(numbers):
    """คำนวณผลรวมของตัวเลข"""
    return sum(numbers)

def calculate_average(numbers):
    """คำนวณค่าเฉลี่ย"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
```

---

### Step 9: สร้างไฟล์ settings.txt

```bash
cat > config/settings.txt << 'EOF'
# Application Settings
app_name=GitLab02
version=1.0
debug=true
language=th
EOF
```

**ตรวจสอบ:**
```bash
cat config/settings.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Application Settings
app_name=GitLab02
version=1.0
debug=true
language=th
```

---

### Step 10: สร้างไฟล์ sample.txt

```bash
cat > data/sample.txt << 'EOF'
# Sample Data File
item1,100,active
item2,200,inactive
item3,150,active
EOF
```

**ตรวจสอบ:**
```bash
cat data/sample.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Sample Data File
item1,100,active
item2,200,inactive
item3,150,active
```

---

### Step 11: ตรวจสอบไฟล์ใหม่ทั้งหมด

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config/
        data/
        src/utils.py

nothing added to commit but untracked files present (use "git add" to track)
```

---

### Step 12: เพิ่มไฟล์ทีละไฟล์และดูความเปลี่ยนแปลง

```bash
git add src/utils.py
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   src/utils.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config/
        data/
```

---

### Step 13: เพิ่มไฟล์ที่เหลือทั้งหมดพร้อมกัน

```bash
git add .
```

**ตรวจสอบ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   config/settings.txt
        new file:   data/sample.txt
        new file:   src/utils.py
```

> 📝 **อธิบาย:** `git add .` เพิ่มไฟล์ใหม่ทั้งหมดในโฟลเดอร์ปัจจุบัน

---

### Step 14: Commit ครั้งที่สอง

```bash
git commit -m "Add utility files, config และ sample data"
```

**ตัวอย่างผลลัพธ์:**
```
[main b2c3d4e] Add utility files, config และ sample data
 3 files changed, 22 insertions(+)
 create mode 100644 config/settings.txt
 create mode 100644 data/sample.txt
 create mode 100644 src/utils.py
```

**ดู commit history:**
```bash
git log --oneline
```

**ตัวอย่างผลลัพธ์:**
```
b2c3d4e (HEAD -> main) Add utility files, config และ sample data
a1b2c3d Initial commit: เพิ่ม main.py
```

**ดู commit history แบบละเอียด:**
```bash
git log --oneline --graph --all
```

**ตัวอย่างผลลัพธ์:**
```
* b2c3d4e (HEAD -> main) Add utility files, config และ sample data
* a1b2c3d Initial commit: เพิ่ม main.py
```

---

## 🌐 Part 3: การทำงานกับ Remote Repository

### Step 15: ตรวจสอบ Remote (ก่อนเพิ่ม)

```bash
git remote -v
```

**ตัวอย่างผลลัพธ์:**
```
(ไม่มีผลลัพธ์ - เพราะยังไม่ได้เพิ่ม remote)
```

---

### Step 16: ตรวจสอบ Remote Branches (ก่อนเพิ่ม remote)

```bash
git branch -r
```

**ตัวอย่างผลลัพธ์:**
```
(ไม่มีผลลัพธ์ - เพราะยังไม่ได้เพิ่ม remote)
```

**ตรวจสอบ branch ทั้งหมด (local และ remote):**
```bash
git branch -a
```

**ตัวอย่างผลลัพธ์:**
```
* main
```

---

### Step 17: เพิ่ม Remote Repository ด้วย `git remote add`

> ⚠️ **หมายเหตุ:** ให้นักศึกษาสร้าง repository บน GitHub ก่อน แล้วใช้ URL ของตัวเอง

**วิธีสร้าง Repository บน GitHub:**
1. ไปที่ https://github.com
2. คลิก "New repository"
3. ตั้งชื่อ `ml-git-lab02_basic`
4. **ไม่ต้อง** เลือก "Add a README file"
5. คลิก "Create repository"

```bash
# รูปแบบคำสั่ง: git remote add <ชื่อ> <URL>
git remote add origin https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git
```

**ตรวจสอบ remote ที่เพิ่ม:**
```bash
git remote -v
```

**ตัวอย่างผลลัพธ์:**
```
origin  https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git (fetch)
origin  https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git (push)
```

> 📝 **อธิบาย:** 
> - `origin` คือชื่อที่ใช้เรียก remote repository (convention ทั่วไป)
> - `fetch` คือ URL สำหรับดึงข้อมูลลงมา
> - `push` คือ URL สำหรับส่งข้อมูลขึ้นไป

---

### Step 18: ดูรายละเอียด Remote เพิ่มเติม

```bash
git remote show origin
```

**ตัวอย่างผลลัพธ์ (ก่อน push):**
```
* remote origin
  Fetch URL: https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git
  Push  URL: https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git
  HEAD branch: (unknown)
```

---

### Step 19: Push ไปยัง Remote ด้วย `git push -u`

```bash
git push -u origin main
```

**ตัวอย่างผลลัพธ์:**
```
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (11/11), 1.15 KiB | 1.15 MiB/s, done.
Total 11 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/ml-git-lab02_basic.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

> 📝 **อธิบาย:**
> - `-u` หรือ `--set-upstream` ตั้งค่าให้ local branch track remote branch
> - หลังจากนี้สามารถใช้ `git push` โดยไม่ต้องระบุ origin main อีก

---

### Step 20: ตรวจสอบ Remote Branches (หลัง push)

```bash
git branch -r
```

**ตัวอย่างผลลัพธ์:**
```
origin/main
```

**ตรวจสอบ branch ทั้งหมด:**
```bash
git branch -a
```

**ตัวอย่างผลลัพธ์:**
```
* main
  remotes/origin/main
```

**ดูรายละเอียด branch พร้อม tracking:**
```bash
git branch -vv
```

**ตัวอย่างผลลัพธ์:**
```
* main b2c3d4e [origin/main] Add utility files, config และ sample data
```

---

## 🔄 Part 4: การดึงข้อมูลจาก Remote (fetch, merge, pull)

### Step 21: จำลองการเปลี่ยนแปลงบน Remote

> 📝 **สถานการณ์:** สมมติว่ามีคนอื่นแก้ไขไฟล์บน GitHub หรือเราแก้ไขผ่าน Web Interface

**ไปที่ GitHub:**
1. เปิด repository บน GitHub
2. คลิกที่ไฟล์ `config/settings.txt`
3. คลิกปุ่ม ✏️ (Edit this file)
4. เพิ่มบรรทัดใหม่: `updated_by=github_web`
5. เลื่อนลงมาที่ "Commit changes"
6. ใส่ commit message: "Update settings.txt via GitHub"
7. คลิก "Commit changes"

---

### Step 22: ตรวจสอบสถานะ Local (ก่อน fetch)

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

> ⚠️ **หมายเหตุ:** Git ยังไม่รู้ว่า remote มีการเปลี่ยนแปลง เพราะยังไม่ได้ติดต่อกับ remote

---

### Step 23: ดึงข้อมูลด้วย `git fetch`

```bash
git fetch origin
```

**ตัวอย่างผลลัพธ์:**
```
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 4 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), 1.05 KiB | 1.05 MiB/s, done.
From https://github.com/YOUR_USERNAME/ml-git-lab02_basic
   b2c3d4e..c3d4e5f  main       -> origin/main
```

> 📝 **อธิบาย:** `git fetch` ดึงข้อมูลจาก remote มาเก็บไว้ที่ `origin/main` แต่ยังไม่รวม (merge) กับ local `main`

---

### Step 24: ตรวจสอบความแตกต่างหลัง fetch

```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

**ดู commit ที่แตกต่างระหว่าง local และ origin:**
```bash
git log main..origin/main --oneline
```

**ตัวอย่างผลลัพธ์:**
```
c3d4e5f Update settings.txt via GitHub
```

**ดู commit ทั้งหมด:**
```bash
git log --oneline --all --graph
```

**ตัวอย่างผลลัพธ์:**
```
* c3d4e5f (origin/main) Update settings.txt via GitHub
* b2c3d4e (HEAD -> main) Add utility files, config และ sample data
* a1b2c3d Initial commit: เพิ่ม main.py
```

---

### Step 25: ดูความแตกต่างของไฟล์

```bash
git diff main origin/main
```

**ตัวอย่างผลลัพธ์:**
```diff
diff --git a/config/settings.txt b/config/settings.txt
index 8a7b3c4..9d8e7f6 100644
--- a/config/settings.txt
+++ b/config/settings.txt
@@ -3,3 +3,4 @@ app_name=GitLab02
 version=1.0
 debug=true
 language=th
+updated_by=github_web
```

**ดูเฉพาะรายชื่อไฟล์ที่แตกต่าง:**
```bash
git diff --name-only main origin/main
```

**ตัวอย่างผลลัพธ์:**
```
config/settings.txt
```

---

### Step 26: รวมการเปลี่ยนแปลงด้วย `git merge`

```bash
git merge origin/main
```

**ตัวอย่างผลลัพธ์:**
```
Updating b2c3d4e..c3d4e5f
Fast-forward
 config/settings.txt | 1 +
 1 file changed, 1 insertion(+)
```

**ตรวจสอบไฟล์:**
```bash
cat config/settings.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Application Settings
app_name=GitLab02
version=1.0
debug=true
language=th
updated_by=github_web
```

**ตรวจสอบ log:**
```bash
git log --oneline -3
```

**ตัวอย่างผลลัพธ์:**
```
c3d4e5f (HEAD -> main, origin/main) Update settings.txt via GitHub
b2c3d4e Add utility files, config และ sample data
a1b2c3d Initial commit: เพิ่ม main.py
```

---

### Step 27: จำลองการเปลี่ยนแปลงอีกครั้งบน GitHub

**ไปที่ GitHub:**
1. แก้ไขไฟล์ `data/sample.txt`
2. เพิ่มบรรทัด: `item4,300,active`
3. Commit changes ด้วย message: "Add item4 to sample data"

---

### Step 28: ใช้ `git pull` (fetch + merge ในคำสั่งเดียว)

```bash
git pull origin main
```

**ตัวอย่างผลลัพธ์:**
```
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 4 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
From https://github.com/YOUR_USERNAME/ml-git-lab02_basic
   c3d4e5f..d4e5f6g  main       -> origin/main
Updating c3d4e5f..d4e5f6g
Fast-forward
 data/sample.txt | 1 +
 1 file changed, 1 insertion(+)
```

> 📝 **อธิบาย:** `git pull` = `git fetch` + `git merge` ในคำสั่งเดียว

**ตรวจสอบไฟล์:**
```bash
cat data/sample.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Sample Data File
item1,100,active
item2,200,inactive
item3,150,active
item4,300,active
```

---

## 🔍 Part 5: การใช้งาน `git checkout origin/main` แบบละเอียด

### Overview ของ `git checkout origin/main`

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    git checkout origin/main - Use Cases                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   1. ดู Remote Branch (Detached HEAD)                                           │
│      git checkout origin/main                                                    │
│                                                                                  │
│   2. ดึงไฟล์เฉพาะจาก Remote                                                      │
│      git checkout origin/main -- <file>                                          │
│                                                                                  │
│   3. ดึงทั้งโฟลเดอร์จาก Remote                                                   │
│      git checkout origin/main -- <folder>/                                       │
│                                                                                  │
│   4. เปรียบเทียบไฟล์ระหว่าง Local และ Remote                                    │
│      git diff main origin/main -- <file>                                         │
│                                                                                  │
│   5. สร้าง Branch ใหม่จาก Remote                                                 │
│      git checkout -b <new-branch> origin/main                                    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 29: เตรียมสภาพแวดล้อมสำหรับทดสอบ

```bash
# ตรวจสอบว่าอยู่ใน main branch
git checkout main

# fetch ข้อมูลล่าสุดจาก remote ก่อนเสมอ
git fetch origin
```

**ตัวอย่างผลลัพธ์:**
```
Already on 'main'
Your branch is up to date with 'origin/main'.
```

---

### Step 30: จำลองการเปลี่ยนแปลงบน GitHub อีกครั้ง

**ไปที่ GitHub แก้ไขไฟล์ `src/utils.py`:**
1. คลิกที่ `src/utils.py`
2. คลิก Edit (✏️)
3. เพิ่ม function ใหม่ที่ท้ายไฟล์:

```python

def multiply(a, b):
    """คูณตัวเลขสองตัว"""
    return a * b
```

4. Commit changes: "Add multiply function"

**Fetch การเปลี่ยนแปลง:**
```bash
git fetch origin
```

**ตัวอย่างผลลัพธ์:**
```
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 1), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (4/4), done.
From https://github.com/YOUR_USERNAME/ml-git-lab02_basic
   d4e5f6g..e5f6g7h  main       -> origin/main
```

---

### Step 31: ตัวอย่างที่ 1 - เข้าสู่ Detached HEAD State

```bash
git checkout origin/main
```

**ตัวอย่างผลลัพธ์:**
```
Note: switching to 'origin/main'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at e5f6g7h Add multiply function
```

> 📝 **อธิบาย:** 
> - **Detached HEAD** หมายความว่าเราไม่ได้อยู่บน branch ใดๆ
> - เหมาะสำหรับการดูหรือทดสอบโค้ดจาก remote โดยไม่กระทบ local branch
> - การเปลี่ยนแปลงที่ทำจะไม่ถูกบันทึกถาวรถ้าไม่สร้าง branch ใหม่

**ตรวจสอบสถานะ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
HEAD detached at origin/main
nothing to commit, working tree clean
```

**ดูว่าอยู่ที่ commit ไหน:**
```bash
git log --oneline -5
```

**ตัวอย่างผลลัพธ์:**
```
e5f6g7h (HEAD, origin/main) Add multiply function
d4e5f6g Add item4 to sample data
c3d4e5f Update settings.txt via GitHub
b2c3d4e (main) Add utility files, config และ sample data
a1b2c3d Initial commit: เพิ่ม main.py
```

**ดูเนื้อหาไฟล์บน origin/main:**
```bash
cat src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```python
"""
Utility Functions Module
"""

def greet(name):
    """ทักทายผู้ใช้"""
    return f"สวัสดี, {name}!"

def calculate_sum(numbers):
    """คำนวณผลรวมของตัวเลข"""
    return sum(numbers)

def calculate_average(numbers):
    """คำนวณค่าเฉลี่ย"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def multiply(a, b):
    """คูณตัวเลขสองตัว"""
    return a * b
```

**กลับไปยัง main branch:**
```bash
git checkout main
```

**ตัวอย่างผลลัพธ์:**
```
Switched to branch 'main'
Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
```

---

### Step 32: ตัวอย่างที่ 2 - ดึงไฟล์เฉพาะจาก Remote

**ตรวจสอบความแตกต่างก่อน:**
```bash
git diff main origin/main -- src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```diff
diff --git a/src/utils.py b/src/utils.py
index abc1234..def5678 100644
--- a/src/utils.py
+++ b/src/utils.py
@@ -13,3 +13,7 @@ def calculate_average(numbers):
     if len(numbers) == 0:
         return 0
     return sum(numbers) / len(numbers)
+
+def multiply(a, b):
+    """คูณตัวเลขสองตัว"""
+    return a * b
```

**ดึงไฟล์จาก origin/main (โดยไม่เปลี่ยน branch):**
```bash
git checkout origin/main -- src/utils.py
```

**ตรวจสอบไฟล์:**
```bash
cat src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```python
"""
Utility Functions Module
"""

def greet(name):
    """ทักทายผู้ใช้"""
    return f"สวัสดี, {name}!"

def calculate_sum(numbers):
    """คำนวณผลรวมของตัวเลข"""
    return sum(numbers)

def calculate_average(numbers):
    """คำนวณค่าเฉลี่ย"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def multiply(a, b):
    """คูณตัวเลขสองตัว"""
    return a * b
```

**ตรวจสอบสถานะ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/utils.py
```

> 📝 **อธิบาย:** ไฟล์ถูกดึงมาและเพิ่มเข้า staging area โดยอัตโนมัติ

**ยกเลิกการเปลี่ยนแปลง (เพื่อทดสอบต่อ):**
```bash
git restore --staged src/utils.py
git restore src/utils.py
```

---

### Step 33: ตัวอย่างที่ 3 - ดึงหลายไฟล์พร้อมกัน

```bash
git checkout origin/main -- config/settings.txt data/sample.txt
```

**ตรวจสอบ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   config/settings.txt
        modified:   data/sample.txt
```

**ยกเลิกการเปลี่ยนแปลง:**
```bash
git restore --staged .
git restore .
```

---

### Step 34: ตัวอย่างที่ 4 - ดึงทั้งโฟลเดอร์จาก Remote

```bash
git checkout origin/main -- src/
```

**ตรวจสอบ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/utils.py
```

> 📝 **อธิบาย:** ไฟล์ทั้งหมดในโฟลเดอร์ `src/` ถูกดึงมาจาก origin/main

**ยกเลิกการเปลี่ยนแปลง:**
```bash
git restore --staged .
git restore .
```

---

### Step 35: ตัวอย่างที่ 5 - กู้คืนไฟล์ที่แก้ไขผิดพลาด

**สร้างการเปลี่ยนแปลงที่ผิดพลาด:**
```bash
cat > src/main.py << 'EOF'
# OOPS! ลบโค้ดทั้งหมดโดยไม่ตั้งใจ
print("mistake!")
EOF
```

**ดูความเสียหาย:**
```bash
cat src/main.py
```

**ตัวอย่างผลลัพธ์:**
```python
# OOPS! ลบโค้ดทั้งหมดโดยไม่ตั้งใจ
print("mistake!")
```

**ตรวจสอบสถานะ:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/main.py
```

**กู้คืนจาก origin/main:**
```bash
git checkout origin/main -- src/main.py
```

**ตรวจสอบว่ากู้คืนสำเร็จ:**
```bash
cat src/main.py
```

**ตัวอย่างผลลัพธ์:**
```python
#!/usr/bin/env python3
"""
Main Application Module
Version: 1.0
"""

def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    print("Hello from Git Lab 02!")
    print("Learning Git basics...")

if __name__ == "__main__":
    main()
```

> ✅ **สำเร็จ!** ไฟล์ถูกกู้คืนจาก remote แล้ว

**ยกเลิกการเปลี่ยนแปลง:**
```bash
git restore --staged .
git restore .
```

---

### Step 36: ตัวอย่างที่ 6 - เปรียบเทียบไฟล์ก่อนตัดสินใจ

**ดู diff ของไฟล์เดียว:**
```bash
git diff HEAD origin/main -- src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```diff
diff --git a/src/utils.py b/src/utils.py
index abc1234..def5678 100644
--- a/src/utils.py
+++ b/src/utils.py
@@ -13,3 +13,7 @@ def calculate_average(numbers):
     if len(numbers) == 0:
         return 0
     return sum(numbers) / len(numbers)
+
+def multiply(a, b):
+    """คูณตัวเลขสองตัว"""
+    return a * b
```

**ดู diff ของทั้งโปรเจค:**
```bash
git diff HEAD origin/main
```

**ดูรายชื่อไฟล์ที่แตกต่าง:**
```bash
git diff --name-only HEAD origin/main
```

**ตัวอย่างผลลัพธ์:**
```
config/settings.txt
data/sample.txt
src/utils.py
```

**ดูสถิติความแตกต่าง:**
```bash
git diff --stat HEAD origin/main
```

**ตัวอย่างผลลัพธ์:**
```
 config/settings.txt | 1 +
 data/sample.txt     | 1 +
 src/utils.py        | 4 ++++
 3 files changed, 6 insertions(+)
```

---

### Step 37: ตัวอย่างที่ 7 - สร้าง Branch ใหม่จาก origin/main

```bash
git checkout -b feature-from-remote origin/main
```

**ตัวอย่างผลลัพธ์:**
```
Switched to a new branch 'feature-from-remote'
branch 'feature-from-remote' set up to track 'origin/main'.
```

**ตรวจสอบ branch:**
```bash
git branch -vv
```

**ตัวอย่างผลลัพธ์:**
```
* feature-from-remote e5f6g7h [origin/main] Add multiply function
  main                b2c3d4e [origin/main: behind 3] Add utility files, config และ sample data
```

**ดู branch ทั้งหมด:**
```bash
git branch -a
```

**ตัวอย่างผลลัพธ์:**
```
* feature-from-remote
  main
  remotes/origin/main
```

**กลับไป main:**
```bash
git checkout main
```

**ลบ branch ที่สร้างทดสอบ:**
```bash
git branch -d feature-from-remote
```

**ตัวอย่างผลลัพธ์:**
```
Deleted branch feature-from-remote (was e5f6g7h).
```

---

### Step 38: ตัวอย่างที่ 8 - ดูไฟล์จาก Remote โดยไม่เปลี่ยน Working Directory

**ใช้ `git show` แทน checkout:**
```bash
git show origin/main:src/utils.py
```

**ตัวอย่างผลลัพธ์:**
```python
"""
Utility Functions Module
"""

def greet(name):
    """ทักทายผู้ใช้"""
    return f"สวัสดี, {name}!"

def calculate_sum(numbers):
    """คำนวณผลรวมของตัวเลข"""
    return sum(numbers)

def calculate_average(numbers):
    """คำนวณค่าเฉลี่ย"""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def multiply(a, b):
    """คูณตัวเลขสองตัว"""
    return a * b
```

> 📝 **อธิบาย:** `git show` แสดงเนื้อหาไฟล์โดยไม่เปลี่ยนแปลง working directory

**บันทึกออกมาเป็นไฟล์ใหม่:**
```bash
git show origin/main:src/utils.py > utils_from_remote.py
```

**ตรวจสอบ:**
```bash
ls -la *.py 2>/dev/null || echo "ไม่มีไฟล์ .py ใน directory ปัจจุบัน"
cat utils_from_remote.py
```

**ลบไฟล์ทดสอบ:**
```bash
rm -f utils_from_remote.py
```

---

### Step 39: ตัวอย่างที่ 9 - ดูโครงสร้างไฟล์บน Remote

```bash
git ls-tree origin/main
```

**ตัวอย่างผลลัพธ์:**
```
040000 tree 1234567890abcdef1234567890abcdef12345678    config
040000 tree abcdef1234567890abcdef1234567890abcdef12    data
040000 tree 567890abcdef1234567890abcdef1234567890ab    src
```

**ดูไฟล์ในโฟลเดอร์ย่อย:**
```bash
git ls-tree origin/main src/
```

**ตัวอย่างผลลัพธ์:**
```
100644 blob abc123def456abc123def456abc123def456abc1    src/main.py
100644 blob def456abc123def456abc123def456abc123def4    src/utils.py
```

**ดูแบบ recursive (ทุกไฟล์):**
```bash
git ls-tree -r origin/main
```

**ตัวอย่างผลลัพธ์:**
```
100644 blob abc123def456abc123def456abc123def456abc1    config/settings.txt
100644 blob def456abc123def456abc123def456abc123def4    data/sample.txt
100644 blob 123456abcdef123456abcdef123456abcdef1234    src/main.py
100644 blob 456789abcdef456789abcdef456789abcdef4567    src/utils.py
```

---

### Step 40: ตัวอย่างที่ 10 - ดูไฟล์จาก Commit เฉพาะ

**ดู commit history ของ remote:**
```bash
git log origin/main --oneline -5
```

**ตัวอย่างผลลัพธ์:**
```
e5f6g7h Add multiply function
d4e5f6g Add item4 to sample data
c3d4e5f Update settings.txt via GitHub
b2c3d4e Add utility files, config และ sample data
a1b2c3d Initial commit: เพิ่ม main.py
```

**ดูไฟล์จาก commit เฉพาะ (เช่น c3d4e5f):**
```bash
git show c3d4e5f:config/settings.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Application Settings
app_name=GitLab02
version=1.0
debug=true
language=th
updated_by=github_web
```

**เปรียบเทียบกับ commit ก่อนหน้า (b2c3d4e):**
```bash
git show b2c3d4e:config/settings.txt
```

**ตัวอย่างผลลัพธ์:**
```
# Application Settings
app_name=GitLab02
version=1.0
debug=true
language=th
```

> 📝 **อธิบาย:** สามารถดูไฟล์จาก commit ใดๆ ในประวัติได้

---

### Step 41: Sync local กับ remote ให้เป็นปัจจุบัน

```bash
git pull origin main
```

**ตัวอย่างผลลัพธ์:**
```
Updating b2c3d4e..e5f6g7h
Fast-forward
 config/settings.txt | 1 +
 data/sample.txt     | 1 +
 src/utils.py        | 4 ++++
 3 files changed, 6 insertions(+)
```

**ตรวจสอบว่า sync แล้ว:**
```bash
git status
```

**ตัวอย่างผลลัพธ์:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 📊 Part 6: สรุปคำสั่งที่เรียนรู้

### คำสั่งพื้นฐาน

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git init` | สร้าง repository ใหม่ |
| `git status` | ตรวจสอบสถานะของไฟล์ |
| `git add <file>` | เพิ่มไฟล์เข้า staging area |
| `git add .` | เพิ่มไฟล์ทั้งหมดเข้า staging area |
| `git commit -m "message"` | บันทึกการเปลี่ยนแปลง |
| `git log --oneline` | ดูประวัติ commit แบบย่อ |
| `git log --oneline --graph --all` | ดูประวัติแบบ graph |

### คำสั่ง Remote

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git remote add <name> <url>` | เพิ่ม remote repository |
| `git remote -v` | ดูรายการ remote ทั้งหมด |
| `git remote show origin` | ดูรายละเอียด remote |
| `git push -u origin main` | push และตั้งค่า upstream |
| `git push` | push (หลังตั้งค่า upstream แล้ว) |

### คำสั่ง Branch

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git branch` | ดู local branches |
| `git branch -r` | ดู remote branches |
| `git branch -a` | ดู branches ทั้งหมด |
| `git branch -vv` | ดู branches พร้อม tracking info |

### คำสั่ง Fetch/Merge/Pull

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `git fetch origin` | ดึงข้อมูลจาก remote (ไม่ merge) |
| `git merge origin/main` | รวมการเปลี่ยนแปลงจาก remote |
| `git pull origin main` | fetch + merge ในคำสั่งเดียว |
| `git diff main origin/main` | เปรียบเทียบ local กับ remote |

### คำสั่ง Checkout origin/main

| คำสั่ง | ผลลัพธ์ |
|--------|---------|
| `git checkout origin/main` | เข้าสู่ Detached HEAD ดูโค้ดบน remote |
| `git checkout origin/main -- <file>` | ดึงไฟล์เฉพาะมา (staged อัตโนมัติ) |
| `git checkout origin/main -- <folder>/` | ดึงทั้งโฟลเดอร์มา |
| `git checkout -b <branch> origin/main` | สร้าง branch ใหม่จาก remote |
| `git show origin/main:<file>` | แสดงเนื้อหาไฟล์ (ไม่เปลี่ยน working dir) |
| `git ls-tree origin/main` | ดูโครงสร้างไฟล์บน remote |

---

## ⚠️ ข้อควรระวัง

1. **ต้อง `git fetch` ก่อนเสมอ** - ถ้าไม่ fetch, origin/main จะเป็นข้อมูลเก่า
2. **Detached HEAD** - ระวังการ commit ใน state นี้ อาจสูญหายได้
3. **Checkout ไฟล์จะ staged อัตโนมัติ** - ถ้าไม่ต้องการต้อง unstage ก่อน commit
4. **ไม่ควรแก้ไขไฟล์ใน Detached HEAD** โดยไม่สร้าง branch ใหม่
5. **ตรวจสอบ `git status` บ่อยๆ** - เพื่อให้รู้ว่าอยู่ใน state ใด

---

## ✅ แบบฝึกหัดท้าย Lab

### แบบฝึกหัดที่ 1: Basic Workflow
1. สร้างไฟล์ใหม่ `src/helper.py` ด้วย `cat > ... << 'EOF'`
2. ใช้ `git add` และ `git commit` บันทึกการเปลี่ยนแปลง
3. Push ขึ้น remote ด้วย `git push`

### แบบฝึกหัดที่ 2: Remote Sync
1. แก้ไขไฟล์บน GitHub Web Interface
2. ใช้ `git fetch` แล้ว `git diff` ดูความแตกต่าง
3. ใช้ `git merge` หรือ `git pull` ดึงการเปลี่ยนแปลงลงมา

### แบบฝึกหัดที่ 3: Checkout Practice
1. ใช้ `git checkout origin/main` เข้าสู่ Detached HEAD
2. ดูไฟล์ต่างๆ แล้วกลับมา main ด้วย `git checkout main`
3. ใช้ `git checkout origin/main -- <file>` ดึงไฟล์เฉพาะมา
4. ใช้ `git show origin/main:<file>` ดูไฟล์โดยไม่เปลี่ยน working directory

### แบบฝึกหัดที่ 4: Branch from Remote
1. สร้าง branch ใหม่จาก origin/main ด้วย `git checkout -b test-branch origin/main`
2. แก้ไขไฟล์และ commit
3. กลับไป main และลบ branch ทดสอบ

---

## 🧹 ทำความสะอาด (Optional)

```bash
# กลับไปโฟลเดอร์ก่อนหน้า
cd ..

# ลบโฟลเดอร์โปรเจค (ถ้าต้องการ)
rm -rf ml-git-lab02_basic
```

---

## 📚 อ้างอิงเพิ่มเติม

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [Pro Git Book (ภาษาไทย)](https://git-scm.com/book/th/v2)

