# ArgoCD Helm install

```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

Setup CRD's
```
kubectl apply -k "https://github.com/argoproj/argo-cd/manifests/crds?ref=v2.12.1"
```

```
helm upgrade --install --namespace argocd --create-namespace -f values.yaml argocd argo/argo-cd --version 2.12.0
```

# Download Argo CD CLI

https://argo-cd.readthedocs.io/en/stable/getting_started/#2-download-argo-cd-cli

For latest Linux version
```
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
```

# Authorization to perform admin actions

https://argo-cd.readthedocs.io/en/stable/getting_started/#4-login-using-the-cli

```
argocd login argocd.qa.ggp.htecoins.com --username admin --grpc-web
Password: 
'admin:login' logged in successfully
Context 'argocd.qa.ggp.htecoins.com' updated
```

# ArgoCD user management

View current users
```
argocd account list --grpc-web
```

Compare settings for installed argocd chart with your custom additions in values.yaml (here "5.29.1" is current chart number from "helm list -A" output)
```
helm -n argocd diff upgrade argocd argo/argo-cd --values values.yaml --version 5.29.1
```

Apply your changes in values.yaml
```
helm -n argocd upgrade argocd argo/argo-cd --values values.yaml --version 5.29.1
```

Set password for user accounts
```
argocd account update-password --account USERNAME1 --new-password PASSWORD1
argocd account update-password --account gitlabci --new-password PASSWORD2
```

Generate token for automation account (for GitlabCI ARGOCD_AUTH_TOKEN variable)
```
argocd account generate-token --account gitlabci --grpc-web
```


# Adding our platform infra repo to ArgoCD via CLI

First of all need to create new deploy token for git repo in https://gitlab.htecoins.com/infrastructure/ggp-k8s-platform/-/settings/repository with scope 'read_repository' and name 'argo_read_repository'. Note new password for token and update config if needed. Then apply yaml config.

```
kubectl apply -f argocd-repositories.yaml
```

# Creating new projects via CLI

https://argo-cd.readthedocs.io/en/stable/getting_started/#creating-apps-via-cli

Apply yaml files from https://gitlab.htecoins.com/infrastructure/ggp-k8s-platform/-/tree/main/argocd-apps/argocd-manifests one-by-one
```
kubectl apply -f project-ggp-common.yaml
kubectl apply -f project-ggp-games.yaml
kubectl apply -f project-ggp-services.yaml
```

# Apply app-of-apps applications for our main projects 

We're using app-of-apps pattern (umbrella charts) for our underlying apps: https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/#app-of-apps-pattern

```
kubectl apply -f app-of-apps-ggp-common.yaml
kubectl apply -f app-of-apps-ggp-games.yaml
kubectl apply -f app-of-apps-ggp-services.yaml
```
