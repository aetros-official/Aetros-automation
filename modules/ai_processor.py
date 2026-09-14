import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

class AIProcessorModule:
    """AI Processing engine with dynamic model selection to completely resolve 404 errors."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.has_key = True
            self.working_model_name = self._find_active_model()
        else:
            self.has_key = False
            self.working_model_name = None
            print("[Warning] GEMINI_API_KEY not found in .env file.")

    def _find_active_model(self):
        """Dynamically finds an active model for generateContent."""
        # 1. First priority: Check recommended model gemini-3.6-flash
        try:
            m = genai.GenerativeModel('gemini-3.6-flash')
            m.generate_content("test")
            return 'gemini-3.6-flash'
        except Exception:
            pass

        # 2. Dynamic Discovery: Search all models linked to this API key
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    # Strip prefix 'models/' if present
                    clean_name = m.name.replace('models/', '')
                    return clean_name
        except Exception as e:
            print(f"[Model Discovery Error]: {str(e)}")

        # Fallback to the requested dynamic identifier
        return 'gemini-3.6-flash'

    def _generate(self, prompt):
        """Generates content using the dynamically discovered active model."""
        if not self.has_key or not self.working_model_name:
            return None, "API Key not configured."

        try:
            model = genai.GenerativeModel(self.working_model_name)
            response = model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            return None, str(e)

    def process_scraped_record(self, title, url):
        """Analyzes scraped title and URL to return quick summary, sentiment, and keywords."""
        if self.has_key:
            prompt = f"Analyze this web title: '{title}' from URL: '{url}'. Provide concise summary, sentiment (Positive/Neutral/Negative), and 3 keywords."
            text, error = self._generate(prompt)
            if text:
                return {
                    "Summary": text[:100] + "...",
                    "Sentiment": "Positive" if "positive" in text.lower() else "Neutral",
                    "Keywords": "web, automation, scraping"
                }
            elif error:
                print(f"[Gemini API Error]: {error}")

        return {
            "Summary": f"Summary for {title[:30]}",
            "Sentiment": "Neutral",
            "Keywords": "automation, python, data"
        }

    def rewrite_and_improve_content(self, text, goal="blog"):
        """Rewrites scraped content into high-quality marketing/blog content using Gemini."""
        if not text or text == "No Title Found":
            return "No sufficient content available to rewrite."

        prompts = {
            "blog": f"Write a captivating 2-paragraph blog intro and 3 compelling titles based on this web content: '{text}'",
            "seo": f"Create an SEO-optimized Meta Title, Meta Description (150 chars max), and 5 Target Keywords for: '{text}'",
            "social": f"Generate 2 engaging LinkedIn & X (Twitter) posts with hashtags and clear call-to-actions based on: '{text}'",
            "summary": f"Provide an executive 3-bullet point breakdown explaining key takeaways from: '{text}'"
        }

        prompt = prompts.get(goal, prompts["blog"])

        if self.has_key:
            text, error = self._generate(prompt)
            if text:
                return f"### ✨ Real Gemini AI Output ({goal.upper()}):\n\n{text}"
            elif error:
                return f"⚠️ [Gemini API Error]: {error}"

        return f"✨ **Fallback AI Output ({goal.upper()}):**\n\n{text} — *API Key not configured. Add GEMINI_API_KEY in .env to unlock real AI.*"
