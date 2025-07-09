from datetime import datetime, timedelta
import random, string
from typing import Optional

# In-memory storage (replace with database in production)
url_store = {}

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def store_url(original_url: str, validity: int, shortcode: Optional[str] = None):
    expiry_time = datetime.utcnow() + timedelta(minutes=validity)

    # Handle custom shortcode
    if shortcode:
        if shortcode in url_store:
            raise ValueError("Shortcode already in use")
    else:
        shortcode = generate_shortcode()
        while shortcode in url_store:
            shortcode = generate_shortcode()

    url_store[shortcode] = {
        "url": original_url,
        "expires": expiry_time
    }

    return shortcode, expiry_time

def get_original_url(shortcode: str):
    data = url_store.get(shortcode)
    if not data:
        raise KeyError("Shortcode does not exist")

    if datetime.utcnow() > data["expires"]:
        raise ValueError("Shortcode has expired")

    return data["url"]
