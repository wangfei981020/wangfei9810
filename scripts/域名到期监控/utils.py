import yaml
import datetime
from collections import namedtuple
from typing import List, Dict
import whois
import os


def delete_old_data(
    config_with_old_data_file: str = "config_with_data.yml",
    start_time=datetime.time(3, 0),
    end_time=datetime.time(3, 10),
):
    # 獲取當前時間
    now = datetime.datetime.now().time()
    # 定義計劃的執行時間範圍（03:00到03:10）
    start_time = start_time
    end_time = end_time

    # 檢查是否在計劃的時間範圍內
    if start_time <= now <= end_time:
        print(f"現在是執行{config_with_old_data_file}刪除的時間範圍。")
        if os.path.exists(config_with_old_data_file):
            try:
                os.remove(config_with_old_data_file)
                print(f"{config_with_old_data_file} 已成功刪除。")
                return True
            except Exception as e:
                print(f"刪除文件時發生錯誤: {e}")
                return False
        else:
            print(f"{config_with_old_data_file} 不存在，無需刪除。")
            return False
    else:
        print(f"現在不是執行{config_with_old_data_file}刪除的時間範圍。")
        return False


def get_remaining_days(expiration_date: str, transform_fmt="%Y-%m-%d %H:%M:%S"):
    expiration_date_obj = datetime.datetime.strptime(expiration_date, transform_fmt)
    today = datetime.datetime.today()
    remaining_time = expiration_date_obj - today
    return remaining_time.days


def get_domain_info(domain_name, output_fmt="%Y-%m-%d %H:%M:%S"):
    try:
        domain_info = whois.query(domain_name)
        print(
            f"present is checking {domain_name} , its info is {domain_info.registrar}"
        )

        issuer = domain_info.registrar
        expiration_date = domain_info.expiration_date
        if issuer:
            issuer = issuer.strip()
        if expiration_date:
            expiration_date = (
                expiration_date[0]
                if isinstance(expiration_date, list)
                else expiration_date
            )
            readable_expiration_date = expiration_date.strftime(output_fmt)
            domain_result = {
                "Domain": domain_name,
                "Issuer": issuer,
                "End_time": readable_expiration_date,
            }
            print(domain_result)
            return domain_result

    except Exception as e:
        print(f"we have {e} error")
        return {
            "Domain": domain_name,
            "Issuer": "Information not available",
            "End_time": "Information not available",
            "Expiration_days_left": "Information not available",
        }


def load_existing_data_config(config_with_old_data_place: str) -> List[dict]:
    """
    讀取舊的配置數據文件，如果文件存在，提取已檢查過的域名列表和相關數據。

    Args:
        config_with_old_data_place (str): 舊的配置數據文件的路徑。

    Returns:
        Tuple[List[str], List[dict]]: 由已檢查過的域名列表和相關數據構成的元組。
    """
    if os.path.exists(config_with_old_data_place):
        with open(config_with_old_data_place, "r") as data_config_file:
            data_config_info = yaml.load(data_config_file, Loader=yaml.FullLoader)
            domain_already_check_list = [
                domain["Domain"] for domain in data_config_info
            ]
    else:
        # 如果文件不存在，初始化空的已檢查過的域名列表和相關數據
        domain_already_check_list = []
        data_config_info = []

    return domain_already_check_list, data_config_info


# 這個函數用於檢查配置是否發生了變化，並返回兩個列表：
# - domain_differences_list: 包含在新配置中但不在舊配置中的域名列表。
# - intersection_data_config_info_list: 包含在新配置和舊配置中都存在的域名的相關數據列表。
def check_config_change(
    config_place: str = "config.yml",
    config_with_old_data_place: str = "config_with_data.yml",
):
    # 讀取新配置文件
    with open(config_place, "r") as config_file:
        config_info = yaml.load(config_file, Loader=yaml.FullLoader)
    domain_list = config_info.get("domains", [])

    domain_already_check_list, data_config_info = load_existing_data_config(
        config_with_old_data_place
    )

    # 找出新配置中有但舊配置中沒有的域名
    domain_differences_list = list(set(domain_list) - set(domain_already_check_list))

    # 找出新配置和舊配置中都存在的域名，以及相關的數據
    domain_intersection_list = list(set(domain_list) & set(domain_already_check_list))
    intersection_data_config_info_list = [
        data for data in data_config_info if data["Domain"] in domain_intersection_list
    ]

    return domain_differences_list, intersection_data_config_info_list


# 這個函數用於更新配置文件，並返回最終的數據配置列表。
# 它根據域名的不同處將新數據添加到現有的數據中，如果某些域名的信息不可用，則會跳過它們。
def update_data(
    output_fmt="%Y-%m-%d %H:%M:%S",
    config_with_old_data_place: str = "config_with_data.yml",
) -> List[Dict]:
    delete_old_data_result = delete_old_data()
    # 使用上面的函數檢查配置的變化
    domain_differences_list, intersection_data_config_info_list = check_config_change()

    # 初始化最終的數據配置列表，它包含舊配置中的數據以及新配置中的不同處。
    final_data_config_list = intersection_data_config_info_list

    # 遍歷新配置中的不同域名，獲取其信息並添加到最終列表中。
    for domain_name in domain_differences_list:
        result = get_domain_info(domain_name, output_fmt=output_fmt)
        if result["Issuer"] == "Information not available" or result["Issuer"] is None:
            print(f"result {result} is either Information not available of None")
            continue
        final_data_config_list.append(result)

    # 更新配置文件（舊配置文件），將最終的數據配置列表寫入其中。
    with open(config_with_old_data_place, "w") as config_data_file:
        yaml.dump(final_data_config_list, config_data_file, default_flow_style=False)

    return final_data_config_list
