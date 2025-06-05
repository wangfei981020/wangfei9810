import re
import yaml
import jenkins
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth


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
    """Jenkins登录验证"""
    env = config_data['projects']['env']
    jenkins_env = f'jenkins_{env}'
    
    if not all(key in config_data['projects'] for key in [jenkins_env, 'username', 'password']):
        raise ValueError("Jenkins配置不完整")
    
    server = jenkins.Jenkins(
        config_data['projects'][jenkins_env],
        username=config_data['projects']['username'],
        password=config_data['projects']['password']
    )
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


def trim_project_name(name):
    """处理G开头的项目名称"""
    if name.startswith('G') and '-' in name:
        return name.split('-', 1)[1]
    return name


def update_job_config(config_data):
    """更新作业配置的核心逻辑"""
    server = jenkins_login(config_data)
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
        # print(f"\n处理作业: {original_name}")
        if original_name != "G32-baccarat-resource-test":
        # if original_name == "G32-baccarat-resource":
        # 跳过排除列表
            exclude_list = ['G32-批量更新勾选job到最新版本']
            if original_name in exclude_list:
                print(f"跳过排除作业: {original_name}")
                continue
            
                    # 名称转换
            trimmed_name = trim_project_name(original_name)
            # print(f"转换后名称: {trimmed_name}")
            try:
                # 获取配置模板
                config_xml = server.get_job_config(source_job)
                config_xml = config_xml.replace('&quot;', '"')
                
                # 替换关键参数
                replacements = {
                    r'def projectName = ".*?"': f'def projectName = "{config_data["projects"]["project_name"]}"',
                    r'def repoName = ".*?"': f'def repoName = "{trimmed_name}"',
                    r'proj=".*?"': f'proj="{config_data["projects"]["project_name"]}-{config_data["projects"]["env"]}"'
                }
                
                for pattern, repl in replacements.items():
                    config_xml = re.sub(pattern, repl, config_xml)
                    
                # 验证XML格式
                ET.fromstring(config_xml)
                # print(config_xml)
                
                # 更新配置
                server.reconfig_job(original_name, config_xml)
                print(f"\033[92m成功更新: {original_name}\033[0m")
                
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