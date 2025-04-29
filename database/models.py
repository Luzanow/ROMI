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
            INSERT OR REPLACE INTO users (telegram_id, name, age, gender, bio, photo, looking_for, city)
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

# Пошук випадкового користувача з того ж міста
async def get_random_user(current_user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT city FROM users WHERE telegram_id = ?", (current_user_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        current_city = row[0]

        cursor = await db.execute("""
            SELECT telegram_id, name, age, gender, bio, photo, looking_for, city
            FROM users
            WHERE telegram_id != ? AND city = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (current_user_id, current_city))
        row = await cursor.fetchone()
        if row:
            return {
                'telegram_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'bio': row[4],
                'photo': row[5],
                'looking_for': row[6],
                'city': row[7]
            }
        return None

# Зберегти лайк
async def add_like(user_id: int, liked_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO likes (user_id, liked_id) VALUES (?, ?)
        """, (user_id, liked_id))
        await db.commit()
