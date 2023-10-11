from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from data.config import ADMINS
import pandas as pd

@dp.message_handler(commands=['excel'])
async def excel_converter(message: types.Message):
    messages = await db.select_all_messages()
    df = pd.DataFrame(messages)
    df.to_excel('messages.xlsx', index=False)
    await message.answer_document(open('messages.xlsx', "rb"))