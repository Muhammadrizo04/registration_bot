import telebot
from botapp.models import BotUser
from .button import *
from telebot.types import ReplyKeyboardRemove
from common.models import Region, District, Quarter
TOKEN = '6584674642:AAG_7MIMMrBiuD_smtd3aJMsofEoCMEXRVk'
bot = telebot.TeleBot(TOKEN)

selected_regions = {}
names_per_page = 10
selected_region_id = None  

############################# quarter filter button #########################################

def create_pagination_buttons(page_number, total_pages, names_queryset):
    keyboard = types.InlineKeyboardMarkup()

    # Fetch names for the current page from the queryset
    names_and_ids = [(quarter.name, quarter.id) for quarter in names_queryset[(page_number - 1) * names_per_page:page_number * names_per_page]]

    # Add names buttons
    for name, quarter_id in names_and_ids:
        button_text = str(name)  # Convert to string to be safe
        button = types.InlineKeyboardButton(button_text, callback_data=f"quarter_id_{quarter_id}")
        keyboard.add(button)


    # Add pagination buttons
    if page_number > 1:
        keyboard.add(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{page_number - 1}"))
    if page_number < total_pages:
        keyboard.add(types.InlineKeyboardButton("Next ➡️", callback_data=f"page_{page_number + 1}"))

    return keyboard

############################# quarter filter button #########################################

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    nick_name = message.chat.first_name
    try:
        user = BotUser.objects.get(chat_id=chat_id)
        bot.send_message(chat_id, "Ro'yxatga oluvchi botimizga hush kelibsiz", reply_markup=languages())
    except BotUser.DoesNotExist:
        BotUser.objects.create(
            chat_id=chat_id,
            nick_name=nick_name,

        )
        bot.send_message(chat_id, "Ro'yxatga oluvchi botimizga hush kelibsiz", reply_markup=languages())

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
        bot.send_message(chat_id, "Iltimos telefon raqamingizni yuboring", reply_markup=contacts_uz())

    elif call.data == "ru":
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_lang = 'RU'
        user.user_state = "wait_phone"
        user.save()
        bot.send_message(chat_id, "Пожалуйста, поделитесь своим номером телефона", reply_markup=contacts_ru())
    
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
        user.user_state = "wait_quarter"
        user.save()
        district.save()
        if current_language  == 'UZ':
            bot.send_message(chat_id, "itimos o'z mfyigizni tanlang", reply_markup=quarter_keyboard_uz(district_id))
        elif current_language == 'RU':
            bot.send_message(chat_id, "выберите общественное собрание вашего района", reply_markup=quarter_keyboard_ru(district_id))
       
    
    elif current_state == "wait_quarter":
        if call.data.startswith("district_"):
            selected_region_id = call.data.split("_")[1]
            selected_regions[chat_id] = selected_region_id  # Store selected region for this user
            quarters = Quarter.objects.filter(district_id=selected_region_id)
            total_pages = (quarters.count() // names_per_page) + ((quarters.count() % names_per_page) > 0)
            page_number = 1
            keyboard = create_pagination_buttons(page_number, total_pages, quarters)
            bot.edit_message_text("Choose a quarter:", chat_id, call.message.message_id, reply_markup=keyboard)

        elif call.data.startswith("page_"):
            page_number = int(call.data.split("_")[1])
            selected_region_id = selected_regions.get(chat_id)  # Retrieve the stored selected region for this user
            if selected_region_id:
                quarters = Quarter.objects.filter(district_id=selected_region_id)
                total_pages = (quarters.count() // names_per_page) + ((quarters.count() % names_per_page) > 0)
                keyboard = create_pagination_buttons(page_number, total_pages, quarters)
                bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=keyboard)

        elif call.data.startswith("quarter_id_"):
            user = BotUser.objects.get_or_create(chat_id=chat_id)[0]
            quarter_id = int(call.data.split("_")[2])
            quarter = Quarter.objects.get(pk=quarter_id)
            user.quarter = quarter
            user.user_state = "wait_adress"
            user.save()
            bot.send_message(chat_id, f"iltimos adresingizni kiting")
            


@bot.message_handler(func=lambda message: True, content_types=['contact'])
def conifrim_phone(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    user = BotUser.objects.get(chat_id=chat_id)
    user.phone_number = phone_number
    current_language = user.user_lang
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

    if message.text == "Ha✅":
        bot.send_message(chat_id, "iltimos ikkinchi raqamingizni kiriting",reply_markup=ReplyKeyboardRemove(selective=False))
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_state = "wait_second_number"
        user.save()

    elif message.text == "Да✅":
        bot.send_message(chat_id, "видети ваш второй номер", reply_markup=ReplyKeyboardRemove(selective=False))
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_state = "wait_second_number"
        user.save()

    elif message.text == "Yo'q❌":
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_state = "wait_fullname"
        user.save()
        bot.send_message(chat_id, "ismingizni kiriting",reply_markup=ReplyKeyboardRemove(selective=False))

    elif message.text == "Нет❌":
        user = BotUser.objects.get(chat_id=chat_id)
        user.user_state = "wait_fullname"
        user.save()
        bot.send_message(chat_id, "ismingizni kiriting RU",reply_markup=ReplyKeyboardRemove(selective=False))

    elif current_state == "wait_second_number":
        user = BotUser.objects.get(chat_id=chat_id)
        user.phone_number = message.text
        user.user_state="wait_fullname"
        user.save()

        if current_language == "UZ":
            bot.send_message(chat_id, "Ism familya sharifni kiriting",reply_markup=ReplyKeyboardRemove(selective=False))

        elif current_language == "RU":
            bot.send_message(chat_id, "iltimos ism familya sharifingizni RU",reply_markup=ReplyKeyboardRemove(selective=False))

    elif current_state == "wait_fullname":
        user = BotUser.objects.get(chat_id=chat_id)
        user.full_name = message.text
        user.user_state = "wait_region"
        user.save()

        if current_language == "UZ":
            bot.send_message(chat_id, "o'z regionigizni tanlang",reply_markup=region_keyboard_uz())
        elif current_language == "RU":
            bot.send_message(chat_id, "regioningizni tanlang RU", reply_markup=region_keyboard_ru())

        
    elif current_state == "wait_adress":
        user = BotUser.objects.get(chat_id=chat_id)
        user.adress=message.text
        user.user_state = "wait_interest"
        user.save()
        bot.send_message(chat_id, "o'z qiziqishlaringizni tanlang")

bot.polling(none_stop=True)





