from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .config import Config

config = Config()

engine = create_async_engine(
    config.DATABASE_URL,
    echo=config.ENVIRONMENT == "development",
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()