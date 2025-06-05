# 每次请求接口刷新一次
docker build -t harbor.slleisure.com/env/loki-resource:v2 .   
docker push harbor.slleisure.com/env/loki-resource:v2

# 每5分钟循环一次，每次请求接口获取最新指标
# 每次请求接口刷新一次
# uat
docker build -t harbor.slleisure.com/env/loki-resource:v3 .   
docker push harbor.slleisure.com/env/loki-resource:v3

# prod
docker build -t harbor.slleisure.com/env/loki-resource:v6 .   
docker push harbor.slleisure.com/env/loki-resource:v6
# prod
docker build -t harbor.slleisure.com/env/loki-resource:v7 .   
docker push harbor.slleisure.com/env/loki-resource:v7
# prod
docker build -t harbor.slleisure.com/env/loki-resource:v9 .   
docker push harbor.slleisure.com/env/loki-resource:v9