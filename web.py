import asyncio
from flask import Flask, render_template, request, jsonify
from loader import db

app = Flask(__name__)

async def get_users():
    await db.create()
    await db.create_table_users()
    users = await db.select_all_users()
    return users

async def get_user_messages(telegram_id):
    await db.create()
    await db.create_table_users()
    messages = await db.select_all_messages()
    message_list = []

    for message in messages:
        if int(message[1]) == int(telegram_id):
            message_dict = {
                'user_id': message[1],
                'yesterday': message[2],
                'today': message[3],
                'tomorrow': message[4],
                'created_at': message[5].isoformat()
            }
            message_list.append(message_dict)

    return message_list

@app.route('/user_messages/<int:telegram_id>')
async def user_messages(telegram_id):
    messages = await get_user_messages(telegram_id)
    print(messages)
    return jsonify({'messages': messages})

@app.route('/')
async def index():
    users = await get_users()
    return render_template('index.html', users=users)

@app.route('/get_user_id', methods=['POST'])
async def get_user_id():
    users = await get_users()
    selected_fullname = request.form.get('selected_fullname')
    user_id = None

    for user in users:
        if user['fullname'] == selected_fullname:
            user_id = user['user_id']
            break

    return jsonify({'user_id': user_id})

if __name__ == '__main__':
    asyncio.run(app.run(debug=True))