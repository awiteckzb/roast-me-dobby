from typing import Dict, Any, List
import requests

from app.config.settings import settings
from app.prompts import DOBBY_PROMPT


class ChatAgent:
    def __init__(self, initial_features: Dict[str, Any], mode: str):
        """
        Initialize the chat agent with extracted features from the image.

        Args:
            initial_features: Dictionary containing features extracted from the uploaded image
            mode: The mode of the chat agent, either 'roast' or 'nice'
        """
        self.api_key = settings.FIREWORKS_API_KEY
        self.api_url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.model = settings.DOBBY_UNHINGED
        self.features = initial_features
        self.conversation_history = []
        self.setup_prompt(mode)

    def setup_prompt(self, mode: str):
        """Set up the initial system prompt with image features"""
        self.prompt = DOBBY_PROMPT[mode].format(
            description=self.features["description"]
        )
        print(f"Prompt: {self.prompt}")

        f"""You need to roast the absolute shit out of this person.
        Here's a description of their physical features:
        
        {self.features['description']}
        
        Do not hold back... Also, do not mention the description in your response. Just act like you saw the actual image."""

    def format_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Format the conversation history and new input for the API call"""
        messages = [
            {"role": "user", "content": self.prompt},
            {"role": "user", "content": "let me know u understand"},
            {"role": "assistant", "content": "yes papa... i understand"},
        ]

        # Add conversation history
        for msg in self.conversation_history:
            messages.append(msg)

        # Add new user input
        messages.append({"role": "user", "content": user_input})

        return messages

    def generate_response(self, user_input: str) -> str:
        """
        Generate a response based on the conversation history and new user input.

        Args:
            user_input: The latest message from the user

        Returns:
            str: The AI's response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {"model": self.model, "messages": self.format_messages(user_input)}

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Extract the response content
            response_data = response.json()
            dobby_response = response_data["choices"][0]["message"]["content"]

            # Remove quotes if present
            if dobby_response.startswith('"') and dobby_response.endswith('"'):
                dobby_response = dobby_response[1:-1]

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append(
                {"role": "assistant", "content": dobby_response}
            )

            return dobby_response

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating response: {str(e)}")
