from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import create_profile
from states.states import ProfileStates

router = Router()

# Клавіатура після створення анкети
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Пошук")],
        [KeyboardButton(text="📝 Змінити анкету")],
    ],
    resize_keyboard=True
)

@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привіт! Давайте створимо вашу анкету. Введіть ваше ім'я:")
    await state.set_state(ProfileStates.name)

@router.message(ProfileStates.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Вкажіть ваш вік:")
    await state.set_state(ProfileStates.age)

@router.message(ProfileStates.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Напишіть короткий опис про себе:")
    await state.set_state(ProfileStates.bio)

@router.message(ProfileStates.bio)
async def get_bio(message: Message, state: FSMContext):
    data = await state.get_data()
    await create_profile(
        telegram_id=message.from_user.id,
        name=data['name'],
        age=data['age'],
        gender="Не вказано",  # можна зробити потім вибір статі
        bio=message.text,
        photo="https://placehold.co/300x400",  # Тестова фотка
        looking_for="Будь-хто"
    )
    await message.answer(
        "Анкету створено ✅\nМожете шукати знайомства або змінити анкету!",
        reply_markup=menu_keyboard
    )
    await state.clear()
