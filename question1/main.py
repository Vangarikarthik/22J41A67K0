from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from models import ShortenRequest, ShortenResponse
from services import store_url, get_original_url
from logger_middleware import log
from datetime import datetime
from typing import Optional
app = FastAPI()

@app.post("/shorturl", response_model=ShortenResponse, status_code=201)
async def create_short_url(request: ShortenRequest):
    try:
        shortcode, expiry = store_url(request.url, request.validity, request.shortcode)
        shortlink = f"http://localhost:8000/{shortcode}"

        await log("backend", "info", "shortener", f"Created shortlink {shortlink} for {request.url}")

        return ShortenResponse(
            shortlink=shortlink,
            expiry=expiry.isoformat() + "Z"
        )
    except ValueError as ve:
        await log("backend", "error", "shortener", str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        await log("backend", "fatal", "shortener", f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/{shortcode}")
async def redirect_to_url(shortcode: str):
    try:
        url = get_original_url(shortcode)
        await log("backend", "info", "redirect", f"Redirecting shortcode {shortcode} to {url}")
        return RedirectResponse(url=url)
    except KeyError:
        await log("backend", "error", "redirect", f"Shortcode {shortcode} not found")
        raise HTTPException(status_code=404, detail="Shortcode not found")
    except ValueError:
        await log("backend", "error", "redirect", f"Shortcode {shortcode} expired")
        raise HTTPException(status_code=410, detail="Shortcode expired")
    except Exception as e:
        await log("backend", "fatal", "redirect", f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
