#!/bin/bash

# Name: AI RMF Tool 
# Description: Pulls updated list of CVE's from cvelistV5 repo. Moves CVE information from subfolders to one central folder the App.py script looks at
#              Link to cvelistV5: https://github.com/CVEProject/cvelistV5
# Date: 02/05/2024 

# pull updated CVE information from cvelistV5
(cd /home/colsons/Documents/repos/cvelistV5/; git pull)

# define source and destination dir. to move CVE info to 
SOURCE_DIR="/home/colsons/Documents/repos/cvelistV5/"
DEST_DIR="/home/colsons/Documents/repos/AI-RMF/chromadb_test/CVEdata/cvelistnosub/cves/"

# use rsync to move all changed files to destination directory used by App.py
find $SOURCE_DIR -name \*.json | rsync -av --files-from - --no-relative / $DEST_DIR
