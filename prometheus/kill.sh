#!/usr/bin/env bash
kubectl delete -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/cadvisor-daemonset.yml
sleep 0.5
kubectl delete -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-configmap.yml
sleep 0.5
kubectl delete -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-deployment.yml
