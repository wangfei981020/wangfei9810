import re
import yaml
import jenkins
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth


# 读取配置文件
def read_config(filename='config.yaml'):
    with open(filename,'r',encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
    return data

# jenkins 登录
def jenkins_login():
    config_data = read_config()
    project_env = config_data['projects']['env']
    jenkins_env = f'jenkins_{project_env}'
    jenkins_url = config_data['projects'][jenkins_env]
    jenkins_user = config_data['projects']['username']
    jenkins_passwd = config_data['projects']['password']
    server = jenkins.Jenkins(jenkins_url, username=jenkins_user, password=jenkins_passwd)
    return server

# 获取 视图 job
def get_view_jobs(view_name):
    server = jenkins_login()
    view = server._get_view_jobs(view_name) 
    return view


def trim_string(input_string):
    # 检查字符串是否以大写字母 "G" 开头
    if input_string.startswith('G'):
        # 查找第一个 "-" 的位置
        dash_pos = input_string.find('-')
        
        # 如果找到了 "-"，则去掉第一个 "-" 之前的部分（包括 "-" 本身）
        if dash_pos != -1:
            return input_string[dash_pos + 1:]  # 截取从 "-" 后面开始的部分
    return input_string  # 如果不以 "G" 开头或没有 "-"，则返回原字符串

def remove_prefix_before_first_underscore(string):
    # 判断字符串中是否包含下划线
    if "_" in string:
        # 使用 split() 方法裁剪第一个下划线及其前面的部分
        return string.split('_', 1)[1]
    else:
        # 如果没有下划线，返回原始字符串
        return string

# 修改job 修改配置
def update_job_config():
    config_data = read_config()
    server = jenkins_login()
    view_name = config_data['projects']['view_name']
    view_job = get_view_jobs(view_name)
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    GREEN = '\033[92m'
    for j in view_job:
        # job_name = trim_string(j['name'])
        job_name = remove_prefix_before_first_underscore(j['name'])
        if j['name'] == 'G32-baccarat-server-backend-test':
            project_name = config_data['projects']['project_name']
            source_job_name = config_data['projects']['source_job_name']
            config_xml = server.get_job_config(source_job_name)
            config_xml = config_xml.replace('&quot;','"')
            config_xml=re.sub(r'def projectName = "(.+?)"', f'def projectName = "{project_name}"', config_xml)
            config_xml = re.sub(r'def repoName = "(.+?)"', f'def repoName = "{job_name}"', config_xml)
            proj = f'{config_data['projects']['project_name']}-{config_data['projects']['env']}'
            config_xml = re.sub(r'proj="(.+?)"', f'proj="{proj}"', config_xml)
            ## 解析 XML 字符串为 ElementTree 对象
            config_xml = ET.fromstring(config_xml)
            update_config_xml = updated_config_xml = ET.tostring(config_xml, encoding='utf-8').decode()
            # 更新 Job 配置
            server.reconfig_job(j['name'], updated_config_xml)
            print(f"{GREEN}Job '{j['name']}' updated successfully.{RESET}")

def main():
    update_job_config()
main()