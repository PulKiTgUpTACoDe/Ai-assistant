import threading
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# Get functions
from core.tools import speech_recognition, speech_synthesis, audio_player
from core.memory import chat_history
from core.agents.langchain_agent import llm_with_tools, llm
from core.agents.langchain_agent import tools

# Initialize components
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False

def handle_command(query):
    global music_playing

    if music_playing and "stop" in query.lower():
        audio_player.music_player.stop()
        music_playing = False
        return

    try:
        messages = [HumanMessage(content=query)]
        
        first_response = llm_with_tools.invoke(messages)
        
        if hasattr(first_response, 'tool_calls') and first_response.tool_calls:
            tool_responses = []
            for tool_call in first_response.tool_calls:
                tool = next((t for t in tools if t.name == tool_call['name']), None)
                if tool:
                    args = tool_call['args']

                    # Handle critical operations
                    if tool.name in ['shutdowm', 'restart', 'exit']:
                        confirmation = speech_recognition.get_confirmation(f"Are you sure you want to {tool.name}?")
                        
                        if not confirmation:
                            continue
                    
                    result = tool.invoke(args)
                    tool_responses.append(
                    ToolMessage(
                        content=str(result['result']),
                        tool_call_id=tool_call['id']
                        )
                    )
                    
                    final_response = llm.invoke(messages + [first_response] + tool_responses)
                    speech_synthesis.say(final_response.content)
                    chat_history_manager.add_message(query, final_response.content)

                    if tool.name == 'play_music':
                        music_playing = True

                else:
                    speech_synthesis.say("Sorry, I can't perform that action.")

        elif first_response.content:
            speech_synthesis.say(first_response.content)
            chat_history_manager.add_message(query, first_response.content)
    
    except Exception as e:
        speech_synthesis.say("Sorry, I encountered an error processing that request.")
        print(f"[Agent Error] {e}")

if __name__ == '__main__':
    print('\nWelcome to AI Assistant')

    # Start speech processing thread
    speech_thread = threading.Thread(target=speech_synthesis.process_speech_queue, daemon=True)
    speech_thread.start()

    # Initial activation message
    speech_synthesis.say("AI assistant is now active.")

    try:
        while True:
            query = speech_recognition.takeCommand()
            if query:
                handle_command(query)

    except KeyboardInterrupt:
        print("\nShutting down...")
        chat_history_manager.end_session()
    except Exception as e:
        print(f"\nError: {e}")
        chat_history_manager.end_session()
        