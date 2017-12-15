# Setting up Prometheus

* Download: https://prometheus.io/download/
* Extract tar.gz file
* Get the reference config file -> https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus.yml
* Inside directory, run `nohup ./prometheus --config.file=prometheus.yml &`

# Setting up K8s Monitoring with Prometheus
##### 1. Launch cAdvisor `DeamonSet`. K8s will launch a POD on every node in cluster.
```
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/cadvisor-daemonset.yml
```
##### 2. Run Prometheus `ConfigMap`. Which basically creates config for Prometheus POD.
```
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-configmap.yml
```
##### 3. Launch Prometheus POD.
```
kubectl create -f https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/prometheus-deployment.yml
```
 * Open TCP port `30900` on any one node in cluster. Access UI one the node IP with `30900` like `http:<NODE_IP>:30900`
 * Automated script to launch: `curl https://raw.githubusercontent.com/OpsMx/scripts/master/prometheus/start.sh | bash`
 * Automated script to kill: `curl https://github.com/OpsMx/scripts/blob/master/prometheus/kill.sh | bash`

##### * For Federation Configuration please refer [here](https://github.com/OpsMx/scripts/blob/master/prometheus/prometheus.yml#L44)
