from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.auth_handler import decode_jwt

from logger import logger


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication")
            if not self.verify_jwt(credentials.credentials):
                return HTTPException(
                    status_code=403, detail="Invalid token or expired toke."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            logger.error(e)
            payload = None

        if payload:
            is_token_valid = True

        return is_token_valid
