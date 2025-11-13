from typing import Optional, Dict
import chainlit as cl
from llm import LLMClient
from database import (
    log_message,
    start_conversation,
    list_conversations,
    get_conversation
)
import chainlit_patch


# ─────────────────────────────────────────────
#  Header Authentication (temporary bypass)
# ─────────────────────────────────────────────
@cl.header_auth_callback
def header_auth_callback(headers: Dict) -> Optional[cl.User]:
    # Temporary bypass for local testing
    return cl.User(identifier="dev-user", metadata={"role": "admin"})


# ─────────────────────────────────────────────
#  Chat start: create thread and build sidebar
# ─────────────────────────────────────────────
@cl.on_chat_start
async def start():
    user = cl.user_session.get("user")
    user_id = user.identifier if user else "anonymous"

    # Create new thread
    thread_id = start_conversation(user_id=user_id)
    cl.user_session.set("thread_id", thread_id)

    # Initialize LLM client
    llm_client = LLMClient()
    llm_client.start_chat(system_prompt="You are a helpful AI tutor assistant.")
    cl.user_session.set("llm_client", llm_client)

    await cl.Message(content=f"🧠 New conversation started for **{user_id}**").send()

    # Build sidebar on session start
    await build_sidebar(user_id)


# ─────────────────────────────────────────────
#  Sidebar builder (persistent left panel)
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
#  Sidebar builder (persistent left panel)
# ─────────────────────────────────────────────
async def build_sidebar(user_id="anonymous"):
    convos = [
        c for c in list_conversations(user_id)
        if get_conversation(c["thread_id"], user_id).get("messages")
    ]

    if not convos:
        html = "<p class='no-convo'>🗂 No saved conversations yet.</p>"
    else:
        html = "<h3>🧠 Your Conversations</h3>"
        for convo in convos:
            html += (
                f"<button class='ucr-btn' data-thread='{convo['thread_id']}'>"
                f"🔁 {convo.get('title', 'Untitled Chat')[:38]}</button><br>"
            )

    # ✅ Correct placement of display="side"
    await cl.ChatSettings(
        elements=[
            cl.Text(name="sidebar", content=f"<div class='ucr-sidebar'>{html}</div>")
        ],
        display="side"
    ).send()

# ─────────────────────────────────────────────
#  Main handler: normal chat + sidebar actions
# ─────────────────────────────────────────────
@cl.on_message
async def main(message: cl.Message):
    text = message.content.strip()
    llm_client = cl.user_session.get("llm_client")
    thread_id = cl.user_session.get("thread_id")
    user = cl.user_session.get("user")
    user_id = user.identifier if user else "anonymous"

    # Sidebar click event → resume conversation
    if text.startswith("resume:"):
        thread_id = text.split("resume:")[-1].strip()
        await resume_conversation(thread_id, user_id)
        return

    if not isinstance(llm_client, LLMClient):
        await cl.Message(content="⚠️ LLM not initialized. Please refresh.").send()
        return

    # Normal chat flow
    log_message("user", text, thread_id, user_id)
    convo = get_conversation(thread_id, user_id)
    gemini_history = [
        {"role": m["role"], "parts": [{"text": m["text"]}]}
        for m in convo.get("messages", [])
    ] if convo else []

    llm_client.start_chat(
        system_prompt="You are a helpful AI tutor assistant.",
        history=gemini_history
    )

    msg = cl.Message(content="")
    async for chunk in stream_response(llm_client, text):
        await msg.stream_token(chunk)
    await msg.send()

    log_message("assistant", msg.content, thread_id, user_id)
    await build_sidebar(user_id)


# ─────────────────────────────────────────────
#  Resume existing conversation
# ─────────────────────────────────────────────
async def resume_conversation(thread_id, user_id):
    convo = get_conversation(thread_id, user_id)
    if not convo:
        await cl.Message(content=f"⚠️ Conversation {thread_id} not found.").send()
        return

    cl.user_session.set("thread_id", convo["thread_id"])

    llm_client = LLMClient()
    gemini_history = [
        {"role": m["role"], "parts": [{"text": m["text"]}]}
        for m in convo.get("messages", [])
    ]
    llm_client.start_chat(
        system_prompt="You are a helpful AI tutor assistant.",
        history=gemini_history
    )
    cl.user_session.set("llm_client", llm_client)

    await cl.Message(content=f"🔁 Resuming **{convo['title']}**").send()
    for m in convo["messages"]:
        await cl.Message(
            author="You" if m["role"] == "user" else "Tutor",
            content=m["text"]
        ).send()


# ─────────────────────────────────────────────
#  Stream helper
# ─────────────────────────────────────────────
async def stream_response(llm_client: LLMClient, message: str):
    for chunk in llm_client.send_message_stream(message):
        yield chunk
