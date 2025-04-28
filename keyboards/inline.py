from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def like_dislike_kb(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❤️ Лайк", callback_data=f"like_{user_id}"),
                InlineKeyboardButton(text="❌ Пропустити", callback_data="skip")
            ]
        ]
    )
