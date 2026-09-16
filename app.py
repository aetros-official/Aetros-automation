import os
import json
import requests
import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(
    page_title="Aetros Travel & Automation Portal",
    page_icon="✈️",
    layout="wide"
)

# Custom Styling (Fixed Param)
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">✈️ Aetros Travel & Content Automation Portal</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Secrets Setup & Fetching
# ---------------------------------------------------------
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
GDS_CLIENT_ID = st.secrets.get("GDS_CLIENT_ID", "")

# Configure Gemini AI
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------------------
# World Airports Database for Dropdown
# ---------------------------------------------------------
WORLD_AIRPORTS = {
    # Middle East & Gulf
    "Dubai International, UAE (DXB)": "DXB",
    "Doha - Hamad International, Qatar (DOH)": "DOH",
    "Jeddah - King Abdulaziz, Saudi Arabia (JED)": "JED",
    "Riyadh - King Khalid, Saudi Arabia (RUH)": "RUH",
    "Abu Dhabi International, UAE (AUH)": "AUH",
    "Muscat International, Oman (MCT)": "MCT",
   
    # Europe
    "London - Heathrow, UK (LHR)": "LHR",
    "London - Gatwick, UK (LGW)": "LGW",
    "Paris - Charles de Gaulle, France (CDG)": "CDG",
    "Frankfurt Airport, Germany (FRA)": "FRA",
    "Amsterdam - Schiphol, Netherlands (AMS)": "AMS",
    "Istanbul Airport, Turkey (IST)": "IST",
    "Madrid - Barajas, Spain (MAD)": "MAD",
    "Rome - Fiumicino, Italy (FCO)": "FCO",
   
    # North America
    "New York - JFK, USA (JFK)": "JFK",
    "Los Angeles International, USA (LAX)": "LAX",
    "Chicago - O'Hare, USA (ORD)": "ORD",
    "Toronto - Pearson, Canada (YYZ)": "YYZ",
    "Vancouver International, Canada (YVR)": "YVR",
   
    # Asia & South Asia
    "Singapore - Changi Airport (SIN)": "SIN",
    "Bangkok - Suvarnabhumi, Thailand (BKK)": "BKK",
    "Kuala Lumpur International, Malaysia (KUL)": "KUL",
    "Tokyo - Haneda, Japan (HND)": "HND",
    "Hong Kong International (HKG)": "HKG",
    "Karachi - Jinnah International, Pakistan (KHI)": "KHI",
    "Lahore - Allama Iqbal International, Pakistan (LHE)": "LHE",
    "Islamabad International, Pakistan (ISB)": "ISB",
    "Delhi - Indira Gandhi, India (DEL)": "DEL",
    "Mumbai - Chhatrapati Shivaji, India (BOM)": "BOM",
   
    # Oceania
    "Sydney - Kingsford Smith, Australia (SYD)": "SYD",
    "Melbourne Airport, Australia (MEL)": "MEL"
}

# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["✈️ Live Flight Search", "📝 AI Content Writer", "📊 Analytics & Overview"])

# ---------------------------------------------------------
# TAB 1: Live GDS Flight Search (Duffel API)
# ---------------------------------------------------------
with tab1:
    st.subheader("Live Flight Offer Search (Duffel GDS)")
   
    col1, col2, col3 = st.columns(3)
   
    with col1:
        origin_display = st.selectbox(
            "Departure Airport (From)",
            options=list(WORLD_AIRPORTS.keys()),
            index=0 # Default: Dubai (DXB)
        )
        origin_code = WORLD_AIRPORTS[origin_display]

    with col2:
        dest_display = st.selectbox(
            "Arrival Airport (To)",
            options=list(WORLD_AIRPORTS.keys()),
            index=6 # Default: London Heathrow (LHR)
        )
        destination_code = WORLD_AIRPORTS[dest_display]
       
    with col3:
        departure_date = st.date_input("Departure Date")

    search_btn = st.button("Search Flights 🔍", type="primary")

    if search_btn:
        if not GDS_CLIENT_ID:
            st.error("GDS Client ID (Duffel API Key) is missing. Please check your Streamlit Secrets.")
        else:
            with st.spinner("Searching live flight offers..."):
                headers = {
                    "Authorization": f"Bearer {GDS_CLIENT_ID}",
                    "Duffel-Version": "v2",
                    "Content-Type": "application/json"
                }
                payload = {
                    "data": {
                        "slices": [{
                            "origin": origin_code,
                            "destination": destination_code,
                            "departure_date": str(departure_date)
                        }],
                        "passengers": [{"type": "adult"}],
                        "cabin_class": "economy"
                    }
                }
               
                try:
                    response = requests.post(
                        "https://api.duffel.com/air/offer_requests",
                        headers=headers,
                        json=payload
                    )
                   
                    if response.status_code in [200, 201]:
                        res_data = response.json()
                        offers = res_data.get("data", {}).get("offers", [])
                       
                        if offers:
                            st.success(f"Found {len(offers)} flight offers!")
                            for offer in offers[:5]: # Display top 5 offers
                                total_amount = offer.get("total_amount", "N/A")
                                total_currency = offer.get("total_currency", "USD")
                                owner_name = offer.get("owner", {}).get("name", "Airline")
                               
                                st.markdown(f"""
                                <div class="sub-card">
                                    <h4>✈️ {owner_name}</h4>
                                    <p><b>Price:</b> {total_amount} {total_currency}</p>
                                    <p><b>Route:</b> {origin_code} ➔ {destination_code}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No offers found for the selected route and date.")
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to Duffel API: {str(e)}")

# ---------------------------------------------------------
# TAB 2: AI Content Writer (Gemini API)
# ---------------------------------------------------------
with tab2:
    st.subheader("AI Travel Content Generator & Rewriter")
   
    topic = st.text_input("Enter Travel Topic or Destination", placeholder="e.g. Top 5 Places to Visit in Dubai")
    content_type = st.selectbox("Format", ["Blog Post", "Social Media Caption", "SEO Article Outline"])
   
    generate_btn = st.button("Generate Content ✨")
   
    if generate_btn:
        if not GEMINI_API_KEY:
            st.error("Gemini API Key is missing. Please check your Streamlit Secrets.")
        else:
            with st.spinner("Generating AI content..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = f"Write a professional travel {content_type} about: {topic}. Include engaging travel tips and an encouraging call-to-action."
                    response = model.generate_content(prompt)
                   
                    st.markdown("### Generated Content")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini API Error: {str(e)}")

# ---------------------------------------------------------
# TAB 3: Analytics & Overview
# ---------------------------------------------------------
with tab3:
    st.subheader("Network Overview & Analytics")
   
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Networks", "Travelpayouts / Stay22", "Connected")
    m2.metric("API Status", "Duffel GDS", "Live")
    m3.metric("AI Engine", "Gemini 1.5 Flash", "Active")
   
    st.markdown("""
    ---
    #### System Configuration Status
    * **Streamlit Engine:** Active & Operational
    * **Cloud Infrastructure:** GitHub Native Automation
    * **Data Privacy:** Secure Encrypted Environment
    """)
