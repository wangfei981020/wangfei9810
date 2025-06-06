# data_check.py
import os
import re
import time
import pytz
import logging
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict
from metrics import (
    JOB_EXECUTION_COUNTER,
    JOB_DURATION_GAUGE,
    LOG_PROCESSED_GAUGE,
    LAST_SUCCESS_GAUGE,
    RESPONSE_STATUS_GAUGE
)

from get_nacos_config import get_config_nacos
from lark_alert import alert_lark, alert_text, alert_text1

logger = logging.getLogger(__name__)

# 常量定义
BASE_FILE_NAME = "./logs/data_wallet.txt"
DATE_FORMAT = "%Y-%m-%d"
LINE_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+([a-f0-9-]+)\s+(https?://\S+)\s+(\d+)$"
)
LOG_PARSE_PATTERN = re.compile(
    r"(?P<time>\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}\.\d+)|"
    r"tid:(?P<tid>[a-f0-9-]+)|"
    r"(?P<url>https?://\S+)|running time = (?P<ms>\d+) ms"
)

# ======================
# 核心业务方法
# ======================
def _query_loki(loki_url, query, namespace, container):
    """执行Loki查询（严格5分钟窗口）"""
    try:
        end_time = int(time.time())
        start_time = end_time - 300  
        response = requests.get(
            loki_url,
            params={
                "query": query,
                "limit": 5000,
                "start": start_time,
                "end": end_time
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json()["data"]["result"]
    except Exception as e:
        logger.error(f"Loki查询失败: {str(e)} [容器: {container}]")
        return None

def _send_alert(config, record):
    config = get_config_nacos()
    """发送实时报警"""
    try:
        content = alert_text1(
            record["tid"], 
            record["url"], 
            record["duration"], 
            record["timestamp"]
        )
        mentioned_list = []
        for j in config["lark_id"].values():
            mentioned = f"<at id={j}>@{j}</at"
            mentioned_list.append(mentioned)
        mentioned_str = ",".join(mentioned_list)
        # content.append(mentioned_str) 
        alert_lark(
            config["webhook_url"],
            "🚨 告警通知",
            "red",
            content,
            mentioned_str
        )
    except Exception as e:
        logger.error(f"发送报警失败: {str(e)}")

def process_and_report(file_path, config):
    """处理日志并发送报告"""
    domain_stats = defaultdict(lambda: {
        "count": 0, 
        "total": 0, 
        "min": float("inf"), 
        "max": 0
    })
    
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = LINE_PATTERN.match(line)
                if not match:
                    logger.warning(f"无效日志格式: {line}")
                    continue
                
                timestamp,tid, url, duration = match.groups()
                try:
                    domain = urlparse(url).netloc
                    duration = int(duration)
                except Exception as e:
                    logger.error(f"数据解析失败: {str(e)} [数据: {line}]")
                    continue
                
                stats = domain_stats[domain]
                stats["count"] += 1
                stats["total"] += duration
                stats["min"] = min(stats["min"], duration)
                stats["max"] = max(stats["max"], duration)

        # 发送统计报告
        for domain, stats in domain_stats.items():
            avg = stats["total"] / stats["count"] if stats["count"] else 0
            report_time = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
            content = alert_text(
                domain,
                stats["count"],
                stats["min"],
                f"{avg:.2f}",
                stats["max"],
                report_time
            )
            mentioned = [f"<at id={id}>@{id}</at>" for id in config["lark_id"].values()]
            alert_lark(
                config["webhook_url"],
                "📊 每日性能报告",
                "green",
                content,
                ",".join(mentioned)
            )
            
    except FileNotFoundError:
        logger.error(f"日志文件不存在: {file_path}")
    except Exception as e:
        logger.error(f"日志处理异常: {str(e)}")

def _cleanup_old_logs(ref_date):
    """清理7天前的日志文件"""
    try:
        cutoff = ref_date - timedelta(days=7)
        pattern = re.compile(rf"^{re.escape(BASE_FILE_NAME)}-(\d{{4}}-\d{{2}}-\d{{2}})$")
        
        for filename in os.listdir("."):
            match = pattern.match(filename)
            if not match:
                continue
            
            try:
                file_date = datetime.strptime(match.group(1), DATE_FORMAT).date()
                if file_date < cutoff.date():
                    os.remove(filename)
                    logger.info(f"已清理过期日志: {filename}")
            except ValueError:
                logger.warning(f"无效文件名格式: {filename}")
            except Exception as e:
                logger.error(f"删除文件失败 {filename}: {str(e)}")
                
    except Exception as e:
        logger.error(f"日志清理失败: {str(e)}")

# ======================
# 定时任务入口
# ======================
def background_job():
    """定时数据收集任务（严格对齐5分钟）"""
    job_name = "5min_collect_job"
    start_time = time.time()
    
    try:
        logger.info("🚀 启动数据收集任务...")
        config = get_config_nacos()
        results = []
        
        for namespace_group in config["containers"]:
            namespace = namespace_group["namespace"]
            for container in namespace_group["containers"]:
                query = f'{{namespace="{namespace}",container="{container}"}} |~ "调用站点交易接口"|="http"|="性能"'
                data = _query_loki(config["loki_url"], query, namespace, container)
                
                if data:
                    for entry in data:
                        for _, log in entry.get("values", []):
                            matches = LOG_PARSE_PATTERN.findall(log)
                            record = {"timestamp": "", "url": "", "duration": ""}
                            for time_part, tid_part,url_part, ms_part in matches:
                                if time_part: record["timestamp"] = time_part
                                if tid_part: record["tid"] = tid_part
                                if url_part: record["url"] = url_part
                                if ms_part: record["duration"] = ms_part
                            
                            if all(record.values()):
                                results.append(record)
                                
                                if int(record["duration"]) > 3000:
                                    _send_alert(config, record)

        if results:
            domain_max_list = []
            domain_min_list = []
            with open(BASE_FILE_NAME, "a") as f:
                for item in results:
                    f.write(f"{item['timestamp']} {item['tid']} {item['url']} {item['duration']}\n")
                    duration = int(item["duration"])
                    if duration > 1000:
                        domain_url = item['url']
                        if domain_url not in domain_max_list:
                            domain_max_list.append(domain_url)

            if domain_max_list:
                for m in list(set(domain_max_list)):
                    status = 1 
                    RESPONSE_STATUS_GAUGE.labels(url=m).set(status)
                    if m in domain_min_list:
                        domain_min_list.remove(m)
                        logger.info(f"{m} 已删除，当前列表:", domain_min_list)
  
            if domain_min_list:
                for d in list(set(domain_min_list)):
                    status = 0
                    RESPONSE_STATUS_GAUGE.labels(url=d).set(status)
            logger.info(f"📥 成功写入 {len(results)} 条日志记录")
            
            
        LOG_PROCESSED_GAUGE.labels(job_name).set(len(results))
        LAST_SUCCESS_GAUGE.labels(job_name).set_to_current_time()
        JOB_EXECUTION_COUNTER.labels(job_name, 'success').inc()
        
    except Exception as e:
        logger.error(f"数据收集任务异常: {str(e)}")
        JOB_EXECUTION_COUNTER.labels(job_name, 'failed').inc()
    finally:
        JOB_DURATION_GAUGE.labels(job_name).set(time.time() - start_time)

def daily_job():
    """每日日志处理任务"""
    job_name = "daily_report_job"
    start_time = time.time()
    
    try:
        logger.info("🌙 启动每日日志处理...")
        config = get_config_nacos()
        tz = pytz.timezone("Asia/Shanghai")
        now = datetime.now(tz)
        
        if os.path.exists(BASE_FILE_NAME):
            process_and_report(BASE_FILE_NAME, config)
            new_name = f"{BASE_FILE_NAME}-{now.strftime(DATE_FORMAT)}"
            os.rename(BASE_FILE_NAME, new_name)
            logger.info(f"🔄 文件已重命名为: {new_name}")
            open(BASE_FILE_NAME, "a").close()
        else:
            logger.warning("⚠️ 未找到当日日志文件")
            
        _cleanup_old_logs(now)
        
        LAST_SUCCESS_GAUGE.labels(job_name).set_to_current_time()
        JOB_EXECUTION_COUNTER.labels(job_name, 'success').inc()
        
    except Exception as e:
        logger.error(f"每日任务失败: {str(e)}")
        JOB_EXECUTION_COUNTER.labels(job_name, 'failed').inc()
    finally:
        JOB_DURATION_GAUGE.labels(job_name).set(time.time() - start_time)