import jenkins
# import os

def trigger_jenkins_build(job_name, other_build_user,jenkins_url,jenkins_username,jenkins_api_token):
    try:
        # Jenkins 配置
        jenkins_url = jenkins_url
        username = jenkins_username
        api_token = jenkins_api_token

        # 创建 Jenkins server 客户端
        server = jenkins.Jenkins(jenkins_url, username=username, password=api_token)

        # 获取 Job 信息
        job_info = server.get_job_info(job_name)

        # 从 job_info 中提取 selected_value 的默认值
        selected_value = None
        for parameter_definition in job_info['actions'][0]['parameterDefinitions']:
            if parameter_definition['name'] == 'selected_value':
                selected_value = parameter_definition['defaultParameterValue']['value']
                break

        if not selected_value:
            raise ValueError("未找到 selected_value 参数")

        # 触发 Jenkins 构建
        params = {
            'selected_value': selected_value,
            'only_restart': False,
            'other_build_user': other_build_user  # 将传入的 other_build_user 参数添加到构建参数中
        }

        # 触发构建
        server.build_job(job_name, parameters=params)

        return f"已触发 Job: {job_name}, 默认最新版本是: {selected_value}, 构建用户是: {other_build_user}"

    except jenkins.JenkinsException as e:
        raise Exception(f"触发构建时出错: {str(e)}")
    except Exception as e:
        raise Exception(f"发生错误: {str(e)}")
