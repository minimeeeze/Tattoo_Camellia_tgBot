from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_menu import get_main_menu_kb

router = Router(name="command_start")


@router.message(CommandStart())
async def cmd_start_handler(message: Message):
    user = message.from_user
    name = user.first_name if user.first_name else "Друг"
    await message.answer(
        f"Привет, {name}! Здесь ты можешь: "
        "записаться на сеанс, посмотреть портфолио, узнать цены и свободные даты \n\n"
        "Что хочешь сделать прямо сейчас?",
        reply_markup=get_main_menu_kb(),
    )
