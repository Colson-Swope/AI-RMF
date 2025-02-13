import json
import ollama
import newQueryDB
import UserData


cve_context = newQueryDB.get_cve_context()
user_data = UserData.get_user_data()
query = f"""
The following is a list of upgradeable packages on a system:
{user_data}
Using the following list of CVEs, are there any vulnerabilities in any of the upgradeable packages? If there are, cite which CVE the vulnerability arises from.
List of possibly related CVEs:
{cve_context}
"""

# print(query)

response = ollama.chat(
    model = "forced-cve",
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]
)

print(response["message"]["content"])
