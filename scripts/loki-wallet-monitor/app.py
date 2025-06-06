from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from apscheduler.schedulers.blocking import BlockingScheduler
from data_checker import background_job, daily_job
import logging
import threading
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__)

@app.route('/actuator/prometheus')
def metrics():
    """Prometheus 指标端点"""
    return Response(
        generate_latest(REGISTRY),
        mimetype=CONTENT_TYPE_LATEST
    )


def run_flask():
    """启动 Flask 服务"""
    app.run(host='0.0.0.0', port=8080)

def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)

    # 启动 Flask 线程
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 设置为守护线程
    flask_thread.start()
    logger.info("🌐 Flask 服务已启动，端口: 8080")

    # 初始化调度器
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    
    # 定时任务配置
    scheduler.add_job(
        background_job,
        trigger=CronTrigger(
            minute='*/5',
            second=0,
            timezone="Asia/Shanghai"
        ),
        name="5min_collect_job"
    )
    
    scheduler.add_job(
        daily_job,
        trigger=CronTrigger(
            hour=0,
            minute=2,
            second=0,
            timezone="Asia/Shanghai"
        ),
        name="daily_report_job"
    )
    
    try:
        logger.info("🟢 调度服务已启动，等待任务执行...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("🔴 服务已停止")
    except Exception as e:
        logger.error(f"服务异常终止: {str(e)}")

if __name__ == "__main__":
    main()