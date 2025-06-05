import requests
import json
import time


timestamp = int(time.time())
print('当前时间戳: ',timestamp)
# 请求 URL
url = "https://gcp-dc-api.g22-prod.com/game/info?agent=eC69Wallet"

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 请求数据
data = {
    "timestamp": timestamp, 
    "productId": "C69", 
    "gameType": "BLRE", 
    "vid": "BL01"
}
print('data',data)

# 发送 POST 请求
# response = requests.post(url, headers=headers, data=json.dumps(data))
response = requests.post(url, headers=headers, json=data)
# response = requests.post(url, headers=headers)

# 输出响应结果
print(f"Status Code: {response.status_code}")
print("Response Body:", response.text)
