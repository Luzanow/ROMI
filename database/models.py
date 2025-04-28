import aiosqlite
from config import DB_PATH

# Створення анкети
async def create_profile(telegram_id: int, name: str, age: int, bio: str, gender: str, looking_for: str, photo: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (telegram_id, name, age, bio, gender, looking_for, photo) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (telegram_id, name, age, bio, gender, looking_for, photo)
        )
        await db.commit()

# Отримати свою анкету
async def get_profile(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT name, age, bio, gender, looking_for, photo FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        profile = await cursor.fetchone()
        return profile

# Оновити анкету
async def update_profile(telegram_id: int, name: str, age: int, bio: str, gender: str, looking_for: str, photo: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET name = ?, age = ?, bio = ?, gender = ?, looking_for = ?, photo = ? WHERE telegram_id = ?",
            (name, age, bio, gender, looking_for, photo, telegram_id)
        )
        await db.commit()

# Пошук інших анкет
async def get_random_user(current_user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, telegram_id, name, age, gender, bio,_
