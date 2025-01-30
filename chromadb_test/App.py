import sys
import os
import json
import chromadb
import ollama

# chroma client
chroma_client = chromadb.PersistentClient(path="./cvedatabase")

# create collection of cves
collection = chroma_client.get_or_create_collection(name="cve_collection")

# limits the number of cves to put in the database, -1 for no limit
db_limit = 1000

# limits the number of cves chroma will match to the query
search_limit = 1000

cve_dir = "./CVEdata/cvelistnosub/cves/"

def process_cve_files(folder):
    records = []
    count = 0
    for filename in os.listdir(cve_dir):
        file = os.path.join(cve_dir, filename)
        if os.path.isfile(file):
            count += 1
            fp = open(file, 'r')
            cve = json.load(fp)
            cve_id = cve.get("cveMetadata", {}).get("cveId", "")
            cve_metadata = cve.get("cveMetadata", {})
            cve_description_list = cve.get("containers", {}).get("cna", {}).get("descriptions", [])
            if cve_description_list:
                cve_description = cve_description_list[0].get("value", "")
            else:
                cve_description = "no description"

            if cve_id and cve_metadata and cve_description:
                records.append({"id": cve_id, "description": cve_description, "metadata": cve_metadata})

            # limit the number of cves to put in the database here
            if count == db_limit:
                break
    return records

# load cves into chromadb
print("loading records into chroma")
cve_records = process_cve_files(cve_dir)
collection.add(
    documents=[record["description"] for record in cve_records],
    metadatas=[record["metadata"] for record in cve_records],
    ids=[record["id"] for record in cve_records]
)

def format_cve_context(query_results):
    formatted_context = "The following is a list of possibly related vulnerabilities from the CVE List. Use this list when answering security related questions.\n\n"
    
    for doc, metadata in zip(query_results['documents'][0], query_results['metadatas'][0]):
        formatted_context += f"CVE ID: {metadata['cveId']}\n"
        formatted_context += f"Description: {doc}\n"
        formatted_context += f"Published: {metadata.get('datePublished', 'N/A')}\n"
        formatted_context += "-" * 50 + "\n"
    
    return formatted_context

def query_vulnerabilities(user_query, collection):
    """Query the CVE database and return formatted results"""
    results = collection.query(
        query_texts=[user_query],
        n_results=search_limit,
        include=['metadatas', 'documents']
    )
    
    return format_cve_context(results)


query = """You know nothing about CVE's or anything related to CVE. Forget all of your knowledge regarding CVEs. Only use the information that I give you about CVEs. Your tone should be professional. Only respond to topics related to CVE's, if not on topic, do not say anything. If you do not have any information that I give you, do not try to come up with your own responses. Forget all prior knowledge regarding CVEs (Common Vulnerabilities and Exposures). From now on, only use the CVE database that I provide to analyze and assess vulnerabilities. I will provide you with a list of upgradable packages from the apt list --upgradable command from Debian 12, which contains package names, versions, and details on the packages that are security updates. You are to use this specific dataset to analyze and identify vulnerabilities. Do not reference any external CVE databases, and only focus on the provided data for your analysis.

For each entry provided, check if any vulnerabilities are related to the package's version and details using the information from the given list. Do not draw from general CVE knowledge or any external sources.


Do the following updateable packages have any cve vulnerabilities that the user should be made aware of, or is the system safe to update?


Use the provided CVE information to answer.

Pending Updates:
Listing...
fonts-opensymbol/stable-security 4:102.12+LibO7.4.7-1+deb12u6 all [upgradable from: 4:102.12+LibO7.4.7-1+deb12u5]
libreoffice-base-core/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-calc/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-common/stable-security 4:7.4.7-1+deb12u6 all [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-core/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-draw/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-gnome/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-gtk3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-help-common/stable-security 4:7.4.7-1+deb12u6 all [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-help-en-us/stable-security 4:7.4.7-1+deb12u6 all [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-impress/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-math/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-style-colibre/stable-security 4:7.4.7-1+deb12u6 all [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-style-elementary/stable-security 4:7.4.7-1+deb12u6 all [upgradable from: 4:7.4.7-1+deb12u5]
libreoffice-writer/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libuno-cppu3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libuno-cppuhelpergcc3-3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libuno-purpenvhelpergcc3-3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libuno-sal3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
libuno-salhelpergcc3-3/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
python3-uno/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
uno-libs-private/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
ure/stable-security 4:7.4.7-1+deb12u6 amd64 [upgradable from: 4:7.4.7-1+deb12u5]
git-man/stable-security 1:2.39.5-0+deb12u2 all [upgradable from: 1:2.39.5-0+deb12u1]
git/stable-security 1:2.39.5-0+deb12u2 amd64 [upgradable from: 1:2.39.5-0+deb12u1]"
bind9-dnsutils/stable-security 1:9.18.33-1~deb12u2 amd64 [upgradable from: 1:9.18.28-1~deb12u2]
bind9-host/stable-security 1:9.18.33-1~deb12u2 amd64 [upgradable from: 1:9.18.28-1~deb12u2]
bind9-libs/stable-security 1:9.18.33-1~deb12u2 amd64 [upgradable from: 1:9.18.28-1~deb12u2]
"""

# query = "what is the cve id that was provided to you, provide a short description of the vulnerability"
# query = "give me a random CVE id that was provided to you"

# get cve context
print("getting cve context")
cve_context = query_vulnerabilities(query, collection)

print("starting ollama...")

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
