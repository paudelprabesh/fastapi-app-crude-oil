from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(engine)
