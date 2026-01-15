import chainlit as cl
from llm import LLMClient
from chainlit.types import ThreadDict
from starlette.datastructures import Headers
from typing import Optional

# ---------------------------------------
# TEMP AUTH (replace with OAuth later)
# ---------------------------------------
@cl.header_auth_callback
async def auth(headers: Headers) -> Optional[cl.User]:
    return cl.User(identifier="dev-user")


# ---------------------------------------
# START CHAT
# ---------------------------------------
@cl.on_chat_start
async def on_chat_start():
    
    user = cl.user_session.get("user")
    user_id = user.identifier if user else "anonymous"


    # Create a NEW LLM session
    llm = LLMClient()
    llm.start_chat(system_prompt="You are a helpful AI tutor assistant.")
    cl.user_session.set("llm_client", llm)

    await cl.Message(
        author="assistant",
        content=f"New conversation started for **{user_id}**"
    ).send()


# ---------------------------------------
# ON USER MESSAGE
# ---------------------------------------
@cl.on_message
async def on_message(message: cl.Message):
    llm = cl.user_session.get("llm_client")
    assert llm is not None

    text = message.content.strip()

    reply = cl.Message(content="")
    buffer = ""

    for chunk in llm.send_message_stream(text): 
        buffer += chunk
        await reply.stream_token(chunk)

    await reply.send()


# ---------------------------------------------
# RESUME CHAT (PostgreSQL) + Rebuild LLM State
# ---------------------------------------------
@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
 
    print(f"Resuming thread: {thread['id']}")

    steps = thread.get("steps", [])
    history = []

    # 1. Replay old messages into the UI
    for step in steps:
        msg_type = step.get("type")
        content = step.get("output")

        if not content:
            continue
        
        author = "user" if msg_type == "user_message" else "assistant"

        # Send back to UI
        await cl.Message(author=author, content=content).send()

        # Capture for restoring LLM
        history.append({"role": author, "content": content})

    # 2. Rebuild your Gemini client
    llm = LLMClient()
    llm.start_chat(system_prompt="You are a helpful AI tutor assistant.")
    assert llm.chat is not None
    
    # 3. Re-feed only user messages to Gemini
    for h in history:
        if h["role"] == "user":
            llm.chat.send_message(h["content"])

    # 4. Save to session
    cl.user_session.set("llm_client", llm)
    cl.user_session.set("history", history)

    await cl.Message(
        author="assistant",
        content="Conversation restored — you may continue."
    ).send()
