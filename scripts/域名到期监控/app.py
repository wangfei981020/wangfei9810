import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
from meritcs import update_data, get_remaining_days
from datetime import datetime
import os

app = Flask(__name__)


# app.py 新增以下内容
from apscheduler.schedulers.background import BackgroundScheduler

# 初始化缓存
cached_metrics = None
last_update = None

CONFIG_PATH = r"d:\code\scripts\域名到期监控\config.yml"
os.environ['CONFIG_PATH'] = CONFIG_PATH
def background_update():
    """后台定时更新数据的独立任务"""
    global cached_metrics, last_update
    try:
        print(f"当前工作目录: {os.getcwd()}")
        # print(f"配置文件路径: {os.environ['CONFIG_PATH']}")

        registry = CollectorRegistry()
        domain_status = Gauge(
            "domain_status",
            "check the status of domains",
            ["domain", "issuer", "end_time"],
            registry=registry
        )
        
        # 获取数据（这里保留你原有的数据处理逻辑）
        domains_info = update_data()
        print('111')
        
        # 填充指标
        for domain_info in domains_info:
            if domain_info["End_time"] == "信息不可用":
                continue
            days = get_remaining_days(domain_info["End_time"])
            domain_status.labels(
                domain=domain_info["Domain"],
                issuer=domain_info["Issuer"],
                end_time=domain_info["End_time"]
            ).set(days)
            
        # 生成 Prometheus 数据并缓存
        cached_metrics = prometheus_client.generate_latest(registry)
        last_update = datetime.now()
    except Exception as e:
        print(f"更新指标失败: {e}")

# 启动后台调度器（每小时更新一次）
scheduler = BackgroundScheduler()
scheduler.add_job(background_update, 'interval', minutes=60)
scheduler.start()
# 启动时立即执行一次查询
background_update()

@app.route("/metrics")
def metrics():
    if not cached_metrics:
        return "Exporter not ready", 503
    return Response(cached_metrics, mimetype="text/plain")


@app.route("/")
def index():
    return "<h1>Customized Exporter</h1><br> <a href='metrics'>Metrics</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9103, debug=True)
