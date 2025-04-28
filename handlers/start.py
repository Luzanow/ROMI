from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.default import gender_kb, looking_for_kb
from database.models import add_user

router = Router()

class ProfileState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    bio = State()
    photo = State()
    looking_for = State()

@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await message.answer("Привіт! Як тебе звати?")
    await state.set_state(ProfileState.name)

@router.message(ProfileState.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Скільки тобі років?")
    await state.set_state(ProfileState.age)

@router.message(ProfileState.age)
async def set_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введи свій вік числом.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Яка твоя стать?", reply_markup=gender_kb())
    await state.set_state(ProfileState.gender)

@router.message(ProfileState.gender)
async def set_gender(message: Message, state: FSMContext):
    if message.text not in ["Чоловік", "Жінка"]:
        await message.answer("Вибери через кнопки.")
        return
    await state.update_data(gender=message.text)
    await message.answer("Опиши себе коротко.")
    await state.set_state(ProfileState.bio)

@router.message(ProfileState.bio)
async def set_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await message.answer("Надішли своє фото 📸")
    await state.set_state(ProfileState.photo)

@router.message(ProfileState.photo)
async def set_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Це не фото!")
        return
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    await message.answer("Кого шукаєш?", reply_markup=looking_for_kb())
    await state.set_state(ProfileState.looking_for)

@router.message(ProfileState.looking_for)
async def set_looking_for(message: Message, state: FSMContext):
    if message.text not in ["Чоловіка", "Жінку", "Неважливо"]:
        await message.answer("Вибери через кнопки.")
        return
    data = await state.get_data()
    await add_user(
        telegram_id=message.from_user.id,
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        bio=data["bio"],
        photo=data["photo"],
        looking_for=message.text
    )
    await message.answer("Анкету створено! 🔥 Можеш шукати знайомства!")
    await state.clear()
