import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import CHANNEL

from loader import dp, db, bot, storage
from keyboards.inline.Approve import messageApproveState
from states.taskAdd import TaskDataAdd
from datetime import datetime, time

@dp.message_handler(commands=['run'])
async def add_tasks(message: types.Message):
    await message.answer("🚀Started scheduler.")
    while True:
        current_time = datetime.now().time()
        formatted_time = current_time.strftime('%H:%M:00')
        formatted_time = datetime.strptime(formatted_time, '%H:%M:%S').time()
        scheduled_messages = await db.get_scheduled_messages(formatted_time)
        if scheduled_messages:
            users = await db.select_all_users()
            for user in users:
                state = dp.current_state(chat=message.chat.id, user=user[0])
                if state is not None:
                    await state.finish()

                await bot.send_message(chat_id=user[0], text="Are you ready to report?", reply_markup=messageApproveState)
                await asyncio.sleep(3)
                
            await asyncio.sleep(30)
        await asyncio.sleep(20)

