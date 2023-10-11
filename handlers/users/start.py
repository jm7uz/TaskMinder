from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

import asyncpg
from loader import dp, db
from data.config import ADMINS
from states.userRegister import UserRegister
from keyboards.inline.Approve import userApprove

user_fullname = {}

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(telegram_id=message.from_user.id,
                                 fullname = "user")
        await message.answer("Welcome!\nPlease enter your full name:")
        await UserRegister.fullName.set()
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer("Welcome.")
        await db.select_user(telegram_id=message.from_user.id)

    
@dp.message_handler(state=UserRegister.fullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    await state.finish()
    user_fullname[message.from_user.id] = message.text
    await message.answer(f"{message.text}\nDid you enter your full name correctly?", reply_markup=userApprove)


@dp.callback_query_handler(lambda c: c.data.startswith('register_confirm'))
async def full_check_correct(call: types.CallbackQuery):
    if call.from_user.id in user_fullname:
        await call.message.delete()
        await db.update_user_fullname(telegram_id=call.from_user.id, fullname = user_fullname[call.from_user.id])
        await call.message.answer("Your information has been saved✅")
    else:
        await call.answer("Error: no data")

@dp.callback_query_handler(lambda c: c.data.startswith('register_cancel'))
async def full_check_correct(call: types.CallbackQuery):
    await call.message.answer("Welcome!\nPlease enter your full name:")
    await UserRegister.fullName.set()
