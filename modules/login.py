from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
from database.accounts import AccountManager
from database.state import StateManager
import asyncio

class LoginManager:
    def __init__(self):
        self.account_manager = None
        self.state_manager = None

    async def initialize(self):
        self.account_manager = AccountManager()
        await self.account_manager.initialize()
        self.state_manager = StateManager()
        await self.state_manager.initialize()

    async def start_login(self, user_id, api_id, api_hash, phone):
        # Save login state
        await self.state_manager.set_login_state(user_id, {
            'step': 'phone',
            'api_id': api_id,
            'api_hash': api_hash,
            'phone': phone
        })

        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()

        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await self.state_manager.set_login_state(user_id, {
                'step': 'otp',
                'api_id': api_id,
                'api_hash': api_hash,
                'phone': phone
            })
            await client.disconnect()
            return "OTP sent. Please enter the code:"
        else:
            # Already authorized
            session_string = client.session.save()
            await self.account_manager.add_account(phone, session_string, api_id, api_hash, user_id)
            await client.disconnect()
            await self.state_manager.clear_login_state(user_id)
            return "Already logged in! Account added."

    async def verify_otp(self, user_id, otp_code):
        state = await self.state_manager.get_login_state(user_id)
        if state.get('step') != 'otp':
            return "No active login session."

        api_id = state['api_id']
        api_hash = state['api_hash']
        phone = state['phone']

        # For simplicity, we'll recreate client. In production, store client in memory
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()

        try:
            await client.sign_in(phone, otp_code)
        except SessionPasswordNeededError:
            await self.state_manager.set_login_state(user_id, {
                'step': '2fa',
                'api_id': api_id,
                'api_hash': api_hash,
                'phone': phone
            })
            await client.disconnect()
            return "2FA required. Please enter your password:"
        except Exception as e:
            await client.disconnect()
            await self.state_manager.clear_login_state(user_id)
            return f"Login failed: {e}"

        # Success
        session_string = client.session.save()
        await self.account_manager.add_account(phone, session_string, api_id, api_hash, user_id)
        await client.disconnect()
        await self.state_manager.clear_login_state(user_id)
        return "Login successful! Account added."

    async def verify_2fa(self, user_id, password):
        state = await self.state_manager.get_login_state(user_id)
        if state.get('step') != '2fa':
            return "No active 2FA session."

        api_id = state['api_id']
        api_hash = state['api_hash']
        phone = state['phone']

        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.connect()

        try:
            await client.sign_in(password=password)
        except Exception as e:
            await client.disconnect()
            await self.state_manager.clear_login_state(user_id)
            return f"2FA failed: {e}"

        # Success
        session_string = client.session.save()
        await self.account_manager.add_account(phone, session_string, api_id, api_hash, user_id)
        await client.disconnect()
        await self.state_manager.clear_login_state(user_id)
        return "Login successful! Account added."