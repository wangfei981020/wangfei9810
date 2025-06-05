import subprocess
from get_nacos import YamlConfig


def AnsiblePlaybook(project_hosts,host_list,deploy_version,s_path,dest_pat):
    # 定义 ansible-playbook 命令和参数
    command = [
    'ansible-playbook',
    '-i', f'/home/cesar/jenkins/{project_hosts}',  # 指定 inventory 文件
    '/home/cesar/jenkins/G20-game-client-h5.yaml',  # 指定 playbook 文件
    '-e', f'deploy_version={deploy_version}',  # 定义额外的变量
    '-e', f'host_list={host_list}',  # 定义主机组变量
    '-e', f'source_path={s_path}',  # 定义源路径变量
    '-e', f'deploy_path={dest_pat}',  # 定义目标路径变量
    '--diff',  # 显示 diff 输出
    ]

    try:
      # 使用 subprocess 执行 ansible-playbook 命令
     # result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
      print(command)

      # 打印标准输出和错误输出
      print("标准输出：")
      print(result.stdout)
    except subprocess.CalledProcessError as e:
      # 如果 ansible-playbook 执行失败，捕获异常并输出错误信息
      print(f"Ansible playbook 执行失败，错误代码：{e.returncode}")
      print(f"错误输出：{e.stderr}")
def write_config(file_name,data):
    with open(file_name, 'w') as file:
        file.write(data)

def rsync_config(nacos_config):
    if nacos_config.get('rsync_config') is not None:
        for i in nacos_config.get('rsync_config'):
            try:
                if nacos_config.get(i) is not None:
                    write_config(i,nacos_config.get(i))
                else:
                    raise ValueError(f"键 '{i}' 存在，但值为 None")
            except KeyError as e:
                    # 如果键 i 不在 nacos_config 中，会抛出 KeyError
                   print(f"缺少同步配置文件: 键 '{e}' 不存在于配置中")
                   sys.exit(1)  # 退出程序，1 表示异常退出
        #print('11111',nacos_config['rsync_config'])
        #print(type(nacos_config['rsync_config']))
    else:
        print(nacos_config['rsync_config'],'kkk')

def main():
    nacos_config=YamlConfig()
    print(nacos_config)
    rsync_config(nacos_config)
    s_path = nacos_config['source_path']
    dest_path = nacos_config['deploy_path']
    project_hosts='g20-uat-hosts'
    host_list='g20-uat-game-client-h5-test'
    deploy_version='uat-0.1.0.134'
    # 项目host文件，主机列表，版本号，源目录，目标目录
    #AnsiblePlaybook(project_hosts,host_list,deploy_version,s_path,dest_path)

main()
#print(YamlConfig())