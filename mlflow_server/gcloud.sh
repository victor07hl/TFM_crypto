#install gcloud cli
##follow this link tutorial
## https://cloud.google.com/sdk/docs/install


#init gcloud (using SA)
# 1. generate the json file from the SA
gcloud auth activate-service-account 691601323130-compute@developer.gserviceaccount.com --key-file=tfmunir_key.json --project=tfmunir-448602

# 2. connect to vm
gcloud compute ssh --zone "us-central1-c" "mlflowserver" --project "tfmunir-448602"


#once on the machine follow this
#install the venv python package
sudo apt install python3.11-venv
sudo apt install python3-pip -y

#create enviroment
python3 -m venv mlflow_env

############################### these scripts can be set them as started scripts######
#activate the env                                                                   #
source mlflow_env/bin/activate                                                      #
                                                                                    #
#install mlflow                                                                     #
pip install mlflow                                                                  #
                                                                                    #
#run mlflow server                                                                  #
mlflow server --host 0.0.0.0 --port 8080                                            #
#####################################################################################

#create init scripts (in this case it will be create in the home directory)
nano init_script.sh
source mlflow_env/bin/activate 
mlflow server --host 0.0.0.0 --port 8080  

#then go to the machine settings and under the automatation section put the following code including
# the #! /bin/bash command
#! /bin/bash
cd /home/victormoreno
./init_script.sh


#link to access
http://34.58.215.162:8080/
