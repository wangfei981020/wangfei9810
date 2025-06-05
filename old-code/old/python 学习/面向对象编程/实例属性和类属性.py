class Student(object):
    count = 0  # 类属性，用于统计学生人数

    def __init__(self, name):
        self.name = name
        Student.count += 1  # 每创建一个实例，count 自动增加

# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Lisa')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)  # 输出学生人数
            print('测试通过!')


{
  "@source": [
    "10.195.2.27"
  ],
  "@timestamp": [
    "2024-10-19T05:01:27.000Z"
  ],
  "agent.ephemeral_id": [
    "1c366035-0844-4698-a8c3-2c5588857bfe"
  ],
  "agent.hostname": [
    "G20_nginx-01"
  ],
  "agent.id": [
    "a325c6b1-ff3c-499d-b98f-a818bd83ecaf"
  ],
  "agent.name": [
    "G20_nginx-01"
  ],
  "agent.type": [
    "filebeat"
  ],
  "agent.version": [
    "8.8.2"
  ],
  "args": [
    "-"
  ],
  "cf_ipcountry": [
    "PH"
  ],
  "cf_ray": [
    "8d4e35d3bdb1ddc1-HKG"
  ],
  "client_real_ip": [
    "10.195.1.84"
  ],
  "device_type": [
    "Windows"
  ],
  "domain": [
    "gci-web.g20-prod.com"
  ],
  "ecs.version": [
    "8.0.0"
  ],
  "fields.environment_name": [
    "PROD"
  ],
  "fields.log_type": [
    "G20-gci-web-backend-access"
  ],
  "fields.product_name": [
    "G20"
  ],
  "host.name": [
    "G20_nginx-01"
  ],
  "hostname": [
    "g20_nginx-01"
  ],
  "http_user_agent": [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
  ],
  "https": [
    ""
  ],
  "input.type": [
    "log"
  ],
  "ip": [
    "156.59.233.150"
  ],
  "log.file.path": [
    "/data/wwwlogs/gci-web-backend-access.log"
  ],
  "log.offset": [
    3886955808
  ],
  "referer": [
    "https://gci-web.g20-prod.com/h5/index.html?param=vltpXpBeyJnYW1lVHlwZSI6IkM2NjE4NiIsImV4Z2FtZSI6InRydWUiLCJhZ2VudCI6ImVDNjlXYWxsZXQiLCJpbkFwcCI6bnVsbCwicHJvY2VkdXJlX2lkIjpudWxsLCJjaGFubmVsIjoiaDUiLCJkbSI6Imh0dHBzOi8vYmluZ29wbHVzLmNvbS9pbmRleCIsInBpZCI6IkM2OSIsImRlbW8iOm51bGwsImdhbWVsZXZlbCI6bnVsbCwidG9wQ2RuVXJscyI6bnVsbCwicGFzc3dvcmQiOiI3MTJmMzQwNmJhMjM3Nzc0NDBiNzg0Yjk0ZjVmMDQxMSIsImxhbmciOiJFTiIsInZpcCI6bnVsbCwid2ViQXBwIjpudWxsLCJ6aGlibyI6InRydWUiLCJkZWZhdWx0U3R5bGUiOm51bGwsImNkblVybCI6bnVsbCwic2Vzc2lvbl9pZCI6bnVsbCwidmlkZW9JRCI6IlJCMDEiLCJ0cmFjZVVVSUQiOiIxYzcwMGVkNC03YTU4LTRlY2UtOGIxZi1hZDBkNTFjZWVlNDkiLCJleHB0aW1lc3RhbXAiOjE3MjkzMTc2ODY1OTQsInJvb21pZCI6bnVsbCwidG9rZW4iOm51bGwsInRvcFByb3h5TGluZXMiOm51bGwsInN6dSI6ImFhIiwic2l0ZSI6ImJwIiwiemhpYm9lZ2FtZSI6InRydWUiLCJyZWRpcmVjdF91cmwiOm51bGwsInVzZXJuYW1lIjoiYmluZ29wbHVzaWJ5MHdmIn0lEehUzW"
  ],
  "request": [
    "/h5/src/import-map.fc960.json"
  ],
  "request_method": [
    "GET"
  ],
  "responsetime": [
    0
  ],
  "scheme": [
    "http"
  ],
  "size": [
    46
  ],
  "status": [
    200
  ],
  "upstreamaddr": [
    "-"
  ],
  "upstreamtime": [
    "-"
  ],
  "_id": "cHUmo5IBhifJpbqw4xT3",
  "_index": ".ds-nginx-g20-gci-web-backend-access-g20-prod-filebeat-2024.10.17-000001",
  "_score": null
}