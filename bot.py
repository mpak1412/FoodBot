import telebot
from telebot import types
from search_recipe import search
from core.settings import Settings
from morphy import morphy
import flask

settings = Settings()
WEBHOOK_URL_BASE = "https://{}:{}".format(settings.WEBHOOK_HOST, str(settings.WEBHOOK_PORT))
WEBHOOK_URL_PATH = "/{}/".format(settings.bot_token)


bot = telebot.TeleBot(settings.bot_token, parse_mode=None, threaded=False)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

count = 0

keyboard = types.InlineKeyboardMarkup()
button_like = types.InlineKeyboardButton(text=b'\xF0\x9F\x91\x8D'.decode('UTF-8'), callback_data='Да')
keyboard.add(button_like)
button_dislike = types.InlineKeyboardButton(text=b'\xF0\x9F\x91\x8E'.decode('UTF-8'), callback_data='Нет')
keyboard.add(button_dislike)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
    Привет! Я бот, который поможет тебе найти рецепт под ингредиенты, которые есть у тебя под рукой! Отправь мне продукты, а я подберу рецепт :).\
    """)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, """\
    Чтобы начать подбор рецептов, необходимо отправить мне ингредиенты в сообщении.\n \
    Если оценить рецепт кнопкой {}, то я буду подбирать новые рецепты под ваши запросы до тех пор, пока рецепты не закончатся.\n \
    Если оценить рецепт кнопкой {}, то я перестану подбирать рецепты  и пожелаю приятного аппетита!\
    """.format(b'\xF0\x9F\x91\x8E'.decode("UTF-8"), b'\xF0\x9F\x91\x8D'.decode("UTF-8")))


@bot.message_handler(func=lambda m: True)
def get_products(message, *args):
    global recipes
    global count
    if len(args) != 0:
        count += 1
    else:
        morphy_text = morphy(message.text.replace(",", "").split())
        recipes = search(morphy_text)
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


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


app.run(host=settings.WEBHOOK_HOST,
        port=settings.WEBHOOK_PORT,
        debug=True)

# if __name__ == "__main__":
#     bot.infinity_polling()
