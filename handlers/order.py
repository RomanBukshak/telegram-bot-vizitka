import logging
import re
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.reply import contact_method_keyboard, telegram_confirm_keyboard, confirm_keyboard, main_menu
from states.order_form import OrderForm

router = Router()
logger = logging.getLogger(__name__)

@router.message(lambda message: message.text == "Оставить заявку")
async def start_order(message: Message, state: FSMContext):
    logger.info(f"Получено сообщение: {message.text}")
    await message.answer("Как вас зовут?")
    await state.set_state(OrderForm.name)

@router.message(OrderForm.name)
async def process_name(message: Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(
            "Что тебя интересует? Выбери ниже:",
            reply_markup=main_menu
        )
        await state.clear()
        return
    await state.update_data(name=message.text)
    await message.answer(
        "📝 Укажите предпочитаемый способ связи с вами\n(Звонок только для РФ номеров):",
        reply_markup=contact_method_keyboard
    )
    await state.set_state(OrderForm.contact_method)

@router.message(OrderForm.contact_method)
async def process_contact_method(message: Message, state: FSMContext):
    contact_method = message.text
    if contact_method == "Назад":
        await message.answer(
            "Что тебя интересует? Выбери ниже:",
            reply_markup=main_menu
        )
        await state.clear()
        return
    if contact_method not in ["Звонок", "Телеграмм", "ВК", "WhatsApp", "Другое"]:
        await message.answer(
            "Пожалуйста, выберите способ связи из предложенных.",
            reply_markup=contact_method_keyboard
        )
        return
    await state.update_data(contact_method=contact_method)
    
    if contact_method == "Телеграмм":
        current_telegram = f"@{message.from_user.username}" if message.from_user.username else "не указан"
        await message.answer(
            f"📝 Тг для связи текущий: {current_telegram} или другой?",
            reply_markup=telegram_confirm_keyboard
        )
        await state.set_state(OrderForm.telegram_confirm)
    else:
        prompt = {
            "Звонок": "📝 Укажите ваш номер телефона (РФ) для связи:",
            "ВК": "📝 Укажите вашу страницу ВК или ID:",
            "WhatsApp": "📝 Укажите ваш номер WhatsApp для связи:",
            "Другое": "📝 Укажите предпочитаемый способ связи:"
        }[contact_method]
        await message.answer(
            prompt,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Назад")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        await state.set_state(OrderForm.contact_details)

@router.message(OrderForm.telegram_confirm)
async def process_telegram_confirm(message: Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(
            "Что тебя интересует? Выбери ниже:",
            reply_markup=main_menu
        )
        await state.clear()
        return
    if message.text not in ["Да", "Нет"]:
        await message.answer(
            "Пожалуйста, выберите 'Да' или 'Нет'.",
            reply_markup=telegram_confirm_keyboard
        )
        return
    if message.text == "Да":
        telegram = f"@{message.from_user.username}" if message.from_user.username else "не указан"
        await state.update_data(contact_details=telegram)
        await message.answer(
            "📝 Укажите вкратце, чем я могу вам помочь и для какого вида бизнеса:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Назад")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        await state.set_state(OrderForm.help_needed)
    else:
        await message.answer(
            "📝 Укажите ваш Telegram для связи:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Назад")]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        await state.set_state(OrderForm.contact_details)

@router.message(OrderForm.contact_details)
async def process_contact_details(message: Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(
            "Что тебя интересует? Выбери ниже:",
            reply_markup=main_menu
        )
        await state.clear()
        return
    data = await state.get_data()
    contact_method = data["contact_method"]
    details = message.text

    # Валидация номера телефона для Звонок и WhatsApp
    if contact_method in ["Звонок", "WhatsApp"]:
        phone_pattern = r"^(?:\+7|7|8)\d{10}$"  # Формат: +71234567890, 71234567890, 81234567890
        if not re.match(phone_pattern, details):
            error_message = "Пожалуйста, укажите корректный номер телефона РФ😔\n" if contact_method == "Звонок" else "Пожалуйста, укажите корректный номер WhatsApp😔\n"
            await message.answer(
                error_message + "В формате +71234567890, либо 71234567890, либо 81234567890",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="Назад")]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            )
            return

    await state.update_data(contact_details=details)
    await message.answer(
        "📝 Укажите вкратце, чем я могу вам помочь и для какого вида бизнеса:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    await state.set_state(OrderForm.help_needed)

@router.message(OrderForm.help_needed)
async def process_help_needed(message: Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(
            "Что тебя интересует? Выбери ниже:",
            reply_markup=main_menu
        )
        await state.clear()
        return
    await state.update_data(help_needed=message.text)
    data = await state.get_data()
    await message.answer(
        "Давайте сверим данные:\n"
        f"Имя: {data['name']}\n"
        f"Способ связи: {data['contact_method']}\n"
        f"Данные для связи: {data['contact_details']}\n"
        f"Описание: {data['help_needed']}\n"
        "Все верно? 😌",
        reply_markup=confirm_keyboard
    )
    await state.set_state(OrderForm.confirm)

@router.message(OrderForm.confirm)
async def process_confirm(message: Message, state: FSMContext, bot):
    if message.text == "Ввести данные заново":
        await message.answer("Как вас зовут?")
        await state.set_state(OrderForm.name)
        return
    if message.text != "Да":
        await message.answer(
            "Пожалуйста, выберите 'Да' или 'Ввести данные заново'.",
            reply_markup=confirm_keyboard
        )
        return
    
    # Отправка заявки в Telegram
    data = await state.get_data()
    try:
        await bot.send_message(
            chat_id=496446561,
            text=(
                "Новая заявка:\n"
                f"Имя: {data['name']}\n"
                f"Способ связи: {data['contact_method']}\n"
                f"Данные для связи: {data['contact_details']}\n"
                f"Описание: {data['help_needed']}"
            )
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке заявки: {e}")
    
    await message.answer(
        "✅ Спасибо! Я свяжусь с вами скоро👊",
        reply_markup=main_menu
    )
    await state.clear()