import os
import pymongo
from dotenv import load_dotenv

def get_db_connection():
    """
    Establishes a connection to the MongoDB database and returns the client,
    the database, and the two main collections.
    """
    # Load environment variables from .env file
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI not found in environment variables. Please check your .env file.")

    try:
        # Create a new client and connect to the server
        client = pymongo.MongoClient(mongo_uri)
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # Define the database and collections
        db = client.vittavivek_db
        knowledge_base = db.knowledge_base
        updates = db.updates
        
        return client, db, knowledge_base, updates
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None

# Add this function to db_utils.py
def get_latest_updates(updates_collection, limit=5):
    """
    Fetches the latest documents from the updates collection, sorted by date.
    """
    try:
        # Sort by date_published in descending order and limit the number of results
        latest = updates_collection.find().sort("date_published", -1).limit(limit)
        return list(latest)
    except Exception as e:
        print(f"Error fetching latest updates: {e}")
        return []

# You can run this file directly to test the connection
if __name__ == "__main__":
    client, db, kb, upd = get_db_connection()
    if client:
        # Do something to test, e.g., print collection names
        print(f"Database: {db.name}")
        print(f"Collections: {db.list_collection_names()}")
        client.close()