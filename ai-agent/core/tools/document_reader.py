import os
from dotenv import load_dotenv
from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

load_dotenv()

# Path to ChromaDB
CHROMA_RAG_DB_PATH = os.path.join(os.getenv("VECTOR_DB_PATH", ""), "rag_documents_db")
COLLECTION_NAME = "intelliAssistant_rag"

# Gemini Embeddings and LLM
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def load_documents_from_folder(folder_path: str) -> List[Document]:
    """Load all PDFs and TXT files from a folder as LangChain Documents."""
    docs = []
    try:
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return docs

        for fname in os.listdir(folder_path):
            fpath = os.path.join(folder_path, fname)
            try:
                if fname.lower().endswith('.pdf'):
                    loader = PyPDFLoader(fpath)
                    docs.extend(fname, loader.load())
                elif fname.lower().endswith('.txt'):
                    loader = TextLoader(fpath, autodetect_encoding=True)
                    docs.extend(fname, loader.load())
            except Exception as e:
                print(f"Error loading file {fname}: {e}")
    except Exception as e:
        print(f"Error accessing folder {folder_path}: {e}")
    return docs

def ingest_documents(folder_path: str):
    """Load and ingest documents into ChromaDB with Gemini embeddings."""
    try:
        docs = load_documents_from_folder(folder_path)
        if not docs:
            print("No documents found in the folder.")
            return

        split_docs = text_splitter.split_documents(docs)

        try:
            vectordb = Chroma(
                collection_name= COLLECTION_NAME,
                embedding_function=embeddings,
                persist_directory=CHROMA_RAG_DB_PATH
            )
            vectordb.add_documents(split_docs)
            print(f"Ingested {len(split_docs)} chunks from {len(docs)} documents into RAG DB.")
        except Exception as e:
            print(f"Error with Chroma vector store: {e}")
    except Exception as e:
        print(f"Document ingestion failed: {e}")

def answer_question(query: str, k: int = 4) -> str:
    """Answer a question using RAG with Gemini and ChromaDB."""
    try:
        # Ensure documents are ingested
        # ingest_documents("ai-agent/public/documents")

        vectordb = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_RAG_DB_PATH
        )

        retriever = vectordb.as_retriever(search_kwargs={"k": k})

        # Define prompt
        prompt = PromptTemplate.from_template(
            "Use the following context to answer the question.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}"
        )

        # Build LCEL RAG chain
        rag_chain = (
            RunnableMap({
                "context": retriever,
                "question": lambda x: x
            })
            | prompt
            | llm
            | StrOutputParser()
        )

        try:
            answer = rag_chain.invoke(query)

            return answer
        except Exception as e:
            print(f"Error invoking RAG chain: {e}")
            return "Sorry, there was an error processing your question."

    except Exception as e:
        print(f"Error in RAG pipeline: {e}")
        return "An error occurred during document retrieval or question answering."