from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍💼 Хлопець"), KeyboardButton(text="👩‍💼 Дівчина")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def looking_for_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👩 Шукаю дівчину"), KeyboardButton(text="👨 Шукаю хлопця")],
            [KeyboardButton(text="👥 Будь-кого")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Так", callback_data="confirm_yes"),
                InlineKeyboardButton(text="✏️ Редагувати", callback_data="confirm_edit"),
            ]
        ]
    )
