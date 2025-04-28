import aiosqlite

async def create_profile(telegram_id, name, age, gender, bio, photo, looking_for):
    async with aiosqlite.connect("your_database.db") as db:
        await db.execute('''
            INSERT INTO profiles (telegram_id, name, age, gender, bio, photo, looking_for)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (telegram_id, name, age, gender, bio, photo, looking_for))
        await db.commit()
