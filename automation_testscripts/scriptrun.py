import sys
import pdb
import os
import glob
import subprocess
import paramiko
from subprocess import Popen
from subprocess import call
import re
import time
import traceback,Queue,threading
import select
import string
import yaml

#Confing yaml file location:
#yaml_locations={"config" : "/home/ubuntu/geethap/config.yml"}

with open('config.yaml', 'r') as ymlfile:
    doc = yaml.load(ymlfile)


# Creating a txt file to store log  information once test runs on server
fname = "new-test-run-logging.txt"
if os.path.isfile(fname):
    print("File does exist at this time")
    # As new-test-run-logging.txt exist, removing the file
    print " Trying to deleting text file %s : " % (fname)
    os.remove(fname)
else:
    print("No such file")

class Commands:
    def __init__(self, retry_time=0):
        self.retry_time = retry_time
        pass

    #Function to connect to server and clients
    def run_cmd(self, key, user_name, host_ip, script):
        i = 0
        while True:
                print("Trying to connect to %s)" % (host_ip))
                try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ip = doc["server"]["host_ip"]
			user = doc["server"]["user_name"]
			key = doc["server"]["key"]
			k = paramiko.RSAKey.from_private_key_file(key)
                        print ("Connecting to server... : %s \n" % ip )
                        ssh.connect( hostname = ip, username = user, pkey = k )
			print ("Connected to the server.. : %s \n" %ip )        

                except paramiko.AuthenticationException:
                        print("Authentication failed when connecting to %s" % host_ip)
                        sys.exit(1)
                except:
                        print("Could not SSH to %s, waiting for it to start" % host_ip)
                        i += 1
                        time.sleep(2)


                # After connection is successful
                # Send the comman to run perticular canary ID
		print "Running script on remote server after connection to it was  successful"
                cmd = script
                #print(cmd)
                stdin , stdout, stderr = ssh.exec_command(cmd)
                for line in stdout:
                   print line
                   with open("new-test-run-logging.txt", "a") as f:
                      f.write(line)

                # Close SSH connection
                print "About to close ssh connection to the remote server"
                ssh.close()
                return




def main():
    # Server and user information
    print "Openning yaml file"
    with open('config.yaml', 'r') as ymlfile:
        doc = yaml.load(ymlfile)

    host_ip = doc["server"]["host_ip"]
    user_name = doc["server"]["user_name"]
    key  = doc["server"]["key"]
    script = doc["script"]

    # Connecting to the server through ssh to host IP
    mytest = Commands()
    mytest.run_cmd(key, user_name, host_ip, script)   



main()




