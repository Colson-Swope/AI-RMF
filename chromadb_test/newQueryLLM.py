import ollama
import newQueryDB
import json


cve_context = newQueryDB.get_cve_context()
query = "What is the CVE that was provided to you?\nList of CVEs:\n" + json.dumps(cve_context)

response = ollama.chat(
    model = "forced-cve",
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]
)

print("Response:\n" + response)
