from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
from typing import Optional
import logging

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Scraper API",
    description="A web scraping API similar to scrape.do",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# User-Agentهای مختلف برای جلوگیری از بلاک شدن
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)"
]

@app.get("/", tags=["Root"])
async def root():
    """Endpoint اصلی برای بررسی سلامت سرویس"""
    return {
        "status": "running",
        "docs": "/docs",
        "scrape_endpoint": "/scrape?url=YOUR_URL"
    }

@app.get("/scrape", tags=["Scraping"])
async def scrape_url(
    url: str = Query(..., description="URL مورد نظر برای اسکراپینگ"),
    timeout: Optional[int] = Query(10, description="تایم‌اوت درخواست (ثانیه)"),
    proxy: Optional[str] = Query(None, description="آدرس پروکسی (اختیاری)")
):
    """
    اسکراپ محتوای یک URL و برگرداندن داده‌های اصلی
    """
    try:
        # انتخاب تصادفی User-Agent
        import random
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }

        proxies = {"http": proxy, "https": proxy} if proxy else None

        logger.info(f"Scraping URL: {url}")
        
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            proxies=proxies
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # حذف اسکریپت‌ها و استایل‌ها برای کاهش حجم داده
        for script in soup(["script", "style"]):
            script.decompose()

        # استخراج داده‌های مهم
        result = {
            "url": url,
            "status": "success",
            "status_code": response.status_code,
            "title": soup.title.string if soup.title else None,
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"] 
                        if soup.find("meta", attrs={"name": "description"}) else None,
            "headings": {
                "h1": [h1.get_text().strip() for h1 in soup.find_all('h1')],
                "h2": [h2.get_text().strip() for h2 in soup.find_all('h2')],
            },
            "links": [
                {
                    "text": a.get_text().strip(),
                    "href": a.get("href"),
                    "external": bool(a.get("href", "").startswith(("http://", "https://")))
                } 
                for a in soup.find_all('a', href=True)
            ],
            "images": [
                {
                    "src": img.get("src"),
                    "alt": img.get("alt", ""),
                    "width": img.get("width"),
                    "height": img.get("height")
                }
                for img in soup.find_all('img')
            ],
            "text_content": soup.get_text(" ", strip=True)[:5000] + "..."  # محدودیت حجم خروجی
        }

        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching URL: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# برای تست محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
