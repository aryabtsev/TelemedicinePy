import pymysql
import datetime
import matplotlib.pyplot as plt
import time
import os

class DataB:

    def __init__(self):
        self.connection = pymysql.connect(host = "173.230.151.37", port = 3306,  user = "root", passwd = "BMT4Ever", database = "mydb")
        self.cursor = self.connection.cursor()


    def select_average_hr(self):
        # получаем среднее сердцебиение
        with self.connection:
            return self.cursor.execute('SELECT AVG(Heart_rate) FROM Telemedicine')


    def select_average_br(self):
        # получаем среднее дыхание
        with self.connection:
            return self.cursor.execute('SELECT AVG(Breath_rate) FROM Telemedicine')


    def select_day_hr(self):
         # получаем чсс за день
        date_input = datetime.date.isoformat(datetime.date.today())
        query = str('SELECT Heart_rate FROM Telemedicine WHERE date == %s' % date_input)

        with self.connection:
            return self.cursor.execute(query)

    def select_day_br(self):
        # получаем чд за день
        date_input = datetime.date.isoformat(datetime.date.today())
        query = str('SELECT Breath_rate FROM Telemedicine WHERE date == %s' % date_input)

        with self.connection:
            return self.cursor.execute(query)

    def _get_current_data(self):
        data_to_send = time.strftime('%Y-%m-%d')
        return data_to_send

    def select_daily(self, what, data_to_send):
        #what == 'time' or 'heart_rate'
        data_to_send = [time.strftime('%Y-%m-%d')]
        cursor = self.connection.cursor()
        sql = ("SELECT " + what + " FROM Telemedicine WHERE date=%s")
        cursor.execute(sql, data_to_send)
        received_data = []
        for result in cursor:
            received_data.append(result)
        return received_data

    def save_daily_plot(self, times, heart_rates, date, signal):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(times, heart_rates, 'r')
        ax.grid(True)
        ax.set_ylabel('Значение %s, уд/мин' %signal)
        ax.set_xlabel('Времена измерений %s' %signal)
        ax.set_title('Изменение %s за '%signal + date)
        # plt.show()

        if not os.path.exists('daily_plots/'):
            os.mkdir('daily_plots')
        plot_name = 'daily_plots/' + date + '.png'
        fig.savefig(plot_name, fmt='png')
        return plot_name

    def get_daily_plot(self,signal,query):
        current_data = self._get_current_data()
        times = self.select_daily('time', [current_data])
        for i in range(len(times)):
            times[i] = times[i][0].seconds

        query_rates = self.select_daily(query, [current_data])
        for i in range(len(query_rates)):
            query_rates[i] = query_rates[i][0]

        plot_name = self.save_daily_plot(times, query_rates, current_data, signal)
        return plot_name


    def last_value(self, signal):
        with self.connection:
                cursor = self.cursor
            # sql = ("SELECT heart_rate FROM Telemedicine WHERE date=SELECT MAX(date) FROM Telemedicine")
                sql = ("SELECT MAX(date) FROM Telemedicine ")
                cursor.execute(sql)
                received_data = []
                for result in cursor:
                    received_data.append(result)
                print(received_data)

                sql = ("SELECT MAX(time) FROM Telemedicine WHERE date=%s")
                date_to_look_for = received_data[0]
                cursor.execute(sql, date_to_look_for)
                received_data = []
                for result in cursor:
                    received_data.append(result)
                print(received_data)
                if signal == 'heart_rate':
                    sql = ("SELECT heart_rate FROM Telemedicine WHERE date=%s AND time=%s")
                elif signal == 'breath_rate':
                    sql = ("SELECT breath_rate FROM Telemedicine WHERE date=%s AND time=%s")
                time_to_look_for = received_data[0]
                date = date_to_look_for[0]
                time_rec = time_to_look_for[0]

                date_to_send = [date.strftime('%Y-%m-%d'), time_rec]

                cursor.execute(sql, date_to_send)
                received_data = []
                for result in cursor:
                    received_data.append(result)
                result = received_data[0][0]
                print(result)
                return result





    def close(self):
        # Закрываем текущее соединение с БД
        self.connection.close()