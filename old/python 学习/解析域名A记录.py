import dns.resolver

# 定义字典来保存不同类型的记录
cname_records_dict = {}
a_records_dict = {}
unknown_records_dict = {}

# 从 config.txt 文件读取域名
with open('config.txt', 'r') as file:
    domains = [line.strip() for line in file if line.strip()]

# 查询每个域名的记录
for domain in domains:
    print(f"解析域名: {domain}")
    
    # 查询 CNAME 记录
    try:
        cname_records = dns.resolver.resolve(domain, 'CNAME')
        cname_records_list = [rdata.to_text() for rdata in cname_records]
        print(f"CNAME记录: {cname_records_list}")
        
        # 如果有 A 记录，先将它从 A 记录字典中删除
        if domain in a_records_dict:
            del a_records_dict[domain]
        
        # 将域名加入 CNAME 记录字典
        cname_records_dict[domain] = cname_records_list
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass
        # print("没有找到 CNAME 记录")

    # 查询 A 记录（如果没有查询过 CNAME 记录，才继续查询 A 记录）
    if domain not in cname_records_dict:  # 只有没有 CNAME 记录时才查询 A 记录
        try:
            a_records = dns.resolver.resolve(domain, 'A')
            a_records_list = [rdata.to_text() for rdata in a_records]
            print(f"A记录: {a_records_list}")
            # 将域名加入 A 记录字典
            a_records_dict[domain] = a_records_list
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
            print("没有找到 A 记录")
    
    # 如果该域名没有 A 记录和 CNAME 记录，将其加入到未知字典
    if domain not in a_records_dict and domain not in cname_records_dict:
        unknown_records_dict[domain] = "没有找到 A 或 CNAME 记录"
    
    print('-' * 40)

# 打印最终的字典
print("A记录字典:")
print(a_records_dict)
print("-" * 40)

print("CNAME记录字典:")
print(cname_records_dict)
print("-" * 40)

print("未知记录字典:")
print(unknown_records_dict)
