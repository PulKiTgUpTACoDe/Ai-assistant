import threading
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# Get methods
from core.tools import speech_recognition, speech_synthesis
from core.memory import chat_history
from core.agents.langchain_agent import llm_with_tools, llm
from core.agents.langchain_agent import tools

# Initialize components
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False


def handle_command(query):
    try:
        messages = [HumanMessage(content=query)]
        first_response = llm_with_tools.invoke(messages)
        
        if hasattr(first_response, 'tool_calls') and first_response.tool_calls:
            tool_responses = []
            for tool_call in first_response.tool_calls:
                if tool_call['name'] in ['shutdown', 'restart', 'exit']: 
                    confirmation = speech_recognition.get_confirmation(f"Are you sure you want to {tool_call['name']}?")
                    if not confirmation:
                        continue
                
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

if __name__ == '__main__':
    speech_synthesis.say('\nWelcome to AI Assistant')

    # Start speech processing thread
    speech_thread = threading.Thread(target=speech_synthesis.process_speech_queue, daemon=True)
    speech_thread.start()

    try:
        while True:
            query = speech_recognition.takeCommand()
            if query:
                speech_synthesis.control_queue.put_nowait("stop")
                handle_command(query)
            pass

    except KeyboardInterrupt:
        print("\nShutting down...")
        chat_history_manager.end_session()
    except Exception as e:
        print(f"\nError: {e}")
        chat_history_manager.end_session()
        