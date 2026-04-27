from database.mongodb import mongodb
from config import ACCOUNTS_COLLECTION, SESSIONS_DIR
import os

class AccountManager:
    def __init__(self):
        self.collection = None
        self.sessions_dir = SESSIONS_DIR
        os.makedirs(self.sessions_dir, exist_ok=True)

    async def initialize(self):
        await mongodb.connect()
        self.collection = mongodb.get_collection(ACCOUNTS_COLLECTION)

    async def add_account(self, phone, session_string, api_id, api_hash, user_id):
        doc = {
            'phone': phone,
            'session_string': session_string,
            'api_id': api_id,
            'api_hash': api_hash,
            'user_id': user_id,
            'active': True,
            'groups': []
        }
        await self.collection.insert_one(doc)

    async def remove_account(self, phone):
        result = await self.collection.delete_one({'phone': phone})
        # Remove session file if exists
        session_file = os.path.join(self.sessions_dir, f"{phone}.session")
        if os.path.exists(session_file):
            os.remove(session_file)
        return result.deleted_count > 0

    async def remove_all_accounts(self):
        # Get all phones first
        phones = []
        async for account in self.collection.find():
            phones.append(account['phone'])

        # Remove from database
        await self.collection.delete_many({})

        # Remove session files
        for phone in phones:
            session_file = os.path.join(self.sessions_dir, f"{phone}.session")
            if os.path.exists(session_file):
                os.remove(session_file)

        return True

    async def get_account(self, phone):
        return await self.collection.find_one({'phone': phone})

    async def get_all_accounts(self):
        accounts = {}
        async for account in self.collection.find():
            accounts[account['phone']] = account
        return accounts

    async def get_user_accounts(self, user_id):
        accounts = {}
        async for account in self.collection.find({'user_id': user_id}):
            accounts[account['phone']] = account
        return accounts

    async def update_groups(self, phone, groups):
        await self.collection.update_one(
            {'phone': phone},
            {'$set': {'groups': groups}}
        )

    async def get_groups(self, phone):
        account = await self.collection.find_one({'phone': phone})
        return account.get('groups', []) if account else []

    async def set_active(self, phone, active):
        await self.collection.update_one(
            {'phone': phone},
            {'$set': {'active': active}}
        )