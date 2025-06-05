# logging.py
import logging

def setup_logging():
    # 配置日志，只输出到控制台
    logging.basicConfig(
        level=logging.INFO,  # 日志级别设置为 INFO
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]  # 只输出到控制台
    )
    return logging.getLogger(__name__)
