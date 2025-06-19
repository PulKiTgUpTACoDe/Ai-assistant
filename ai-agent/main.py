import threading
from dotenv import load_dotenv

load_dotenv()

# Get methods
from core.tools import speech_recognition, speech_synthesis, document_reader
from core.memory import chat_history
from core.agents.langchain_agent import langgraph_agent
from core.agents.langchain_agent import tools

# Initialize components
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False


def handle_command(query, agent=langgraph_agent):
    try:
        prev_conversations = chat_history_manager.get_history()
        
        messages = [
            ("system", "You are an advanced AI assistant designed to help users with a wide range of tasks and tools. You can execute various tools in parallel or in order to give the most precide output the user would need."
            "I want you to not use asterisks signs in your answers"
            "Your goal is to assist users efficiently, provide accurate information, and execute tasks seamlessly. Always prioritize user safety and confirm before performing critical actions like shutting down or restarting the system.")
        ]

        if prev_conversations:
            messages.append(("user", prev_conversations))

        messages.append(("user", query))
        result = agent.invoke({"messages": messages})

        ai_message = result["messages"][-1].content
        speech_synthesis.say(ai_message)

        chat_history_manager.add_message(query, ai_message)

    except Exception as e:
        speech_synthesis.say("Sorry, I encountered an error processing that request.")
        print(f"[Agent Error] {e}")

def initialize_background_tasks():
    speech_thread = threading.Thread(target=speech_synthesis.process_speech_queue, daemon=True)
    speech_thread.start()
    
    # Start document ingestion in background
    ingest_thread = threading.Thread(target=lambda: document_reader.ingest_documents("ai-agent/public/documents"), daemon=True)
    ingest_thread.start()

if __name__ == '__main__':
    initialize_background_tasks()
    
    speech_synthesis.say('\nWelcome to AI Assistant')
    print("\nListening...")

    try:
        while True:
            query = speech_recognition.takeCommand()
            if query:
                speech_synthesis.control_queue.put_nowait("stop")
                handle_command(query)

    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        