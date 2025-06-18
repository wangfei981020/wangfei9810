```
$ helm repo add elastic https://helm.elastic.co
```

```
$ helm upgrade --install elasticsearch -f values.yaml elastic/elasticsearch -n db-services --wait
```