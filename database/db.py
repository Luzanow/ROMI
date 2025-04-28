import aiosqlite
from config import DB_PATH

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
                looking_for TEXT
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
