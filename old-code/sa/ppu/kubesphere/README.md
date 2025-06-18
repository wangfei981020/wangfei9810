```
# 部署Kubesphere到Kubernetes
# 注意：部署的时候ks-core不可直接使用ClusterIP方式暴露，否则会报错，需要在部署完后更改为ClusterIP，然后再通过Istio进行暴露服务
$ kubectl apply -f kubesphere-installer.yaml
$ kubectl apply -f cluster-configuration.yaml

# 查看部署情况
$ kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l 'app in (ks-install, ks-installer)' -o jsonpath='{.items[0].metadata.name}') -f

Console: http://10.163.50.16:30880
Account: admin
Password: P@88w0rd

# 修改Kubesphere暴露方式NodePort为ClusterIP模式
$ kubectl edit service ks-console -n kubesphere-system

# 开启虚拟服务通过Istio暴露到网络
$ kubectl apply -f kubesphere-virtualservice.yaml 

# 注入Istio // 让Kubesphere所有流量走Istio，否则会部分服务不可用
$ kubectl label namespace kubesphere-system istio-injection=enabled --overwrite
$ kubectl get namespace -L istio-injection
$ kubectl label namespace kubesphere-system istio-injection-
```

- bug: 当部署kube-promethues-stack的时候，如已经部署了kubesphere会出现错误，需优先部署kube-promethues-stack，然后配置kubesphere使用外部Prometheus
`endpoint： http://prometheus-operated.kubesphere-monitoring-system.svc:9090`