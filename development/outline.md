----
title: Upgrading the AI Tutor's Extensibility
author:
- Neftali Watkinson Medina
- Joshua Zingale
abstract: The AI Tutor is an ongoing research project by Dr. Neftali Watkinson Medina with his Ph.D. student Joshua. In order to make easier the development of the AI Tutor, the current UI must be overhauled to prioritize future extensibility while minimizing complexity. This project seeks to migrate the current AI Tutor's functionality to Chainlit, an open-source Python library for creating Chatbot-like applications. The student will create a web interface for the AI Tutor using Chainlit, leveraging its component library. The student will also integrate with the AI Tutor's current authentication system and business logic to maintain state between this student-facing application and the existent instructor-facing application. As time permits, the student will also integrate embedded questions into the chat interface and the Model Context Protocol.
----

# Introduction

Currently, the AI Tutor has a hand-rolled chat interface. This interface is good, but extending it with the features we want is a challenge.
We therefore want to adopt [Chainlit](https://docs.chainlit.io/) for our front-end for the chat feature.
Chainlit is a Python library that offers a clean interface out of the box and has many built-in components useful for chat front-ends.

The goal is to replace the current AI Tutor's chat interface entirely by Chainlit and, as time permits, to extend the AI Tutor's functionality.

# Deliverables

These should be completed in loose order from first to last.

1. Configure a working interface with an LLM to which message can be sent and from which they can be received.
    - To allow easier swapping out of the language model, do not use any API directly in the code.
    Instead, create an API in [llm.py](/src/ucr_chatbot_interface/llm.py) that can be used throughout codebase.
    - Chainlit has some [tutorials](https://docs.chainlit.io/get-started/pure-python), [examples](https://docs.chainlit.io/examples/cookbook), and a [reference](https://docs.chainlit.io/api-reference/lifecycle-hooks/on-chat-start).
2. Every message sent to and received from the LLM should be stored in a database.
    - Use [pymongo](https://www.w3schools.com/python/python_mongodb_create_db.asp) with MongoDB.
3. Each should should have a unique account on the platform.
    - A User should only have access to his messages.
    - A User's chat history should be available to him.
    - To authenticate users, use Chainlit's [Google OAuth Support](https://docs.chainlit.io/authentication/oauth#google).
4. There should be a unique chatbot configuration (e.g. system prompt and in the future MCP tools) per course.
    - To determine whether a student is in a course, we must make an API call to somewhere yet to be determined.
    - Upon entering the website, a student should be able to select which of his courses about which he would like to ask questions. 
5. Customize the styling of the interface to align UC Riverside's [brand identity](https://brand.ucr.edu/).
    - Use Chainlit's supported [customization features](https://docs.chainlit.io/customisation/overview).
6. Add the ability for the Tutor to ask students questions from within the chat.
    - The UI should be doable with something like [AskActionMessage](https://docs.chainlit.io/api-reference/ask/ask-for-action).
    - Student submissions, alongside the correctness thereof, should be stored in the database.
7. Leverage [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) to allow the addition of arbitrary tools for doing things like data retrieval.

# Starting Coding

This project is planned to continue, possibly for multiple years.
Therefore, coding with a good style is important, that others can easily understand, debug, and add to the codebase.
See [CONTRIBUTING.md](/CONTRIBUTING.md)