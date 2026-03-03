
# Build and run the container as before:

## create directory

   
    mkdir LAB4_Week10_Frontend
    cd    LAB4_Week10_Frontend
    

## git clone branch dev
    
    
   ```
    git clone https://github.com/Tuchsanai/MLOps.git
   ```
   
   ```   
    cd MLOps/03_Docker_AND_API/Week10/Lab4/frontend
   ```


1. **Build the Docker Image**:
   ```bash
   docker build -t streamlit-app_lab5  .
   ```

2. **Run the Docker Container**:
   ```bash
   docker run -d --rm -p 8089:8501 -v  ./:/app -e BACKEND_URL=34.142.254.39  streamlit-app_lab5 
   ```


![Demo](./output.jpg)
![Demo](./server.jpg)

