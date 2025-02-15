import json
import ollama
import newQueryDB
import UserUpdateData

# number of times to generate a response
num_responses = 1

cve_context = newQueryDB.get_cve_context()
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
    print("--------------- RESPONSE " + str(i) + " ------------------------------------------") 

model_response = response["message"]["content"]

print(model_response)

