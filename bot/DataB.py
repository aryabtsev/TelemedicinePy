import pymysql
import datetime

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




                    #SELECT * FROM
     #   your_table_name
     #   WHERE
      #  your_field_name = "whatever";

    def close(self):
        # Закрываем текущее соединение с БД
        self.connection.close()