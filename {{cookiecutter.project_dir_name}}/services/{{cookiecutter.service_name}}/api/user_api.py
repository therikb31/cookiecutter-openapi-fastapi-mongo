from typing import List, Optional, Dict
from fastapi import HTTPException

from openapi.{{ cookiecutter.service_name }}.apis.user_api_base import BaseUserApi
from openapi.{{ cookiecutter.service_name }}.models.user import User
from libs.mongodb.odm import MongoDBAPI
from libs.mongodb.databases import MongoDatabases
from libs.mongodb.collections import MongoCollections
from libs.mongodb.client import MongoManager


class UserApiImpl(BaseUserApi):
    """
    A MongoDB implementation of the User API.
    """

    def __init__(self):
        self.db = MongoDBAPI(
            client=MongoManager.get_client(),
            database_name=MongoDatabases.PROJECT.value,
            collection_name=MongoCollections.USERS.value,
            model=User,
        )

    async def create_user(
        self,
        user: Optional[User],
    ) -> User:
        """This can only be done by the logged in user."""
        if user and user.username:
            # check if user already exists?
            existing = await self.db.find_one({"username": user.username})
            if existing:
                # Update? Or fail? The previous impl updated/overwrote
                await self.db.update_one({"username": user.username}, user)
                return user
            else:
                await self.db.insert_one(user)
                return user

        # If valid user not provided, or username missing
        if user:
            # Fallback if just one of them is missing?
            # Previous impl raised 400 only if 'user' was None (actually that logic was a bit fuzzy)
            pass

        raise HTTPException(status_code=400, detail="Invalid user input")

    async def create_users_with_list_input(
        self,
        user: Optional[List[User]],
    ) -> User:
        """Creates list of users with given input array."""
        if user:
            last_user = None
            for u in user:
                if u and u.username:
                    existing = await self.db.find_one({"username": u.username})
                    if existing:
                        await self.db.update_one({"username": u.username}, u)
                    else:
                        await self.db.insert_one(u)
                    last_user = u

            if last_user:
                return last_user

        raise HTTPException(status_code=400, detail="No users provided")

    async def login_user(
        self,
        username: Optional[str],
        password: Optional[str],
    ) -> str:
        """Log into the system."""
        if username:
            stored_user = await self.db.find_one({"username": username})
            if stored_user and stored_user.password == password:
                return f"logged-in-token-{username}"

        raise HTTPException(
            status_code=400, detail="Invalid username/password supplied"
        )

    async def logout_user(
        self,
    ) -> None:
        """Log user out of the system."""
        # Stateless / demo implementation - nothing to invalidate
        pass

    async def get_user_by_name(
        self,
        username: str,
    ) -> User:
        """Get user detail based on username."""
        user = await self.db.find_one({"username": username})
        if user:
            return user

        raise HTTPException(status_code=404, detail="User not found")

    async def update_user(
        self,
        username: str,
        user: Optional[User],
    ) -> None:
        """This can only be done by the logged in user."""
        existing = await self.db.find_one({"username": username})
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")

        if user:
            if user.username and user.username != username:
                # Update username means creating new doc and deleting old one, or just updating field if we used _id
                # Since we don't have stable IDs in this random model, let's treat username as PK
                # Check collision
                collision = await self.db.find_one({"username": user.username})
                if collision:
                    # This might be tricky. The original impl just overwrote.
                    # Let's delete old and insert new.
                    await self.db.delete_one({"username": username})
                    await self.db.insert_one(user)
                else:
                    await self.db.delete_one({"username": username})
                    await self.db.insert_one(user)
            else:
                await self.db.update_one({"username": username}, user)

    async def delete_user(
        self,
        username: str,
    ) -> None:
        """This can only be done by the logged in user."""
        success = await self.db.delete_one({"username": username})
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
