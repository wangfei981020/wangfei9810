argocd manifests

```sh
# gitlabwebhook


# in g32-cluster
kubectl create namespace argocd
# crd resource
kubectl apply -k "https://github.com/argoproj/argo-cd/manifests/crds?ref=v2.6.7"


# in infra-cluster
# 先创建 appproj 和 repo 资源
kubectl apply -f project-g32-prod.yaml 
kubectl apply -f argocd-repositories.yaml
# 最后创建 apps 
kubectl apply -f app-of-apps-g32-prod.yaml 

```
