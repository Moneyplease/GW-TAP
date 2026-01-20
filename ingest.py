from ligo.gracedb.rest import GraceDb

def fetch_event():
    client = GraceDb()
    events = client.superevents(query = "category: Production", max_results = 500)
    results = []
    for event in events:
        results.append(event)
    print(f"Fetched {len(results)} events from GraceDB.")
    return results

