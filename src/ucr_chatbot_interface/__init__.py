"""A chainlit-powered web server for interacting with an AI Tutor."""

from pathlib import Path

from chainlit.utils import mount_chainlit
import fastapi


def create_app() -> fastapi.FastAPI:
    """Generates the FastAPI application for the chatbot interface"""
    app = fastapi.FastAPI()

    mount_chainlit(app=app, target=str(Path(__file__).parent / "cl_app.py"), path="/")
    return app
