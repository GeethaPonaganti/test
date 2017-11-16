#!/usr//bin/env python2
'''
Author : OpsMx
Description :  Retrives pods in cluster/Replicasets
'''

import json
import argparse
import warnings
warnings.filterwarnings("ignore")

try:
    import requests
except ImportError:
    print "[!] 'requests' module is not found. please install-> 'sudo pip2 install reuests'"


METRIC_NAME = "container_cpu_user_seconds_total"
CLUSTER_URL = "http://{}:9090/api/v1/series?match[]=up&match[]={}{{container_label_cluster='{}'}}"
REPLICASET_URL = "http://{}:9090/api/v1/series?match[]=up&match[]={}{{container_label_replication_controller='{}'}}"


class PrometheusAPI:
    def __init__(self, serverip, namespace):
        self.serverip = serverip
        self.namespace = namespace

    def get_latest_cluster(self, cluster):
        version = dict()
        try:
            json_data = requests.get(CLUSTER_URL.format(self.serverip, METRIC_NAME, cluster)).json()
        except:
            print "[!] Not able to fetch cluster info"
            exit(1)
        for items in json_data["data"]:
            if items["__name__"] == METRIC_NAME:
                try:
                    version.setdefault(int(items["container_label_version"]), items["container_label_replication_controller"])
                except KeyError:
                    pass
        if version:
            return version[max(version)]
        else:
            print "[!] Specified cluster not found"
            exit(1)

    def get_pods(self, replicaset_name):
        data =list()
        try:
            json_data = requests.get(REPLICASET_URL.format(self.serverip, METRIC_NAME, replicaset_name)).json()
        except:
            print "[!] Not able to fetch pods info"
            exit(1)
        for items in json_data["data"]:
            if items["__name__"] == METRIC_NAME and items["container_label_io_kubernetes_pod_namespace"] == self.namespace:
                try:
                    info = {
                        "applicationName": items["container_label_app"],
                        "podName": items["container_label_io_kubernetes_pod_name"],
                        "sgName": items["container_label_io_kubernetes_pod_name"],
                        "creationTimestamp": items["container_label_annotation_kubernetes_io_config_seen"],
                        }
                    data.append(info)
                except KeyError:
                    pass
        print json.dumps(data)


if __name__ == '__main__':
    NAMESPACE = "default"
    parser = argparse.ArgumentParser(description="Retrives pods in cluster/Replicasets from Prometheus")
    parser.add_argument("-c", action="store", dest="cls_name", help="Gets the pods in this cluster")
    parser.add_argument("-C", action="store", dest="current_cls_name", help="Gets the pods in 'current' cluster")
    parser.add_argument("-s", action="store", dest="serverip", help="Prometheus server IP")
    parser.add_argument("-n", action="store", dest="namespace", help="Namespace, Default:'default'")
    parser.add_argument("-v", action="store_true", dest="validate", default=False, help="Validates the config file")
    options = parser.parse_args()
    if options.namespace:
        NAMESPACE = options.namespace
    if options.cls_name and options.serverip:
        pro = PrometheusAPI(options.serverip, NAMESPACE)
        pro.get_pods(options.cls_name)
        exit(0)
    elif options.current_cls_name and options.serverip:
        pro = PrometheusAPI(options.serverip, NAMESPACE)
        latest_cluster = pro.get_latest_cluster(options.current_cls_name.replace("-current", ""))
        pro.get_pods(latest_cluster)
        exit(0)
    else:
        print "[!] Please specify 'cluster name'. Help-> python2 pods-finder.py -h"
        exit(1)
