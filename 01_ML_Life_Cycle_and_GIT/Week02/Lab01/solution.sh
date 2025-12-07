#!/bin/bash

# Solution script for Lab 01

# Clean up any previous runs
./clean.sh

echo "======================================================="
echo "Step 1: Initial Setup and First Commit"
echo "======================================================="

echo "1. Creating directory and initializing git..."
mkdir git-lab
cd git-lab
git init

echo "2. Creating initial files..."
echo "Content for file 1" > file1.txt
echo "Content for file 2" > file2.txt
echo "Content for file 3" > file3.txt

echo "3. Checking status..."
git status

echo "4. Adding files and committing..."
git add file1.txt file2.txt file3.txt
git commit -m "Initial commit with three files"

echo "======================================================="
echo "Step 2: Modify Files and Second Commit"
echo "======================================================="

echo "1. Modifying files..."
echo "Additional content for file 1" >> file1.txt
echo "Additional content for file 2" >> file2.txt

echo "2. Checking diff..."
git diff

echo "3. Committing changes..."
git add file1.txt file2.txt
git commit -m "Updated file1 and file2"

echo "======================================================="
echo "Step 3: .gitignore and Final Commit"
echo "======================================================="

echo "1. Creating a file to ignore..."
echo "Secret stuff" > secret.log
echo "Secret stuff 2" > .env

echo "2. Ignoring the file..."
echo "*.log" > .gitignore
echo ".env" >> .gitignore

echo "3. Modifying file3..."
echo "Additional content for file 3" >> file3.txt

echo "4. Checking status (notice ignored files are not listed)..."
git status

echo "5. Committing final changes..."
git add .
git commit -m "Final update including gitignore"

echo "======================================================="
echo "Lab completed successfully!"
echo "Here is the log:"
git log --oneline --graph --all
