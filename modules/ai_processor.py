import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIProcessorModule:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.has_key = True
        else:
            self.has_key = False

    def generate_content(self, topic, context=""):
        if not self.has_key:
            return "⚠️ GEMINI_API_KEY is missing in your .env file."

        prompt = f"Topic: {topic}\nContext: {context}\n\nPlease generate a concise article."

        # Supported Active Models Only
        models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']

        for m in models:
            try:
                model = genai.GenerativeModel(m)
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    return response.text
            except Exception:
                continue

        return "Gemini API Error: Could not connect to API endpoints. Please check your API key."

    def process_content(self, topic, context=""):
        return self.generate_content(topic, context)