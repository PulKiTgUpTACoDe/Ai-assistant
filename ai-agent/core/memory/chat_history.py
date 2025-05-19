from .vector_memory import VectorMemory

class ChatHistory:
    def __init__(self, session_only=True):
        self.session_only = session_only
        self.session_history = []
        self.vector_memory = VectorMemory()

    def add_message(self, user_message, ai_message):
        self.session_history.append({"user": user_message, "ai": ai_message})
        
        try:
            self.vector_memory.add_conversation(user_message, ai_message)
        except Exception as e:
            print(f"Error adding to vector memory: {str(e)}")

    def get_history(self, max_messages=10):
        recent_messages = self.session_history[-max_messages:] if max_messages > 0 else self.session_history
        
        history_str = ""
        for message in recent_messages:
            history_str += f"User: {message['user']}\nAI: {message['ai']}\n"
        
        return history_str
    
    def get_relevant_context(self, query, k=3) -> dict:
        try:
            return self.vector_memory.get_relevant_context(query, k)
        except Exception as e:
            print(f"Error retrieving relevant context: {e}")
            return ""

    def reset_history(self):
        self.session_history = []
        
        if not self.session_only:
            try:
                self.vector_memory.reset()
                print("Vector memory has been reset")
            except Exception as e:
                print(f"Error resetting vector memory: {e}")
    
    def end_session(self):
        self.session_history = []
        
        if self.session_only:
            try:
                self.vector_memory.reset()
                print("Session ended - Vector memory has been cleared")
            except Exception as e:
                print(f"Error clearing vector memory on session end: {e}") 