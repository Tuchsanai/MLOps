

```
docker build -f ./Dockerfile -t tuchsanai/mlops_2568_2:latest   .

```

```
docker pull tuchsanai/mlops_2568_2:latest
```

```
docker run -d --rm \
  -p 8888:8888 \
  tuchsanai/mlops_2568_2:latest
```