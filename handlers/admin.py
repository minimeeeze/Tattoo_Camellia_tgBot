from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
from sqlalchemy import insert, delete
from db.models import Slot
from db.session import get_async_session  # ← твоя новая функция

router = Router(name="admin")

ADMIN_IDS = [615491519, 1275949035]  # твой ID, ок


@router.message(Command("add_slot"), F.from_user.id.in_(ADMIN_IDS))
async def add_slot(message: Message):
    args = message.text.split()[1:]  # всё после /add_slot
    if len(args) != 2:
        await message.answer("Формат: /add_slot YYYY-MM-DD HH:MM")
        return

    try:
        dt_str = f"{args[0]} {args[1]}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")  # ← правильно: %H:%M
    except ValueError:
        await message.answer(
            "Неправильный формат даты/времени\nПример: 2026-02-25 16:00"
        )
        return

    # Новая сессия: получаем и сразу используем в with
    async with await get_async_session() as session:
        stmt = insert(Slot).values(datetime=dt)  # ← правильно: datetime=dt (не ==)
        await session.execute(stmt)
        await session.commit()

    await message.answer(f"Слот {dt_str} добавлен!")


@router.message(Command("remove_slot"), F.from_user.id.in_(ADMIN_IDS))
async def remove_slot(message: Message):
    args = message.text.split()[1:]  # ← было [:1] — это ломало аргументы
    if len(args) != 2:
        await message.answer("Формат: /remove_slot YYYY-MM-DD HH:MM")
        return

    try:
        dt_str = f"{args[0]} {args[1]}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer("Неправильный формат даты/времени")
        return

    async with await get_async_session() as session:
        stmt = delete(Slot).where(
            Slot.datetime == dt
        )  # ← правильно: Slot.datetime == dt
        result = await session.execute(stmt)
        await session.commit()

        if result.rowcount == 0:
            await message.answer(f"Слота {dt_str} не найдено")
        else:
            await message.answer(f"Слот {dt_str} удалён!")
