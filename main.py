import database
import ingest
import ask_ai

def main():
    connect, v_collection = database.create_db()

    for superevent in ingest.fetch_event():
        database.insert_superevent(connect, v_collection, superevent)
        print(superevent['superevent_id'])
        fits_path = ingest.download_skymap(superevent['superevent_id'])
    print("Superevents have been inserted into the database and vector collection.")

    query = "What are the most recent gravitational wave superevents?"
    response = ask_ai.ask_ollama(query)
    print(f"AI Response: {response}")
    connect.close()


if __name__ == "__main__":
    main()