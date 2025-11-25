
# 🐳 MLOps Docker Environment Setup

This repository provides a ready-to-use **Docker container for MLOps learning and experimentation**.
It includes essential tools such as **Python 3, JupyterLab, scikit-learn, pandas, and OpenCV**, pre-configured for seamless execution across both **Linux** and **Windows** environments.

---

## 🔧 Build Docker Image

Use the following command to **build the Docker image** from the provided `Dockerfile`:

```bash
docker build -f ./Dockerfile -t tuchsanai/mlops_2568_2:latest .
```

This command:

* Builds the image from the current directory (`.`)
* Tags it as `tuchsanai/mlops_2568_2:latest`
* Uses the `Dockerfile` in the root folder

---

## 🚀 Push Image to Docker Hub

Once the image is built, push it to your Docker Hub repository:

```bash
docker push tuchsanai/mlops_2568_2:latest
```

This ensures your image can be pulled and used on any machine without rebuilding it locally.

---

## 🖥️ Run the Container


```bash
docker run -d -p 8081:8888 --name mlops-container tuchsanai/mlops_2568_2:latest
```

* `-d`: Run in detached mode (background)
* `-p 8081:8888`: Map container port 8888 to local port 8081
* `--name mlops-container`: Assigns a custom container name
* Launches **JupyterLab** accessible via [http://localhost:8888](http://localhost:8888)


## 📚 Access JupyterLab

Once the container is running, open your browser and visit:

👉 **[http://localhost:8081](http://localhost:8081)**
Use the token or password defined in the image configuration (e.g., `mlops`).

---

## 🧩 Notes

* You can stop the container anytime with:

  ```bash
  docker stop mlops-container
  ```
* Restart it again later with:

  ```bash
  docker start mlops-container
  ```

---

### 🧠 Summary

| Action                 | Command                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------- |
| **Build image**        | `docker build -f ./Dockerfile -t tuchsanai/mlops_2568_2:latest .`                       |
| **Push to Docker Hub** | `docker push tuchsanai/mlops_2568_2:latest`                                             |
| **Run (Linux)**        | `docker run -d -p 8888:8888 --name mlops-container tuchsanai/mlops_2568_2:latest`       |
| **Run (Windows)**      | `docker run -d ^ -p 8888:8888 ^ --name mlops-container ^ tuchsanai/mlops_2568_2:latest` |
| **Access JupyterLab**  | [http://localhost:8888](http://localhost:8888)                                          |

---

Would you like me to **add a “Dockerfile Overview” section** describing what’s inside (like dependencies and environment setup)? It would make the README more educational for students.
