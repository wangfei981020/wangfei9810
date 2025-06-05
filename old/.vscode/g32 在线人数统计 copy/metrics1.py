import yaml
import requests
import warnings


class Metrics:
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    def __config(self):
        _config = None
        with open("config.yml", "r") as f:
            _config = yaml.safe_load(f)
        return _config

    def __values(self, method, project, url):
        _values = []
        data_dict = {}
        headers = {
            "Accept": "application/json",
        }
        try:
            response = requests.request(
                method, url, headers=headers, timeout=(1, 1), verify=False
            )
            if response.status_code != 200:
                return _values
            print('555', response.json())
            for key, value in response.json().items():  # 使用 items() 遍历字典的键值对
                if key == 'data':
                    if value != None:
                        for i in value:
                            data_dict['project'] = project
                            data_dict["vid"] = i["gameRoomId"]
                            data_dict["gmtype"] = i["gameId"]   
                            data_dict["players"] = i["online"]  
                            _values.append(data_dict) 
                            print('777',data_dict)                        
                    else:
                        data_dict['project'] = project
                        data_dict["vid"] = "0"
                        data_dict["gmtype"] = "0"
                        data_dict["players"] = "0"
                        _values.append(data_dict)  
                if key == 'result':
                    for i in value:
                        i['project'] = project
                        if project == 'g20':
                            i["vid"] = i["id"]
                            i["gmtype"] = i["gameType"]
                        if project == "g23":
                            i["vid"] = i["id"]
                            i["gmtype"] = i["gameType"]   
                        _values.append(i)                        

            print('_values',_values)
        except Exception as e:
            print(e)
        return _values

    def run(self):
        _data = []
        for cf in self.__config():
            _value = self.__values(cf["method"], cf["project"], cf["url"])
            if not _value:
                continue
            _data.append(_value)
        return _data
