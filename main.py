import database
import ingest
import ask_ai

def main():
    # Create or connect to the database and vector collection
    connect, v_collection = database.create_db()

    # Ingest superevents and insert them into the database and vector collection
    for superevent in ingest.fetch_event():
        database.insert_superevent(connect, v_collection, superevent)
    print("Superevents have been inserted into the database and vector collection.")
    # Example query to the AI assistant
    query = "What are the most recent gravitational wave superevents?"
    response = ask_ai.ask_ollama(query)
    print(f"AI Response: {response}")
    connect.close()


if __name__ == "__main__":
    main()