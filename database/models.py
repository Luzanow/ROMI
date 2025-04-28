from database.db import get_db

async def add_like(user_id: int, liked_id: int):
    db = await get_db()
    await db.execute(
        "INSERT INTO likes (user_id, liked_id) VALUES (?, ?)",
        (user_id, liked_id)
    )
    await db.commit()
    await db.close()

async def check_match(user_id: int, liked_id: int) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "SELECT id FROM likes WHERE user_id = ? AND liked_id = ?",
        (liked_id, user_id)
    )
    result = await cursor.fetchone()
    await db.close()
    return result is not None
