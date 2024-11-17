import asyncio
import os
import pytest

from pathlib import Path

from src.database import clear_tables
from config_data.config import Config, load_config

config: Config = load_config(".env")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert config.variablesData.MODE == "TEST"

    project_root = Path(__file__)
    while not (project_root / "alembic.ini").exists():
        if project_root.parent == project_root:
            raise FileNotFoundError("alembic.ini not found in project")
        project_root = project_root.parent

    os.chdir(project_root)
    os.system("alembic upgrade head")
    asyncio.run(clear_tables())
