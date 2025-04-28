import aiosqlite
from config import DB_PATH

async def create_profile(telegram_id: int, name: str, age: int, bio: str, gender: str, looking_for: str, photo: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (telegram_id, name, age, bio, gender, looking_for, photo) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (telegram_id, name, age, bio, gender, looking_for, photo)
        )
        await db.commit()
        
