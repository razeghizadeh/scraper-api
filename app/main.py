from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .scraper import scrape_raw_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape-raw")
async def scrape_raw(url: str):
    try:
        html_content = scrape_raw_html(url)
        return {
            "status": "success",
            "url": url,
            "html": html_content,
            "content_type": "text/html"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching raw HTML: {str(e)}"
        )
