import telebot
from doctor import Doctors
from telebot import types
import cherrypy
from telegramcalendar import create_calendar
import datetime


from DataB import DataB as DB
import config

global date
date = ""



bot = telebot.TeleBot(config.token)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
markup_auth = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_choose = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_auth.row('Авторизация')
markup.row('Частота сердцебиения', 'Частота дыхания')
markup.row('Получить показания за день')
markup_choose.row('ЧСС за день', 'ЧД за день')

# markup.row('Heart_rate', 'Breath_rate')
users = {}
current_shown_dates={}

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

def authorization(message):
    if message.text == "25052015":
        bot.send_message(message.chat.id, text="Авторизация успешна")
        users[message.chat.id] = Doctors(message.chat.id)
       # print("Залогинился" + message.from_user)
        bot.send_message(message.chat.id, text="Выберите, что вы хотите запросить:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Неверный пароль")


@bot.message_handler(regexp='/auth|/Auth|/Авторизация|Авторизация')
def subscribe_chat(message):
    if message.chat.id in users:
        bot.send_message(message.chat.id, "Вы уже авторизованы:)")
        bot.send_message(message.chat.id, text="Выберите, что вы хотите запросить:", reply_markup=markup)
    else:
        sent = bot.send_message(message.chat.id, "Введите пароль:")
        bot.register_next_step_handler(sent, authorization)  # перебрасываем следующее сообщение в функцию авторизации






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




@bot.message_handler(regexp='Получить показания за день|/Get_day_line')
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Выберите дату", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'След. месяц')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Выберите дату", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'Пред. месяц')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Выберите дату", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass



@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    print(saved_date)
    if(saved_date is not None):
        day=call.data[13:]
        print(day)
        global date
        date = datetime.date(int(saved_date[0]),int(saved_date[1]),int(day))
        date = str(date.isoformat())
        #bot.answer_callback_query(call.id, text="")
        sent = bot.send_message(call.message.chat.id, text="Выберите, какие показания Вы хотите получить за %s" % date,
                                reply_markup=markup_choose)
        bot.register_next_step_handler(sent, choose)
    else:
        #Do something to inform of the error
        pass

def choose(message):
    if message.text == ('ЧСС за день'):
        global date
        db_worker = DB()
        heart_rate = DB.get_daily_plot(db_worker, 'ЧСС', 'heart_rate', date)
        # Отсоединяемся от БД
        db_worker.close()

        bot.send_photo(message.chat.id, open(heart_rate, 'rb'))
        bot.send_message(message.chat.id, text="Выберите новый запрос", reply_markup=markup)
    elif message.text == ('ЧД за день'):

        db_worker = DB()
        breath_rate = DB.get_daily_plot(db_worker, 'ЧД', 'breath_rate', date)

        # Отсоединяемся от БД
        db_worker.close()
        bot.send_photo(message.chat.id, open(breath_rate, 'rb'))
        bot.send_message(message.chat.id, text="Выберите новый запрос", reply_markup=markup)
    else: bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


# @bot.message_handler(regexp='Получить показания за день')
# def idk(message):
#     if message.chat.id in users:
#         date = None
#         get_calendar(message)
#
#         while date == None:
#             date = get_day(func=lambda call: call.data[0:13] == 'calendar-day-')
#
#         print('yo')
#         sent = bot.send_message(message.chat.id, text="Выберите, какие показания Вы хотите получить за %s" %date, reply_markup=markup_choose)
#         bot.register_next_step_handler(sent, choose)
#     else:
#         bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")




# @bot.message_handler(regexp='ЧСС за день|/Day_hr|График ЧСС')
# def day_hr_request(message):
#     if message.chat.id in users:
#         # Подключаемся к БД
#         get_calendar(message)
#         date = get_day()
#
#         if date:
#             db_worker = DB()
#             # Вытягивание из БД среднего ЧСС
#             heart_rate = DB.get_daily_plot(db_worker, 'ЧСС', 'heart_rate', date = date)
#             # Отсоединяемся от БД
#             db_worker.close()
#
#             bot.send_photo(message.chat.id, open(heart_rate, 'rb'))
#     else:
#         bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")
#
#
# @bot.message_handler(regexp='/Day_br|/График ЧД|График ЧД')
# def day_hr_request(message):
#     if message.chat.id in users:
#         # Подключаемся к БД
#         db_worker = DB()
#         # Вытягивание из БД среднего ЧСС
#         breath_rate = DB.get_daily_plot(db_worker, 'ЧД', 'breath_rate')
#         # Отсоединяемся от БД
#         db_worker.close()
#
#         bot.send_photo(message.chat.id, open(breath_rate, 'rb'))
#     else:
#         bot.send_message(message.chat.id, text="Вы не авторизованы. Для начала авторизуйтесь отправив /auth")


def check_alarm():
    db_worker = DB()
    result = DB.last_value(db_worker, signal='heart_rate')
    if result < 40:
        bot.send_message(users, text="Внимание, частота сердечных сокращений упала до %d" % result)


@bot.message_handler(regexp="25052015|ЧД за день|ЧСС за день")
def crutch(message):
    pass

@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def answer_all_other(message):
    bot.send_message(message.chat.id,
                     text="Авторизуйтесь /auth или если уже, введите, пожалуйста, одну из команд: /Heart_rate, /Breath_rate или /Get_day_line",
                     reply_markup=markup)


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

#Ставим заново вебхук
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

#Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

# if __name__ == '__main__':
#
#     bot.polling(none_stop=True)

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
