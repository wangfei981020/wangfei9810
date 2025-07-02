# Add repository
```
helm repo add grafana https://grafana.github.io/helm-charts
```


# Install chart
```
helm upgrade --install loki-distributed --namespace loki -f values-loki-dirstributed.yaml grafana/loki-distributed --version 0.80.1 --wait
helm upgrade --install loki-promtail -f values-promtail.yaml --namespace loki grafana/promtail --version 6.16.6 --wait
```


