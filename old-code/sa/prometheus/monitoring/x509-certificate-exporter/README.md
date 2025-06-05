### Install exporter 
```
helm repo add enix https://charts.enix.io

helm upgrade --install -f values.yaml x509-certificate-exporter enix/x509-certificate-exporter --version 3.17.0 -n monitoring --wait
```