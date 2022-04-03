from aiogram import types
from aiogram.dispatcher import FSMContext

from core_buttons.inline_buttons import menuButtons


async def timeout(start_time: float, stop_time: float, message: types.Message, state: FSMContext):
    if (stop_time - start_time) >= 90:
        await state.finish()
        await message.answer(text="Таймаут очікування")
        await message.answer(text="Виберіть наступну дію: ", reply_markup=menuButtons)
        return True
    return False
