# database/models.py
import aiosqlite
from config import DB_PATH

# Створення таблиць
async def create_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                age INTEGER,
                gender TEXT,
                bio TEXT,
                photo TEXT,
                looking_for TEXT,
                city TEXT
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                liked_id INTEGER
            )
        ''')
        await db.commit()

# Створення анкети
async def create_profile(telegram_id: int, name: str, age: int, gender: str, bio: str, photo: str, looking_for: str, city: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, name, age, gender, bio, photo, looking_for, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (telegram_id, name, age, gender, bio, photo, looking_for, city))
        await db.commit()

# Отримати свою анкету
async def get_profile(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT name, age, gender, bio, photo, looking_for, city
            FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        return await cursor.fetchone()

# Пошук інших користувачів з того самого міста
async def get_random_users(current_user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT city FROM users WHERE telegram_id = ?", (current_user_id,))
        result = await cursor.fetchone()
        if not result:
            return []
        current_city = result[0]

        cursor = await db.execute("""
            SELECT id, telegram_id, name, age, gender, bio, photo, looking_for, city
            FROM users
            WHERE telegram_id != ? AND city = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (current_user_id, current_city))
        return await cursor.fetchall()
