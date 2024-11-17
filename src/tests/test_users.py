import pytest
from httpx import AsyncClient

from src.tests.conftest import client, users_data


@pytest.mark.asyncio
async def test_create_users(client: AsyncClient, users_data):
    for user_data in users_data:
        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200

        # resp_dict = response.json()
        # print(resp_dict)
