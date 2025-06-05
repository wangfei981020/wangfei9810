import requests
import json
import time
import re
from collections import defaultdict

# 配置 Loki 服务器地址和查询参数
loki_url = "http://loki.g32-prod.com/loki/api/v1/query"

# 查询条件：例如查询某一时间范围内的日志
query = '{namespace=~"g32-admin", pod=~".*"} |= "ERROR" |~ "code.*[0-9]+"'

# 设置查询时间范围：过去5分钟
end_time = int(time.time())  # 当前时间
start_time = end_time - 3600  # 5分钟前的时间戳

# 格式化时间为 Loki API 所需的 RFC3339 格式
start_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_time))
end_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(end_time))

# 构造请求参数
params = {
    'query': query,
    'limit': 1000,  # 最大返回结果数
    'start': start_time,
    'end': end_time
}

# 发送 GET 请求到 Loki API
response = requests.get(loki_url, params=params)
data_list = {}
# 使用 defaultdict 来方便处理重复的 key
# result = defaultdict(lambda: defaultdict(lambda: {"num": 0}))
count_dict = defaultdict(int)
# 检查响应状态码
if response.status_code == 200:
    data = response.json()
    # print(data)
    if 'data' in data and 'result' in data['data']:
        logs = data['data']['result']
        # print(logs)
        # for l in logs:
        #     print(l.keys())
        for log_stream in logs:
            stream = log_stream['stream']
            # print(f"Stream: {log_stream['stream']}")
            # print(f"Stream: {log_stream['stream']}")
            container = stream['container']
            namespace = stream['namespace']
            data_list['container'] = container
            data_list['namespace'] = namespace

            for entry in log_stream['values']:
                code_msg_pattern = r'"code":"(\d+)","msg":"([^"]+)"'
                code_msg_matches = re.findall(code_msg_pattern, entry[1])
                for match in code_msg_matches:
                    code, msg = match
                    count_dict[(code, msg)] += 1
                    # print(f"{{Code: {code}, Msg: {msg}}}")
                # 将统计信息加入到现有字典中
                data_list['transaction_stats'] = []

                # 添加统计结果到字典
                for (code, msg), count in count_dict.items():
                    data_list['transaction_stats'].append({
                        'Code': code,
                        'Msg': msg,
                        'Num': count
                    })

else:
    print(f"请求失败，状态码：{response.status_code}")

print(data_list)

