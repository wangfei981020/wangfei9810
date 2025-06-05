logging

## install
```sh
# repo
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# promtail
cd promtail
helm upgrade --install promtail . -f values.yaml -n logging

# loki
cd loki
helm upgrade --install loki . -f values.yaml -n logging
kubectl apply -f vs.yaml
```
