# Lab 01: Git Fundamentals

## 🎯 Pipeline Overview

ก่อนเริ่ม LAB มาทำความเข้าใจภาพรวมของ Git workflow กันก่อน:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🎯 Git Fundamentals Pipeline                         │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: Setup                Step 2-3: Basic Workflow
─────────────                ────────────────────────
                             
  📁 mkdir                     📝 Edit Files
     │                              │
     ▼                              ▼
  📂 cd                        ┌─────────┐    git diff
     │                         │ Working │ ◄────────── 👁️ ดูความแตกต่าง
     ▼                         │Directory│
  🎬 git init                  └────┬────┘
     │                              │ git add
     ▼                              ▼
  📦 .git/                     ┌─────────┐
   (repository)                │ Staging │
                               │  Area   │
                               └────┬────┘
                                    │ git commit
                                    ▼
                               ┌─────────┐
                               │  Local  │
                               │  Repo   │
                               │ (.git/) │
                               └─────────┘

Step 4: .gitignore           Step 5-6: History & Branch
──────────────────           ─────────────────────────

  🚫 .gitignore                 📜 git log
     │                              │
     ├── .env         ────►         ▼
     └── *.log                  ┌─────────────┐
                                │ Commit      │
  ❌ ไม่ถูก track               │ History     │
                                └─────────────┘
                                      │
                                      ▼
                                🌿 git branch -m
                                   (rename branch)
```


---

## 📋 Learning Objectives

| Step | หัวข้อ | คำสั่งหลัก | เป้าหมาย |
|------|--------|-----------|----------|
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

---

## 📝 Lab Instructions

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

   > 💡 *This creates a hidden `.git` folder that tracks your changes.*

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

2. **Check Status**

   See how Git views these new files:

   ```bash
   git status
   ```

   > 💡 *You should see the files listed as "Untracked files".*

3. **Stage the files**

   Add the files to the "Staging Area". This tells Git you want to include these updates in the next snapshot.

   ```bash
   git add file1.txt file2.txt file3.txt
   ```

4. **Commit**

   Save the snapshot with a descriptive message:

   ```bash
   git commit -m "Initial commit with three files"
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

2. **Inspect Changes**

   Before adding, it is good practice to review exactly what changed:

   ```bash
   git diff
   ```

   > 💡 *This shows the line-by-line differences between your working directory and the last commit.*

   **Example Output:**
   ```diff
   diff --git a/file1.txt b/file1.txt
   --- a/file1.txt
   +++ b/file1.txt
   @@ -1 +1,2 @@
    Content for file 1
   +Additional content for file 1
   ```

3. **Commit Step-by-Step**

   Let's modify the staging area and commit:

   ```bash
   git add file1.txt file2.txt
   git commit -m "Updated file1 and file2"
   ```

---

### Step 4: Ignoring Files with `.gitignore`

Sometimes you have files you do NOT want to track (temporary files, partial builds, secrets).

```
   🚫 .gitignore
        │
        ├── .env      ──► ❌ Ignored (secrets)
        └── *.log     ──► ❌ Ignored (logs)
```

1. **Create "secret" files**

   These mimic files that shouldn't be in Git:

   ```bash
   echo "Secret API Key" > .env
   echo "Debug logs..." > debug.log
   ```

2. **Create `.gitignore`**

   Create a special file named `.gitignore` and list the patterns to ignore:

   ```bash
   echo ".env" > .gitignore
   echo "*.log" >> .gitignore
   ```

3. **Verify Status**

   Check status again. You should see `.gitignore` as a new untracked file, but NOT `.env` or `debug.log`:

   ```bash
   git status
   ```

   **Expected Output:**
   ```
   Untracked files:
     .gitignore

   (notice .env and debug.log are NOT listed)
   ```

4. **Final Commit**

   Add the ignore file and any other pending changes:

   ```bash
   echo "More content" >> file3.txt
   git add .
   git commit -m "Final update with gitignore"
   ```

---

### Step 5: Review History

Look at the history of your project:

```bash
git log --oneline --graph --all
```

**Example Output:**
```
* a1b2c3d (HEAD -> master) Final update with gitignore
* e4f5g6h Updated file1 and file2
* i7j8k9l Initial commit with three files
```

---

### Step 6: Renaming Branches

Git allows you to rename branches easily. This is commonly used to rename the default `master` branch to `main`.

```
   🌿 master  ───►  git branch -m  ───►  🌿 main
```

1. **Check current branch name**

   First, see what branch you're on:

   ```bash
   git branch
   ```

   > 💡 *The asterisk (*) indicates your current branch.*

2. **Rename the current branch to `main`**

   Use the `-m` (move) flag to rename:

   ```bash
   git branch -m main
   ```

3. **Verify the rename**

   ```bash
   git branch
   ```

   > ✅ *You should now see `main` instead of `master`.*

4. **Rename it back to `master`**

   You can rename branches as many times as needed:

   ```bash
   git branch -m master
   ```

5. **Rename a branch you're NOT on** (optional)

   If you want to rename a different branch, specify both names:

   ```bash
   git branch -m old-name new-name
   ```

> ⚠️ **Note**: If you're working with a remote repository (like GitHub), renaming the local branch doesn't automatically update the remote. You would need to push the new branch and delete the old one on the remote.

---

## 📚 Summary

### Commands Learned

| Command | Description |
|---------|-------------|
| `git init` | Initialize a new repository |
| `git status` | Check the state of your files |
| `git add <file>` | Stage changes for commit |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save a snapshot of staged changes |
| `git diff` | View differences between working directory and last commit |
| `git log` | View commit history |
| `git log --oneline --graph --all` | View compact commit history with graph |
| `git branch` | List branches |
| `git branch -m <new-name>` | Rename current branch |

