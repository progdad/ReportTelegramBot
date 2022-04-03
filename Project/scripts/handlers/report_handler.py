import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonOther, InputPeerChannel

# This Project Tools
from database.api_data import BotDB
from handlers.fsm_states.links_state import FSMlinks
from handlers.fsm_states.state_timeout import timeout
from handlers.setup_userbot import SetupUserBotSession
from core_buttons.inline_buttons import backStateButton, menuButtons
from logger_settings.logger_setup import set_logger
from logger_settings.error_answer import error_function


class ReportTool(SetupUserBotSession, BotDB):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        dp.register_callback_query_handler(self.report_button_handler, text="Report")
        dp.register_message_handler(self.handle_report_process, state=FSMlinks.links)
        self.report_runner_flag = False

    async def report_button_handler(self, call: types.CallbackQuery):
        logger = await set_logger(namespace="ReportTool.report_button_handler", uid=call.message.chat.id)
        try:
            session = await self.__session_exists(user_id=call.message.chat.id)
            self.api_data = await self.get_api_data(uid=call.message.chat.id)
            if not session or not self.api_data:
                await call.message.answer(text="Здається, ви ще не налаштували свого юзер бота.",
                                          reply_markup=menuButtons)
                logger.info("didn't set up the user bot session")
                return

            answer = "Чудово. Тепер надішліть посилання на телеграм канали окупантів. " \
                "Достатньо просто переслати мені повідомлення з каналу @stoprussiachannel, " \
                "а я вилучу всі необхідні посилання."
            await call.message.answer(text=answer, reply_markup=backStateButton)
            self.state_links_start = time.time()
            await FSMlinks.links.set()
        except Exception as exception:
            await error_function(call.message, logger, exception)

    async def __session_exists(self, user_id: int):
        try:
            user_session = self.user_sessions_path + f"{user_id}.session"
            with open(user_session, "r"):
                return True
        except FileNotFoundError:
            return False

    async def handle_report_process(self, message: types.Message, state: FSMContext):
        logger = await set_logger(namespace="ReportTool.handle_report_process", uid=message.chat.id)
        logger.info("starting the reports handler")
        try:
            state_links_stop = time.time()
            if await timeout(self.state_links_start, state_links_stop, message, state):
                return

            links = await self.__parse_links(message)
            if await self.__is_user_reporting(message.chat.id):
                await message.answer(text="Зараз кидаю скарги, не пишіть, будь ласка, нічого")
                logger.info("trying to send something while bot is reporting")
            elif links:
                self.report_runner_flag = message.chat.id

                await self.__report(links, message)

                self.report_runner_flag = False
                await state.finish()
                await message.answer(text="Скарги надіслані! Гарна робота.")
                await message.answer(text="Виберіть наступну дію: ", reply_markup=menuButtons)
            else:
                logger.info("were sent no links")
                await state.finish()
                await message.answer(text="Не знайдено жодного посилання :/")
                await message.answer(text="Виберіть наступну дію:", reply_markup=menuButtons)

        except Exception as exception:
            await state.finish()
            await error_function(message, logger, exception)

    async def __is_user_reporting(self, uid: int):
        if self.report_runner_flag == uid:
            return True

    @staticmethod
    async def __parse_links(message: types.Message):
        logger = await set_logger(namespace="ReportTool.__parse_links", uid=message.chat.id)
        try:
            links = [
                word.split("/")[-1] for word in message.text.split()
                if (("t.me" in word) or ("@" in word)) and ("stoprussiachaneel" not in word.lower())
            ]
            return links
        except Exception as exception:
            await error_function(message, logger, exception)

    async def __report(self, list_of_channels: list, message: types.Message):
        logger = await set_logger(namespace="ReportTool.__report", uid=message.chat.id)
        logger.info("starting report")
        try:
            api_id, api_hash = self.api_data[0]
            client = Client(
                session_name=f"{message.chat.id}",
                workdir=self.user_sessions_path,
                api_id=api_id,
                api_hash=api_hash
            )
            await client.start()
            await client.get_users(message.chat.id)

            logger.info("client instance has been started")

            for channel_un in list_of_channels:
                try:
                    channel_json_response = await client.resolve_peer(f"@{channel_un}")
                    channel_id = channel_json_response["channel_id"]
                    access_hash = channel_json_response["access_hash"]
                except Exception:
                    await message.answer(f"Немає такого каналу - @{channel_un}")
                    logger.info(f"no such channel - @{channel_un}")
                    continue

                channel = InputPeerChannel(channel_id=channel_id, access_hash=access_hash)
                report_text = "This is a propaganda channel of the Russian Federation, " \
                              "which is part of the information war against Ukraine. " \
                              "Pay attention to this and block this channel, which spreads fake information, " \
                              "demoralizes and deceives people, and helps to kill Ukrainians."
                report_peer = ReportPeer(
                    peer=channel,
                    reason=InputReportReasonOther(),
                    message=report_text
                )
                await client.send(report_peer)
                await message.answer(f"Скарга на канал @{channel_un} надіслана.")
                logger.info(f"report on @{channel_un} was sent")
            await client.stop()
        except Exception as exception:
            await error_function(message, logger, exception)
