import os
from fastapi import FastAPI
import chromadb
# import ollama

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    import ollama

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    # print(results)
    context = results["documents"][0][0] if results["documents"] else ""

    if USE_MOCK_LLM:
        return {"answer": context}

    answer = ollama.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )

    return {"answer": answer["response"]}


#                For Containerization Reference Only
# --------------------------------------------------------------------------------------------
# from fastapi import FastAPI
# import chromadb
# import ollama

# app = FastAPI()
# chroma = chromadb.PersistentClient(path="./db")
# collection = chroma.get_or_create_collection("docs")
# ollama_client = ollama.Client(host="http://host.docker.internal:11434")


# @app.post("/query")
# def query(q: str):
#     results = collection.query(query_texts=[q], n_results=1)
#     # print(results)
#     context = results["documents"][0][0] if results["documents"] else ""

#     answer = ollama_client.generate(
#         model="tinyllama",
#         prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
#     )

#     return {"answer": answer["response"]}
