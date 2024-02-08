import telebot
from botapp.models import *
from .button import *
from telebot.types import ReplyKeyboardRemove
from common.models import Region, District, Quarter
from django.conf import settings
import os
TOKEN = '6584674642:AAG_7MIMMrBiuD_smtd3aJMsofEoCMEXRVk'
bot = telebot.TeleBot(TOKEN)

names_per_page = 10
selected_region_id = None
############################# quarter filter button #########################################

def quarter_buttons_uz(page_number, total_pages, names_queryset):
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # Set row width to 2 for quarters
    names_and_ids = [(quarter.name_uz, quarter.id) for quarter in names_queryset[(page_number - 1) * names_per_page:page_number * names_per_page]]
    for index, (name_uz, quarter_id) in enumerate(names_and_ids):
        button_text = str(name_uz)  # Convert to string to be safe
        button = types.InlineKeyboardButton(button_text, callback_data=f"quarter_id_{quarter_id}")
        if index % 2 == 0:
            row = [button]
            if index == len(names_and_ids) - 1:
                keyboard.row(button)
        else:
            row.append(button)
            keyboard.row(*row)  # Add a complete row of 2 buttons

    navigation_buttons = []
    if page_number > 1:
        navigation_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page_number - 1}"))
    if page_number < total_pages:
        navigation_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_{page_number + 1}"))
    keyboard.row(*navigation_buttons)

    return keyboard


def quarter_buttons_ru(page_number, total_pages, names_queryset):
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # Set row width to 2 for quarters
    names_and_ids = [(quarter.name_ru, quarter.id) for quarter in names_queryset[(page_number - 1) * names_per_page:page_number * names_per_page]]
    for index, (name_ru, quarter_id) in enumerate(names_and_ids):
        button_text = str(name_ru)  # Convert to string to be safe
        button = types.InlineKeyboardButton(button_text, callback_data=f"quarter_id_{quarter_id}")
        if index % 2 == 0:
            row = [button]
            if index == len(names_and_ids) - 1:
                keyboard.row(button)
        else:
            row.append(button)
            keyboard.row(*row)  # Add a complete row of 2 buttons

    navigation_buttons = []
    if page_number > 1:
        navigation_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page_number - 1}"))
    if page_number < total_pages:
        navigation_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_{page_number + 1}"))
    keyboard.row(*navigation_buttons)

    return keyboard



############################# quarter filter button #########################################

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    nick_name = message.chat.first_name
    try:
        user = BotUser.objects.get(chat_id=chat_id)
        bot.send_message(chat_id, "Salom! Bizning ta'lim va karyeraga bag`ishlangan botimizga xush kelibsiz. Muvaffaqiyatli kelajak sari yo'lda sizga yordam berishga tayyormiz! Keling, siz haqingizda ba'zi muhim narsalarni bilib olaylik. ", reply_markup=languages())
    except BotUser.DoesNotExist:
        BotUser.objects.create(
            chat_id=chat_id,
            nick_name=nick_name,

        )
        bot.send_message(chat_id, "Salom! Bizning ta'lim va karyeraga bag`ishlangan botimizga xush kelibsiz. Muvaffaqiyatli kelajak sari yo'lda sizga yordam berishga tayyormiz! Keling, siz haqingizda ba'zi muhim narsalarni bilib olaylik. ", reply_markup=languages())

