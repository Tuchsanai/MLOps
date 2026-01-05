


```

# Step 1: Run container
docker run -d -p 5000:5000 -p 8888:8888 --name mlops-container -v "C:\Users\oishi\Documents\GitHub\MLOps\02_MLFLOW\01_basic\02_MLflow_Tracking\LAB:/home/student/workspace" tuchsanai/mlops_2568_2:latest

# Step 2: Create directories
docker exec mlops-container mkdir -p /home/student/workspace/mlflowserver-lab/mlruns_db
docker exec mlops-container mkdir -p /home/student/workspace/mlflowserver-lab/mlartifacts

# Step 3: Start MLflow server
docker exec -d mlops-container mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:////home/student/workspace/mlflowserver-lab/mlruns_db/mlflow.db --artifacts-destination /home/student/workspace/mlflowserver-lab/mlartifacts --serve-artifacts

```


# Linux Delete existing dev branch (local and remote)

```

git branch -D dev 2>/dev/null
git push origin --delete dev 2>/dev/null

# Create dev from main
git checkout main
git pull origin main
git checkout -b dev

# Add PDF and image patterns to .gitignore (which already exists from main)
cat >> .gitignore << 'EOF'

# Dev branch exclusions
*.svg
*.pdf
*.md
*.png
*.jpg
*.jpeg
*.gif
*.bmp
*.tiff
*.webp
EOF

# Remove any tracked PDFs/images from git (keeps files locally)
git rm -r --cached . 2>/dev/null
git add .

# Commit and push
git commit -m "Create dev branch with PDF and image exclusions"
git push -u origin dev

# Return to main branch
git checkout main

```


# Windows PowerShell Delete existing dev branch (local and remote)

```
# Delete existing dev branch (local and remote)
git branch -D dev 2>$null
git push origin --delete dev 2>$null

# Create dev from main
git checkout main
git pull origin main
git checkout -b dev

# Add PDF and image patterns to .gitignore
@"

# Dev branch exclusions
*.svg
*.md
*.pdf
*.png
*.jpg
*.jpeg
*.gif
*.bmp
*.tiff
*.webp
"@ | Add-Content .gitignore

# Remove any tracked PDFs/images from git (keeps files locally)
git rm -r --cached . 2>$null
git add .

# Commit and push
git commit -m "Create dev branch with PDF and image exclusions"
git push -u origin dev

# Return to main branch
git checkout main

```
