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

# Custom Styling for Ultra Premium UI
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
    </style>
""", unsafe_allow_html=True)

# Secrets & Hidden Backend Commission Tracking Setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
TP_MARKER = st.secrets.get("TP_MARKER", "384921")
STAY22_KEY = st.secrets.get("STAY22_KEY", "aetros_travel")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ---------------------------------------------------------
# SIDEBAR: 100% AETROS BRANDED (AFFILIATE + WHITE LABEL)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/airplane-take-off.png", width=65)
    st.title("⚙️ Aetros Admin Hub")
    st.caption("Own Brand Control & Partner Engine")
   
    st.markdown("---")
   
    # 1. OWN AFFILIATE PROGRAM
    with st.expander("👑 Aetros Partner Program", expanded=True):
        st.markdown("**Earn with Aetros**")
        st.caption("Generate custom tracking links for your affiliates and campaigns.")
       
        partner_id = st.text_input("Partner/Campaign ID", value="pin_campaign_01")
        st.markdown("🔗 **Your Branded Referral Link:**")
        st.code(f"https://aetros-automation.streamlit.app/?ref={partner_id}", language="text")

    # 2. WHITE LABEL ENGINE CONTROLS
    with st.expander("🏷️ Aetros White Label Engine"):
        st.text_input("Portal Title", value="Aetros Global Travel & Mobility Hub")
        st.selectbox("Default Currency", ["USD ($)", "EUR (€)", "GBP (£)", "AED (AH)", "PKR (Rs)"])
        st.text_input("White Label Domain", value="booking.aetros.com")
        st.success("✅ Aetros White Label Active")

    # 3. PINTEREST TRAFFIC HUB
    with st.expander("📌 Pinterest Campaign Hub"):
        st.write("Active Direct Landing URL:")
        st.code("https://aetros-automation.streamlit.app/", language="text")

    # 4. EARNINGS SUMMARY
    st.markdown("---")
    st.markdown("### 📊 Aetros Network Performance")
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
    "Riyadh King Khalid, KSA (RUH)": "RUH",
    "Istanbul Airport, Turkey (IST)": "IST",
    "Paris Charles de Gaulle, France (CDG)": "CDG",
    "Singapore Changi (SIN)": "SIN",
    "Bangkok Suvarnabhumi, Thailand (BKK)": "BKK",
    "Karachi Jinnah Intl, Pakistan (KHI)": "KHI",
    "Lahore Allama Iqbal Intl, Pakistan (LHE)": "LHE",
    "Islamabad Intl, Pakistan (ISB)": "ISB"
}

GLOBAL_HOTEL_LOCATIONS = {
    "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah", "Ras Al Khaimah"],
    "Saudi Arabia": ["Makkah", "Madinah", "Jeddah", "Riyadh", "Al Ula"],
    "United Kingdom": ["London", "Manchester", "Edinburgh", "Birmingham"],
    "United States": ["New York", "Los Angeles", "Miami", "Chicago", "Las Vegas"],
    "Turkey": ["Istanbul", "Antalya", "Cappadocia", "Bodrum"],
    "Thailand": ["Bangkok", "Phuket", "Pattaya", "Chiang Mai"],
    "Pakistan": ["Hunza Valley", "Skardu", "Islamabad", "Lahore", "Karachi"],
    "Switzerland": ["Zurich", "Geneva", "Interlaken", "Lucerne"],
    "Maldives": ["Male", "Maafushi", "Baa Atoll"]
}

POPULAR_TAXI_HUBS = [
    "Dubai International Airport (DXB)",
    "Downtown Dubai / Burj Khalifa Area",
    "Jeddah Airport (JED) to Makkah Hotels",
    "London Heathrow Airport (LHR)",
    "Central London / Oxford Street",
    "Istanbul Airport (IST) to Sultanahmet",
    "New York JFK Airport to Manhattan",
    "Islamabad Airport (ISB) to Blue Area",
    "Lahore Airport (LHE) to Gulberg",
    "Other Custom Address (Type Below)"
]

# Tabs UI Structure
tab_flight, tab_hotel, tab_ride, tab_ai = st.tabs([
    "✈️ Flights (Airlines)",
    "🏨 Hotels, Resorts & Villas",
    "🚕 Taxi & Car Rental",
    "✨ AI Travel Assistant"
])

# ---------------------------------------------------------
# TAB 1: FLIGHTS
# ---------------------------------------------------------
with tab_flight:
    st.markdown("### ✈️ Global Airline & Airport Network Search")
   
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        origin_type = st.radio("Origin Selection Mode", ["Dropdown List", "Type Any Airport / City"], key="ori_t")
        if origin_type == "Dropdown List":
            origin_display = st.selectbox("From (Departure)", list(POPULAR_AIRPORTS.keys()))
            origin_code = POPULAR_AIRPORTS[origin_display]
        else:
            custom_ori = st.text_input("Enter Airport / City Code", placeholder="e.g. Tokyo Haneda or HND")
            origin_code = custom_ori if custom_ori else "DXB"
           
    with col_f2:
        dest_type = st.radio("Destination Selection Mode", ["Dropdown List", "Type Any Airport / City"], key="dest_t")
        if dest_type == "Dropdown List":
            dest_display = st.selectbox("To (Arrival)", list(POPULAR_AIRPORTS.keys()), index=1)
            destination_code = POPULAR_AIRPORTS[dest_display]
        else:
            custom_dest = st.text_input("Enter Destination City / Airport", placeholder="e.g. London Gatwick or LGW")
            destination_code = custom_dest if custom_dest else "LHR"
           
    with col_f3:
        dep_date = st.date_input("Departure Date")
        cabin_class = st.selectbox("Class", ["Economy", "Premium Economy", "Business", "First Class"])

    if st.button("Search All Global Flights 🔍", type="primary"):
        with st.spinner("Connecting to Global Flight Engine..."):
            st.success(f"Live Flights Found for route: **{origin_code} ➔ {destination_code}**")
           
            sample_flights = [
                {"airline": "Emirates / Partner", "code": origin_code, "dest": destination_code, "price": "$480", "type": "Direct Non-Stop"},
                {"airline": "Qatar Airways", "code": origin_code, "dest": destination_code, "price": "$450", "type": "1 Stop (Doha)"},
                {"airline": "Turkish Airlines", "code": origin_code, "dest": destination_code, "price": "$420", "type": "1 Stop (Istanbul)"}
            ]
           
            for f_idx, flight in enumerate(sample_flights):
                st.markdown(f"""
                <div class="card-box">
                    <span class="price-tag">{flight['price']}</span>
                    <h3>✈️ {flight['airline']} <span class="badge-tag">{flight['type']}</span></h3>
                    <p style="color: #64748B;">Route: <b>{flight['code']}</b> to <b>{flight['dest']}</b> | Cabin: <b>{cabin_class}</b></p>
                </div>
                """, unsafe_allow_html=True)
               
                with st.expander(f"Instant Book Flight ({flight['price']})"):
                    with st.form(f"flight_book_{f_idx}"):
                        fn = st.text_input("Full Name (as per Passport)")
                        em = st.text_input("Email Address")
                        pp = st.text_input("Passport Number")
                        if st.form_submit_button("Confirm Booking 🎟️"):
                            if fn and em:
                                st.success(f"Ticket Reserved! Booking Confirmation sent to {em}.")
                            else:
                                st.warning("Please complete all details.")

# ---------------------------------------------------------
# TAB 2: HOTELS, RESORTS & VILLAS
# ---------------------------------------------------------
with tab_hotel:
    st.markdown("### 🏨 Worldwide Accommodations (Hotels, Resorts, Villas)")
   
    col_h1, col_h2, col_h3 = st.columns(3)
   
    with col_h1:
        c_options = list(GLOBAL_HOTEL_LOCATIONS.keys()) + ["Other Country (Type in Search Bar Below)"]
        selected_country = st.selectbox("1. Select/Search Country 🔍", c_options)

    with col_h2:
        if selected_country == "Other Country (Type in Search Bar Below)":
            selected_city = "Custom Location"
            target_city = st.text_input("2. Enter Custom City / Region / Street", placeholder="e.g. Zurich, Switzerland or Oxford Street")
        else:
            cities_list = GLOBAL_HOTEL_LOCATIONS[selected_country] + ["Other City/Street (Type Below)"]
            selected_city = st.selectbox("2. Select/Search City 🔍", cities_list)
            if selected_city == "Other City/Street (Type Below)":
                target_city = st.text_input("Enter Specific City / Street Search", placeholder="e.g. Marina District")
            else:
                target_city = f"{selected_city}, {selected_country}"

    with col_h3:
        prop_type = st.selectbox("Property Type", ["All Accommodation Types", "5-Star Luxury Resort", "Boutique Hotel", "Private Villa / Apartment", "Budget Stay"])

    manual_hotel_search = st.text_input("🔍 Direct Search Bar (Type Any Specific Hotel, Resort or Exact Address directly):", placeholder="e.g. Burj Al Arab Dubai, Atlantis The Palm, or 5th Avenue New York")

    if st.button("Search Accommodations 🔎", type="primary"):
        final_search_loc = manual_hotel_search if manual_hotel_search else (target_city if target_city else "Selected Destination")
       
        with st.spinner(f"Scanning Hotels & Resorts for '{final_search_loc}'..."):
            st.markdown(f"#### Top Stays Found for: `{final_search_loc}`")
           
            stays = [
                {"name": f"Grand Resort & Spa ({final_search_loc})", "type": "5-Star Luxury Resort", "price": "$220/night", "rating": "⭐⭐⭐⭐⭐ (4.9)"},
                {"name": f"Horizon Executive Suites ({final_search_loc})", "type": "Luxury Apartment / Villa", "price": "$160/night", "rating": "⭐⭐⭐⭐ (4.7)"},
                {"name": f"Central City Hotel ({final_search_loc})", "type": "Boutique Hotel", "price": "$95/night", "rating": "⭐⭐⭐⭐ (4.5)"}
            ]
           
            for s_idx, stay in enumerate(stays):
                st.markdown(f"""
                <div class="card-box">
                    <span class="price-tag">{stay['price']}</span>
                    <h3>🏨 {stay['name']}</h3>
                    <p><span class="badge-tag">{stay['type']}</span> | Rating: <b>{stay['rating']}</b></p>
                </div>
                """, unsafe_allow_html=True)
               
                with st.expander(f"Book Room at {stay['name']}"):
                    with st.form(f"hotel_form_{s_idx}"):
                        g_name = st.text_input("Guest Name")
                        g_phone = st.text_input("Mobile / WhatsApp Number")
                        checkin = st.date_input("Check-in Date", key=f"dt_{s_idx}")
                        if st.form_submit_button("Confirm Instant Reservation 🏨"):
                            if g_name and g_phone:
                                st.success(f"Reservation Successful for {g_name}! Voucher sent to {g_phone}.")
                            else:
                                st.warning("Please fill in contact info.")

# ---------------------------------------------------------
# TAB 3: TAXI & CAR RENTAL
# ---------------------------------------------------------
with tab_ride:
    st.markdown("### 🚕 Global Taxi, Airport Transfers & Luxury Car Rentals")
   
    col_r1, col_r2, col_r3 = st.columns(3)
   
    with col_r1:
        pu_choice = st.selectbox("1. Pick-up Location (Select/Search) 🔍", POPULAR_TAXI_HUBS)
        pu_manual = st.text_input("OR Type Exact Pick-up Address / Street:", placeholder="e.g. Hotel Front Desk / Street Name", key="pu_m")
        pickup = pu_manual if pu_manual else (pu_choice if pu_choice != "Other Custom Address (Type Below)" else "")
           
    with col_r2:
        do_choice = st.selectbox("2. Drop-off Location (Select/Search) 🔍", POPULAR_TAXI_HUBS, index=1)
        do_manual = st.text_input("OR Type Exact Drop-off Address / Street:", placeholder="e.g. Airport Terminal 3 / Specific Villa", key="do_m")
        dropoff = do_manual if do_manual else (do_choice if do_choice != "Other Custom Address (Type Below)" else "")

    with col_r3:
        ride_type = st.selectbox("Vehicle Class", ["Standard Sedan / Taxi", "Executive Luxury SUV", "Airport Shuttle Bus", "Private Chauffeur VIP"])

    if st.button("Find Rides & Transfers 🚗", type="primary"):
        if not pickup or not dropoff:
            st.warning("Please specify both Pick-up and Drop-off locations.")
        else:
            with st.spinner("Finding available drivers and vehicles..."):
                rides = [
                    {"type": ride_type, "provider": "Aetros Express Transfer", "eta": "5-10 mins", "price": "$35"},
                    {"type": "Premium VIP Chauffeur", "provider": "Global Black Car Service", "eta": "Scheduled Pick-up", "price": "$75"}
                ]
               
                for r_idx, ride in enumerate(rides):
                    st.markdown(f"""
                    <div class="card-box">
                        <span class="price-tag">{ride['price']}</span>
                        <h3>🚗 {ride['provider']} ({ride['type']})</h3>
                        <p><b>From:</b> {pickup} <br><b>To:</b> {dropoff} <br><b>Pickup Status:</b> {ride['eta']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                   
                    with st.expander(f"Book Ride ({ride['price']})"):
                        with st.form(f"ride_form_{r_idx}"):
                            r_name = st.text_input("Passenger Name")
                            r_contact = st.text_input("Phone Number for Driver SMS")
                            if st.form_submit_button("Confirm Ride Booking 🚕"):
                                if r_name and r_contact:
                                    st.success(f"Ride confirmed for {r_name}! Driver will contact via {r_contact}.")
                                else:
                                    st.warning("Please enter your name and phone number.")

# ---------------------------------------------------------
# TAB 4: AI TRAVEL ASSISTANT
# ---------------------------------------------------------
with tab_ai:
    st.markdown("### ✨ AI Travel Itinerary & Content Generator")
    ai_topic = st.text_input("Topic / Destination Itinerary", placeholder="e.g. 3-Day Travel Plan for Istanbul")
    if st.button("Generate AI Plan 🪄"):
        if not GEMINI_API_KEY:
            st.error("Gemini API key is required.")
        else:
            with st.spinner("Writing itinerary..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    res = model.generate_content(f"Create a concise, professional travel guide for: {ai_topic}")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
