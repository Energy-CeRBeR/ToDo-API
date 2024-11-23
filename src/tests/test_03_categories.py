import pytest
from httpx import AsyncClient
from collections import defaultdict


import src.tests.conftest
from src.tests.conftest import client, get_test_users_data, get_test_categories_data, create_user_helper, \
    get_token_helper, create_categories_helper, get_categories_helper

from src.categories.schemas import SuccessfulResponse


@pytest.mark.asyncio
async def test_show_categories(client: AsyncClient, get_test_users_data):
    response = await client.get("/categories/")
    assert response.status_code == 403

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
    response = await client.post("/categories/", json=get_test_categories_data[0][0])
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

    src.tests.conftest.CREATE_CATEGORIES_FLAG = False


@pytest.mark.asyncio
async def test_get_category(client: AsyncClient, get_test_users_data):
    response = await client.get("/categories/1")
    assert response.status_code == 403

    users_with_categories = defaultdict(list)

    for user_data in get_test_users_data:
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        users_with_categories[access_token] = await get_categories_helper(client, access_token)

        for category in users_with_categories[access_token]:
            response = await client.get(
                f'/categories/{category["id"]}',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            assert resp_dict == category

    access_tokens = list(users_with_categories.keys())
    for i in range(len(access_tokens)):
        for j in range(i + 1, len(access_tokens)):
            access_token1 = access_tokens[i]
            access_token2 = access_tokens[j]

            for category2 in users_with_categories[access_token2]:
                response = await client.get(
                    f'/categories/{category2["id"]}',
                    headers={"Authorization": f"Bearer {access_token1}"}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.get(
        f'/categories/{non_existed_id}',
        headers={"Authorization": f"Bearer {access_tokens[0]}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_edit_category(client: AsyncClient, get_test_users_data):
    response = await client.put("/categories/1")
    assert response.status_code == 403

    users_with_categories = defaultdict(list)

    for user_data in get_test_users_data:
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        users_with_categories[access_token] = await get_categories_helper(client, access_token)

        for category in users_with_categories[access_token]:
            base_category_data = {
                "name": category["name"],
                "color": category["color"],
            }
            upd_category_data = {
                "name": category["name"] + "_edited",
                "color": "#F44336"
            }

            response = await client.put(
                f'/categories/{category["id"]}',
                json=upd_category_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            assert resp_dict["name"] == upd_category_data["name"]
            assert resp_dict["color"] == upd_category_data["color"]

            response = await client.put(
                f'/categories/{category["id"]}',
                json=base_category_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

    access_tokens = list(users_with_categories.keys())
    for i in range(len(access_tokens)):
        for j in range(i + 1, len(access_tokens)):
            access_token1 = access_tokens[i]
            access_token2 = access_tokens[j]

            for category2 in users_with_categories[access_token2]:
                response = await client.put(
                    f'/categories/{category2["id"]}',
                    json={"name": "name", "color": "#F44336"},
                    headers={"Authorization": f"Bearer {access_token1}"}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.put(
        f'/categories/{non_existed_id}',
        json={"name": "name", "color": "#F44336"},
        headers={"Authorization": f"Bearer {access_tokens[0]}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, get_test_users_data, get_test_categories_data):
    response = await client.delete("/categories/1")
    assert response.status_code == 403

    users_with_categories = defaultdict(list)

    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if src.tests.conftest.CREATE_USER_FLAG:
            await create_user_helper(client, user_data)

        access_token = src.tests.conftest.ACCESS_TOKENS[user_data["email"]] \
            if user_data["email"] in src.tests.conftest.ACCESS_TOKENS else await get_token_helper(client, user_data)

        users_with_categories[access_token] = await get_categories_helper(client, access_token)

        for category in users_with_categories[access_token]:
            if category["name"] != "base_category":
                response = await client.delete(
                    f'/categories/{category["id"]}',
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                assert response.status_code == 200
                assert response.json() == SuccessfulResponse().dict()

        del src.tests.conftest.CATEGORIES[access_token]
        for category_data in get_test_categories_data[i]:
            await create_categories_helper(client, category_data, access_token)
        users_with_categories[access_token] = await get_categories_helper(client, access_token)

    access_tokens = list(users_with_categories.keys())
    for i in range(len(access_tokens)):
        for j in range(i + 1, len(access_tokens)):
            access_token1 = access_tokens[i]
            access_token2 = access_tokens[j]

            for category2 in users_with_categories[access_token2]:
                response = await client.delete(
                    f'/categories/{category2["id"]}',
                    headers={"Authorization": f"Bearer {access_token1}"}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.delete(
        f'/categories/{non_existed_id}',
        headers={"Authorization": f"Bearer {access_tokens[0]}"}
    )
    assert response.status_code == 404
