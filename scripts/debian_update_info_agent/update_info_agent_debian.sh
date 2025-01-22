#!/bin/bash
# Name: Project AI RMF Tool
# Date: 1/14/2025
# Description: Collects patch information from Debian based systems and sends to central server

# path to where information is stored 
SYSTEM_CONFIG_FILE="debian_sys_config.txt"
SYSTEM_PATCH_REPORT_AI_FILE="debian_patch_report_ai.txt"

# get system info 
DATE=$(date +"%m-%d-%Y")
TIME=$(date +"%H:%M:%S")
OS_NAME=$(hostname)
OS_VERSION=$(uname -v)
COMPUTER_NAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')

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
