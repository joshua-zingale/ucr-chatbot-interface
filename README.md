# ucr-chatbot-interface

A chainlit-powered chat interface for the [UCR chatbot](https://github.com/joshua-zingale/ucr-chatbot-pathway-program/tree/master).


# Running the Application

First, install [uv](https://docs.astral.sh/uv/).

Second, clone the repository. Then, install the package from the root directory of the repository with

```bash
uv pip install -e .
```

Finally, start the server with

```bash
uv run -m ucr_chatbot_interface
```

You should now be able to use the application by visiting `http://127.0.0.1:8000` in your web browser.
