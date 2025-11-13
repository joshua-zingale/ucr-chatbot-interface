# database.py
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import os

# Connect to local MongoDB (same URI from MongoDB Compass or .env)
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))

db = client["ai_tutor"]
conversations = db["conversations"]  # replaces "messages" collection

# Default fallback user (for anonymous sessions)
DEFAULT_USER_ID = "anonymous"


# ─────────────────────────────────────────────
#  Create new conversation
# ─────────────────────────────────────────────
def start_conversation(title=None, user_id: str = DEFAULT_USER_ID):
    """Create a new conversation thread for this user."""
    thread_id = str(uuid4())
    conversation = {
        "thread_id": thread_id,
        "user_id": user_id,
        "title": title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
        "messages": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    conversations.insert_one(conversation)
    return thread_id


# ─────────────────────────────────────────────
#  Log message to conversation
# ─────────────────────────────────────────────
def log_message(role: str, text: str, thread_id: str, user_id: str = DEFAULT_USER_ID):
    """Add a message (user or assistant) to an existing conversation."""
    conversations.update_one(
        {"thread_id": thread_id, "user_id": user_id},
        {
            "$push": {
                "messages": {
                    "role": role,
                    "text": text,
                    "timestamp": datetime.utcnow()
                }
            },
            "$set": {"updated_at": datetime.utcnow()}
        },
        upsert=True  # ensures conversation exists even if missing
    )


# ─────────────────────────────────────────────
#  Retrieve full conversation
# ─────────────────────────────────────────────
def get_conversation(thread_id: str, user_id: str = DEFAULT_USER_ID):
    """Retrieve a single conversation and its messages."""
    convo = conversations.find_one({"thread_id": thread_id, "user_id": user_id}, {"_id": 0})
    return convo or {}


# ─────────────────────────────────────────────
#  List all user conversations
# ─────────────────────────────────────────────
def list_conversations(user_id: str = DEFAULT_USER_ID):
    """Return all conversation threads for this user, sorted by last update."""
    return list(
        conversations.find(
            {"user_id": user_id},
            {"_id": 0, "thread_id": 1, "title": 1, "updated_at": 1}
        ).sort("updated_at", -1)
    )


# ─────────────────────────────────────────────
#  Delete conversation (optional)
# ─────────────────────────────────────────────
def delete_conversation(thread_id: str, user_id: str = DEFAULT_USER_ID):
    """Delete a conversation by ID."""
    conversations.delete_one({"thread_id": thread_id, "user_id": user_id})
