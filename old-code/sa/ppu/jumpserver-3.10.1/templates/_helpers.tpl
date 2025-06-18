{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "jumpserver.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "jumpserver.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "jumpserver.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "jumpserver.labels" -}}
app.kubernetes.io/name: {{ include "jumpserver.name" . }}
helm.sh/chart: {{ include "jumpserver.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "jumpserver.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{ default (include "jumpserver.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
{{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Define JumpServer database.
*/}}

{{- define "jumpserver.mysql.fullname" -}}
{{- $name := default "mysql" .Values.mysql.nameOverride -}}
{{- printf "%s-%s-master" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "jumpserver.database.host" -}}
{{- .Values.externalDatabase.host -}}
{{- end -}}

{{- define "jumpserver.database.port" -}}
{{- .Values.externalDatabase.port -}}
{{- end -}}

{{- define "jumpserver.database.user" -}}
{{- .Values.externalDatabase.user -}}
{{- end -}}

{{- define "jumpserver.database.password" -}}
{{- .Values.externalDatabase.password -}}
{{- end -}}

{{- define "jumpserver.database.engine" -}}
{{- .Values.externalDatabase.engine -}}
{{- end -}}

{{- define "jumpserver.database.database" -}}
{{- .Values.externalDatabase.database -}}
{{- end -}}

{{/*
Define JumpServer sentinel.
*/}}

{{- define "jumpserver.sentinel.hosts" -}}
{{- if .Values.externalSentinel.hosts -}}
{{- .Values.externalSentinel.hosts -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.sentinel.password" -}}
{{- if .Values.externalSentinel.password -}}
{{- .Values.externalSentinel.password -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.sentinel.socketTimeout" -}}
{{- if .Values.externalSentinel.socketTimeout -}}
{{- .Values.externalSentinel.socketTimeout -}}
{{- end -}}
{{- end -}}

{{/*
Define JumpServer redis.
*/}}

{{- define "jumpserver.redis.fullname" -}}
{{- $name := default "redis" .Values.redis.nameOverride -}}
{{- printf "%s-%s-master" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "jumpserver.redis.host" -}}
{{- if .Values.externalRedis.host -}}
{{- .Values.externalRedis.host -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.redis.port" -}}
{{- if .Values.externalRedis.port -}}
{{- .Values.externalRedis.port -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.redis.password" -}}
{{- if .Values.externalRedis.password -}}
{{- .Values.externalRedis.password -}}
{{- end -}}
{{- end -}}

{{/*
Define JumpServer StorageClass.
*/}}

{{- define "jumpserver.core.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.core.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.koko.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.koko.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.lion.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.lion.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.magnus.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.magnus.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.chen.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.chen.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.kael.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.kael.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.razor.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.razor.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.xrdp.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.xrdp.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.video.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.video.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.web.storageClass" -}}
{{- if .Values.global.storageClass }}
{{- .Values.global.storageClass }}
{{- else -}}
{{- .Values.web.persistence.storageClassName -}}
{{- end -}}
{{- end -}}

{{/*
Define JumpServer magnus ports.
*/}}

{{- define "jumpserver.magnus.mysql.port" -}}
{{- default 33061 .Values.magnus.service.mysql.port -}}
{{- end -}}

{{- define "jumpserver.magnus.mariadb.port" -}}
{{- default 33062 .Values.magnus.service.mariadb.port -}}
{{- end -}}

{{- define "jumpserver.magnus.redis.port" -}}
{{- default 63790 .Values.magnus.service.redis.port -}}
{{- end -}}

{{- define "jumpserver.magnus.postgresql.port" -}}
{{- default 54320 .Values.magnus.service.postgresql.port -}}
{{- end -}}

{{- define "jumpserver.magnus.sqlserver.port" -}}
{{- default 14330 .Values.magnus.service.sqlserver.port -}}
{{- end -}}

{{- define "jumpserver.magnus.oracle.ports" -}}
{{- default "30000-30100" .Values.magnus.service.oracle.ports -}}
{{- end -}}

{{- define "jumpserver.magnus.oracle.port.start" -}}
{{- if .Values.magnus.service.oracle.ports }}
{{- .Values.magnus.service.oracle.ports | splitList "-" | first }}
{{- else -}}
{{- default 30000 -}}
{{- end -}}
{{- end -}}

{{- define "jumpserver.magnus.oracle.port.end" -}}
{{- if .Values.magnus.service.oracle.ports }}
{{- add (.Values.magnus.service.oracle.ports | splitList "-" | last) 1 }}
{{- else -}}
{{- default 30101 -}}
{{- end -}}
{{- end -}}
