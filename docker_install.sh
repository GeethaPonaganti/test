#!/bin/bash
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
