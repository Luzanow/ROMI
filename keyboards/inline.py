from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def like_dislike_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❤️", callback_data=f"like_{user_id}"),
                InlineKeyboardButton(text="📩", callback_data=f"chat_{user_id}"),
                InlineKeyboardButton(text="👎", callback_data=f"dislike_{user_id}"),
                InlineKeyboardButton(text="😴", callback_data="skip"),
            ]
        ]
    )
