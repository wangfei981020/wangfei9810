# app.py
from flask import Flask, Response
from metrics import get_logs, convert_to_prometheus_format

# 初始化 Flask 应用
app = Flask(__name__)

# 定义 /metrics 接口
@app.route('/metrics')
def metrics():
    count_dict = get_logs()  # 获取 Loki 的日志统计
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

    prometheus_metrics = convert_to_prometheus_format(count_dict)
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
    app.run(debug=True, host='0.0.0.0', port=9108)