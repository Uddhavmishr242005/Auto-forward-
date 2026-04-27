from database.accounts import AccountManager
from database.state import StateManager
from services.detector import GroupDetector
import asyncio

class AccountManagerModule:
    def __init__(self):
        self.account_manager = None
        self.state_manager = None

    async def initialize(self):
        self.account_manager = AccountManager()
        await self.account_manager.initialize()
        self.state_manager = StateManager()
        await self.state_manager.initialize()

    async def get_accounts_list(self):
        accounts = await self.account_manager.get_all_accounts()
        if not accounts:
            return "No accounts found."

        result = "📱 Accounts:\n"
        for i, (phone, data) in enumerate(accounts.items(), 1):
            groups_count = len(data.get('groups', []))
            result += f"{i}. {phone} - {groups_count} groups\n"
        return result

    async def remove_single_account(self, phone):
        if await self.account_manager.remove_account(phone):
            return f"Account {phone} removed."
        return "Account not found."

    async def remove_all_accounts(self):
        await self.account_manager.remove_all_accounts()
        return "All accounts removed."

    async def set_account_active(self, phone, active):
        account = await self.account_manager.get_account(phone)
        if not account:
            return f"Account {phone} not found."

        await self.account_manager.set_active(phone, active)
        action = "started" if active else "stopped"
        return f"Account {phone} {action} successfully."

    async def detect_groups_for_all(self):
        accounts = await self.account_manager.get_all_accounts()
        total_groups = 0

        for phone, account_data in accounts.items():
            try:
                groups = await GroupDetector.detect_groups_for_account(
                    account_data['session_string'],
                    account_data['api_id'],
                    account_data['api_hash']
                )
                await self.account_manager.update_groups(phone, groups)
                total_groups += len(groups)
                print(f"Detected {len(groups)} groups for {phone}")
            except Exception as e:
                print(f"Error detecting groups for {phone}: {e}")

        await self.state_manager.set_total_groups(total_groups)
        return f"Group detection completed. Total groups: {total_groups}"