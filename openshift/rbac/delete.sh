#/bin/bash

kubectl delete -f role.yml
kubectl delete -f service_account.yml
kubectl delete -f role_binding.yml
