import requests
from lxml import html
from lxml_html_clean import Cleaner

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # تمیز کردن HTML (اختیاری)
        cleaner = Cleaner()
        cleaned_html = cleaner.clean_html(response.text)
        
        return cleaned_html
        
    except Exception as e:
        raise Exception(f"Error scraping website: {str(e)}")
