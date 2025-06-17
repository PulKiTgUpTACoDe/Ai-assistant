import threading
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

load_dotenv()

# Get methods
from core.tools import speech_recognition, speech_synthesis, document_reader
from core.memory import chat_history
from core.agents.langchain_agent import llm_with_tools, llm
from core.agents.langchain_agent import tools

# Initialize components
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False


def handle_command(query, llm_tools=llm_with_tools):
    try:
        prev_conversations = chat_history_manager.get_history()
        messages = [
            SystemMessage(
                content="You are an advanced AI assistant designed to help users with a wide range of tasks and tools. You can execute various tools in parallel or in order to give the most precide output the user would need."
                "I want you to not use asterisks signs in your answers"
                "Your goal is to assist users efficiently, provide accurate information, and execute tasks seamlessly. Always prioritize user safety and confirm before performing critical actions like shutting down or restarting the system."
            ),
            HumanMessage(content=prev_conversations + "\n\n" + query)]
        
        first_response = llm_tools.invoke(messages)
        
        if hasattr(first_response, 'tool_calls') and first_response.tool_calls:
            tool_responses = []
            for tool_call in first_response.tool_calls:
                
                tool = next((t for t in tools if t.name == tool_call['name']), None)
                if tool:
                    result = tool.invoke(tool_call['args'])
                    tool_responses.append(ToolMessage(
                        content=str(result['result']),
                        tool_call_id=tool_call['id']
                    ))
            
            # Generate final response after all tool calls
            if tool_responses:
                final_response = llm.invoke(messages + [first_response] + tool_responses)
                speech_synthesis.say(final_response.content)
                chat_history_manager.add_message(query, final_response.content)

        elif first_response.content:
            speech_synthesis.say(first_response.content)
            chat_history_manager.add_message(query, first_response.content)
    
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
        