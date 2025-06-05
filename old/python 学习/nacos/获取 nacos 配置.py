# http://nacos.uat-jenkins.com/

import nacos
import yaml

def YamlConfig():
    # Nginx 域名和端口（反向代理）
    # NACOS_SERVER = 'nacos.uat-jenkins.com'  # 替换为你的 Nginx 域名
    NACOS_SERVER = 'infra-nacos.slleisure.com'  # 替换为你的 Nginx 域名
    NACOS_PORT = 80                       # Nginx 配置的端口，实际是代理到 Nacos 服务的端口



    # Nacos 登录账号和密码
    NACOS_USERNAME = 'pull'  # 替换为你的 Nacos 用户名
    NACOS_PASSWORD = '123456'  # 替换为你的 Nacos 密码
    # 初始化 Nacos 客户端，指定命名空间（如果有的话）
    namespace = 'public'  # 替换为你创建的命名空间 ID
    client = nacos.NacosClient(f"{NACOS_SERVER}:{NACOS_PORT}", namespace=namespace,username=NACOS_USERNAME,password=NACOS_PASSWORD)

    # 获取配置的 data_id 和 group
    data_id = 'test'  # 替换为你需要获取的配置 dataId
    group = 'DEFAULT_GROUP'      # 配置的分组，通常是 'DEFAULT_GROUP'

    try:
        # 获取指定 data_id 和 group 的配置
        config = client.get_config(data_id, group)
        yaml_config = yaml.safe_load(config)
        # print("获取的配置:", config)
            # 打印解析后的 YAML 配置
        # print("\n解析后的配置:")
        print(yaml_config)
        return yaml_config
    except Exception as e:
        print("获取配置失败:", e)

def main():
    YamlConfig()

main()
