from flask import Flask, request, jsonify
from lark_message import send_lark_card_message, get_lark_id_from_nacos

app = Flask(__name__)

@app.route('/send_lark_card', methods=['POST'])
def send_lark_card():
    try:
        # 从请求中获取 JSON 数据
        data = request.get_json()

        # 获取传递的参数
        name_value = data.get('name')
        namespace = data.get('namespace')
        container = data.get('container')
        version = data.get('version')
        uptime = data.get('uptime')
        status = data.get('status', False)
        other_build_user = data.get('other_build_user', "None")

        nacos_info = get_lark_id_from_nacos()
        # Lark Webhook URL
        #lark_webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/80a20ce1-0c68-47e3-9977-710ea0a5a3b1"
        # lark_webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/c21cdeb0-7247-41b5-8b98-2dfc83df3285"
        lark_webhook_url = nacos_info['lark_info']['lark_webhook_url']

        # 设置标题
        title = "服务更新成功通知" if status else "服务更新失败通知"
        
        # 判断 `other_build_user` 参数是否为 "None"，如果不为 "None" 则替换 `name_value`
        if other_build_user != "None":
            name_value = other_build_user  # 如果传入了 `other_build_user`，则使用它的值

        # 内容列表
        content_list = [
            f"Name: {name_value}",
            f"Namespace: {namespace}",
            f"Container: {container}",
            f"Version: {version}",
            f"UptimeTime: {uptime}",
        ]

        # 获取 at_id 根据 name 参数
        # at_id = get_lark_id_from_nacos(name_value)
        at_id = nacos_info['lark_info']['lark_id'][name_value]
        if at_id:
            mentioned_list = at_id  # 如果找到对应的 at_id，则加入 mentioned_list
        else:
            mentioned_list = None  # 如果没有找到 at_id，则不执行 @ 操作
        
        # 调用函数发送卡片消息
        send_lark_card_message(lark_webhook_url, title, content_list, status, mentioned_list)
        
        return jsonify({"message": "Lark 卡片消息已发送!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
