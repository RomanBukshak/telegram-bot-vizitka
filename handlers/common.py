import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.reply import main_menu

router = Router()
logger = logging.getLogger(__name__)

# Функция для показа главного меню
async def show_main_menu(message: Message):
    await message.answer(
        "Что тебя интересует? Выбери ниже:",
        reply_markup=main_menu
    )

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_name = message.from_user.first_name or "друг"
    await message.answer(
        f"👋 Привет #{user_name}! Я бот-визитка Романа Букшака — IT-специалиста с опытом "
        "в веб-разработке и создании Telegram-ботов. Помогаю бизнесу автоматизировать процессы "
        "и привлекать клиентов! 🚀\n\nЧто тебя интересует? Выбери ниже:",
        reply_markup=main_menu
    )

@router.message(lambda message: message.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    await show_main_menu(message)

@router.message()
async def handle_unknown(message: Message):
    logger.info(f"Получено сообщение: {message.text}")
    await message.answer(
        "Не знаю такой команды 😅 Используй кнопки меню или напиши /start",
        reply_markup=main_menu
    )