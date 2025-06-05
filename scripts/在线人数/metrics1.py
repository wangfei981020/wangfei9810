import yaml
import requests
import warnings
import logging
from typing import List, Dict, Any, Optional
from get_nacos import get_gameroom_id_from_nacos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

class GameDataProcessor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self.session.verify = False

    def _send_request(self, method: str, url: str) -> Optional[dict]:
        try:
            response = self.session.request(method, url, timeout=(1, 1))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {str(e)}")
            # return []

    def _process_game_data(self, project_config: dict) -> List[dict]:
        project_name = project_config.get('project')
        response = self._send_request(
            project_config.get('method'),
            project_config.get('url')
        )

        # 如果 response 为 None 或 response.get('data') 为空，使用默认值
        if not response or not response.get('data'):
            # 使用默认值填充数据
            base_entries = []
            for game_config in project_config.get('game', []):
                game_id = game_config['gameId']['value']
                for room_config in game_config['gameId'].get('gameRoomIds', []):
                    entry = {
                        'project': project_name,
                        'vid': room_config['value'],
                        'gmtype': game_id,
                        room_config['roomId']: room_config['value'],
                        'players': 0  # 默认人数为 0
                    }
                    base_entries.append(entry)
            return base_entries  # 返回默认数据

        # 构建基础数据结构
        base_entries = []
        for game_config in project_config.get('game', []):
            game_id = game_config['gameId']['value']
            for room_config in game_config['gameId'].get('gameRoomIds', []):
                entry = {
                    'project': project_name,
                    'vid': room_config['value'],
                    'gmtype': game_id,
                    room_config['roomId']: room_config['value'],
                    'players': 0  # 默认人数为 0
                }
                base_entries.append(entry)

        # 更新在线人数
        for data_item in response.get('data', []):
            room_id = str(data_item.get('gameRoomId'))
            online = data_item.get('online', 0)
            for entry in base_entries:
                for key in entry:
                    if str(key) == room_id:
                        entry['players'] = online
                        break
        return [
            {k: v for k, v in entry.items() if not k.isdigit()}
            for entry in base_entries
        ]

    def _process_game_result(self, project_config: dict) -> List[dict]:
        project_name = project_config.get('project')
        response = self._send_request(
            project_config.get('method'),
            project_config.get('url')
        )
        if not response or not response.get('result'):
            return []
        base_entries = []  
        for item in response.get('result'):
            vid = item.get("id") if item.get("id") else item.get("vid")
            gmtype = item.get("gameType") if item.get("gameType") else item.get("gmtype")
            base_entries.append({
                "project": project_name,
                "vid": vid,
                "gmtype": gmtype,
                "players": item.get("players", 0),
            })
        return base_entries  # 返回构建好的数据

    def process_all_projects(self, nacos_config: List[dict]) -> List[dict]:
        results = []
        for project_config in nacos_config:
            if project_config.get('project') in ('g32', 'ppu'):
                response = self._send_request(
                    project_config.get('method'),
                    project_config.get('url')
                )
                if not response or response.get('code') != '0000':
                    logger.error(f"Skipping g32 project {project_config.get('project')} due to request failure.")
                    continue  # 跳过该项目的处理
                results.extend(self._process_game_data(project_config))
            else:
                results.extend(self._process_game_result(project_config))
        return results

    def run(self):
            nacos_config = get_gameroom_id_from_nacos()  # 假设这是获取配置的方法
            processed_data = self.process_all_projects(nacos_config)
            logger.info(f"Processed data: {processed_data}")
            return processed_data



processor = GameDataProcessor()
processor.run()