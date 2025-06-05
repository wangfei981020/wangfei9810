import requests
import time

# Loki 查询 URL
loki_url = 'http://loki.g32-prod.com/loki/api/v1/query_range'

# 获取当前时间戳和前一分钟的时间戳
end_timestamp = int(time.time())  # 当前时间戳（秒）
start_timestamp = end_timestamp - 300  # 前一分钟的时间戳（秒）

# 将时间戳转换为纳秒（Loki 使用纳秒级时间戳）
start_timestamp_ns = start_timestamp * int(1e9)
end_timestamp_ns = end_timestamp * int(1e9)

# 定义查询表达式
query = '{namespace="g32-game-center", pod=~".*"} |= "ERROR" |~ "code.*[0-9]+"'

# 设置请求参数
params = {
    'query': query,
    'start': start_timestamp_ns,  # 开始时间（纳秒）
    'end': end_timestamp_ns,  # 结束时间（纳秒）
    # 'step': '60',  # 查询间隔时间，单位为秒
}

# 发送 GET 请求到 Loki API
response = requests.get(loki_url, params=params)

# 检查请求是否成功
if response.status_code == 200:
    # 解析响应的 JSON 数据
    data = response.json()
    print(data)
    # 打印响应数据（日志内容）
    if 'data' in data and 'result' in data['data']:
        logs = data['data']['result']
        if logs:
            for stream in logs:
                print(f"Stream: {stream['stream']}")
                for value in stream['values']:
                    timestamp, log_line = value
                    print(f"Timestamp: {timestamp}, Log: {log_line}")
        else:
            print("没有找到日志数据")
    else:
        print("响应数据格式错误")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"错误内容: {response.text}")
