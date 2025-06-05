import requests
import json
import yaml

# 读取 YAML 文件，根据 name 获取对应的 at_id
def get_lark_id_from_nacos(name):
    try:
        with open('at_ids.yaml', 'r') as file:
            at_ids = yaml.safe_load(file)
            print(at_ids.get(name))
        return at_ids.get(name)
    except FileNotFoundError:
        print("YAML 文件未找到，请检查路径")
        return None
    except yaml.YAMLError as e:
        print(f"读取 YAML 文件时发生错误: {e}")
        return None

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
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(message_data)
    )

    # 输出结果
    if response.status_code == 200:
        print("消息发送成功！")
    else:
        print(f"发送失败，状态码: {response.status_code}, 响应内容: {response.text}")
