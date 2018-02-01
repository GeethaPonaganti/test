# Service Account Creation for Spinnaker

1. Create Service Account
```
kubectl create -f service_account.yml
```
2. Create `Role`
```
kubectl create -f role.yml
```
3. Apply `RoleBinding` to `Service Account`
```
kubectl apply -f role_binding.yml
```
