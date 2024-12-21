https://www.youtube.com/watch?v=e3GuonR1r-0&t=1231s




# DVC Lab: Managing Image Dataset with Python Environment

## Lab Objectives

1. Install and configure **DVC** in a Python project.
2. Set up a local Git repository for version control.
3. Track an image dataset using **DVC**.
4. Demonstrate basic DVC commands for data versioning.

---

## Prerequisites

- Python installed on your system.
- Git installed on your system.
- A GitHub account (optional, for remote repository).

---

## Step 1: Install Dependencies

### Install Git

Ensure Git is installed. Use the following commands based on your OS:

**Ubuntu/Debian**:

```bash
sudo apt update && sudo apt install git -y
```

**Windows**: Download and install Git from [git-scm.com](https://git-scm.com/).

**macOS**:

```bash
brew install git
```

### Install Python and Virtual Environment

**Ubuntu/Debian**:

```bash
sudo apt install python3 python3-venv -y
```

**Windows/macOS**: Download and install Python from [python.org](https://www.python.org/).

---

## Step 2: Create a Project Directory and Initialize Git

1. Create a new project directory:

   ```bash
   mkdir dvc-image-lab && cd dvc-image-lab
   ```

2. Initialize a Git repository:

   ```bash
   git init
   ```

3. Create a `.gitignore` file to exclude unnecessary files:

   ```bash
   echo "venv/\n*.dvc\n*.DS_Store\n__pycache__/" > .gitignore
   ```

---

## Step 3: Set Up Python Environment

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Windows: .\venv\Scripts\activate
   ```

2. Install required Python packages:

   ```bash
   pip install dvc[all] numpy opencv-python
   ```

3. Save dependencies to `requirements.txt`:

   ```bash
   pip freeze > requirements.txt
   ```

---

## Step 4: Initialize DVC

1. Initialize DVC in the project:

   ```bash
   dvc init
   ```

2. Add and commit the DVC configuration files:

   ```bash
   git add .
   git commit -m "Initialize Git and DVC"
   ```

---

## Step 5: Add an Image Dataset

1. Create a directory for your dataset:

   ```bash
   mkdir data
   ```

2. Add images to the `data` directory (or download a dataset). For example, you can use [Kaggle](https://www.kaggle.com/) datasets.

3. Track the dataset using DVC:

   ```bash
   dvc add data
   ```

4. Add the `.dvc` file to Git:

   ```bash
   git add data.dvc .gitignore
   git commit -m "Track image dataset with DVC"
   ```

---

## Step 6: Set Up Remote Storage (Optional)

1. Add a remote storage location (e.g., Google Drive, AWS S3, etc.):

   ```bash
   dvc remote add -d myremote s3://mybucket/path
   ```

2. Push the dataset to remote storage:

   ```bash
   dvc push
   ```

3. Commit the remote configuration:

   ```bash
   git add .dvc/config
   git commit -m "Configure DVC remote storage"
   ```

---

## Step 7: Basic DVC Commands

### Check Dataset Status

```bash
dvc status
```

### Pull Dataset from Remote

```bash
dvc pull
```

### Remove Dataset from Workspace

```bash
dvc remove data.dvc
```

### Retrieve Dataset Again

```bash
dvc checkout
```

---

## Step 8: Example Python Script

Create a Python script `process_images.py` to process the dataset:

```python
import os
import cv2

data_dir = "data"
output_dir = "processed"
os.makedirs(output_dir, exist_ok=True)

for img_name in os.listdir(data_dir):
    img_path = os.path.join(data_dir, img_name)
    img = cv2.imread(img_path)

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Save processed image
    output_path = os.path.join(output_dir, img_name)
    cv2.imwrite(output_path, gray_img)

print("Image processing complete.")
```

Run the script:

```bash
python process_images.py
```

Track the processed images with DVC:

```bash
dvc add processed
```

Commit changes:

```bash
git add processed.dvc .gitignore

git commit -m "Add processed images"
```

Push changes to remote storage:

```bash
dvc push
```

---

## Lab Wrap-Up

You have now learned how to:

- Set up a Python environment for DVC.
- Track and version an image dataset.
- Push and pull data with remote storage.
- Integrate dataset management into a Python workflow.

---

## Additional Exercises

1. Use a different remote storage provider and update the remote configuration.
2. Implement a Python script to augment the dataset and track it with DVC.
3. Collaborate with a team by sharing your Git repository and remote storage.

---

Happy versioning with DVC!

