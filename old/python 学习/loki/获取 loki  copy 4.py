from flask import Flask, Response
import requests
import json
import time
import re
import yaml
from collections import defaultdict
from collections import Counter
# from collections import counter

# 配置 Loki 服务器地址和查询参数
# loki_url = "http://loki.g32-prod.com/loki/api/v1/query"
loki_url = "http://loki.g32-prod.com/loki/api/v1/query_range"
# loki_url = "http://loki.g32-prod.com/loki/api/api/ds/query?ds_type=loki&requestId=explore_sn7_1"

# 获取当前时间戳和前一分钟的时间戳
end_timestamp = int(time.time())  # 当前时间戳（秒）
start_timestamp = end_timestamp - 3000  # 前一分钟的时间戳（秒）

# 将时间戳转换为纳秒（Loki 使用纳秒级时间戳）
start_timestamp_ns = start_timestamp * int(1e9)
end_timestamp_ns = end_timestamp * int(1e9)

# 构造请求参数
def read_config():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        return config

def get_logs():
    # 请求 Loki 数据
    count_dict = defaultdict(int)  # 用于统计 transaction stats
    config = read_config()

    for n in config['namespace']:
        query = f'{{namespace="{n}", pod=~".*"}} |= "ERROR" |~ "code.*[0-9]+"'
        # query = '{namespace="g32-game-center", pod=~".*"} |= "ERROR" |~ "code\":\"(\\d+)\",\"msg\":\"([^\"]+)\"'

        # 构造查询参数
        params = {
            'query': query,
            'start': start_timestamp_ns,  # 开始时间（纳秒）
            'end': end_timestamp_ns,  # 结束时间（纳秒）
            # 'step': '60',  # 查询间隔时间，单位为秒
        }
        # 发送请求
        response = requests.get(loki_url, params=params)
        # print(response)

        if response.status_code == 200:
            data = response.json()
            # print(data)
            if 'data' in data and 'result' in data['data']:
                logs = data['data']['result']
                # print(logs)
                for log_stream in logs:
                    # 提取容器和命名空间信息
                    stream = log_stream['stream']
                    container = stream['container']
                    namespace = stream['namespace']

                    # 遍历日志内容中的每一条记录
                    for entry in log_stream['values']:
                        # 正则匹配 "code" 和 "msg"
                        code_msg_pattern = r'"code":"(\d+)","msg":"([^"]+)"'
                        code_msg_matches = re.findall(code_msg_pattern, entry[1])

                        # 更新计数器
                        counter = Counter(code_msg_matches)

                        for match in code_msg_matches:
                            code, msg = match
                            count_dict[(namespace, container, code, msg)] += 1
                            # count_dict[match] += 1
        else:
            return Response(
                json.dumps({"error": "请求失败", "status_code": response.status_code}),
                status=response.status_code,
                mimetype='application/json'
            )
    # 打印最终统计结果
    # print("Final Statistics:")
    return count_dict
    # print(count_dict)
    # for (code, msg), num in count_dict.items():
    #     print(f'{{"namespace": "{namespace}", "container": "{container}", "code": "{code}", "msg": "{msg}", "num": {num}}}')

def convert_to_prometheus_format(count_dict):
    
    prometheus_lines = []

    # 遍历 defaultdict 数据
    for (namespace, container, code, msg), count in count_dict.items():
        # 格式化为 Prometheus 指标格式
        prometheus_line = f'log_error_count{{namespace="{namespace}", container="{container}", code="{code}", msg="{msg}"}} {count}'
        print(prometheus_line)
        # prometheus_lines.append(prometheus_line)
    # print(prometheus_lines)
    # return prometheus_lines
def main():
    data_list = get_logs()
    convert_to_prometheus_format(data_list)
main()
# 执行日志查询

