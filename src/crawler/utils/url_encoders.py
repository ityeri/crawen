import hashlib
from typing import Callable
from urllib.parse import quote

def sha256_encoder(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()

def percent_encoder(url: str) -> str:
    return quote(url, safe='')


default_encoder: Callable[[str], str] = percent_encoder