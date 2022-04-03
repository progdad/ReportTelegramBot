from __future__ import annotations

from aiogram import executor, types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# This Project Tools
from __init__ import API_BOT_TOKEN

from logger_settings.logger_setup import set_logger
from logger_settings.error_answer import error_function

from core_buttons.keyboard_button import menuButton
from core_buttons.inline_buttons import menuButtons

from handlers.report_handler import ReportTool


bot = Bot(token=API_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


class MyBot(ReportTool):
    def __init__(self):
        super().__init__(dp)
        dp.register_message_handler(self.start_handler, commands=["start"])
        dp.register_message_handler(self.main_menu, text="🔵 Головне Меню 🟡")
        dp.register_callback_query_handler(self.back_state_button, state="*", text="Back State")
        dp.register_callback_query_handler(self.source_code, text="Source Code")

    @staticmethod
    async def start_handler(message: types.Message):
        logger = await set_logger(namespace="MyBot.start_handler", uid=message.chat.id)
        logger.info("sent /start command")
        try:
            answer = "Мої вітання !\n" \
                "Для того щоб почати користуватися ботом, натисніть на кнопку \"Головне меню\". " \
                "В самому меню натисніть кнопку \"Налаштування\"."
            await message.answer(text=answer, reply_markup=menuButton)
        except Exception as exception:
            await error_function(message, logger, exception)

    @staticmethod
    async def main_menu(message: types.Message):
        logger = await set_logger(namespace="MyBot.main_menu", uid=message.chat.id)
        logger.info("pressed \"Menu\" button")
        try:
            await message.answer(text="Виберіть наступну дію: ", reply_markup=menuButtons)
        except Exception as exception:
            await error_function(message, logger, exception)

    @staticmethod
    async def back_state_button(call: types.CallbackQuery, state: FSMContext):
        logger = await set_logger(namespace="MyBot.back_state_button", uid=call.message.chat.id)
        try:
            current_state = await state.get_state()
            if current_state is None:
                logger.info("this back_state_button is not active")
                await call.message.answer(text="Кнопка не дійсна...")
                return
            logger.info("clicked on back_state_button; return back")
            await state.finish()
            await call.message.answer(text="Повернувся назад")
            await call.message.answer(
                text="Виберіть наступну дію:",
                reply_markup=menuButtons
            )
        except Exception as exception:
            await error_function(call.message, logger, exception)

    @staticmethod
    async def source_code(call: types.CallbackQuery):
        logger = await set_logger(namespace="MyBot.source_code", uid=call.message.chat.id)
        logger.info("pressed \"Source Code\" button")
        try:
            await call.message.answer(text="Вихідний код проекту >>> \nhttps://github.com/progdad/")
            await call.message.answer(
                text="Виберіть наступну дію:",
                reply_markup=menuButtons
            )
        except Exception as exception:
            await error_function(call.message, logger, exception)


if __name__ == '__main__':
    reportBot = MyBot()
    executor.start_polling(dp, skip_updates=True)
