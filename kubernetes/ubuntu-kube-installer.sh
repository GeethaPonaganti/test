#/bin/bash

FIND_IP="http://checkip.amazonaws.com/"
PUBLIC_IP=`curl -s "$FIND_IP"`
echo "Your Public IP: $PUBLIC_IP"
echo "NOTE: Don't run the script with 'sudo'. Installation will start in 5 seconds"
sleep 5
sudo apt-get update
sudo apt-get upgrade -y
echo "Installing Docker"
#sudo apt-get remove docker docker-engine docker.io -y
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual -y
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - -y
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
sudo apt-get update
sudo apt-get install -y docker-ce --allow-unauthenticated
sudo usermod -aG docker $USER
docker ps
if [ $? == 0 ]; then
  echo "Docker Installation Successfull"
else
  echo "Docker Installation Failed"
  exit 1
fi
if [[ -z `cat /etc/lsb-release | grep 16.04` ]]; then
  echo "Exiting installation of Kubernetes(with kubeadm) which requries Ubuntu 16.04"
  exit 1
fi
echo ""
echo "Do you want to install Kubernetes?[y/n]"
read ans
if [ "$ans" == "y" ]; then
if [[ -z `cat /etc/lsb-release | grep 16.04` ]]; then
  echo "Exiting installation of Kubernetes(with kubeadm) which requries Ubuntu 16.04"
  exit 1
fi
sudo apt-get install -y apt-transport-https
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - -y
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl kubernetes-cni --allow-unauthenticated
if [[ -n "$PUBLIC_IP" ]]; then
  echo "Your Public IP: $PUBLIC_IP"
  sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=$PUBLIC_IP --skip-preflight-checks
else
  echo "Not able to find your public IP"
  sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --skip-preflight-checks
fi
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl taint nodes --all node-role.kubernetes.io/master-
kubectl create clusterrolebinding anonymous-cluster-admin-binding --clusterrole=cluster-admin --user=system:anonymous
#echo "Launching cAdvisor Container"
#sudo docker run \
#  --volume=/:/rootfs:ro \
#  --volume=/var/run:/var/run:rw \
#  --volume=/sys:/sys:ro \
#  --volume=/var/lib/docker/:/var/lib/docker:ro \
#  --volume=/dev/disk/:/dev/disk:ro \
#  --publish=9090:8080 \
#  --detach=true \
#  --name=cadvisor \
#  --restart always \
#  google/cadvisor:latest
echo ""
echo "**===============IMPORT NOTE===============**"
echo "1. PLEASE DO CHANGES AS SPECIFIED in https://goo.gl/fMLVEA"
echo "2. Restart kubelet daemon"
echo "3. RUN==> kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.0/Documentation/kube-flannel.yml"

#kubectl create -f https://raw.githubusercontent.com/coreos/flannel/v0.8.0/Documentation/kube-flannel-rbac.yml
#kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
#kubectl get pods --all-namespaces
#echo ""
#kubectl cluster-info
#echo ""
#sudo docker run --net=host --volume=/var/lib/docker/:/var/lib/docker:ro --volume=/sys/fs/cgroup/:/sys/fs/cgroup/:ro -it --name=opsmx-collector -d opsmx11/tcollector
fi
