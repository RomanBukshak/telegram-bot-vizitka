from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обо мне"), KeyboardButton(text="О боте")],
        [KeyboardButton(text="Идеи воронок и ботов"), KeyboardButton(text="Мои услуги")],
        [KeyboardButton(text="Связаться со мной")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Меню для разделов (Связаться, Назад)
section_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Связаться")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Меню для разделов с дополнительной кнопкой (Связаться, Назад, Идеи воронок и ботов)
section_menu_with_funnels = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Связаться")],
        [KeyboardButton(text="Идеи воронок и ботов")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Меню для "Связаться со мной"
contact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оставить заявку")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Клавиатура для выбора способа связи
contact_method_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Звонок"), KeyboardButton(text="Телеграмм")],
        [KeyboardButton(text="ВК"), KeyboardButton(text="WhatsApp")],
        [KeyboardButton(text="Другое"), KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура для подтверждения Telegram
telegram_confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")],
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура для подтверждения данных
confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Ввести данные заново")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)