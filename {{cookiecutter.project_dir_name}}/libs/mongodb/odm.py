from typing import Type, TypeVar, List, Optional, Generic, Dict, Any
from pydantic import BaseModel
from pymongo import ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient

T = TypeVar("T", bound=BaseModel)


class MongoDBAPI(Generic[T]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        database_name: str,
        collection_name: str,
        model: Type[T],
    ):
        self._client = client
        self._database_name = database_name
        self._collection_name = collection_name
        self.model = model

    @property
    def collection(self):
        return self._client[self._database_name][self._collection_name]

    async def find_one(self, query: Dict[str, Any]) -> Optional[T]:
        document = await self.collection.find_one(query)
        if document:
            return self.model.model_validate(document)
        return None

    async def find_many(self, query: Dict[str, Any] = {}, limit: int = 100) -> List[T]:
        cursor = self.collection.find(query).limit(limit)
        results = []
        async for document in cursor:
            results.append(self.model.model_validate(document))
        return results

    async def insert_one(self, document: T) -> T:
        data = document.model_dump(by_alias=True, exclude_none=True)
        await self.collection.insert_one(data)
        return document

    async def update_one(self, query: Dict[str, Any], update_data: T) -> Optional[T]:
        data = update_data.model_dump(by_alias=True, exclude_none=True)
        updated_document = await self.collection.find_one_and_update(
            query, {"$set": data}, return_document=ReturnDocument.AFTER
        )
        if updated_document:
            return self.model.model_validate(updated_document)
        return None

    async def delete_one(self, query: Dict[str, Any]) -> bool:
        result = await self.collection.delete_one(query)
        return result.deleted_count > 0
