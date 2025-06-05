import yaml
import requests
import warnings
import logging
from get_nacos import get_gameroom_id_from_nacos
from typing import List, Dict, Any

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            logger.error(f"Request failed for {url}: {e}")
            # print(f"Request failed for {url}: {e}")
            return {}

    def __initialize_mappings(self, gameRoomId_mappings: List[Dict[str, Any]]) -> Dict[str, str]:
        """生成 gameRoomId 和 gameId 的映射字典"""
        gameRoomId_map = {}
        gameId_map = {}
        
        for items in gameRoomId_mappings:
            # 获取 gameRoomId 映射
            gameRoomId_list = items.get('gameRoomId', [])
            for item in gameRoomId_list:
                print('item',item)
                if 'name' in item and 'value' in item:
                    gameRoomId_map[item['name']] = item['value']

            # 获取 gameId 映射
            gameId_list = items.get('gameId', [])
            for item in gameId_list:
                if 'name' in item and 'value' in item:
                    gameId_map[item['name']] = item['value']
        # print('gameRoomId_map',gameRoomId_map)
        # print('gameId_map',gameId_map)
        return gameRoomId_map, gameId_map

    # def __parse_values(self, data: Dict[str, Any], project: str, gameRoomId_map: Dict[str, str], gameId_map: Dict[str, str]) -> List[Dict[str, Any]]:
    def __parse_values(self, data: Dict[str, Any], project: str, nacos_info) -> List[Dict[str, Any]]:
        """解析API返回的数据，并更新gameRoomId和gameId"""
        values = []
        nacos_game_info = []
        gameRoomId_map = {} 
        gameId_map = {}

        for i in nacos_info:
            if i.get('game') != None:
                game_info = i.get('game')
                nacos_game_info.append(game_info)
                for i in game_info:
                    # print('i',i)
                    # print('111')
                    gameId_map[i['gameId']['name']] = i['gameId']['value']
                    room_ids = i['gameId']['gameRoomIds']
                    for i in room_ids:
                        # print('222')
                        gameRoomId_map[i['roomId']] = i['value']
                        # gameId_map['game'] = gameRoomId_map
                        # gameRoomId_map = {} 

        # print('gameId_map',gameId_map)  
        # print('gameRoomId_map',gameRoomId_map)  
        if "data" in data and data["data"] is not None:
            for item in data["data"]:
                # 更新 gameRoomId 和 gameId
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

        # 如果没有 'data' 字段，则返回默认值
        elif "data" in data:
            values.append({
                "project": project,
                "vid": "0",
                "gmtype": "0",
                "players": "0",
            })

        # 处理 'result' 字段
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
        keys_to_delete = []
        player_info = []
        num = 0
        if project == "ppu" or project == "g32":
            for key,value in gameRoomId_map.items():
                for i in values:
                    if value == i['vid']:
                        keys_to_delete.append(key)
                    # print('i',i['vid'])
            for key in keys_to_delete:
                print('delete_key',key)
                del gameRoomId_map[key]
            # print('gameRoomId_map_delete',gameRoomId_map)
            for i in nacos_info:
                if i.get('game') != None:
                    game_info = i.get('game')
                    nacos_game_info.append(game_info)
                    for i in game_info:
                        # print('i',i)
                        # print('111')
                        # gameId_map[i['gameId']['name']] = i['gameId']['value']
                        room_ids = i['gameId']['gameRoomIds']
                        # print('room_ids',room_ids)
                        num += 1
                        gameID = i['gameId']['value']
                        for i in room_ids:
                            # print('222')
                            gameRoomId = i['value']
                            player_info.append({
                                "project": project,
                                "vid": gameRoomId,
                                "gmtype": gameID,
                                "players": "0",
                        })
            for i in player_info:
                # print('i',i)

                values.append({
                    "project": i.get("project","0"),
                    "vid": i.get("vid", "0"),
                    "gmtype": i.get("gmtype", "0"),
                    "players": i.get("players", "0"),
                })

        # print('player_info',player_info)
        print('values',values)
        # print('num',num)
        return values

    def run(self) -> List[Dict[str, Any]]:
        """运行并获取所有项目的指标数据"""
        results = []
        gameRoomId_mappings = get_gameroom_id_from_nacos()  # 获取 gameRoomId 的映射关系
        
        # 初始化映射字典
        # gameRoomId_map, gameId_map = self.__initialize_mappings(gameRoomId_mappings)
        # print('gameRoomId_map',gameRoomId_map)

        # 遍历每个项目配置并获取数据
        for config in gameRoomId_mappings:
            method = config.get("method")
            project = config.get("project")
            url = config.get("url")

            if not all([method, project, url]):
                print(f"Invalid config: {config}")
                continue

            # 获取并处理数据
            data = self.__fetch_data(method, url)
            if not data:
                continue

            # 使用映射字典解析返回的数据
            values = self.__parse_values(data, project, gameRoomId_mappings)
            if values:
                results.extend(values)

        return results

# Metrics().run()