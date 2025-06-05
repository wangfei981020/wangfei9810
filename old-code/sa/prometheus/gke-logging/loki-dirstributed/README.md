# Add repository
```
helm repo add grafana https://grafana.github.io/helm-charts
```


# Install chart
```bash
# aws
helm upgrade --install loki-distributed --namespace loki -f aws-values-loki-dirstributed.yaml grafana/loki-distributed --version 0.80.1 --wait
# gcp
helm upgrade --install loki-distributed --namespace loki -f gcp-values-loki-dirstributed.yaml grafana/loki-distributed --version 0.80.1 --wait

helm upgrade --install loki-promtail -f values-promtail.yaml --namespace loki grafana/promtail --version 6.16.6 
```

