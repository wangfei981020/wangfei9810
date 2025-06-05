import time
import requests
import logging
from collections import deque
from datetime import datetime
import pytz
from prometheus_client import Gauge
from get_nacos_config import get_config_nacos
from lark_alert import alert_lark, alert_text

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 定义 Prometheus 指标和全局状态记录
container_status = Gauge('container_status', '当前容器的状态', ['namespace', 'container'])
# 全局状态跟踪字典，结构：{(namespace, container): deque(maxlen=6)}
status_history = {}
data_history = {}

def _query_loki(url, query, namespace, container):
    """执行 Loki 查询并返回是否有数据"""
    try:
        end_time_ns = int(time.time()) 
        # 保持一个10秒的查询窗口
        start_time_ns = end_time_ns - 10 
        response = requests.get(
            url,
            params={
                'query': query,
                'limit': 1000,
                'start': start_time_ns,
                'end': end_time_ns
            },
            timeout=10
        )
        response.raise_for_status()
        result_count = len(response.json()['data']['result'])
        result_logs = response.json()["data"]['result']
        if result_logs != []:
            for i in result_logs:
                msg = i['values'][0][-1]
        else:
            msg = False
        return {
            'namespace': namespace,
            'container': container,
            'count': 1 if result_count > 0 else 0,
            'message': msg
        }
    except Exception as e:
        logger.error(f"Loki 查询失败: {str(e)}")
        logger.error(f"container: {container}")
        return {'namespace': namespace, 'container': container, 'count': 0,'message': False}

def background_job():

    """后台循环任务，不断查询 Loki 并更新 Prometheus 指标"""
    config = get_config_nacos()
    loki_url = config['loki_url']
    
    while True:
        cycle_start = time.time()
        logger.info("========== 开始新一轮查询周期 ==========")
        
        for namespace_group in config['containers']:
            namespace = namespace_group['namespace']
            for container in namespace_group['containers']:
                query = f'{{namespace="{namespace}",container=~"{container}.*"}} |~ "Link.* timestamp.* Round.*"'
                
                # 执行查询
                data = _query_loki(loki_url, query, namespace, container)
                key = (namespace, container)
                
                # 初始化历史记录队列
                if key not in status_history:
                    status_history[key] = deque(maxlen=6)  # 保存6次记录
                    data_history[key] = deque(maxlen=1)
                # 记录本次查询结果
                status_history[key].append(data['count'])
                
                # 判断状态：如果最近6次查询中有任意一次结果为1，则认为状态为正常（1）
                current_status = 1 if any(status_history[key]) else 0
                if current_status != 0:
                    if data['message'] != False:
                        data_history[key].append(data['message'])
                container_status.labels(namespace=namespace, container=container).set(int(current_status))
                
                logger.info(
                    f"状态更新 | 命名空间: {namespace:15} | 容器: {container:20} | "
                    f"本次结果: {data['count']} | 最终状态: {current_status} | "
                    f"历史记录: {list(status_history[key])} | "
                    f"历史消息: {list(data_history[key])} "
                )
                data_history_list = list(data_history[key])
                data_history_str = ''.join(data_history_list)
                if int(current_status) == 0:
                    if len(list(status_history[key])) == 6:
                        shanghai_tz = pytz.timezone('Asia/Shanghai')
                        current_time = datetime.now(shanghai_tz)
                        message = f"{container} 30分钟内搜不到指定格式日志: Link-xxx timestamp: xxx Round: xxx"
                        content_list = alert_text(namespace, container, current_status, message, current_time,data_history_str)
                        mentioned_list = []
                        for j in config["lark_id"].values():
                            mentioned = f"<at id={j}>@{j}</at"
                            mentioned_list.append(mentioned)
                        mentioned_str = ",".join(mentioned_list)
                        content_list.append(mentioned_str) 
                        webhook_url = config['webhook_url']
                        alert_lark(webhook_url, "⚠️⚠️⚠️告警通知", "red",content_list,mentioned_str)
                        logger.info(f"{container} 调用 lark")
        
        # 精确控制循环间隔
        elapsed = time.time() - cycle_start
        sleep_time = max(20 - elapsed, 10)
        logger.info(f"本轮查询完成，耗时 {elapsed:.2f} 秒，下次查询将在 {sleep_time:.2f} 秒后执行\n")
        time.sleep(sleep_time)
