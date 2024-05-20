from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic_settings import BaseSettings
from bson import json_util
import requests
import json
from functools import lru_cache

class Environment(BaseSettings):
    database_name: str
    mongo_uri: str
    vizinhos: str

    class Config:
        env_file = ".env"

    @property
    def neighbor_list(self):
        return json.loads(self.vizinhos.replace("'", '"'))
    
    @property
    def total_neighbors(self):
        return len(self.neighbor_list)

app = FastAPI()

@lru_cache()
def get_environment() -> Environment:
    return Environment()

@app.get("/api/{_id}")
def get_document(_id: str):
    env = get_environment()
    print(f"Connecting to MongoDB at {env.mongo_uri}, using database {env.database_name}")
    mongo_client = MongoClient(env.mongo_uri)
    database = mongo_client[env.database_name]
    collection = database["listingsAndReviews"]
    
    print(f"Searching for document with _id: {_id} in local database")
    document = collection.find_one({"_id": _id})
    
    if document:
        print(f"Document found locally: {document}")
        return json_util.loads(json_util.dumps(document))
    else:
        print(f"Document with _id: {_id} not found in local database")
        raise HTTPException(status_code=404, detail="Document not found")

@app.get("/{_id}")
def get_document(_id: str, depth: int = 0):
    env = get_environment()
    print(f"Connecting to MongoDB at {env.mongo_uri}, using database {env.database_name}")
    mongo_client = MongoClient(env.mongo_uri)
    database = mongo_client[env.database_name]
    collection = database["listingsAndReviews"]
    
    print(f"Searching for document with _id: {_id} in local database")
    document = collection.find_one({"_id": _id})
    
    if document:
        print(f"Document found locally: {document}")
        return json_util.loads(json_util.dumps(document))
    elif depth < env.total_neighbors:
        print(f"total: {env.total_neighbors}.")
        print(f"Document not found locally. Searching in neighbors with depth {depth}.")
        return fetch_from_neighbors(env.neighbor_list, _id, depth + 1)
    else:
        print(f"Document with _id: {_id} not found in local database or neighbors.")
        raise HTTPException(status_code=404, detail="Document not found")

def fetch_from_neighbors(vizinhos, _id, depth):
    for vizinho in vizinhos:
        try:
            print(f"Connecting to neighbor {vizinho}")
            response = requests.get(f"http://{vizinho}/{_id}?depth={depth}")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error connecting to {vizinho}: {e}")
    print(f"Document with _id: {_id} not found in any neighbor.")
    raise HTTPException(status_code=404, detail="Document not found in any node")