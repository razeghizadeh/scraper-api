import requests

def scrape_raw_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    }
    
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        # غیرفعال کردن تغییرات خودکار در encoding
        allow_redirects=True,
        stream=True  # برای دریافت پاسخ به صورت stream
    )
    
    response.raise_for_status()
    
    # تنظیم encoding در صورت وجود در هدرها
    if 'charset' in response.headers.get('content-type', ''):
        response.encoding = response.apparent_encoding
    
    # دریافت محتوای خام بدون هیچ پردازشی
    raw_html = response.text
    
    return raw_html
