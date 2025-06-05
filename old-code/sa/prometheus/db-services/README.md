DolphinScheduler
```sh
# https://dolphinscheduler.apache.org/zh-cn/docs/3.2.2/guide/installation/kubernetes

export VERSION=3.2.1
helm pull oci://registry-1.docker.io/apache/dolphinscheduler-helm --version ${VERSION}
tar -xvf dolphinscheduler-helm-${VERSION}.tgz
cd dolphinscheduler-helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency update .
helm upgrade --install dolphinscheduler . -n db-services

kubectl apply -f vs.yaml
```
