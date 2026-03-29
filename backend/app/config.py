from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str
    FRONTEND_URL: str = "http://localhost:5500"
    MONGO_URL: str = "mongodb://mongo:27017"

    class Config:
        env_file = ".env"

settings = Settings()
