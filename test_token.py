import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GEMINI_API_KEY")

print(f"Token Loaded: {token[:12]}...")

# Step 1: Check Google OAuth / Access Token Validity
token_info_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
res_token = requests.get(token_info_url)

print("\n--- TOKEN STATUS CHECK ---")
if res_token.status_code == 200:
    print("✅ Token Status: ACTIVE!")
    print(f"Expires In: {res_token.json().get('expires_in')} seconds")
else:
    print("❌ Token Status: EXPIRED or INVALID")
    print(f"Google Response: {res_token.text}")

# Step 2: Test Call with Bearer Authentication
print("\n--- TESTING GEMINI API VIA BEARER HEADER ---")
gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "contents": [{"parts": [{"text": "Hello, respond with Status OK"}]}]
}

res_gemini = requests.post(gemini_url, json=payload, headers=headers)
print(f"Gemini API Status Code: {res_gemini.status_code}")
print(f"Gemini Response: {res_gemini.text}")