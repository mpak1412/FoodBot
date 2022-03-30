import telebot
from telebot import types
from search_recipe import search


TOKEN = "5170186949:AAF2qfgd846wZRb2VFV0R9krT2jLtmFod14"
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Привет! Напиши продукты - я подберу рецепт.\
    """)


@bot.message_handler(func=lambda m: True)
def get_products(message):
    recipes = search(message.text.replace(",", "").split())
    print(recipes)
    for i in range(len(recipes)):
        mess = f"*Название*: \n{recipes[i][0]}\n*Ингредиенты*: \n{recipes[i][2]}\n*Рецепт*: \n{recipes[i][1]}"
        if len(mess) > 4096:
            for x in range(0, len(mess), 4095):
                bot.reply_to(message, text=mess[x:x + 4095], parse_mode="Markdown")
        else:
            bot.reply_to(message, mess, parse_mode="Markdown")
    # keyboard = types.InlineKeyboardMarkup()
    # button_like = types.InlineKeyboardButton(text='Да', callback_data='Да')
    # keyboard.add(button_like)
    # button_dislike = types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    # keyboard.add(button_dislike)
    # bot.send_message(message.chat.id, 'buttons', reply_markup=keyboard)


bot.infinity_polling()
