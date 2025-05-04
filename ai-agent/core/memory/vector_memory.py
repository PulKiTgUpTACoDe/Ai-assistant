import os
import chromadb
from google import genai
from google.generativeai import types
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class GeminiEmbeddingFunction:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

    def __call__(self, input: List[str]) -> List[List[float]]:
        """Main embedding method required by ChromaDB"""
        embeddings = []

        for text in input:
            result = self.client.models.embed_content(
                model = "gemini-embedding-exp-03-07",
                contents = text,
                config={ 'task_type':"SEMANTIC_SIMILARITY", "output_dimensionality": 64 },
            )
            # Extract the actual numerical values and flatten the list
            numerical_embeddings = [value for embedding in result.embeddings for value in embedding.values]
            embeddings.append(numerical_embeddings)
        return embeddings
    
    def name(self) -> str:
        """Required by Chroma for embedding function identification"""
        return "gemini-embedding-exp-03-07"
    
class VectorMemory:
    def __init__(self, 
                 persist_directory: str = os.getenv("VECTOR_DB_PATH"),
                 collection_name: str = "conversations"):
        
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize Chroma client and collection
        self._initialize_client()
        
    def _initialize_client(self) -> None:
        """Initialize Chroma client with default settings"""
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Get or create collection with modern parameters
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=GeminiEmbeddingFunction()
        )

    def add_conversation(self, user_message: str, ai_message: str, context: Dict[str, Any] = None) -> None:
        conversation = f"User: {user_message}\nAI: {ai_message}"
        metadata = {
            "user_message": user_message,
            "ai_message": ai_message,
            "context": json.dumps(context) if context else "{}"
        }
        
        # Generate ID based on current count
        entry_id = str(self.collection.count() + 1)
        
        self.collection.add(
            documents=[conversation],
            metadatas=[metadata],
            ids=[entry_id]
        )

    def search(self, query: str, k: int = 3) -> Any:
        results = self.collection.query(
            query_texts=[query],
            n_results=min(k, self.collection.count()),
            include=["metadatas", "distances"]
        )
        
        formatted_results = []
        for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
            formatted_results.append({
                "user_message": metadata["user_message"],
                "ai_message": metadata["ai_message"],
                "context": json.loads(metadata["context"]),
                "score": 1 - distance  # Convert cosine distance to similarity score
            })
        
        return formatted_results

    def get_relevant_context(self, query: str, k: int = 3) -> dict:
        results = self.search(query, k)
        
        if not results:
            return {"result": "", "error": "No relevant context found"}
        
        context = "Previous relevant conversations:\n\n"
        for i, result in enumerate(results):
            context += f"User: {result['user_message']}\nAI: {result['ai_message']}\n\n"
        
        return {"result": context.strip()}

    def reset(self) -> None:
        """Reset the vector memory by deleting the collection"""
        self.client.delete_collection(name=self.collection_name)
        self._initialize_client()
        print("Vector memory has been reset")

