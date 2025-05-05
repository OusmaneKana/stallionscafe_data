# mongo_connection.py
from pymongo import MongoClient
import pandas as pd
import streamlit as st 


#MONGODB Data
MONGO_URI = st.secrets.MONGO_URI
DB_NAME = st.secrets.DB_NAME
ATTENDANCE_COLLECTION_NAME = st.secrets.ATTENDANCE_COLLECTION_NAME
PLANS_COLLECTION_NAME  = st.secrets.PLANS_COLLECTION_NAME



client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_meal_attendance_data():
    collection = db[ATTENDANCE_COLLECTION_NAME]
    records = list(collection.find({}))
    return pd.DataFrame(records)

def get_meal_plan_data():
    collection = db[PLANS_COLLECTION_NAME]
    records = list(collection.find({}))
    return pd.DataFrame(records)
