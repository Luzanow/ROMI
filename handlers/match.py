from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import get_random_user, add_like, check_match

router = Router()

# Клавіатура реакцій, як у "Дайвінчик"
def reaction_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❤️", callback_data="like"),
                InlineKeyboardButton(text="📷", callback_data="photo"),
                InlineKeyboardButton(text="❌", callback_data="dislike"),
                InlineKeyboardButton(text="🛌", callback_data="skip")
            ]
        ]
    )

@router.message(F.text == "🔍 Знайти друзів")
async def show_random_profile(message: Message, state: FSMContext):
    user = await get_random_user(current_user_id=message.from_user.id)
    if not user:
        await message.answer("Немає більше анкет 😞")
        return

    profile_text = (
        f"{user['name']}, {user['age']} років\n"
        f"📍 {user['city']}\n"
        f"💬 {user['bio']}"
    )

    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=user['photo'],
        caption=profile_text,
        reply_markup=reaction_keyboard()
    )
    await state.update_data(current_shown_id=user['telegram_id'])

@router.callback_query(F.data.in_(["like", "dislike", "skip", "photo"]))
async def handle_reaction(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    shown_user_id = data.get("current_shown_id")

    if not shown_user_id:
        await callback.message.answer("Опитування недійсне.")
        return

    if callback.data == "like":
        await add_like(callback.from_user.id, shown_user_id)
        if await check_match(callback.from_user.id, shown_user_id):
            await callback.message.answer("😍 Це взаємно! Ви отримаєте чат")
        else:
            await callback.message.answer("💘 Ви лайкнули анкету!")
    elif callback.data == "dislike":
        await callback.message.answer("🙈 Анкету пропущено")
    elif callback.data == "photo":
        await callback.message.answer("📷 Фото вже показано")
    elif callback.data == "skip":
        await callback.message.answer("➡️ Наступна анкета")

    await show_random_profile(callback.message, state)
