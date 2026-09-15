import os
import requests
from datetime import datetime

# GitHub Secrets سے API Key حاصل کرنا
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("❌ Error: GROQ_API_KEY environment variable missing.")
    exit(1)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}

# 100% Active Stable Models (Primary and Fallback)
models_to_try = [
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile"
]

output_content = None

print("⚡ Running Aetros Automated Pipeline...")

for model_name in models_to_try:
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
            print(f"✅ Success with model: {model_name}")
            break
        else:
            err = data.get("error", {}).get("message", "API Failure")
            print(f"⚠️ Warning: Model {model_name} failed. Error: {err}")

    except Exception as e:
        print(f"⚠️ Connection Exception on {model_name}: {str(e)}")

# File Saving Logic
if output_content:
    os.makedirs("generated_content", exist_ok=True)
    filename = f"generated_content/travel_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_content)
       
    print(f"🎉 Pipeline Complete! Content saved to {filename}")
else:
    print("❌ All models failed to generate content.")
    exit(1)
