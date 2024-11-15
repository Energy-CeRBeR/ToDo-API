from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession

from sqlalchemy.orm import DeclarativeBase

from config_data.config import Config, load_config

config: Config = load_config(".env")
DATABASE_URL = config.database.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass
