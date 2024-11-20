import asyncio
import os
import pytest
import pytest_asyncio

from typing import AsyncGenerator, List, Dict, Generator
from pathlib import Path

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.database import clear_tables
from src.main import app
from config_data.config import Config, load_config

config: Config = load_config(".env")


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    assert config.variablesData.MODE == "TEST"

    project_root = Path(__file__)
    while not (project_root / "alembic.ini").exists():
        if project_root.parent == project_root:
            raise FileNotFoundError("alembic.ini not found in project")
        project_root = project_root.parent

    os.chdir(project_root)
    os.system("alembic upgrade head")
    await clear_tables()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    httpx_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")
    async with httpx_client as client:
        yield client


@pytest.fixture(scope="module")
def get_test_users_data() -> List[Dict]:
    users = []
    for i in range(2):
        user = {
            "name": f"TestName{i + 1}",
            "surname": f"TestSurname{i + 1}",
            "short_name": f"TestShort{i + 1}",
            "email": f"test_user{i + 1}@example.com",
            "gender": "male" if i % 2 == 0 else "female",
            "password": f"TestPassword{i + 1}"
        }
        users.append(user)

    return users


@pytest.fixture(scope="module")
def get_test_admin_users_data() -> List[Dict]:
    users = []
    for i in range(2):
        user = {
            "name": f"admin_TestName{i + 1}",
            "surname": f"admin_TestSurname{i + 1}",
            "short_name": f"admin_TestShort{i + 1}",
            "email": f"admin_test_user{i + 1}@example.com",
            "gender": "admin_male" if i % 2 == 0 else "female",
            "password": f"admin_TestPassword{i + 1}"
        }
        users.append(user)

    return users


async def create_user_helper(client: AsyncClient, user_data: dict) -> None:
    response = await client.post("/user/register", json=user_data)
    assert response.status_code == 200 or response.status_code == 400


async def get_token_helper(client: AsyncClient, user_data: dict) -> str:
    global ACCESS_TOKENS

    params = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    response = await client.post("/user/login", params=params)
    assert response.status_code == 200

    resp_dict: dict = response.json()
    access_token = resp_dict.get("access_token", "")
    assert len(access_token) > 0

    ACCESS_TOKENS[user_data["email"]] = resp_dict["access_token"]

    return access_token


CREATE_USER_FLAG = True
ACCESS_TOKENS = dict()
