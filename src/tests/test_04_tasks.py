import pytest
from httpx import AsyncClient
from collections import defaultdict

import src.tests.conftest
from src.tests.conftest import client, get_test_users_data, get_test_categories_data, create_user_helper, \
    get_token_helper, create_categories_helper, get_categories_helper


@pytest.mark.asyncio
async def test_create_tasks(client: AsyncClient, get_test_users_data, get_test_categories_data):
    response = await client.post("/tasks/", json=get_test_categories_data[0][0])
    assert response.status_code == 403

    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)
        response = await client.get("/user/self", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        current_user = response.json()


@pytest.mark.asyncio
async def test_show_tasks(client: AsyncClient, get_test_users_data):
    response = await client.get("/tasks/")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        response = await client.get("/tasks/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        resp_dict = response.json()
        for category in resp_dict:
            src.tests.conftest.CATEGORIES[access_token].append(category)
