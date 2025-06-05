from flask import Flask, Response
import requests
import json
import time
import re
import yaml
from collections import defaultdict
from collections import Counter

# 配置 Loki 服务器地址和查询参数


# 获取当前时间戳和前五分钟的时间戳（3000秒）
end_timestamp = int(time.time())  # 当前时间戳（秒）
start_timestamp = end_timestamp - 300  # 前五分钟的时间戳（秒）

# 将时间戳转换为纳秒（Loki 使用纳秒级时间戳）
start_timestamp_ns = start_timestamp * int(1e9)
end_timestamp_ns = end_timestamp * int(1e9)

# 初始化 Flask 应用
app = Flask(__name__)

# 读取配置文件
def read_config():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        # print(config)
        return config

# 从 Loki 获取日志数据并返回计数结果
def get_logs():
    count_dict = defaultdict(int)  # 用于统计 transaction stats
    config = read_config()
    loki_url = config['loki_url']

    for n in config['namespace']:
        query = f'{{namespace="{n}", pod=~".*"}} |= "ERROR" |~ "code.*[0-9]+"'

        # 构造查询参数
        params = {
            'query': query,
            'start': start_timestamp_ns,  # 开始时间（纳秒）
            'end': end_timestamp_ns,  # 结束时间（纳秒）
        }

        # 发送请求到 Loki
        # response = requests.get(loki_url, params=params)
        try:
            response = requests.get(loki_url, params=params, timeout=60)
            # 在这里处理返回的 response 数据
            # print(response.status_code)  # 打印响应状态码
            # print(response.text)  # 打印响应内容

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
                            # print(entry[1])
                            # 正则匹配 "code" 和 "msg"
                            # code_msg_pattern = r'"code":"(\d+)","msg":"([^"]+)"'
                            code_msg_pattern = r'tid:([a-zA-Z0-9\-]+).*?"code":"(\d+)","msg":"([^"]+)"'
                            # code_msg_pattern = r'tid:([a-zA-Z0-9\-]+).*?"code({.*?})'
                            # code_msg_pattern = r'tid:([a-zA-Z0-9\-]+).*?code=([a-zA-Z0-9\-]+).*?({.*?})?'
                            code_msg_matches = re.findall(code_msg_pattern, entry[1])
                            # print(code_msg_matches)
                            if code_msg_matches != []:
                                # print(code_msg_matches)
                                # print(type(code_msg_matches))
                                # print(entry[1])
                                log_lines = entry[1].splitlines()
                                # 获取前30行内容
                                first_30_lines = log_lines[:30]
                                first_30_lines_str = '\n'.join(first_30_lines)
                                # print('30行内容: ',first_30_lines_str)
                                # Exception
                                # new_log_data = [(tid, code, msg, first_30_lines_str) for tid, code, msg in code_msg_matches]
                                for match in code_msg_matches:
                                    tid, code, msg = match
                                    count_dict[(namespace, container, tid,code, msg,first_30_lines_str)] += 1
                                # print(new_log_data)
                                # count_dict[(namespace, container, tid,code, msg)] += 1
                                # return new_log_data
                                # 输出前30行
                                # for line in first_30_lines:
                                #     print('30行内容: ',line)  
                                    # print(line)

                            # 更新计数器
                            # for match in code_msg_matches:
                            #     tid, code, msg = match
                            #     count_dict[(namespace, container, tid,code, msg)] += 1
            else:
                return Response(
                    json.dumps({"error": "请求失败", "status_code": response.status_code}),
                    status=response.status_code,
                    mimetype='application/json'
                )
        except requests.exceptions.Timeout:
            print("请求超时！")
        except requests.exceptions.RequestException as e:
            print(f"请求发生异常: {e}")
    # print(count_dict)
    return count_dict

# 转换为 Prometheus 格式
def convert_to_prometheus_format(count_dict):
    prometheus_lines = []
    for (namespace, container, tid,code, msg,exception), count in count_dict.items():
        prometheus_line = f'log_error_count{{namespace="{namespace}", container="{container}",tid="{tid}", code="{code}", msg="{msg}",Exception="{exception}"}} {count}'
        prometheus_lines.append(prometheus_line)
    return "\n".join(prometheus_lines)

# 定义 /metrics 接口
@app.route('/metrics')
def metrics():
    count_dict = get_logs()
    prometheus_metrics = convert_to_prometheus_format(count_dict)
    print(prometheus_metrics)
    return Response(prometheus_metrics, content_type='text/plain; version=0.0.4; charset=utf-8')
# metrics()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# get_logs()
# print(count_dict)
