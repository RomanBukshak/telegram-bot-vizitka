import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

# Импортируем обработчики
from handlers import common, sections, order

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


dp.include_router(sections.router)  
dp.include_router(order.router)     
dp.include_router(common.router)    

async def main():
    try:
        logger.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        await asyncio.sleep(5)
        await main()

if __name__ == "__main__":
    asyncio.run(main())