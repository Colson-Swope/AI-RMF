#!/bin/bash
# Name: Project AI RMF Tool
# Date: 1/14/2025
# Description: Collects patch information from Debian based systems and sends to central server
# References:
# https://www.tecmint.com/commands-to-collect-system-and-hardware-information-in-linux/

# get system info 
DATE=$(date +"%m-%d-%Y")
TIME=$(date +"%H:%M:%S")
OS_NAME=$(hostnamectl | awk '/Operating System/')
OS_VERSION=$(uname -v)
COMPUTER_NAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
USER_NAME=$(whoami)
MODEL_OUTPUT="rmfclient/output_${COMPUTER_NAME}"

# path to where information is stored 
mkdir "rmfclient/${COMPUTER_NAME}"
touch "rmfclient/${COMPUTER_NAME}/sys_config.txt"
touch "rmfclient/${COMPUTER_NAME}/patch_report_ai.txt"

mkdir "${MODEL_OUTPUT}"
touch "${MODEL_OUTPUT}/output.txt"
#touch ${MODEL_OUTPUT}/pdf_output.pdf

SYSTEM_CONFIG_FILE="rmfclient/${COMPUTER_NAME}/sys_config.txt"
SYSTEM_PATCH_REPORT_AI_FILE="rmfclient/${COMPUTER_NAME}/patch_report_ai.txt"

# write system info to file
echo -e "Date: $DATE" > $SYSTEM_CONFIG_FILE
echo -e "Time: $TIME" >> $SYSTEM_CONFIG_FILE
echo -e "$OS_NAME" >> $SYSTEM_CONFIG_FILE
echo -e "OS Version: $OS_VERSION" >> $SYSTEM_CONFIG_FILE
echo -e "Computer Name: $COMPUTER_NAME" >> $SYSTEM_CONFIG_FILE
echo -e "IP Address: $IP_ADDR" >> $SYSTEM_CONFIG_FILE

# write security patch info to file 
sudo apt update
UPDATES=$(apt list --upgradable)
echo -e "Pending Updates:\n$UPDATES\n" > $SYSTEM_PATCH_REPORT_AI_FILE

# copy info folder to target server
INFO_FOLDER="rmfclient/${COMPUTER_NAME}"

scp -r $INFO_FOLDER student@172.24.24.38:/home/student/2025-ai-cybersecurity-rmf-tool/chromadb/machine_transfer/

scp -r $MODEL_OUTPUT student@172.24.24.38:/home/student/2025-ai-cybersecurity-rmf-tool/chromadb/model_output/

