import yaml
import requests
import warnings
from get_nacos import get_gameroom_id_from_nacos
from typing import List, Dict, Any


class Metrics:
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    def __fetch_data(self, method: str, url: str) -> Dict[str, Any]:
        """发送HTTP请求并获取数据"""
        headers = {"Accept": "application/json"}
        try:
            response = requests.request(method, url, headers=headers, timeout=(1, 1), verify=False)
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return {}

    def __parse_values(self, data: Dict[str, Any], project: str, gameRoomId_mappings: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """解析API返回的数据，并更新gameRoomId"""
        values = []
        
        # 生成一个映射字典，name -> value，忽略没有 name 的项
        gameRoomId_map = {}
        gameId_map = {}
        for items in gameRoomId_mappings:
            gameRoomId_list = items.get('gameRoomId',[])
            gameId_list = items.get('gameId',[])
            # print('items',items)
            if gameRoomId_list:
                for item in gameRoomId_list:
                    print('item',item)
                    if 'name' in item and 'value' in item:  # 检查 'name' 和 'value' 是否存在
                        gameRoomId_map[item['name']] = item['value']
            if gameId_list:
                for item in gameId_list:
                    if 'name' in item and 'value' in item:  # 检查 'name' 和 'value' 是否存在
                        gameId_map[item['name']] = item['value']

        # 处理 data 字段
        if "data" in data and data["data"] is not None:
            for item in data["data"]:
                # 如果 gameRoomId 的 name 存在映射字典中，就替换为对应的 value
                gameRoomId = item.get("gameRoomId", "")
                gameId = item.get("gameId", "")
                if gameRoomId in gameRoomId_map:
                    item["gameRoomId"] = gameRoomId_map[gameRoomId]
                if gameId in gameId_map:
                    item["gameId"] = gameId_map[gameId]
                values.append({
                    "project": project,
                    "vid": item.get("gameRoomId", "0"),
                    "gmtype": item.get("gameId", "0"),
                    "players": item.get("online", "0"),
                })

        elif "data" in data:
            values.append({
                "project": project,
                "vid": "0",
                "gmtype": "0",
                "players": "0",
            })

        if "result" in data:
            values.extend(
                {
                    "project": project,
                    "vid": item.get("id", "0"),
                    "gmtype": item.get("gameType", "0"),
                    **item,  # 保留原始数据中的其他字段
                }
                for item in data["result"]
            )

        print(values)  # 可以用于调试
        return values
    def run(self) -> List[Dict[str, Any]]:
        """运行并获取所有项目的指标数据"""
        results = []
        gameRoomId_mappings = get_gameroom_id_from_nacos()  # 获取 gameRoomId 的映射关系

        for config in gameRoomId_mappings:
            print('config', config)
            method = config.get("method")
            project = config.get("project")
            url = config.get("url")

            if not all([method, project, url]):
                print(f"Invalid config: {config}")
                continue

            data = self.__fetch_data(method, url)
            if not data:
                continue

            # 使用获取的映射数据
            values = self.__parse_values(data, project, gameRoomId_mappings)
            if values:
                results.extend(values)

        return results

# Metrics().run()