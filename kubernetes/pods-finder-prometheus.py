#!/usr/bin/env python2
'''
Author : OpsMx
Description :  Retrives pods in cluster/Replicasets from Prometheus
'''

import json
import argparse
import warnings
import re
from datetime import datetime
warnings.filterwarnings("ignore")

try:
    import requests
except ImportError:
    print "[!] 'requests' module is not found. please install-> 'sudo pip2 install requests'"
    exit(1)


METRIC_NAME = "container_cpu_user_seconds_total"
CLUSTER_URL = "http://{}/api/v1/series?match[]=up&match[]={}{{container_label_cluster='{}'}}"
REPLICASET_URL = "http://{}/api/v1/series?match[]=up&match[]={}{{container_label_replication_controller='{}'}}"


class PrometheusAPI:
    def __init__(self, serverip, namespace):
        self.serverip = serverip
        self.namespace = namespace

    def get_latest_cluster(self, cluster):
        version = dict()
        try:
            json_data = requests.get(CLUSTER_URL.format(self.serverip, METRIC_NAME, cluster),  timeout=5).json()
        except requests.exceptions.ConnectTimeout:
            print "[!] Connection timeout for {}".format(self.serverip)
            exit(1)
        except:
            print "[!] Not able to fetch cluster info"
            exit(1)
        for items in json_data["data"]:
            if items["__name__"] == METRIC_NAME:
                try:
                    times = items["container_label_annotation_kubernetes_io_config_seen"][:-4]
                    version.setdefault(datetime.strptime(times, '%Y-%m-%dT%H:%M:%S.%f'), items["container_label_replication_controller"])
                    #version.setdefault(int(items["container_label_version"]), items["container_label_replication_controller"])
                except KeyError:
                    pass
        if version:
            return version[max(version)]
        else:
            print "[!] Specified cluster is not found"
            exit(1)

    def get_pods(self, replicaset_name):
        data1 = list()
        data2 = dict()
        try:
            json_data = requests.get(REPLICASET_URL.format(self.serverip, METRIC_NAME, replicaset_name), timeout=5).json()
        except requests.exceptions.ConnectTimeout:
            print "[!] Connection timeout for {}".format(self.serverip)
        except:
            print "[!] Not able to fetch pods info"
            exit(1)
        for items in json_data["data"]:
            if items["__name__"] == METRIC_NAME and items["container_label_io_kubernetes_pod_namespace"] == self.namespace:
                try:
                    info = {
                        "applicationName": items["container_label_app"],
                        "podName": items["container_label_io_kubernetes_pod_name"],
                        "sgName": items["container_label_replication_controller"],
                        "creationTimestamp": items["container_label_annotation_kubernetes_io_config_seen"],
                        }
                    #data1.append(info)
                    times = items["container_label_annotation_kubernetes_io_config_seen"][:-4]  # Removing Zone
                    data2.setdefault(datetime.strptime(times, '%Y-%m-%dT%H:%M:%S.%f'), info)
                except KeyError:
                    pass
        #print json.dumps(data1)
        print json.dumps([data2[max(data2)]])


if __name__ == '__main__':
    NAMESPACE = "default"
    parser = argparse.ArgumentParser(description="Retrives pods in cluster/Replicasets from Prometheus")
    parser.add_argument("-c", action="store", dest="cls_name", help="Gets the pods in this cluster(Baseline)")
    parser.add_argument("-C", action="store", dest="current_cls_name", help="Gets the pods in 'current' cluster(Curent)")
    parser.add_argument("-s", action="store", dest="serverip", help="Prometheus enpoint. Format SERVERIP:PORT")
    parser.add_argument("-n", action="store", dest="namespace", help="Namespace, Default:'default'")
    options = parser.parse_args()
    if options.serverip:
        match = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', options.serverip)
        if not match:
            print "[!] Invalid enpoint. The endpoint should be like http:127.0.0.1:9090"
            exit(1)
    else:
        print "[!] Please specify prometheus endpoint. For help-> python pods-finder-prometheus.py -h"
        exit(1)
    if options.namespace:
        NAMESPACE = options.namespace
    if options.cls_name and options.serverip:
        pro = PrometheusAPI(match[0], NAMESPACE)
        pro.get_pods(options.cls_name)
        exit(0)
    elif options.current_cls_name and options.serverip:
        pro = PrometheusAPI(match[0], NAMESPACE)
        latest_cluster = pro.get_latest_cluster(options.current_cls_name.replace("-current", ""))
        pro.get_pods(latest_cluster)
        exit(0)
    else:
        print "[!] Please specify 'cluster name'. Help-> python2 pods-finder-prometheus.py -h"
        exit(1)
