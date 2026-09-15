import os
import requests
from datetime import datetime

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("❌ Error: GROQ_API_KEY environment variable missing.")
    exit(1)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama3-70b-8192",
    "messages": [
        {
            "role": "user",
            "content": "Write a high-converting travel affiliate guide breakdown with key destinations, budgeting tips, and recommended booking links layout."
        }
    ]
}

print("⚡ Running Aetros Automated Pipeline...")

try:
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
   
    if response.status_code == 200 and "choices" in data:
        output_content = data["choices"][0]["message"]["content"]
       
        os.makedirs("generated_content", exist_ok=True)
        filename = f"generated_content/travel_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
       
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output_content)
           
        print(f"✅ Success! Content generated and saved to {filename}")
    else:
        err = data.get("error", {}).get("message", "API Failure")
        print(f"❌ API Error: {err}")
        exit(1)

except Exception as e:
    print(f"❌ Connection Exception: {str(e)}")
    exit(1)
