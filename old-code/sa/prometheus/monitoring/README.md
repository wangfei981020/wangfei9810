monitoring

## install
```sh
# repo
helm repo add promprometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# kube-prometheus-stack
cd kube-prometheus-stack
helm upgrade --install kube-prometheus-stack . -f values.yaml -n monitoring
kubectl apply -f vs.yaml


# kubernetes-event-exporter
cd kubernetes-event-exporter
helm upgrade --install kubernetes-event-exporter . -f values.yaml -n monitoring


# prometheus-kafka-exporter
cd prometheus-kafka-exporter
helm upgrade --install g29-kafka-exporter . -f xxx-values.yaml -n monitoring


# prometheus-redis-exporter
cd prometheus-redis-exporter
helm upgrade --install g29-redis-exporter . -f xxx-values.yaml -n monitoring
helm upgrade --install g32-redis-exporter . -f xxx-values.yaml -n monitoring


# rocketmq-exporter
cd rocketmq-exporter
kubectl apply -f all.yaml -n monitoring


# x509-certificate-exporter
cd x509-certificate-exporter
helm upgrade --install x509-certificate-exporter enix/x509-certificate-exporter -f values.yaml -n monitoring


# prometheus-blackbox-exporter
cd prometheus-blackbox-exporter
helm upgrade --install prometheus-blackbox-exporter . -f values.yaml -n monitoring
```
