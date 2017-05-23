import pymysql
import datetime
import time
import matplotlib.pyplot as plt
import os

class DataB:

    def __init__(self, host, port, user, pswd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.db = db
        self.connection = None
        pass

    def connect_to_db(self):
        try:
            self.connection = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.pswd, db = self.db)
            self.cursor = self.connection.cursor()
        except pymysql.Error as e:
            raise e

    def select_average_hr(self):
        # получаем среднее сердцебиение
        with self.connection:
            return self.cursor.execute('SELECT AVG(Heart_rate) FROM Telemedicine')

    def select_average_br(self):
        # получаем среднее дыхание
        with self.connection:
            return self.cursor.execute('SELECT AVG(Breath_rate) FROM Telemedicine')

    def get_current_data(self):
        data_to_send = time.strftime('%Y-%m-%d')
        print(data_to_send)
        return data_to_send

    def select_daily(self, what, data_to_send):
        #what == 'time' or 'heart_rate' or 'breath_rate'

        sql = ("SELECT " + what + " FROM Telemedicine WHERE date=%s")
        self.cursor.execute(sql, data_to_send)
        received_data = []
        for result in self.cursor:
            received_data.append(result)
        return received_data

    def save_daily_plot(self, times, heart_rates, date):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(times, heart_rates, 'r')
        ax.grid(True)
        ax.set_ylabel('Значение ЧСС, уд/мин')
        ax.set_xlabel('Время измерения, ч')
        ax.set_title('Изменение ЧСС за ' + date)
        plt.show()

        if not os.path.exists('daily_plots/'):
            os.mkdir('daily_plots')
        plot_name = 'daily_plots/' + date + '.png'
        fig.savefig(plot_name, fmt='png')
        return plot_name

    def _make_time(self, timedelta):
        hours = timedelta.seconds // 3600
        minutes = (timedelta.seconds - hours * 3600) // 60
        seconds = timedelta.seconds - hours * 3600 - minutes * 60
        result = hours + (minutes / 60) + (seconds / 3600)
        return result

    def make_daily_plot(self):
        current_data = self.get_current_data()

        #!!!!!!!!!!!!!!!!!
        current_data = '2017-05-22'
        #!!!!!!!!!!!!!!!!!!!!

        times = self.select_daily('time', [current_data])
        for i in range(len(times)):
            times[i] = self._make_time(times[i][0])

        heart_rates = self.select_daily('heart_rate', [current_data])
        for i in range(len(heart_rates)):
            heart_rates[i] = heart_rates[i][0]

        plot_name = self.save_daily_plot(times, heart_rates, current_data)
        return plot_name

    def close(self):
        # Закрываем текущее соединение с БД
        self.connection.close()


writer = DataB("173.230.151.37", 3306, "root", "BMT4Ever", "mydb")
writer.connect_to_db()
plot_name = writer.make_daily_plot()
