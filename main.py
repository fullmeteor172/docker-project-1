from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone
import hashlib
from typing import Dict
import os
import redis.asyncio as redis  # async redis client

app = FastAPI(title="URL Shortener API", version="1.0.0")

# Redis connection (host = service name in docker-compose)
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True  # makes get/set work with str instead of bytes
)

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
async def get_status():
    """Health check endpoint (checks Redis too)."""
    try:
        pong = await redis_client.ping()
        return {"status": "ok", "redis": "up" if pong else "down"}
    except Exception:
        return {"status": "ok", "redis": "down"}


@app.get("/api/v1/time")
def get_time() -> Dict[str, str]:
    """Return current UTC time (ISO 8601, timezone-aware)."""
    return {"time": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v1/shorten", response_model=URLResponse)
async def shorten_url(request: URLRequest) -> URLResponse:
    """Generate a short code for the given URL and store it."""
    url_str = str(request.url)
    code = hashlib.md5(url_str.encode()).hexdigest()[:6]
    await redis_client.set(code, url_str)
    return URLResponse(code=code, short_url=f"/{code}")

@app.get("/{code}")
async def resolve_url(code: str):
    """Redirect to the original URL for a given short code."""
    url = await redis_client.get(code)
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=url, status_code=307)  # 307 = Temporary Redirect