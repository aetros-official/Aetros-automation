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

# Custom Styling for Ultra Premium Booking.com & Agoda Style UI
st.markdown("""
    <style>
    .top-navbar {
        background: linear-gradient(135deg, #003580, #0071c2);
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .top-navbar h1 {
        color: white;
        font-size: 1.8rem;
        margin: 0;
        font-weight: 800;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1A365D;
        text-align: center;
        margin-bottom: 20px;
    }
    .search-container {
        background-color: #FFB700;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    /* Clean Footer Styling */
    .footer-box {
        background-color: #F8FAFC;
        border-top: 1px solid #E2E8F0;
        padding: 30px 20px;
        margin-top: 40px;
        color: #475569;
        font-size: 0.9rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    .footer-column {
        min-width: 160px;
        margin-bottom: 15px;
    }
    .footer-column h4 {
        color: #003580;
        font-size: 1rem;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .footer-column ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }
    .footer-column ul li {
        margin-bottom: 6px;
    }
    .footer-column ul li a {
        color: #64748B;
        text-decoration: none;
    }
    .footer-column ul li a:hover {
        color: #0071c2;
        text-decoration: underline;
    }
    .footer-end {
        text-align: center;
        background-color: #F8FAFC;
        padding-bottom: 20px;
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
# SIDEBAR: AETROS BRANDED CONTROLS & GLOBAL PAYOUTS
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/airplane-take-off.png", width=65)
    st.title("⚙️ Aetros Admin Hub")
    st.caption("Own Brand Control & Partner Engine")
   
    st.markdown("---")
   
    with st.expander("👑 Aetros Partner Program", expanded=True):
        st.markdown("**Earn with Aetros**")
        partner_id = st.text_input("Partner/Campaign ID", value="pin_campaign_01")
        st.code(f"https://aetros-automation.streamlit.app/?ref={partner_id}", language="text")
       
        st.markdown("---")
        st.markdown("### 💳 Global Payout Setup")
        st.caption("Minimum Threshold: **$50.00**")
       
        payout_method = st.selectbox(
            "Preferred Withdrawal Method",
            ["PayPal (Global)", "Payoneer (Mastercard)", "Wise (Bank Transfer)", "Direct SWIFT Wire", "Crypto / USDT (Optional)"]
        )
       
        if "PayPal" in payout_method:
            st.text_input("PayPal Email Address", placeholder="name@example.com")
        elif "Payoneer" in payout_method:
            st.text_input("Payoneer Email / ID", placeholder="user@payoneer.com")
        elif "Wise" in payout_method:
            st.text_input("Wise Account Email / IBAN", placeholder="IBAN or Email")
        elif "SWIFT" in payout_method:
            st.text_input("Bank SWIFT / IBAN Details", placeholder="Account # & SWIFT code")
        else:
            st.text_input("USDT Wallet Address (TRC20)", placeholder="T... wallet address")
           
        st.info("ℹ️ Balances below $50 remain safely escrowed until threshold is reached.")

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
# LUXURIOUS TOP HEADER (Booking.com / Agoda Style)
# ---------------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <div>
        <h1>🌍 Aetros</h1>
        <span style="font-size: 0.85rem; color: #E2E8F0;">Global Travel & Mobility Hub</span>
    </div>
    <div>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
            💱 Currency: USD ($) | 🌐 Global Reach
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

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
# PROFESSIONAL FOOTER SECTION
# ---------------------------------------------------------
footer_html = """
<div class="footer-box">
    <div class="footer-column">
        <h4>Support & Help</h4>
        <ul>
            <li><a href="#">Contact Customer Support</a></li>
            <li><a href="#">Manage Your Bookings</a></li>
            <li><a href="#">Safety & Security</a></li>
            <li><a href="#">FAQ & Help Desk</a></li>
        </ul>
    </div>
    <div class="footer-column">
        <h4>Discover Travel</h4>
        <ul>
            <li><a href="#">Global Flight Finder</a></li>
            <li><a href="#">Luxury Resorts & Villas</a></li>
            <li><a href="#">Airport Taxi Transfers</a></li>
            <li><a href="#">Seasonal Deals</a></li>
        </ul>
    </div>
    <div class="footer-column">
        <h4>Terms & Policies</h4>
        <ul>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Terms & Conditions</a></li>
            <li><a href="#">Refund & Cancellation</a></li>
            <li><a href="#">Payout & Inactivity Rules</a></li>
        </ul>
    </div>
    <div class="footer-column">
        <h4>Partner Network</h4>
        <ul>
            <li><a href="#">Aetros Partner Program</a></li>
            <li><a href="#">Influencer Login</a></li>
            <li><a href="#">White Label Integration</a></li>
            <li><a href="#">Global Payout Options</a></li>
        </ul>
    </div>
    <div class="footer-column">
        <h4>About Aetros</h4>
        <ul>
            <li><a href="#">How Aetros Works</a></li>
            <li><a href="#">Global Mobility Hub</a></li>
            <li><a href="#">Careers & Press</a></li>
            <li><a href="#">Corporate Partnership</a></li>
        </ul>
    </div>
</div>
<div class="footer-end">
    <p>© 2026 Aetros Global Travel & Mobility Hub. All rights reserved. Powered by Autonomous Travel Tech.</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
