import threading
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage

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
        messages = [
            SystemMessage(
                content="You are an advanced AI assistant designed to help users with a wide range of tasks. Your capabilities include: "
                        "1. Voice Interaction: You can listen to and respond to user queries using speech recognition and synthesis. "
                        "2. Tool Integration: You have access to various tools for tasks like web searching, playing music, getting news, solving math problems, and more. "
                        "3. Context Awareness: You can recall past conversations and provide relevant context to improve interactions. "
                        "4. Visual Analysis: You can analyze images and describe what you see using object detection and image recognition. "
                        "5. System Control: You can perform system operations like shutting down, restarting, or adjusting volume. "
                        "6. Real-Time Information: You can fetch real-time data like weather, news, and current events. "
                        "7. Multi-Lingual response: You can respond in english as well as in hindi according to the language of the query and by responding hindi means responding in hindi language but in english text (whatsapp language of India)"
                        "Your goal is to assist users efficiently, provide accurate information, and execute tasks seamlessly. Always prioritize user safety and confirm before performing critical actions like shutting down or restarting the system."
            ),
            HumanMessage(content=query)]
        
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
        