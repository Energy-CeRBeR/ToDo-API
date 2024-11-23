from collections import defaultdict

import pytest
from httpx import AsyncClient

import src.tests.conftest
from src.tests.conftest import client, get_test_users_data, get_test_categories_data, create_user_helper, \
    get_token_helper, create_categories_helper, get_categories_helper

from src.categories.schemas import CategoryResponse


@pytest.mark.asyncio
async def test_show_categories(client: AsyncClient, get_test_users_data):
    for user_data in get_test_users_data:
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        response = await client.get("/categories/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        resp_dict = response.json()
        for category in resp_dict:
            src.tests.conftest.CATEGORIES[access_token].append(category)


@pytest.mark.asyncio
async def test_create_categories(client: AsyncClient, get_test_users_data, get_test_categories_data):
    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)
        response = await client.get("/user/self", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        current_user = response.json()

        for category_data in get_test_categories_data[i]:
            response = await client.post(
                "/categories/",
                json=category_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            src.tests.conftest.CATEGORIES[access_token].append(resp_dict)

            assert resp_dict["name"] == category_data["name"]
            assert resp_dict["color"] == category_data["color"]
            assert resp_dict["user_id"] == current_user["id"]


@pytest.mark.asyncio
async def test_get_category(client: AsyncClient, get_test_users_data, get_test_categories_data):
    users_with_categories = defaultdict(list)

    for user_data in get_test_users_data:
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        users_with_categories[access_token] = await get_categories_helper(client, access_token)

        for category in users_with_categories[access_token]:
            response = await client.post(
                f'/categories/{category["id"]}',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()

    for key, value in users_with_categories.items():
        print(key)
        print(value)
        print()
