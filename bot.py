import telebot
from telebot import types
from search_recipe import search


TOKEN = "5170186949:AAF2qfgd846wZRb2VFV0R9krT2jLtmFod14"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

count = 0

keyboard = types.InlineKeyboardMarkup()
button_like = types.InlineKeyboardButton(text=b'\xF0\x9F\x91\x8D'.decode('UTF-8'), callback_data='Да')
keyboard.add(button_like)
button_dislike = types.InlineKeyboardButton(text=b'\xF0\x9F\x91\x8E'.decode('UTF-8'), callback_data='Нет')
keyboard.add(button_dislike)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Привет! Напиши продукты - я подберу рецепт.\
    """)


@bot.message_handler(func=lambda m: True)
def get_products(message, *args):
    global recipes
    # global count
    # recipes = search(message.text.replace(",", "").split())
    global count
    # count = 0
    if len(args) != 0:
        count += 1
    else:
        recipes = search(message.text.replace(",", "").split())
    # print(recipes)
    # schet = 0
    try:
        mess = f"<b>Название</b>: \n{recipes[count][0]}\n<b>Ингредиенты</b>: \n{recipes[count][2]}\n<b>Рецепт</b>: \n{recipes[count][1]}"
        if len(mess) > 4096:
            for x in range(0, len(mess), 4095):
                if x >= 4095:
                    bot.send_message(message.chat.id, text=mess[x:x + 4095], parse_mode="HTML", reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, text=mess[x:x + 4095], parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, text=mess, parse_mode="HTML", reply_markup=keyboard)

    except IndexError:
        list_out = "По данным ингредиентам рецептов больше нет {}".format(b'\xF0\x9F\x92\xA9'.decode("UTF-8"))
        bot.send_message(message.chat.id, list_out)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    if call.data == "Нет":
        get_products(call.message, 1)
    else:
        like_mess = "Хороший выбор! Приятного аппетита! {}".format(b'\xF0\x9F\x91\xBB'.decode("UTF-8"))
        bot.send_message(call.message.chat.id, like_mess)


bot.infinity_polling()
