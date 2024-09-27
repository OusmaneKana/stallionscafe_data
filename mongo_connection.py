# mongo_connection.py
from pymongo import MongoClient
import pandas as pd
import streamlit as st 
def get_mongo_client(uri: str):
    return MongoClient(uri)

def get_meal_data(collection):
    records = list(collection.find({}))
    return pd.DataFrame(records)

# Use your own MongoDB URI and collection details
MONGO_URI = st.secrets.MONGO_URI
DB_NAME = st.secrets.DB_NAME
COLLECTION_NAME = st.secrets.COLLECTION_NAME

client = get_mongo_client(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
