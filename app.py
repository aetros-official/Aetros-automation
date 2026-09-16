import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import requests
import os
from core.local_db import LocalDBConnector
from main import full_aetros_workflow
from modules.ai_processor import AIProcessorModule

# Page Configuration
st.set_page_config(page_title="Aetros Travel & Automation Portal", page_icon="✈️", layout="wide")

# Custom CSS for Modern UI Layout
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-box h1 {
        color: #ffffff !important;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .header-box p {
        color: #e0e0e0;
        font-size: 1.1rem;
    }
    .flight-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #2a5298;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .flight-price {
        font-size: 1.6rem;
        font-weight: bold;
        color: #2a5298;
    }
    .airline-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333333;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 1px solid #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2a5298 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top Header Banner
st.markdown("""
    <div class="header-box">
        <h1>✈️ Aetros Travel & Automation Dashboard</h1>
        <p>Live GDS Flight Search, AI Content Generator & Smart Analytics Engine</p>
    </div>
""", unsafe_allow_html=True)

# Initialize AI Engine
ai_engine = AIProcessorModule()

# Sidebar Controls
st.sidebar.title("⚙️ Dashboard Controls")
if st.sidebar.button("🚀 Run Automation Pipeline"):
    with st.spinner("Executing Workflow..."):
        full_aetros_workflow()
    st.sidebar.success("Pipeline executed successfully!")

st.sidebar.divider()
st.sidebar.info("Connected Systems: Duffel GDS API, SQLite DB & Google Sheets")

# Database Connection
db = LocalDBConnector()
conn = db.get_connection()

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "✈️ Live Flight Search (GDS)",
    "🤖 AI Content Writer",
    "📊 Analytics & Data"
])

# ----------------------------------------------------
# TAB 1: Live Flight Search
# ----------------------------------------------------
with tab1:
    st.markdown("### 🔍 Search Worldwide Flights")
    st.caption("Real-time GDS/NDC Fares and Schedules via Duffel API")

    DUFFEL_API_KEY = os.getenv("GDS_CLIENT_ID")

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            origin = st.text_input("🛫 Origin (Departure Code)", value="LHR")
        with col2:
            destination = st.text_input("🛬 Destination (Arrival Code)", value="DXB")
        with col3:
            departure_date = st.date_input("📅 Departure Date")

        search_btn = st.button("🔍 Search Flights", type="primary", use_container_width=True)

    st.divider()

    if search_btn:
        if not DUFFEL_API_KEY:
            st.error("API Key Missing! Please configure GDS_CLIENT_ID in GitHub Secrets.")
        else:
            with st.spinner("Fetching Live Flight Data from Duffel API..."):
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {DUFFEL_API_KEY}",
                    "Duffel-Version": "v2"
                }
                payload = {
                    "data": {
                        "slices": [
                            {
                                "origin": origin,
                                "destination": destination,
                                "departure_date": str(departure_date)
                            }
                        ],
                        "passengers": [{"type": "adult"}],
                        "cabin_class": "economy"
                    }
                }
                try:
                    response = requests.post("https://api.duffel.com/air/offer_requests", json=payload, headers=headers)
                    if response.status_code in [200, 201]:
                        offers = response.json().get("data", {}).get("offers", [])
                        st.success(f"Found {len(offers)} Live Flight Offers!")
                       
                        for offer in offers[:5]:
                            total_amount = offer.get("total_amount")
                            currency = offer.get("total_currency")
                            owner_name = offer.get("owner", {}).get("name", "Airline")
                            offer_id = offer.get('id')

                            st.markdown(f"""
                                <div class="flight-card">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <div class="airline-name">✈️ {owner_name}</div>
                                            <small style="color: #666;">Offer ID: {offer_id}</small>
                                        </div>
                                        <div class="flight-price">{total_amount} {currency}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("Failed to fetch flight offers. Check airport codes and date.")
                except Exception as ex:
                    st.error(f"Connection Error: {str(ex)}")

# ----------------------------------------------------
# TAB 2: AI Content Writer
# ----------------------------------------------------
with tab2:
    st.markdown("### 🤖 AI Content Rewriter & Optimizer")
    st.caption("Transform scraped travel data into blog posts and SEO content")

    try:
        df = pd.read_sql_query("SELECT * FROM scraped_backup ORDER BY id DESC", conn)
       
        if not df.empty:
            selected_url = st.selectbox("Select Page URL:", df['url'].unique())
            selected_row = df[df['url'] == selected_url].iloc[0]

            st.info(f"**Original Title:** {selected_row['title']}\n\n**Current AI Summary:** {selected_row['ai_summary']}")

            goal = st.selectbox("Select Optimization Goal:", ["blog", "seo", "social", "summary"], format_func=lambda x: x.upper())

            if st.button("✨ Optimize Content with AI", type="primary"):
                with st.spinner("AI Agent is rewriting content..."):
                    enhanced_text = ai_engine.rewrite_and_improve_content(selected_row['title'], goal=goal)
                    st.success("Optimization Complete!")
                    st.markdown(f"#### Generated Output:\n{enhanced_text}")
        else:
            st.warning("No records found in local database. Run the automation pipeline first.")
    except Exception as e:
        st.error(f"Database Error: {str(e)}")

# ----------------------------------------------------
# TAB 3: Analytics & Data
# ----------------------------------------------------
with tab3:
    st.markdown("### 📊 Performance & Analytics")
   
    try:
        if 'df' in locals() and not df.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Records Scraped", len(df))
            m2.metric("Unique URLs", df['url'].nunique())
            m3.metric("Successful Scrapes", len(df[df['status_code'] == 200]))

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Sentiment Analysis")
                sentiment_counts = df['sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                fig1 = px.pie(sentiment_counts, names='Sentiment', values='Count', hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.subheader("Status Code Breakdown")
                status_counts = df['status_code'].value_counts().reset_index()
                status_counts.columns = ['Status Code', 'Count']
                fig2 = px.bar(status_counts, x='Status Code', y='Count', text='Count', color='Status Code')
                st.plotly_chart(fig2, use_container_width=True)

            st.divider()
            st.subheader("Detailed Scraped Data")
            st.dataframe(df[['timestamp', 'url', 'title', 'sentiment', 'ai_summary', 'keywords']], use_container_width=True)
        else:
            st.warning("No analytics data available. Run the pipeline first.")
    except Exception as e:
        st.error(f"Analytics Error: {str(e)}")

# Close Database Connection
conn.close()
