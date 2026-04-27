# Telegram Auto Forward Bot

🚀 A comprehensive Telegram bot for automated message forwarding to groups across multiple accounts with MongoDB storage and user authorization.

## Features

- ✅ **Authorized User System**: Owner and user roles with access control
- ✅ **MongoDB Storage**: Persistent data storage with restart-safe operation
- ✅ **Session Login System**: OTP/2FA support with session management
- ✅ **Custom Message Management**: Set and store custom messages
- ✅ **Auto Group Detection**: Automatically detect and store groups
- ✅ **Start/Stop Forwarding**: Real-time control with threading
- ✅ **Timer System**: Configurable delays (hours:minutes:seconds)
- ✅ **Admin Panel**: User management for owners
- ✅ **Exception Handling**: FloodWait protection and retry logic
- ✅ **Rate Limiting**: Respects Telegram's limits

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. MongoDB Setup
**Option A: Local MongoDB**
```bash
# Install MongoDB locally
sudo apt-get install mongodb  # Ubuntu/Debian
# or
brew install mongodb          # macOS

# Start MongoDB
sudo systemctl start mongodb  # Linux
brew services start mongodb   # macOS
```

**Option B: MongoDB Atlas (Cloud)**
1. Create account at https://www.mongodb.com/atlas
2. Create a cluster
3. Get connection string

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here
OWNER_ID=your_telegram_user_id_here
MONGODB_URL=mongodb://localhost:27017
# Optional alias supported for compatibility
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=telegram_bot
```

### 4. Get Credentials

**Bot Token:**
- Message @BotFather on Telegram
- Create a new bot and get the token

**API Credentials:**
- Visit https://my.telegram.org/
- Login and create an app
- Get API_ID and API_HASH

**Owner ID:**
- Message @userinfobot on Telegram
- Get your numeric user ID

### 5. Run the Bot
```bash
python bot.py
```

## Database Structure

### Collections:
- **users**: User authorization data
- **accounts**: Telegram account sessions
- **groups**: Detected groups per account
- **settings**: Global bot settings

## User Roles

- **OWNER**: Full access, can manage users
- **USER**: Limited access, can use bot features

## Usage

### For Owners:
1. Start bot with `/start`
2. Access Admin Panel to manage users
3. Add authorized users by their Telegram ID

### For Users:
1. Get added by owner
2. Start bot with `/start`
3. Use all bot features

### Bot Features:
- **Custom Messages**: Set messages to forward
- **Timer Settings**: Configure delays
- **Account Management**: Login/logout accounts
- **Forwarding Control**: Start/stop automated forwarding

## Security Features

- ✅ Owner-only user management
- ✅ Access control on all operations
- ✅ No duplicate user registration
- ✅ Secure session storage
- ✅ Rate limit compliance

## Project Structure

```
├── bot.py                 # Main bot application
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── README.md            # Documentation
├── modules/
│   ├── login.py         # Login management
│   ├── forwarding.py    # Forwarding logic
│   ├── timer.py         # Timer management
│   ├── account.py       # Account management
│   └── user_manager.py  # User authorization
├── services/
│   ├── sender.py        # Message sending
│   └── detector.py      # Group detection
├── database/
│   ├── mongodb.py       # MongoDB connection
│   ├── accounts.py      # Account storage
│   └── state.py         # State management
└── helpers/
    └── buttons.py       # UI components
```

## Troubleshooting

**MongoDB Connection Issues:**
- Ensure MongoDB is running
- Check connection string in .env
- Verify network access for cloud MongoDB

**Bot Not Responding:**
- Check BOT_TOKEN in .env
- Verify bot is added to groups (if needed)
- Check console for error messages

**Authorization Issues:**
- Verify OWNER_ID is correct
- Check if user is added to authorized list
- Ensure MongoDB has user data

## Safety Notes

- Respect Telegram's Terms of Service
- Use reasonable delays to avoid rate limits
- Only forward to groups you have permission to message
- Keep API credentials secure
- Regular backup of MongoDB data

## License

This project is for educational purposes only.</content>
<parameter name="filePath">/workspaces/Auto-forward-/README.md# Telegram Auto Forward Bot

🚀 A comprehensive Telegram bot for automated message forwarding to groups across multiple accounts.

## Features

- ✅ Session login system with OTP/2FA support
- ✅ Custom message management
- ✅ Auto group detection from accounts
- ✅ Start/Stop forwarding controls
- ✅ Timer system (seconds/minutes/hours)
- ✅ Multi-account support
- ✅ Inline keyboard UI exactly as specified
- ✅ Exception handling and flood protection
- ✅ State management

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export API_ID="your_api_id_here"
   export API_HASH="your_api_hash_here"
   ```

3. **Get your bot token:**
   - Message @BotFather on Telegram
   - Create a new bot and get the token

4. **Get API credentials:**
   - Go to https://my.telegram.org/
   - Login and create an app
   - Get API_ID and API_HASH

5. **Run the bot:**
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot with `/start`
2. Use the inline keyboard menus to navigate
3. Login to Telegram accounts via Direct Login
4. Set custom messages
5. Configure timer settings
6. Start forwarding

## Project Structure

```
├── bot.py                 # Main bot application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── modules/
│   ├── login.py         # Login management
│   ├── forwarding.py    # Forwarding logic
│   ├── timer.py         # Timer management
│   └── account.py       # Account management
├── services/
│   ├── sender.py        # Message sending service
│   └── detector.py      # Group detection service
├── database/
│   ├── accounts.py      # Account storage
│   └── state.py         # State management
└── helpers/
    └── buttons.py       # UI button definitions
```

## Safety Notes

- Respect Telegram's Terms of Service
- Use reasonable delays to avoid rate limits
- Only forward to groups you have permission to message
- Keep your API credentials secure

## License

This project is for educational purposes only.