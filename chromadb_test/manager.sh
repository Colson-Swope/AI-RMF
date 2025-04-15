#!/bin/bash
# Name: Project AI RMF Tool
# Date: 1/14/2025
# Description: Takes files from machine_transfer -> runs QueryLLM -> Sends output to model_output. Allows for dynamic scaling of end-point machines. 
# References: 
# https://stackoverflow.com/questions/5163144/what-are-the-special-dollar-sign-shell-variables
# https://chatgpt.com/share/67d5b050-ac04-8003-92bf-678ce225dd28


TRANSFER_DIR="./machine_transfer"
LLM="QueryLLM.py"

# create files for high level report
rm "./machine_transfer/master_query.txt"
touch "./machine_transfer/master_query.txt"
mkdir "./model_output/output_high_level_report"
touch "./model_output/output_high_level_report/pdf_output.pdf"
touch "./model_output/output_high_level_report/docx_output.docx"
touch "./model_output/output_high_level_report/output.txt"

# consolidate info for high-level report 
# iterate through each folder in machine_transfer directory 
for dir in "$TRANSFER_DIR"/*/; do
    if [ -d "$dir" ]; then
        # obtain folder name 
        folder_name=$(basename "$dir")

        cat "$TRANSFER_DIR/$folder_name/sys_config.txt" >> "$TRANSFER_DIR/master_query.txt"
        cat "$TRANSFER_DIR/$folder_name/patch_report_ai.txt" >> "$TRANSFER_DIR/master_query.txt"
    fi
done

# generate report tailored to each machine 
for dir in "$TRANSFER_DIR"/*/; do 
    if [ -d "$dir" ]; then

        # obtain folder name 
        folder_name=$(basename "$dir")

        # query LLM with folder name as argument
        python3 "$LLM" "$folder_name"

        # error checking for Python script 
        if [ $? -eq 0 ]; then
            # uncommment this line in production
            #rm -rf "$dir"
            echo "removed $dir" 
        else
            echo "LLM failed for $dir, folder not deleted"
        fi
    else
        echo "transfer dir does not exist" 
    fi
done

echo "done." 
