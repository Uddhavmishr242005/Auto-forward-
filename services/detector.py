from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel
from config import MAX_GROUPS_PER_ACCOUNT
import asyncio

class GroupDetector:
    def __init__(self, session_string, api_id, api_hash):
        self.session_string = session_string
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None

    async def connect(self):
        self.client = TelegramClient(
            StringSession(self.session_string),
            self.api_id,
            self.api_hash
        )
        await self.client.connect()

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()

    async def detect_groups(self):
        if not self.client:
            await self.connect()

        groups = []
        try:
            async for dialog in self.client.iter_dialogs():
                if isinstance(dialog.entity, Channel) and dialog.entity.megagroup:
                    # It's a supergroup/channel
                    groups.append({
                        'chat_id': dialog.entity.id,
                        'title': dialog.entity.title,
                        'username': dialog.entity.username
                    })
                elif hasattr(dialog.entity, 'megagroup') and dialog.entity.megagroup:
                    # Regular group
                    groups.append({
                        'chat_id': dialog.entity.id,
                        'title': dialog.entity.title,
                        'username': dialog.entity.username
                    })

                if len(groups) >= MAX_GROUPS_PER_ACCOUNT:
                    break

        except Exception as e:
            print(f"Error detecting groups: {e}")

        return groups

    @staticmethod
    async def detect_groups_for_account(session_string, api_id, api_hash):
        detector = GroupDetector(session_string, api_id, api_hash)
        try:
            await detector.connect()
            groups = await detector.detect_groups()
            return groups
        finally:
            await detector.disconnect()