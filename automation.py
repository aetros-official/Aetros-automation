import os
import requests
from datetime import datetime

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("❌ Error: GROQ_API_KEY environment variable missing.")
    exit(1)

headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}

# 1. Fetch available active models directly from Groq API
models_url = "https://api.groq.com/openai/v1/models"
available_models = []

try:
    models_response = requests.get(models_url, headers=headers)
    if models_response.status_code == 200:
        models_data = models_response.json()
        available_models = [m["id"] for m in models_data.get("data", []) if "id" in m]
        print(f"📋 Available Active Models in your Groq Account: {available_models}")
except Exception as e:
    print(f"⚠️ Could not fetch models list: {str(e)}")

# Fallback default active models list
if not available_models:
    available_models = ["llama-3.3-70b-specdec", "llama3-8b-8192", "gemma2-9b-it", "qwen-2.5-coder-32b"]

url = "https://api.groq.com/openai/v1/chat/completions"
output_content = None

print("⚡ Running Aetros Automated Pipeline...")

for model_name in available_models:
    print(f"🔄 Attempting with model: {model_name}...")
   
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "Write a high-converting travel affiliate guide breakdown with key destinations, budgeting tips, and recommended booking links layout."
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
       
        if response.status_code == 200 and "choices" in data:
            output_content = data["choices"][0]["message"]["content"]
            print(f"✅ Success with active model: {model_name}")
            break
        else:
            err = data.get("error", {}).get("message", "API Failure")
            print(f"⚠️ Warning: Model {model_name} failed. Error: {err}")

    except Exception as e:
        print(f"⚠️ Connection Exception on {model_name}: {str(e)}")

# Save Output Content
if output_content:
    os.makedirs("generated_content", exist_ok=True)
    filename = f"generated_content/travel_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_content)
       
    print(f"🎉 Pipeline Complete! Content saved to {filename}")
else:
    print("❌ All available models failed to generate content.")
    exit(1)
