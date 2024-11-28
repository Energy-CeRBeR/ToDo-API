import asyncio
import os
import pytest
import pytest_asyncio

from typing import AsyncGenerator, List, Dict, Generator
from pathlib import Path
from copy import deepcopy
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.database import clear_tables
from main import app
from src.users.repositories import UserRepository
from config_data.config import Config, load_config
from src.users.schemas import UserCreate

config: Config = load_config(".env")

TEST_USERS_COUNT = 2
TEST_CATEGORIES_COUNT = 2
TEST_TASKS_COUNT_IN_CATEGORY = 2

TEST_DATA = dict()
TESTS_DATA_TEMPLATE = {
    "access_token": "",
    "categories": [],
    "tasks": []
}

TEST_ADMIN_DATA = {
    "admin": {
        "data": dict(),
        "access_token": ""
    },
    "user": {
        "data": dict(),
        "access_token": ""
    }
}

USERS: List[Dict] = list()


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
        users.append(
            {
                "name": f"TestName{i + 1}",
                "surname": f"TestSurname{i + 1}",
                "short_name": f"TestShort{i + 1}",
                "email": f"test_user{i + 1}@example.com",
                "gender": "male" if i % 2 == 0 else "female",
                "password": f"TestPassword{i + 1}"
            }
        )

    return users


@pytest.fixture(scope="module")
def get_test_categories_data() -> List[List[Dict]]:
    categories = []
    for i in range(TEST_USERS_COUNT):
        colors = ["#F44336", "#4CAF50"]
        user_categories = []
        for j in range(TEST_CATEGORIES_COUNT):
            user_categories.append(
                {
                    "name": f"{j + 1}_category_user_{i + 1}",
                    "color": colors[j]
                }
            )
        categories.append(user_categories)

    return categories


@pytest.fixture(scope="module")
def get_test_tasks_data() -> List[List[Dict]]:
    tasks = []

    for i, email in enumerate(TEST_DATA):
        user_data = TEST_DATA[email]
        user_tasks = []
        count = 0
        for j in range(TEST_CATEGORIES_COUNT):
            for t in range(TEST_TASKS_COUNT_IN_CATEGORY):
                count += 1
                user_tasks.append(
                    {
                        "name": f"{count}_Task_user_{i + 1}",
                        "description": f"{count}_task_description_user_{i + 1}",
                        "priority": 1 + (i + j + t) % 3,
                        "category_id": user_data["categories"][j]["id"],
                        "date": "2025-01-01"
                    }
                )
        tasks.append(user_tasks)

    return tasks


async def create_user_helper(client: AsyncClient, user_data: dict) -> None:
    response = await client.post("/user/register", json=user_data)
    assert response.status_code == 200 or response.status_code == 400

    TEST_DATA[user_data["email"]] = deepcopy(TESTS_DATA_TEMPLATE)


async def create_categories_helper(client: AsyncClient, category_data: dict, access_token: str) -> None:
    response = await client.post(
        "/categories/",
        json=category_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


async def create_tasks_helper(client: AsyncClient, task_data: dict, access_token: str) -> None:
    response = await client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200


async def create_admin_and_base_users_helper(client: AsyncClient) -> None:
    admin_user = {
        "name": f"test_admin",
        "surname": f"test_admin_surname",
        "short_name": f"test_admin_shortname",
        "email": f"admin_test_user@example.com",
        "gender": "male",
        "password": f"admin_TestPassword"
    }

    base_user = {
        "name": f"test_base",
        "surname": f"test_base_surname",
        "short_name": f"test_base_shortname",
        "email": f"admin_base_user@example.com",
        "gender": "female",
        "password": f"base_TestPassword"
    }

    if not TEST_ADMIN_DATA["admin"]["data"] or not TEST_ADMIN_DATA["user"]["data"]:
        if not TEST_ADMIN_DATA["admin"]["access_token"]:
            admin = await UserRepository().set_admin_status(
                await UserRepository().create_user(UserCreate(**admin_user))
            )
            TEST_ADMIN_DATA["admin"]["data"] = admin.to_dict()

            params = {
                "email": admin_user["email"],
                "password": admin_user["password"]
            }

            response = await client.post("/user/login", params=params)
            assert response.status_code == 200

            resp_dict: dict = response.json()
            access_token = resp_dict.get("access_token", "")
            assert len(access_token) > 0

            TEST_ADMIN_DATA["admin"]["access_token"] = access_token

        if not TEST_ADMIN_DATA["user"]["data"]:
            user = await UserRepository().create_user(UserCreate(**base_user))
            TEST_ADMIN_DATA["user"]["data"] = user.to_dict()


async def get_all_users_helper() -> List[Dict]:
    global USERS

    if USERS:
        return USERS

    USERS = list(map(lambda x: x.to_dict(), await UserRepository().get_all_users()))
    return USERS


async def get_token_helper(client: AsyncClient, user_data: dict) -> str:
    params = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    response = await client.post("/user/login", params=params)
    assert response.status_code == 200

    resp_dict: dict = response.json()
    access_token = resp_dict.get("access_token", "")
    assert len(access_token) > 0

    TEST_DATA[user_data["email"]]["access_token"] = resp_dict["access_token"]

    return access_token


async def get_categories_helper(client: AsyncClient, user_data: TESTS_DATA_TEMPLATE) -> List[dict]:
    if len(TEST_DATA[user_data["email"]]["categories"]) == TEST_CATEGORIES_COUNT + 1:
        return TEST_DATA[user_data["email"]]["categories"]

    TEST_DATA[user_data["email"]]["categories"] = []
    response = await client.get(
        "/categories/",
        headers={"Authorization": f'Bearer {TEST_DATA[user_data["email"]]["access_token"]}'}
    )
    assert response.status_code == 200

    resp_dict = response.json()
    for category in resp_dict:
        TEST_DATA[user_data["email"]]["categories"].append(category)

    return TEST_DATA[user_data["email"]]["categories"]


async def get_tasks_helper(client: AsyncClient, user_data: TESTS_DATA_TEMPLATE) -> List[dict]:
    if len(TEST_DATA[user_data["email"]]["tasks"]) == TEST_CATEGORIES_COUNT * TEST_TASKS_COUNT_IN_CATEGORY:
        return TEST_DATA[user_data["email"]]["tasks"]

    TEST_DATA[user_data["email"]]["tasks"] = []
    response = await client.get(
        "/tasks/",
        headers={"Authorization": f'Bearer {TEST_DATA[user_data["email"]]["access_token"]}'}
    )
    assert response.status_code == 200

    resp_dict = response.json()
    for task in resp_dict:
        TEST_DATA[user_data["email"]]["tasks"].append(task)

    return TEST_DATA[user_data["email"]]["tasks"]
