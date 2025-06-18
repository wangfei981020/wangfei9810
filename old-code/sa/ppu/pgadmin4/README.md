### Add repository
```
$ helm repo add runix https://helm.runix.net/
$ helm repo update runix
```

### Install chart
```
$ helm upgrade --install --namespace db-services pgadmin4 -f values.yaml runix/pgadmin4 --create-namespace --version 1.14.6 --wait
$ kubectl apply -f pgadmin4-virtualservice.yaml
```