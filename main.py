import os
import logging
import asyncio
from aiogram import Bot
from main_bot.start_handler import dp
from dotenv import load_dotenv
from DB.Db import PG
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot  = Bot(TOKEN)
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())