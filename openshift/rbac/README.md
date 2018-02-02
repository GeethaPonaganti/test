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
4. Get `service-account-token`
```
secret=`kubectl describe sa spinnaker | grep Tokens | cut -d ":" -f 2 | tr -d '[:space:]'`
kubectl describe secrets $secret
```
 Copy token and make kubeconfig file
