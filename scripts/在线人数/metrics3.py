import yaml
import requests
import warnings
import logging
import time
import json
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


    # def _send_request(self, method: str, url: str, data: dict = None) -> Optional[dict]:
    def _send_request(self, method: str, url: str, data=None) -> Optional[dict]:
        try:
            # merged_headers = {**self.session.headers, **(headers or {})}
            if data is None:
                response = self.session.request(method, url, timeout=(1, 1))
            else:
                print('1111',url)
                self.session.headers.update({"Content-Type": "application/json"})
                response = self.session.request(method, url, json=data, timeout=(1, 1))
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

    def _get_custom_datas(self, p_data) -> List[dict]:
        """根据项目名生成自定义 Header"""
        h = {}
        if not p_data is None:
            timestamp = int(time.time())
            for i in p_data:
                for k,v in i.items():
                    if k == "timestamp":
                        h[k] = int(timestamp)
                    else:
                        h[k] = v
            return h
        return None

    def _process_game_result(self, project_config: dict) -> List[dict]:
        project_name = project_config.get('project')
        p_data = project_config.get('datas')
        custom_datas = self._get_custom_datas(p_data)
        response = self._send_request(
            project_config.get('method'),
            project_config.get('url'),
            custom_datas
        )

        base_entries = []  
        num = 0
        if not response or not response.get('result'):
            data_dict = response.get('body')
            if data_dict:
                num += 1 
                vid = data_dict.get("vid") if data_dict.get("vid") else data_dict.get("vid")
                gmtype = data_dict.get("gameType") if data_dict.get("gameType") else data_dict.get("gmtype")
                base_entries.append({
                    "project": project_name,
                    "vid": vid,
                    "gmtype": gmtype,
                    "players": data_dict.get("onlinePlayerCount", 0),
                })
                return base_entries
            return []
        print('response.get',response.get('result'),'proiject',project_name)
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
            if project_config.get('project') in ('g33', 'ppu'):
                response = self._send_request(
                    project_config.get('method'),
                    project_config.get('url')
                )
                if not response or response.get('code') != '0000':
                    logger.error(f"Skipping g33 project {project_config.get('project')} due to request failure.")
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