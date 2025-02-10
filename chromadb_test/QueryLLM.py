import ollama
import QueryDB

cve_context = QueryDB.get_cve_context()
query = "Find CVEs related to the following updates\n" + QueryDB.get_db_query()

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
