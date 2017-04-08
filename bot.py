import telebot
import config
from DataB import DataB as DB
from telebot import types

bot = telebot.TeleBot(config.token)
markup = types.ReplyKeyboardMarkup()
#markup.row('Heart_rate', 'Breath_rate')



@bot.message_handler(commands=['start'])
def start(message):
    # Подключаемся к БД
    #db_worker = DB(config.database_name)

    # Формируем разметку клавиатуры
    markup.row('/Heart_rate', '/Breath_rate')

    # Вывод предложения
    bot.send_message(message.chat.id, text = "Выберите, что вы хотите запросить:", reply_markup=markup)

    # Отсоединяемся от БД
    #db_worker.close()

@bot.message_handler(commands=['Heart_rate'])
def hr_request(message):
    # Подключаемся к БД
    db_worker = DB(config.database_name)
    # Вытягивание из БД среднего ЧСС
    heart_rate = DB.select_average_hr(db_worker)


    bot.send_message(message.chat.id, text = (f'Среднее значение ЧСС за все время измерений = {heart_rate}'))
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['Breath_rate'])
def hr_request(message):
    # Подключаемся к БД
    db_worker = DB(config.database_name)
    # Вытягивание из БД среднего ЧСС
    breath_rate = DB.select_average_br(db_worker)
    # Отсоединяемся от БД
    db_worker.close()

    bot.send_message(message.chat.id, text = (f'Среднее значение ЧД за все время измерений = {breath_rate}'))






if __name__ == '__main__':

    bot.polling(none_stop=True)