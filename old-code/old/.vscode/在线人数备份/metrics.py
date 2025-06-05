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
        headers = {
            "Accept": "application/json",
        }
        try:
            response = requests.request(
                method, url, headers=headers, timeout=(1, 1), verify=False
            )
            if response.status_code != 200:
                return _values
            for i in response.json()["result"]:
                i["project"] = project
                if project == 'g20':
                    i["vid"] = i["id"]
                    i["gmtype"] = i["gameType"]

                if project == 'g23':
                    i["vid"] = i["id"]
                    i["gmtype"] = i["gameType"]
                    
                _values.append(i)
            print(_values)
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
