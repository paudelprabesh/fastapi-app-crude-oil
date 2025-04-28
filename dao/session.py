from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

# SQLALCHEMY
engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(engine)
