import os
import re
import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired, BadRequest

# This Project Tools
from core_buttons.inline_buttons import backInlineStateButton, backStateButton, menuButtons
from database.api_data import BotDB
from handlers.fsm_states.userbot_data_state import FSMuserbot
from logger_settings.error_answer import error_function
from logger_settings.logger_setup import set_logger


startSettingUserBotUp = InlineKeyboardButton(text="▶️Почати Налаштування ▶", callback_data="Start")

startOrBack = InlineKeyboardMarkup(row_width=4).add(startSettingUserBotUp).add(backInlineStateButton)


class SetupUserBotSession(BotDB):
    def __init__(self, dp: Dispatcher):
        super().__init__()
        dp.register_callback_query_handler(self.userbot_using_data_agreement, text="Session Settings")
        dp.register_callback_query_handler(self.start_setting_up, text="Start", state=FSMuserbot.start_or_back)
        dp.register_message_handler(self.__api_id, state=FSMuserbot.api_id)
        dp.register_message_handler(self.__api_hash, state=FSMuserbot.api_hash)
        dp.register_message_handler(self.__phone_number, state=FSMuserbot.phone_number)
        dp.register_message_handler(self.__auth_code, state=FSMuserbot.auth_code)
        dp.register_message_handler(self.__password, state=FSMuserbot.password)

        self.userbot_client_data = {}
        self.state_wait_starts = {}

        scripts_starts = os.getcwd().find("scripts")
        self.user_sessions_path = os.getcwd()[:scripts_starts] + "user_sessions/"

    @staticmethod
    async def userbot_using_data_agreement(call: types.CallbackQuery):
        logger = await set_logger(namespace="SetupUserBotSession.userbot_using_data_agreement",
                                  uid=call.message.chat.id)
        logger.info("user is on agreement stage")
        try:
            answer = "Уважно прочитайте інструкцію https://telegra.ph/%D0%86nstrukc%D1%96ya-koristuvannya-botom-blockru-bot-04-02 " \
                     "та починайте налаштування."
            await call.message.answer(text=answer, reply_markup=startOrBack)
            await FSMuserbot.start_or_back.set()
        except Exception as exception:
            await error_function(call.message, logger, exception)

    async def start_setting_up(self, call: types.CallbackQuery, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.start_setting_up", uid=call.message.chat.id)
        logger.info("user has started setting up userbot")
        try:
            await state.finish()
            await call.message.answer(text="Починаю налаштування. Будьте уважні !")
            await call.message.answer(text="Введіть api_id: ", reply_markup=backStateButton)

            self.state_wait_starts["api_id"] = time.time()
            await FSMuserbot.api_id.set()
        except Exception as exception:
            await error_function(call.message, logger, exception)

    async def __api_id(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.__api_id", uid=message.chat.id)
        logger.info(f"sent api_id - {message.text}")
        try:
            api_id_wait_start = self.state_wait_starts["api_id"]
            api_id_wait_stop = time.time()
            if await self.__timeout(api_id_wait_start, api_id_wait_stop, message, state):
                return

            self.userbot_client_data["api_id"] = message.text
            await state.finish()
            await message.answer(text="Введіть api_hash: ", reply_markup=backStateButton)

            self.state_wait_starts["api_hash"] = time.time()
            await FSMuserbot.api_hash.set()
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __api_hash(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.__api_hash", uid=message.chat.id)
        logger.info(f"sent api_hash - {message.text}")
        try:
            api_hash_wait_start = self.state_wait_starts["api_hash"]
            api_hash_wait_stop = time.time()
            if await self.__timeout(api_hash_wait_start, api_hash_wait_stop, message, state):
                return

            self.userbot_client_data["api_hash"] = message.text
            await state.finish()
            await message.answer(text="Введіть номер телефону: ",
                                 reply_markup=backStateButton)

            self.state_wait_starts["phone_number"] = time.time()
            await FSMuserbot.phone_number.set()
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __phone_number(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.__phone_number", uid=message.chat.id)
        logger.info(f"sent phone_number")
        try:
            phone_number_wait_start = self.state_wait_starts["phone_number"]
            phone_number_wait_stop = time.time()
            if await self.__timeout(phone_number_wait_start, phone_number_wait_stop, message, state):
                return

            self.userbot_client_data["phone_number"] = message.text

            await state.finish()
            await self.__create_client_session(user_id=message.chat.id, message=message)
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __create_client_session(self, user_id, message: types.Message):
        logger = await set_logger(namespace="SetupUserBotSession.__create_client_session", uid=user_id)
        logger.info("creating user bot session")
        try:
            self.api_id = self.userbot_client_data["api_id"].strip()
            self.api_hash = self.userbot_client_data["api_hash"].strip()

            self.client = Client(
                session_name=f"{user_id}",
                workdir=self.user_sessions_path,
                api_id=self.api_id,
                api_hash=self.api_hash,
            )
            await self.client.connect()

            await message.answer(text="Зараз вам буде надіслано аутентифікаційний код. Введіть його: ",
                                 reply_markup=backStateButton)

            self.phone_number = self.userbot_client_data["phone_number"]
            self.auth_code_response = await self.client.send_code(self.phone_number)

            logger.info("confirmation code was sent successfully")

            self.state_wait_starts["auth_code"] = time.time()
            await FSMuserbot.auth_code.set()
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __auth_code(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.__auth_code", uid=message.chat.id)
        try:
            auth_code_wait_start = self.state_wait_starts["auth_code"]
            auth_code_wait_stop = time.time()
            if await self.__timeout(auth_code_wait_start, auth_code_wait_stop, message, state):
                return

            await state.finish()
            pure_auth_code = re.sub("[^0-9]", "", message.text)
            await self.__log_in_user_bot(auth_code=pure_auth_code, message=message)
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __log_in_user_bot(self, auth_code: str, message: types.Message):
        logger = await set_logger(namespace="SetupUserBotSession.__log_in_user_bot", uid=message.chat.id)
        try:
            phone_code_hash = self.auth_code_response["phone_code_hash"]
            await self.client.sign_in(self.phone_number, phone_code_hash, auth_code)
            logger.info("client session has been created successfully")
            await self.client.disconnect()

            await self.save_api_data(uid=message.chat.id, api_id=self.api_id, api_hash=self.api_hash)

            await message.answer("Налаштування повністю завершено. Юзербот готовий до використання.")
            await message.answer(text="Можемо починати кидати скарги !", reply_markup=menuButtons)
            logger.info("USER BOT SESSION SEEMS TO BE DONE")

        except SessionPasswordNeeded:
            logger.info("two-step verification is required")
            await message.answer(text="Вкажіть хмарний пароль: ",
                                 reply_markup=backStateButton)
            self.state_wait_starts["password"] = time.time()
            await FSMuserbot.password.set()
        except PhoneCodeInvalid:
            logger.info("authentication code is invalid")
            await message.answer(text="Невірний код авторизації телеграм.")
            await message.answer(text="Виберіть наступну дію: ",
                                 reply_markup=menuButtons)
        except PhoneCodeExpired:
            logger.info("authentication code has expired")
            await message.answer(text="Код авторизації телеграм не валідний.")
            await message.answer(text="Виберіть наступну дію: ",
                                 reply_markup=menuButtons)

    async def __password(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="SetupUserBotSession.__password", uid=message.chat.id)
        try:
            password_wait_start = self.state_wait_starts["password"]
            password_wait_stop = time.time()
            if await self.__timeout(password_wait_start, password_wait_stop, message, state):
                return

            try:
                password = message.text
                await self.client.check_password(password)
                await self.client.disconnect()

                await self.save_api_data(uid=message.chat.id, api_id=self.api_id, api_hash=self.api_hash)

                await message.answer("Налаштування повністю завершено. Юзербот готовий до використання.")
                await message.answer(text="Можемо починати кидати скарги !", reply_markup=menuButtons)
                logger.info("USER BOT SESSION SEEMS TO BE DONE")
            except BadRequest:
                logger.info("Invalid password")
                await message.answer("Невірний пароль. Налаштування скинуто.")
                await message.answer(text="Виберіть наступну дію: ", reply_markup=menuButtons)
                logger.info("setting session up was stopped")
            finally:
                await state.finish()
        except Exception as exception:
            await error_function(message, logger, exception)

    @staticmethod
    async def __timeout(start_time: float, stop_time: float, message: types.Message, state: FSMContext):
        if (stop_time - start_time) >= 90:
            await state.finish()
            await message.answer(text="Таймаут очікування")
            await message.answer(text="Виберіть наступну дію: ", reply_markup=menuButtons)
            return True
        return False
