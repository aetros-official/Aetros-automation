import requests
from bs4 import BeautifulSoup

class WebScraperModule:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

    def scrape_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract clean text from paragraphs
                paragraphs = [p.get_text() for p in soup.find_all('p')]
                text_content = " ".join(paragraphs)
                return text_content[:3000] if text_content else "No readable text content found."
            else:
                return f"Failed to fetch content, Status code: {response.status_code}"
        except Exception as e:
            return f"Scraping error: {str(e)}"