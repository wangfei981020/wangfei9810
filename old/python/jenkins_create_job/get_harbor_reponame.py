import requests
from requests.auth import HTTPBasicAuth

url = "https://harbor.slleisure.com/api/v2.0/projects/{project_name}/repositories/{repository_name}/tags"
username = "cesar"
password = "Cesar-526"

ProjectName = ['g29']


def get_harbor_project(project_name):
    for p in project_name:
        project_url = 'https://harbor.slleisure.com/api/v2.0/projects/%s/repositories' % p 
        response = requests.get(project_url,auth=HTTPBasicAuth(username,password))
        # print(response)
        ImageName = response.json() 
        for i in ImageName:
            print(i['name'].split('/',1)[1])


def main():
    get_harbor_project(ProjectName)
main()