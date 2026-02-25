# LAB 2: Nginx Port Mapping with Docker

## Overview

In this lab, you will learn how to run an **Nginx web server** inside a Docker container and expose it to the outside world using **port mapping**. Port mapping allows traffic from the host machine (or a cloud VM) to be forwarded into the container, making the web server accessible via a browser.

By the end of this lab, you will be able to:
- Pull and run the official Nginx Docker image
- Map a host port to a container port using the `-p` flag
- Verify that Nginx is accessible through a browser using the VM's external IP

---

## Prerequisites

- Docker is installed and running (see LAB 1)
- You are connected to a VM instance (e.g., Google Cloud Compute Engine)

---

## Step 1: Create the Lab Directory

Create a dedicated directory for this lab and navigate into it.

```bash
mkdir LAB3_Nginx_Port_mapping
cd LAB3_Nginx_Port_mapping
```

---

## Step 2: Clone the Repository

Clone the MLOps repository to get all lab materials.

```bash
git clone https://github.com/Tuchsanai/MLOps.git
```

Then navigate to the LAB3 folder:

```bash
cd MLOps/04_Docker_AND_API/01_Docker/LAB2_Nginx_Port_mapping
```

---

## Step 3: Run Nginx with Port Mapping

Use the `docker run` command with the `-p` flag to map **port 8080** on the host to **port 80** inside the container (Nginx's default port).

```bash
docker run -p 8080:80 nginx
```

**Flag explanation:**
- `-p 8080:80` — Maps host port `8080` → container port `80`
- `nginx` — Uses the official Nginx image from Docker Hub

> Docker will automatically pull the Nginx image from Docker Hub if it is not already available locally.

---

## Step 4: Verify in the Browser

Once the container is running, open a browser and navigate to your VM's **External IP** on port **8080**:

```
http://<YOUR_EXTERNAL_IP>:8080
```

You should see the **"Welcome to nginx!"** page, confirming that the container is running and port mapping is working correctly.

![Demo](./portmap_demo1.jpg)

> **Note:** In the example above, the VM's External IP is `34.142.254.39`, so the URL is `http://34.142.254.39:8080`. Replace this with your own VM's External IP address.

---



## Stopping the Container


Then stop it later with:

```bash
docker ps               # Find the container ID
docker stop <container_id>
```
