I'll help you create a Docker setup for a student lab with a Gradio frontend and FastAPI backend, using RandomForestClassifier and GradientBoostingClassifier with the Iris dataset. Here's a complete solution with separate Dockerfiles for frontend and backend:
Project Structure
student-lab/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── interface.py
└── README.md
Backend Implementation
backend/Dockerfile
dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8087

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8087"]
backend/requirements.txt
fastapi
uvicorn
scikit-learn
numpy
backend/app.py
python
from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import numpy as np

app = FastAPI()

# Load and prepare data
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train models
rf_model = RandomForestClassifier(random_state=42)
gb_model = GradientBoostingClassifier(random_state=42)
rf_model.fit(X_train, y_train)
gb_model.fit(X_train, y_train)

@app.get("/predict")
async def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    
    rf_pred = rf_model.predict(input_data)[0]
    gb_pred = gb_model.predict(input_data)[0]
    
    return {
        "random_forest": {
            "prediction": int(rf_pred),
            "class": iris.target_names[rf_pred]
        },
        "gradient_boosting": {
            "prediction": int(gb_pred),
            "class": iris.target_names[gb_pred]
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
Frontend Implementation
frontend/Dockerfile
dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY interface.py .

EXPOSE 8085

CMD ["python", "interface.py"]
frontend/requirements.txt
gradio
requests
frontend/interface.py
python
import gradio as gr
import requests

def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
    try:
        # Call backend API
        response = requests.get(
            "http://backend:8087/predict",
            params={
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            }
        )
        response.raise_for_status()
        predictions = response.json()
        
        return (
            f"Random Forest Prediction: {predictions['random_forest']['class']}",
            f"Gradient Boosting Prediction: {predictions['gradient_boosting']['class']}"
        )
    except Exception as e:
        return f"Error: {str(e)}", f"Error: {str(e)}"

# Create Gradio interface
interface = gr.Interface(
    fn=predict_iris,
    inputs=[
        gr.Slider(4.0, 8.0, step=0.1, label="Sepal Length"),
        gr.Slider(2.0, 4.5, step=0.1, label="Sepal Width"),
        gr.Slider(1.0, 7.0, step=0.1, label="Petal Length"),
        gr.Slider(0.1, 2.5, step=0.1, label="Petal Width")
    ],
    outputs=[
        gr.Textbox(label="Random Forest Result"),
        gr.Textbox(label="Gradient Boosting Result")
    ],
    title="Iris Flower Classification",
    description="Enter flower measurements to predict species using Random Forest and Gradient Boosting"
)

interface.launch(server_name="0.0.0.0", server_port=8085)
README.md
markdown
# Student Lab - Iris Classification

## Prerequisites
- Docker installed on your system

## Build and Run Instructions

1. Build the backend:
```bash
cd backend
docker build -t iris-backend .
Build the frontend:
bash
cd ../frontend
docker build -t iris-frontend .
Run the backend:
bash
docker run -d --name backend -p 8087:8087 iris-backend
Run the frontend:
bash
docker run -d --name frontend -p 8085:8085 --link backend iris-frontend
Access the application:
Open your browser at http://localhost:8085
Notes
Backend runs on port 8087
Frontend runs on port 8085
The application uses the Iris dataset with RandomForest and GradientBoosting classifiers
Input values correspond to sepal length, sepal width, petal length, and petal width

### How to Use
1. Create the directory structure and files as shown above
2. Place all files in a GitHub repository
3. Students can:
   - Clone the repository
   - Build the Docker images using the provided commands
   - Run the containers
   - Access the Gradio interface at http://localhost:8085
   - Input flower measurements using sliders
   - View predictions from both classifiers

### Design Features
- **Frontend**: Clean Gradio interface with:
  - Sliders for intuitive input
  - Separate output boxes for each classifier
  - Descriptive title and instructions
- **Backend**: FastAPI with:
  - Simple prediction endpoint
  - Health check endpoint
  - Returns both class number and name
- **Docker**: 
  - Lightweight Python 3.9-slim base image
  - Separate containers for frontend and backend
  - Exposed ports as specified (8085 frontend, 8087 backend)

This setup provides a complete, containerized ML lab environment that students can easily run and experiment with.