# Lab 01: Git Fundamentals

## 🎯 Pipeline Overview

ก่อนเริ่ม LAB มาทำความเข้าใจภาพรวมของ Git workflow ทั้ง 7 ขั้นตอน:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          🎯 Git Fundamentals Pipeline                           │
└─────────────────────────────────────────────────────────────────────────────────┘

  Step 0                Step 1              Steps 2-3             Step 4
  CONFIG               SETUP            BASIC WORKFLOW          GITIGNORE
┌──────────┐        ┌──────────┐        ┌──────────┐         ┌──────────┐
│ 👤 ตั้งค่า │        │ 📁 สร้าง   │        │ 📝 แก้ไข   │         │ 🚫 กำหนด  │
│  ตัวตน    │───────▶│ Repository│───────▶│ และบันทึก  │────────▶│ ไฟล์ที่   │
│          │        │          │        │          │         │ ไม่ track │
└──────────┘        └──────────┘        └──────────┘         └──────────┘
     │                   │                   │                    │
     ▼                   ▼                   ▼                    ▼
 git config          git init           git add              .gitignore
 --global                               git commit           .env, *.log
                                        git diff


  Step 5                Step 6
  HISTORY              BRANCH
┌──────────┐        ┌──────────┐
│ 📜 ดู     │        │ 🌿 จัดการ │
│ ประวัติ   │───────▶│  Branch  │───────▶  ✅ DONE!
│          │        │          │
└──────────┘        └──────────┘
     │                   │
     ▼                   ▼
  git log           git branch -m


═══════════════════════════════════════════════════════════════════════════════════
                              📦 Git Three Areas
═══════════════════════════════════════════════════════════════════════════════════

  ┌─────────────────┐      git add       ┌─────────────────┐     git commit     ┌─────────────────┐
  │                 │ ─────────────────▶ │                 │ ─────────────────▶ │                 │
  │    WORKING      │                    │     STAGING     │                    │      LOCAL      │
  │   DIRECTORY     │                    │      AREA       │                    │   REPOSITORY    │
  │                 │                    │                 │                    │                 │
  │  📝 แก้ไขไฟล์    │                    │  📦 เตรียม commit │                    │  💾 บันทึกถาวร   │
  └─────────────────┘                    └─────────────────┘                    └─────────────────┘
         │                                                                              │
         │                              git diff                                        │
         │◀─────────────────────────────────────────────────────────────────────────────│
         │                         (เปรียบเทียบความต่าง)                                  │
```

---

## 📋 Learning Objectives

| Step | หัวข้อ | คำสั่งหลัก | เป้าหมาย |
|------|--------|-----------|----------|
| 0 | Configuration | `git config` | ตั้งค่าข้อมูลผู้ใช้ |
| 1 | Initial Setup | `git init` | สร้าง repository ใหม่ |
| 2 | Basic Workflow | `git add`, `git commit` | เข้าใจ staging และ commit |
| 3 | View Changes | `git diff`, `git status` | ตรวจสอบความเปลี่ยนแปลง |
| 4 | Ignore Files | `.gitignore` | ระบุไฟล์ที่ไม่ต้องการ track |
| 5 | History | `git log` | ดูประวัติ commits |
| 6 | Branch | `git branch -m` | เปลี่ยนชื่อ branch |

---

## ⚙️ Prerequisites

- Git must be installed on your machine
- ตรวจสอบด้วยคำสั่ง: `git --version`
- Tree command (optional): `sudo apt install tree` หรือ `brew install tree`

---

## 📝 Lab Instructions

### Step 0: Configure Git Identity

ก่อนเริ่มใช้งาน Git ครั้งแรก **จำเป็นต้องตั้งค่าข้อมูลผู้ใช้ก่อน** เพราะทุกครั้งที่ทำ commit Git จะบันทึกว่าใครเป็นคนทำการเปลี่ยนแปลง

```
   👤 user.name  ───►  🏷️ ชื่อที่แสดงใน commit
   📧 user.email ───►  🏷️ email ที่แสดงใน commit
