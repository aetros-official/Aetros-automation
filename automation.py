import os
import requests
from datetime import datetime

# --- 1. ENVIRONMENT VARIABLES & SECRETS ---
groq_key = os.getenv("GROQ_API_KEY")

# Primary GDS/CRS Credentials (Amadeus / Sabre GDS Direct Integration)
GDS_CLIENT_ID = os.getenv("GDS_CLIENT_ID", "YOUR_GDS_CLIENT_ID")
GDS_CLIENT_SECRET = os.getenv("GDS_CLIENT_SECRET", "YOUR_GDS_CLIENT_SECRET")

if not groq_key:
    print("❌ Error: GROQ_API_KEY environment variable missing.")
    exit(1)

headers = {
    "Authorization": f"Bearer {groq_key}",
    "Content-Type": "application/json"
}

# --- 2. GDS / CRS DIRECT DATA FETCHING FUNCTION ---
def fetch_live_gds_data(origin="LHR", destination="DXB"):
    print(f"📡 Connecting to Direct GDS/CRS Network (Origin: {origin} -> Dest: {destination})...")
   
    # Simulation/Fallback structure for GDS Direct API Response
    # Once API keys are added to GitHub Secrets, this connects directly to Amadeus/Sabre GDS endpoint
    if GDS_CLIENT_ID != "YOUR_GDS_CLIENT_ID":
        try:
            # Step A: Auth Token from GDS Authentication Server
            auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            auth_response = requests.post(auth_url, data={
                'grant_type': 'client_credentials',
                'client_id': GDS_CLIENT_ID,
                'client_secret': GDS_CLIENT_SECRET
            })
           
            if auth_response.status_code == 200:
                access_token = auth_response.json()['access_token']
               
                # Step B: Direct GDS Flight & CRS Hotel Search Query
                gds_search_url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate=2026-11-01&adults=1"
                gds_headers = {"Authorization": f"Bearer {access_token}"}
               
                gds_res = requests.get(gds_search_url, headers=gds_headers)
                if gds_res.status_code == 200:
                    print("✅ Successfully fetched live GDS/CRS inventory data!")
                    return str(gds_res.json())[:1500] # Pass GDS payload
        except Exception as e:
            print(f"⚠️ GDS Network Connection Alert: {str(e)}")

    # GDS Schema Template (Fallback when credentials are being set up)
    print("ℹ️ Using GDS Standard Data Schema for Engine Processing...")
    return f"GDS Source: Amadeus/Sabre Core Engine. Direct Carrier Schedules, Live Cabin Classes, Real-time CRS Hotel Rates for {destination}."

# Fetch Live GDS Payload
gds_raw_payload = fetch_live_gds_data("ISB", "IST")

# --- 3. FETCH GROQ ACTIVE MODELS ---
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

# --- 4. GDS/CRS DYNAMIC PROMPT ---
prompt = f"""
You are the Core AI Engine for an Enterprise Travel Portal connected directly to Global Distribution Systems (GDS) and Central Reservation Systems (CRS).

Raw Live GDS/CRS Data:
"{gds_raw_payload}"

Instructions:
1. Generate an authoritative, highly technical, and converting Travel & Fare Analysis Guide in Markdown (.md).
2. Highlight Direct Airline Schedules, Live Cabin Class Availabilities, and Official Hotel CRS Rates.
3. Structure for White-Label Direct Booking Integration:
   - Insert [GDS_FLIGHT_SEARCH_WIDGET] for direct airline seat booking.
   - Insert [CRS_HOTEL_INVENTORY_WIDGET] for direct hotel property booking.
4. Ensure 0% dependency on 3rd party affiliate networks. Everything must reflect direct GDS/CRS sources.
"""

url = "https://api.groq.com/openai/v1/chat/completions"
output_content = None

print("⚡ Running Direct GDS/CRS Pipeline...")

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

# --- 5. SAVE OUTPUT ---
if output_content:
    os.makedirs("generated_content", exist_ok=True)
    filename = f"generated_content/gds_direct_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
   
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_content)
       
    print(f"🎉 Pipeline Complete! GDS Direct Content saved to {filename}")
else:
    print("❌ All models failed.")
    exit(1)
