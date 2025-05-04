from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .scraper import scrape_website

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape(url: str):
    try:
        html_content = scrape_website(url)
        return {
            "status": "success",
            "url": url,
            "html": html_content
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
