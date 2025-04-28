from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Пошук"), KeyboardButton(text="📄 Моя анкета")],
            [KeyboardButton(text="✏️ Редагувати анкету")]
        ],
        resize_keyboard=True
    )
