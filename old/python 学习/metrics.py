# metrics.py
import requests
import re
import time
import yaml
from collections import defaultdict

# 获取当前时间戳和前五分钟的时间戳（300秒）
#end_timestamp = int(time.time())  # 当前时间戳（秒）
#start_timestamp = end_timestamp - 300  # 前五分钟的时间戳（秒）

# 将时间戳转换为纳秒（Loki 使用纳秒级时间戳）
#start_timestamp_ns = start_timestamp * int(1e9)
#end_timestamp_ns = end_timestamp * int(1e9)

def get_dynamic_time_range():
    end_timestamp = int(time.time())  # 当前时间戳（秒）
    start_timestamp = end_timestamp - 300  # 前五分钟的时间戳（秒）

    start_timestamp_ns = start_timestamp * int(1e9)
    end_timestamp_ns = end_timestamp * int(1e9)

    return start_timestamp_ns, end_timestamp_ns

# 读取配置文件
def read_config():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config

# 从 Loki 获取日志数据并返回计数结果
def get_logs():
    count_dict = defaultdict(int)  # 用于统计 transaction stats
    config = read_config()
    loki_url = config['loki_url']
    start_timestamp_ns, end_timestamp_ns = get_dynamic_time_range()
    for n in config['namespace']:
        query = f'{{namespace="{n}", pod=~".*"}} |= "ERROR" |~ "code.*[0-9]+"'

        # 构造查询参数
        params = {
            'query': query,
            'start': start_timestamp_ns,  # 开始时间（纳秒）
            'end': end_timestamp_ns,  # 结束时间（纳秒）
        }

        # 发送请求到 Loki
        response = requests.get(loki_url, params=params)

        if response.status_code == 200:
            data = response.json()

            if 'data' in data and 'result' in data['data']:
                logs = data['data']['result']

                for log_stream in logs:
                    stream = log_stream['stream']
                    container = stream['container']
                    namespace = stream['namespace']

                    # 遍历日志内容中的每一条记录
                    for entry in log_stream['values']:
                        # 正则匹配 "code" 和 "msg"
                        code_msg_pattern = r'"code":"(\d+)","msg":"([^"]+)"'
                        code_msg_matches = re.findall(code_msg_pattern, entry[1])

                        # 更新计数器
                        for match in code_msg_matches:
                            code, msg = match
                            count_dict[(namespace, container, code, msg)] += 1
        else:
            return {"error": "请求失败", "status_code": response.status_code}

    return count_dict

# 转换为 Prometheus 格式
def convert_to_prometheus_format(count_dict):
    prometheus_lines = []
    for (namespace, container, code, msg), count in count_dict.items():
        prometheus_line = f'log_error_count{{namespace="{namespace}", container="{container}", code="{code}", msg="{msg}"}} {count}'
        prometheus_lines.append(prometheus_line)
    return "\n".join(prometheus_lines)