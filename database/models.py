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

# Створення анкети користувача
async def create_profile(telegram_id: int, name: str, age: int, gender: str, bio: str, photo: str, looking_for: str, city: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, name, age, gender, bio, photo, looking_for, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (telegram_id, name, age, gender, bio, photo, looking_for, city))
        await db.commit()

# Отримати анкету за telegram_id
async def get_profile(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT name, age, gender, bio, photo, looking_for, city
            FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        return await cursor.fetchone()

# Пошук випадкових користувачів (наприклад, для свайпів)
async def get_random_users(current_user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT id, telegram_id, name, age, gender, bio, photo, looking_for, city
            FROM users
            WHERE telegram_id != ?
            ORDER BY RANDOM()
            LIMIT 10
        """, (current_user_id,))
        return await cursor.fetchall()
