from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
from config import FLOOD_WAIT_BASE, MESSAGE_DELAY
import asyncio

class MessageSender:
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

    async def send_message(self, chat_id, message):
        if not self.client:
            await self.connect()

        try:
            await self.client.send_message(chat_id, message)
            await asyncio.sleep(MESSAGE_DELAY)
            return True
        except FloodWaitError as e:
            print(f"Flood wait: {e.seconds}")
            await asyncio.sleep(e.seconds + FLOOD_WAIT_BASE)
            return await self.send_message(chat_id, message)
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")
            return False

    async def send_to_groups(self, groups, message, delay=1):
        sent_count = 0
        for group in groups:
            success = await self.send_message(group['chat_id'], message)
            if success:
                sent_count += 1
            await asyncio.sleep(delay)
        return sent_count

    @staticmethod
    async def send_to_account_groups(session_string, api_id, api_hash, groups, message, delay=1):
        sender = MessageSender(session_string, api_id, api_hash)
        try:
            await sender.connect()
            sent = await sender.send_to_groups(groups, message, delay)
            return sent
        finally:
            await sender.disconnect()