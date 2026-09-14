import streamlit as st
from modules.web_scraper import WebScraperModule
from modules.ai_processor import AIProcessorModule
from modules.database import AetrosDB

# Initialize Heavy Modules in Memory to Avoid Re-instantiating
@st.cache_resource
def get_scraper():
    return WebScraperModule()

@st.cache_resource
def get_ai_processor():
    return AIProcessorModule()

@st.cache_resource
def get_db():
    return AetrosDB()

def full_aetros_workflow(url, topic):
    scraper = get_scraper()
    ai = get_ai_processor()
    db = get_db()
   
    # Fast Execution
    scraped_data = scraper.scrape_url(url)
    ai_response = ai.generate_content(topic, context=scraped_data)
   
    # Save to Database asynchronously / quickly
    db.save_log({"url": url, "topic": topic, "status": "Success"})
   
    return scraped_data, ai_response