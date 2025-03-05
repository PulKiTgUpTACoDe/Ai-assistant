import json
import os

class ChatHistory:
    def __init__(self, filename="chat_history.json"):
        self.filename = filename
        self.history = self.load_history()

    def load_history(self):
        """Loads chat history from a JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        else:
            return []

    def save_history(self):
        """Saves chat history to a JSON file."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving chat history: {e}")

    def add_message(self, user_message, ai_message):
        """Adds a new message pair to the chat history."""
        self.history.append({"user": user_message, "ai": ai_message}) #Ensuring the keys are lower case.
        self.save_history()

    def get_history(self):
        """Returns the chat history as a string."""
        history_str = ""
        for message in self.history:
            if isinstance(message, dict) and 'user' in message and 'ai' in message:
                history_str += f"User: {message['user']}\nAI: {message['ai']}\n"
            else:
                print(f"Warning: Invalid message in chat history: {message}")
        return history_str

    def reset_history(self):
        """Clears the chat history and saves it to the file."""
        self.history = []
        self.save_history()