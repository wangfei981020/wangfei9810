import yaml
import requests
import warnings
from typing import List, Dict, Any


class Metrics:
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    def __config(self) -> List[Dict[str, Any]]:
        """加载配置文件"""
        with open("config.yml", "r") as f:
            return yaml.safe_load(f)

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

    def __parse_values(self, data: Dict[str, Any], project: str) -> List[Dict[str, Any]]:
        """解析API返回的数据"""
        values = []

        # 处理 data 字段
        if "data" in data and data["data"] is not None:
            values.extend(
                {
                    "project": project,
                    "vid": item.get("gameRoomId", "0"),
                    "gmtype": item.get("gameId", "0"),
                    "players": item.get("online", "0"),
                }
                for item in data["data"]
            )
        elif "data" in data:
            values.append(
                {
                    "project": project,
                    "vid": "0",
                    "gmtype": "0",
                    "players": "0",
                }
            )

        # 处理 result 字段
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
        print(values)
        return values

    def run(self) -> List[Dict[str, Any]]:
        """运行并获取所有项目的指标数据"""
        results = []
        for config in self.__config():
            method = config.get("method")
            project = config.get("project")
            url = config.get("url")

            if not all([method, project, url]):
                print(f"Invalid config: {config}")
                continue

            data = self.__fetch_data(method, url)
            if not data:
                continue

            values = self.__parse_values(data, project)
            if values:
                results.extend(values)

        return results

