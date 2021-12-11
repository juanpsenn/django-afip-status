import os
from typing import Optional


def is_authenticated(token: Optional[str]) -> bool:
    if token and type(token) == str:
        return token.replace("Token ", "") == os.getenv("APIKEY")
    return False
