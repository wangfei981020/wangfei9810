import yaml
import requests
import warnings
import logging
from typing import List, Dict, Any
from get_nacos import get_gameroom_id_from_nacos

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
            return {}

    def __parse_values(self, data: Dict[str, Any], project: str, nacos_info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """解析API返回的数据，并更新gameRoomId和gameId"""
        values = []
        gameRoomId_map = {}
        gameId_map = {}

        # 从nacos_info中提取gameRoomId和gameId的映射关系
        for i in nacos_info:
            if i.get('game') is not None:
                game_info = i.get('game')
                for game in game_info:
                    gameId_map[game['gameId']['name']] = game['gameId']['value']
                    for room in game['gameId']['gameRoomIds']:
                        gameRoomId_map[room['roomId']] = room['value']

        # 处理 'data' 字段
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

        # 处理特定项目的额外逻辑
        if project in ["ppu", "g32"]:
            keys_to_delete = [key for key, value in gameRoomId_map.items() if any(value == i['vid'] for i in values)]
            for key in keys_to_delete:
                del gameRoomId_map[key]

            # 添加未在values中的gameRoomId信息
            for i in nacos_info:
                if i.get('game') is not None:
                    game_info = i.get('game')
                    for game in game_info:
                        gameID = game['gameId']['value']
                        for room in game['gameId']['gameRoomIds']:
                            gameRoomId = room['value']
                            if gameRoomId not in [i['vid'] for i in values]:
                                values.append({
                                    "project": project,
                                    "vid": gameRoomId,
                                    "gmtype": gameID,
                                    "players": "0",
                                })

        logger.info(f"Parsed values for project {project}: {values}")
        return values

    def run(self) -> List[Dict[str, Any]]:
        """运行并获取所有项目的指标数据"""
        results = []
        gameRoomId_mappings = get_gameroom_id_from_nacos()  # 获取 gameRoomId 的映射关系

        # 遍历每个项目配置并获取数据
        for config in gameRoomId_mappings:
            method = config.get("method")
            project = config.get("project")
            url = config.get("url")

            if not all([method, project, url]):
                logger.warning(f"Invalid config: {config}")
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