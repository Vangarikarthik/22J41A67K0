from pydantic import BaseModel, HttpUrl
from typing import Optional

class ShortenRequest(BaseModel):
    url: HttpUrl
    validity: Optional[int] = 30  # Defaults to 30 minutes
    shortcode: Optional[str] = None

class ShortenResponse(BaseModel):
    shortlink: str
    expiry: str
