# https://www.geeksforgeeks.org/create-a-file-path-with-variables-in-python/
# https://chatgpt.com/share/67f16589-50a8-8003-b7fd-a843ba498f1c

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
user_machine_data = UserMachineInfo.get_user_machine_info(target_system_name_input)

# process AI model output and put in model_output folder for target client system 
file_folder_base = './model_output/'
file_folder_computer_name = target_system_name_output
passed_variable = file_folder_base + file_folder_computer_name
input_file = os.path.join(passed_variable, 'output.txt') 

# query model 
query = f"""
CVE INFO do not include in report = {cve_context} this is for your knowledge only. leave out of the report.  

Only say something when I tell you to. 
Do not mention specific CVE's. Only mention if CVE's exist or not. 

Here is some computer information: {user_machine_data}
Here is some update information: {user_update_data}

Instructions for the prompt below: 
    WRITE = write out word for word 
    "content in quotes' = should be your own writing based on the given info 

Now construct a report that management can use to assist with the RMF process for OS patch management. Report should be used to document compliance. 


WRITE = *** System Overview ***
WRITE = {user_machine_data}
WRITE = *** Patch Status Summary ***
WRITE = "List out pending patches, and their relavance to security based on CVE information"
WRITE = *** Compliance with RMF Controls *** 
WRITE = "advice for flaw remediation in place" 
WRITE = "advice for identification, reporting / corrective action"
WRITE = "advice for configuration management"
WRITE = "advice for vulnerability checks" 
WRITE = *** Recommended next steps ***
WRITE = "provide Review and Assess Updates"
WRITE = "provide Scheduling patch deployments"
WRITE = "provide guidance for Update documentation" 
WRITE = *** Risk Assessment ***
WRITE = "Explain the potential risk, the impact level, and mitigation plan based on current patch and CVE information" 

BE DESCRIPTIVE! do not get technical. keep it simple for general management.
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
