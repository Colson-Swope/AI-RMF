# https://www.geeksforgeeks.org/create-a-file-path-with-variables-in-python/

import json
import ollama
import QueryDB
import UserUpdateData
import UserMachineInfo
import CreateDB
import os
import text_to_pdf
import text_to_docx
import sys 

# number of times to generate a response
num_responses = 1

# accept file arguments from manager.sh bash script 
target_system_name_input = sys.argv[1]
target_system_name_output = "output_" + target_system_name_input

# retrieve CVE context 
cve_context = QueryDB.get_cve_context(target_system_name_input)

# process machine transfer data for target client system 
user_update_data = UserUpdateData.get_user_update_data(target_system_name_input) 
user_macine_data = UserMachineInfo.get_user_machine_info(target_system_name_input)

# process AI model output and put in model_output folder for target client system 
file_folder_base = './model_output/'
file_folder_computer_name = target_system_name_output
passed_variable = file_folder_base + file_folder_computer_name
input_file = os.path.join(passed_variable, 'output.txt') 

# query model 
query = f"""
Considering the following CVEs:
{cve_context}

User's system has upgradeable packages:
{user_update_data}

For each upgradeable package in the user's system, ONLY find CVEs related to package version. 

DO NOT MENTION ANY PACKAGE THAT DOES NOT HAVE AN AFFILIATED CVE

Write EXACT format, nothing else, exactly like this: 

    At the header of the document, add this information: 
    {user_macine_data}

    
    As another heading, write: CVE List for Unpatched Programs: 
    ---
    Numbered list) 
    Name of package: *name of package with pending update  
    Current version: *current version of installed package
    Update version: *version of pending update
    Affiliated CVES: *list the CVES 
    ----
    
    After each CVE is iterated through write the following at the bottom of the report, only once, like a conclusion: 

    ---
    Patch Deployment: *give advice on patch deployment* 
    
    Operational Problems: *give advice for how to prepare for operational issues as a result of patching*
    ---
"""

# generate num_responses responses
for i in range(num_responses):
    response = ollama.chat(
        model = "forced-cve",
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]
    )
    # print("--------------- RESPONSE " + str(i) + " ------------------------------------------") 

model_response = response["message"]["content"]

print(model_response)

# write response to pdf and docx files (user will choose which one to download at a later time)
with open(input_file, 'w') as file:  
    file.write(model_response)

# create pdf and docx files 
pdf_output_file = os.path.join(passed_variable, 'pdf_output.pdf')
docx_output_file = os.path.join(passed_variable, 'docx_output.docx')

text_to_pdf.create_pdf(input_file, pdf_output_file)
text_to_docx.create_docx(input_file, docx_output_file)