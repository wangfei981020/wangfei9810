#!/bin/bash
# This script deploys Loki using Helm with a specified values file and namespace.

helm upgrade --install loki . -f values.yaml -n logging