import json
import ollama
import newQueryDB

# number of times to generate a response
num_responses = 10

cve_context = newQueryDB.get_cve_context()
user_data = UserData.get_user_data()

query = f"""
You are a security analyst checking system vulnerabilities.

Considering the following CVEs:
{cve_context}

The user's system has the following upgradeable packages:
{user_data}

For each upgradeable package in the user's system, find the CVEs that are related. If no CVE mentions a package, do not include it in the results. When listing the CVEs, list the CVE and the upgradeable package from the user's machine that the CVE might threaten.
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
    print(response["message"]["content"])


#print(response["message"]["content"])
