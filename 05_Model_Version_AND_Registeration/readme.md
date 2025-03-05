
# Start PostgreSQL:



```
docker run -d \
  --name postgres-mlflow \
  -e POSTGRES_USER=mlflow \
  -e POSTGRES_PASSWORD=mlflow \
  -e POSTGRES_DB=mlflow_db \
  -p 5432:5432 \
  postgres:latest

```


# Run MLflow with PostgreSQL:

```
docker run -p 5000:5000 \
  --link postgres-mlflow \
  ghcr.io/mlflow/mlflow:latest \
  mlflow server \
    --backend-store-uri postgresql://mlflow:mlflow@postgres-mlflow:5432/mlflow_db \
    --default-artifact-root file:///mlflow/artifacts \
    --host 0.0.0.0
```


## Explanation:
--link postgres-mlflow: Links the MLflow container to the PostgreSQL container (though --network is preferred in modern Docker setups).

--backend-store-uri: Specifies the PostgreSQL connection string.

--default-artifact-root: Uses a file-based artifact store inside the container (you can also mount a volume or use cloud storage like S3)

