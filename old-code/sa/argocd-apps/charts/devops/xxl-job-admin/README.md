# xxl-job-admin

![Version: 1.1.0](https://img.shields.io/badge/Version-1.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 2.4.0](https://img.shields.io/badge/AppVersion-2.4.0-informational?style=flat-square)

This chart bootstraps a [xxl-job-admin](https://github.com/xuxueli/xxl-job/) replication  cluster deployment on a [Kubernetes](https://kubernetes.io/) cluster using the [Helm](https://helm.sh/) package manager.

Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- MySQL 5.6+


## Usage


[Helm](https://helm.sh) must be installed to use the charts.  Please refer to
Helm's [documentation](https://helm.sh/docs) to get started.

Once Helm has been set up correctly, add the repo as follows:

    helm repo add <alias> https://joelee2012.github.io/helm-charts

If you had already added this repo earlier, run `helm repo update` to retrieve
the latest versions of the packages.  You can then run `helm search repo
xxl-job-admin` to see the charts.

To install the xxl-job-admin chart:

    helm install my-xxl-job-admin <alias>/xxl-job-admin

To uninstall the chart:

    helm uninstall my-xxl-job-admin


## Configuration

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing).
To see all configurable options with detailed comments, visit the chart's [values.yaml](./values.yaml), or run these configuration commands:

```console
# Helm 3
$ helm show values <alias>/xxl-job-admin
```

## Configure database 
Set connection detail of [MySQL](https://www.mysql.com) for xxl-job-admin

    ## configure the database detail
    mysql:
        host: mysql.mysql
        port: 3306
        user: xxl_job
        password: changeme
        database: xxl_job

## Init database
Set `initDB.enabled=true` will init database in MySQL

    initDB:
        enabled: true


Or download the `tables_xxl_job.sql` from https://github.com/xuxueli/xxl-job/blob/master/doc/db/tables_xxl_job.sql to init database


## Parameters

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| env | list | `[]` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"xuxueli/xxl-job-admin"` |  |
| image.tag | string | `"2.4.0"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.className | string | `""` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths[0].path | string | `"/xxl-job-admin"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| initContainers | list | `[]` |  |
| initDB.enabled | bool | `true` |  |
| initDB.image.pullPolicy | string | `"IfNotPresent"` |  |
| initDB.image.registry | string | `"bitnami/mysql"` |  |
| initDB.image.tag | string | `"5.7"` |  |
| javaOpts | string | `""` |  |
| mysql.database | string | `"xxl_job"` |  |
| mysql.host | string | `"mysql.mysql"` |  |
| mysql.password | string | `"changeme"` |  |
| mysql.port | int | `3306` |  |
| mysql.user | string | `"xxl_job"` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| properties.management.health.mail.enabled | bool | `false` |  |
| properties.management.server.servlet.context-path | string | `"/actuator"` |  |
| properties.mybatis.mapper-locations | string | `"classpath:/mybatis-mapper/*Mapper.xml"` |  |
| properties.server.port | int | `8080` |  |
| properties.server.servlet.context-path | string | `"/xxl-job-admin"` |  |
| properties.spring.datasource.driver-class-name | string | `"com.mysql.cj.jdbc.Driver"` |  |
| properties.spring.datasource.hikari.auto-commit | bool | `true` |  |
| properties.spring.datasource.hikari.connection-test-query | string | `"SELECT 1"` |  |
| properties.spring.datasource.hikari.connection-timeout | int | `10000` |  |
| properties.spring.datasource.hikari.idle-timeout | int | `30000` |  |
| properties.spring.datasource.hikari.max-lifetime | int | `900000` |  |
| properties.spring.datasource.hikari.maximum-pool-size | int | `30` |  |
| properties.spring.datasource.hikari.minimum-idle | int | `10` |  |
| properties.spring.datasource.hikari.pool-name | string | `"HikariCP"` |  |
| properties.spring.datasource.hikari.validation-timeout | int | `1000` |  |
| properties.spring.datasource.password | string | `"${mysql.password}"` |  |
| properties.spring.datasource.type | string | `"com.zaxxer.hikari.HikariDataSource"` |  |
| properties.spring.datasource.url | string | `"jdbc:mysql://${mysql.host}:${mysql.port}/${mysql.database}?useUnicode=true&characterEncoding=UTF-8&autoReconnect=true&serverTimezone=Asia/Shanghai"` |  |
| properties.spring.datasource.username | string | `"${mysql.user}"` |  |
| properties.spring.freemarker.charset | string | `"UTF-8"` |  |
| properties.spring.freemarker.request-context-attribute | string | `"request"` |  |
| properties.spring.freemarker.settings.number_format | string | `"0.##########"` |  |
| properties.spring.freemarker.suffix | string | `".ftl"` |  |
| properties.spring.freemarker.templateLoaderPath | string | `"classpath:/templates/"` |  |
| properties.spring.mail.from | string | `nil` |  |
| properties.spring.mail.host | string | `nil` |  |
| properties.spring.mail.password | string | `nil` |  |
| properties.spring.mail.port | string | `nil` |  |
| properties.spring.mail.properties.mail.smtp.auth | bool | `true` |  |
| properties.spring.mail.properties.mail.smtp.socketFactory.class | string | `"javax.net.ssl.SSLSocketFactory"` |  |
| properties.spring.mail.properties.mail.smtp.starttls.enable | bool | `true` |  |
| properties.spring.mail.properties.mail.smtp.starttls.required | bool | `true` |  |
| properties.spring.mail.username | string | `nil` |  |
| properties.spring.mvc.servlet.load-on-startup | int | `0` |  |
| properties.spring.mvc.static-path-pattern | string | `"/static/**"` |  |
| properties.spring.resources.static-locations | string | `"classpath:/static/"` |  |
| properties.xxl.job.accessToken | string | `"default_token"` |  |
| properties.xxl.job.i18n | string | `"zh_CN"` |  |
| properties.xxl.job.logretentiondays | int | `30` |  |
| properties.xxl.job.triggerpool.fast.max | int | `200` |  |
| properties.xxl.job.triggerpool.slow.max | int | `100` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8080` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `""` |  |
| skywalking.enabled | bool | `false` |  |
| skywalking.optionalPlugins | list | `[]` |  |
| skywalking.version | string | `"8.9.0"` |  |
| tolerations | list | `[]` |  |
| xxlJobAdminParams | list | `[]` |  |