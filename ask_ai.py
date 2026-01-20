import chromadb
import ollama

def ask_ollama(query):
    v_client = chromadb.PersistentClient(path="./vector_db")
    v_collection = v_client.get_or_create_collection(name="superevents_collection")

    results = v_collection.query(
        query_texts = [query],
        n_results = 5
    )

    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    ids = results['ids'][0]
    
    context = ""
    for i in range(len(docs)):
        context += f"Superevent ID: {ids[i]}\n"
        context += f"Metadata: {metadatas[i]}\n"
        context += f"Details: {docs[i]}\n\n"
                
    prompt = f"""
    You are an AI assistant knowledgeable about gravitational wave superevents.
    Analyze and answer the questions based on the following context:
    Context: {context}
    Question: {query}
    Provide a concise and accurate answer.
    """
    response = ollama.generate(model = "llama3", prompt = prompt)
    return response['response']