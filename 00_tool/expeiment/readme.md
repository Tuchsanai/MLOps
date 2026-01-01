

```
docker run -d -p 8888:8888  -p 8080:8080 --name mlflow-container tuchsanai/mlops_mlflow_2568_2:latest 
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
*.pdf
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
