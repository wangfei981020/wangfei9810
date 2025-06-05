apache-doris

```sh
# install
helm repo add doris-repo https://charts.selectdb.com
helm repo update

# namespace and istio-injection
kubectl create namespace doris
#kubectl label namespaces doris istio-injection=enabled

# pull charts
helm pull --untar doris-repo/doris-operator
helm pull --untar doris-repo/doris

# install doris-operator
cd doris-operator
helm upgrade --install -n doris operator . -f values.yaml

# install doriscluster
cd doris
helm upgrade --install -n doris doriscluster . -f values.yaml
kubectl apply -f service-extra.yaml
kubectl apply -f servicemonitor.yaml
kubectl apply -f vs.yaml
kubectl apply -f doris-nginx.yaml
```
