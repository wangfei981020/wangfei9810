import re
import jenkins
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import yaml
import logging
from typing import List, Dict
from pathlib import Path
import colorlog

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 配置颜色格式
# log_format = "%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s"

# # 定义颜色格式
# color_formatter = colorlog.ColoredFormatter(
#     log_format,
#     log_colors={
#         "DEBUG": "cyan",
#         "INFO": "green",
#         "WARNING": "yellow",
#         "ERROR": "red",
#         "CRITICAL": "bold_red",
#     },
# )

# color_formatter = colorlog.ColoredFormatter(log_format)
# 控制台颜色
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'

class Config:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.jenkins = self.config['jenkins']

class ConfigFileReader:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def get_file(self) -> str:
        """
        读取并返回配置文件内容
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logging.info("成功读取配置文件内容")
            return content.splitlines()
        except Exception as e:
            logging.error(f"读取配置文件失败: {e}")
            return ""

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
            print('repositories',repositories)
            for repo_name in repositories:
                self._process_single_job(repo_name, config_xml, existing_jobs)
                
        except Exception as e:
            logging.error(f"创建任务失败: {e}")
            
    def _get_source_job_config(self) -> str:
        return self.server.get_job_config(self.config['source_job_name']).replace('&quot;', '"')
        
    def _process_single_job(self, repo_name: str, config_xml: str, existing_jobs: List[str]) -> None:
        new_job_name = f"{repo_name}"
        
        if new_job_name in existing_jobs:
            print(f"{YELLOW}{new_job_name} job 已存在，跳过创建此项目{RESET}")
            # logging.warning(f"{YELLOW}{new_job_name} job 已存在，跳过创建此项目{RESET}")
            return
            
        modified_config = self._modify_job_config(config_xml, repo_name)
        self._create_and_add_to_view(new_job_name, modified_config)
        
    def _modify_job_config(self, config_xml: str, repo_name: str) -> str:
        PROJECT_NAME = self.config["project_name"].upper()
        replacements = {
            r'<description>G01_activity</description>': f'<description>{repo_name}</description>',
            r'def fs = new File(.*)': f'def fs = new File("/data/vcs/{self.config["project_name"]}/tidb/{repo_name}")',
            r'<projectName>G01_template_vm_job</projectName>': f'<projectName>{repo_name}</projectName>',
            r'<projectFullName>G01_template_vm_job</projectFullName>': f'<projectFullName>{repo_name}</projectFullName>',
            rf'ansible-playbook /etc/ansible(.+?).yaml': f'ansible-playbook /etc/ansible/{PROJECT_NAME}/{repo_name}.yaml'
        }
   
        for pattern, replacement in replacements.items():
            config_xml = re.sub(pattern, replacement, config_xml)
        # print('config_xml',config_xml)        
            
        return config_xml
        
    def _create_and_add_to_view(self, job_name: str, config_xml: str) -> None:
        try:
            self.server.create_job(job_name, config_xml)
            self._add_job_to_view(job_name)
            # logging.info(f"{GREEN}视图 {self.config['view_name']} 已成功更新，添加了job {job_name}.{RESET}")
            print(f"{GREEN}视图 {self.config['view_name']} 已成功更新，添加了job {job_name}.{RESET}")
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
        config_task_path = current_dir / 'config_task.yaml'
        config = Config(str(config_path))
        # confi_task = Config(str(config_task_path))
        
        # 获取列表
        config_file = ConfigFileReader(config_task_path)
        repositories = ConfigFileReader.get_file(config_file)
        # print('repositories',repositories)
        
        # # # 创建Jenkins任务
        jenkins_manager = JenkinsManager(config)
        jenkins_manager.create_jobs(repositories)
        
    except Exception as e:
        logging.error(f"程序执行失败: {e}")

if __name__ == "__main__":
    main()