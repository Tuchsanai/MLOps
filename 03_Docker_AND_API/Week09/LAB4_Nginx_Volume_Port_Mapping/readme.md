


| ![gpc](./gpc.jpg) | ![web](./web.jpg) |
|:---:|:---:|




## create directory

   
    mkdir LAB4_Nginx_Volume_Port_Mapping
    cd    LAB4_Nginx_Volume_Port_Mapping


## git clone branch dev
    
    
   
    git clone  https://github.com/Tuchsanai/MLOps.git

   
    cd MLOps/03_Docker_AND_API/Week09/LAB4_Nginx_Volume_Port_Mapping




## 2 Run Nginx with port mapping and volume mapping

```

docker run -d -p 8083:80 -v ${PWD}/web_demo:/usr/share/nginx/html:ro  nginx

```






