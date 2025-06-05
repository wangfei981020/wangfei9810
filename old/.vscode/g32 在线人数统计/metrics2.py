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
            return None

    def _process_game_data(self, project_config: dict) -> List[dict]:
        project_name = project_config.get('project')
        response = self._send_request(
            project_config.get('method'),
            project_config.get('url')
        )

        if not response or not response.get('data'):
            return []

        # 构建基础数据结构
        base_entries = []
        for game_config in project_config.get('game', []):
            game_id = game_config['gameId']['value']
            print('game_id',game_id)
            for room_config in game_config['gameId'].get('gameRoomIds', []):
                print('room_config',room_config)
                entry = {
                    'project': project_name,
                    'vid': game_id,
                    'gmtype': room_config['value'],
                    room_config['roomId']: room_config['value'],
                    'players': 0
                }
                base_entries.append(entry)

        # 更新在线人数
        for data_item in response.get('data', []):
            print('data_item',data_item)
            room_id = str(data_item.get('gameRoomId'))
            online = data_item.get('online', 0)
            print('online',online)
            # print('base_entries',base_entries)
            for entry in base_entries:
                for key in entry:
                    # print('key',key)
                    # print('ev_id',entry)
                    # print('room_id',room_id)
                    # print('entry_key',entry.keys())
                    if str(key) == room_id:
                        # print('1111',room_id)
                        entry['players'] = online
                        break

        # 过滤数字键值
        return base_entries 
        # return [
        #     {k: v for k, v in entry.items() if not k.isdigit()}
        #     for entry in base_entries
        # ]
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
            # print('item',item)
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
                results.extend(self._process_game_data(project_config))
            else:
                results.extend(self._process_game_result(project_config))
        return results

# 使用示例
if __name__ == "__main__":
    processor = GameDataProcessor()
    nacos_config = get_gameroom_id_from_nacos()  # 假设这是获取配置的方法
    processed_data = processor.process_all_projects(nacos_config)
    logger.info(f"Processed data: {processed_data}")