```

1. **ตั้งค่าชื่อผู้ใช้**

   ```bash
   git config --global user.name "YourUsername"
   ```

   > 💡 *เปลี่ยน `YourUsername` เป็นชื่อของคุณ เช่น `"Somchai Jaidee"`*

2. **ตั้งค่า email**

   ```bash
   git config --global user.email "youremail@example.com"
   ```

   > 💡 *เปลี่ยน `youremail@example.com` เป็น email ของคุณ*

3. **ตรวจสอบการตั้งค่า**

   ```bash
   git config --list
   ```

   **Expected Output:**
   ```
   user.name=YourUsername
   user.email=youremail@example.com
   ...
   ```

   หรือตรวจสอบทีละค่า:

   ```bash
   git config user.name
   git config user.email
   ```

**🔑 คำอธิบาย `git config`:**

| Option | ความหมาย |
|--------|----------|
| `--global` | ตั้งค่าสำหรับผู้ใช้ทั้งระบบ (ใช้ได้กับทุก repository) |
| `--local` | ตั้งค่าเฉพาะ repository ปัจจุบัน (ค่า default ถ้าไม่ระบุ) |
| `--system` | ตั้งค่าสำหรับทุกผู้ใช้ในเครื่อง (ต้องการสิทธิ์ admin) |
| `user.name` | ชื่อที่จะปรากฏใน commit history |
| `user.email` | email ที่จะปรากฏใน commit history |


---

### Step 1: Initial Setup

1. **Create a working directory**

   Open your terminal and run the following commands to create a directory for this lab:

   ```bash
   mkdir git-lab
   cd git-lab
   ```

2. **Initialize Git**

   Initialize a new Git repository in this directory:

   ```bash
   git init
   ```

3. **View directory structure with `tree`**

   ใช้คำสั่ง `tree` เพื่อดูโครงสร้างโฟลเดอร์:

   ```bash
   tree -a -L 2
   ```

   **Expected Output:**
   ```
   .
   └── .git
       ├── HEAD
       ├── config
       ├── description
       ├── hooks
       ├── info
       ├── objects
       └── refs
   ```

   > 💡 *`-a` แสดงไฟล์ hidden, `-L 2` แสดง 2 ระดับ*
   > 💡 *โฟลเดอร์ `.git` คือที่เก็บข้อมูล repository ทั้งหมด*

---

### Step 2: The Basic Workflow (Edit, Add, Commit)

```
   📝 Create Files  ───►  📦 git add  ───►  💾 git commit
```

1. **Create some files**

   Create three text files with some content:

   ```bash
   echo "Content for file 1" > file1.txt
   echo "Content for file 2" > file2.txt
   echo "Content for file 3" > file3.txt
   ```

2. **View directory structure**

   ```bash
   tree -a -L 1
   ```

   **Expected Output:**
   ```
   .
   ├── .git
   ├── file1.txt
   ├── file2.txt
   └── file3.txt
   ```

3. **📄 File Contents Created:**

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file1.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 1                                      │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file2.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 2                                      │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file3.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 3                                      │
   └─────────────────────────────────────────────────────────┘
   ```

   **🔍 Verify file contents:**
   ```bash
   cat file1.txt
   cat file2.txt
   cat file3.txt
   ```

4. **Check Status**

   See how Git views these new files:

   ```bash
   git status
   ```

   **Expected Output:**
   ```
   On branch master

   No commits yet

   Untracked files:
     (use "git add <file>..." to include in what will be committed)
           file1.txt
           file2.txt
           file3.txt

   nothing added to commit but untracked files present (use "git add" to track)
   ```

   > 💡 *"Untracked files" = ไฟล์ใหม่ที่ Git ยังไม่ได้ติดตาม*

5. **Stage the files**

   Add the files to the "Staging Area":

   ```bash
   git add file1.txt file2.txt file3.txt
   ```

   **Check status after staging:**
   ```bash
   git status
   ```

   **Expected Output:**
   ```
   On branch master

   No commits yet

   Changes to be committed:
     (use "git rm --cached <file>..." to unstage)
           new file:   file1.txt
           new file:   file2.txt
           new file:   file3.txt
   ```

   > 💡 *"Changes to be committed" = ไฟล์พร้อมที่จะ commit แล้ว*

