import openai
from langdetect import detect 

class ChatBot:
    def __init__(self, api_key):
        openai.api_key = api_key
        openai.base_url = "https://api.deepseek.com/v1/"

    def chat(self, query, chat_history):
        """Handles AI conversation with language context using DeepSeek"""

        # Detect input language
        input_lang = detect(query) if query else 'en'

        # Create system message with language context
        system_msg = {
            "role": "system",
            "content": f"Respond in {input_lang} text strictly. Maintain natural conversation flow."
        }

        try:
            messages = [
                system_msg,
                {"role": "user", "content": f"{chat_history}\n{query}"}
            ]

            response = openai.ChatCompletion.create(
                model="deepseek-r1",
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )

            assistant_response = response.choices[0].message.content
            formatted_response = f"\n{assistant_response}\n" if "```" in assistant_response else assistant_response

            # Detect response language
            try:
                detect_lang = detect(assistant_response)
                detect_lang = 'hi' if detect_lang == 'hi' else 'en'
            except:
                detect_lang = 'en'

            return formatted_response, detect_lang

        except Exception as e:
            print(f"Chat error: {e}")
            return "I'm having trouble responding right now.", 'en' 