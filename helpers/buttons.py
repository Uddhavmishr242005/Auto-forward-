from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("Custom Messages 💬", callback_data="custom_messages"), InlineKeyboardButton("TIMER ⏳", callback_data="timer")],
        [InlineKeyboardButton("TEST FORWARD 🧪", callback_data="test_forward"), InlineKeyboardButton("Start FORWARDING 🟢", callback_data="start_forwarding")],
        [InlineKeyboardButton("Stop FORWARDING 🔴", callback_data="stop_forwarding"), InlineKeyboardButton("FORWARDING HELP 🩸", callback_data="forwarding_help")],
        [InlineKeyboardButton("Account Menu 📱", callback_data="account_menu"), InlineKeyboardButton("🔐 Admin Panel", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def account_menu():
    keyboard = [
        [InlineKeyboardButton("DIRECT LOGIN ✨", callback_data="direct_login"), InlineKeyboardButton("Start Account 💚", callback_data="start_account")],
        [InlineKeyboardButton("Stop Account 🔴", callback_data="stop_account"), InlineKeyboardButton("Manage Accounts 📗", callback_data="manage_accounts")],
        [InlineKeyboardButton("Account HELP 🧷", callback_data="account_help"), InlineKeyboardButton("Back to Main Menu 🔙", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def manage_accounts_menu():
    keyboard = [
        [InlineKeyboardButton("Remove Single 1️⃣", callback_data="remove_single"), InlineKeyboardButton("Remove All ⚡", callback_data="remove_all")],
        [InlineKeyboardButton("Manage ACC Help 🩺", callback_data="manage_help"), InlineKeyboardButton("Back to Account Menu 🔙", callback_data="account_menu")],
        [InlineKeyboardButton("Back to Main Menu 🔙", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def timer_menu():
    keyboard = [
        [InlineKeyboardButton("Single Timer 1️⃣", callback_data="single_timer"), InlineKeyboardButton("All Timer ⚡", callback_data="all_timer")],
        [InlineKeyboardButton("TIMER HELP 🍗", callback_data="timer_help"), InlineKeyboardButton("Back to Main Menu 🔙", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_panel():
    keyboard = [
        [InlineKeyboardButton("➕ Add User", callback_data="add_user"), InlineKeyboardButton("➖ Remove User", callback_data="remove_user")],
        [InlineKeyboardButton("📋 List Users", callback_data="list_users"), InlineKeyboardButton("Back to Main Menu 🔙", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main():
    keyboard = [[InlineKeyboardButton("Back to Main Menu 🔙", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)

def confirm_remove_all():
    keyboard = [
        [InlineKeyboardButton("Yes, Remove All ⚡", callback_data="confirm_remove_all")],
        [InlineKeyboardButton("Cancel ❌", callback_data="manage_accounts")]
    ]
    return InlineKeyboardMarkup(keyboard)
