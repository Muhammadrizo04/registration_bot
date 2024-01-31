from telebot import types

from common.models import Region, District, Quarter

def confirm_uz():
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton(text="Ha✅")
    no = types.KeyboardButton(text="Yo'q❌")
    button.add(yes, no)
    return button

def confirm_ru():
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

def region_keyboard_uz():
    keyboard = types.InlineKeyboardMarkup()
    regions = Region.objects.all()
    for region in regions:
        button = types.InlineKeyboardButton(region.name_uz, callback_data=f'region_{region.id}')
        keyboard.add(button)
    return keyboard

def region_keyboard_ru():
    keyboard = types.InlineKeyboardMarkup()
    regions = Region.objects.all()
    for region in regions:
        button = types.InlineKeyboardButton(region.name_ru, callback_data=f'region_{region.id}')
        keyboard.add(button)
    return keyboard

def district_keyboard_uz(region_id):
    keyboard = types.InlineKeyboardMarkup()
    districts = District.objects.filter(region_id=region_id)
    for district in districts:
        button = types.InlineKeyboardButton(district.name_uz, callback_data=f'district_{district.id}')
        keyboard.add(button)
    return keyboard

def district_keyboard_ru(region_id):
    keyboard = types.InlineKeyboardMarkup()
    districts = District.objects.filter(region_id=region_id)
    for district in districts:
        button = types.InlineKeyboardButton(district.name_ru, callback_data=f'district_{district.id}')
        keyboard.add(button)
    return keyboard

def quarter_keyboard_uz(district_id):
    keyboard = types.InlineKeyboardMarkup()
    quarters = Quarter.objects.filter(district_id=district_id)
    for quarter in quarters:
        button = types.InlineKeyboardButton(quarter.name_uz, callback_data=f'quarter_{quarter.id}')
        keyboard.add(button)
    return keyboard

def quarter_keyboard_ru(district_id):
    keyboard = types.InlineKeyboardMarkup()
    quarters = Quarter.objects.filter(district_id=district_id)
    for quarter in quarters:
        button = types.InlineKeyboardButton(quarter.name_uz, callback_data=f'quarter_{quarter.id}')
        keyboard.add(button)
    return keyboard