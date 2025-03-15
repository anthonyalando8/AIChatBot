import google.generativeai as genai
import os
from collections import defaultdict
from dotenv import load_dotenv
from . import models
from datetime import datetime


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

    def response_model(self, user, message: str = "Hello?") -> str:
        """
        Generate a response from the model based on user input.

        Args:
            username: The username to track conversation history.
            message: The user's message to the model.

        Returns:
            A string containing the model's response.
        """
        # Ensure history is correctly formatted
        try:
            history = self.histories.get(user.username, [])

            # Start chat with properly formatted history
            text_model = self.model_text.start_chat(history=history)

            response = text_model.send_message(message, stream=True)

            # Ensure full iteration before accessing response attributes
            collected_text = []

            for chunk in response:
                collected_text.append(chunk.text)

            model_response = "".join(collected_text)  # Combine chunks into a full response

            # new_history = response.history

            # self.update_user_history(user, new_history)
            
            return model_response
        
        except Exception as e:
            print(f"Error occured {e}")
            return ""
    
    def update_user_history(self, user = None, history = None):
        if not(history and user):
            print("Nothing to update")
            return
        try:
            # update user history

            self.histories[user.username] = history

            previous_history, _ = models.ChatHistory.objects.get_or_create(user=user)

            current_date_time = datetime.now()

            previous_history.chat_history = history

            previous_history.last_updated = current_date_time

            previous_history.save()

        except Exception as e:
            print(f"Error updating: {e}")
        
        
        


