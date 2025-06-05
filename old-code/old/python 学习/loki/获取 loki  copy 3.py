import requests
import time
import re
from collections import defaultdict

# 配置 Loki 服务器地址和查询参数
loki_url = "http://loki.g32-prod.com/loki/api/v1/query"

# 需要查询的命名空间列表
namespaces = [
    "g32-admin", "g32-base", "g32-bet-settle", "g32-game", 
    "g32-game-center", "g32-merchant", "g32-openapi", "g32-user", "g32-wallet"
]

# 设置查询时间范围：过去30分钟
end_time = int(time.time())  # 当前时间
start_time = end_time - 1800  # 30分钟前的时间戳

# 格式化时间为 Loki API 所需的 RFC3339 格式
start_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_time))
end_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(end_time))

# 初始化一个字典，用来存储所有命名空间的数据
all_data = {}

# 循环遍历命名空间列表
for namespace in namespaces:
    # 构造查询条件
    query = f'{{namespace=~"g32-wallet", pod=~".*"}} |= "ERROR" |~ "code.*[0-9]+"'

    # 构造请求参数
    params = {
        'query': query,
        'limit': 1000,  # 最大返回结果数
        'start': start_time,
        'end': end_time
    }

    # 发送 GET 请求到 Loki API
    response = requests.get(loki_url, params=params)
    count_dict = defaultdict(int)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'result' in data['data']:
            logs = data['data']['result']
            # print(logs)
            for log_stream in logs:
                stream = log_stream['stream']
                container = stream.get('container', 'Unknown')
                namespace = stream.get('namespace', 'Unknown')
                
                for entry in log_stream['values']:
                    # code_msg_pattern = r'"code":"(\d+)","msg":"([^"]+)"'
                    code_msg_pattern = r'{"code":"(\d+)","msg":"(.*?)"}'
                    code_msg_matches = re.findall(code_msg_pattern, entry[1])
                    for match in code_msg_matches:
                        code, msg = match
                        count_dict[(code, msg)] += 1

    else:
        print(f"请求失败，状态码：{response.status_code}")

    # 将统计信息加入到 all_data 中，生成 Prometheus 格式的输出
    if namespace not in all_data:
        all_data[namespace] = []
    
    for (code, msg), count in count_dict.items():
        # 输出 Prometheus 格式：log_transaction_count{namespace="g32-admin", code="1354", msg="Transaction failed."} 70
        prom_metric = f'log_transaction_count{{namespace="{namespace}",container="{container}" code="{code}", msg="{msg}"}} {count}'
        all_data[namespace].append(prom_metric)

# 输出所有命名空间的 Prometheus 格式数据
for namespace, metrics in all_data.items():
    for metric in metrics:
        print(metric)
