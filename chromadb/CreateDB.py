import os
import json
import chromadb

# The amount of CVEs to put in the DB, -1 for no limit
limit = 10000

cve_dir = "./cve_information/CVEdata/cvelistnosub/cves/"

client = chromadb.PersistentClient(path="./cve_information/cvedatabase/")
collection = client.get_or_create_collection("cve_collection")

resources = []

def process_cve_file(filename):
    if filename.startswith("CVE"):
        f = open(cve_dir + filename)
        cve_data = json.load(f)

        # Extract ID
        id = cve_data.get('cveMetadata', {}).get('cveId', 'Unknown ID')

        # Extract Description
        description = (
            cve_data.get('containers', {})
                    .get('cna', {})
                    .get('descriptions', [{}])[0]
                    .get('value', 'No Description Available')
        )

        # Extract Affected Products
        affected_products = [
            entry.get('product', 'Unknown Product')
            for entry in cve_data.get('containers', {}).get('cna', {}).get('affected', [])
        ]


        # Construct the CVE
        cve = {
            "id": id,
            "metadata": {
                "affected_products": ', '.join(affected_products)
            },
            "document": description
        }

        # Add the CVE to the list of CVEs
        resources.append(cve)

count = 0
# Extract all CVEs from the cve directory
for filename in os.listdir(cve_dir):
    print("adding file " + str(count))
    process_cve_file(filename)
    count += 1
    if count > limit:
        break;


# force one of the libre office cves to be added
# libre_cve_name = "CVE-2023-2255.json"
# process_cve_file(libre_cve_name)

# Add all relevant CVEs to the database
collection.add(
    ids=[entry['id'] for entry in resources],
    metadatas=[entry['metadata'] for entry in resources],
    documents=[entry['document'] for entry in resources]
)
