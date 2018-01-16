#!/bin/bash

FIND_IP=http://checkip.amazonaws.com/
#sudo yum remove docker docker-common docker-selinux docker-engine -y
echo "Installing Docker"
sudo yum -y install http://mirror.centos.org/centos/7/extras/x86_64/Packages/container-selinux-2.21-1.el7.noarch.rpm
sudo yum install -y yum-utils device-mapper-persistent-data lvm2 wget git
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum makecache fast
sudo yum install -y docker-ce
sudo systemctl enable docker.service
sudo systemctl start docker.service
echo "Docker Installation Successfull!"
echo ""
echo ""
echo "Setup will start Openshift installation in 3 seconds, please ensure that oc binary is in /bin/.(or press Ctrl+c to stop!)"
echo ""
echo ""
sleep 3
#wget https://github.com/openshift/origin/releases/download/v3.6.0/openshift-origin-server-v3.6.0-c4dd4cf-linux-64bit.tar.gz
#tar -xvf openshift-origin-server-v3.6.0-c4dd4cf-linux-64bit.tar.gz
#sudo cp openshift-origin-server-v3.6.0-c4dd4cf-linux-64bit/oc /bin/
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
   "insecure-registries": [
     "172.30.0.0/16"
   ],
   "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
PUBLIC_IP=`curl -s "$FIND_IP"`
if [[ -n "$PUBLIC_IP" ]]; then
  echo "\nYour Public IP: $PUBLIC_IP"
  oc cluster up --public-hostname=$PUBLIC_IP #--version=v1.5.1
else
  echo "\nNot able to find your public IP"
  oc cluster up #--version=v1.5.1
fi
sudo systemctl stop firewalld
echo ""
echo ""
echo "TIP: If installation is not successfull, please restart docker daemon and run oc cluster up --public-hostname=<PUBLIC_IP>"
echo "Please give cluster admin privilages to system:anonymous user for Spinnaker. Refer:https://github.com/OpsMx/scripts/wiki/OpenShift"
#sudo yum install firewalld -y
#sudo firewall-cmd --permanent --new-zone dockerc
#sudo firewall-cmd --permanent --zone dockerc --add-source 172.17.0.0/16
#sudo firewall-cmd --permanent --zone dockerc --add-port 8443/tcp
#sudo firewall-cmd --permanent --zone dockerc --add-port 53/udp
#sudo firewall-cmd --permanent --zone dockerc --add-port 8053/udp
#sudo firewall-cmd --reload
