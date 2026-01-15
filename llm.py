import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class LLMClient:
    """Interface to Gemini LLM (used inside Chainlit sessions)."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key) # pyright: ignore[reportPrivateImportUsage]

        # Default model
        self.model = genai.GenerativeModel("models/gemini-2.0-flash") # pyright: ignore[reportPrivateImportUsage]
        self.chat = None

    def start_chat(self, system_prompt: str | None = None) -> None:
        """Initialize chat session with optional system prompt."""

        if system_prompt:
            self.model = genai.GenerativeModel( # pyright: ignore[reportPrivateImportUsage]
                "models/gemini-2.0-flash", system_instruction=system_prompt
            )

        self.chat = self.model.start_chat()

    def send_message(self, message: str) -> str:
        """Send a full message (non-stream)."""
        if not self.chat:
            self.start_chat()

        assert self.chat is not None
        response = self.chat.send_message(message)
        return response.text

    def send_message_stream(self, message: str):
        """Stream Gemini's response token-by-token."""
        if not self.chat:
            self.start_chat()

        try:
            assert self.chat is not None
            response = self.chat.send_message(message, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            print(f"[ERROR] Gemini stream failed: {e}")
            yield "(Error: Gemini API call failed.)"
