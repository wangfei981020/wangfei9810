import re
import jenkins
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth


projects = {'project_name': 'g32','env':'uat','jenkins_uat':'https://uat-jenkins.slleisure.com','jenkins_prod':'https://jk.slleisure.com'}
# 原有任务名称
# source_job_name = 'k8s-g29_analysis-admin-frontend' 
source_job_name = 'k8s-test_agent-api-backend-g32-test' 
# 目标视图的名称        
view_name = 'PPU-K8S-G32-GLI'
# view_name = 'G32-UAT'
def get_harbor_project(project_name):
    url = "https://harbor.slleisure.com/api/v2.0/projects/{project_name}/repositories/{repository_name}/tags"
    username = "cesar"
    password = "Cesar-526"
    page = 1
    size = 10
    all_repositories = []
    while True:
        project_url = 'https://harbor.slleisure.com/api/v2.0/projects/%s/repositories?page=%s&size=%s' % (project_name,page,size)
        response = requests.get(project_url,auth=HTTPBasicAuth(username,password))
        if response.status_code != 200:
            print("Error:", response.status_code)
            break
        repositories = response.json()
        if not repositories:
            break
        for i in repositories:
            image_name = i['name'].split('/',1)[1]
            print('image_name:',image_name)
            if "datatranssvr-backend" not in image_name :
                all_repositories.append(image_name)
        page += 1
    # all_repositories = ["g20-gci-web-backend"]
    return all_repositories


def jenkins_login():
    # Jenkins 服务器的 URL 和凭据
    # # UAT jenkins
    # jenkins_uat = 'https://uat-jenkins.slleisure.com'
    # # prod jenkins
    # jenkins_prod = 'https://jk.slleisure.com'
    username = 'cesar'
    password = 'cesar-526'
    jenkins_env = f'jenkins_{projects['env']}'
    jenkins_url = projects[jenkins_env]
    # print(jenkins_url)
    # 连接到 Jenkins
    server = jenkins.Jenkins(jenkins_url, username=username, password=password)
    return server

def get_view_jobs(view_name):
    server = jenkins_login()
    view = server._get_view_jobs(view_name) 
    return view

def create_jenkins_job():
    server = jenkins_login()
    config_xml = server.get_job_config(source_job_name)
    config_xml = config_xml.replace('&quot;','"')
    project_name = projects['project_name']
    harbor_reponame = get_harbor_project(project_name)
    for r_n in harbor_reponame:
        config_xml=re.sub(r'def projectName = "(.+?)"', f'def projectName = "{project_name}"', config_xml)
        config_xml = re.sub(r'def repoName = "(.+?)"', f'def repoName = "{r_n}"', config_xml)
        config_xml = re.sub(rf'proj="g29-{projects['env']}"', f'proj="{project_name}-{projects['env']}"', config_xml)
        if projects['env'] == 'prod':
            config_xml = re.sub(r'cd /data/k8s/g29-prod-deployment', f'cd /data/k8s/{project_name}-{projects['env']}-deployment', config_xml)
        print('------------------------------------------------------------')
        new_job_name = f'k8s-{projects['project_name']}_{r_n}'
        # print(new_job_name)
        # new_job_name = f'G32-{r_n}'
        # new_job_name = f'test-k8s-{projects['project_name']}_{r_n}'
        view_list = []
        YELLOW = '\033[93m'
        RESET = '\033[0m'
        GREEN = '\033[92m'
        # 创建新任务
        view = get_view_jobs(view_name)
        for i in view:
            view_list.append(i['name'])
        if  new_job_name in view_list:
            print(f'{YELLOW}{new_job_name} job 已存在，跳过创建此项目{RESET}')
        else:
            server.create_job(new_job_name, config_xml)
            view_jobs = [i['name'] for i in view]
            view_config = server.get_view_config(view_name)
            view_root = ET.fromstring(view_config)
            job_names = view_root.find('jobNames')
            new_job_element = ET.Element('string')
            new_job_element.text = new_job_name
            job_names.append(new_job_element)
            # 重新配置视图
            server.reconfig_view(view_name, ET.tostring(view_root, encoding='utf-8').decode('utf-8'))
            print(f'{GREEN}视图 {view_name} 已成功更新，添加了job {new_job_name}.{RESET}')

def main():
    create_jenkins_job()
main()