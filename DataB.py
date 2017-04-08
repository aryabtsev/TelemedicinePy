import sqlite3

class DataB:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def select_average_hr(self):
        # получаем среднее сердцебиение
        with self.connection:
            return self.cursor.execute('SELECT AVG(Heart_rate) FROM TeleMedicine').fetchall()


    def select_average_br(self):
        # получаем среднее дыхание
        with self.connection:
            return self.cursor.execute('SELECT AVG(Breath_rate) FROM TeleMedicine').fetchall()

    def close(self):
        # Закрываем текущее соединение с БД
        self.connection.close()