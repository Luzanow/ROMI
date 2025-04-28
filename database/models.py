import aiosqlite
from config import DB_PATH

async def add_user(telegram_id, name, age, gender, bio, photo, looking_for):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (telegram_id, name, age, gender, bio, photo, looking_for)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (telegram_id, name, age, gender, bio, photo, looking_for))
        await db.commit()

async def get_random_user(current_user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM users WHERE telegram_id != ?', (current_user_id,)) as cursor:
            return await cursor.fetchall()

async def add_like(user_id, liked_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT INTO likes (user_id, liked_id) VALUES (?, ?)', (user_id, liked_id))
        await db.commit()

async def check_match(user_id, liked_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM likes WHERE user_id = ? AND liked_id = ?', (liked_id, user_id)) as cursor:
            match = await cursor.fetchone()
            return match is not None
