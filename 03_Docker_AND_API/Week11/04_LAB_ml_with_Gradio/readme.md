
# Student Lab - Iris Classification with Machine Learning

This project is a containerized Machine Learning lab designed for students. It features a Gradio frontend for user interaction and a FastAPI backend implementing RandomForestClassifier and GradientBoostingClassifier models using the Iris dataset.

## Project Overview

- **Backend**: FastAPI serving ML predictions
    - Port: 8087
    - Models: RandomForestClassifier, GradientBoostingClassifier
    - Dataset: Iris flower dataset

- **Frontend**: Gradio interface for input and visualization
    - Port: 8085
    - Features: Sliders for measurements, dual model predictions

- **Containerization**: Docker with separate images for frontend and backend

## Project Structure

```
student-lab/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── interface.py
└── README.md
```

## Prerequisites

-   Docker installed on your system
-   Git (for cloning the repository)

## Setup and Running Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd student-lab
```

### 2. Build the Docker Images

Build the backend image:

```bash
cd backend
docker build -t iris-backend .
cd ..
```

Build the frontend image:

```bash
cd frontend
docker build -t iris-frontend .
cd ..
```

### 3. Run the Containers

Run the backend container:

```bash
docker run -d --name backend -p 8087:8087 iris-backend
```

Run the frontend container (linked to backend):

```bash
docker run -d --name frontend -p 8085:8085 --link backend iris-frontend
```

### 4. Access the Application

-   Open your web browser
-   Navigate to: `http://localhost:8085`
-   Use the sliders to input flower measurements
-   View predictions from both models

## Usage

On the Gradio interface:

-   Adjust sliders for:
    -   Sepal Length (4.0-8.0)
    -   Sepal Width (2.0-4.5)
    -   Petal Length (1.0-7.0)
    -   Petal Width (0.1-2.5)
-   View instant predictions for Iris species from both classifiers

The output shows:

-   Random Forest prediction
-   Gradient Boosting prediction

## Features

**Frontend:**

-   Intuitive slider inputs
-   Clear display of predictions from both models
-   Responsive design

**Backend:**

-   RESTful API with prediction endpoint
-   Health check endpoint
-   Pre-trained ML models

**Docker:**

-   Isolated environments
-   Easy deployment
-   Consistent execution across systems

## Troubleshooting

If the interface doesn't load:

-   Check if both containers are running: `docker ps`
-   Verify port mapping: 8085 (frontend), 8087 (backend)
-   Ensure containers can communicate (`--link backend`)
-   Restart containers if needed:

```bash
docker stop frontend backend
docker rm frontend backend
```

Then rerun the `docker run` commands.

## Learning Objectives

-   Understand Random Forest and Gradient Boosting algorithms
-   Explore containerization with Docker
-   Interact with ML models through a web interface
-   Experience API-driven application architecture

## Contributing

Feel free to fork this repository and submit pull requests with improvements!

This README provides:

-   Clear setup instructions
-   Project overview and structure
-   Usage guidelines
-   Troubleshooting tips
-   Educational context

Students can easily follow these steps to get the lab running on their systems and start experimenting with the ML models through the Gradio interface.
```
