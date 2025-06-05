## 配置 Helm repo

```sh {"id":"01J6EFKJVM9RR5VXKWYCE8F3Z6"}
$ helm repo add istio https://istio-release.storage.googleapis.com/charts
$ helm repo update
```

## install istio-base && istiod

```sh {"id":"01J6EFKJVM9RR5VXKWYGCPCRHY"}
kubectl create namespace istio-system
cd g32-prod-deployment/istio-system/helm/

helm upgrade --install istio-base istio/base -n istio-system --version 1.23.2 --wait
helm upgrade --install istiod istio/istiod -f values-istiod.yaml -n istio-system --version 1.23.2 --wait
```

## install istio gateway
```sh {"id":"01J6EFKJVM9RR5VXKWYGR09HZD"}
# 临时手动导入证书
cd g32-prod-deployment/istio-system/gateway/ssl
kubectl create secret tls slleisure-com-cert --cert=./slleisure.com.crt --key=./slleisure.com.key -n istio-system
kubectl create secret tls g32-prod-com-cert --cert=./g32-prod.com.crt --key=./g32-prod.com.key -n istio-system
kubectl create secret tls dragontiger-game-com-cert --cert=./dragontiger-game.com.crt --key=./dragontiger-game.com.key -n istio-system
kubectl create secret tls classicbaccarat-game-com-cert --cert=./classicbaccarat-game.com.crt --key=./classicbaccarat-game.com.key -n istio-system
kubectl create secret tls roulettegame-frontend-com-cert --cert=./roulettegame-frontend.com.crt --key=./roulettegame-frontend.com.key -n istio-system
kubectl create secret tls sicbo-game-com-cert --cert=./sicbo-game.com.crt --key=./sicbo-game.com.key -n istio-system
kubectl create secret tls speedbaccarat-game-com-cert --cert=./speedbaccarat-game.com.crt --key=./speedbaccarat-game.com.key -n istio-system


cd g32-prod-deployment/istio-system/helm/
helm upgrade --install istio-ingressgateway-inner istio/gateway -f g32-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install istio-ingressgateway-extra istio/gateway -f g32-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait

cd g32-prod-deployment/istio-system/gateway/g32-gateway
kubectl apply -f istio-ingressgateway-inner.yaml
kubectl apply -f istio-ingressgateway-extra.yaml
kubectl apply -f dragon-tiger-game-extra.yaml

cd g32-prod-deployment/istio-system/gateway/g31-gateway

helm upgrade --install g31-istio-ingressgateway-inner istio/gateway -f g31-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g31-istio-ingressgateway-extra istio/gateway -f g31-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait

kubectl apply -f g31-istio-ingressgateway-extra.yaml
kubectl apply -f g31-istio-ingressgateway-inner.yaml

cd g32-prod-deployment/istio-system/gateway/g101-gateway

helm upgrade --install g101-istio-ingressgateway-inner istio/gateway -f g101-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g101-istio-ingressgateway-extra istio/gateway -f g101-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait

kubectl apply -f g101-istio-ingressgateway-extra.yaml
kubectl apply -f g101-istio-ingressgateway-inner.yaml

cd g32-prod-deployment/istio-system/gateway/g35-gateway

helm upgrade --install g35-istio-ingressgateway-inner istio/gateway -f g35-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g35-istio-ingressgateway-extra istio/gateway -f g35-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait

kubectl apply -f g35-istio-ingressgateway-extra.yaml
kubectl apply -f g35-istio-ingressgateway-inner.yaml

cd otb-prod-deployment/istio-system/gateway/otb-gateway

helm upgrade --install otb-istio-ingressgateway-inner istio/gateway -f otb-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install otb-istio-ingressgateway-extra istio/gateway -f otb-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait

kubectl apply -f otb-istio-ingressgateway-extra.yaml
kubectl apply -f otb-istio-ingressgateway-inner.yaml

cd otb-prod-deployment/istio-system/helm
helm upgrade --install g39-istio-ingressgateway-inner istio/gateway -f g39-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g39-istio-ingressgateway-extra istio/gateway -f g39-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait
cd /data/helm/otb-prod-deployment/istio-system/gateway/g39-gateway
kubectl apply -f g39-istio-ingressgateway-extra.yaml
kubectl apply -f g39-istio-ingressgateway-inner.yaml

cd otb-prod-deployment/istio-system/helm
helm upgrade --install g22-istio-ingressgateway-inner istio/gateway -f g22-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g22-istio-ingressgateway-extra istio/gateway -f g22-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait
cd /data/helm/otb-prod-deployment/istio-system/gateway/g22-gateway
kubectl apply -f g22-istio-ingressgateway-extra.yaml
kubectl apply -f g22-istio-ingressgateway-inner.yaml


cd otb-prod-deployment/istio-system/helm
helm upgrade --install g38-istio-ingressgateway-inner istio/gateway -f g38-values-gateway-inner.yaml -n istio-system --version 1.23.2 --wait
helm upgrade --install g38-istio-ingressgateway-extra istio/gateway -f g38-values-gateway-extra.yaml -n istio-system --version 1.23.2 --wait
cd /data/helm/otb-prod-deployment/istio-system/gateway/g38-gateway
kubectl apply -f g38-istio-ingressgateway-extra.yaml
kubectl apply -f g38-istio-ingressgateway-inner.yaml

```


