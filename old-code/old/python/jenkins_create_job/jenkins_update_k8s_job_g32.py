import re
import yaml
import jenkins
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
import requests


def read_config(filename='config.yaml'):
    """读取并返回配置文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: 配置文件 '{filename}' 不存在")
        raise
    except yaml.YAMLError as e:
        print(f"Error: YAML解析失败 {filename}. {e}")
        raise


def jenkins_login(config_data):
    """Jenkins登录验证，获取Crumb Token"""
    env = config_data['projects']['env']
    jenkins_env = f'jenkins_{env}'
    
    if not all(key in config_data['projects'] for key in [jenkins_env, 'username', 'password']):
        raise ValueError("Jenkins配置不完整")
    
    server_url = config_data['projects'][jenkins_env]
    username = config_data['projects']['username']
    password = config_data['projects']['password']
    
    # 使用请求获取Crumb Token
    auth = HTTPBasicAuth(username, password)
    crumb_url = f"{server_url}/crumbIssuer/api/json"
    response = requests.get(crumb_url, auth=auth)
    
    if response.status_code != 200:
        print(f"Error: 获取 Crumb Token 失败 {response.status_code}")
        raise ValueError("无法获取 Crumb Token")
    
    crumb_data = response.json()
    crumb = crumb_data['crumb']
    crumb_request_field = crumb_data['crumbRequestField']
    
    # 返回 Jenkins 实例和 crumb token
    server = jenkins.Jenkins(server_url, username=username, password=password)
    return server, crumb, crumb_request_field


def get_view_jobs(server, view_name):
    """获取指定视图中的所有作业"""
    try:
        return server.get_jobs(view_name=view_name)
    except jenkins.JenkinsException as e:
        print(f"Error: 无法获取视图 '{view_name}' 的作业列表. {e}")
        all_views = server.get_views()
        print(f"可用视图列表: {[v['name'] for v in all_views]}")
        raise


def trim_project_name(string):
    """裁剪字符串，去掉第一个下划线及其前面的部分"""
    if "_" in string:
        return string.split('_', 1)[1]
    return string


def update_job_config(config_data):
    """更新作业配置的核心逻辑"""
    server, crumb, crumb_request_field = jenkins_login(config_data)
    view_name = config_data['projects']['view_name']
    source_job = config_data['projects']['source_job_name']
    
    print(f"\n{'='*30}\n开始处理视图: {view_name}\n{'='*30}")
    
    try:
        jobs = get_view_jobs(server, view_name)
        print(f"发现 {len(jobs)} 个待处理作业")
    except Exception as e:
        print(f"终止: 无法获取作业列表 - {e}")
        return

    for job in jobs:
        original_name = job['name']
        
        # if original_name != "k8s-test_agent-api-backend-g101":
        if original_name == "k8s-testgli_agent-api-backend":
            exclude_list = ['G101GLI-批量更新勾选job到最新版本']
            if original_name in exclude_list:
                print(f"跳过排除作业: {original_name}")
                continue
            
            trimmed_name = trim_project_name(original_name)
            repoName = original_name.split('_')[1]
            
            try:
                config_xml = server.get_job_config(source_job)
                config_xml = config_xml.replace('&quot;', '"')
                
                # 替换关键参数
                replacements = {
                    r'def projectName = ".*?"': f'def projectName = "{config_data["projects"]["project_name"]}"',
                    r'def repoName = ".*?"': f'def repoName = "{repoName}"',
                    r'proj=".*?"': f'proj="{config_data["projects"]["project_name"]}-{config_data["projects"]["env"]}"'
                }
                
                for pattern, repl in replacements.items():
                    config_xml = re.sub(pattern, repl, config_xml)
                
                # 验证XML格式
                ET.fromstring(config_xml)
                
                # 更新作业配置时传递Crumb Token
                headers = {
                    crumb_request_field: crumb,
                    "Content-Type": "application/xml"
                }
                
                # 调用 Jenkins API 更新作业配置
                server_url = config_data['projects'][f'jenkins_{config_data["projects"]["env"]}']
                job_url = f"{server_url}/job/{original_name}/config.xml"
                
                # 使用 requests 来发送 POST 请求更新 Jenkins 配置
                response = requests.post(job_url, data=config_xml, headers=headers, auth=HTTPBasicAuth(config_data['projects']['username'], config_data['projects']['password']))
                
                if response.status_code == 200:
                    print(f"\033[92m成功更新: {original_name}\033[0m")
                else:
                    print(f"\033[91m配置更新失败: {original_name} - 状态码: {response.status_code}\033[0m")
            
            except jenkins.JenkinsException as e:
                print(f"\033[91m配置更新失败: {original_name} - {e}\033[0m")
            except ET.ParseError as e:
                print(f"\033[91mXML解析失败: {original_name} - {e}\033[0m")


def main():
    try:
        config = read_config()
        update_job_config(config)
    except Exception as e:
        print(f"\n\033[91m主流程异常: {e}\033[0m")


if __name__ == "__main__":
    main()
