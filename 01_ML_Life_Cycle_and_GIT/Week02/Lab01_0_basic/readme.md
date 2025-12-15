# Lab 01: Git Fundamentals

In this lab, you will practice the fundamental Git workflow: creating a repository, staging files, checking status, examining differences, and committing changes. We will also cover how to ignore specific files using `.gitignore`.

**Prerequisites**: Git must be installed on your machine.

---

## Lab Instructions

### Step 1: Initial Setup

1.  **Create a working directory**:
    Open your terminal and run the following commands to create a directory for this lab:
```bash
    mkdir git-lab
    cd git-lab
```

2.  **Initialize Git**:
    Initialize a new Git repository in this directory:
```bash
    git init
```
    *This creates a hidden `.git` folder that tracks your changes.*

### Step 2: The Basic Workflow (Edit, Add, Commit)

1.  **Create some files**:
    Create three text files with some content:
```bash
    echo "Content for file 1" > file1.txt
    echo "Content for file 2" > file2.txt
    echo "Content for file 3" > file3.txt
```

2.  **Check Status**:
    See how Git views these new files:
```bash
    git status
```
    *You should see the files listed as "Untracked files".*

3.  **Stage the files**:
    Add the files to the "Staging Area". This tells Git you want to include these updates in the next snapshot.
```bash
    git add file1.txt file2.txt file3.txt
```

4.  **Commit**:
    Save the snapshot with a descriptive message:
```bash
    git commit -m "Initial commit with three files"
```

### Step 3: Modifying Files and using `git diff`

1.  **Modify files**:
    Append new content to two of existing files:
```bash
    echo "Additional content for file 1" >> file1.txt
    echo "Additional content for file 2" >> file2.txt
```

2.  **Inspect Changes**:
    Before adding, it is good practice to review exactly what changed:
```bash
    git diff
```
    *This shows the line-by-line differences between your working directory and the last commit.*

3.  **Commit Step-by-Step**:
    Let's modify the staging area and commit.
```bash
    git add file1.txt file2.txt
    git commit -m "Updated file1 and file2"
```

### Step 4: Ignoring Files with `.gitignore`

Sometimes you have files you do NOT want to track (temporary files, partial builds, secrets).

1.  **Create "secret" files**:
    These mimic files that shouldn't be in Git.
```bash
    echo "Secret API Key" > .env
    echo "Debug logs..." > debug.log
```

2.  **Create `.gitignore`**:
    Create a special file named `.gitignore` and list the patterns to ignore:
```bash
    echo ".env" > .gitignore
    echo "*.log" >> .gitignore
```

3.  **Verify Status**:
    Check status again. You should see `.gitignore` as a new untracked file, but NOT `.env` or `debug.log`.
```bash
    git status
```

4.  **Final Commit**:
    Add the ignore file and any other pending changes.
```bash
    echo "More content" >> file3.txt
    git add .
    git commit -m "Final update with gitignore"
```

### Step 5: Review History

Look at the history of your project:
```bash
git log --oneline --graph --all
```

### Step 6: Renaming Branches

Git allows you to rename branches easily. This is commonly used to rename the default `master` branch to `main`.

1.  **Check current branch name**:
    First, see what branch you're on:
```bash
    git branch
```
    *The asterisk (*) indicates your current branch.*

2.  **Rename the current branch to `main`**:
    Use the `-m` (move) flag to rename:
```bash
    git branch -m main
```

3.  **Verify the rename**:
```bash
    git branch
```
    *You should now see `main` instead of `master`.*

4.  **Rename it back to `master`**:
    You can rename branches as many times as needed:
```bash
    git branch -m master
```

5.  **Rename a branch you're NOT on** (optional):
    If you want to rename a different branch, specify both names:
```bash
    git branch -m old-name new-name
```

> **Note**: If you're working with a remote repository (like GitHub), renaming the local branch doesn't automatically update the remote. You would need to push the new branch and delete the old one on the remote.

---

## Summary

In this lab, you learned:

- `git init` — Initialize a new repository
- `git status` — Check the state of your files
- `git add` — Stage changes for commit
- `git commit` — Save a snapshot of staged changes
- `git diff` — View differences between working directory and last commit
- `.gitignore` — Specify files/patterns to exclude from tracking
- `git log` — View commit history
- `git branch -m` — Rename branches

---