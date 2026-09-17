"""
Application Configuration
Manages environment variables and settings using Pydantic
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional, Union, List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Pralay Flash Flood Prediction System"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    POSTGRES_USER: str = "pralay_user"
    POSTGRES_PASSWORD: str = "pralay_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "pralay_db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # MQTT Broker
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    MQTT_USE_TLS: bool = False

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # External APIs
    IMD_API_URL: str = "https://mausam.imd.gov.in/imd_latest/contents/api"
    IMD_API_KEY: Optional[str] = None

    # ML Model Paths
    MODEL_DIR: str = "./ml/models/trained"
    LSTM_MODEL_PATH: str = "./ml/models/trained/lstm_flood.pth"
    XGBOOST_MODEL_PATH: str = "./ml/models/trained/xgboost_risk.pkl"
    ENSEMBLE_MODEL_PATH: str = "./ml/models/trained/ensemble.pkl"

    # Alert Thresholds
    RISK_THRESHOLD_LOW: float = 0.3
    RISK_THRESHOLD_MODERATE: float = 0.5
    RISK_THRESHOLD_HIGH: float = 0.7
    RISK_THRESHOLD_EXTREME: float = 0.85

    # Notification Services
    SMS_PROVIDER_URL: Optional[str] = None
    SMS_API_KEY: Optional[str] = None
    FCM_SERVER_KEY: Optional[str] = None

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    @field_validator("CORS_ORIGINS")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
