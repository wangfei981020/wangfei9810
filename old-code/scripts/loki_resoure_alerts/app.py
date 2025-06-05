from flask import Flask, Response
from prometheus_client import generate_latest
from data_checker import refresh_metrics  # 导入 refresh_metrics 函数

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    # 每次请求 /metrics 时，先刷新数据
    refresh_metrics()
    metrics_data = generate_latest()
    return Response(metrics_data, mimetype='text/plain')

if __name__ == "__main__":
    port = 8000
    app.run(host='0.0.0.0', port=port)
