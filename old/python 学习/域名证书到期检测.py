import dns.resolver

def get_dns_records(domain):
    a_records = []
    cname_records = []
    
    try:
        # 获取 A 记录（域名的 IP 地址）
        a_answers = dns.resolver.resolve(domain, 'A')
        for rdata in a_answers:
            a_records.append(rdata.to_text())
        
        # 获取 CNAME 记录（别名）
        cname_answers = dns.resolver.resolve(domain, 'CNAME')
        for rdata in cname_answers:
            cname_records.append(rdata.to_text())
        
    except dns.resolver.NoAnswer:
        print(f"没有找到 {domain} 的 A 或 CNAME 记录")
    except dns.resolver.NXDOMAIN:
        print(f"域名 {domain} 不存在")
    except Exception as e:
        print(f"查询 DNS 记录时发生错误: {e}")
    
    return a_records, cname_records

# 示例：获取域名的 A 记录和 CNAME 记录
domain = "g19-uat.com"
a_records, cname_records = get_dns_records(domain)

print(f"{domain} 的 A 记录（IP 地址）: {a_records}")
print(f"{domain} 的 CNAME 记录（别名）: {cname_records}")
