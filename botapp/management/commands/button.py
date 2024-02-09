from telebot import types

from common.models import Region, District, Quarter
from botapp.models import *


def confirm_uz():
    button = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Ha✅", callback_data="confirm_uz")
    no = types.InlineKeyboardButton(text="Yo'q❌", callback_data="cancel_uz")
    button.add(yes, no)
    return button


def confirm_ru():
    button = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да✅", callback_data="confirm_ru")
    no = types.InlineKeyboardButton(text="Нет❌", callback_data="cancel_ru")
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
    regions = Region.objects.all().order_by('name_uz')
    for region in regions:
        button = types.InlineKeyboardButton(region.name_uz, callback_data=f'region_{region.id}')
        keyboard.add(button)
    return keyboard


def region_keyboard_ru():
    keyboard = types.InlineKeyboardMarkup()
    regions = Region.objects.all().order_by('name_ru')
    for region in regions:
        button = types.InlineKeyboardButton(region.name_ru, callback_data=f'region_{region.id}')
        keyboard.add(button)
    return keyboard


def district_keyboard_uz(region_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    districts = District.objects.filter(region_id=region_id).order_by('name_uz')
    buttons = []

    for district in districts:
        button = types.InlineKeyboardButton(district.name_uz, callback_data=f'district_{district.id}')
        buttons.append(button)

    while buttons:
        row = buttons[:2]
        keyboard.add(*row)
        buttons = buttons[2:]

    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 

    return keyboard



def district_keyboard_ru(region_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    districts = District.objects.filter(region_id=region_id).order_by('name_ru')
    buttons = []
    for district in districts:
        button = types.InlineKeyboardButton(district.name_ru, callback_data=f'district_{district.id}')
        buttons.append(button)
    while buttons:
        row = buttons[:2]
        keyboard.add(*row)
        buttons = buttons[2:]
    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def interest_keyboard_uz():
    keyboard = types.InlineKeyboardMarkup()
    interests = Interest.objects.all().order_by('name_uz')
    for interest in interests:
        button = types.InlineKeyboardButton(interest.name_uz, callback_data=f"interest_{interest.id}")
        keyboard.add(button)
    return keyboard


def interest_keyboard_ru():
    keyboard = types.InlineKeyboardMarkup()
    interests = Interest.objects.all().order_by('name_ru')
    for interest in interests:
        button = types.InlineKeyboardButton(interest.name_ru, callback_data=f"interest_{interest.id}")
        keyboard.add(button)
    return keyboard


def education_keyboard(interest_id):
    keyboard = types.InlineKeyboardMarkup()
    educations = Education.objects.filter(interest_id=interest_id).order_by('name_uz')
    for education in educations:
        button = types.InlineKeyboardButton(education.name_uz, callback_data=f"education_{education.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def category_keyboard_uz(interest_id):
    keyboard = types.InlineKeyboardMarkup()
    categorys = Category.objects.filter(interest_id=interest_id).order_by('name_uz')
    for category in categorys:
        button = types.InlineKeyboardButton(category.name_uz, callback_data=f"category_{category.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def category_keyboard_ru(interest_id):
    keyboard = types.InlineKeyboardMarkup()
    categorys = Category.objects.filter(interest_id=interest_id).order_by('name_ru')
    for category in categorys:
        button = types.InlineKeyboardButton(category.name_ru, callback_data=f"category_{category.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def course_keyboard_uz(category_id):
    keyboard = types.InlineKeyboardMarkup()
    courses = Course.objects.filter(category_id=category_id).order_by('name_uz')
    for course in courses:
        button = types.InlineKeyboardButton(course.name_uz, callback_data=f"course_{course.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def course_keyboard_ru(category_id):
    keyboard = types.InlineKeyboardMarkup()
    courses = Course.objects.filter(category_id=category_id).order_by('name_ru')
    for course in courses:
        button = types.InlineKeyboardButton(course.name_ru, callback_data=f"course_{course.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard


def problem_keyboard_uz():
    keyboard = types.InlineKeyboardMarkup()
    # Use the custom manager method to get only parent problems
    problems = Problem.objects.get_parents().order_by('name_uz')
    for problem in problems:
        button = types.InlineKeyboardButton(problem.name_uz, callback_data=f"problem_{problem.id}")
        keyboard.add(button)
    return keyboard


def problem_keyboard_ru():
    keyboard = types.InlineKeyboardMarkup()
    # Use the custom manager method to get only parent problems
    problems = Problem.objects.get_parents().order_by('name_ru')
    for problem in problems:
        button = types.InlineKeyboardButton(problem.name_ru, callback_data=f"problem_{problem.id}")
        keyboard.add(button)
    return keyboard


def problem_child_uz(problem_id):
    keyboard = types.InlineKeyboardMarkup()
    problems = Problem.objects.filter(parent__id=problem_id).order_by('name_uz')
    for problem in problems:
        button = types.InlineKeyboardButton(problem.name_uz, callback_data=f"child_{problem.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard

def problem_child_ru(problem_id):
    keyboard = types.InlineKeyboardMarkup()
    problems = Problem.objects.filter(parent__id=problem_id).order_by('name_uz')
    for problem in problems:
        button = types.InlineKeyboardButton(problem.name_ru, callback_data=f"child_{problem.id}")
        keyboard.add(button)
    back_button = types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_regions')
    keyboard.add(back_button) 
    return keyboard