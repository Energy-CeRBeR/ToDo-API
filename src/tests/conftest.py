import asyncio
import pytest

from httpx import AsyncClient
from starlette.testclient import TestClient

from typing import Any
from typing import Generator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config_data.config import Config, load_config
from src.main import app

config: Config = load_config(".env")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    engine = create_async_engine(config.database.TEST_DATABASE_URL, future=True, echo=True)
    async_session = async_sessionmaker(engine)

    httpx_client = AsyncClient(app=app, base_url="http://testserver")

    async with httpx_client as client:
        yield client
