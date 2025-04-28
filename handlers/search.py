from aiogram import Router
from aiogram.types import Message
from database.models import get_random_user
from keyboards.inline import like_dislike_kb

router = Router()

@router.message(lambda message: message.text == "🔍 Пошук")
async def search_profiles(message: Message):
    users = await get_random_user(message.from_user.id)
    if not users:
        await message.answer("Наразі немає анкет для перегляду 😔")
        return
    for user in users:
        user_id, telegram_id, name, age, gender, bio, photo, looking_for = user
        text = f"{name}, {age} років\n📄 {bio}"
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text, reply_markup=like_dislike_kb(telegram_id))
