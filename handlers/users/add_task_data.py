from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import CHANNEL

from loader import dp, db, bot
from keyboards.inline.Approve import messageApprove
from states.taskAdd import TaskDataAdd

from datetime import datetime, timedelta

# @dp.message_handler(commands=['add'])
@dp.callback_query_handler(lambda c: c.data.startswith('approve_message_state'))
async def add_tasks(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except:
        pass
    await call.message.answer("what did you do yesterday?: ")
    await TaskDataAdd.yesterday.set()

@dp.message_handler(state=TaskDataAdd.yesterday)
async def answer_yesterday(message: types.Message, state: FSMContext):
    await state.set_data(
        {
        "yesterday_text" : message.text
        }
    )
    await message.answer("what did you do today?: ")
    await TaskDataAdd.today.set()

@dp.message_handler(state=TaskDataAdd.today)
async def today_yesterday(message: types.Message, state: FSMContext):
    await state.update_data(
        {
        "today_text" : message.text
        }
    )
    await message.answer("what are you going to do tomorrow?: ")
    await TaskDataAdd.tomorrow.set()

@dp.message_handler(state=TaskDataAdd.tomorrow)
async def today_yesterday(message: types.Message, state: FSMContext):
    today_date = datetime.today()
    yesterday_date = today_date - timedelta(days=1)
    tomorrow_date = today_date + timedelta(days=1)

    today_date_str = today_date.strftime('%Y-%m-%d')
    yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')
    tomorrow_date_str = tomorrow_date.strftime('%Y-%m-%d')

    await state.update_data(
        {
        "tomorrow_text" : message.text
        }
    )

    datas = await state.get_data()
    yesterday = datas['yesterday_text']
    today = datas['today_text']
    tomorrow = message.text

    await message.answer(f"<b>Yesterday {yesterday_date_str}</b>\n{yesterday}\n\n"
                        f"<b>Today {today_date_str}</b>\n{today}\n\n"
                        f"<b>Tomorrow {tomorrow_date_str}</b>\n{tomorrow}", reply_markup=messageApprove)
    
    await TaskDataAdd.data_verification.set()

@dp.callback_query_handler(lambda c: c.data.startswith('message_confirm'), state=TaskDataAdd.data_verification)
async def answer_message_data_verification_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    today_date = datetime.today()
    current_time = datetime.now()
    
    yesterday_date = today_date - timedelta(days=1)
    tomorrow_date = today_date + timedelta(days=1)

    time_str = current_time.strftime('%H:%M:%S')
    today_date_str = today_date.strftime('%Y-%m-%d')
    yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')
    tomorrow_date_str = tomorrow_date.strftime('%Y-%m-%d')

    datas = await state.get_data()
    yesterday = datas['yesterday_text']
    today = datas['today_text']
    tomorrow = datas['tomorrow_text']

    save_text = f"<b>Yesterday {yesterday_date_str}</b>\n{yesterday}\n\n"
    save_text +=f"<b>Today {today_date_str}</b>\n{today}\n\n"
    save_text +=f"<b>Tomorrow {tomorrow_date_str}</b>\n{tomorrow}"
    
    user_data = await db.select_user(telegram_id = call.from_user.id)

    await db.add_message(user_id=call.from_user.id, yesterday=yesterday, today=today, tomorrow=tomorrow)
    save_text += f"\n\n⏰ {time_str} 📆 {today_date_str}"
    await bot.send_message(chat_id=CHANNEL, text=f"👤{user_data[1]}\n\n{save_text}")
    save_text += "\ndata saved✅"
    await call.message.answer(save_text)

    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('message_cancel'), state=TaskDataAdd.data_verification)
async def answer_message_data_verification_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("canceled.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data.startswith('cancel_message_state'))
async def answer_message_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("canceled✅")
