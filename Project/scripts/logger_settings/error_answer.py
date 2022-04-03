from core_buttons.inline_buttons import menuButtons


async def error_function(message, logger, exception):
    await message.answer(text=f"Сталася помилка.",
                         reply_markup=menuButtons)
    logger.error(exception)
