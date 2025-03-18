#!/bin/bash
# Name: Project AI RMF Tool
# Date: 1/14/2025
# Description: Collects patch information from Debian based systems and sends to central server
# References:
# https://www.tecmint.com/commands-to-collect-system-and-hardware-information-in-linux/

# get system info 
DATE=$(date +"%m-%d-%Y")
TIME=$(date +"%H:%M:%S")
OS_NAME=$(hostname)
OS_VERSION=$(uname -v)
COMPUTER_NAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
USER_NAME=$(whoami)
MODEL_OUTPUT="output_${COMPUTER_NAME}"

# path to where information is stored 
mkdir ${COMPUTER_NAME}
touch ${COMPUTER_NAME}/sys_config.txt
touch ${COMPUTER_NAME}/patch_report_ai.txt

mkdir ${MODEL_OUTPUT}
touch ${MODEL_OUTPUT}/output.txt
#touch ${MODEL_OUTPUT}/pdf_output.pdf

SYSTEM_CONFIG_FILE="/home/${USER_NAME}/${COMPUTER_NAME}/sys_config.txt"
SYSTEM_PATCH_REPORT_AI_FILE="/home/${USER_NAME}/${COMPUTER_NAME}/patch_report_ai.txt"

# write system info to file 
echo -e "Date: $DATE" > $SYSTEM_CONFIG_FILE
echo -e "Time: $TIME" >> $SYSTEM_CONFIG_FILE
echo -e "OS Name: $OS_NAME" >> $SYSTEM_CONFIG_FILE
echo -e "OS Version: $OS_VERSION" >> $SYSTEM_CONFIG_FILE
echo -e "Computer Name: $COMPUTER_NAME" >> $SYSTEM_CONFIG_FILE
echo -e "IP Address: $IP_ADDR" >> $SYSTEM_CONFIG_FILE

# write security patch info to file 
sudo apt update
UPDATES=$(apt list --upgradable)
echo -e "Pending Updates:\n$UPDATES\n" > $SYSTEM_PATCH_REPORT_AI_FILE

# copy info folder to target server
INFO_FOLDER="/home/${USER_NAME}/${COMPUTER_NAME}"

scp -P 922 -r $INFO_FOLDER swopec2@kb322-18.cs.wwu.edu:/home/swopec2/Documents/GitHub/AI-RMF/chromadb_test/machine_transfer/

#scp -r $INFO_FOLDER student@172.24.24.7:/home/student/rmftool/AI-RMF/chromadb_test/machine_transfer/

scp -P 922 -r $MODEL_OUTPUT swopec2@kb322-18.cs.wwu.edu:/home/swopec2/Documents/GitHub/AI-RMF/chromadb_test/model_output/

# scp -r $INFO_FOLDER student@172.24.24.7:/home/student/rmftool/AI-RMF/chromadb_test/machine_transfer/

