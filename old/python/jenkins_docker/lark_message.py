import requests
import json
import nacos
import yaml
import logging
import time

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从 Nacos 获取 lark_id 配置
def get_lark_id_from_nacos():
    NACOS_SERVER = 'infra-nacos.slleisure.com'  # 替换为你的 Nginx 域名
    # NACOS_SERVER = 'nacos-headless.devops'  # 替换为你的 Nginx 域名
    # NACOS_PORT = 8848  # Nginx 配置的端口，实际是代理到 Nacos 服务的端口
    NACOS_PORT = 80  # Nginx 配置的端口，实际是代理到 Nacos 服务的端口
    NACOS_USERNAME = 'jenkins-pull'  # 替换为你的 Nacos 用户名
    NACOS_PASSWORD = '123456'  # 替换为你的 Nacos 密码
    namespace = 'devops'  # 替换为你创建的命名空间 ID

    # 设置重试次数与重试间隔
    retry_count = 3  # 最大重试次数为3次
    retry_interval = 5  # 每次重试间隔5秒

    # 尝试第一次连接
    try:
        logger.info("尝试初始化 Nacos 客户端...")
        client = nacos.NacosClient(f"{NACOS_SERVER}:{NACOS_PORT}", namespace=namespace, username=NACOS_USERNAME, password=NACOS_PASSWORD)
        logger.info("成功初始化 Nacos 客户端！")
    except (requests.exceptions.RequestException, nacos.exception.NacosRequestException) as e:
        # 第一次连接失败后进行重试
        logger.error(f"第一次初始化 Nacos 客户端失败: {e}")
        # 重试机制
        for attempt in range(retry_count):
            try:
                logger.info(f"第 {attempt + 1} 次尝试初始化 Nacos 客户端...")
                client = nacos.NacosClient(f"{NACOS_SERVER}:{NACOS_PORT}", namespace=namespace, username=NACOS_USERNAME, password=NACOS_PASSWORD)
                logger.info("成功初始化 Nacos 客户端！")
                break  # 成功初始化客户端后退出重试循环
            except (requests.exceptions.RequestException, nacos.exception.NacosRequestException) as e:
                logger.error(f"初始化 Nacos 客户端失败 (第 {attempt + 1} 次尝试): {e}")
            
            if attempt < retry_count - 1:
                logger.info(f"等待 {retry_interval} 秒后重试...")
                time.sleep(retry_interval)
            else:
                logger.error("所有重试尝试都失败了，无法连接到 Nacos 服务。")
                raise  # 最后一次失败时抛出异常

    # 获取配置的 data_id 和 group
    data_id = 'update-jenkins-k8s-job'  # 替换为你需要获取的配置 dataId
    group = 'DEFAULT_GROUP'  # 配置的分组，通常是 'DEFAULT_GROUP'
    try:
        # 获取指定 data_id 和 group 的配置
        config = client.get_config(data_id, group)
        yaml_config = yaml.safe_load(config)
        logger.info("成功获取 nacos配置!!!")
        return yaml_config
    except Exception as e:
        logger.error("获取配置失败: %s", e)

def send_lark_card_message(webhook_url, title, content_list, status, mentioned_list=None):
    """
    发送 Lark 卡片消息

    :param webhook_url: Lark 的 Webhook URL
    :param title: 卡片的标题
    :param content_list: 包含多个文本内容的列表
    :param status: 状态值，用于决定卡片的颜色
    :param mentioned_list: 要 @ 的用户 ID 列表
    :return: None
    """
    # 根据 status 来选择卡片颜色
    card_color = "red" if not status else "green"  # 如果 status 为 True，卡片颜色为绿色

    # 如果有指定要 @ 的用户，则将其作为单独一行添加
    if mentioned_list:
        content_list.append(f"<at id={mentioned_list}>@{mentioned_list}</at>")  # 新增一行专门用来 @ 用户
        print('content_list',content_list)

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

    # 发送请求
    try:
        response = requests.post(
            webhook_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(message_data)
        )

        # 输出结果
        if response.status_code == 200:
            logger.info("消息发送成功！")
        else:
            logger.error("发送失败，状态码: %d, 响应内容: %s", response.status_code, response.text)
    except Exception as e:
        logger.error("发送消息时发生错误: %s", e)
