from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings

# SQLALCHEMY
engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    ),
)
SessionLocal = async_sessionmaker(engine)
