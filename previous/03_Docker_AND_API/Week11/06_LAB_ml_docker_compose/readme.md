
# Docker Compose  Iris Classification Lab

## What’s This About?

* **Backend:** FastAPI serving predictions on port 8087
* **Models:** Random Forest & Gradient Boosting
* **Data:** Iris dataset
* **Frontend:** Gradio UI on port 8085
* **Features:** Sliders for flower measurements, dual predictions
* **Setup:** Docker + Docker Compose for easy deployment

## How It Connects


## Project Layout

```bash
student-lab/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── interface.py
├── docker-compose.yml
└── README.md
```

#### docker-compose.yml

```bash
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8087:8087"
    container_name: iris-backend
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8085:8085"
    container_name: iris-frontend
    depends_on:
      - backend
    restart: unless-stopped
    links:
      - backend
```

## Get It Running

### Prerequisites

* Docker
* Docker Compose

### Steps

1.  **Grab the Code:**

    ```bash
    git clone git clone https://github.com/Tuchsanai/MLOps.git
    cd  MLOps/03_Docker_AND_API/Week11/06_LAB_ml_docker_compose/

2.  **Start Everything:**

    ```bash
    docker-compose up --build -d
    ```

## Check It Out

* Open `http://localhost:8085` in your browser.
* Play with the sliders, see the predictions.

## Shut It Down

```bash
docker-compose down
```
