import os
import sqlite3
from telebot import TeleBot
from telebot import types
from telebot.types import ReplyKeyboardRemove
from buttons import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, 'data.sqlite')

TOKEN = "6464390310:AAEDgUK1-WKaxfI6TGWaqRdB_thdorx80z8"
bot = TeleBot(TOKEN)

# Function to establish a database connection

def get_db_connection():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor


# Function to create tables if they don't exist


@bot.message_handler(commands=['start'])
def start_message(message):
    connection, cursor = get_db_connection()

    # Insert or update user information in the SQLite database
    cursor.execute('SELECT * FROM users WHERE chat_id=? ;',[message.from_user.id])
    info = cursor.fetchall()
    if not info:
        cursor.execute('INSERT INTO users(name,chat_id) VALUES(?,?);',[ message.from_user.first_name, message.from_user.id])

    connection.commit()
    connection.close()
    bot.send_message(
        message.chat.id,
        f"Asslamu aleykum {message.from_user.first_name} tillardan birinni tanlang\n\n Привет {message.from_user.first_name} выберите один из языков ",
        reply_markup=languages()
    )
@bot.callback_query_handler(func=lambda call: True)
def info(call):
    connection, cursor = get_db_connection()
    cursor.execute('SELECT * FROM users WHERE chat_id=? ;',[call.from_user.id])
    info = cursor.fetchall()
    if call.data == "uz":
        bot.send_message(
            call.message.chat.id,
            "Iltimos telefon raqamingizni yuboring",
            reply_markup=contacts_uz()
        )

        if not info:
            cursor.execute('INSERT INTO users(name,chat_id) VALUES(?,?);',[call.from_user.first_name, call.from_user.id])
        else:
            cursor.execute("UPDATE users SET user_lang='Uz' WHERE id=?;",[info[0][0]])

        connection.commit()
        connection.close()
    elif call.data == "ru":
        bot.send_message(
            call.message.chat.id,
            "Пожалуйста, поделитесь своим номером телефона",
            reply_markup=contacts_ru()
        )
        if not info:
            cursor.execute('INSERT INTO users(name,chat_id) VALUES(?,?);',[call.from_user.first_name, call.from_user.id])
        else:
            cursor.execute("UPDATE users SET user_lang='Ru' WHERE id=?;",[info[0][0]])

    elif info[0][10]=="wait_district":
        region_id = call.data
        if info[0][9]=="Uz":
            cursor.execute('SELECT id, name_uz FROM districts WHERE region_id=?;', [region_id])
            districts = cursor.fetchall()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for district in districts:
                button = types.InlineKeyboardButton(text=district[1], callback_data=str(districts[0]))
                keyboard.add(button)

            bot.send_message(
                call.message.chat.id,
                "Iltimos tumanni tanlang:",
                reply_markup=keyboard
            )
        elif info[0][9]=="Ru":
            cursor.execute('SELECT id, name_ru FROM districts WHERE region_id=?;', [region_id])
            districts = cursor.fetchall()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for district in districts:
                button = types.InlineKeyboardButton(text=district[1], callback_data=str(districts[0]))
                keyboard.add(button)

            bot.send_message(
                call.message.chat.id,
                "Iltimos tumanni tanlang:",
                reply_markup=keyboard
            )
        cursor.execute("UPDATE users SET user_state='wait_quarters' WHERE chat_id=?;", [call.message.chat.id])
    elif info[0][10] == "wait_quarters":
        district_id = call.data
        cursor.execute('SELECT id, name FROM quarters WHERE district_id=?;', [district_id])
        quarters = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for quarter in quarters:
            button = types.InlineKeyboardButton(text=quarter[1], callback_data=str(quarter[0]))
            keyboard.add(button)

        bot.send_message(
            call.message.chat.id,
            "Iltimos mahallani tanlang:",
            reply_markup=keyboard
        )

    connection.commit()
    connection.close()
