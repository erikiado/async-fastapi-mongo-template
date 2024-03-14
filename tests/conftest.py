from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from bson import ObjectId
from datetime import datetime

from zana.config import settings as global_settings
from zana.main import app, init_mongo
from zana.utils import get_logger


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(
            app=app,
            base_url="http://testserver",
    ) as client:
        app.state.logger = get_logger(__name__)
        app.state.mongo_client, app.state.mongo_db, app.state.mongo_collection = await init_mongo(
            global_settings.test_db_name, global_settings.db_url, global_settings.collection
        )

        collection = global_settings.collection

        # Drop collection
        await app.state.mongo_collection[collection].drop()
        # Create mock users
        users = create_mock_users()
        for user in users:
            await app.state.mongo_collection[collection].insert_one(user)

        yield client


# Create mock users
def create_mock_users():
    return [
        {
            "_id": ObjectId("60e9e2b1b3e9e4d3e4e6e3e9"),
            "name": "Erick",
            "age": 30,
            "telephone": "1234567890",
            "created_at": datetime.now().isoformat(),
        },
        {
            "_id": ObjectId("60e9e2b1b3e9e4d3e4e6e3e8"),
            "name": "John",
            "age": 40,
            "telephone": "0987654321",
            "created_at": datetime.now().isoformat(),
        },
    ]
