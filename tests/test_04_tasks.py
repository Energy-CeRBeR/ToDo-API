import pytest
from httpx import AsyncClient

from src.tasks.schemas import SuccessfulResponse
from tests.conftest import create_user_helper, get_token_helper, TEST_DATA, get_tasks_helper, create_tasks_helper


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
                assert resp_dict[key] == task_data[key]

            TEST_DATA[user_data["email"]]["tasks"].append(resp_dict)

    base_json = {
        "name": "name",
        "description": "description",
        "priority": 1,
        "category_id": TEST_DATA[get_test_users_data[1]["email"]]["categories"][0]["id"],
        "date": "2025-01-01"
    }

    response = await client.post(
        f'/tasks/',
        json=base_json,
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 403

    base_json["category_id"] = -1
    response = await client.post(
        f'/tasks/',
        json=base_json,
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404


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


@pytest.mark.asyncio
async def test_edit_task(client: AsyncClient, get_test_users_data):
    response = await client.put("/tasks/1")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)
        await get_tasks_helper(client, user_data)

        for ind, task in enumerate(TEST_DATA[user_data["email"]]["tasks"]):
            base_task_data = {
                "name": task["name"],
                "description": task["description"],
                "priority": task["priority"],
                "category_id": task["category_id"],
                "date": task["date"]
            }
            upd_task_data = {
                "name": "edited_" + task["name"],
                "description": "edited_" + task["description"],
                "priority": 4 - task["priority"],
                "category_id": task["category_id"],
                "date": "2025-01-02"
            }

            response = await client.put(
                f'/tasks/{task["id"]}',
                json=upd_task_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict: dict = response.json()
            for key in upd_task_data:
                assert resp_dict[key] == upd_task_data[key]

            response = await client.put(
                f'/tasks/{task["id"]}',
                json=base_task_data,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

    base_json = {
        "name": "name",
        "description": "description",
        "priority": 1,
        "category_id": 1,
        "date": "2025-01-01"
    }

    for i in range(len(get_test_users_data)):
        for j in range(i + 1, len(get_test_users_data)):
            for task2 in TEST_DATA[get_test_users_data[j]["email"]]["tasks"]:
                base_json["category_id"] = TEST_DATA[get_test_users_data[j]["email"]]["categories"][0]["id"]
                response = await client.put(
                    f'/tasks/{task2["id"]}',
                    json=base_json,
                    headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[i]["email"]]["access_token"]}'}
                )
                assert response.status_code == 403

    non_existed_id = -1
    base_json["category_id"] = TEST_DATA[get_test_users_data[0]["email"]]["categories"][0]["id"]
    response = await client.put(
        f'/tasks/{non_existed_id}',
        json=base_json,
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404

    base_json["category_id"] = -1
    response = await client.put(
        f'/tasks/{TEST_DATA[get_test_users_data[0]["email"]]["tasks"][0]["id"]}',
        json=base_json,
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404

    base_json["category_id"] = TEST_DATA[get_test_users_data[1]["email"]]["categories"][0]["id"]
    response = await client.put(
        f'/tasks/{TEST_DATA[get_test_users_data[0]["email"]]["tasks"][0]["id"]}',
        json=base_json,
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_change_task_status(client: AsyncClient, get_test_users_data, get_test_tasks_data):
    response = await client.put("/tasks/1/change_status")
    assert response.status_code == 403

    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)
        await get_tasks_helper(client, user_data)

        for task in TEST_DATA[user_data["email"]]["tasks"]:
            response = await client.put(
                f'/tasks/{task["id"]}/change_status',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

            resp_dict = response.json()
            assert resp_dict["completed"] is False or resp_dict["completed"] is True \
                   and resp_dict["completed"] != task["completed"]

            response = await client.put(
                f'/tasks/{task["id"]}/change_status',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200

    for i in range(len(get_test_users_data)):
        for j in range(i + 1, len(get_test_users_data)):
            for task2 in TEST_DATA[get_test_users_data[j]["email"]]["tasks"]:
                response = await client.put(
                    f'/tasks/{task2["id"]}/change_status',
                    headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[i]["email"]]["access_token"]}'}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.put(
        f'/tasks/{non_existed_id}/change_status',
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, get_test_users_data, get_test_tasks_data):
    response = await client.delete("/tasks/1")
    assert response.status_code == 403

    for i in range(len(get_test_users_data)):
        user_data = get_test_users_data[i]
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

        access_token = TEST_DATA[user_data["email"]]["access_token"] if user_data["email"] in TEST_DATA \
            else await get_token_helper(client, user_data)
        await get_tasks_helper(client, user_data)

        for task in TEST_DATA[user_data["email"]]["tasks"]:
            response = await client.delete(
                f'/tasks/{task["id"]}',
                headers={"Authorization": f"Bearer {access_token}"}
            )
            assert response.status_code == 200
            assert response.json() == SuccessfulResponse().dict()

        TEST_DATA[user_data["email"]]["tasks"] = []
        for task_data in get_test_tasks_data[i]:
            await create_tasks_helper(client, task_data, access_token)
        await get_tasks_helper(client, user_data)

    for i in range(len(get_test_users_data)):
        for j in range(i + 1, len(get_test_users_data)):
            for task2 in TEST_DATA[get_test_users_data[j]["email"]]["tasks"]:
                response = await client.delete(
                    f'/tasks/{task2["id"]}',
                    headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[i]["email"]]["access_token"]}'}
                )
                assert response.status_code == 403

    non_existed_id = -1
    response = await client.delete(
        f'/tasks/{non_existed_id}',
        headers={"Authorization": f'Bearer {TEST_DATA[get_test_users_data[0]["email"]]["access_token"]}'}
    )
    assert response.status_code == 404
