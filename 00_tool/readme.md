

```
docker build -f ./Dockerfile -t tuchsanai/mlops_2568_2:latest   .

```

```
docker push tuchsanai/mlops_2568_2:latest
```


```
docker run -d \
  -p 8888:8888 \
  --name mlops-container \
  tuchsanai/mlops_2568_2:latest
```