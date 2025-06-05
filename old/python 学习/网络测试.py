import requests
import time

# 设置目标 URL 和 POST 请求的 JSON 数据
url = "http://g01-gci-api-gcp-w.agqjapi.com/callback/userValidate"
headers = {'Content-Type': 'application/json'}
data = {"token": "002php1349"}

# 循环 100 次
for _ in range(3):
    # 发送 POST 请求
    response = requests.post(url, json=data, headers=headers)
    
    # 确保请求成功
    if response.status_code == 200:
        # 获取响应的 JSON 数据
        response_json = response.json()
        
        # 查找 'real' 字段并输出
        if 'real' in response_json:
            print(response_json['real'])
    else:
        print(f"请求失败，状态码：{response.status_code}")
    
    # 暂停 1 秒
    time.sleep(1)


