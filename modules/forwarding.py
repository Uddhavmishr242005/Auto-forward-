from database.accounts import AccountManager
from database.state import StateManager
from services.sender import MessageSender
from services.detector import GroupDetector
import asyncio
import threading

class ForwardingManager:
    def __init__(self):
        self.account_manager = None
        self.state_manager = None
        self.is_running = False
        self.thread = None

    async def initialize(self):
        self.account_manager = AccountManager()
        await self.account_manager.initialize()
        self.state_manager = StateManager()
        await self.state_manager.initialize()

    async def start_forwarding(self):
        if self.is_running:
            return "Already running!"

        state = await self.state_manager.get_all()
        if not state['message_text']:
            return "No message set! Please set a custom message first."

        accounts = await self.account_manager.get_all_accounts()
        if not accounts:
            return "No accounts available! Please login first."

        self.is_running = True
        await self.state_manager.set_running(True)
        self.thread = threading.Thread(target=self._forward_loop, daemon=True)
        self.thread.start()
        return "Forwarding started!"

    async def stop_forwarding(self):
        self.is_running = False
        await self.state_manager.set_running(False)
        return "Forwarding stopped!"

    def _forward_loop(self):
        asyncio.run(self._async_forward_loop())

    async def _async_forward_loop(self):
        while self.is_running:
            state = await self.state_manager.get_all()
            message = state['message_text']
            delay = state['delay_time']

            accounts = await self.account_manager.get_all_accounts()

            for phone, account_data in accounts.items():
                if not self.is_running:
                    break

                groups = account_data.get('groups', [])
                if not groups:
                    # Try to detect groups
                    try:
                        groups = await GroupDetector.detect_groups_for_account(
                            account_data['session_string'],
                            account_data['api_id'],
                            account_data['api_hash']
                        )
                        await self.account_manager.update_groups(phone, groups)
                    except Exception as e:
                        print(f"Error detecting groups for {phone}: {e}")
                        continue

                if groups:
                    sent = await MessageSender.send_to_account_groups(
                        account_data['session_string'],
                        account_data['api_id'],
                        account_data['api_hash'],
                        groups,
                        message,
                        delay
                    )
                    print(f"Sent to {sent}/{len(groups)} groups for account {phone}")

            # Wait for timer
            await asyncio.sleep(delay * 60)  # Convert minutes to seconds, adjust as needed

    async def test_forward(self):
        state = await self.state_manager.get_all()
        message = state['message_text']
        if not message:
            return "No message set!"

        accounts = await self.account_manager.get_all_accounts()
        total_groups = sum(len(acc.get('groups', [])) for acc in accounts.values())

        return f"Test: Message='{message[:50]}...', Accounts={len(accounts)}, Total Groups={total_groups}"