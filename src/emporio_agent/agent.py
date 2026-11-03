# The agent: Gemini model + tools + conversation history

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from emporio_agent import tools
from emporio_agent.prompts import build_system_prompt

load_dotenv()

DEFAULT_MODEL = "gemini-3.5-flash"

# Functions the model is allowed to call
TOOLS = [
    tools.search_products,
    tools.get_product_details,
    tools.list_categories,
    tools.get_active_promotions,
    tools.get_order_status,
    tools.register_complaint,
]


class Agent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Copy .env.example to .env and add your key.")
        self.model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        # Try again a few times when the API is busy (errors 429/503)
        retry = types.HttpRetryOptions(attempts=4, initial_delay=2.0)
        self.client = genai.Client(api_key=api_key, http_options=types.HttpOptions(retry_options=retry))
        self.reset()

    # Start a new conversation (empty history)
    def reset(self):
        config = types.GenerateContentConfig(
            system_instruction=build_system_prompt(),
            tools=TOOLS,
            temperature=0.3,
        )
        # The chat object keeps the history and runs the tools automatically
        self.chat = self.client.chats.create(model=self.model, config=config)

    # Send a customer message and return the answer and the tools used
    def send(self, message):
        history_size = len(self.chat.get_history())
        response = self.chat.send_message(message)

        # Look at the new messages in the history to find the tool calls
        tool_calls = []
        for content in self.chat.get_history()[history_size:]:
            for part in content.parts or []:
                if part.function_call:
                    tool_calls.append(f"{part.function_call.name}({dict(part.function_call.args or {})})")

        return response.text, tool_calls
