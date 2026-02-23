from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

app = FastAPI()

# Load and train models at startup
iris = load_iris()
X, y = iris.data, iris.target

# Train RandomForestClassifier
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)

# Train GradientBoostingClassifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_model.fit(X, y)

# Input data model
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: IrisInput):
    # Convert input to array
    input_data = np.array([[data.sepal_length, data.sepal_width, 
                           data.petal_length, data.petal_width]])
    
    # Get predictions
    rf_pred = rf_model.predict(input_data)[0]
    gb_pred = gb_model.predict(input_data)[0]
    
    # Map predictions to Iris species
    species = {0: "setosa", 1: "versicolor", 2: "virginica"}
    
    return {
        "random_forest": species[rf_pred],
        "gradient_boosting": species[gb_pred]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8087)
