import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("❌ Error: GROQ_API_KEY environment variable missing.")
    exit(1)

headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}

# --- 1. WEB SCRAPING FUNCTION ---
def scrape_travel_ideas(target_url):
    print(f"🕷️ Scraping travel content from: {target_url}...")
    try:
        scrape_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(target_url, headers=scrape_headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            # Extract paragraphs and headings
            paragraphs = [p.get_text() for p in soup.find_all(['h1', 'h2', 'p']) if len(p.get_text().strip()) > 30]
            extracted_text = " ".join(paragraphs[:10]) # Limit context size
            print("✅ Web scraping successful!")
            return extracted_text
        else:
            print(f"⚠️ Scraping failed with status: {res.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Scraping exception: {str(e)}")
        return None

# Sample target URL for trends/travel news (Can be replaced dynamically)
scraped_data = scrape_travel_ideas("https://www.wiki travel.org") or "Top budget travel destinations and luxury stay recommendations."

# --- 2. FETCH GROQ ACTIVE MODELS ---
models_url = "https://api.groq.com/openai/v1/models"
available_models = []

try:
    models_response = requests.get(models_url, headers=headers)
    if models_response.status_code == 200:
        models_data = models_response.json()
        available_models = [m["id"] for m in models_data.get("data", []) if "id" in m]
except Exception as e:
    print(f"⚠️ Model fetching failed: {str(e)}")

if not available_models:
    available_models = ["llama-3.3-70b-specdec", "llama3-8b-8192", "gemma2-9b-it"]

# --- 3. DYNAMIC PROMPT (AFFILIATE + WHITE LABEL READY) ---
prompt = f"""
You are an expert Travel Affiliate Content Creator and White-Label Marketing Specialist.
Based on the following scraped travel information:
"{scraped_data[:1500]}"

Write a comprehensive, high-converting Travel Guide in Markdown (.md) format.

Structure Requirement:
1. Catchy SEO Title
2. Introduction & Overview
3. Top Recommendations & Attractions
4. Budgeting & Accommodation Tips
5. Interactive Action Sections:
   - Insert [AFFILIATE_WIDGET_PLACEHOLDER] for hotel & stay widgets (Stay22 / Booking.com).
   - Insert [WHITE_LABEL_PORTAL_LINK] for search engines/custom booking engines.

Make it highly engaging, optimized for readers, and ready for deployment.
"""

url = "https://api.groq.com/openai/v1/chat/completions"
output_content = None

print("⚡ Running Web-Scraped Aetros Pipeline...")

for model_name in available_models:
    print(f"🔄 Attempting with model: {model_name}...")
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
       
        if response.status_code == 200 and "choices" in data:
            output_content = data["choices"][0]["message"]["content"]
            print(f"✅ Success with model: {model_name}")
            break
        else:
            err = data.get("error", {}).get("message", "API Failure")
            print(f"⚠️ Warning: Model {model_name} failed. Error: {err}")

    except Exception as e:
        print(f"⚠️ Exception on {model_name}: {str(e)}")

# --- 4. SAVE OUTPUT ---
if output_content:
    os.makedirs("generated_content", exist_ok=True)
    filename = f"generated_content/scraped_affiliate_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_content)
       
    print(f"🎉 Pipeline Complete! Scraped & Generated content saved to {filename}")
else:
    print("❌ All models failed.")
    exit(1)
