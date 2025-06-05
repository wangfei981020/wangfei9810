# config.yaml 存放namespace 、lark 告警机器人、loki URL
# metrics.py 获取日志，过滤日志，并告警lark
# app.py 每五分钟调用脚本一次

docker build -t code_monitor:v7 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v7