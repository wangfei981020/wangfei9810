import yaml

# 读取配置文件
def read_config():
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
        print(config)
        return config
read_config()


docker build -t code_monitor:latest .
docker run -d -p 9108:9108 --name code_monitor code_monitor:latest 
docker stop code_monitor 
docker rm code_monitor 
docker rmi code_monitor 
curl 127.0.0.1:9108/metrics
gunicorn -c config.py --access-logfile --error-logfile app:app 
gunicorn -c config.py app:app 

gunicorn -w 4 --access-logfile - --error-logfile - app:app
{"code":"1354","msg":"Transaction failed."}


docker build -t flink-cdc:latest .
docker run -d --name flink-jobmanager \
  -e JOB_MANAGER_RPC_ADDRESS=flink-jobmanager \
  -p 8081:8081 \
  flink-cdc:latest jobmanager

docker tag SOURCE_IMAGE[:TAG] harbor.slleisure.com/demo/REPOSITORY[:TAG]

docker tag flink-cdc:latest harbor.slleisure.com/demo/flink-cdc:latest
docker push harbor.slleisure.com/demo/flink-cdc:latest



docker build -t jenkins_update_job_monitor:v8 .
docker run -d -p 8088:8088 -p 5000:5000 --name jenkins_update_job_monitor jenkins_update_job_monitor:v1 
docker stop jenkins_update_job_monitor 
docker rm jenkins_update_job_monitor 
docker rmi jenkins_update_job_monitor 

docker build -t jenkins_update_job_monitor:v8 .
docker tag jenkins_update_job_monitor:v7 harbor.slleisure.com/env/jenkins_update_job_monitor:v7
docker push harbor.slleisure.com/env/jenkins_update_job_monitor:v7


docker build -t online_users_monitor:v13 .
docker run -d -p 8088:8088 -p 8089:8089 --name online_users_monitor  online_users_monitor:v3 
docker stop online_users_monitor 
docker rm online_users_monitor 
docker rmi online_users_monitor 

docker tag online_users_monitor:v13 harbor.slleisure.com/env/online_users_monitor:v13
docker push harbor.slleisure.com/env/online_users_monitor:v13

online-users-monitor

online-users

helm upgrade -i online-users-monitor . -n online-users
helm upgrade -i online-users-monitor . -f values.yaml -n online-users
helm uninstall online-users-monitor -n online-users



docker build -t centersvr:v13 .
docker run --name centersvr  centersvr:v3 sleep 36000
docker tag centersvr:v13 harbor.slleisure.com/env/centersvr:v13
docker push harbor.slleisure.com/env/centersvr:v13



docker build -t harbor.slleisure.com/env/update-jenkins-k8s-job:v9 .
docker push harbor.slleisure.com/env/update-jenkins-k8s-job:v9


docker build -t code_monitor_uat:v3 .
docker run -d -p 9110:9110 --name code_monitor_uat code_monitor_uat:v3
docker stop code_monitor 
docker rm code_monitor 
docker rmi code_monitor 
curl 127.0.0.1:9110/metrics
gunicorn -c config.py --access-logfile --error-logfile app:app 
gunicorn -c config.py app:app 


docker build -t code_monitor:v3 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v3

docker build -t code_monitor:v5 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v5


gunicorn -w 4 --access-logfile - --error-logfile - app:app
{"code":"1354","msg":"Transaction failed."}

docker build -t harbor.slleisure.com/env/players-exporter:v10 .
docker push harbor.slleisure.com/env/players-exporter:v10 .

docker tag e-color-game-frontend:latest harbor.slleisure.com/g35/e-color-game-frontend:20250221193510-01
docker push harbor.slleisure.com/g35/e-color-game-frontend:20250221193510-01
docker run -d --name ecolor-frontend ecolor-frontend:20250221180910-01 sleep 3600


docker load -i  e-color-game-server-backend.tar
docker tag e-color-game-server-backend:latest harbor.slleisure.com/g35/e-color-game-server-backend:20250226173910-01
docker push harbor.slleisure.com/g35/e-color-game-server-backend:20250226173910-01


docker build -t jenkins_update_job_monitor:v8 .
docker tag jenkins_update_job_monitor:v7 harbor.slleisure.com/env/jenkins_update_job_monitor:v7
docker push harbor.slleisure.com/env/jenkins_update_job_monitor:v7

docker build -t code_monitor:v6 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v6

docker build -t code_monitor:v7 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v7


docker build -t harbor.slleisure.com/env/players-exporter:v11 .
docker push harbor.slleisure.com/env/players-exporter:v11



docker build -t code_monitor:v8 .
docker run -d -p 9108:9108 --name code_monitor_prod code_monitor:v8