 直接helm安装
helm upgrade --install -n kubesphere-system --create-namespace ks-core https://charts.kubesphere.io/main/ks-core-1.1.3.tgz --debug --wait
or
helm upgrade --install -n kubesphere-system --create-namespace ks-core . --debug --wait
or
helm upgrade --install -n kubesphere-system --create-namespace ks-core ks-core --debug --wait