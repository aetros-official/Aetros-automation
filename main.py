import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Aetros Automation Studio", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #F8FAFC; }
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white; border: none; padding: 12px 28px;
        font-size: 16px; font-weight: 600; border-radius: 8px; width: 100%;
    }
    .status-card {
        background: #1E293B; border: 1px solid #334155;
        border-radius: 12px; padding: 20px; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #818CF8;'>⚡ Aetros Automation Studio</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    url_input = st.text_input("Target URL:", "https://example.com")
with col2:
    topic_input = st.text_input("Target Topic:", "Travel Affiliate Guide")

if st.button("🚀 Execute Full Pipeline"):
    with st.spinner("Generating High-Speed AI Output..."):
        groq_key = os.getenv("GROQ_API_KEY")
       
        if not groq_key:
            st.error("⚠️ GROQ_API_KEY is missing in .env file!")
        else:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Topic: {topic_input}\nContext: {url_input}\nWrite a short structured breakdown for a travel affiliate blog."
                    }
                ]
            }
           
            try:
                response = requests.post(url, json=payload, headers=headers)
                data = response.json()
               
                if response.status_code == 200 and "choices" in data:
                    output_text = data["choices"][0]["message"]["content"]
                    st.success("✨ Pipeline Executed Successfully!")
                    st.markdown("### 📑 AI Content Output")
                    st.markdown(f"<div class='status-card'>{output_text}</div>", unsafe_allow_html=True)
                else:
                    err_msg = data.get("error", {}).get("message", "API Request Failed")
                    st.error(f"Groq API Error: {err_msg}")
                   
            except Exception as ex:
                st.error(f"Connection Exception: {str(ex)}")