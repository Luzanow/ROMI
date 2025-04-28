import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import create_db
from handlers import start, search, match

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(search.router)
    dp.include_router(match.router)

    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
