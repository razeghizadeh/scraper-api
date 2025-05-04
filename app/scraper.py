import requests
from urllib.parse import urlparse

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def validate_url(url):
    """اعتبارسنجی URL"""
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        return False
    except:
        return False

def scrape_raw_html(url, user_agent=None):
    if not validate_url(url):
        raise ValueError("Invalid URL format")
    
    headers = {
        "User-Agent": user_agent or DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }
    
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            stream=True
        )
        response.raise_for_status()
        
        # تنظیم encoding مناسب
        if response.encoding is None:
            response.encoding = 'utf-8'
            
        return response.text
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
