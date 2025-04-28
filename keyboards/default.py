from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def gender_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Чоловік"), KeyboardButton(text="Жінка")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def looking_for_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Чоловіка"), KeyboardButton(text="Жінку")],
            [KeyboardButton(text="Неважливо")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
