import os
import json
import chromadb

# chroma client
chroma_client = chromadb.PersistentClient(path="./cvedatabase")

# create collection of cves
# collection = chroma_client.get_or_create_collection(name="cve_collection")
collection = chroma_client.get_collection(name = "cve_collection")


# limits the number of cves chroma will match to the query
search_limit = 1

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

query = "libreoffice"
query = """fonts-opensymbol/stable-security 4:102.12+LibO7.4.7-1+deb12u6 all [upgradable from: 4:102.12+LibO7.4.7-1+deb12u5]
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
git/stable-security 1:2.39.5-0+deb12u2 amd64 [upgradable from: 1:2.39.5-0+deb12u1]
"""

def get_cve_context():
    return query_vulnerabilities(query, collection)

def get_db_query():
    return query
