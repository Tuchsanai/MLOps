
# Here’s a simple command to run MLflow with its tracking server:


## create directory

```
mkdir -p MLflow  # -p flag ensures no error if directory already exists
cd MLflow
```

# Run MLflow UI with Docker

```
docker run -d \
  -p 5000:5000 \
  -v "$(pwd):/mlflow" \
  ghcr.io/mlflow/mlflow:latest \
  mlflow ui \
  --backend-store-uri file:///mlflow \
  --host 0.0.0.0
```

## Verify It Works:

After running, check 

```
http://ip_address:5000 
```

in your browser.You should see the MLflow UI where you can log experiments.




## Delete all containers

```
docker stop $(docker ps -a -q) 2>/dev/null || true
docker rm $(docker ps -a -q) 2>/dev/null || true

docker rmi $(docker images -q) 2>/dev/null || true

docker volume rm $(docker volume ls -q) 2>/dev/null || true
docker network prune -f 2>/dev/null || true

```