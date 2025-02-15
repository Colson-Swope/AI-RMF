import chromadb
import UserUpdateData

# number of cves to return
limit = 10

chroma_client = chromadb.PersistentClient(path="./cve_information/cvedatabase")
collection = chroma_client.get_collection(name = "cve_collection")


def query_db(user_query, search_limit):
    results = collection.query(
        query_texts=[user_query],
        n_results=limit,
        include=['metadatas', 'documents']
    )
    return results


def format_cves(cves):
    formatted_cve_context = "List of CVEs:\n"
    for i in range(limit):
        formatted_cve_context += str(relevant_cves['ids'][0][i])
        formatted_cve_context += '\n'
        formatted_cve_context += str(relevant_cves['documents'][0][i])
        formatted_cve_context += '\n'
        formatted_cve_context += str(relevant_cves['metadatas'][0][i])
        formatted_cve_context += '\n'
        formatted_cve_context += '\n'

    return formatted_cve_context


relevant_cves = query_db(UserUpdateData.get_user_update_data(), limit)
formatted_cves = format_cves(relevant_cves)


def get_cve_context():
    return formatted_cves
