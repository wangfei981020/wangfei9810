import logging
import requests
import json
import datetime
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 向 Lark 发送告警
def alert_lark(webhook_url, title, card_color,content_list, mentioned_list=None):
    # 构建卡片消息内容
    message_data = {
        "msg_type": "interactive",  # 指定消息类型为 "interactive"（卡片消息）
        "card": {
            "config": {
                "wide_screen_mode": True,  # 可选：开启宽屏模式
                "enable_forward": True     # 可选：允许转发
            },
            "header": {
                "template": card_color,  # 根据 status 选择卡片的颜色模板
                "title": {
                    "content": title,  # 卡片的标题
                    "tag": "plain_text"  # 标题为纯文本
                }
            },
            "elements": [
                {
                    "tag": "div",  # 卡片内容部分
                    "text": {
                        "content": content,
                        "tag": "lark_md"  # 使用 Lark Markdown 语法来格式化文本
                    }
                } for content in content_list
            ]
        }
    }

    try: 
        response = requests.post(webhook_url, data=json.dumps(message_data), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            logging.info(f"告警消息发送成功 at {datetime.datetime.now()}")
        else:
            logging.error(f"告警消息发送失败，状态码: {response.status_code}, 错误信息: {response.text}")
    except Exception as e:
        logging.error(f"发送告警消息时发生未知异常: {e}")
        logging.error(f"未发送消息: {content_list}")

def alert_text(domain, count, data_min,data_avg,data_max,alert_time):
    content_list = [
            f"**电子钱包性能统计**",
            f"**域名**: {domain}",
            f"**交易**: {count} 次",
            f"**性能**: 最快: {data_min}ms    平均: {data_avg}ms    最慢: {data_max}ms",
            f"**日期**: {alert_time}"
        ]
    return content_list

def alert_text1(tid,domain, ms, alert_time):
    content_list = [
            f"**G32 电子钱包当前域名性能已超过1000ms**",
            f"**tid**: {tid}",
            f"**域名**: {domain}",
            f"**ms**: {ms}",
            f"**Time**: {alert_time}"
        ]

    return content_list