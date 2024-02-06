from telebot import types

from common.models import Region, District, Quarter
from botapp.models import *

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
    buttons = []  
    for district in districts:
        button = types.InlineKeyboardButton(district.name_uz, callback_data=f'district_{district.id}')
        buttons.append(button)
    while buttons:
        row = buttons[:2] 
        keyboard.add(*row)  
        buttons = buttons[2:] 

    return keyboard

def district_keyboard_ru(region_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    districts = District.objects.filter(region_id=region_id)
    buttons = []  
    for district in districts:
        button = types.InlineKeyboardButton(district.name_ru, callback_data=f'district_{district.id}')
        buttons.append(button)
    while buttons:
        row = buttons[:2] 
        keyboard.add(*row)  
        buttons = buttons[2:] 

    return keyboard


def interest_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    interests = Interest.objects.all()
    for interest in interests:
        button = types.InlineKeyboardButton(interest.name, callback_data=f"interest_{interest.id}")
        keyboard.add(button)
    return keyboard

def education_keyboard(interest_id):
    keyboard = types.InlineKeyboardMarkup()
    educations = Education.objects.filter(interest_id=interest_id)
    for education in educations:
        button = types.InlineKeyboardButton(education.name, callback_data=f"education_{education.id}")
        keyboard.add(button)
    return keyboard

def course_keyboard(education_id):
    keyboard = types.InlineKeyboardMarkup()
    courses = Course.objects.filter(education_id=education_id)
    for course in courses:
        button = types.InlineKeyboardButton(course.name, callback_data=f"course_{course.id}")
        keyboard.add(button)
    return keyboard