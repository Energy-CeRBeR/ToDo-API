import pytest
from httpx import AsyncClient

from src.tests.conftest import client, get_test_users_data


@pytest.mark.asyncio
async def test_create_users(client: AsyncClient, get_test_users_data):
    for user_data in get_test_users_data:
        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200

        resp_dict: dict = response.json()
        assert resp_dict.get("token_type", "") == "Bearer"
        assert len(resp_dict.get("access_token", "")) > 0
        assert len(resp_dict.get("refresh_token", "")) > 0


@pytest.mark.asyncio
async def test_login_users(client: AsyncClient, get_test_users_data):
    for user_data in get_test_users_data:
        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200

        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = await client.post("/user/login", params=params)
        assert response.status_code == 200

        resp_dict: dict = response.json()
        assert resp_dict.get("token_type", "") == "Bearer"
        assert len(resp_dict.get("access_token", "")) > 0
        assert len(resp_dict.get("refresh_token", "")) > 0


@pytest.mark.asyncio
async def test_self_user(client: AsyncClient, get_test_users_data):
    for user_data in get_test_users_data:
        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200

        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        response = await client.post("/user/login", params=params)
        assert response.status_code == 200

        resp_dict: dict = response.json()
        access_token = resp_dict.get("access_token", "")
        assert len(access_token) > 0

        response = await client.get("/user/self", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        resp_dict: dict = response.json()
        print(resp_dict)

        for key in user_data:
            if key != "password":
                assert user_data[key] == resp_dict[key]

        assert resp_dict["is_admin"] is False
        assert resp_dict["is_verified"] is False
        assert resp_dict["is_active"] is True
        assert len(resp_dict.get("categories", [])) == 1
        assert resp_dict["categories"][0]["name"] == "base_category"
        assert resp_dict["categories"][0]["color"] == "#FFFFFF"
        assert resp_dict["categories"][0]["user_id"] == resp_dict["id"]
