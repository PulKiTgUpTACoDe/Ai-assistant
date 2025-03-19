from google import genai
from openai import OpenAI
from langdetect import detect

class GeminiAI:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def chat(self, query, chat_history):
        """Handles AI conversation with language context."""

        # Detect input language
        input_lang = detect(query) if query else 'en'

        # Add language context to system message
        system_msg = f"You are a helpful assistant. Respond in {input_lang} text strictly. if the input is in Hindi then only respond in Hindi text else English."

        try:
            prompt = f"{chat_history}\n{query}"

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[system_msg, prompt]
            )

            assistant_response = response.text
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