6. **Commit**

   Save the snapshot with a descriptive message:

   ```bash
   git commit -m "Initial commit with three files"
   ```

   **Expected Output:**
   ```
   [master (root-commit) abc1234] Initial commit with three files
    3 files changed, 3 insertions(+)
    create mode 100644 file1.txt
    create mode 100644 file2.txt
    create mode 100644 file3.txt
   ```

---

### Step 3: Modifying Files and using `git diff`

```
   📝 Modify  ───►  👁️ git diff  ───►  📦 git add  ───►  💾 git commit
```

1. **Modify files**

   Append new content to two of existing files:

   ```bash
   echo "Additional content for file 1" >> file1.txt
   echo "Additional content for file 2" >> file2.txt
   ```

2. **📄 File Contents After Modification:**

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file1.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 1                                      │
   │ Additional content for file 1    ◄── 🆕 NEW LINE ADDED  │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file2.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 2                                      │
   │ Additional content for file 2    ◄── 🆕 NEW LINE ADDED  │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file3.txt                      (ไม่มีการเปลี่ยนแปลง)    │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 3                                      │
   └─────────────────────────────────────────────────────────┘
   ```

   **🔍 Verify changes:**
   ```bash
   cat file1.txt
   ```

3. **Inspect Changes with `git diff`**

   Before adding, review exactly what changed:

   ```bash
   git diff
   ```

   **Expected Output:**
   ```diff
   diff --git a/file1.txt b/file1.txt
   index 1234567..abcdefg 100644
   --- a/file1.txt
   +++ b/file1.txt
   @@ -1 +1,2 @@
    Content for file 1
   +Additional content for file 1

   diff --git a/file2.txt b/file2.txt
   index 1234567..abcdefg 100644
   --- a/file2.txt
   +++ b/file2.txt
   @@ -1 +1,2 @@
    Content for file 2
   +Additional content for file 2
   ```

   **🔑 Understanding `git diff` Output:**

   | Symbol | Meaning |
   |--------|---------|
   | `+` (green) | บรรทัดที่เพิ่มเข้ามาใหม่ |
   | `-` (red) | บรรทัดที่ถูกลบออก |
   | `@@` | ตำแหน่งที่มีการเปลี่ยนแปลง |

4. **Commit the changes**

   ```bash
   git add file1.txt file2.txt
   git commit -m "Updated file1 and file2"
   ```

   **Expected Output:**
   ```
   [master def5678] Updated file1 and file2
    2 files changed, 2 insertions(+)
   ```

---

### Step 4: Ignoring Files with `.gitignore`

Sometimes you have files you do NOT want to track (temporary files, partial builds, secrets).

```
   🚫 .gitignore  ───►  .env     ❌ Ignored
                  ───►  *.log    ❌ Ignored
```

1. **Create "secret" files**

   These mimic files that shouldn't be in Git:

   ```bash
   echo "Secret API Key" > .env
   echo "Debug logs..." > debug.log
   ```

2. **View directory structure**

   ```bash
   tree -a -L 1
   ```

   **Expected Output:**
   ```
   .
   ├── .env
   ├── .git
   ├── debug.log
   ├── file1.txt
   ├── file2.txt
   └── file3.txt
   ```

3. **📄 Secret File Contents:**

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ 🔐 .env                      (SECRET - DO NOT COMMIT!)  │
   ├─────────────────────────────────────────────────────────┤
   │ Secret API Key                                          │
   └─────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────┐
   │ 📋 debug.log                    (LOG - DO NOT COMMIT!)  │
   ├─────────────────────────────────────────────────────────┤
   │ Debug logs...                                           │
   └─────────────────────────────────────────────────────────┘
   ```

4. **Create `.gitignore`**

   Create a special file named `.gitignore` and list the patterns to ignore:

   ```bash
   echo ".env" > .gitignore
   echo "*.log" >> .gitignore
   ```

