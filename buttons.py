from telebot import types

def confirmation_uz():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton(text="Ha✅")
    no = types.KeyboardButton(text="Yo'q❌")
    button.add(yes, no)
    return button

def confirmation_ru():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton(text="Да✅")
    no = types.KeyboardButton(text="Нет❌")
    button.add(yes, no)
    return button

def languages():
    language = types.InlineKeyboardMarkup()
    language_uz = types.InlineKeyboardButton(text='Uzbek tili 🇺🇿', callback_data='uz')
    language_ru = types.InlineKeyboardButton(text='Русский язык 🇷🇺', callback_data='ru')

    language.add(language_uz, language_ru)
    return language

def contacts_uz():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reg_button = types.KeyboardButton(text="Telefon raqamini ulashish", request_contact=True)
    keyboard.add(reg_button)
    return keyboard

def contacts_ru():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reg_button = types.KeyboardButton(text="поделитесь номером телефона", request_contact=True)
    keyboard.add(reg_button)
    return keyboard
