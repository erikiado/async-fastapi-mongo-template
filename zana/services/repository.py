from bson import ObjectId
from pymongo.errors import WriteError
from pymongo.results import InsertOneResult

import zana.main as zana
from zana.routers.exceptions import AlreadyExistsHTTPException


async def document_id_helper(document: dict) -> dict:
    document["id"] = document.pop("_id")
    return document


async def retrieve_user(document_id: str, collection: str) -> dict:
    """

    :param document_id:
    :param collection:
    :return:
    """
    document_filter = {"_id": ObjectId(document_id)}
    if document := await zana.app.state.mongo_collection[collection].find_one(document_filter):
        return await document_id_helper(document)
    else:
        raise ValueError(f"No document found for {document_id=} in {collection=}")


async def retrieve_users(collection: str) -> list:
    """

    :param collection:
    :return:
    """
    documents = []
    async for document in zana.app.state.mongo_collection[collection].find():
        documents.append(await document_id_helper(document))
    return {
        "users": documents
    }


async def create_user(document, collection: str) -> InsertOneResult:
    """

    :param document:
    :param collection:
    :return:
    """
    try:
        # document["created_at"] = datetime.now()
        document: InsertOneResult = await zana.app.state.mongo_collection[collection].insert_one(
            document.model_dump())
        return document
    except WriteError as e:
        # TODO: this not make sense as id from mongo will be always unique if we not pass it
        raise AlreadyExistsHTTPException(msg=str(e)) from e


async def update_user_by_id(document_id: str, document: dict, collection: str) -> dict:
    """

    :param document_id:
    :param document:
    :param collection:
    :return:
    """
    document_filter = {"_id": ObjectId(document_id)}
    if await zana.app.state.mongo_collection[collection].find_one(document_filter):
        await zana.app.state.mongo_collection[collection].update_one(document_filter, {"$set": document.model_dump(exclude_unset=True)})
        return await retrieve_user(document_id, collection)
    else:
        raise ValueError(f"No document found for {document_id=} in {collection=}")


async def delete_user_by_id(document_id: str, collection: str) -> dict:
    """

    :param document_id:
    :param collection:
    :return:
    """
    document_filter = {"_id": ObjectId(document_id)}
    if document := await zana.app.state.mongo_collection[collection].find_one(document_filter):
        await zana.app.state.mongo_collection[collection].delete_one(document_filter)
        return await document_id_helper(document)
    else:
        raise ValueError(f"No document found for {document_id=} in {collection=}")


async def get_mongo_meta() -> dict:
    list_databases = await zana.app.state.mongo_client.list_database_names()
    list_of_collections = {}
    for db in list_databases:
        list_of_collections[db] = await zana.app.state.mongo_client[db].list_collection_names()
    mongo_meta = await zana.app.state.mongo_client.server_info()
    return {"version": mongo_meta["version"], "databases": list_databases, "collections": list_of_collections}
