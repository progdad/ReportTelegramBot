from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


reportButton = InlineKeyboardButton(text="⛔️Скаржитись ⛔", callback_data="Report")
changeUserbotData = InlineKeyboardButton(text="⚙️ Налаштування ⚙", callback_data="Session Settings")

backInlineStateButton = InlineKeyboardButton(text="⬅️Назад ⬅", callback_data="Back State")

menuButtons = InlineKeyboardMarkup(row_width=4).add(reportButton).add(changeUserbotData)
backStateButton = InlineKeyboardMarkup(row_width=4).add(backInlineStateButton)
