import ssl
import socket
from datetime import datetime


def get_certificate_info(domain: str, port: int = 443):
    """
    获取域名的证书信息，包括到期时间和签发机构。

    :param domain: 要监控的域名
    :param port: HTTPS 端口，默认为 443
    :return: 包含到期时间和签发机构的字典
    """
    context = ssl.create_default_context()
    with socket.create_connection((domain, port)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

            # 解析证书到期时间
            expiry_date_str = cert['notAfter']
            expiry_date = datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')

            # 解析签发机构信息
            # issuer = dict((key, value) for (key, value) in cert['issuer'])
            # issuer_org = issuer.get('organizationName', 'Unknown Issuer')

            # issuer = dict(x[0] for x in cert['issuer'])
            issuer = dict(x[0] for x in cert['issuer'])
            issuer_org = issuer.get('organizationName', 'Unknown Issuer')

            return {
                'expiry_date': expiry_date,
                'issuer': issuer_org
            }


def monitor_certificate(domain: str, days_threshold: int = 30):
    """
    监控证书到期时间并打印提醒。

    :param domain: 要监控的域名
    :param days_threshold: 提醒阈值，剩余多少天时触发提醒
    """
    try:
        cert_info = get_certificate_info(domain)
        expiry_date = cert_info['expiry_date']
        issuer = cert_info['issuer']

        days_left = (expiry_date - datetime.utcnow()).days
        if days_left <= days_threshold:
            print(f"[警告] 域名 {domain} 的证书将在 {days_left} 天后到期 "
                  f"(到期日期: {expiry_date}, 签发机构: {issuer})")
        else:
            print(f"[正常] 域名 {domain} 的证书剩余有效期 {days_left} 天 "
                  f"(到期日期: {expiry_date}, 签发机构: {issuer})")
    except Exception as e:
        print(f"[错误] 无法检查域名 {domain} 的证书: {e}")


# 示例：对多个域名监控
if __name__ == "__main__":
    domains_to_monitor = ["agent-web-p.g09uat.com", "goproxy.g20-uat.com","anchor-web.g20-uat.com"]
    for domain in domains_to_monitor:
        monitor_certificate(domain, days_threshold=30)



