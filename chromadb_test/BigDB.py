import chromadb
import ollama
import os
import json
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi import FastAPI
import uvicorn

# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("json_knowledge_base")

# Function to load JSON files into ChromaDB
def load_json_to_chromadb(directory):
    file_count = 0
    existing_ids = set(collection.get()["ids"]) if collection.count() > 0 else set()  # Fetch existing file IDs
    
    for file in os.listdir(directory):
        if file.endswith(".json") and file not in existing_ids:  # Check if file is already indexed
            file_path = os.path.join(directory, file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    text = json.dumps(data)  # Convert JSON to a string
                    collection.add(
                        documents=[text],  
                        ids=[file]  
                    )
                    file_count += 1
                    if file_count % 1000 == 0:
                        print(f"Indexed {file_count} files...")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
        else:
            print(f"Skipping {file}, already indexed.")

def retrieve_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=1  # Retrieve the most relavant document
    )
    return "\n".join(results["documents"][0]) if results["documents"] else ""

def ask_ollama(query):
    context = retrieve_context(query)
    prompt = f"Use the following information to answer the question:\n\n{context}\n\nQuestion: {query}"
    
    response = ollama.chat(model="forced-cve", messages=[{"role": "user", "content": prompt}])
    
    return response['message']['content']

load_json_to_chromadb("/home/colsons/repos/AI-RMF/chromadb_test/CVEdata/cvelistnosub/cves/")

# Example query
# query = "Give me info on CVE-1999-0068"
# response = ask_ollama(query)
# print(response)

# Debug response 
debug_response = "CVE-2025-25247. only give me the written description of this vulnerability"
testing = retrieve_context(debug_response) 
print(testing)
