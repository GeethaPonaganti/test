#!/bin/bash
echo "Killing all docker container...."
for number in {1,2}
do
	sudo docker rm -f `sudo docker ps | awk '{print $1}' | tail -n+2`
	sleep 1
done

echo "Removing all Docker Images..."
for number in {1,2}
do
	sudo docker rmi -f `sudo docker images | awk '{print $3}' | tail -n+2`
	sleep 1
done
echo 
