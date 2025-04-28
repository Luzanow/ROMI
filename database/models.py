from database.db import get_db

async def create_profile(telegram_id, name, age, gender, bio, photo, looking_for):
    db = await get_db()
    await db.execute('''
        INSERT INTO profiles (telegram_id, name, age, gender, bio, photo, looking_for)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (telegram_id, name, age, gender, bio, photo, looking_for))
    await db.commit()
    await db.close()

async def get_random_user(current_user_id):
    db = await get_db()
    cursor = await db.execute('''
        SELECT id, telegram_id, name, age, gender, bio, photo, looking_for
        FROM profiles
        WHERE telegram_id != ?
        ORDER BY RANDOM()
        LIMIT 1
    ''', (current_user_id,))
    user = await cursor.fetchone()
    await db.close()
    return [user] if user else []
