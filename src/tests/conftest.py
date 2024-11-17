import asyncio
import os
import pytest

from typing import AsyncGenerator
from pathlib import Path

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.database import clear_tables
from src.main import app
from config_data.config import Config, load_config

config: Config = load_config(".env")


@pytest.fixture(scope="session", autouse=True)
def client():
    assert config.variablesData.MODE == "TEST"

    project_root = Path(__file__)
    while not (project_root / "alembic.ini").exists():
        if project_root.parent == project_root:
            raise FileNotFoundError("alembic.ini not found in project")
        project_root = project_root.parent

    os.chdir(project_root)
    os.system("alembic upgrade head")
    asyncio.run(clear_tables())


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    httpx_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000")
    async with httpx_client as client:
        yield client
