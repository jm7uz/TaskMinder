from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# 1-usul.
userApprove = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Confirmation", callback_data="register_confirm"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="register_cancel"),
    ],

])

messageApprove = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Confirmation", callback_data="message_confirm"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="message_cancel"),
    ],

])

messageApproveState = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes, of course", callback_data="approve_message_state"),
    ],

])