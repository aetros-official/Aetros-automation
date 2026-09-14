import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from core.local_db import LocalDBConnector
from main import full_aetros_workflow
from modules.ai_processor import AIProcessorModule

st.set_page_config(page_title="Aetros Automation Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 Aetros Automation Platform")
st.markdown("Live Analytics & AI Content Management Dashboard")

# Initialize AI Engine
ai_engine = AIProcessorModule()

# Sidebar Controls
st.sidebar.header("🕹️ Controls")
if st.sidebar.button("▶️ Run Instant Scraper Pipeline"):
    with st.spinner("Executing Full Automation Workflow..."):
        full_aetros_workflow()
    st.sidebar.success("Pipeline executed successfully!")

st.sidebar.divider()
st.sidebar.info("Database Source: SQLite (aetros_backup.db) & Google Sheets")

# Load DB Data
db = LocalDBConnector()
conn = db.get_connection()

# Navigation Tabs
tab1, tab2 = st.tabs(["📊 Analytics & Data", "✍️ AI Content Writing Agent"])

try:
    df = pd.read_sql_query("SELECT * FROM scraped_backup ORDER BY id DESC", conn)
    conn.close()

    with tab1:
        if not df.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Records Scraped", len(df))
            m2.metric("Unique URLs", df['url'].nunique())
            m3.metric("Successful Scrapes", len(df[df['status_code'] == 200]))

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Sentiment Analysis Distribution")
                sentiment_counts = df['sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                fig1 = px.pie(sentiment_counts, names='Sentiment', values='Count', hole=0.4)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.subheader("🌐 Status Code Breakdown")
                status_counts = df['status_code'].value_counts().reset_index()
                status_counts.columns = ['Status Code', 'Count']
                fig2 = px.bar(status_counts, x='Status Code', y='Count', text='Count', color='Status Code')
                st.plotly_chart(fig2, use_container_width=True)

            st.divider()
            st.subheader("📋 Scraped Records & AI Summaries")
            st.dataframe(df[['timestamp', 'url', 'title', 'sentiment', 'ai_summary', 'keywords']], use_container_width=True)
        else:
            st.warning("No data found in local database. Run the pipeline first!")

    # TAB 2: AI Content Writing Agent
    with tab2:
        st.subheader("🤖 AI Content Rewriter & Optimizer")
        st.write("Select any scraped content from your database and let the AI rewrite or optimize it.")

        if not df.empty:
            selected_url = st.selectbox("Select Scraped Page URL:", df['url'].unique())
            selected_row = df[df['url'] == selected_url].iloc[0]

            st.info(f"**Original Title:** {selected_row['title']}\n\n**Current AI Summary:** {selected_row['ai_summary']}")

            goal = st.selectbox("Select Rewrite Goal:", ["blog", "seo", "social", "summary"], format_func=lambda x: x.upper())

            if st.button("✨ Improve Content with AI"):
                with st.spinner("AI Agent is re-writing content..."):
                    enhanced_text = ai_engine.rewrite_and_improve_content(selected_row['title'], goal=goal)
                    st.success("Transformation Complete!")
                    st.markdown(f"### Output Result:\n{enhanced_text}")
        else:
            st.warning("Please run the scraper pipeline first to load data into the AI Editor.")

except Exception as e:
    st.error(f"Error loading database records: {str(e)}")