5. **📄 `.gitignore` Contents:**

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ 🚫 .gitignore                                           │
   ├─────────────────────────────────────────────────────────┤
   │ .env          ◄── ignore ไฟล์ชื่อ .env                   │
   │ *.log         ◄── ignore ไฟล์ทุกไฟล์ที่ลงท้ายด้วย .log    │
   └─────────────────────────────────────────────────────────┘
   ```

6. **View updated directory structure**

   ```bash
   tree -a -L 1
   ```

   **Expected Output:**
   ```
   .
   ├── .env          ◄── ❌ IGNORED
   ├── .git
   ├── .gitignore    ◄── 🆕 NEW (will be tracked)
   ├── debug.log     ◄── ❌ IGNORED
   ├── file1.txt
   ├── file2.txt
   └── file3.txt
   ```

7. **Verify Status**

   Check status again. You should see `.gitignore` as a new untracked file, but NOT `.env` or `debug.log`:

   ```bash
   git status
   ```

   **Expected Output:**
   ```
   On branch master
   Untracked files:
     (use "git add <file>..." to include in what will be committed)
           .gitignore

   nothing added to commit but untracked files present (use "git add" to track)
   ```

   > ✅ *สังเกตว่า `.env` และ `debug.log` ไม่แสดงใน status แล้ว!*

8. **Add more content to file3 and Final Commit**

   ```bash
   echo "More content" >> file3.txt
   ```

   **📄 file3.txt After Modification:**

   ```
   ┌─────────────────────────────────────────────────────────┐
   │ 📄 file3.txt                                            │
   ├─────────────────────────────────────────────────────────┤
   │ Content for file 3                                      │
   │ More content                     ◄── 🆕 NEW LINE ADDED  │
   └─────────────────────────────────────────────────────────┘
   ```

   ```bash
   git add .
   git commit -m "Final update with gitignore"
   ```

   **Expected Output:**
   ```
   [master ghi9012] Final update with gitignore
    2 files changed, 3 insertions(+)
    create mode 100644 .gitignore
   ```

---

### Step 5: Review History

Look at the history of your project:

```bash
git log --oneline --graph --all
```

**Expected Output:**
```
* a1b2c3d (HEAD -> master) Final update with gitignore
* e4f5g6h Updated file1 and file2
* i7j8k9l Initial commit with three files
```

**📊 Commit History Visualization:**

```
┌──────────────────────────────────────────────────────────────────────┐
│                        📜 Commit History                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Commit 3: "Final update with gitignore"         ◄── HEAD (ปัจจุบัน)  │
│  ├── 🆕 Added: .gitignore                                            │
│  └── 📝 Modified: file3.txt (+1 line)                                │
│       │                                                              │
│       ▼                                                              │
│  Commit 2: "Updated file1 and file2"                                 │
│  ├── 📝 Modified: file1.txt (+1 line)                                │
│  └── 📝 Modified: file2.txt (+1 line)                                │
│       │                                                              │
│       ▼                                                              │
│  Commit 1: "Initial commit with three files"     ◄── First commit    │
│  ├── 🆕 Added: file1.txt                                             │
│  ├── 🆕 Added: file2.txt                                             │
│  └── 🆕 Added: file3.txt                                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**🔍 View Details of a Specific Commit:**
```bash
git show --stat HEAD
```

**Expected Output:**
```
commit a1b2c3d (HEAD -> master)
Author: Your Name <your.email@example.com>
Date:   ...

    Final update with gitignore

 .gitignore | 2 ++
 file3.txt  | 1 +
 2 files changed, 3 insertions(+)
```

---

### Step 6: Renaming Branches

Git allows you to rename branches easily. This is commonly used to rename the default `master` branch to `main`.

```
   🌿 master  ───►  git branch -m  ───►  🌿 main
```

1. **Check current branch name**

   ```bash
   git branch
   ```

   **Expected Output:**
   ```
   * master
   ```

   > 💡 *The asterisk (*) indicates your current branch.*

