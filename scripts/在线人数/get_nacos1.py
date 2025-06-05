import requests
import nacos
import yaml
import logging
import os
from typing import List, Dict, Any

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置项抽象化
NACOS_CONFIG = {
    # 'server': 'nacos-headless.devops',
    'server': 'infra-nacos.slleisure.com',
    # 'port': 8848,
    'port': 80,
    'username': 'jenkins-pull',
    'password': '123456',
    'namespace': 'devops',
    'data_id': 'players-exporter.yml',
    'group': 'DEFAULT_GROUP',
    # 构建缓存文件路径为相对路径 'nacos-data/snapshot/players-exporter.yml+DEFAULT_GROUP+devops'
    'cache_file': os.path.join('nacos-data', 'snapshot', 'players-exporter.yml+DEFAULT_GROUP+devops')  # 使用 os.path.join 来保证路径的跨平台兼容性
}

def load_yaml(file_path: str) -> Dict[str, Any]:
    """加载并解析 YAML 文件"""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def connect_to_nacos() -> nacos.NacosClient:
    """连接 Nacos 服务"""
    try:
        logger.info(f"尝试连接 Nacos 服务: {NACOS_CONFIG['server']}:{NACOS_CONFIG['port']}...")
        client = nacos.NacosClient(
            f"{NACOS_CONFIG['server']}:{NACOS_CONFIG['port']}",
            namespace=NACOS_CONFIG['namespace'],
            username=NACOS_CONFIG['username'],
            password=NACOS_CONFIG['password']
        )
        logger.info("成功连接 Nacos 服务！")
        return client
    except (requests.exceptions.RequestException, nacos.exception.NacosRequestException) as e:
        logger.error(f"初始化 Nacos 客户端失败: {e}")
        return None

def get_config_from_nacos(client: nacos.NacosClient) -> List[Dict[str, Any]]:
    """从 Nacos 获取配置"""
    try:
        logger.info("从 Nacos 获取配置...")
        config = client.get_config(NACOS_CONFIG['data_id'], NACOS_CONFIG['group'])
        yaml_config = yaml.safe_load(config)
        return yaml_config.get('project_info', [])
    except Exception as e:
        logger.error(f"从 Nacos 获取配置失败: {e}")
        return []

def get_config_from_cache() -> List[Dict[str, Any]]:
    """从本地缓存文件获取配置"""
    # 确保目录存在
    cache_dir = os.path.dirname(NACOS_CONFIG['cache_file'])
    if not os.path.exists(cache_dir):
        logger.error(f"缓存目录 {cache_dir} 不存在！")
        raise FileNotFoundError(f"缓存目录 {cache_dir} 不存在，无法继续操作！")

    if os.path.exists(NACOS_CONFIG['cache_file']):
        logger.info(f"从本地缓存文件 {NACOS_CONFIG['cache_file']} 读取配置...")
        load_yaml1 = load_yaml(NACOS_CONFIG['cache_file']).get('project_info', [])
        return load_yaml1
    else:
        logger.error(f"本地缓存文件 {NACOS_CONFIG['cache_file']} 不存在！")
        raise FileNotFoundError(f"缓存文件 {NACOS_CONFIG['cache_file']} 不存在，无法继续操作！")

def get_gameroom_id_from_nacos() -> List[Dict[str, Any]]:
    """获取 Nacos 配置，如果失败则读取本地缓存"""
    # 尝试连接 Nacos
    client = connect_to_nacos()

    if client:
        # 从 Nacos 获取配置
        project_info = get_config_from_nacos(client)
        if project_info:
            return project_info

    # 如果 Nacos 获取失败，读取本地缓存
    return get_config_from_cache()


