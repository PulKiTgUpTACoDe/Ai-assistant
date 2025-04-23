import threading
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# Get methods
# from core.utils.wake_word import WakeWordDetector
from core.tools import speech_recognition, speech_synthesis
from core.memory import chat_history
from core.agents.langchain_agent import llm_with_tools, llm
from core.agents.langchain_agent import tools

# Initialize components
chat_history_manager = chat_history.ChatHistory(session_only=True)
music_playing = False

# Initialize wake word
# wake_detector = WakeWordDetector(os.getenv("PICOVOICE_ACCESS_KEY"))
# wake_detector.initialize()

def handle_command(query):

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

                else:
                    speech_synthesis.say("Sorry, I can't perform that action.")

        elif first_response.content:
            speech_synthesis.say(first_response.content)
            chat_history_manager.add_message(query, first_response.content)
    
    except Exception as e:
        speech_synthesis.say("Sorry, I encountered an error processing that request.")
        print(f"[Agent Error] {e}")

# def wake_word_listener():
#     """Continuously listen for wake word"""

#     while True:
#         wake_detector.start_listening()
#         wake_detector.detected_event.wait()

#         # Word detected
#         speech_synthesis.say("Yes? How can I help you")
#         wake_detector.stop()

#         # Get command
#         query = speech_recognition.takeCommand()
#         if query:
#             handle_command(query)

if __name__ == '__main__':
    speech_synthesis.say('\nWelcome to AI Assistant')

    # Start speech processing thread
    speech_thread = threading.Thread(target=speech_synthesis.process_speech_queue, daemon=True)
    speech_thread.start()

    # Start wake word listener thread
    # wake_thread = threading.Thread(target=wake_word_listener, daemon=True)
    # wake_thread.start()

    # Initial activation message
    # speech_synthesis.say("AI assistant is now active.")

    try:
        while True:
            query = speech_recognition.takeCommand()
            if query:
                handle_command(query)
            pass

    except KeyboardInterrupt:
        print("\nShutting down...")
        # wake_detector.stop()
        chat_history_manager.end_session()
    except Exception as e:
        print(f"\nError: {e}")
        # wake_detector.stop()
        chat_history_manager.end_session()
        