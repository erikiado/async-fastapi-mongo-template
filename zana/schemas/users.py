from bson import ObjectId as _ObjectId
from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import List, Optional
from typing_extensions import Annotated


# def check_object_id(value: str) -> str:
#     if not _ObjectId.is_valid(value):
#         raise ValueError('Invalid ObjectId')
#     return value


def check_object_id(value: _ObjectId) -> str:
    """
    Checks if the given _ObjectId is valid and returns it as a string.

    Args:
        value: The _ObjectId to be checked.

    Returns:
        str: The _ObjectId as a string.

    Raises:
        ValueError: If the _ObjectId is invalid.
    """

    if not _ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")
    return str(value)


ObjectIdField = Annotated[str, BeforeValidator(check_object_id)]

config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)


class User(BaseModel):
    model_config = config

    # optional name
    name: str
    age: int
    telephone: str
    created_at: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    telephone: Optional[str] = None


class UserResponse(BaseModel):
    id: ObjectIdField


class UsersResponse(BaseModel):
    users: List[UserResponse]
