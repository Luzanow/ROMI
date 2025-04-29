from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

like_dislike_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❤️", callback_data="like"),
        InlineKeyboardButton(text="👎", callback_data="dislike"),
        InlineKeyboardButton(text="⏭", callback_data="next")
    ]
])
