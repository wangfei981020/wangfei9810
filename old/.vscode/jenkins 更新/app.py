from flask import Flask, request
from prometheus_client import start_http_server, generate_latest
import receive_data  # 导入 receive_data 模块

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive():
    """
    接收 POST 请求的数据，并传递给 receive_data 进行处理
    """
    data = request.json  # 获取 JSON 数据
    print(f"Received data: {data}")
    
    # 调用 receive_data.py 中的处理函数
    receive_data.process_data(data)
    
    return "Data received", 200

# /metrics 路由，用于暴露 Prometheus 指标
@app.route('/metrics')
def metrics():
    """
    返回 Prometheus 指标
    """
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    # 启动 Prometheus HTTP 服务，暴露指标数据
    start_http_server(8088)  # Prometheus 指标端口
    
    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=8080)
