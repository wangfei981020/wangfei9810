# 使用 Alpine 版本的 Python 镜像，作为基础镜像
FROM python:3.9-alpine


# 设置时区为 UTC
RUN apk add --no-cache tzdata \
    #&& cp /usr/share/zoneinfo/UTC /etc/localtime \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    #&& echo "UTC" > /etc/timezone \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata  # 删除 tzdata 来减小镜像体积

# 设置工作目录
WORKDIR /app

# 复制本地文件到容器
COPY * /app/

# 安装 依赖
RUN apk add --no-cache \
    bash \
    curl \ 
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install tzdata \
    && apk del python3-dev gcc musl-dev linux-headers


# 设置容器的默认命令
CMD ["python", "app.py"]

# 暴露容器运行的端口（在 Flask 中设置为8080）
EXPOSE 8080