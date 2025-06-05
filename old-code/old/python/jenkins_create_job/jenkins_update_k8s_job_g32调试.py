import re
import yaml
import jenkins
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth


# 读取配置文件
def read_config(filename='config.yaml'):
    """读取并返回配置文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except FileNotFoundError:
        print(f"Error: The config file '{filename}' was not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file {filename}. {e}")
        raise


# jenkins 登录
def jenkins_login(config_data):
    """使用配置数据登录 Jenkins 并返回 Jenkins server 实例"""
    project_env = config_data['projects']['env']
    jenkins_env = f'jenkins_{project_env}'
    jenkins_url = config_data['projects'].get(jenkins_env)
    jenkins_user = config_data['projects'].get('username')
    jenkins_passwd = config_data['projects'].get('password')
    
    if not all([jenkins_url, jenkins_user, jenkins_passwd]):
        print("Error: Missing Jenkins configuration in the config file.")
        raise ValueError("Jenkins URL, username, or password not found in the config.")
    
    server = jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_passwd)
    return server


def get_view_jobs(server, view_name):
    """获取指定视图中的所有作业"""
    try:
        # 关键修复：明确指定view_name参数
        return server.get_jobs(view_name=view_name)
    except jenkins.JenkinsException as e:
        print(f"Error: 无法获取视图 '{view_name}' 的作业列表. {e}")
        # 添加调试信息
        all_views = server.get_views()
        print(f"可用视图列表: {[v['name'] for v in all_views]}")
        raise


# 裁剪字符串，去掉下划线前面的部分
def remove_prefix_before_first_underscore(string):
    """裁剪字符串，去掉第一个下划线及其前面的部分"""
    if "_" in string:
        return string.split('_', 1)[1]
    return string

# 已大写G开头的JOB
def trim_string(input_string):
    # 检查字符串是否以大写字母 "G" 开头
    if input_string.startswith('G'):
        # 查找第一个 "-" 的位置
        dash_pos = input_string.find('-')
        
        # 如果找到了 "-"，则去掉第一个 "-" 之前的部分（包括 "-" 本身）
        if dash_pos != -1:
            return input_string[dash_pos + 1:]  # 截取从 "-" 后面开始的部分
    return input_string  # 如果不以 "G" 开头或没有 "-"，则返回原字符串

# 更新 Jenkins 作业配置
def update_job_config(config_data):
    """更新 Jenkins 作业配置"""
    server = jenkins_login(config_data)
    view_name = config_data['projects']['view_name']
    print('view_name:',view_name)
    
    try:
        view_jobs = get_view_jobs(server, view_name)
    except Exception as e:
        print(f"Error: Unable to fetch jobs from view '{view_name}'. {e}")
        return

    YELLOW = '\033[93m'
    RESET = '\033[0m'
    GREEN = '\033[92m'
    
    for j in view_jobs:
        job_name= j['name']
        if 'G32-' in j['name'] and j['name'] != 'G32-批量更新勾选job到最新版本':
        # if 'G32-' in j['name'] and j['name'] != 'G32-批量更新勾选job到最新版本' and j['name']!= 'G32-gitlab-test' and j['name'] != 'G32-restart-test' and j['name'] != 'G32-baccarat-server-backend-test' and j['name'] != 'G32-批量更新勾选job到最新版本-test':
            print('zzz',j['name'])
            project_name = config_data['projects']['project_name']
            source_job_name = config_data['projects']['source_job_name']
            try:
                config_xml = server.get_job_config(source_job_name)
                config_xml = config_xml.replace('&quot;', '"')
                # 更新项目名称和仓库名称
                config_xml = re.sub(r'def projectName = "(.+?)"', f'def projectName = "{project_name}"', config_xml)
                config_xml = re.sub(r'def repoName = "(.+?)"', f'def repoName = "{job_name}"', config_xml)
                proj = f'{project_name}-{config_data["projects"]["env"]}'
                config_xml = re.sub(r'proj="(.+?)"', f'proj="{proj}"', config_xml)


                # 解析并更新 XML 配置
                config_xml_tree = ET.fromstring(config_xml)
                updated_config_xml = ET.tostring(config_xml_tree, encoding='utf-8').decode()

                # 更新作业配置
                server.reconfig_job(j['name'], updated_config_xml)
                print(f"{GREEN}Job '{j['name']}' updated successfully.{RESET}")
            except jenkins.JenkinsException as e:
                print(f"Error: Failed to update job '{j['name']}'. {e}")


def main():
    config_data = read_config()  # 读取配置文件
    update_job_config(config_data)  # 更新 Jenkins 作业配置

if __name__ == "__main__":
    main()