@bot.callback_query_handler(func=lambda call: True)
def lang(call):
    chat_id = call.message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    current_language = user.user_lang
    current_state = user.user_state
    user.save()
    if call.data == "uz":
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_lang = 'UZ'
        user.user_state = "wait_phone"
        user.save()
        bot.send_message(chat_id, "Endi qo'shimcha ma'lumot kerak bo'lganda siz bilan bog'lanishimiz uchun aloqa telefon raqamingizni baham ko'ring. ", reply_markup=contacts_uz())

    elif call.data == "ru":
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_lang = 'RU'
        user.user_state = "wait_phone"
        user.save()
        bot.send_message(chat_id, "Теперь поделитесь своим контактным номером телефона, чтобы мы могли связаться с вами, когда нам понадобится дополнительная информация.", reply_markup=contacts_ru())
    
    elif current_state == "wait_region":
        user = BotUser.objects.get(chat_id=chat_id)
        region_id = call.data.split('_')[1]
        region = Region.objects.get(pk=region_id)
        user.region = region
        user.user_state = "wait_district"
        user.save()
        region.save()

        if current_language == 'UZ':
            bot.send_message(chat_id, "itimos tuman yoki shaharni tanlang", reply_markup=district_keyboard_uz(region_id))
        elif current_language == 'RU':
            bot.send_message(chat_id, "Выберите свой район или город", reply_markup=district_keyboard_ru(region_id))

    elif current_state == "wait_district":
        user = BotUser.objects.get(chat_id=chat_id)
        district_id = call.data.split('_')[1]
        district = District.objects.get(pk=district_id)
        user.district = district
        user.selected_district_id = district_id
        user.user_state = "wait_quarter"
        user.save()
        district.save()
        quarters = Quarter.objects.filter(district_id=district_id)  # Fetch quarters for selected district
        total_pages = (quarters.count() // names_per_page) + (quarters.count() % names_per_page > 0)
        page_number = 1  # Start from the first page

        if current_language == 'UZ':
            bot.send_message(chat_id, "Iltimos o'z MFYingizni tanlang", reply_markup=quarter_buttons_uz(page_number, total_pages, quarters))
        elif current_language == 'RU':
            bot.send_message(chat_id, "Выберите общественное собрание вашего района", reply_markup=quarter_buttons_ru(page_number, total_pages, quarters))
       
    
    elif current_state == "wait_quarter":
        if call.data.startswith("district_"):
            district_id = call.data.split("_")[1]
            quarters = Quarter.objects.filter(district_id=district_id)
            total_pages = (quarters.count() // names_per_page) + ((quarters.count() % names_per_page) > 0)
            page_number = 1
            keyboard = quarter_buttons_uz(page_number, total_pages, quarters)
            bot.edit_message_text("Choose a quarter:", chat_id, call.message.message_id, reply_markup=keyboard)

        elif call.data.startswith("page_"):
            page_number = int(call.data.split("_")[1])
            user = BotUser.objects.get(chat_id=chat_id)
            district_id = user.selected_district_id
            quarters = Quarter.objects.filter(district_id=district_id)
            total_pages = (quarters.count() // names_per_page) + ((quarters.count() % names_per_page) > 0)
            keyboard = quarter_buttons_uz(page_number, total_pages, quarters)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)


        elif call.data.startswith("quarter_id_"):
            user = BotUser.objects.get_or_create(chat_id=chat_id)[0]
            quarter_id = int(call.data.split("_")[2])
            quarter = Quarter.objects.get(pk=quarter_id)
            user.quarter = quarter
            user.user_state = "wait_adress"
            user.save()
            if current_language == 'UZ':
                photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(chat_id, photo, "Mas'ul xodimlar siz bilan bog'lanishi uchun aniq yashash manzilingizni ko'rsating.")
            elif current_language == 'RU':
                photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
                with open(photo_path, 'rb') as photo:
                    bot.send_photo(chat_id, photo, "Укажите свой точный адрес проживания, чтобы ответственный персонал мог связаться с вами.")
       
    elif current_state == "wait_interest":
        user = BotUser.objects.get(chat_id=chat_id)
        interest_id = call.data.split('_')[1]
        interest = Interest.objects.get(pk=interest_id)
        user.interest = interest
        user.user_state = "wait_education"
        user.save()
        interest.save()
        if current_language == 'UZ':
            bot.send_message(chat_id, "Qayerda o'qishni hohlaysiz", reply_markup=education_keyboard(interest_id))
        elif current_language == 'RU':
            bot.send_message(chat_id, "Где вы хотите учиться?", reply_markup=education_keyboard(interest_id))

    elif current_state == "wait_education":
        user = BotUser.objects.get(chat_id=chat_id)
        education_id = call.data.split('_')[1]
        education = Education.objects.get(pk=education_id)
        user.education = education
        user.user_state = "wait_category"
        user.save()
        education.save()
        if current_language == 'UZ':
            bot.send_message(chat_id, "Qaysi yo'nalishda o'qishni hohlaysiz", reply_markup=category_keyboard_uz(education_id))
        elif current_language == 'RU':
            bot.send_message(chat_id, "В каком направлении вы хотите учиться", reply_markup=category_keyboard_ru(education_id))

    elif current_state == "wait_category":
        user = BotUser.objects.get(chat_id=chat_id)
        category_id = call.data.split('_')[1]
        category = Category.objects.get(pk=category_id)
        user.category = category
        user.user_state = "wait_course"
        user.save()
        category.save()
        if current_language == 'UZ':
            bot.send_message(chat_id, "qaysi kursda o'qishni hohlaysiz", reply_markup=course_keyboard_uz(category_id))
        elif current_language == 'RU':
            bot.send_message(chat_id, "какой курс вы хотите изучать", reply_markup=course_keyboard_ru(category_id))



    elif current_state == "wait_course":
        user = BotUser.objects.get(chat_id=chat_id)
        course_id = call.data.split('_')[1]
        course = Course.objects.get(pk=course_id)
        user.course = course
        user.user_state = "wait_problems"
        user.save()
        course.save()
        if current_language == 'UZ':
            bot.send_message(chat_id, "sizda ushbu kurda o'qish uchun qanday muamolar mavjud?", reply_markup=problem_keyboard_uz())
        elif current_language == 'RU':
            bot.send_message(chat_id, "Какие проблемы вам предстоит изучить на этом курсе?", reply_markup=problem_keyboard_ru())

    elif current_state == "wait_problems":
        user = BotUser.objects.get(chat_id=chat_id)
        problem_id = call.data.split('_')[1]
        problem = Problem.objects.get(pk=problem_id)
        user.problem = problem
        user.save()
        problem.save()
        if current_language == 'UZ':
            bot.send_message(chat_id, "tugadi")
        elif current_language == 'RU':
            bot.send_message(chat_id, "end")


    elif current_state == "wait_conifrim":
        if call.data == "confirm_uz":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_second_number"
            user.save()
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg') 
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "iltimos ikkinchi raqamingizni kiriting",reply_markup=ReplyKeyboardRemove(selective=False))


        elif call.data == "confirm_ru":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_second_number"
            user.save()
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg') 
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "видети ваш второй номер", reply_markup=ReplyKeyboardRemove(selective=False))


        elif call.data == "cancel_uz":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_fullname"
            user.save()
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "Iltimos, familiyangizni, ismingizni va otangizning ismini (to'liq) ko'rsating.",reply_markup=ReplyKeyboardRemove(selective=False))

        elif call.data == "cancel_ru":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_fullname"
            user.save()
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "Пожалуйста, укажите свою фамилию, имя и отчество (полностью).",reply_markup=ReplyKeyboardRemove(selective=False))




