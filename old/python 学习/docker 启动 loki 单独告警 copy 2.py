from flask import Flask, Response
import requests
import json
import time
import os
import re
import yaml
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import shutil
from collections import defaultdict

# 初始化 Flask 应用
app = Flask(__name__)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 获取时间戳
def get_dynamic_time_range():
    end_timestamp = int(time.time())  # 当前时间戳（秒）
    start_timestamp = end_timestamp - 300  # 前五分钟的时间戳（秒）
    start_timestamp_ns = start_timestamp
    print('start time: ',start_timestamp_ns)
    end_timestamp_ns = end_timestamp
    print('end time: ',end_timestamp_ns)
    return start_timestamp_ns, end_timestamp_ns

# 读取配置文件
def read_config():
    with open('config1.yml', 'r',encoding='utf-8') as f:
        config = yaml.safe_load(f)
        return config

# 从 Loki 获取日志数据
def get_logs():
    count_dict = defaultdict(int)  # 用于统计 transaction stats
    specify_dict = defaultdict(int)  # 用于统计 transaction stats
    config = read_config()
    loki_url = config['loki_url']
    start_timestamp_ns, end_timestamp_ns = get_dynamic_time_range()
    all_logs = []
    for n in config['namespace']:
        # query = f'{{namespace="{n}", pod=~".*"}} |= "ERROR" |~ "code.*[0-9]+"'
        query = f'{{namespace="g32-wallet", pod="wallet-client-backend"}} |= "ERROR" |~ "code.*[0-9]+"'
        if n == "g32-wallet" or n == "g32-openapi":
            for c in config['containers']:
                if c['namespace'] == n:
                    namespaces = c['namespace']
                    containers = c['container']
                    query = f'{{namespace="{n}", container="{containers}"}} |= "ERROR"'
                    # query = '{namespace="g32-game-center", container="game-event-source-backend"} |= "ERROR"'
                    # query = '{namespace="g32-wallet", container="wallet-client-backend"} |= "ERROR"'
        params = {
            'query': query,
            'start': start_timestamp_ns,
            'end': end_timestamp_ns,
            'limit': 100
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
                            # print('1111',code_msg_matches)
                            if container == "openapi-backend" or container == "wallet-client-backend":
                                entry_log = entry[1].split()
                                tid = entry_log[2].split(':')[1]
                                # print('333',tid)
                                if entry_log[3] == "ERROR":
                                    log_lines = entry[1].splitlines()
                                    first_30_lines = log_lines[:30]  # 获取前30行内容
                                    first_30_str = '\n'.join(first_30_lines)
                                    specify_dict[(namespace,container,tid,first_30_str)] += 1

                            if code_msg_matches != []:

                                log_lines = entry[1].splitlines()
                                first_30_lines = log_lines[:30]  # 获取前30行内容
                                first_30_lines_str = '\n'.join(first_30_lines)
                                for match in code_msg_matches:
                                    tid, code, msg = match
                                    count_dict[(namespace, container, tid, code, msg, first_30_lines_str)] += 1
                                    
            else:
                logging.error(f"请求失败, 状态码: {response.status_code}")
        except requests.exceptions.Timeout:
            logging.error(f"请求超时! url: {loki_url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"请求发生异常: {e}")
    # print('333',count_dict)

    return count_dict,specify_dict

# 生成告警文本
def alert_text(namespace, container, tid, code, msg, exception, value):
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

# 指定 container 告警文本
def alert_specify_text(namespace, container, tid,exception, value):
    text = f"""**G32 status code alarm**
**Status Level: S2 Triggered**
**Namespace:** {namespace}
**Container:** {container}
**Tid:** {tid}
**Value:** {value}
**Exception:**
{exception}
    """
    return text

# 向 Lark 发送告警
def alert_lark(text,webhook_url,alert_s,alert_temp):
    alert_message = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    # "content": "⚠️ 告警通知"
                    "content": alert_s
                },
                # "template": "red"
                "template": alert_temp
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": text
                    }
                }
            ]
        }
    }
    try: 
        response = requests.post(webhook_url, data=json.dumps(alert_message), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            logging.info(f"告警消息发送成功 at {datetime.datetime.now()}")
        else:
            logging.error(f"告警消息发送失败，状态码: {response.status_code}, 错误信息: {response.text}")
    except Exception as e:
        logging.error(f"发送告警消息时发生未知异常: {e}")
        logging.error(f"未发送消息: {text}")

def parse_json_with_escape(json_str):
    # 替换掉转义的引号
    fixed_str = json_str.replace('\\"', '"')
    return json.loads(fixed_str)

def is_file(error_log_path):
    config = read_config()
    webhook_url = config['webhook_url']
    if os.path.isfile(error_log_path):
        with open(error_log_path,'r',encoding='utf-8') as file:
            data = json.load(file)
            for i in data:
                namespace = re.search(r'"namespace":"([^"]+)"',i).group(1)
                container = re.search(r'"container":"([^"]+)"',i).group(1)
                tid = re.search(r'"tid":"([^"]+)"',i).group(1)
                code = re.search(r'"code":"([^"]+)"',i).group(1)
                msg = re.search(r'"msg":"([^"]+)"',i).group(1)
                exception_list = i.split(',')[5:-1]
                exception1 = ''.join(exception_list).split(':')[1:]
                exception = ''.join(exception1).strip('"')
                alert_text_recover = alert_text(namespace, container, tid, code, msg, exception, 0)
                alert_lark(alert_text_recover,webhook_url,"✅ 恢复通知","green")
                # 删除告警文件
        os.remove(error_log_path)
        logging.info('删除告警文件: %s' % error_log_path)       
    else:
        logging.info('无错误日志')
# 转换为 Prometheus 格式
def convert_to_prometheus_format(count_dict,specify_dict):   
    config = read_config()
    webhook_url = config['webhook_url']
    prometheus_lines = []
    alert_text1 = "No error status code"
    alert_text2 = "No error"
    alert_status = "Flase"
    # num = 0
    error_log_path = "error_log.json"
    if not count_dict:
        is_file(error_log_path)
        print('是空的')
    else:
        # print('不是空的')
        for (namespace, container, tid, code, msg, exception), count in count_dict.items():
            text1 = f'{{"namespace":"{namespace}", "container":"{container}","tid":"{tid}", "code":"{code}", "msg":"{msg}","exception":"{exception}","count":"{count}"}}'
            alert_text1 = alert_text(namespace, container, tid, code, msg, exception, count)
            logging.info({"time": {datetime.datetime.now()}, "tid": {tid},"code": {code},"msg":{msg}, "task":"task is triggered to execute at the current time "})
            prometheus_line = f'log_error{{namespace="{namespace}", container="{container}",tid="{tid}", code="{code}", msg="{msg}"}} {count}'
            # alert_lark(alert_text1,webhook_url,"⚠️ 告警通知","red")
            # num +=1
            prometheus_lines.append(prometheus_line)
            # 读取现有数据
            try:
                with open(error_log_path, "r") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []

            if isinstance(existing_data, str):
                existing_data = []  # 如果它是字符串，转换成空列表
            # 追加新数据
            existing_data.append(text1)

            # 将更新后的数据写入文件
            with open(error_log_path, "w") as f:
                json.dump(existing_data, f, indent=4)
        for (namespace, container,tid,exception), count in specify_dict.items():
            # if container == "wallet-client-backend" or container == "openapi-backend" or container == "game-event-source-backend":
            if container == "wallet-client-backend" or container == "openapi-backend":
                g32_wallet_openapi_webhook_url = config['g32_wallet_openapi_webhook_url']
                alert_text2 = alert_specify_text(namespace, container,tid,exception, count)
                # print('111',alert_text2)
                # logging.info({"time": {datetime.datetime.now()}, "tid": {tid},"msg": "task is triggered to execute at the current time "})
                # alert_lark(alert_text2,g32_wallet_openapi_webhook_url,"⚠️ 告警通知","red")
    # print('aaaa',num)
    return "\n".join(prometheus_lines)
    # return alert_text1,alert_text2

# 每5分钟执行一次的任务
def scheduled_task():
    count_dict,specify_dict = get_logs()
    prometheus_metrics = convert_to_prometheus_format(count_dict,specify_dict)
    # logging.info(f'111 {prometheus_metrics}')
    logging.info(f"task is triggered to execute at the current time {datetime.datetime.now()}")

# 配置 APScheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=3)  # 每5分钟执行一次任务
    scheduler.start()
    scheduled_task()
    
start_scheduler()
# @app.route('/task')
# def task():
#     return "Flask app is running. Task will run every 5 minutes."
@app.route('/metrics')
def metrics():
    count_dict,specify_dict = get_logs()
    # prometheus_metrics = convert_to_prometheus_format(count_dict,specify_dict)
    if "error" in count_dict:
        return Response(
            f'{{"error": "{count_dict["error"]}", "status_code": {count_dict["status_code"]}}}',
            status=count_dict["status_code"],
            mimetype='application/json',
            headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',  # 禁用缓存
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )

    prometheus_metrics = convert_to_prometheus_format(count_dict,specify_dict)
    if prometheus_metrics == "":
        prometheus_line = f'log_error{{status="true"}} 1'
        return prometheus_line
    
    logging.info('111 %s' % prometheus_metrics)
    return Response(
        prometheus_metrics,
        content_type='text/plain; version=0.0.4; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',  # 禁用缓存
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)




    
