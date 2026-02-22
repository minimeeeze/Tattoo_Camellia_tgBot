from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записаться сейчас")],
            [KeyboardButton(text="Примеры работ")],
            [KeyboardButton(text="Прайс-лист")],
            [KeyboardButton(text="Свободные даты")],
            [KeyboardButton(text="У меня другой вопрос")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выбери действие",
    )
    return kb
