import telebot
from doctor import Doctors
from telebot import types
import cherrypy

from DataB import DataB as DB
import config

WEBHOOK_HOST = '173.230.151.37'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '../webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '../webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
markup_auth = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_auth.row('Авторизация')
markup.row('Частота сердцебиения', 'Частота дыхания')
markup.row('График ЧСС', 'График ЧД')
# markup.row('Heart_rate', 'Breath_rate')
users = {}


# def check_user(id):
#     if id not in users:
#         current_user = Doctors(id)
#         users[id] = current_user
#         return current_user


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(regexp="/Start|/START|/start")
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Отправьте /auth для авторизации и начала работы :)",
                 reply_markup=markup_auth)


@bot.message_handler(regexp='/auth|/Auth|/Авторизация|Авторизация')
def subscribe_chat(message):
    if message.chat.id in users:
        bot.send_message(message.chat.id, "Вы уже авторизованы:)")
    else:
        sent = bot.send_message(message.chat.id, "Введите пароль:")
        bot.register_next_step_handler(sent, authorization)  # перебрасываем следующее сообщение в функцию авторизации


def authorization(message):
    if message.text == "25052015":
        bot.send_message(message.chat.id, text="Авторизация успешна")
        users[message.chat.id] = Doctors(message.chat.id)
        print("Залогинился" + message.from_user)
        bot.send_message(message.chat.id, text="Выберите, что вы хотите запросить:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Неверный пароль")


# def check(message):
#     if message.chat.id in users:
#         pass
#     else:
#         bot.send_message(message.chat.id, text = "Вы не авторизованы. Для начала авторизуйтесь отправив /auth")










@bot.message_handler(regexp='Heart_rate|/Heart_rate|Частота сердцебиения|/Частота сердцебиения')
def hr_request(message):
    if message.chat.id in users:
        # Подключаемся к БД
        db_worker = DB()
        # Вытягивание из БД среднего ЧСС
        heart_rate = DB.last_value(db_worker, signal='heart_rate')

        # bot.send_message(message.chat.id, text=" Блаблаблабла", reply_markup=markup)
        bot.send_message(message.chat.id, text=('Последнее измерение ЧСС = %d' % heart_rate))
        # Отсоединяемся от БД
        db_worker.close()
    else:
        bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


@bot.message_handler(regexp='Breath_rate|/Breath_rate|Частота дыхания|/Частота дыхания')
def hr_request(message):
    if message.chat.id in users:
        # Подключаемся к БД
        db_worker = DB()
        # Вытягивание из БД среднего ЧСС
        breath_rate = DB.last_value(db_worker, signal='breath_rate')
        # Отсоединяемся от БД
        db_worker.close()

        bot.send_message(message.chat.id, text=('Последнее измерение ЧД =  %d' % breath_rate))
    else:
        bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


@bot.message_handler(regexp='ЧСС за день|/Day_hr|График ЧСС')
def day_hr_request(message):
    if message.chat.id in users:
        # Подключаемся к БД
        db_worker = DB()
        # Вытягивание из БД среднего ЧСС
        heart_rate = DB.get_daily_plot(db_worker, 'ЧСС', 'heart_rate')
        # Отсоединяемся от БД
        db_worker.close()

        bot.send_photo(message.chat.id, open(heart_rate, 'rb'))
    else:
        bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


@bot.message_handler(regexp='/Day_br|/График ЧД|График ЧД')
def day_hr_request(message):
    if message.chat.id in users:
        # Подключаемся к БД
        db_worker = DB()
        # Вытягивание из БД среднего ЧСС
        breath_rate = DB.get_daily_plot(db_worker, 'ЧД', 'breath_rate')
        # Отсоединяемся от БД
        db_worker.close()

        bot.send_photo(message.chat.id, open(breath_rate, 'rb'))
    else:
        bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


def check_alarm():
    db_worker = DB()
    result = DB.last_value(db_worker, signal='heart_rate')
    if result < 40:
        bot.send_message(users, text="Внимание, частота сердечных сокращений упала до %d" % result)


@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def answer_all_other(message):
    bot.send_message(message.chat.id,
                     text="Авторизуйтесь /auth или если уже, введите, пожалуйста, одну из команд: /Heart_rate или /Breath_rate",
                     reply_markup=markup)


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

# if __name__ == '__main__':
#
#     bot.polling(none_stop=True)

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
