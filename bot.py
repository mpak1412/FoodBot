import telebot


TOKEN = "5170186949:AAF2qfgd846wZRb2VFV0R9krT2jLtmFod14"
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Привет! Напиши продукты - я подберу рецепт.\
    """)


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

@bot.message_handler(func=lambda m: True)
def get_products(message):
    mess = message.text.replace(",", "").split()
    print(mess)
    # bot.reply_to(message, mess)




bot.infinity_polling()
