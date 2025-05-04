import requests
from bs4 import BeautifulSoup

def scrape_website(url, params):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # اینجا منطق اسکراپینگ خاص شما قرار می‌گیرد
    # مثال ساده:
    data = {
        "title": soup.title.string if soup.title else None,
        "links": [a['href'] for a in soup.find_all('a', href=True)],
        "text": soup.get_text()
    }
    
    return data
