import telebot
from botapp.models import BotUsers 

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    nickname = message.from_user.username

    # Check if user already exists
    user, created = BotUsers.objects.get_or_create(
        chat_id=chat_id,
        defaults={'nickname': nickname}
    )

    if created:
        bot.send_message(chat_id, "Welcome! Your information has been saved.")
    else:
        bot.send_message(chat_id, "Welcome back! You are already registered.")

bot.polling(none_stop=True)
