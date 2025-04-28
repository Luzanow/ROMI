from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import add_like, check_match

router = Router()

@router.callback_query(F.data.startswith("like_"))
async def like_user(call: CallbackQuery):
    liked_id = int(call.data.split("_")[1])
    user_id = call.from_user.id

    await add_like(user_id, liked_id)
    if await check_match(user_id, liked_id):
        await call.message.answer("🎉 У вас взаємний лайк! Починайте спілкування!")
        await call.bot.send_message(liked_id, f"🎉 У тебе взаємний лайк з {call.from_user.first_name}!")

    await call.message.delete()
