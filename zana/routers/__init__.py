from fastapi import APIRouter

from zana.routers.v1.users import router as users_api

router = APIRouter()

router.include_router(users_api, prefix="/users", tags=["users"])
