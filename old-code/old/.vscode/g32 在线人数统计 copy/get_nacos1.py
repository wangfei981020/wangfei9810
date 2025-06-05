import requests
import json
import nacos
import yaml
import logging
# import time

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_gameroom_id_from_nacos():
    # NACOS_SERVER = 'nacos-headless.devops'  # 替换为你的 Nginx 域名
    NACOS_SERVER = 'infra-nacos.slleisure.com'  # 替换为你的 Nginx 域名
    # NACOS_PORT = 8848  # Nginx 配置的端口，实际是代理到 Nacos 服务的端口
    NACOS_PORT = 80  # Nginx 配置的端口，实际是代理到 Nacos 服务的端口
    NACOS_USERNAME = 'jenkins-pull'  # 替换为你的 Nacos 用户名
    NACOS_PASSWORD = '123456'  # 替换为你的 Nacos 密码
    namespace = 'devops'  # 替换为你创建的命名空间 ID
    data_id = 'players-exporter.yml'  # 替换为你需要获取的配置 dataId
    group = 'DEFAULT_GROUP'  # 配置的分组，通常是 'DEFAULT_GROUP'

    # 尝试第一次连接
    try:
        logger.info("尝试初始化 Nacos 客户端...")
        client = nacos.NacosClient(f"{NACOS_SERVER}:{NACOS_PORT}", namespace=namespace, username=NACOS_USERNAME, password=NACOS_PASSWORD)
        logger.info("成功初始化 Nacos 客户端！")
    except (requests.exceptions.RequestException, nacos.exception.NacosRequestException) as e:
        # 第一次连接失败后进行重试
        logger.error(f"初始化 Nacos 客户端失败: {e}")

    # 获取配置的 data_id 和 group

    # 获取指定 data_id 和 group 的配置
    config = client.get_config(data_id, group)
    yaml_config = yaml.safe_load(config)
    return yaml_config.get('project_info',[])

# get_lark_id_from_nacos()