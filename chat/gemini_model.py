import google.generativeai as genai
import os
from collections import defaultdict
from dotenv import load_dotenv

class Model:
    """
    A class to manage interactions with the genai Generative Model API.

    Attributes:
        model_text: The generative model used for text responses.
        histories: A dictionary storing user conversation histories.
    """
    def __init__(self) -> None:
        """Initialize the Model class and configure the genai API."""
        load_dotenv()
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("API key is missing. Set it in the environment variables.")

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            raise RuntimeError("Failed to configure genai API.") from e

        self.model_text = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.histories = defaultdict(list)

    def response_model(self, username: str, message: str = "Hello?") -> str:
        """
        Generate a response from the model based on user input.

        Args:
            username: The username to track conversation history.
            message: The user's message to the model.

        Returns:
            A string containing the model's response.
        """
        history = []
        if username in self.histories:
            history = self.histories[username]
        text_model = self.model_text.start_chat(history=history)
        response = text_model.send_message(message, stream=True)
        self.histories[username].append({"user": message, "model": "".join(chunk for chunk in response)})
        return "".join(chunk for chunk in response)