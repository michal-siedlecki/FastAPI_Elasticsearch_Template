import os
import secrets
from typing import Any, Dict, Optional
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))


class Settings(BaseSettings):
    API_VERSION: str = "/api/v1"
    APP_SECRET_KEY: str = secrets.token_urlsafe(32)
    PASSWORD_RESET_TOKEN_EXPIRES_MINUTES: int = 30
    SERVER_HOST: AnyHttpUrl = "http://127.0.0.1:8000"
    ES_SERVER: str = "http://127.0.0.1:9200"
    ES_USER: str = os.getenv('ES_USER')
    ES_PASSWORD: str = os.getenv('ES_PASSWORD')

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = os.getenv('SMTP_PORT')
    SMTP_HOST: Optional[str] = os.getenv('SMTP_HOST')
    SMTP_USER: Optional[str] = os.getenv('SMTP_USER')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    MAIL_FROM: Optional[EmailStr] = os.getenv('MAIL_FROM')
    MAIL_FROM_NAME: Optional[str] = os.getenv('MAIL_FROM_NAME')
    EMAIL_TEMPLATES_DIR: str = "core/email_templates"
    EMAILS_ENABLED: bool = False

    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')
    CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
    HS256 = os.getenv('HS256')

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )


settings = Settings()
