import pytest
from httpx import AsyncClient

from src.tests.conftest import client, get_test_users_data
from src.users.schemas import SuccessfulResponse


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


@pytest.mark.asyncio
async def test_create_users(client: AsyncClient, get_test_users_data):
    global CREATE_USER_FLAG

    for user_data in get_test_users_data:
        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200

        resp_dict: dict = response.json()
        assert resp_dict.get("token_type", "") == "Bearer"
        assert len(resp_dict.get("access_token", "")) > 0
        assert len(resp_dict.get("refresh_token", "")) > 0

    CREATE_USER_FLAG = False


@pytest.mark.asyncio
async def test_login_users(client: AsyncClient, get_test_users_data):
    global CREATE_USER_FLAG, ACCESS_TOKENS

    for user_data in get_test_users_data:
        if CREATE_USER_FLAG:
            await create_user_helper(client, user_data)
            CREATE_USER_FLAG = False

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

        ACCESS_TOKENS[user_data["email"]] = resp_dict["access_token"]


@pytest.mark.asyncio
async def test_self_user(client: AsyncClient, get_test_users_data):
    global CREATE_USER_FLAG, ACCESS_TOKENS

    for user_data in get_test_users_data:
        if CREATE_USER_FLAG:
            await create_user_helper(client, user_data)
            CREATE_USER_FLAG = False

        access_token = ACCESS_TOKENS[user_data["email"]] if user_data["email"] in ACCESS_TOKENS \
            else await get_token_helper(client, user_data)
        response = await client.get("/user/self", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        resp_dict: dict = response.json()
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


@pytest.mark.asyncio
async def test_edit_user(client: AsyncClient, get_test_users_data):
    global CREATE_USER_FLAG, ACCESS_TOKENS

    for user_data in get_test_users_data:
        if CREATE_USER_FLAG:
            await create_user_helper(client, user_data)
            CREATE_USER_FLAG = False

        access_token = ACCESS_TOKENS[user_data["email"]] if user_data["email"] in ACCESS_TOKENS \
            else await get_token_helper(client, user_data)

        base_user_data = {
            "name": user_data["name"],
            "surname": user_data["surname"],
            "gender": user_data["gender"]
        }

        upd_user_data = {
            "name": user_data["name"] + "_edited",
            "surname": user_data["surname"] + "_edited",
            "gender": "male" if user_data["gender"] == "female" else "female"
        }

        response = await client.put(
            "/user/edit",
            json=upd_user_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200

        resp_dict: dict = response.json()
        for key in upd_user_data:
            assert upd_user_data[key] == resp_dict[key]

        response = await client.put(
            "/user/edit",
            json=base_user_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, get_test_users_data):
    global CREATE_USER_FLAG, ACCESS_TOKENS

    for user_data in get_test_users_data:
        if CREATE_USER_FLAG:
            await create_user_helper(client, user_data)
            CREATE_USER_FLAG = False

        access_token = ACCESS_TOKENS[user_data["email"]] if user_data["email"] in ACCESS_TOKENS \
            else await get_token_helper(client, user_data)

        response = await client.delete("/user/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        assert response.json() == SuccessfulResponse().dict()

        response = await client.post("/user/register", json=user_data)
        assert response.status_code == 200
