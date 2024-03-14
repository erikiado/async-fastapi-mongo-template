from contextlib import asynccontextmanager

from fastapi import FastAPI

from zana.config import settings as global_settings
from zana.routers import router as v1
from zana.services.repository import get_mongo_meta
from zana.utils import get_logger, init_mongo

if global_settings.environment == "local":
    get_logger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = get_logger(__name__)
    app.state.logger.info("Starting zana-cion...")
    app.state.mongo_client, app.state.mongo_db, app.state.mongo_collection = await init_mongo(
        global_settings.db_name, global_settings.db_url, global_settings.collection
    )
    try:
        yield
    finally:
        app.state.logger.info("hope you feel better...")


app = FastAPI(lifespan=lifespan, title="Zana Users API", version="0.1.0")

app.include_router(v1, prefix="/api/v1")


@app.get("/health-check")
async def health_check():
    return await get_mongo_meta()
