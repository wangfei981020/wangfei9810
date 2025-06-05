import os 
import yaml
import shutil
# from rueml import load, dump
import oyaml as yaml
# from yamlordereddictloader import Loader

project_dirs =  ['test-backend','test2-backend']
# 获取当前脚本目录
current_dir = os.path.dirname(os.path.abspath(__file__))

Chart_yaml = "Chart.yaml"
def create_dir():
    for d in project_dirs:
        # 创建新目录
        source_dir = os.path.join(current_dir, 'base-central-backend')
        new_directory = os.path.join(current_dir, d)
        if os.path.exists(new_directory):
            shutil.rmtree(new_directory)
        shutil.copytree(source_dir,new_directory)
        modify_chart_name(d,Chart_yaml)
        # os.makedirs(new_directory, exist_ok=True)

def get_data(dir,path_yaml):
    chat_yaml_file = os.path.join(current_dir, dir,path_yaml)
    print(chat_yaml_file)
    return chat_yaml_file

def modify_chart_name(file_dir,file_path):
    data = get_data(file_dir,file_path)
    lines = []
    
    with open(data,'r') as f:
        lines = f.readlines()
        print(lines)
    for i, line in enumerate(lines):
        if line.startswith('name'):
            lines[i] = f'name: {file_dir}\n'
            break
    with open(data,'w') as f:
        f.writelines(lines)


def main():
    create_dir()

main()
