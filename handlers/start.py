from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models import create_profile
from keyboards.menu import menu_keyboard
from states.states import ProfileStates

router = Router()

@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привіт! Давай створимо твою анкету 🌟\n\nВведи своє ім'я 👤:")
    await state.set_state(ProfileStates.name)

@router.message(ProfileStates.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Скільки тобі років 🎂:")
    await state.set_state(ProfileStates.age)

@router.message(ProfileStates.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введи вік цифрою! 🔢")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Напиши коротко про себе 📄:")
    await state.set_state(ProfileStates.bio)

@router.message(ProfileStates.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.answer("Тепер надішли 1 своє фото 📸:")
    await state.set_state(ProfileStates.photo)

@router.message(ProfileStates.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Будь ласка, надішли саме фото!")
        return

    # Оновлюємо state з фото
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()

    # Створюємо анкету
    await create_profile(
        telegram_id=message.from_user.id,
        name=data['name'],
        age=data['age'],
        gender="Не вказано",
        bio=data['bio'],
        photo=data['photo'],
        looking_for="Будь-хто"
    )

    profile_text = (
        f"👤 Ім'я: {data['name']}\n"
        f"🎂 Вік: {data['age']}\n"
        f"📄 Про себе: {data['bio']}\n"
    )

    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=data['photo'],
        caption="Ось як виглядає твоя анкета:\n\n" + profile_text
    )

    await message.answer(
        "✅ Анкету створено!\nЩо будемо робити далі?",
        reply_markup=menu_keyboard()
    )
    await state.clear()
