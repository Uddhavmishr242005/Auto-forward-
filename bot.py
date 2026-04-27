import asyncio
from config import BOT_TOKEN, OWNER_ID
from helpers.buttons import main_menu, account_menu, manage_accounts_menu, timer_menu, back_to_main, confirm_remove_all, admin_panel
from modules.login import LoginManager
from modules.forwarding import ForwardingManager
from modules.timer import TimerManager
from modules.account import AccountManagerModule
from modules.user_manager import UserManager
from database.state import StateManager

# Only import telegram stuff if we have a token
if BOT_TOKEN and BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE':
    from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
else:
    print("Warning: BOT_TOKEN not set. Bot will not function without proper token.")

class TelegramBot:
    def __init__(self):
        if not (BOT_TOKEN and BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE'):
            raise ValueError("BOT_TOKEN not configured")

        self.app = Application.builder().token(BOT_TOKEN).build()
        self.login_manager = None
        self.forwarding_manager = None
        self.timer_manager = None
        self.account_manager_module = None
        self.user_manager = None
        self.state_manager = None

    async def initialize(self):
        # Initialize all managers
        self.login_manager = LoginManager()
        await self.login_manager.initialize()

        self.forwarding_manager = ForwardingManager()
        await self.forwarding_manager.initialize()

        self.timer_manager = TimerManager()
        await self.timer_manager.initialize()

        self.account_manager_module = AccountManagerModule()
        await self.account_manager_module.initialize()

        self.user_manager = UserManager()
        await self.user_manager.initialize()

        self.state_manager = StateManager()
        await self.state_manager.initialize()

        # Setup handlers
        self.setup_handlers()

    def setup_handlers(self):
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))

        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))

        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        # Check authorization
        if not await self.user_manager.is_authorized(user_id):
            await update.message.reply_text(
                "❌ Access Denied!\n\nYou are not authorized to use this bot.\nContact the owner for access."
            )
            return

        await update.message.reply_text(
            "🚀 Welcome to Telegram Auto Forward Bot!\n\nChoose an option:",
            reply_markup=main_menu()
        )

    async def check_authorization(self, user_id: int) -> bool:
        """Check if user is authorized"""
        return await self.user_manager.is_authorized(user_id)

    async def check_owner(self, user_id: int) -> bool:
        """Check if user is owner"""
        return await self.user_manager.is_owner(user_id)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        data = query.data
        user_id = update.effective_user.id

        # Check authorization
        if not await self.check_authorization(user_id):
            await query.edit_message_text("❌ Access Denied! You are not authorized to use this bot.")
            return

        if data == "main_menu":
            await query.edit_message_text("Main Menu:", reply_markup=main_menu())

        elif data == "admin_panel":
            if not await self.check_owner(user_id):
                await query.edit_message_text("❌ Only owner can access admin panel!", reply_markup=main_menu())
                return
            await query.edit_message_text("🔐 Admin Panel:", reply_markup=admin_panel())

        elif data == "add_user":
            if not await self.check_owner(user_id):
                await query.edit_message_text("❌ Only owner can add users!", reply_markup=admin_panel())
                return
            await query.edit_message_text(
                "➕ Add User\n\nSend the Telegram User ID to add:",
                reply_markup=back_to_main()
            )
            context.user_data['expecting'] = 'add_user'

        elif data == "remove_user":
            if not await self.check_owner(user_id):
                await query.edit_message_text("❌ Only owner can remove users!", reply_markup=admin_panel())
                return
            users = await self.user_manager.get_all_users()
            if not users:
                await query.edit_message_text("No users to remove.", reply_markup=admin_panel())
                return

            keyboard = []
            for user in users:
                if user['user_id'] != OWNER_ID:  # Don't allow removing owner
                    keyboard.append([InlineKeyboardButton(f"Remove {user['user_id']} ({user['role']})", callback_data=f"remove_user_{user['user_id']}")])
            keyboard.append([InlineKeyboardButton("Back to Admin Panel 🔙", callback_data="admin_panel")])

            await query.edit_message_text(
                "Select user to remove:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data.startswith("remove_user_"):
            if not await self.check_owner(user_id):
                await query.edit_message_text("❌ Only owner can remove users!", reply_markup=admin_panel())
                return
            target_user_id = int(data[12:])  # Remove "remove_user_" prefix
            if await self.user_manager.remove_user(target_user_id):
                await query.edit_message_text(f"✅ User {target_user_id} removed!", reply_markup=admin_panel())
            else:
                await query.edit_message_text("❌ Failed to remove user!", reply_markup=admin_panel())

        elif data == "list_users":
            if not await self.check_owner(user_id):
                await query.edit_message_text("❌ Only owner can list users!", reply_markup=admin_panel())
                return
            users = await self.user_manager.get_all_users()
            if not users:
                await query.edit_message_text("No users found.", reply_markup=admin_panel())
                return

            user_list = "📋 Authorized Users:\n\n"
            for user in users:
                user_list += f"ID: {user['user_id']} - Role: {user['role']}\n"
            await query.edit_message_text(user_list, reply_markup=admin_panel())

        elif data == "custom_messages":
            await query.edit_message_text(
                "💬 Send your custom message:",
                reply_markup=back_to_main()
            )
            # Set state for expecting message
            context.user_data['expecting'] = 'custom_message'

        elif data == "timer":
            await query.edit_message_text("⏳ Timer Settings:", reply_markup=timer_menu())

        elif data == "test_forward":
            result = await self.forwarding_manager.test_forward()
            await query.edit_message_text(f"🧪 {result}", reply_markup=main_menu())

        elif data == "start_forwarding":
            result = await self.forwarding_manager.start_forwarding()
            await query.edit_message_text(f"🟢 {result}", reply_markup=main_menu())

        elif data == "stop_forwarding":
            result = await self.forwarding_manager.stop_forwarding()
            await query.edit_message_text(f"🔴 {result}", reply_markup=main_menu())

        elif data == "account_menu":
            await query.edit_message_text("Account Menu:", reply_markup=account_menu())

        elif data == "direct_login":
            await query.edit_message_text(
                "✨ Direct Login\n\nSend API_ID:",
                reply_markup=back_to_main()
            )
            context.user_data['login_step'] = 'api_id'

        elif data == "start_account":
            await query.edit_message_text(
                "💚 Start Account\n\nSend the phone number of the account to start (with country code):",
                reply_markup=back_to_main()
            )
            context.user_data['expecting'] = 'start_account'

        elif data == "stop_account":
            await query.edit_message_text(
                "🔴 Stop Account\n\nSend the phone number of the account to stop (with country code):",
                reply_markup=back_to_main()
            )
            context.user_data['expecting'] = 'stop_account'

        elif data == "manage_accounts":
            accounts_list = await self.account_manager_module.get_accounts_list()
            await query.edit_message_text(
                f"📗 Manage Accounts:\n\n{accounts_list}",
                reply_markup=manage_accounts_menu()
            )

        elif data == "remove_single":
            accounts = await self.account_manager_module.account_manager.get_all_accounts()
            if not accounts:
                await query.edit_message_text("No accounts to remove.", reply_markup=manage_accounts_menu())
                return

            keyboard = []
            for phone in accounts.keys():
                keyboard.append([InlineKeyboardButton(f"Remove {phone}", callback_data=f"remove_{phone}")])
            keyboard.append([InlineKeyboardButton("Back to Manage Accounts 🔙", callback_data="manage_accounts")])

            await query.edit_message_text(
                "Select account to remove:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        elif data.startswith("remove_"):
            phone = data[7:]  # Remove "remove_" prefix
            result = await self.account_manager_module.remove_single_account(phone)
            await query.edit_message_text(result, reply_markup=manage_accounts_menu())

        elif data == "remove_all":
            await query.edit_message_text(
                "⚠️ Are you sure you want to remove ALL accounts?",
                reply_markup=confirm_remove_all()
            )

        elif data == "confirm_remove_all":
            result = await self.account_manager_module.remove_all_accounts()
            await query.edit_message_text(result, reply_markup=manage_accounts_menu())

        elif data == "single_timer":
            await query.edit_message_text(
                "1️⃣ Single Account Timer\n\nSend timer in format: hours:minutes:seconds\nExample: 1:30:45",
                reply_markup=back_to_main()
            )
            context.user_data['expecting'] = 'single_timer'

        elif data == "all_timer":
            await query.edit_message_text(
                "⚡ All Accounts Timer\n\nSend timer in format: hours:minutes:seconds\nExample: 1:30:45",
                reply_markup=back_to_main()
            )
            context.user_data['expecting'] = 'all_timer'

        # Help handlers
        elif data == "forwarding_help":
            help_text = """
🩸 FORWARDING HELP

• Custom Messages: Set the message to forward
• Timer: Set delay between forwards
• Test Forward: Check current setup
• Start/Stop: Control forwarding process

Forwarding sends your message to all detected groups across all accounts with the set delay.
"""
            await query.edit_message_text(help_text, reply_markup=main_menu())

        elif data == "account_help":
            help_text = """
🧷 ACCOUNT HELP

• Direct Login: Login with API credentials
• Start/Stop Account: Control individual accounts
• Manage Accounts: Remove accounts

Login process:
1. Get API_ID and API_HASH from my.telegram.org
2. Enter phone number
3. Enter OTP code
4. Enter 2FA password if required
"""
            await query.edit_message_text(help_text, reply_markup=account_menu())

        elif data == "manage_help":
            help_text = """
🩺 MANAGE ACCOUNTS HELP

• Remove Single: Delete one account
• Remove All: Delete all accounts

⚠️ Removing accounts will delete session data and detected groups.
"""
            await query.edit_message_text(help_text, reply_markup=manage_accounts_menu())

        elif data == "timer_help":
            help_text = """
🍗 TIMER HELP

• Single Account: Set timer for one account
• All Accounts: Set timer for all accounts

Format: hours:minutes:seconds
Max: 24:59:59

Timer sets delay between message sends.
"""
            await query.edit_message_text(help_text, reply_markup=timer_menu())

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text

        # Check authorization first
        if not await self.check_authorization(user_id):
            await update.message.reply_text("❌ Access Denied! You are not authorized to use this bot.")
            return

        expecting = context.user_data.get('expecting')
        login_step = context.user_data.get('login_step')

        if expecting == 'custom_message':
            await self.state_manager.set_message(text)
            await update.message.reply_text(f"✅ Message set: {text[:50]}...", reply_markup=main_menu())
            context.user_data['expecting'] = None

        elif expecting == 'add_user':
            if not await self.check_owner(user_id):
                await update.message.reply_text("❌ Only owner can add users!", reply_markup=admin_panel())
                context.user_data['expecting'] = None
                return

            try:
                target_user_id = int(text.strip())
                if await self.user_manager.add_user(target_user_id, "user"):
                    await update.message.reply_text(f"✅ User {target_user_id} added successfully!", reply_markup=admin_panel())
                else:
                    await update.message.reply_text("❌ Failed to add user. User may already exist or invalid ID.", reply_markup=admin_panel())
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID. Please send a valid numeric user ID.", reply_markup=admin_panel())

            context.user_data['expecting'] = None

        elif expecting == 'start_account':
            phone = text.strip()
            result = await self.account_manager_module.set_account_active(phone, True)
            await update.message.reply_text(result, reply_markup=account_menu())
            context.user_data['expecting'] = None

        elif expecting == 'stop_account':
            phone = text.strip()
            result = await self.account_manager_module.set_account_active(phone, False)
            await update.message.reply_text(result, reply_markup=account_menu())
            context.user_data['expecting'] = None

        elif expecting in ['single_timer', 'all_timer']:
            result = await self.timer_manager.set_timer(text)
            await update.message.reply_text(result, reply_markup=main_menu())
            context.user_data['expecting'] = None

        elif login_step == 'api_id':
            context.user_data['api_id'] = text
            await update.message.reply_text("Send API_HASH:")
            context.user_data['login_step'] = 'api_hash'

        elif login_step == 'api_hash':
            context.user_data['api_hash'] = text
            await update.message.reply_text("Send PHONE NUMBER (with country code):")
            context.user_data['login_step'] = 'phone'

        elif login_step == 'phone':
            api_id = context.user_data.get('api_id')
            api_hash = context.user_data.get('api_hash')
            phone = text

            try:
                result = await self.login_manager.start_login(user_id, int(api_id), api_hash, phone)
                await update.message.reply_text(result)

                if "OTP sent" in result:
                    context.user_data['login_step'] = 'otp'
                else:
                    context.user_data['login_step'] = None

            except Exception as e:
                await update.message.reply_text(f"❌ Login failed: {e}")
                context.user_data['login_step'] = None

        elif login_step == 'otp':
            try:
                result = await self.login_manager.verify_otp(user_id, text)
                await update.message.reply_text(result)

                if "2FA required" in result:
                    context.user_data['login_step'] = '2fa'
                else:
                    context.user_data['login_step'] = None

            except Exception as e:
                await update.message.reply_text(f"❌ OTP verification failed: {e}")
                context.user_data['login_step'] = None

        elif login_step == '2fa':
            try:
                result = await self.login_manager.verify_2fa(user_id, text)
                await update.message.reply_text(result)
                context.user_data['login_step'] = None

            except Exception as e:
                await update.message.reply_text(f"❌ 2FA verification failed: {e}")
                context.user_data['login_step'] = None

        else:
            await update.message.reply_text("Please use the menu buttons or /start command.")

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.initialize())
        self.app.run_polling(close_loop=False)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()