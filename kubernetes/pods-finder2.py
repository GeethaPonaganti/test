#!/usr/bin/env python2
'''
Author : OpsMx
Description :  Retrives pods in cluster/Replicasets
'''

import json
import argparse
import os
import yaml
import warnings
warnings.filterwarnings("ignore")
try:
    import kubernetes
except ImportError:
    print "[!] 'kubernetes' python module not found. Please install-> 'sudo pip2 install kubernetes'"
    exit(1)


class K8sAPI:
    def __init__(self, config_loc, namespace):
        self.config_location = config_loc
        self.namespace = namespace
        try:
            kubernetes.config.load_kube_config(self.config_location)
            v1 = kubernetes.client.CoreV1Api()
            self.pods = v1.list_namespaced_pod(self.namespace).to_dict()
        except yaml.parser.ParserError:
            print "[!] There were error(s) in kube config file. Please check again"
            exit(1)
        except kubernetes.client.rest.ApiException:
            print "[!] Not able to fetch details. Check 'namespace' is available in cluster"
            exit(1)

    def get_latest_cluster(self, cluster):
        versions = dict()
        cluster_name = None
        for items in self.pods["items"]:
            try:
                cluster_name = items["metadata"]["labels"]["cluster"]
            except:
                continue
            if cluster_name == cluster:
                versions.setdefault(int(items["metadata"]["labels"]["version"]),
                            items["metadata"]["labels"]["replication-controller"])
        try:
            return versions[max(versions)]
        except:
            print "[!] Cluster details not found"
            exit(1)

    def get_latest_pod(self, cluster_name):
        data = list()
        for items in self.pods["items"]:
            try:
                replication_con = items["metadata"]["labels"]["replication-controller"]
            except: continue
            if replication_con == cluster_name:
                info = {
                    "applicationName": items["metadata"]["labels"]["app"],
                    "podName": items["metadata"]["name"],
                    "sgName": items["metadata"]["labels"]["replication-controller"],
                    "creationTimestamp": str(items["metadata"]["creation_timestamp"])
                    }
                data.append(info)
        print json.dumps(data)


if __name__ == '__main__':
    NAMESPACE = "default"
    KUBE_CONFIG = os.path.join(os.path.expanduser("~"), ".kube/config")

    parser = argparse.ArgumentParser(description="Retrives pods in cluster/Replicasets. \
                                                        NOTE: Please specify kube config file location")
    parser.add_argument("-c", action="store", dest="cls_name", help="Gets the pods in this cluster")
    parser.add_argument("-C", action="store", dest="current_cls_name", help="Gets the pods in 'current' cluster")
    parser.add_argument("-f", action="store", dest="config_location", help="kube config location. \
                                                                            Default:~/.kube/config")
    parser.add_argument("-n", action="store", dest="namespace", help="Namespace, Default:'default'")
    parser.add_argument("-v", action="store_true", dest="validate", default=False, help="Validates the config file")
    options = parser.parse_args()
    if options.config_location:
        if os.path.exists(options.config_location):
            KUBE_CONFIG = options.config_location
        else:
            print "[!] Specified kube config file path is not valid"
            exit(1)
    else:
        if not os.path.exists(KUBE_CONFIG):
            print "[!] kube config file not available"
            exit(1)
    if options.namespace:
        NAMESPACE = options.namespace
    if options.validate:
        k8s = K8sAPI(KUBE_CONFIG, NAMESPACE)
        if k8s.pods["items"]:
            print "Success"
            exit(0)
        else:
            print "Failed"
            exit(1)
    if options.cls_name:
        k8s = K8sAPI(KUBE_CONFIG, NAMESPACE)
        k8s.get_latest_pod(options.cls_name)
    elif options.current_cls_name:
        k8s = K8sAPI(KUBE_CONFIG, NAMESPACE)
        latest_cluster = k8s.get_latest_cluster(options.current_cls_name.replace("-current", ""))
        if latest_cluster:
            k8s.get_latest_pod(latest_cluster)
    else:
        print "[!] Please specify 'cluster name'. Help-> python2 pods-finder.py -h"
