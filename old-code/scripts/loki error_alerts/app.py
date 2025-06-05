from flask import Flask, Response
import logging
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from metrics import get_logs,convert_to_prometheus_format


# 初始化 Flask 应用
app = Flask(__name__)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# 每5分钟执行一次的任务
def scheduled_task():
    count_dict,specify_dict = get_logs()
    prometheus_metrics = convert_to_prometheus_format(count_dict,specify_dict)
    logging.info(f"task is triggered to execute at the current time {datetime.datetime.now()}")

# 配置 APScheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=3)  # 每5分钟执行一次任务
    scheduler.start()
    scheduled_task()
    
@app.route('/task')
def task():
    return "Flask app is running. Task will run every 5 minutes."
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
        prometheus_line = f'log_error{{code="00000"}} 0'
        return prometheus_line
    
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
    app.run(debug=True, host='0.0.0.0', port=9108, use_reloader=False)