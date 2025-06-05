import whois
from datetime import datetime

# 记录域名的告警状态
alert_triggered = False  # 初始状态为没有触发告警

def get_domain_expiry(domain):
    # 获取域名的 WHOIS 信息
    w = whois.whois(domain)

    # 获取域名的到期时间
    expiration_date = w.expiration_date

    # 如果返回的到期时间是一个列表（有些 WHOIS 返回的是多个日期）
    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    # 如果有到期时间，返回该时间
    if expiration_date:
        return expiration_date
    else:
        return None

def days_until_expiry(domain):
    # 获取域名的到期时间
    expiry_date = get_domain_expiry(domain)
    
    if expiry_date:
        # 获取当前日期时间
        current_date = datetime.now()

        # 计算到期时间和当前时间的差异（以天为单位）
        delta = expiry_date - current_date

        # 返回剩余天数
        return delta.days
    else:
        return None

def check_expiry_alert(domain):
    global alert_triggered  # 引用全局变量

    # 获取域名的剩余天数
    days_left = days_until_expiry(domain)
    
    if days_left is None:
        print(f"无法获取域名 {domain} 的到期时间。")
    elif days_left <= 15:
        # 剩余天数小于等于 15 天，触发告警
        if not alert_triggered:
            print(f"域名 {domain} 剩余 {days_left} 天，触发告警！")
            alert_triggered = True  # 标记已经触发过告警
        else:
            print(f"域名 {domain} 剩余 {days_left} 天，告警已触发，无需再次告警。")
    elif days_left > 15:
        # 剩余天数大于 15 天，恢复告警
        if alert_triggered:
            print(f"域名 {domain} 剩余 {days_left} 天，恢复告警。")
            alert_triggered = False  # 恢复告警，更新状态
        else:
            print(f"域名 {domain} 剩余 {days_left} 天，不需要恢复告警。")

# 示例：查询域名的剩余天数并进行告警检查
domain = "g19-uat.com"
check_expiry_alert(domain)

# 如果续费或其他原因导致到期时间更新，可以再运行一次检查
# 检查域名到期时间的变化
check_expiry_alert(domain)
