import telebot
from botapp.models import BotUser
from .button import *
from telebot.types import ReplyKeyboardRemove
from common.models import Region, District, Quarter
TOKEN = '6584674642:AAG_7MIMMrBiuD_smtd3aJMsofEoCMEXRVk'
bot = telebot.TeleBot(TOKEN)

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
        user = BotUser.objects.get(chat_id=chat_id)
        quarter_id = call.data.split('_')[1]
        quarter = Quarter.objects.get(pk=quarter_id)
        user.quarter = quarter
        user.user_state = "wait_adress"
        user.save()
        quarter.save()
        if current_language  == 'UZ':
            bot.send_message(chat_id, "itimos o'z adresingizni kiriting")
        elif current_language == 'RU':
            bot.send_message(chat_id, "Пожалуйста, введите ваш адрес")
            


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
        user.save()

        if current_language == "UZ":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state="wait_fullname"
            user.save()
            bot.send_message(chat_id, "Ism familya sharifni kiriting",reply_markup=ReplyKeyboardRemove(selective=False))

        elif current_language == "RU":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state="wait_fullname"
            user.save()
            bot.send_message(chat_id, "iltimos ism familya sharifingizni RU",reply_markup=ReplyKeyboardRemove(selective=False))

    elif current_state == "wait_fullname":
        user = BotUser.objects.get(chat_id=chat_id)
        user.full_name = message.text
        user.save()

        if current_language == "UZ":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_region"
            user.save()
            bot.send_message(chat_id, "o'z regionigizni tanlang",reply_markup=region_keyboard_uz())
        elif current_language == "RU":
            user = BotUser.objects.get(chat_id=chat_id)
            user.user_state = "wait_region"
            user.save()
            bot.send_message(chat_id, "regioningizni tanlang RU", reply_markup=region_keyboard_ru())

bot.polling(none_stop=True)