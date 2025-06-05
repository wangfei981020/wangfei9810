```bash
helm repo add pingcap https://charts.pingcap.org/
helm repo update

# TiDB Operator
kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.0/manifests/crd.yaml
helm upgrade --install tidb-operator pingcap/tidb-operator --namespace g101-tidb --version v1.6.0 --wait

# Install
kubectl apply -f tidb-cluster.yaml -n g101-tidb
kubectl apply -f tidb-dashboard.yaml -n g101-tidb
kubectl apply -f tidb-monitor.yaml -n g101-tidb
kubectl apply -f tidb-ngmonitoring.yaml -n g101-tidb

kubectl apply -f vs.yaml
```
