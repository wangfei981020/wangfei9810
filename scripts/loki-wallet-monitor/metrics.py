# metrics.py
from prometheus_client import Counter, Gauge

# 监控指标定义
METRICS_PORT = 8080

# 自定义指标
JOB_EXECUTION_COUNTER = Counter(
    'scheduler_job_executions_total',
    'Total job executions',
    ['job_name', 'status']
)

JOB_DURATION_GAUGE = Gauge(
    'scheduler_job_duration_seconds',
    'Job execution duration',
    ['job_name']
)

LOG_PROCESSED_GAUGE = Gauge(
    'scheduler_logs_processed_total',
    'Total processed logs',
    ['job_name']
)

LAST_SUCCESS_GAUGE = Gauge(
    'scheduler_last_success_timestamp',
    'Timestamp of last successful job run',
    ['job_name']
)

RESPONSE_STATUS_GAUGE = Gauge(
    'http_response_status',
    'HTTP response status (1=超过1000ms, 0=正常)',
    ['url']  # 按URL维度记录
)