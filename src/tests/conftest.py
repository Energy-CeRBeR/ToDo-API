import os
from pathlib import Path

import pytest

from alembic import op

from config_data.config import Config, load_config

config: Config = load_config(".env")


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    print("Check base")
    assert config.variablesData.MODE == "TEST"

    print("START")

    project_root = Path(__file__)
    while not (project_root / "alembic.ini").exists():
        if project_root.parent == project_root:
            raise FileNotFoundError("alembic.ini not found in project")
        project_root = project_root.parent

    os.chdir(project_root)
    os.system("alembic upgrade head")
    # op.execute(f"DELETE FROM {config.database.DB_NAME}")

    print("SUCCESS")