@bot.message_handler(func=lambda message: True, content_types=['contact'])
def conifrim_phone(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    user = BotUser.objects.get(chat_id=chat_id)
    user.phone_number = phone_number
    current_language = user.user_lang
    user.user_state = "wait_conifrim"
    user.save()
    if current_language == 'UZ':
        bot.send_message(chat_id,"Sizda ikkinchi raqam mavjudmi?",reply_markup=confirm_uz())
    elif current_language == 'RU':
        bot.send_message(chat_id,"у вас ест второй номер?",reply_markup=confirm_ru())

@bot.message_handler(func=lambda message: True, content_types=['text'])
def messages(message):
    chat_id = message.chat.id
    user = BotUser.objects.get(chat_id=chat_id)
    current_state = user.user_state
    current_language = user.user_lang
    user.save()

    if current_state == "wait_second_number":
        user = BotUser.objects.get(chat_id=chat_id)
        user.phone_number = message.text
        user.user_state="wait_fullname"
        user.save()

        if current_language == "UZ":
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                # bot.send_photo(chat_id, photo, "itimos tuman yoki shaharni tanlang",reply_markup=district_keyboard_uz(region_id))
                bot.send_photo(chat_id,photo, "Iltimos, familiyangizni, ismingizni va otangizning ismini (to'liq) ko'rsating. ")

        elif current_language == "RU":
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "Пожалуйста, укажите свою фамилию, имя и отчество (полностью).")

    elif current_state == "wait_fullname":
        user = BotUser.objects.get(chat_id=chat_id)
        user.full_name = message.text
        user.user_state = "wait_age"
        user.save()

        if current_language == "UZ":
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "Yoshingiz nechida? Bu bizga ma'lumotlarimizni sizning ehtiyojlaringizga moslashtirishga yordam beradi.",reply_markup=ReplyKeyboardRemove(selective=False))
        elif current_language == "RU":
            photo_path = os.path.join(settings.BASE_DIR, 'media', 'photos', 'astrum.jpg')  # Construct the path to the image
            with open(photo_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, "Сколько тебе лет? Это помогает нам адаптировать нашу информацию к вашим потребностям.",reply_markup=ReplyKeyboardRemove(selective=False))

    elif current_state == "wait_age":
        user = BotUser.objects.get(chat_id=chat_id)
        user.age = message.text
        user.user_state = "wait_region"
        user.save()
        if current_language == "UZ":
            bot.send_message(chat_id, "o'z regionigizni tanlang",reply_markup=region_keyboard_uz())
        elif current_language == "RU":
            bot.send_message(chat_id, "o'z regionigizni tanlang Ru",reply_markup=region_keyboard_ru())


    elif current_state == "wait_adress":
        user = BotUser.objects.get(chat_id=chat_id)
        user.adress=message.text
        user.user_state = "wait_interest"
        user.save()
        if current_language == "UZ":
            bot.send_message(chat_id, "Qaysi soha sizni ko'proq qiziqtiradi? Bir yoki bir nechta variantni tanlang: ", reply_markup=interest_keyboard_uz())
        elif current_language == "RU":
            bot.send_message(chat_id, "Какая сфера вас интересует больше всего? Выберите один или несколько вариантов:", reply_markup=interest_keyboard_ru())

            
bot.polling(none_stop=True)





