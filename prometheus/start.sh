#!/usr/bin/env bash
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/cadvisor-daemonset.yml
sleep 0.5
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-configmap.yml
sleep 0.5
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-deployment.yml
echo ""
echo "NOTE: Open TCP port 30900 on any one node in cluster. Access UI one the node IP with 30900 like http:<NODE_IP>:30900"