@bot.message_handler(func=lambda message: True, content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number

    connection, cursor = get_db_connection()

    cursor.execute(
        "UPDATE users SET phone_number = ? WHERE chat_id = ?",
        (phone_number, chat_id)
    )


    cursor.execute('SELECT * FROM users WHERE chat_id=? ;',[message.from_user.id])
    info=cursor.fetchall()
    if info[0][9]=="Uz":
        bot.send_message(
            message.chat.id,
            f"Sizda ikkinchi raqam mavjudmi?",
            reply_markup=confirmation_uz()
        )
    elif info[0][9]=="Ru":
        bot.send_message(
            message.chat.id,
            f"у вас ест второй номер?",
            reply_markup=confirmation_ru()
        )



    connection.commit()
    connection.close()
# Add another message handler to handle the full name input
@bot.message_handler(func=lambda message: True, content_types=['text'])
def get_number(message):
    connection, cursor = get_db_connection()
    cursor.execute('SELECT * FROM users WHERE chat_id=? ;',[message.from_user.id])
    info = cursor.fetchall()

    if message.text == "Ha✅":
        bot.send_message(
            message.chat.id,
            "iltimos ikkinchi raqamingizni kiriting",
            reply_markup=ReplyKeyboardRemove(selective=False)
        )
        cursor.execute("UPDATE users SET user_state='get_2number' WHERE chat_id=?;", [message.chat.id])
    elif message.text == "Да✅":
        bot.send_message(
            message.chat.id,
            "видети ваш второй номер",
            reply_markup=ReplyKeyboardRemove(selective=False)
        )
        cursor.execute("UPDATE users SET user_state='get_2number' WHERE chat_id=?;", [message.chat.id])
    elif info[0][10] == "get_2number":
        cursor.execute("UPDATE users SET phone_number_2=? WHERE chat_id=?;", [message.text, message.chat.id])
        cursor.execute("UPDATE users SET user_state='full_name_received' WHERE chat_id=?;", [message.chat.id])
        if info[0][9]=="Uz":
            bot.send_message(
                message.chat.id,
                "iltimos ism familya sharifingizni kiriting",
                reply_markup=ReplyKeyboardRemove(selective=False)
            )
        elif info[0][9]=="Ru":
            bot.send_message(
                message.chat.id,
                "iltimos ism familya sharifingizni RU",
                reply_markup=ReplyKeyboardRemove(selective=False)
            )
    elif info[0][10] == "full_name_received":
        cursor.execute("UPDATE users SET fullname=? WHERE chat_id=?;", [message.text, message.chat.id])
        cursor.execute("UPDATE users SET user_state='have_name' WHERE chat_id=?;", [message.chat.id])
        connection.commit()
        cursor.execute('SELECT * FROM users WHERE chat_id=? ;', [message.from_user.id])
        info = cursor.fetchall()
        select_region_button(message)
    elif message.text == "Yo'q❌":
        bot.send_message(
            message.chat.id,
            "iltimos ism familya sharifingizni kiriting",
            reply_markup=ReplyKeyboardRemove(selective=False)
        )
        cursor.execute("UPDATE users SET user_state='wait_fullname' WHERE chat_id=?;", [message.chat.id])

    elif message.text == "Нет❌":
        bot.send_message(
            message.chat.id,
            "iltimos ism familya sharifingizni kiriting RU",
            reply_markup=ReplyKeyboardRemove(selective=False)
        )
        cursor.execute("UPDATE users SET user_state='wait_fullname' WHERE chat_id=?;", [message.chat.id])
    elif info[0][10] == "wait_fullname":
        cursor.execute("UPDATE users SET fullname=? WHERE chat_id=?;", [message.text, message.chat.id])
        cursor.execute("UPDATE users SET user_state='have_name' WHERE chat_id=?;", [message.chat.id])
        connection.commit()
        cursor.execute('SELECT * FROM users WHERE chat_id=? ;', [message.from_user.id])
        info = cursor.fetchall()
        select_region_button(message)
    connection.commit()
    connection.close()


def select_region_button(message):
    connection, cursor = get_db_connection()
    cursor.execute('SELECT * FROM users WHERE chat_id=? ;',[message.from_user.id])
    info = cursor.fetchall()
    if info[0][9] == "Uz":
        cursor.execute('SELECT id, name_uz FROM regions;')
        regions = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for region in regions:
            button = types.InlineKeyboardButton(text=region[1], callback_data=str(region[0]))
            keyboard.add(button)
            print(f"calldata: {button.callback_data}")

        bot.send_message(
            message.chat.id,
            "Iltimos hududingizni tanlang:",
            reply_markup=keyboard
        )
    elif info[0][9] == "Ru":
        cursor.execute('SELECT id, name_ru FROM regions;')
        regions = cursor.fetchall()

        # Create buttons based on the regions in Russian language
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for region in regions:
            button = types.InlineKeyboardButton(text=region[1], callback_data=str(region[0]))
            keyboard.add(button)

        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите ваш регион:",
            reply_markup=keyboard
        )

    cursor.execute("UPDATE users SET user_state='wait_district' WHERE chat_id=?;", [message.chat.id])
    connection.commit()
    connection.close()




# Add similar logic for the Russian language if needed




bot.delete_webhook()
bot.infinity_polling()


