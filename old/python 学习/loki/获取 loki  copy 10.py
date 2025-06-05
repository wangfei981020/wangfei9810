from flask import Flask, Response
import requests
import json
import time
import re
import yaml
from collections import defaultdict
# from collections import Counter
import logging 
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

def get_dynamic_time_range():
    end_timestamp = int(time.time())  # 当前时间戳（秒）
    start_timestamp = end_timestamp - 300  # 前五分钟的时间戳（秒）

    start_timestamp_ns = start_timestamp * int(1e9)
    end_timestamp_ns = end_timestamp * int(1e9)

    return start_timestamp_ns, end_timestamp_ns

# 初始化 Flask 应用
app = Flask(__name__)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为 DEBUG（也可以选择 INFO, WARNING, ERROR, CRITICAL）
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志的输出格式
    handlers=[
        logging.StreamHandler()  # 输出到控制台
    ]
)

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
        params = {
            'query': query,
            'start': start_timestamp_ns,  # 开始时间（纳秒）
            'end': end_timestamp_ns,  # 结束时间（纳秒）
        }

        try:
            response = requests.get(loki_url, params=params, timeout=60)
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
                            code_msg_pattern = r'tid:([a-zA-Z0-9\-]+).*?"code":"(\d+)","msg":"([^"]+)"'
                            code_msg_matches = re.findall(code_msg_pattern, entry[1])
                            if code_msg_matches != []:
                                log_lines = entry[1].splitlines()
                                # 获取前30行内容
                                first_30_lines = log_lines[:30]
                                # print(first_30_lines)
                                first_30_lines_str = '\n'.join(first_30_lines)
                                for match in code_msg_matches:
                                    tid, code, msg = match
                                    count_dict[(namespace, container, tid,code, msg,first_30_lines_str)] += 1
            else:
                return Response(
                    json.dumps({"error": "请求失败", "status_code": response.status_code}),
                    status=response.status_code,
                    mimetype='application/json'
                )
        except requests.exceptions.Timeout:
            logging.error('请求超时! url: ', loki_url)
        except requests.exceptions.RequestException as e:
            logging.error(f"请求发生异常: {e}")
    return count_dict

def alert_text(namespace,container,tid,code,msg,exception,value):
    text = f"""**G32 status code alarm**
**Status Level: S2 Triggered**
**Namespace:** {namespace}
**Container:** {container}
**Tid:** {tid}
**Code:** {{"code":"{code}","msg":"{msg}"}}
**Value:** {value}
**Exception:**
{exception}
    """
    return text

def alert_lark(text):
    # g32 lark
    # webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/2a095143-634f-4197-862e-e63a770c63ec"
    # loki-test
    # webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/04dd7c92-e67f-4b49-9c3b-e96f049b8e45"
    config = read_config()
    webhook_url = config['webhook_url']

    # 定义告警内容
    alert_message = {
        "msg_type": "interactive",  # 消息类型为卡片
        "card": {
            "config": {"wide_screen_mode": True},  # 开启宽屏模式
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "⚠️ 告警通知"  # 卡片标题
                },
                "template": "red"  # 使用红色模板表示告警
            },
            "elements": [
                {
                    "tag": "div",  # 使用 div 标签来包装文本
                    "text": {
                        "tag": "lark_md",  # 使用 lark_md 来设置富文本
                        "content": text
                    }
                }
            ]
        }
    }

    # 发送 POST 请求
    response = requests.post(webhook_url, data=json.dumps(alert_message), headers={'Content-Type': 'application/json'})

    # 打印响应状态
    if response.status_code == 200:
        logging.info(f'Task executed at {datetime.datetime.now()} 告警消息发送成功')
    else:
        logging.info(f"告警消息发送失败，状态码: {response.status_code}, 错误信息: {response.text}")

# 转换为 Prometheus 格式
def convert_to_prometheus_format(count_dict):   
    prometheus_lines = []
    for (namespace, container, tid,code, msg,exception), count in count_dict.items():
        prometheus_line = f'log_error_count{{namespace="{namespace}", container="{container}",tid="{tid}", code="{code}", msg="{msg}"}} {count}'
        alert_text1 = alert_text(namespace,container,tid,code,msg,exception,count)
        # logging.info(f"Task executed at {datetime.datetime.now()}")
        # alert_lark(alert_text1)
        prometheus_lines.append(prometheus_line)

    return "\n".join(prometheus_lines)

# 配置 APScheduler
def start_scheduler():
    count_dict = get_logs()
    my_task = convert_to_prometheus_format(count_dict)
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_task, 'interval', minutes=5)  # 每5分钟执行一次任务
    scheduler.start()


# 定义 /metrics 接口
@app.route('/task')
def task():
    # count_dict = get_logs()
    # prometheus_metrics = convert_to_prometheus_format(count_dict)
    # print(prometheus_metrics)
    # return Response(prometheus_metrics, content_type='text/plain; version=0.0.4; charset=utf-8')
    return "Flask app is running. Task will run every 5 minutes."

if __name__ == '__main__':
    # 启动调度器
    start_scheduler()
    app.run(debug=True, host='0.0.0.0', port=5000,use_reloader=False)



