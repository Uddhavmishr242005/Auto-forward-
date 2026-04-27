from database.mongodb import mongodb
from config import SETTINGS_COLLECTION

class StateManager:
    def __init__(self):
        self.collection = None

    async def initialize(self):
        await mongodb.connect()
        self.collection = mongodb.get_collection(SETTINGS_COLLECTION)

        # Ensure default settings exist
        await self.ensure_default_settings()

    async def ensure_default_settings(self):
        """Ensure default settings document exists"""
        settings = await self.collection.find_one({"type": "global"})
        if not settings:
            await self.collection.insert_one({
                "type": "global",
                "is_running": False,
                "message_text": "",
                "delay_time": 1,
                "total_groups": 0,
                "current_index": 0,
                "active_accounts": []
            })

    async def get_all(self):
        settings = await self.collection.find_one({"type": "global"})
        return settings if settings else {
            "is_running": False,
            "message_text": "",
            "delay_time": 1,
            "total_groups": 0,
            "current_index": 0,
            "active_accounts": []
        }

    async def set_running(self, status):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"is_running": status}}
        )

    async def set_message(self, message):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"message_text": message}}
        )

    async def set_delay(self, delay):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"delay_time": delay}}
        )

    async def set_total_groups(self, count):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"total_groups": count}}
        )

    async def set_current_index(self, index):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"current_index": index}}
        )

    async def set_active_accounts(self, accounts):
        await self.collection.update_one(
            {"type": "global"},
            {"$set": {"active_accounts": accounts}}
        )

    async def get_login_state(self, user_id):
        settings = await self.collection.find_one({"type": f"login_{user_id}"})
        return settings.get("state", {}) if settings else {}

    async def set_login_state(self, user_id, state_data):
        await self.collection.update_one(
            {"type": f"login_{user_id}"},
            {"$set": {"state": state_data}},
            upsert=True
        )

    async def clear_login_state(self, user_id):
        await self.collection.delete_one({"type": f"login_{user_id}"})