import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Đường dẫn tới thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Các giá trị này sẽ được nạp từ environment variables hoặc file .env
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    REDIS_URL: str
    RATE_LIMIT: str
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE if ENV_FILE.exists() else None,
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()


