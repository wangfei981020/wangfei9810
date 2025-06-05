import re

# 示例日志条目
logs = [
    "2025/04/16 08:16:06.090 [   INFO] [notice_post.go:327]  Link-4f06fb5229e7486ea5be42a95ef93268 timestamp:2025-04-16 08:16:06.090 Round: GD001254160C2 GameRoomID: 500000001 Command: Bet_Confirm",
    "2025/04/16 08:16:06.090 [   INFO] [notice_post.go:327]  Link-4f06fb5229e7486ea5be42a95ef93268 timestamp:2025-04-16 08:16:06.090 Round:  GameRoomID: 500000001 Command: Bet_Confirm"
]

# 正则表达式，用于匹配 Round 值
pattern = r"Round:\s*([^\s]*)\s*GameRoomID"

# 遍历日志并查找 Round 为空的条目
for log in logs:
    match = re.search(pattern, log)
    if match and match.group(1):  # 如果 Round 值为空
        print("Round 值为空的日志条目:", match.group(1))