2. **Rename the current branch to `main`**

   ```bash
   git branch -m main
   ```

3. **Verify the rename**

   ```bash
   git branch
   ```

   **Expected Output:**
   ```
   * main
   ```

   > ✅ *เปลี่ยนชื่อจาก `master` เป็น `main` แล้ว!*

4. **Rename it back to `master`**

   ```bash
   git branch -m master
   git branch
   ```

   **Expected Output:**
   ```
   * master
   ```

5. **Rename a branch you're NOT on** (optional)

   If you want to rename a different branch, specify both names:

   ```bash
   git branch -m old-name new-name
   ```

> ⚠️ **Note**: If you're working with a remote repository (like GitHub), renaming the local branch doesn't automatically update the remote.

---

## 📊 Final State Summary

### Final Directory Structure

```bash
tree -a -L 1
```

**Expected Output:**
```
.
├── .env          ◄── ❌ NOT tracked (ignored)
├── .git          ◄── 📦 Git repository data
├── .gitignore    ◄── ✅ Tracked
├── debug.log     ◄── ❌ NOT tracked (ignored)
├── file1.txt     ◄── ✅ Tracked
├── file2.txt     ◄── ✅ Tracked
└── file3.txt     ◄── ✅ Tracked
```

### 📄 Final File Contents

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📄 file1.txt                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Content for file 1                                                          │
│ Additional content for file 1                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📄 file2.txt                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Content for file 2                                                          │
│ Additional content for file 2                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📄 file3.txt                                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Content for file 3                                                          │
│ More content                                                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🚫 .gitignore                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ .env                                                                        │
│ *.log                                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔐 .env (IGNORED - not in Git)                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Secret API Key                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 debug.log (IGNORED - not in Git)                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Debug logs...                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Summary

### Commands Learned

| Command | Description |
|---------|-------------|
| `git config --global user.name "name"` | ตั้งค่าชื่อผู้ใช้ (global) |
| `git config --global user.email "email"` | ตั้งค่า email ผู้ใช้ (global) |
| `git config --list` | แสดงการตั้งค่าทั้งหมด |
| `git init` | Initialize a new repository |
| `git status` | Check the state of your files |
| `git add <file>` | Stage changes for commit |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save a snapshot of staged changes |
| `git diff` | View differences between working directory and last commit |
| `git log` | View commit history |
| `git log --oneline --graph --all` | View compact commit history with graph |
| `git show --stat HEAD` | View details of the latest commit |
| `git branch` | List branches |
| `git branch -m <new-name>` | Rename current branch |
| `tree -a -L <level>` | แสดงโครงสร้างโฟลเดอร์ (รวมไฟล์ hidden) |

### Key Concepts

| Concept | Description |
|---------|-------------|
| Git Config | การตั้งค่า Git สำหรับผู้ใช้ (ชื่อ, email) |
| Working Directory | โฟลเดอร์ที่เราทำงานอยู่ - ที่เก็บไฟล์จริง |
| Staging Area | พื้นที่เตรียมไฟล์ก่อน commit |
| Repository (.git) | ฐานข้อมูล Git ที่เก็บประวัติทั้งหมด |
| Untracked | ไฟล์ใหม่ที่ Git ยังไม่รู้จัก |
| Staged | ไฟล์ที่พร้อมจะ commit |
| Committed | ไฟล์ที่บันทึกลง repository แล้ว |
| Ignored | ไฟล์ที่ Git จะไม่ track ตาม .gitignore |

---

## 🎯 Quick Reference: Tree Command

| Command | Description |
|---------|-------------|
| `tree` | แสดงโครงสร้างทั้งหมด |
| `tree -a` | แสดงรวมไฟล์ hidden (เริ่มด้วย `.`) |
| `tree -L 2` | แสดงแค่ 2 ระดับ |
| `tree -d` | แสดงเฉพาะโฟลเดอร์ |
| `tree -I "node_modules"` | ไม่แสดง pattern ที่กำหนด |
| `tree --gitignore` | ไม่แสดงไฟล์ที่อยู่ใน .gitignore |