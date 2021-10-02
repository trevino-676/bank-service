import time
from typing import Optional
from os import environ

import jwt

from logger import logger


JWT_SECRET = environ.get("SECRET_KEY")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM") or "HS256"


def decode_jwt(token: str) -> Optional[dict]:
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["exp"] >= time.time() else None
    except Exception as e:
        logger.error(e)
        return {}

