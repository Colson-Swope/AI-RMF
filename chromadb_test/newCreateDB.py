import os
import json
import chromadb

# The amount of CVEs to put in the DB, -1 for no limit
limit = 100

cve_dir = "./CVEdata/cvelistnosub/cves/"

client = chromadb.PersistentClient(path="./cvedatabase/")
collection = client.get_or_create_collection("cve_collection")

resources = []

def process_cve_file(filename):
    if filename.startswith("CVE"):
        f = open(cve_dir + filename)
        cve_data = json.load(f)

        #id = cve_data['cveMetadata']['cveId']
        #metadata = cve_data['cveMetadata']
        #affected_product = cve_data['containers']['cna']['affected'][0]['product']
        #description = cve_data['containers']['cna']['descriptions'][0]['value']


        id = cve_data.get('cveMetadata', {}).get('cveId', 'Unknown ID')

        # Extract Description (first available description)
        description = (
            cve_data.get('containers', {})
                    .get('cna', {})
                    .get('descriptions', [{}])[0]
                    .get('value', 'No Description Available')
        )

        # Extract Affected Products (list of products)
        affected_products = [
            entry.get('product', 'Unknown Product')
            for entry in cve_data.get('containers', {}).get('cna', {}).get('affected', [])
        ]


        cve = {
            "id": id,
            "metadata": {
                "affected_products": ', '.join(affected_products)
            },
            "document": description
        }

        resources.append(cve)

count = 0
for filename in os.listdir(cve_dir):
    print("adding file " + str(count))
    process_cve_file(filename)
    count += 1
    if count > limit:
        break;


# force one of the libre office cves to be added
libre_cve_name = "CVE-2023-2255.json"
process_cve_file(libre_cve_name)

collection.add(
    ids=[entry['id'] for entry in resources],
    metadatas=[entry['metadata'] for entry in resources],
    documents=[entry['document'] for entry in resources]
)
