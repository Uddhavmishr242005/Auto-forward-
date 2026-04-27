from database.mongodb import mongodb
from config import USERS_COLLECTION, OWNER_ID
from typing import Optional

class UserManager:
    def __init__(self):
        self.collection = None

    async def initialize(self):
        await mongodb.connect()
        self.collection = mongodb.get_collection(USERS_COLLECTION)

        # Ensure owner exists
        await self.ensure_owner()

    async def ensure_owner(self):
        """Ensure the owner is in the database"""
        owner_doc = await self.collection.find_one({"user_id": OWNER_ID})
        if not owner_doc:
            await self.collection.insert_one({
                "user_id": OWNER_ID,
                "role": "owner"
            })

    async def get_user_role(self, user_id: int) -> Optional[str]:
        """Get user role, returns None if user not authorized"""
        user_doc = await self.collection.find_one({"user_id": user_id})
        return user_doc.get("role") if user_doc else None

    async def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        role = await self.get_user_role(user_id)
        return role is not None

    async def is_owner(self, user_id: int) -> bool:
        """Check if user is owner"""
        role = await self.get_user_role(user_id)
        return role == "owner"

    async def add_user(self, user_id: int, role: str = "user") -> bool:
        """Add a user to authorized list"""
        if role not in ["user", "owner"]:
            return False

        # Check if user already exists
        existing = await self.collection.find_one({"user_id": user_id})
        if existing:
            return False

        await self.collection.insert_one({
            "user_id": user_id,
            "role": role
        })
        return True

    async def remove_user(self, user_id: int) -> bool:
        """Remove a user from authorized list"""
        # Don't allow removing owner
        if user_id == OWNER_ID:
            return False

        result = await self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    async def get_all_users(self) -> list:
        """Get all authorized users"""
        users = []
        async for user in self.collection.find():
            users.append({
                "user_id": user["user_id"],
                "role": user["role"]
            })
        return users

    async def update_user_role(self, user_id: int, new_role: str) -> bool:
        """Update user role"""
        if new_role not in ["user", "owner"]:
            return False

        # Don't allow changing owner's role
        if user_id == OWNER_ID:
            return False

        result = await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"role": new_role}}
        )
        return result.modified_count > 0