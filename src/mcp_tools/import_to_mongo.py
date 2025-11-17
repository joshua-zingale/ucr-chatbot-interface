import json
from pymongo import MongoClient

MONGO_URI = "mongodb://127.0.0.1:27017"
DB_NAME = "quizdb"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for topic, questions in data.items():
    collection_name = topic.lower().replace(" ", "_")
    col = db[collection_name]
    col.delete_many({})
    col.insert_many(questions)
    print(f"Imported {len(questions)} questions into collection '{collection_name}'.")
