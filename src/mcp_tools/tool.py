from typing import List, TypedDict
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient

class MCQ(TypedDict):
    question: str
    choices: List[str]
    correct_answer: str

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["quizdb"]

mcp = FastMCP()

@mcp.tool()
def fetch_questions(subject: str) -> list[MCQ]:
    collection_name = subject.lower().replace(" ", "_")
    if collection_name not in db.list_collection_names():
        raise ValueError(f"Subject '{subject}' does not exist.")
    col = db[collection_name]
    return list(col.find({}, {"_id": 0}))

if __name__ == "__main__":
    print(fetch_questions("math"))
