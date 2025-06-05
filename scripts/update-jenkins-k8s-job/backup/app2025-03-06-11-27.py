import json
from logs_info import setup_logging
from flask import Flask, request, jsonify
from jenkins_build import trigger_jenkins_build
from lark_message import send_lark_card_message, get_lark_id_from_nacos

# 设置日志
logger = setup_logging()

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
        status = data.get('status')
        nacos_info = get_lark_id_from_nacos()
        
        # Lark Webhook URL
        lark_webhook_url = nacos_info['lark_info']['lark_webhook_url']

        # 设置标题 
        if status == "green":
            title = "✅✅✅服务更新成功通知" 
            card_color = "green"
        elif status == "red":
            title = "❌❌❌服务更新失败通知" 
            card_color = "red"
        elif status == "orange":
            title = "⚠⚠⚠当前更新版本和之前版本相同,没有变化!!!" 
            card_color = "orange"
        else:
            title = "⚠⚠⚠服务启动已超过五分钟,请手动查看服务启动状态!!!" 
            card_color = "yellow"

        # 内容列表
        content_list = [
            f"Name: {name_value}",
            f"Namespace: {namespace}",
            f"Container: {container}",
            f"Version: {version}",
            f"UptimeTime: {uptime}",
        ]

        # 获取 at_id 根据 name 参数
        lark_names = nacos_info['lark_info']['lark_id']
        at_id = lark_names.get(name_value,[])
        if at_id != []:
            mentioned_list = at_id  # 如果找到对应的 at_id，则加入 mentioned_list
        else:
            logger.warning("This user has no Lark information yet, user: %s", name_value)
            mentioned_list = None  # 如果没有找到 at_id，则不执行 @ 操作

        
        # 调用函数发送卡片消息
        send_lark_card_message(lark_webhook_url, title, card_color,content_list, mentioned_list)
        
        return jsonify({"message": "Lark 卡片消息已发送!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/trigger_jenkins_build', methods=['POST'])
def trigger_jenkins_build_route():
    try:
        nacos_info = get_lark_id_from_nacos()
        # 从 POST 请求中获取 JSON 数据
        data = request.get_json()

        # 获取传递的参数
        job_name = data.get('jobname')

        if not job_name:
            return jsonify({"error": "missing parameter 'jobname'"}), 400

        # 调用 jenkins_build.py 中的函数来触发 Jenkins 构建
        jenkins_url = nacos_info['jenkins_info']['jenkins_url']
        jenkins_username = nacos_info['jenkins_info']['jenkins_username']
        jenkins_api_token = nacos_info['jenkins_info']['jenkins_api_token']
        result = trigger_jenkins_build(job_name, jenkins_url,jenkins_username,jenkins_api_token)

        # 返回成功响应
        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)