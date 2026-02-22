from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from sqlalchemy import insert, delete
from db.models import Slot
from db.session import get_async_session

router = Router(name="admin")

ADMIN_IDS = [615491519]


@router.message(Command("add_slot"), F.from_user.id.in_(ADMIN_IDS))
async def add_slot(message: Message):
    args = message.text.split()[1:]
    if len(args) != 2:
        await message.answer("Формат: /add_slot ГГГГ-ММ-ДД ЧЧ:ММ")
        return

    try:
        dt_str = f"{args[0]} {args[1]}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H-%M")
    except ValueError:
        await message.answer("Неправильный формат даты/времени")
        return

    async with get_async_session() as session:
        stmt = insert(Slot).values(datetime == dt)
        await session.execute(stmt)
        await session.commit()

    await message.answer(f"Слот {dt_str} добавлен!")


@router.message(Command("remove_slot"), F.from_user.id.in_(ADMIN_IDS))
async def remove_slot(message: Message):
    args = message.text.split()[:1]
    if len(args) != 2:
        await message.answer("Формат: /remove_slot ГГГГ-ММ-ДД ЧЧ:ММ")
        return

    try:
        dt_str = f"{args[0]} {args[1]}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H-%M")
    except ValueError:
        await message.answer("Такого слота нет!")
        return

    async with get_async_session() as session:
        stmt = delete(Slot).where(datetime == dt)
        await session.execute(stmt)
        await session.commit()

    await message.answer(f"Слот {dt_str} удалён!")
