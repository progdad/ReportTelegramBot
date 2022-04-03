from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


mainMenuButton = KeyboardButton(text="🔵 Головне Меню 🟡")
menuButton = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(mainMenuButton)
