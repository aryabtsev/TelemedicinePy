import pymysql


class DbWriter:
    def __init__(self, host, port, user, pswd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pswd = pswd
        self.db = db
        self.myDb = None
        pass

    def connect_to_db(self):
        try:
            self.myDb = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.pswd, db = self.db)
        except pymysql.Error as e:
            raise e

    def push_to_db(self, result_hr, result_br, device_id, date, time):
        data_to_send = [result_hr, result_br, device_id, date, time]
        try:
            cursor = self.myDb.cursor()
            sql = ("INSERT INTO Telemedicine (heart_rate,breath_rate,device_id,date, time) VALUES (%s,%s,%s,%s,%s)")
            cursor.execute(sql, data_to_send)
            self.myDb.commit()
        except pymysql.Error as e:
            raise e
