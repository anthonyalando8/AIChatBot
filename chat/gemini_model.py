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
        self.histories = {}

    def response_model(self, username: str, message: str = "Hello?") -> str:
        """
        Generate a response from the model based on user input.

        Args:
            username: The username to track conversation history.
            message: The user's message to the model.

        Returns:
            A string containing the model's response.
        """
        # Ensure history is correctly formatted
        history = self.histories.get(username, [])
        
        # Reformat history to match Gemini API expectations
        formatted_history = []
        for entry in history:
            formatted_history.append({"role": "user", "parts": [entry["user"]]})
            formatted_history.append({"role": "model", "parts": [entry["model"]]})

        # Start chat with properly formatted history
        text_model = self.model_text.start_chat(history=formatted_history)

        response = text_model.send_message(message, stream=True)

        # Ensure full iteration before accessing response attributes
        collected_text = []
        for chunk in response:
            collected_text.append(chunk.text)

        model_response = "".join(collected_text)  # Combine chunks into a full response
        
        # Append new conversation entries in correct format
        history.append({"user": message, "model": model_response})
        self.histories[username] = history

        return model_response


