import os
from .vector_memory import VectorMemory

class ChatHistory:
    def __init__(self, session_only=True):
        """
        Initialize the chat history manager with FAISS vector memory.
        
        Args:
            session_only: If True, history will be cleared when the session ends
        """
        self.session_only = session_only
        # Keep track of current session messages separately
        self.session_history = []
        # Initialize vector memory for semantic search
        self.vector_memory = VectorMemory()

    def add_message(self, user_message, ai_message):
        """
        Adds a new message pair to the chat history and vector memory.
        
        Args:
            user_message: The user's message
            ai_message: The AI's response
        """
        # Add to current session history
        self.session_history.append({"user": user_message, "ai": ai_message})
        
        # Also add to vector memory for semantic search
        try:
            self.vector_memory.add_conversation(user_message, ai_message)
        except Exception as e:
            print(f"Error adding to vector memory: {e}")

    def get_history(self, max_messages=50):
        """
        Returns the recent chat history as a string.
        
        Args:
            max_messages: Maximum number of recent messages to include
            
        Returns:
            String representation of chat history
        """
        # Get only the most recent messages
        recent_messages = self.session_history[-max_messages:] if max_messages > 0 else self.session_history
        
        history_str = ""
        for message in recent_messages:
            history_str += f"User: {message['user']}\nAI: {message['ai']}\n"
        
        return history_str
    
    def get_relevant_context(self, query, k=5):
        """
        Returns relevant conversation history based on semantic similarity.
        
        Args:
            query: The query to find relevant context for
            k: Number of relevant conversations to include
            
        Returns:
            String representation of relevant conversation history
        """
        try:
            return self.vector_memory.get_relevant_context(query, k)
        except Exception as e:
            print(f"Error retrieving relevant context: {e}")
            return ""

    def reset_history(self):
        """
        Clears the chat history.
        If session_only is True, only clears the session history.
        Otherwise, also resets the vector memory.
        """
        # Always clear session history
        self.session_history = []
        
        # Reset vector memory only if we're not in session-only mode
        if not self.session_only:
            try:
                self.vector_memory.reset()
                print("Vector memory has been reset")
            except Exception as e:
                print(f"Error resetting vector memory: {e}")
    
    def end_session(self):
        """
        End the current session and clean up resources.
        If session_only is True, also reset vector memory.
        """
        # Clear session history
        self.session_history = []
        
        # In session-only mode, we clear the vector memory when the session ends
        if self.session_only:
            try:
                self.vector_memory.reset()
                print("Session ended - Vector memory has been cleared")
            except Exception as e:
                print(f"Error clearing vector memory on session end: {e}") 