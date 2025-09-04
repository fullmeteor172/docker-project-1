from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone
import hashlib
from typing import Dict
import os

app = FastAPI(title="URL Shortener API", version="1.0.0")

# In-memory storage for Level 1 (to be replaced with Redis in Level 2)
url_store: Dict[str, str] = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class URLRequest(BaseModel):
    url: HttpUrl  # Validates input is a proper URL


class URLResponse(BaseModel):
    code: str
    short_url: str

@app.get("/")
def homepage():
    """Serve the frontend index.html."""
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/api/v1/status")
def get_status() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/v1/time")
def get_time() -> Dict[str, str]:
    """Return current UTC time (ISO 8601, timezone-aware)."""
    return {"time": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v1/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest) -> URLResponse:
    """Generate a short code for the given URL and store it."""
    url_str = str(request.url)  # ensure it's a plain string
    code = hashlib.md5(url_str.encode()).hexdigest()[:6]
    url_store[code] = url_str
    return URLResponse(code=code, short_url=f"/api/v1/{code}")

@app.get("/{code}")
def resolve_url(code: str):
    """Redirect to the original URL for a given short code."""
    url = url_store.get(code)
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url, status_code=307)  # 307 = Temporary Redirect
