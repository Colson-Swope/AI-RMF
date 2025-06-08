AI model: Llama 3.2 ran through Ollama

This software uses retrieval augmented generation in order to provide the AI model with CVE information.

The CVE list is pulled using bashsort.sh
CreateDB.py creates a database using information from the CVE list

```
+-----------+           +------------+
|  Endpoint | --------> |  Database  |----------|
|           |           +------------+          |
|           |\                                  |
|           | \                                 v
+-----------+  \                          +------------+
                \-----------------------> |  AI Model  |
                                          +------------+
                                              |
                                              v
                                         +----------+
                                         |  Output  |
                                         +----------+
```

QueryLLM.py and QueryDB.py are used to query the LLM and the database simultaneously. The endpoint data is used to query the database, which contains metadata inserted in CreateDB.py. It will return a list of formatted CVE information that will be used in QueryLLM.py.

QueryLLM.py contains the prompt used for report generation. The LLM uses both the prompt as well as the CVE information when generating.

The model does not need to be trained on the new CVE information, the database only needs to be updated with new CVEs.
