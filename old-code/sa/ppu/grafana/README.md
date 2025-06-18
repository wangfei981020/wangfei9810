grafana

```sh
helm upgrade --install infra-grafana . -f values.yaml -n monitoring


# create vs
kubectl apply -f vs.yaml
```
