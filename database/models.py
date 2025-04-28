import aiosqlite
from config import DB_PATH

# Створення нової анкети
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

# Отримати випадкового користувача для пошуку
async def get_random_user(current_user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, telegram_id, name, age, gender, bio, photo, looking_for FROM users WHERE telegram_id != ? ORDER BY RANDOM() LIMIT 10",
            (current_user_id,)
        )
        users = await cursor.fetchall()
        return users

# Додати лайк
async def add_like(user_id: int, liked_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO likes (user_id, liked_id) VALUES (?, ?)",
            (user_id, liked_id)
        )
        await db.commit()

# Перевірити чи є взаємний лайк
async def check_match(user_id: int, liked_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM likes WHERE user_id = ? AND liked_id = ?",
            (user_id, liked_id)
        )
        match = await cursor.fetchone()
        return match is not None
