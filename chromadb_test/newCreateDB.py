import json
import chromadb

cve_dir = "./CVEdata/cvelistnosub/cves/"

client = chromadb.PersistentClient(path="./cvedatabase/")
collection = client.get_or_create_collection("cve_collection")

resources = []

def process_cve_file(filename):
    f = open(cve_dir + filename)
    cve_data = json.load(f)

    id = cve_data['cveMetadata']['cveId']
    metadata = cve_data['cveMetadata']
    affected_product = cve_data['containers']['cna']['affected'][0]['product']
    description = cve_data['containers']['cna']['descriptions'][0]['value']

    cve = {
        "id": id,
        "metadata": {
            "assigner_name": metadata['assignerShortName'],
            "date_published": metadata['datePublished'],
            "affected_product": affected_product
        },
        "document": description
    }

    if metadata and affected_product and description:
        resources.append(cve)


cve_name = "CVE-2024-25316.json"
process_cve_file(cve_name)

collection.add(
    ids=[entry['id'] for entry in resources],
    metadatas=[entry['metadata'] for entry in resources],
    documents=[entry['document'] for entry in resources]
)
