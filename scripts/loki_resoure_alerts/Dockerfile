# 使用官方 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 复制当前目录内容到容器中的 /app 目录
COPY ./app.py /app/app.py
COPY ./data_checker.py /app/data_checker.py
COPY ./get_nacos_config.py /app/get_nacos_config.py
COPY ./lark_alert.py /app/lark_alert.py
COPY ./metrics.py /app/metrics.py
COPY ./requirements.txt /app/requirements.txt

# 安装 requirements.txt 中列出的所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置默认命令来运行 app.py
CMD ["python3", "app.py"]