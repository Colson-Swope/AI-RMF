import json
import ollama
import QueryDB
import UserUpdateData
# refresh DB 
import CreateDB
import os
import text_to_pdf
import text_to_docx

# number of times to generate a response
num_responses = 1

cve_context = QueryDB.get_cve_context()

# file path argument here 
user_update_data = UserUpdateData.get_user_update_data() 

query = f"""
Considering the following CVEs:
{cve_context}

User's system has upgradeable packages:
{user_update_data}

For each upgradeable package in the user's system, ONLY find CVEs related to package version. 

DO NOT MENTION ANY PACKAGE THAT DOES NOT HAVE AN AFFILIATED CVE

Write EXACT format, nothing else, exactly like this: 

    Numbered list) 
    Name of package: *name of package with pending update  
    Current version: *current version of installed package
    Update version: *version of pending update
    Affiliated CVES: *list the CVES 

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

# change to dynamic path when GUI is finished
file_folder = './model_output/output_RMF-Client01'
# replace with dynamic file path when GUI is done 
input_file = os.path.join(file_folder, 'output.txt') 

with open(input_file, 'w') as file:  
    file.write(model_response)

# replace with dynamic file path when GUI is finished 
pdf_output_file = os.path.join(file_folder, 'pdf_output.pdf')
docx_output_file = os.path.join(file_folder, 'docx_output.docx')

text_to_pdf.create_pdf(input_file, pdf_output_file)
text_to_docx.create_docx(input_file, docx_output_file)

