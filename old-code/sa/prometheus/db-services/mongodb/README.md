mongodb

```sh
# install to g101-prod
helm upgrade --install -n g101-prod mongodb . -f values.yaml
kubectl apply -f vs.yaml
```
