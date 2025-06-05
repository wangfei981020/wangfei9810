import requests
from requests.auth import HTTPBasicAuth

url = "https://harbor.slleisure.com/api/v2.0/projects/{project_name}/repositories/{repository_name}/tags"
username = "cesar"
password = "Cesar-526"

# response = requests.get(url, auth=HTTPBasicAuth(username, password))
# tags = response.json()
# print(tags)
ProjectName = ['g18','g29','g32']


def get_harbor_project(project_name):
    for p in project_name:
        # print(p)
        project_url = 'https://harbor.slleisure.com/api/v2.0/projects/%s/repositories' % p 
        response = requests.get(project_url,auth=HTTPBasicAuth(username,password))
        # print(response)
        ImageName = response.json() 
        # for i in ImageName:
        #     # print(i['name'])
        tag_url = 'https://harbor.slleisure.com/api/v2.0/projects/g32/repositories/user-task-backend/artifacts?with_tag=true' 
        response1 = requests.get(tag_url,auth=HTTPBasicAuth(username,password))
        tag = response1.json()
        for t in tag:
            print(t['tags'])
        # print(tag['tags'])


def main():
    get_harbor_project(ProjectName)
main()

    

