import yaml
import datetime
from typing import List, Dict
import whois
import os


def delete_old_data(config_with_old_data_file: str = "config_with_data.yml", start_time=datetime.time(3, 0), end_time=datetime.time(3, 10)) -> bool:
    """ 删除旧数据配置文件（config_with_data.yml） """
    now = datetime.datetime.now().time()
    if start_time <= now <= end_time:
        print(f"现在是执行 {config_with_old_data_file} 删除的时间范围。")
        if os.path.exists(config_with_old_data_file):
            try:
                os.remove(config_with_old_data_file)
                print(f"{config_with_old_data_file} 已成功删除。")
                return True
            except Exception as e:
                print(f"删除文件时发生错误: {e}")
                return False
        else:
            print(f"{config_with_old_data_file} 不存在，无法删除。")
    else:
        print(f"当前时间不在执行删除的时间范围内。")
    return False


def get_remaining_days(expiration_date: str, transform_fmt="%Y-%m-%d %H:%M:%S") -> int:
    """ 获取域名剩余的天数 """
    expiration_date_obj = datetime.datetime.strptime(expiration_date, transform_fmt)
    today = datetime.datetime.today()
    remaining_time = expiration_date_obj - today
    return remaining_time.days


def get_domain_info(domain_name: str, output_fmt="%Y-%m-%d %H:%M:%S") -> Dict[str, str]:
    """ 获取域名的详细信息 """
    try:
        domain_info = whois.query(domain_name)
        print(f"正在检查 {domain_name}, 其注册商为 {domain_info.registrar}")
        issuer = domain_info.registrar or "未知"
        expiration_date = domain_info.expiration_date
        if expiration_date:
            expiration_date = expiration_date[0] if isinstance(expiration_date, list) else expiration_date
            readable_expiration_date = expiration_date.strftime(output_fmt)
            return {
                "Domain": domain_name,
                "Issuer": issuer.strip(),
                "End_time": readable_expiration_date,
            }
        return {
            "Domain": domain_name,
            "Issuer": issuer.strip(),
            "End_time": "Information not available",
        }
    except Exception as e:
        print(f"查询域名 {domain_name} 时发生错误: {e}")
        return {
            "Domain": domain_name,
            "Issuer": "信息不可用",
            "End_time": "信息不可用",
        }


def load_existing_data_config(config_with_old_data_place: str) -> List[Dict]:
    """ 读取已有的配置数据文件 """
    if os.path.exists(config_with_old_data_place):
        with open(config_with_old_data_place, "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader) or []
    return []


def check_config_change(config_place: str = "config.yml", config_with_old_data_place: str = "config_with_data.yml") -> (List[str], List[Dict]):
    """ 检查新配置与旧配置之间的差异 """
    # with open(config_place, "r") as config_file:
    with open('d:\code\scripts\域名到期监控\config.yml', "r") as config_file:
        config_info = yaml.load(config_file, Loader=yaml.FullLoader)
    new_domains = set(config_info.get("domains", []))

    existing_data = load_existing_data_config(config_with_old_data_place)
    existing_domains = {data["Domain"] for data in existing_data}

    domain_differences = list(new_domains - existing_domains)
    intersection_data = [data for data in existing_data if data["Domain"] in new_domains]

    return domain_differences, intersection_data


def update_data(config_place: str = "config.yml", config_with_old_data_place: str = "config_with_data.yml", output_fmt="%Y-%m-%d %H:%M:%S") -> List[Dict]:
    """ 更新配置文件，合并新旧数据 """
    if delete_old_data(config_with_old_data_place):
        print("删除旧配置文件成功。")

    domain_differences, intersection_data = check_config_change(config_place, config_with_old_data_place)
    final_data_config = intersection_data

    for domain_name in domain_differences:
        result = get_domain_info(domain_name, output_fmt)
        if result["Issuer"] != "信息不可用":
            final_data_config.append(result)

    # 保存合并后的数据
    with open(config_with_old_data_place, "w") as config_data_file:
        yaml.dump(final_data_config, config_data_file, default_flow_style=False)

    return final_data_config
