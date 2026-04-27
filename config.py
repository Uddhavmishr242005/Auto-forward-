import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
API_ID = os.getenv('API_ID', 'YOUR_API_ID_HERE')
API_HASH = os.getenv('API_HASH', 'YOUR_API_HASH_HERE')

# Owner Configuration
OWNER_ID = int(os.getenv('OWNER_ID', '0'))  # Set your Telegram user ID here

# MongoDB Configuration
MONGODB_URL = os.getenv('MONGODB_URL', os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
DATABASE_NAME = os.getenv('DATABASE_NAME', 'telegram_bot')

# Collections
USERS_COLLECTION = 'users'
ACCOUNTS_COLLECTION = 'accounts'
GROUPS_COLLECTION = 'groups'
SETTINGS_COLLECTION = 'settings'

# Database paths
SESSIONS_DIR = 'sessions'
ACCOUNTS_DB = 'database/accounts.json'
STATE_DB = 'database/state.json'

# Limits
MAX_GROUPS_PER_ACCOUNT = 500
FLOOD_WAIT_BASE = 30
MESSAGE_DELAY = 1

# Timer limits
MAX_HOURS = 24
MAX_MINUTES = 59
MAX_SECONDS = 59