import requests
from requests.auth import HTTPBasicAuth

url = "https://harbor.slleisure.com/api/v2.0/projects/{project_name}/repositories/{repository_name}/tags"
username = "cesar"
password = "Cesar-526"



def get_harbor_project(project_name):
    page = 1
    size = 10
    all_repositories = []
    while True:
        project_url = 'https://harbor.slleisure.com/api/v2.0/projects/%s/repositories?page=%s&size=%s' % (ProjectName,page,size)
        response = requests.get(project_url,auth=HTTPBasicAuth(username,password))
        if response.status_code != 200:
            print("Error:", response.status_code)
            break
        repositories = response.json()
        if not repositories:
            break
        for i in repositories:
            image_name = i['name'].split('/',1)[1]
            all_repositories.append(image_name)
        page += 1


    print(f"Total repositories fetched: {len(all_repositories)}")
    print(all_repositories)
    return all_repositories



def main():
    get_harbor_project(ProjectName)
main()