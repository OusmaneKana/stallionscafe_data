# mongo_connection.py
from pymongo import MongoClient
import pandas as pd

def get_mongo_client(uri: str):
    return MongoClient(uri)

def get_meal_data(collection):
    records = list(collection.find({}))
    return pd.DataFrame(records)

# Use your own MongoDB URI and collection details
MONGO_URI = "mongodb+srv://python_gateway:U3E5lsB3XyrpmztB@cluster0.af3tfmj.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "NAU"
COLLECTION_NAME = "Cafeteria Attendance"

client = get_mongo_client(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
