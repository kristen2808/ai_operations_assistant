import os

class Config:
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "ai_operations_postgres")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "ai_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "ai_password")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_operations")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"