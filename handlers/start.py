from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# Імпортуємо кнопки з правильного місця
from keyboards.registration import gender_keyboard, looking_for_keyboard, confirm_keyboard

# Імпортуємо стани
from states.registration import RegistrationStates

# Функція збереження профілю
from database.models import create_profile

router = Router()

@router.message(F.text == "/start")
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Привіт! Скільки тобі років? 🎂")
    await state.set_state(RegistrationStates.age)

@router.message(RegistrationStates.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введи вік цифрою! 🔢")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Обери свою стать 👨‍💼👩‍💼:", reply_markup=gender_keyboard())
    await state.set_state(RegistrationStates.gender)

@router.message(RegistrationStates.gender)
async def get_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Кого хочеш знайти? 👀", reply_markup=looking_for_keyboard())
    await state.set_state(RegistrationStates.looking_for)

@router.message(RegistrationStates.looking_for)
async def get_looking_for(message: Message, state: FSMContext):
    await state.update_data(looking_for=message.text)
    await message.answer("Із якого ти міста? 📍 (Введи вручну)")
    await state.set_state(RegistrationStates.city)

@router.message(RegistrationStates.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Як тебе називати? ✏️ (Ім'я або нік)")
    await state.set_state(RegistrationStates.name)

@router.message(RegistrationStates.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Розкажи трохи про себе 📄:")
    await state.set_state(RegistrationStates.bio)

@router.message(RegistrationStates.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.answer("Тепер надішли своє фото 📸:")
    await state.set_state(RegistrationStates.photo)

@router.message(RegistrationStates.photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Будь ласка, надішли саме фото! 📸")
        return
    
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)

    data = await state.get_data()

    text = (
        f"👤 Ім'я: {data['name']}\n"
        f"🎂 Вік: {data['age']}\n"
        f"📍 Місто: {data['city']}\n"
        f"💬 Про себе: {data['bio']}\n"
        f"👀 Кого шукає: {data['looking_for']}\n"
        f"⚧ Стать: {data['gender']}"
    )

    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_file_id,
        caption="Так виглядає твоя анкета:\n\n" + text,
        reply_markup=confirm_keyboard()
    )

    await state.set_state(RegistrationStates.confirm)

@router.callback_query(F.data == "confirm_yes")
async def confirm_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await create_profile(
        telegram_id=callback.from_user.id,
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        bio=data['bio'],
        photo=data['photo'],
        looking_for=data['looking_for'],
        city=data['city']
    )

    await callback.message.answer("✅ Анкету збережено! Тепер можеш шукати людей.")
    await state.clear()

@router.callback_query(F.data == "confirm_edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Окей, давай почнемо заново! Напиши свій вік 🎂:")
    await state.set_state(RegistrationStates.age)
