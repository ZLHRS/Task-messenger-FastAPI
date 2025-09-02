from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()


class DataBaseConfig:
    user: Optional[str] = os.getenv("POSTGRES_USER")
    password: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    host: Optional[str] = os.getenv("POSTGRES_HOST", "localhost")
    port: Optional[str] = os.getenv("POSTGRES_PORT", "5432")
    db: Optional[str] = os.getenv("POSTGRES_DB")

    def get_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings:
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")


class AdminInfo:
    ADMIN_USERNAME: Optional[str] = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: Optional[str] = os.getenv("ADMIN_PASSWORD")


class EmailInfo:
    EMAIL_PORT: Optional[int] = os.getenv("EMAIL_PORT")
    EMAIL_HOST: Optional[str] = os.getenv("EMAIL_HOST")
    EMAIL_USERNAME: Optional[str] = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: Optional[str] = os.getenv("EMAIL_PASSWORD")


settings = Settings()
admin_info = AdminInfo()
data_base_config = DataBaseConfig()
email_info = EmailInfo()


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_url = os.getenv("CELERY_BROKER", "amqp://guest:guest@localhost:5672//")
data_base = data_base_config.get_url()
