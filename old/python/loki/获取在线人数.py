import requests
import time
from datetime import datetime, timedelta

# Loki API 地址
loki_url = "http://ppu-loki.slleisure.com/loki/api/v1/query_range"

# 查询语句
query = '{namespace="g32-uat", container="message-client-backend"} |~ "JoinEvent 加入ws房间 事件 收到-client|LeaveEvent 事件"'

# 当前时间，减去 5 分钟
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=5)

# 转换为 Unix 时间戳
end_timestamp = int(end_time.timestamp() * 1000000000)  # 纳秒
start_timestamp = int(start_time.timestamp() * 1000000000)  # 纳秒

# 设置查询参数
params = {
    'query': query,
    'start': start_timestamp,
    'end': end_timestamp,
    'limit': 1000  # 可以根据需要修改最大返回日志条数
}

# 发送请求
response = requests.get(loki_url, params=params)

# 检查响应状态
if response.status_code == 200:
    data = response.json()
    # 输出查询结果
    if 'data' in data and 'result' in data['data']:
        logs = data['data']['result']
        if logs:
            for stream in logs:
                for entry in stream['values']:
                    timestamp = int(entry[0]) / 1000000000  # 转换为秒
                    log_message = entry[1]
                    print(f"{datetime.utcfromtimestamp(timestamp)}: {log_message}")
        else:
            print("No logs found within the specified time range.")
    else:
        print("Error: No valid log data found.")
else:
    print(f"Request failed with status code {response.status_code}")
