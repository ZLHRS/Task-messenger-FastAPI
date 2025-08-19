import jwt
from datetime import timedelta, timezone, datetime
from core.config import Settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
default_expire_time = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    copy_data = data.copy()
    expire_time = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=default_expire_time)
    )
    copy_data.update({"exp": expire_time})
    return jwt.encode(copy_data, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
