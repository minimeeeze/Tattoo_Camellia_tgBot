from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
async def proc_sign_up(message: Message):

    await message.answer(
        f"Отлично! Давай запишемся. \n"
        "Напиши желаемую дату или выбери из свободных.\n"
        "Менеджер свяжется с тобой для уточнения"
    )


@router.message(F.text == "Примеры работ")
async def get_portfolio(message: Message):

    await message.answer(
        f"Вот мои последние работы 👇\n"
        "Все мои работы можешь посмотреть в галерее канала\n"
        "@TATTOO_CAMELLIA"
    )


@router.message(F.text == "Прайс-лист")
async def get_pricelist(message: Message):

    if not PRICEIMAGE:
        await message.answer("Прайс-лист пока недоступен 😅")
        return

    await message.answer_photo(
        photo=PRICEIMAGE, caption="Вот актуальный прайс-лист", parse_mode="HTML"
    )


@router.message(F.text == "Свободные даты")
async def get_free_slots(message: Message):

    async with get_async_session() as session:
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

    else:
        builder = InlineKeyboardBuilder()

        for slot in free_slots:
            text = slot.datetime.strftime("%d %B %H:%M")
            data = f"book_{slot.id}"
            builder.button(text=text, callback_data=data)

        builder.adjust(3)

        kb = builder.as_markup(resize_keyboard=False)

        await message.answer("Выбери дату:", reply_markup=kb)


@router.callback_query(F.data.startswith("book_"))
async def proc_book_date(callback: CallbackQuery):
    slot_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("Дата забронирована! Ждите подтверждения.")
    await callback.answer("Запись прошла успешно!", show_alert=True)


# @router.message(F.text == "У меня другой вопрос")
