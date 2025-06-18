# Jumpserver

[Jumpserver](http://www.jumpserver.org/) 是全球首款完全开源的堡垒机, 使用 GNU GPL v2.0 开源协议, 是符合 4A 的专业运维审计系统。

## 使用方法

```bash
helm repo add jumpserver https://jumpserver.github.io/helm-charts
```

## 介绍

当前 Chart 包含了 Jumpserver 所需的基本组件

## 依赖

- Kubernetes 1.20+
- Helm 3.0

**Tip**: List all releases using `helm repo list`

## 参数

下面的表格中列出了一些必要的参数，发布前请先阅读并设置

### 总览

`global.imageRegistry` 和 `global.imageOwner` 用于指定镜像仓库地址和用户名，如果使用私有仓库，还需要需要设置 `global.imagePullSecrets` 参数，用于指定私有仓库认证凭据。

| 参数                      | 描述                | 默认值      |
| ------------------------- | ------------------ | ----------- |
| `nameOveride`             | name override      | `nil`       |
| `fullNameOveride`         | full name override | `nil`       |
| `global.imageRegistry`    | 仓库地址           | `docker.io` |
| `global.imageOwner`       | 仓库用户名         | `jumpserver` |
| `global.imagePullSecrets` | 私有仓库认证凭据    | `nil`       |
| `global.storageClass`     | 存储 sc            | `nil`       |
| `ingress.enabled`         | 开启 ingress       | `true`      |
| `core.enabled`            | 开启 core          | `true`      |
| `koko.enabled`            | 开启 koko          | `true`      |
| `lion.enabled`            | 开启 lion          | `true`      |
| `magnus.enabled`          | 开启 magnus        | `true`      |
| `chen.enabled`            | 开启 chen          | `true`      |
| `kael.enabled`            | 开启 kael          | `true`      |
| `web.enabled`             | 开启 web           | `true`      |
| `xpack.enable`            | 开启 xpack         | `false`     |

### 必填

如果 `global` 中的参数和其他组件中的参数同时存在，将优先使用 `global` 中的参数。

| 参数                           | 描述                                          | 默认值                 |
| ------------------------------ | ---------------------------------------------| ---------------------- |
| `global.storageClass`          | 持久化存储                                    | `nil`                  |
| `core.config.secretKey`        | 加密秘钥 生产环境中请修改为随机字符串，请勿外泄  | `nil`                  |
| `core.config.bootstrapToken`   | 预共享 Token 组件注册需要使用                  | `nil`                  |
| `externalDatabase.engine`      | 数据库引擎                                    | `mysql`                |
| `externalDatabase.host`        | 数据库 IP 地址                                | `nil`                  |
| `externalDatabase.port`        | 数据库端口                                    | `3306`                 |
| `externalDatabase.user`        | 数据库用户名                                  | `jumpserver`           |
| `externalDatabase.password`    | 数据库密码                                    | `nil`                  |
| `externalDatabase.database`    | 数据库名称                                    | `nil`                  |
| `externalRedis.host`           | redisIP 地址                                 | `nil`                  |
| `externalRedis.port`           | redis 端口                                   | `6379`                 |
| `externalRedis.password`       | redis 密码                                   | `nil`                  |

### Redis Sentinel

配置 `externalSentinel` 参数后，将优先使用 `Sentinel`，`Redis` 即使配置也不会使用。  
注意：`Sentinel` 密码和 `Redis` 密码需要分别设置。

| 参数                             | 描述                                          | 默认值                |
| -------------------------------- | ---------------------------------------------| --------------------- |
| `externalSentinel.hosts`         | Sentinel 地址池                               | `nil`                 |
| `externalSentinel.password`      | Sentinel 认证密码                             | `6379`                |
| `externalRedis.password`         | redis 密码                                    | `nil`                 |
| `externalSentinel.socketTimeout` | Sentinel 超时时间，单位 秒(s)                 | `5`                   |

### 其他

| 参数                  | 描述                                                       | 默认值  |
| --------------------- | --------------------------------------------------------- | ------- |
| `log.level`           | 日志等级                                                   | `INFO`  |
| `replicaCount`        | 副本数量                                                   | `1`     |
| `persistence`         | 持久化存储相关设置                                         | `nil`   |

在 `helm install` 时通过 `--set key=value[,key=value]` 指定参数. 举例:

```bash
helm install jumpserver ./ \
--set ingress.enabled=true
```

上条命令开启了 ingress.

**注**: 默认使用 [values.yaml](values.yaml)

## 示例

```bash
helm install jms-k8s jumpserver/jumpserver -n default \
--set core.config.secretKey=GxrLH7rewfsRN8B9Zl6MEGD50Uou4LF6UVsEIayGMhYll8dqmn \
--set core.config.bootstrapToken=ilR8RvAbK7lgRTxs \
--set global.storageClass=jms-data \
--set externalDatabase.engine=mysql \
--set externalDatabase.host=jms-mysql \
--set externalDatabase.port=3306 \
--set externalDatabase.user=jms \
--set externalDatabase.password=Password131 \
--set externalDatabase.database=jumpserver \
--set externalRedis.host=jms-redis-master \
--set externalRedis.port=6379 \
--set koko.service.type=NodePort \
--set web.service.type=NodePort \
--set externalRedis.password=PasswordRedis
```

## 卸载

删除 `jms-k8s` release:

```bash
$ helm delete jms-k8s -n default
```

上条命令删除了所有包含在 release 中的组件

## 鸣谢说明

本项目初始代码是由 [xiaomaimuchanyiyiba](https://github.com/xiaomaimuchanyiyiba) 贡献。[原仓库地址](https://github.com/xiaomaimuchanyiyiba/jumpserver)
