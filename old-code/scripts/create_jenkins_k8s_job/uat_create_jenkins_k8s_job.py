import re
import jenkins
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import yaml
import logging
from typing import List, Dict
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 控制台颜色
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'

class Config:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.jenkins = self.config['jenkins']
        self.harbor = self.config['harbor']

class HarborClient:
    def __init__(self, config: Config):
        self.config = config.harbor
        self.auth = HTTPBasicAuth(self.config['username'], self.config['password'])
        
    def get_repositories(self, project_name: str) -> List[str]:
        page = 1
        size = 10
        all_repositories = []
        
        while True:
            try:
                project_url = f"{self.config['url']}/api/v2.0/projects/{project_name}/repositories?page={page}&size={size}"
                print('project_url',project_url)
                response = requests.get(project_url, auth=self.auth)
                response.raise_for_status()
                
                repositories = response.json()
                if not repositories:
                    break
                    
                for repo in repositories:
                    image_name = repo['name'].split('/', 1)[1]
                    logging.info(f'Found image: {image_name}')
                    all_repositories.append(image_name)
                        
                page += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"获取Harbor仓库失败: {e}")
                break
        all_repositories = ['e-color-game-server-backend'] 
        return all_repositories

class JenkinsManager:
    def __init__(self, config: Config):
        self.config = config.jenkins
        self.server = self._connect_jenkins()
        
    def _connect_jenkins(self) -> jenkins.Jenkins:
        jenkins_env = f"jenkins_{self.config['env']}"
        jenkins_url = self.config[jenkins_env]
        return jenkins.Jenkins(
            jenkins_url,
            username=self.config['username'],
            password=self.config['password']
        )
        
    def get_view_jobs(self) -> List[Dict]:
        try:
            return self.server._get_view_jobs(self.config['view_name'])
        except jenkins.JenkinsException as e:
            logging.error(f"获取视图任务失败: {e}")
            return []
            
    def create_jobs(self, repositories: List[str]) -> None:
        try:
            config_xml = self._get_source_job_config()
            existing_jobs = [job['name'] for job in self.get_view_jobs()]
            
            for repo_name in repositories:
                self._process_single_job(repo_name, config_xml, existing_jobs)
                
        except Exception as e:
            logging.error(f"创建任务失败: {e}")
            
    def _get_source_job_config(self) -> str:
        return self.server.get_job_config(self.config['source_job_name']).replace('&quot;', '"')
        
    def _process_single_job(self, repo_name: str, config_xml: str, existing_jobs: List[str]) -> None:
        # new_job_name = f"k8s-{self.config['project_name']}_{repo_name}"
        new_job_name = f"k8s-{self.config['project_name']}_{repo_name}"
        print('new_job_name', new_job_name)
        
        if new_job_name in existing_jobs:
            logging.warning(f"{YELLOW}{new_job_name} job 已存在，跳过创建此项目{RESET}")
            return
            
        modified_config = self._modify_job_config(config_xml, repo_name)
        self._create_and_add_to_view(new_job_name, modified_config)
        
    def _modify_job_config(self, config_xml: str, repo_name: str) -> str:
        replacements = {
            r'def projectName = "(.+?)"': f'def projectName = "{self.config["project_name"]}"',
            r'def repoName = "(.+?)"': f'def repoName = "{repo_name}"',
            rf'proj="g29-{self.config["env"]}"': f'proj="{self.config["project_name"]}-{self.config["env"]}"'
        }
        
        if self.config['env'] == 'prod':
            replacements[r'cd /data/k8s/g29-prod-deployment'] = \
                f'cd /data/k8s/{self.config["project_name"]}-{self.config["env"]}-deployment'
                
        for pattern, replacement in replacements.items():
            config_xml = re.sub(pattern, replacement, config_xml)
            
        return config_xml
        
    def _create_and_add_to_view(self, job_name: str, config_xml: str) -> None:
        try:
            self.server.create_job(job_name, config_xml)
            self._add_job_to_view(job_name)
            logging.info(f"{GREEN}视图 {self.config['view_name']} 已成功更新，添加了job {job_name}.{RESET}")
        except jenkins.JenkinsException as e:
            logging.error(f"创建或添加任务失败: {e}")
            
    def _add_job_to_view(self, job_name: str) -> None:
        view_config = self.server.get_view_config(self.config['view_name'])
        view_root = ET.fromstring(view_config)
        job_names = view_root.find('jobNames')
        new_job_element = ET.Element('string')
        new_job_element.text = job_name
        job_names.append(new_job_element)
        
        self.server.reconfig_view(
            self.config['view_name'],
            ET.tostring(view_root, encoding='utf-8').decode('utf-8')
        )

def main():
    try:
        # 获取当前脚本所在目录
        current_dir = Path(__file__).parent
        config_path = current_dir / 'create_config.yaml'
        config = Config(str(config_path))
        
        # 获取Harbor仓库列表
        harbor_client = HarborClient(config)
        repositories = harbor_client.get_repositories(config.jenkins['project_name'])
        
        # # 创建Jenkins任务
        jenkins_manager = JenkinsManager(config)
        jenkins_manager.create_jobs(repositories)
        
    except Exception as e:
        logging.error(f"程序执行失败: {e}")

if __name__ == "__main__":
    main()