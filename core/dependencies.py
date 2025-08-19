import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jwt import ExpiredSignatureError, DecodeError
from core.config import Settings
from utils.redis_cashe import get_redis

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token_from_redis = await get_redis("my_token")
    if token != token_from_redis:
        raise HTTPException(status_code=401, detail="Log back into your account")
    try:
        payload = jwt.decode(
            token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "username": username, "email": email, "role": role}
    except JWTError as jwterr:
        raise HTTPException(status_code=401, detail="Invalid token") from jwterr
    except ExpiredSignatureError as expirederr:
        raise HTTPException(
            status_code=401, detail="Token expired, please log in again"
        ) from expirederr
    except DecodeError as decodeerr:
        raise HTTPException(status_code=401, detail="Invalid token") from decodeerr


async def get_current_admin(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403, detail="You don't have permission to perform this action"
        )
    return current_user
