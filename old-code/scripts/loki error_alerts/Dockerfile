FROM python:3.9-slim-buster

# 设置时区为马尼拉时间 (菲律宾标准时间 UTC+8)
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Manila /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 工作目录
WORKDIR /usr/local/app

# 复制当前目录内容到容器
COPY . .

# 安装依赖
RUN apt update
RUN pip3 install -r requirements.txt && \
    groupadd appgroup && useradd app -G appgroup && \
    chown -R app:appgroup /usr/local/app 

# 暴露端口
EXPOSE 9108

# 切换为应用用户
USER app

# 启动 Gunicorn
#CMD ["/usr/local/bin/python","app.py"]

CMD ["/usr/local/bin/gunicorn","-c","config.py","app:app"]