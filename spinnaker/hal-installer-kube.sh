#!/bin/bash
USERNAME=veerendra2
REPOSITORIES=veerendra2/restapp
ADDRESS=quay.io
file=~/.kube/config
if [ -f "$file" ]
then
	echo "$file Found."
else
	echo "$file not found. Place the kubernetes authentication file in ~/.kube"
    exit 1
fi
sudo apt-get update
sudo apt-get upgrade -y
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/stable/InstallHalyard.sh
sudo bash InstallHalyard.sh
hal config deploy edit --type localdebian
hal config storage edit --type redis
hal config provider docker-registry enable
hal config provider docker-registry account add my-docker-registry --address $ADDRESS --repositories $REPOSITORIES --username $USERNAME --password
hal config provider kubernetes enable
hal config provider kubernetes account add my-k8s-account --docker-registries my-docker-registry
VERSION=`hal version list | grep "):" | tail -n-1 | cut -d " " -f 3`
hal config version edit --version $VERSION
sudo hal deploy apply
