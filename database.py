import sqlite3
import json
import chromadb

def create_db():
    connect = sqlite3.connect('app_database.db')
    cursor = connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superevents (
            superevent_id TEXT PRIMARY KEY,
            category TEXT,
            t_0 REAL,
            far REAL,
            labels TEXT,
            instruments TEXT,
            raw_json TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connect.commit()

    v_client = chromadb.PersistentClient(path="./vector_db")
    v_collection = v_client.get_or_create_collection(name="superevents_collection")
    return connect, v_collection

def insert_superevent(connect, v_collection, superevent):
    superevent_id = superevent['superevent_id']
    labels = ",".join(superevent.get('labels', []))
    preferred = superevent.get('preferred_event_data', {})
    instruments = preferred.get('instruments', [])
    
    cursor = connect.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO superevents 
        (superevent_id, category, t_0, far, labels, instruments, raw_json, last_updated) 
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (
        superevent_id,
        superevent.get('category'),
        superevent.get('t_0'),
        superevent.get('far'),
        labels,     
        instruments,
        json.dumps(superevent)
    ))
    connect.commit()

    v_collection.upsert(
        documents=[json.dumps(superevent)],
        ids=[superevent_id],
        metadatas=[{
            "category": superevent.get('category'),
            "far": preferred.get('far'),
            "instruments": instruments
        }]
    )



            
            
                   