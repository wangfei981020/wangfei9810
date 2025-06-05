from flask import Flask, Response
import requests
import json
import time
import re
from collections import defaultdict

app = Flask(__name__)

# 配置 Loki 服务器地址和查询参数
loki_url = "http://loki.g32-prod.com/loki/api/v1/query"

# 查询条件：例如查询某一时间范围内的日志
query = '{namespace=~"g32.*", pod=~".*"} |= "ERROR" |~ "code.*[0-9]+"'  # 可以根据实际修改查询条件

# 设置查询时间范围：过去5分钟
end_time = int(time.time())  # 当前时间
start_time = end_time - 300  # 5分钟前的时间戳

# 格式化时间为 Loki API 所需的 RFC3339 格式
start_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(start_time))
end_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(end_time))

# 构造请求参数
params = {
    'query': query,
    'limit': 100,  # 最大返回结果数
    'start': start_time,
    'end': end_time
}

@app.route('/metrics', methods=['GET'])
def get_logs():
    # 请求 Loki 数据
    response = requests.get(loki_url, params=params)
    count_dict = defaultdict(int)  # 用于统计 transaction stats

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'result' in data['data']:
            logs = data['data']['result']
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
                    for match in code_msg_matches:
                        code, msg = match
                        count_dict[(code, msg)] += 1

    else:
        return Response(
            json.dumps({"error": "请求失败", "status_code": response.status_code}),
            status=response.status_code,
            mimetype='application/json'
        )

    # 输出 Prometheus 格式的数据
    prometheus_metrics = []
    for (code, msg), count in count_dict.items():
        # 格式化 Prometheus 指标
        prometheus_metrics.append(
            f'log_error{{container="{container}", namespace="{namespace}", code="{code}", msg="{msg}"}} {count}\n'
        )

    # 返回结果为 Prometheus 格式
    return Response(''.join(prometheus_metrics), mimetype='text/plain')

if __name__ == '__main__':
    # 启动 Flask Web 服务器，监听 0.0.0.0:5000 地址
    app.run(host='0.0.0.0', port=5000)
