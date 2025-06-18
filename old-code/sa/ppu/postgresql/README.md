### Add repository

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm repo update bitnami
```

### Install chart

```
$ helm upgrade --install --namespace db-services postgresql -f values.yaml bitnami/postgresql --create-namespace --wait
```

