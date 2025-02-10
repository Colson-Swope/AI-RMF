import ollama
import QueryDB

cve_context = QueryDB.get_cve_context()
query = "Find CVEs related to the following updates\n" + QueryDB.get_db_query()
# query = "what is the cve that was provided to you?"

print("Running Ollama with prompt:\n" + query + "\n\n")

response = ollama.chat(
    model="forced-cve",
    messages=[
        {
            "role": "system",
            "content": cve_context
        },
        {
            "role": "user",
            "content": query
        }
    ]
)
# print(cve_context)

print("\nAnalysis Results:")
print(response["message"]["content"])
