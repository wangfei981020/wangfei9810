import yaml
import requests
import warnings
import logging
from typing import List, Dict, Any
from get_nacos import get_gameroom_id_from_nacos

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def send_post_request(method, url):
    """发送HTTP请求并获取数据"""
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    headers = {"Accept": "application/json"}
    try:
        response = requests.request(method, url, headers=headers, timeout=(1, 1), verify=False)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return {}



def __parse_values(nacos_info):
    values = []
    default_g32_dict = {}
    default_g32_list = []
    default_ppu_dict = {}
    default_ppu_list = []

    for i in nacos_info:
        project_name = i.get('project')
        if project_name == 'g32':
            request_method = i.get('method')
            request_url = i.get('url')
            response = send_post_request(request_method,request_url)
            for j in i.get('game'):
                gameId = j.get('gameId')
                gameId_value = j['gameId']['value']
                for t in gameId.get('gameRoomIds'):
                    roomId_name = t.get('roomId')
                    roomId_value = t.get('value')
                    default_g32_dict['project'] = project_name  
                    default_g32_dict[roomId_name] = roomId_value
                    default_g32_dict['vid'] = gameId_value
                    default_g32_dict['gmtype'] = roomId_value
                    default_g32_dict['players'] = 0
                    default_g32_list.append(default_g32_dict)
                    default_g32_dict = {}

            try:
                if response.get('data',[]) != [] or response.get('data') != "None" or response.get('data') != "null":
                # if response.get('result',[]) != []:
                    for item in response.get('data'):
                        for d in default_g32_list:
                            request_gameRoomId = item.get('gameRoomId')
                            request_players = item.get('online')
                            if request_gameRoomId in d:
                                d['players'] = request_players
            except TypeError:
                print("Skipping non-iterable or None object.")
            for i in default_g32_list:
                filtered_dict = {k: v for k, v in i.items() if not k.isdigit()}
                values.append(filtered_dict)

        elif project_name == 'ppu':
            request_method = i.get('method')
            request_url = i.get('url')
            response = send_post_request(request_method,request_url)
            for j in i.get('game'):
                gameId = j.get('gameId')
                gameId_value = j['gameId']['value']
                for t in gameId.get('gameRoomIds'):
                    roomId_name = t.get('roomId')
                    roomId_value = t.get('value')
                    default_ppu_dict['project'] = project_name  
                    default_ppu_dict[roomId_name] = roomId_value
                    default_ppu_dict['vid'] = gameId_value
                    default_ppu_dict['gmtype'] = roomId_value
                    default_ppu_dict['players'] = 0
                    default_ppu_list.append(default_ppu_dict)
                    default_ppu_dict = {}
            try:
                if response.get('data',[]) != [] or response.get('data') != None or response.get('data') != null:
                # if response.get('result',[]) != []:
                    for item in response.get('data'):
                        for d in default_ppu_list:
                            request_gameRoomId = item.get('gameRoomId')
                            request_players = item.get('online')
                            if request_gameRoomId in d:
                                d['players'] = request_players
            except TypeError:
                print("Skipping non-iterable or None object.")

            for i in default_ppu_list:
                filtered_dict = {k: v for k, v in i.items() if not k.isdigit()}
                values.append(filtered_dict)
        else:
            request_method = i.get('method')
            request_url = i.get('url')
            response = send_post_request(request_method,request_url)
            if response.get('result',[]) != []:
                for item in response.get('result'):
                    if item.get("id", []) != []:
                        vid = item.get("id")
                    else:
                        vid = item.get("vid")
                    if item.get("gameType",[]) != []:
                        gmtype = item.get("gameType")
                    else:
                        gmtype = item.get("gmtype")
                    # values.append({
                    #     "project": project_name,
                    #     "vid": vid,
                    #     "gmtype": gmtype,
                    #     "players": item.get("players", "0000"),
                    # })
    print('values',values)
    return values

def run():
    nacos_info = get_gameroom_id_from_nacos()
    data = __parse_values(nacos_info)
    print('data',data)


run()