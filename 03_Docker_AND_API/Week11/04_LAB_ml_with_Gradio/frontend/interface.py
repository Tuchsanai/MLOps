import gradio as gr
import requests

# Backend URL (adjusted for Docker linking)
BACKEND_URL = "http://backend:8087/predict"

def predict_iris(sepal_length, sepal_width, petal_length, petal_width):
   # Prepare data for API call
   data = {
       "sepal_length": sepal_length,
       "sepal_width": sepal_width,
       "petal_length": petal_length,
       "petal_width": petal_width
   }
   
 
   # Make request to backend
   try:
       response = requests.post(BACKEND_URL, json=data)
       response.raise_for_status()
       predictions = response.json()
       return (
           f"Random Forest: {predictions['random_forest']}",
           f"Gradient Boosting: {predictions['gradient_boosting']}"
       )
   except Exception as e:
       return f"Error: {str(e)}", f"Error: {str(e)}"

# Gradio interface
interface = gr.Interface(
   fn=predict_iris,
   inputs=[
       gr.Slider(4.0, 8.0, step=0.1, label="Sepal Length (cm)"),
       gr.Slider(2.0, 4.5, step=0.1, label="Sepal Width (cm)"),
       gr.Slider(1.0, 7.0, step=0.1, label="Petal Length (cm)"),
       gr.Slider(0.1, 2.5, step=0.1, label="Petal Width (cm)")
   ],
   outputs=[
       gr.Textbox(label="Random Forest Prediction"),
       gr.Textbox(label="Gradient Boosting Prediction")
   ],
   title="Iris Species Classifier",
   description="Adjust the sliders to input flower measurements and see predictions from two ML models."
)

if __name__ == "__main__":
   interface.launch(server_name="0.0.0.0", server_port=8085)-