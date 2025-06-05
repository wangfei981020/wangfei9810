\import threading
from flask import Flask, Response
from prometheus_client import generate_latest
from data_checker import background_job  # 导入 data_check 中的后台任务

app = Flask(__name__)

# @app.route("/metrics")
@app.route("/actuator/prometheus")
def metrics():
    """请求 /metrics 接口时返回最新 Prometheus 指标数据"""
    metrics_data = generate_latest()
    return Response(metrics_data, mimetype="text/plain")

if __name__ == '__main__':
    # 启动后台线程执行查询任务
    thread = threading.Thread(target=background_job)
    thread.daemon = True
    thread.start()
    
    app.run(host='0.0.0.0', port=8000)
