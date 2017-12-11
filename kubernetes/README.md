# Kubernetes
Check [wiki](https://github.com/OpsMx/scripts/wiki/Kubernetes) for more info 

* `curl https://raw.githubusercontent.com/OpsMx/scripts/master/kubernetes/ubuntu-kube-installer.sh | bash`
## Retrives PODS from `Prometheus`
##### **Dependency: `requests` Python module required: `sudo pip2 install requests`
##### Download RUN-> wget -qO pods-finder-prometheus.py https://raw.githubusercontent.com/OpsMx/scripts/master/kubernetes/prometheus-pods.py
* Help
```
ubuntu@localhost:~$ python2 pods-finder-prometheus.py -h
usage: pods-prometheus.py [-h] [-c CLS_NAME] [-C CURRENT_CLS_NAME]
                          [-s SERVERIP] [-n NAMESPACE]

Retrives pods in cluster/Replicasets from Prometheus

optional arguments:
  -h, --help           show this help message and exit
  -c CLS_NAME          Gets the pods in this cluster(Baseline)
  -C CURRENT_CLS_NAME  Gets the pods in 'current' cluster(Current)
  -s SERVERIP          Prometheus enpoint. Format SERVERIP:PORT
  -n NAMESPACE         Namespace, Default:'default'

```
* ##### Gets all pods in `current deployed` cluster
```
veeru@ultron:~/kubernetes$ python2 pods-finder-prometheus.py -s xx.xx.xx.105:9090 -n default -C oxygen-prod-current
[
   {
      "applicationName":"oxygen",
      "creationTimestamp":"2017-11-13T19:03:43.031991375Z",
      "sgName":"oxygen-prod-v001-rz4wt",
      "podName":"oxygen-prod-v001-rz4wt"
   },
   {
      "applicationName":"oxygen",
      "creationTimestamp":"2017-11-13T19:03:43.019775014Z",
      "sgName":"oxygen-prod-v001-7cncr",
      "podName":"oxygen-prod-v001-7cncr"
   }
]
```
* ##### Gets all pods in `specified` cluster
```
veeru@ultron:~/kubernetes$ python2 pods-finder-prometheus.py -s xx.xx.xx.105:9090 -n default -c oxygen-prod-v001

[
   {
      "applicationName":"oxygen",
      "creationTimestamp":"2017-11-13T19:03:43.031991375Z",
      "sgName":"oxygen-prod-v001-rz4wt",
      "podName":"oxygen-prod-v001-rz4wt"
   },
   {
      "applicationName":"oxygen",
      "creationTimestamp":"2017-11-13T19:03:43.019775014Z",
      "sgName":"oxygen-prod-v001-7cncr",
      "podName":"oxygen-prod-v001-7cncr"
   }
]
```


## Retrieves PODS in cluster/Replicasets (Version 2)
##### **Dependency: `kubernetes` Python module required: `sudo pip2 install kubernetes`
##### To download,RUN-> wget -qO pods-finder.py https://raw.githubusercontent.com/OpsMx/scripts/master/kubernetes/pods-finder2.py
* Help
```
ubuntu@opsmx:~$ python2 pods-finder.py -h
usage: pods-finder.py [-h] [-c CLS_NAME] [-C CURRENT_CLS_NAME]
                      [-f CONFIG_LOCATION] [-n NAMESPACE] [-v]

Retrives pods in cluster/Replicasets. NOTE: Please specify kube config file
location

optional arguments:
  -h, --help           show this help message and exit
  -c CLS_NAME          Gets the pods in this cluster
  -C CURRENT_CLS_NAME  Gets the pods in 'current' cluster
  -f CONFIG_LOCATION   kube config location. Default:~/.kube/config
  -n NAMESPACE         Namespace, Default:'default'
  -v                   Validates the config file
```
* Config file and namespace Validation
```
ubuntu@ghost:~$ python2 pods-finder.py -v -f /path/to/config/file
Success
```
* Specify Namespace and Kube config location
  * NOTE: By default the script assumes kube config file location is at `~/.kube/config`
  * NOTE: By default the script assumes the namespace as `default`
```
ubuntu@opsmx:~$ python2 pods-finder.py -n default -f /home/ubuntu/.kube/config -C oxygen-prod-current
[
   {
      "applicationName":"oxygen",
      "creationTimestamp":"2017-11-14 10:46:47+00:00",
      "sgName":"oxygen-prod-v007",
      "podName":"oxygen-prod-v007-lwwjz"
   }
]
```
* ##### Gets all pods in `current deployed` cluster
```
root@ultron:/# python2 pods-finder.py -n default -f /home/ubuntu/.kube/config -c radium-prod-v003
[
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T10:10:53Z",
      "sgName":"radium-prod-v003",
      "podName":"radium-prod-v003-779wx"
   },
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T10:10:53Z",
      "sgName":"radium-prod-v003",
      "podName":"radium-prod-v003-b46lr"
   }
]
```
* ##### Gets all pods in `specified` cluster
```
root@ultron:/# python2 pods-finder.py -n default -f /home/ubuntu/.kube/config -c radium-prod-v001
[
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T08:13:59Z",
      "sgName":"radium-prod-v001",
      "podName":"radium-prod-v001-bpfqt"
   },
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T08:13:59Z",
      "sgName":"radium-prod-v001",
      "podName":"radium-prod-v001-dz8d6"
   }
]
```
## Latest PODs finder from `cluster name` or `cluster name with version` (kube-pod-finder.py)[** OLDER VERSION **]
  * ##### Help
  ```
  python kube-pod-finder.py -h
  usage: kube-pod-finder.py [-h] [-c CLUSTER_NAME]

  Latest pods finder in K8s cluster. NOTE: Please specify 'K8s_IP' in script

  optional arguments:
    -h, --help       show this help message and exit
    -c CLUSTER_NAME  cluster name or cluster name with version
  ```

  * ##### Get PODs from `cluster name with VERSION`
  ```
  python kube-pod-finder.py -c datadogtest1-sg1-v010
[{"applicationName": "datadogtest1", "creationTimestamp": "2017-10-16 19:58:13", "sgName": "datadogtest1-sg1-v010", "podName": "datadogtest1-sg1-v010-hqp3s"}]
  ```
  * ##### Get latest/current PODs in the `cluster`
  ```
 python kube-pod-finder.py -c datadogtest1-sg1-current
[{"applicationName": "datadogtest1", "creationTimestamp": "2017-10-17 09:13:44", "sgName": "datadogtest1-sg1-v012", "podName": "datadogtest1-sg1-v012-bpsm2"}]
  ```
  * Please specify `K8s_IP` in the script. If needed specify `NAMESPACE` also.
  * Get the script ---> `wget -qO kube-pod-finder.py https://goo.gl/62Gu11`

## Retrives PODs in the `cluster` (pods-finder.py) [** OLDER VERSION **]
* ##### Dowload -> `wget -qO pods-finder.py https://goo.gl/jqs2GV`
* ##### Help
```
root@ultron:/home/veeru/Desktop# python kube.py -h
usage: kube.py [-h] [-c CLS_NAME] [-C CURRENT_CLS_NAME]

Latest pods finder in K8s cluster. NOTE: Please specify 'K8s_IP' in script

optional arguments:
  -h, --help           show this help message and exit
  -c CLS_NAME          Gets the pods in this cluster
  -C CURRENT_CLS_NAME  Gets the pods in 'current' cluster
```
* ##### Gets all pods in `current deployed` cluster
```
root@ultron:/# python2 pods-finder.py -C radium-prod-current
[
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T10:10:53Z",
      "sgName":"radium-prod-v003",
      "podName":"radium-prod-v003-779wx"
   },
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T10:10:53Z",
      "sgName":"radium-prod-v003",
      "podName":"radium-prod-v003-b46lr"
   }
]
```
* ##### Gets all pods in `specified` cluster
```
root@ultron:/# python2 pods-finder.py -c radium-prod-v001
[
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T08:13:59Z",
      "sgName":"radium-prod-v001",
      "podName":"radium-prod-v001-bpfqt"
   },
   {
      "applicationName":"radium",
      "creationTimestamp":"2017-11-10T08:13:59Z",
      "sgName":"radium-prod-v001",
      "podName":"radium-prod-v001-dz8d6"
   }
]
```
