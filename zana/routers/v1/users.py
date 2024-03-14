from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from zana.config import settings as global_settings
from zana.routers.exceptions import NotFoundHTTPException
from zana.schemas.users import User, UserResponse, ObjectIdField, UsersResponse, UserUpdate
from zana.services.repository import create_user, retrieve_user, retrieve_users, update_user_by_id, delete_user_by_id

collection = global_settings.collection

router = APIRouter()


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_description="User created",
    response_model=UserResponse,
)
async def add_user(payload: User):
    """

    :param payload:
    :return:
    """
    try:
        # payload = jsonable_encoder(payload)
        document = await create_user(payload, collection)
        return {"id": str(document.inserted_id)}
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception)) from exception


@router.get(
    "/{object_id}",
    response_description="User retrieved",
    response_model=UserResponse,
)
async def get_user(object_id: ObjectIdField):
    """

    :param object_id:
    :return:
    """
    # print(f"object_id: {object_id}")
    try:
        return await retrieve_user(object_id, collection)
    except (ValueError, TypeError) as exception:
        raise NotFoundHTTPException(msg=str(exception)) from exception


@router.get(
    "/",
    response_description="Users retrieved",
    response_model=UsersResponse,
)
async def get_users():
    """

    :return:
    """
    try:
        return await retrieve_users(collection)
    except (ValueError, TypeError) as exception:
        raise NotFoundHTTPException(msg=str(exception)) from exception


@router.put(
    "/{object_id}",
    response_description="User updated",
    response_model=UserResponse,
)
async def update_user(object_id: ObjectIdField, payload: UserUpdate):
    """

    :param object_id:
    :param payload:
    :return:
    """
    try:
        # payload = jsonable_encoder(payload)
        document = await update_user_by_id(object_id, payload, collection)
        return document
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception)) from exception


@router.delete(
    "/{object_id}",
    response_description="User deleted",
    response_model=UserResponse,
)
async def delete_user(object_id: ObjectIdField):
    """

    :param object_id:
    :return:
    """
    try:
        return await delete_user_by_id(object_id, collection)
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception)) from exception
