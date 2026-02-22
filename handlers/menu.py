from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from os import getenv
from dotenv import load_dotenv

from db.session import get_async_session
from db.models import Slot
from sqlalchemy import select
from datetime import datetime as dt_now

load_dotenv()
PRICEIMAGE = getenv("PRICELIST")

router = Router(name="menu_handlers")


@router.message(F.text == "Записаться сейчас")
async def process_sign_up(message: Message):
    await message.answer(
        "Отлично! Давай запишемся.\n"
        "Напиши желаемую дату или выбери из свободных.\n"
        "Менеджер свяжется с тобой для уточнения"
    )


@router.message(F.text == "Примеры работ")
async def get_portfolio(message: Message):
    await message.answer(
        "Вот мои последние работы 👇\n"
        "Все работы можно посмотреть в галерее канала\n"
        "@TATTOO_CAMELLIA"
    )


@router.message(F.text == "Прайс-лист")
async def get_pricelist(message: Message):
    if not PRICEIMAGE:
        await message.answer("Прайс-лист пока недоступен 😅")
        return

    await message.answer_photo(
        photo=PRICEIMAGE, caption="Вот актуальный прайс-лист 📊", parse_mode="HTML"
    )


@router.message(F.text == "Свободные даты")
async def get_free_slots(message: Message):
    async with await get_async_session() as session:
        stmt = (
            select(Slot)
            .where(Slot.status == "free", Slot.datetime > dt_now.utcnow())
            .order_by(Slot.datetime)
        )
        result = await session.execute(stmt)
        free_slots = result.scalars().all()

    if not free_slots:
        await message.answer("Нет свободных дат :(")
        return

    builder = InlineKeyboardBuilder()

    for slot in free_slots:
        text = slot.datetime.strftime("%d %B %H:%M")
        data = f"book_{slot.id}"
        builder.button(text=text, callback_data=data)

    builder.adjust(3)  # по 3 в ряд — выглядит дорого-богато

    kb = builder.as_markup()

    await message.answer("Выбери дату:", reply_markup=kb)


@router.callback_query(F.data.startswith("book_"))
async def process_book_date(callback: CallbackQuery):
    slot_id = int(callback.data.split("_")[1])

    # Здесь пока просто подтверждение
    # Позже добавим проверку статуса + бронь в БД

    await callback.message.edit_text(
        f"Вы выбрали слот с ID {slot_id}.\n"
        "Дата забронирована! Ждите подтверждения мастера."
    )
    await callback.answer("Запись прошла успешно!", show_alert=True)


# @router.message(F.text == "У меня другой вопрос")
