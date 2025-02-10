import chromadb
import json
import os

# chroma client
chroma_client = chromadb.PersistentClient(path="./cvedatabase")

# create collection of cves
collection = chroma_client.get_or_create_collection(name="cve_collection")

# limits the number of cves to put in the database, -1 for no limit
db_limit = 10000


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
