import asyncio
from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from datetime import datetime, time

async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()
    await db.create_table_messages()
    await db.create_table_time_control()
    
    # try:
    #     time_to_insert = time.fromisoformat("23:59:00")
    #     await db.add_time(time_to_insert)
    # except Exception as e:
    #     print(e)
        
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
