import requests
import json
import argparse

def send_lark_card_message(webhook_url, title, content_list, status):
    """
    发送 Lark 卡片消息

    :param webhook_url: Lark 的 Webhook URL
    :param title: 卡片的标题
    :param content_list: 包含多个文本内容的列表
    :param status: 状态值，用于决定卡片的颜色
    :return: None
    """
    # 根据 status 来选择卡片颜色
    card_color = "red" if not status else "green"  # 如果 status 为 True，卡片颜色为绿色

    # 卡片消息内容
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
    print("状态码:", response.status_code)
    print("响应内容:", response.text)

    if response.status_code == 200:
        print("消息发送成功！")
    else:
        print(f"发送失败，状态码: {response.status_code}, 响应内容: {response.text}")


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="发送 Lark 卡片消息")
    parser.add_argument("name", help="Name 参数")
    parser.add_argument("namespace", help="Namespace 参数")
    parser.add_argument("container", help="Container 参数")
    parser.add_argument("version", help="Version 参数")
    parser.add_argument("uptime", help="UpdateTime 参数")
    parser.add_argument("--status", type=bool, default=False, help="状态值，决定卡片颜色，默认为 True (绿色)")

    # 解析命令行参数
    args = parser.parse_args()

    # 示例调用
    lark_webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/9084aa91-d958-458d-baf3-c923ab253592"
    title = "服务更新通知"
    content_list = [
        f"Name: {args.name}",
        f"Namespace: {args.namespace}",
        f"Container: {args.container}",
        f"Version: {args.version}",
        f"UptimeTime: {args.uptime}"
    ]
    
    # 调用函数发送卡片消息
    send_lark_card_message(lark_webhook_url, title, content_list, args.status)

# 调用 main 函数
if __name__ == "__main__":
    main()
