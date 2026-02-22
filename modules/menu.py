from aiogram import Router
from aiogram import F
from aiogram.types import Message

router = Router(name="menu_handlers")


@router.message(F.text == "Записаться сейчас")
async def proc_sing_up(message: Message):
    await message.answer(
        f"Отлично! Давай запишемся. \n"
        "Напиши желаемую дату или выбери из свободных.\n"
        "Менеджер свяжется с тобой для уточнения"
    )

@router.message(F.text == "Примеры работ")
async def get_portfolio(message: Message):
    await message.answer(f"Вот мои последние работы 👇\n"
                         "Все мои работы можешь посмотреть в галерее канала\n"
                         "@TATTOO_CAMELLIA")



@router.message(F.text == "Прайс-лист")
async def get_pricelist(message: Message):
    await message.answer_photo(photo=)



@router.message(F.text == "Свободные даты")



@router.message(F.text == "У меня другой вопрос")