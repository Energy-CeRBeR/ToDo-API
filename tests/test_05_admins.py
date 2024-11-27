import pytest
from httpx import AsyncClient

from tests.conftest import create_user_helper, TEST_DATA, TEST_ADMIN_DATA, create_admin_and_base_users_helper, \
    get_all_users_helper
from src.users.repositories import UserRepository


@pytest.mark.asyncio
async def test_get_all_users_data(client: AsyncClient, get_test_users_data):
    response = await client.get("/admin/users")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.get("/admin/users", headers={"Authorization": f"Bearer {user_access_token}"})
    assert response.status_code == 403

    response = await client.get("/admin/users", headers={"Authorization": f"Bearer {admin_access_token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, get_test_users_data):
    response = await client.get("/admin/users/1")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    all_users_dict = await get_all_users_helper()

    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.get(
        f"/admin/users/{all_users_dict[0]['id']}",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403

    for user in all_users_dict:
        response = await client.get(
            f"/admin/users/{user['id']}",
            headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        assert response.status_code == 200

    response = await client.get(
        f"/admin/users/-1",
        headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_change_admin_status(client: AsyncClient, get_test_users_data):
    response = await client.put("/admin/users/1/change_admin_status")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    all_users_dict = await get_all_users_helper()

    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.put(
        f"/admin/users/{all_users_dict[0]['id']}/change_admin_status",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403

    for user in all_users_dict:
        response = await client.put(
            f"/admin/users/{user['id']}/change_admin_status",
            headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        if not user["is_admin"]:
            assert response.status_code == 200
            assert response.json()["is_admin"] != user["is_admin"]

            await UserRepository().change_admin_status(await UserRepository().get_user_by_id(user["id"]))
        else:
            assert response.status_code == 403

    response = await client.put(
        f"/admin/users/-1/change_admin_status",
        headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_change_verified_status(client: AsyncClient, get_test_users_data):
    response = await client.put("/admin/users/1/change_verified_status")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    all_users_dict = await get_all_users_helper()

    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.put(
        f"/admin/users/{all_users_dict[0]['id']}/change_verified_status",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403

    for user in all_users_dict:
        response = await client.put(
            f"/admin/users/{user['id']}/change_verified_status",
            headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        if not user["is_admin"]:
            assert response.status_code == 200
            assert response.json()["is_verified"] != user["is_verified"]

            await UserRepository().change_verified_status(await UserRepository().get_user_by_id(user["id"]))
        else:
            assert response.status_code == 403

    response = await client.put(
        f"/admin/users/-1/change_verified_status",
        headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_change_active_status(client: AsyncClient, get_test_users_data):
    response = await client.put("/admin/users/1/change_active_status")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    all_users_dict = await get_all_users_helper()

    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.put(
        f"/admin/users/{all_users_dict[0]['id']}/change_active_status",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403

    for user in all_users_dict:
        response = await client.put(
            f"/admin/users/{user['id']}/change_active_status",
            headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        if not user["is_admin"]:
            assert response.status_code == 200
            assert response.json()["is_active"] != user["is_active"]

            await UserRepository().change_active_status(await UserRepository().get_user_by_id(user["id"]))
        else:
            assert response.status_code == 403

    response = await client.put(
        f"/admin/users/-1/change_active_status",
        headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_by_id(client: AsyncClient, get_test_users_data):
    response = await client.delete("/admin/users/1")
    assert response.status_code == 403

    for user_data in get_test_users_data:
        if user_data["email"] not in TEST_DATA:
            await create_user_helper(client, user_data)

    await create_admin_and_base_users_helper(client)
    all_users_dict = await get_all_users_helper()

    admin_access_token = TEST_ADMIN_DATA["admin"]["access_token"]
    user_access_token = TEST_ADMIN_DATA["user"]["access_token"]

    response = await client.delete(
        f"/admin/users/{all_users_dict[0]['id']}",
        headers={"Authorization": f"Bearer {user_access_token}"}
    )
    assert response.status_code == 403

    for user in all_users_dict:
        response = await client.delete(
            f"/admin/users/{user['id']}",
            headers={"Authorization": f"Bearer {admin_access_token}"}
        )
        if not user["is_admin"]:
            assert response.status_code == 200
        else:
            assert response.status_code == 403

    TEST_DATA.clear()

    response = await client.delete(
        f"/admin/users/-1",
        headers={"Authorization": f"Bearer {admin_access_token}"}
    )
    assert response.status_code == 404
