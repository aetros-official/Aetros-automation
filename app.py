import os
import json
import requests
import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(
    page_title="Aetros Global Travel & Mobility Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Ultra Premium UI & Footer
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 25px;
    }
    .card-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: 800;
        color: #059669;
        float: right;
    }
    .badge-tag {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    /* Professional Footer Styling */
    .footer-container {
        background-color: #F8FAFC;
        border-top: 1px solid #E2E8F0;
        padding: 40px 20px 20px 20px;
        margin-top: 50px;
        color: #475569;
        font-size: 0.9rem;
    }
    .footer-col h4 {
        color: #1E3A8A;
        font-size: 1rem;
        margin-bottom: 15px;
        font-weight: 700;
    }
    .footer-col ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .footer-col ul li {
        margin-bottom: 8px;
    }
    .footer-col ul li a {
        color: #64748B;
        text-decoration: none;
    }
    .footer-col ul li a:hover {
        color: #3B82F6;
        text-decoration: underline;
    }
    .footer-bottom {
        text-align: center;
        border-top: 1px solid #E2E8F0;
        margin-top: 30px;
        padding-top: 20px;
        color: #94A3B8;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# Secrets & Backend Setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------------------
# SIDEBAR: AETROS BRANDED CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/airplane-take-off.png", width=65)
    st.title("⚙️ Aetros Admin Hub")
    st.caption("Own Brand Control & Partner Engine")
   
    st.markdown("---")
   
    with st.expander("👑 Aetros Partner Program", expanded=True):
        st.markdown("**Earn with Aetros** ($50 Min. Payout)")
        partner_id = st.text_input("Partner/Campaign ID", value="pin_campaign_01")
        st.code(f"https://aetros-automation.streamlit.app/?ref={partner_id}", language="text")
        st.caption("Payout Options: PayPal, Payoneer, Wise, Crypto (USDT)")

    with st.expander("🏷️ White Label Engine"):
        st.text_input("Portal Title", value="Aetros Global Travel & Mobility Hub")
        st.selectbox("Default Currency", ["USD ($)", "EUR (€)", "GBP (£)", "PKR (Rs)"])
        st.success("✅ Aetros White Label Active")

    st.markdown("---")
    st.markdown("### 📊 Network Summary")
    c1, c2 = st.columns(2)
    c1.metric("Total Clicks", "3,420")
    c2.metric("Commissions", "$850")

# ---------------------------------------------------------
# MAIN DASHBOARD CONTENT
# ---------------------------------------------------------
st.markdown('<div class="main-header">🌍 Aetros Global Travel & Mobility Hub</div>', unsafe_allow_html=True)

POPULAR_AIRPORTS = {
    "Dubai International, UAE (DXB)": "DXB",
    "London Heathrow, UK (LHR)": "LHR",
    "New York JFK, USA (JFK)": "JFK",
    "Jeddah King Abdulaziz, KSA (JED)": "JED",
    "Istanbul Airport, Turkey (IST)": "IST",
    "Karachi Jinnah Intl, Pakistan (KHI)": "KHI"
}

GLOBAL_HOTEL_LOCATIONS = {
    "United Arab Emirates": ["Dubai", "Abu Dhabi"],
    "Saudi Arabia": ["Makkah", "Madinah", "Jeddah", "Riyadh"],
    "United Kingdom": ["London", "Manchester"],
    "Pakistan": ["Hunza Valley", "Skardu", "Islamabad", "Lahore"]
}

POPULAR_TAXI_HUBS = [
    "Dubai International Airport (DXB)",
    "Jeddah Airport (JED) to Makkah Hotels",
    "London Heathrow Airport (LHR)",
    "Islamabad Airport (ISB) to Blue Area"
]

tab_flight, tab_hotel, tab_ride, tab_ai = st.tabs([
    "✈️ Flights",
    "🏨 Hotels & Resorts",
    "🚕 Taxis & Transfers",
    "✨ AI Assistant"
])

with tab_flight:
    st.markdown("### ✈️ Global Flight Search")
    f_orig = st.selectbox("From", list(POPULAR_AIRPORTS.keys()))
    f_dest = st.selectbox("To", list(POPULAR_AIRPORTS.keys()), index=1)
    if st.button("Search Flights 🔍", type="primary"):
        st.success(f"Live flights fetched for route: **{POPULAR_AIRPORTS[f_orig]} ➔ {POPULAR_AIRPORTS[f_dest]}**")

with tab_hotel:
    st.markdown("### 🏨 Worldwide Accommodations")
    h_country = st.selectbox("Select Country", list(GLOBAL_HOTEL_LOCATIONS.keys()))
    h_city = st.selectbox("Select City", GLOBAL_HOTEL_LOCATIONS[h_country])
    if st.button("Search Accommodations 🔎", type="primary"):
        st.success(f"Top stays found for **{h_city}, {h_country}**")

with tab_ride:
    st.markdown("### 🚕 Taxis & Airport Transfers")
    r_from = st.selectbox("Pick-up Location", POPULAR_TAXI_HUBS)
    r_to = st.selectbox("Drop-off Location", POPULAR_TAXI_HUBS, index=1)
    if st.button("Find Rides 🚗", type="primary"):
        st.success(f"Transfer arranged from **{r_from}** to **{r_to}**")

with tab_ai:
    st.markdown("### ✨ AI Travel Assistant")
    topic = st.text_input("Enter Destination or Plan", placeholder="e.g. 3-day trip to Dubai")
    if st.button("Generate AI Plan 🪄") and GEMINI_API_KEY:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(f"Create a short travel guide for: {topic}")
        st.write(res.text)

# ---------------------------------------------------------
# PROFESSIONAL FOOTER SECTION (Booking.com Style)
# ---------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; max-width: 1200px; margin: auto;">
       
        <div class="footer-col" style="flex: 1; min-width: 180px; margin-bottom: 20px;">
            <h4>Support & Help</h4>
            <ul>
                <li><a href="#" target="_blank">Contact Customer Support</a></li>
                <li><a href="#" target="_blank">Manage Your Bookings</a></li>
                <li><a href="#" target="_blank">Safety & Security Center</a></li>
                <li><a href="#" target="_blank">FAQ & Help Desk</a></li>
            </ul>
        </div>
       
        <div class="footer-col" style="flex: 1; min-width: 180px; margin-bottom: 20px;">
            <h4>Discover Travel</h4>
            <ul>
                <li><a href="#" target="_blank">Global Flight Finder</a></li>
                <li><a href="#" target="_blank">Luxury Resorts & Villas</a></li>
                <li><a href="#" target="_blank">Airport Taxi Transfers</a></li>
                <li><a href="#" target="_blank">Seasonal Travel Deals</a></li>
            </ul>
        </div>
       
        <div class="footer-col" style="flex: 1; min-width: 180px; margin-bottom: 20px;">
            <h4>Terms & Policies</h4>
            <ul>
                <li><a href="#" target="_blank">Privacy Policy</a></li>
                <li><a href="#" target="_blank">Terms & Conditions</a></li>
                <li><a href="#" target="_blank">Refund & Cancellation</a></li>
                <li><a href="#" target="_blank">Inactivity & Payout Rules</a></li>
            </ul>
        </div>
       
        <div class="footer-col" style="flex: 1; min-width: 180px; margin-bottom: 20px;">
            <h4>Partner Network</h4>
            <ul>
                <li><a href="#" target="_blank">Aetros Partner Program</a></li>
                <li><a href="#" target="_blank">Influencer Login</a></li>
                <li><a href="#" target="_blank">White Label Integration</a></li>
                <li><a href="#" target="_blank">Global Payout Options</a></li>
            </ul>
        </div>
       
        <div class="footer-col" style="flex: 1; min-width: 180px; margin-bottom: 20px;">
            <h4>About Aetros</h4>
            <ul>
                <li><a href="#" target="_blank">How Aetros Works</a></li>
                <li><a href="#" target="_blank">Global Mobility Hub</a></li>
                <li><a href="#" target="_blank">Careers & Press</a></li>
                <li><a href="#" target="_blank">Corporate Partnership</a></li>
            </ul>
        </div>
       
    </div>
   
    <div class="footer-bottom">
        <p>© 2026 Aetros Global Travel & Mobility Hub. All rights reserved. Powered by Autonomous Travel Tech.</p>
    </div>
</div>
""", unsafe_allow_html=True)
