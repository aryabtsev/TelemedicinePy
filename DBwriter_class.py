import matplotlib.pyplot as plt
import MySQLdb
import time
import os


class DbWriter:
    def __init__(self, host, port, user, pswd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.db = db
        pass

    def connect_to_db(self):
        try:
            self.myDb = MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.pswd, db = self.db)
        except MySQLdb.Error as e:
            raise e


    def push_to_db(self, result_hr, result_br, device_id, date, time):
        data_to_send = [result_hr, result_br, device_id, date, time]
        try:
            cursor = self.myDb.cursor()
            sql = ("INSERT INTO Telemedicine (heart_rate,breath_rate,device_id,date, time) VALUES (%s,%s,%s,%s,%s)")
            cursor.execute(sql, data_to_send)
            self.myDb.commit()
        except MySQLdb.Error as e:
            raise e

#     def select_day_br(self):
#         #date = time.strftime('%Y-%m-%d')
#         data_to_send = [time.strftime('%Y-%m-%d')]
#         cursor = self.myDb.cursor()
#         sql = ("SELECT heart_rate FROM Telemedicine WHERE date=%s")
#         cursor.execute(sql,data_to_send)
#         received_data = []
#         for result in cursor:
#             received_data.append(result)
#         return received_data

    def _get_current_data():
        data_to_send = [time.strftime('%Y-%m-%d')]
        return data_to_send
    
    def select_daily(self, what, data_to_send):
        #what == 'time' or 'heart_rate'
        #data_to_send = [time.strftime('%Y-%m-%d')]
        cursor = self.myDb.cursor()
        sql = ("SELECT " + what + " FROM Telemedicine WHERE date=%s")
        cursor.execute(sql, data_to_send)
        received_data = []
        for result in cursor:
            received_data.append(result)
        return received_data

    def save_daily_plot(times, heart_rates, date):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(times, heart_rates, 'r')
        ax.grid(True)
        ax.set_ylabel('Значение ЧСС, уд/мин')
        ax.set_xlabel('Времена измерений ЧСС')
        ax.set_title('Изменение ЧСС за ' + date)
        plt.show()

        if not os.path.exists('daily_plots/'):
            os.mkdir('daily_plots')
        plot_name = 'daily_plots/' + date + '.png'
        fig.savefig(plot_name, fmt='png')
        return plot_name
    
    def get_daily_plot():
        current_data = self._get_current_data()
        times = self.select_daily('time', current_data)
        heart_rates = self.select_daily('heart_rate', current_data)
        plot_name self.save_daily_plot(times, heart_rates, current_data)
        return plot_name
        
        
