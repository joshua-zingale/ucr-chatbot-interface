"""Plumbing for interacting with the AI Tutor and other APIs"""

import typing as t
from pydantic import BaseModel


class Message(BaseModel):
    """A message from a conversation history"""

    body: str
    message_id: int
    type: t.Literal["BOT_MESSAGE"] | t.Literal["STUDENT_MESSAGE"]


def get_messages(conversation_id: int) -> t.Sequence[Message]:
    """Fetch all messages belonging to a conversation"""
    return [Message(body="example message", message_id=1, type="STUDENT_MESSAGE")]
