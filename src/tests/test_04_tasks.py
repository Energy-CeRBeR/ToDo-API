import pytest
from httpx import AsyncClient

from src.tests.conftest import client, get_test_users_data, create_user_helper, get_token_helper, TEST_DATA, \
    get_test_tasks_data, get_tasks_helper


@pytest.mark.asyncio
async def test_create_tasks(client: AsyncClient, get_test_users_data, get_test_tasks_data):
    response = await client.post("/tasks/", json=get_test_tasks_data[0][0])
    assert response.status_code == 403

    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)
        response = await client.get("/user/self", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        current_user = response.json()
        for task_data in get_test_tasks_data[i]:
            response = await client.post(
                "/tasks/",
                json=task_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            assert resp_dict["user_id"] == current_user["id"]
            for key in task_data:
                assert task_data[key] == resp_dict[key]

            TEST_DATA[user_data["email"]]["tasks"].append(resp_dict)


@pytest.mark.asyncio
async def test_show_tasks(client: AsyncClient, get_test_users_data):
    response = await client.get("/tasks/")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)

        response = await client.get("/tasks/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, get_test_users_data):
    response = await client.get("/tasks/1")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)
        await get_tasks_helper(client, user_data)

        for task in TEST_DATA[user_data["email"]]["tasks"]:
            response = await client.get(
                f'/tasks/{task["id"]}',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            assert resp_dict == task

    for i in range(len(get_test_users_data)):
        for j in range(i + 1, len(get_test_users_data)):
            for task2 in TEST_DATA[get_test_users_data[j]["email"]]["tasks"]:
                response = await client.get(
                    f'/tasks/{task2["id"]}',
                    headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[i]["email"]]["access_token"]}'}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.get(
        f'/tasks/{non_existed_id}',
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404
