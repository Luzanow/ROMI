from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import get_random_user

router = Router()

# Клавіатура реакцій, як у "Дайвінчик"
def reaction_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❤️", callback_data="like"),
                InlineKeyboardButton(text="📷", callback_data="photo"),
                InlineKeyboardButton(text="❌", callback_data="dislike"),
                InlineKeyboardButton(text="💤", callback_data="skip")
            ]
        ]
    )

@router.message(F.text == "🔍 Знайти друзів")
async def show_random_profile(message: Message, state: FSMContext):
    users = await get_random_user(current_user_id=message.from_user.id)
    if not users:
        await message.answer("😢 Анкет більше немає у твоєму місті.")
        return

    user = users[0]
    await state.update_data(current_shown_id=user[1])  # telegram_id

    profile_text = (
        f"{user[2]}, {user[3]} років\n"       # name, age
        f"📍 {user[9]}\n"                      # city
        f"💬 {user[5]}"                        # bio
    )

    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=user[6],  # photo file_id
        caption=profile_text,
        reply_markup=reaction_keyboard()
    )

@router.callback_query(F.data.in_(["like", "dislike", "skip", "photo"]))
async def handle_reaction(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    shown_user_id = data.get("current_shown_id")

    if callback.data == "like":
        await callback.message.answer("💘 Тобі сподобалась анкета!")
        # await save_like(callback.from_user.id, shown_user_id)
    elif callback.data == "dislike":
        await callback.message.answer("🙈 Ти пропустив(ла) цю анкету.")
    elif callback.data == "photo":
        await callback.message.answer("📸 Фото вже показано 😉")
    elif callback.data == "skip":
        await callback.message.answer("➡️ Переходимо до наступної анкети...")

    await callback.message.delete()
    await show_random_profile(callback.message, state)
