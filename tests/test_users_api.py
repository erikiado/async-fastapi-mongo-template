import pytest
from bson import ObjectId
from fastapi import status
from httpx import AsyncClient
from datetime import datetime

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "payload, status_code",
    ((
        {
            "name": "Erick",
            "age": "30",
            "telephone": "1234567890",
            "created_at": datetime.now().isoformat(),
        },
        status.HTTP_201_CREATED,
    ),),
)
@pytest.mark.asyncio
# Test document create endpoint
async def test_create_user(client: AsyncClient, payload: dict, status_code: int):
    # Send POST request
    response = await client.post("/api/v1/users", json=payload)
    # Assert HTTP code and if received document id is valid
    assert response.status_code == status_code
    print(response.json())
    assert ObjectId.is_valid(response.json()["id"])


@pytest.mark.parametrize(
    "object_id, status_code",
    (
        ("60e9e2b1b3e9e4d3e4e6e3e9", status.HTTP_200_OK),
        ("60e9e2b1b3e9e4d3e4e6e3e7", status.HTTP_404_NOT_FOUND),
    ),
)
@pytest.mark.asyncio
# Test document retrieve endpoint
async def test_retrieve_user(client: AsyncClient, object_id: str, status_code: int):
    # Send GET request
    response = await client.get(f"/api/v1/users/{object_id}")
    # Assert HTTP code
    assert response.status_code == status_code
    # If response is OK, assert if received document id is valid
    if status_code == status.HTTP_200_OK:
        assert ObjectId.is_valid(response.json()["id"])
    else:
        assert response.json() == {'detail': "No document found for document_id='60e9e2b1b3e9e4d3e4e6e3e7' in collection='users'"}
    print(response.json())


# Test documents retrieve endpoint
@pytest.mark.asyncio
async def test_retrieve_users(client: AsyncClient):
    # Send GET request
    response = await client.get("/api/v1/users/")
    # Assert HTTP code
    assert response.status_code == status.HTTP_200_OK
    # Assert if received document id is valid
    for document in response.json()["users"]:
        assert ObjectId.is_valid(document["id"])
    print(response.json())


@pytest.mark.parametrize(
    "object_id, status_code",
    (
        ("60e9e2b1b3e9e4d3e4e6e3e9", status.HTTP_200_OK),
        ("60e9e2b1b3e9e4d3e4e6e3e7", status.HTTP_404_NOT_FOUND),
    ),
)
@pytest.mark.asyncio
# Test document update endpoint
async def test_update_user(client: AsyncClient, object_id: str, status_code: int):
    # Send PUT request
    response = await client.put(f"/api/v1/users/{object_id}", json={"name": "Erikiado"})
    # Assert HTTP code
    assert response.status_code == status_code
    # If response is OK, assert if received document id is valid
    if status_code == status.HTTP_200_OK:
        assert ObjectId.is_valid(response.json()["id"])
    else:
        assert response.json() == {'detail': "No document found for document_id='60e9e2b1b3e9e4d3e4e6e3e7' in collection='users'"}
    print(response.json())


# Test document delete endpoint
@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    # Send DELETE request
    response = await client.delete("/api/v1/users/60e9e2b1b3e9e4d3e4e6e3e9")
    # Assert HTTP code
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
