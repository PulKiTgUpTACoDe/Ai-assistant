import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorMemory:
    def __init__(self, 
                 index_directory: str = os.getenv("VECTOR_DB_PATH", "database/faiss_index"),
                 model_name: str = "all-MiniLM-L6-v2",
                 dimension: int = 384):
        """
        Initialize the vector memory with FAISS index.
        
        Args:
            index_directory: Directory to store FAISS index and metadata
            model_name: Name of the sentence transformer model to use
            dimension: Dimension of the embeddings
        """
        self.index_directory = index_directory
        self.model_name = model_name
        self.dimension = dimension
        self.index_path = os.path.join(index_directory, "faiss.index")
        self.metadata_path = os.path.join(index_directory, "metadata.json")
        
        # Create model for generating embeddings
        self.model = SentenceTransformer(model_name)
        
        # Create or load FAISS index
        self._initialize_index()
        
    def _initialize_index(self) -> None:
        """Initialize or load the FAISS index and metadata."""
        # Create index directory if it doesn't exist
        os.makedirs(self.index_directory, exist_ok=True)
        
        # Load or create index
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print(f"Loaded FAISS index with {self.index.ntotal} entries")
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Creating a new one.")
                self.index = faiss.IndexFlatL2(self.dimension)
        else:
            print("Creating new FAISS index")
            self.index = faiss.IndexFlatL2(self.dimension)
        
        # Load or create metadata
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print(f"Error loading metadata: {e}. Creating empty metadata.")
                self.metadata = []
        else:
            self.metadata = []
    
    def add_conversation(self, user_message: str, ai_message: str, context: Dict[str, Any] = None) -> None:
        """
        Add a conversation pair to the vector memory.
        
        Args:
            user_message: The user's message
            ai_message: The AI's response
            context: Additional context about the conversation
        """
        # Concatenate messages to create a single entry
        conversation = f"User: {user_message}\nAI: {ai_message}"
        
        # Get embedding
        embedding = self.model.encode([conversation])[0]
        
        # Add to FAISS index
        faiss.normalize_L2(np.array([embedding], dtype=np.float32))
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Add metadata
        entry_id = len(self.metadata)
        metadata_entry = {
            "id": entry_id,
            "user_message": user_message,
            "ai_message": ai_message,
            "context": context or {},
            "timestamp": os.path.getmtime(self.index_path) if os.path.exists(self.index_path) else 0
        }
        self.metadata.append(metadata_entry)
        
        # Save changes
        self._save()
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar conversations.
        
        Args:
            query: The query string
            k: Number of results to return
            
        Returns:
            List of metadata entries for similar conversations
        """
        if self.index.ntotal == 0:
            return []
        
        # Get query embedding
        query_embedding = self.model.encode([query])[0]
        query_embedding = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_embedding)
        
        # Search FAISS index
        k = min(k, self.index.ntotal)  # Don't request more results than we have
        distances, indices = self.index.search(query_embedding, k)
        
        # Return metadata for results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.metadata):  # Ensure index is valid
                result = self.metadata[idx].copy()
                result["distance"] = float(distances[0][i])
                results.append(result)
        
        return results
    
    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """
        Get relevant conversation history as context for a query.
        
        Args:
            query: The query string
            k: Number of relevant conversations to include
            
        Returns:
            String representation of relevant conversation history
        """
        results = self.search(query, k)
        
        if not results:
            return ""
        
        context = "Previous relevant conversations:\n\n"
        for i, result in enumerate(results):
            context += f"User: {result['user_message']}\nAI: {result['ai_message']}\n\n"
        
        return context.strip()
    
    def _save(self) -> None:
        """Save the FAISS index and metadata to disk."""
        try:
            faiss.write_index(self.index, self.index_path)
            
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"Error saving vector memory: {e}")
    
    def reset(self) -> None:
        """Reset the vector memory by creating a new index and clearing metadata."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        self._save()
        print("Vector memory has been reset") 