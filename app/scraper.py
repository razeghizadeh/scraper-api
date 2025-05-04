import requests

def scrape_website(url, params):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    # بازگرداندن محتوای خام HTML بدون هیچ پردازشی
    return {
        "html": response.text,
        "status_code": response.status_code,
        "headers": dict(response.headers)
    }
