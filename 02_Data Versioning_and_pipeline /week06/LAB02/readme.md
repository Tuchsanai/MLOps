## DVC Lab: Upload and Download Images using GCS

### Objective
Set up a DVC (Data Version Control) workflow where:
- A **local computer** uploads an image folder to Google Cloud Storage (GCS).
- A **remote Ubuntu server** downloads the image folder from GCS using DVC.

---

### Prerequisites
- Python and DVC installed on both systems.
- GCS bucket created and access credentials (service account JSON file).
- Internet access for both systems.

---

## Local Computer Steps (Create New Repository on GitHub and Upload to GCS)


1. **Create a Remote Repository**:
   - Create a new repository on a platform like GitHub, GitLab, or Bitbucket.

2. **Add Remote and Push**:
   ```bash
   git branch -M main
   git remote add origin [REMOTE-URL]
   git push -u origin main
   ```

### 1. Create and Activate Python Environment

#### For Windows:
```bash
python -m venv dvc_env
.\dvc_env\Scripts\activate
pip install --upgrade pip
```

#### For macOS:
```bash
python3 -m venv dvc_env
source dvc_env/bin/activate
pip install --upgrade pip
```

### 2. Install DVC and GCS Plugin
```bash
pip install dvc dvc-gs
```

### 3. Initialize DVC Repository (ให้นักศึกษา copy รูปภาพใน floder ./LAB02/images มาใส่ไว้ใน  ./img ที่สร้างขึ้น)
```bash
git init
mkdir img
cd img
# Add 2-3 images to the img folder for testing
cd ..
dvc init
git add .
git commit -m "Initialize DVC and add img folder"
```
```bash
git init
mkdir img
cd img
# Add some images to the img folder
cd ..
dvc init
git add .
git commit -m "Initialize DVC and add img folder"
```

### 4. Set Up GCS as a DVC Remote
```bash
dvc remote add -d myremote gs://<your-bucket-name>
```

### 5. Configure GCS Credentials
Create a service account in GCP and download the JSON key file. Specify the credentials:
```bash
dvc remote modify myremote credentialpath /path/to/your/service_account.json
```

### 6. Track the Image Folder
```bash
dvc add img
```

### 7. Push Data to GCS
```bash
git add img.dvc .gitignore
git commit -m "Track img folder with DVC"
dvc push
```

---

## Remote Ubuntu Steps (Download from GCS)

### 1. Install DVC and GCS Plugin
```bash
sudo apt update
sudo apt install python3-pip
pip install dvc dvc-gs
```

### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 3. Set Up GCS Remote
Ensure the same GCS remote configuration is set:
```bash
dvc remote add -d myremote gs://<your-bucket-name>
dvc remote modify myremote credentialpath /path/to/your/service_account.json
```

### 4. Pull Data from GCS
```bash
dvc pull
```

---

### Verification
- Verify that the `img` folder is correctly downloaded on the remote server.
- Confirm that the GCS bucket contains the uploaded data.

---

### Clean-Up (Optional)
- To remove DVC-tracked data locally: `dvc remove img.dvc`
- To delete the bucket contents: `gsutil rm -r gs://<your-bucket-name>`

---

### Best Practices
- Always version your datasets with DVC.
- Use separate GCP credentials for different projects.
- Avoid hardcoding sensitive credentials directly in code or repositories.

