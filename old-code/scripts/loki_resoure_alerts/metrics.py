from prometheus_client import Gauge, CollectorRegistry, generate_latest

# 自定义注册表避免冲突
registry = CollectorRegistry()

# 容器状态指标（带标签）
DATA_STATUS = Gauge(
    'container_data_status',
    '容器数据状态（1=正常，0=告警）',
    ['namespace', 'container'],
    registry=registry
)

# 通知计数器
WEBHOOK_COUNTER = Gauge(
    'webhook_notifications_total',
    '飞书通知发送次数',
    ['container', 'type'],
    registry=registry
)

def get_latest_metrics():
    """获取最新指标数据"""
    return generate_latest(registry)

