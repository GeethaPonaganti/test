#/bin/bash

kubectl apply -f role.yml
kubectl apply -f service_account.yml
kubectl apply -f role_binding.yml
