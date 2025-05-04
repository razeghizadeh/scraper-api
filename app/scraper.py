from requests_html import HTMLSession
import time

def scrape_website(url):
    session = HTMLSession()
    
    try:
        # تنظیمات مرورگر headless
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu'
        ]
        
        # ایجاد session با قابلیت رندرینگ جاوااسکریپت
        response = session.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # اجرای جاوااسکریپت و صبر برای لود کامل صفحه
        response.html.render(timeout=20, sleep=5)
        
        # دریافت HTML پس از رندرینگ کامل
        return response.html.html
        
    except Exception as e:
        raise Exception(f"Error scraping website: {str(e)}")
    finally:
        session.close()
