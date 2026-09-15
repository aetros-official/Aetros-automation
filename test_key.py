import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(f"Loaded Key Status: {'Found' if api_key else 'Missing'}")

# Google AI Studio Updated 2026 Endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

headers = {'Content-Type': 'application/json'}
payload = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": "Hello Gemini, verify this API connection."}]
        }
    ]
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")
except Exception as e:
    print(f"Connection Error: {e}")