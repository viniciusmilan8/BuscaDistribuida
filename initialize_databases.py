from pymongo import MongoClient
import time

def wait_for_mongo(uri, timeout=60):
    client = MongoClient(uri)
    start_time = time.time()
    while True:
        try:
            client.admin.command('ping')
            print("MongoDB is available")
            return True
        except Exception as e:
            print(f"Waiting for MongoDB... {e}")
            time.sleep(2)
            if time.time() - start_time > timeout:
                print("Timeout waiting for MongoDB")
                return False

def initialize_database(uri, db_name, data):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db["listingsAndReviews"]
    collection.insert_many(data)

if wait_for_mongo("mongodb://mongodb:27017"):
    data_api_1 = [
        {"_id": "101", "name": "Listing 101", "description": "Description of listing 101"},
        {"_id": "102", "name": "Listing 102", "description": "Description of listing 102"}
    ]

    data_api_2 = [
        {"_id": "201", "name": "Listing 201", "description": "Description of listing 201"},
        {"_id": "202", "name": "Listing 202", "description": "Description of listing 202"}
    ]

    data_api_3 = [
        {"_id": "301", "name": "Listing 301", "description": "Description of listing 301"},
        {"_id": "302", "name": "Listing 302", "description": "Description of listing 302"}
    ]

    initialize_database("mongodb://mongodb:27017", "api_1_db", data_api_1)
    initialize_database("mongodb://mongodb:27017", "api_2_db", data_api_2)
    initialize_database("mongodb://mongodb:27017", "api_3_db", data_api_3)

    print("Databases initialized successfully.")
else:
    print("Failed to connect to MongoDB within the timeout period.")