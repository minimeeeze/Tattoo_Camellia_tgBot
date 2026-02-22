# main.py
# Точка входа бота — здесь создаём Bot, Dispatcher, подключаем роутеры и запускаем

import asyncio
import logging
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


# Импортируем все роутеры
from handlers.command_start import router as start_router
from handlers.menu import router as menu_router
from handlers.admin import router as admin_router

# Если добавишь admin.py, payments.py и т.д. — добавь сюда же:
# from handlers.admin import router as admin_router

# Загружаем .env

# Явно указываем относительный путь от места запуска main.py
load_dotenv("secret.env")

# Настраиваем логи (чтобы видеть ошибки и что происходит)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def main() -> None:
    # Берём токен из .env
    token = getenv("BOT_TOKEN")
    if not token:
        logging.error("BOT_TOKEN не найден в .env!")
        return

    # Создаём бота с HTML-разметкой по умолчанию
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Создаём диспетчер и подключаем роутеры
    dp = Dispatcher()

    # Порядок важен: /start обычно первый, потом меню, потом всё остальное
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(admin_router)
    # dp.include_router(admin_router)  # если добавишь

    # Запускаем polling (для теста и разработки)
    # Можно потом переключить на webhook
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
