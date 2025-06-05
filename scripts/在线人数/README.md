docker build -t harbor.slleisure.com/env/players-exporter:v11 .
docker push harbor.slleisure.com/env/players-exporter:v11

prod
docker build -t harbor.slleisure.com/env/players-exporter:v16 .
docker push harbor.slleisure.com/env/players-exporter:v16

