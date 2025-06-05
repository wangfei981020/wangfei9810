from prometheus_client import Gauge
from prometheus_client import REGISTRY
import subprocess
import time
import json
import os
import logging

# 定义 Prometheus 指标，使用 job, proj, dest_namespace, current_time 作为标签
jenkins_update_job_gauge = Gauge('jenkins_update_job', 'The start time of the job', ['proj', 'job', 'dest_namespace','current_time','image_tag'])

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 获取所有已注册的指标
def get_all_metrics():
    metrics = {}
    for metric_family in REGISTRY.collect():
        for sample in metric_family.samples:
            metric_name = sample.name
            label_values = sample.labels
            value = sample.value
            metrics[(metric_name, tuple(label_values.items()))] = value
    return metrics

def process_data(data):
    """
    处理接收到的数据并更新 Prometheus 指标
    """
    proj = data['job'] + '-' + data['proj']  # 将 job 和 proj 组合在一起
    dest_namespace = data['proj']  # 获取 dest_namespace
    status = data['status']
    job = data['job']
    current_time = data['current_time']
    image_tag = data["image_tag"]
    if status == "false":
        status = 1
    else:
        status = 0 
    # 获取所有指标并打印
    all_metrics = get_all_metrics()
    for (metric_name, labels), value in all_metrics.items():
        # print("metric_name:",metric_name)
        if metric_name != "jenkins_update_job":
            job_name = False
        if metric_name == "jenkins_update_job":
            job_name = True

    if job_name:
        print('job_name:',job_name)
        # jenkins_update_job_gauge.remove(proj=,data['job'],namespace,current_time)
        labels_dict = dict(labels)
        if labels_dict['proj'] == proj:
            print('labels_dict:',labels_dict['proj'])
            labels_prometheus_format = ', '.join([f'{key}="{value}"' for key, value in labels])
            print('labels_dict:',labels_prometheus_format)
            proj_old = labels_dict['proj']
            job_old = labels_dict['job'] 
            namespace_old = labels_dict['dest_namespace']
            current_time_old = labels_dict['current_time']
            image_tag_old = labels_dict['image_tag']
            logger.info('Removing metric with labels: proj=%s, job=%s, dest_namespace=%s, current_time=%s, image_tag=%s',
                                proj, job, dest_namespace, current_time, image_tag)
            jenkins_update_job_gauge.remove(proj_old,job_old,namespace_old,current_time_old,image_tag_old)
            jenkins_update_job_gauge.labels(proj=proj, job=job, dest_namespace=dest_namespace,current_time=current_time,image_tag=image_tag).set(status)
            logger.info('Updated metric: proj=%s, job=%s, dest_namespace=%s, current_time=%s, image_tag=%s with status %d',
                                proj, job, dest_namespace, current_time, image_tag, status)
        else:
            jenkins_update_job_gauge.labels(proj=proj, job=job, dest_namespace=dest_namespace,current_time=current_time,image_tag=image_tag).set(status)
            logger.info('Updated metric: proj=%s, job=%s, dest_namespace=%s, current_time=%s, image_tag=%s with status %d',
                                proj, job, dest_namespace, current_time, image_tag, status)            
    else:
        jenkins_update_job_gauge.labels(proj=proj, job=job, dest_namespace=dest_namespace,current_time=current_time,image_tag=image_tag).set(status)
        logger.info('Added new metric: proj=%s, job=%s, dest_namespace=%s, current_time=%s, image_tag=%s with status %d',
                    proj, job, dest_namespace, current_time, image_tag, status)

