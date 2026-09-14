# 🚀 Aetros: Enterprise-Grade AI Scraper & Content Automation Platform

**Aetros** is an end-to-end web scraping and AI-driven content transformation ecosystem built with Python, Playwright, Streamlit, and Google Gemini API. It empowers users to extract unstructured data from web platforms, store structured records, and generate marketing-ready content, SEO metadata, and social posts dynamically.

---

## 🌟 Key Features

* **🌐 Automated Web Scraping:** High-speed data extraction using Playwright for handling dynamic web content.
* **⚡ Real-Time Streamlit Dashboard:** Interactive UI to trigger scraping runs, view analytics, and query records.
* **🧠 Gemini AI Integration:** Automated content rewriting, SEO optimization, and social media post creation using Google's latest Gemini API.
* **📊 Dual Database Storage:** Seamless data logging with SQLite and automated Google Sheets syncing.
* **🛡️ Robust Error Handling & Dynamic Model Discovery:** Built-in auto-discovery mechanisms to ensure continuous API stability and zero downtime.

---

## 🏗️ Tech Stack

* **Language:** Python 3.10+
* **UI Framework:** Streamlit
* **Browser Automation:** Playwright
* **Database / Storage:** SQLite, Google Sheets API (`gspread`)
* **AI Engine:** Google Gemini API (`google-generativeai`)
* **Environment Management:** `python-dotenv`

---

## 📁 Directory Structure

```text
aetros/
├── app.py                   # Streamlit Main Dashboard Application
├── .env                     # Environment Configuration (API Keys & Configs)
├── requirements.txt         # Project Dependencies
├── modules/
│   ├── scraper.py           # Playwright Extraction Logic
│   ├── database.py          # SQLite & Google Sheets Sync Operations
│   └── ai_processor.py      # Gemini AI Content Generation & Rewriting
└── data/
    └── aetros_data.db       # Local SQLite Database Storage

