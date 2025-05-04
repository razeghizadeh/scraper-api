from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .scraper import scrape_raw_html

app = FastAPI(title="Raw HTML Scraper API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Raw HTML Scraper API is running!"}

@app.get("/api/scrape")
async def scrape_raw(
    url: str = Query(..., description="URL to scrape"),
    user_agent: str = Query(None, description="Custom User-Agent header")
):
    try:
        html_content = scrape_raw_html(url, user_agent)
        return {
            "status": "success",
            "url": url,
            "html": html_content
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
