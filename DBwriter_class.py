import MySQLdb

myDb = MySQLdb.connect(host='173.230.151.37', port=3306, user='ivan', password='BMT4Ever!', database = 'mydb')

def push_to_db(result_hr,result_br) :
    cursor = myDb.cursor("""INSERT IN Telemedicine VALUES""")
    cursor.execute(sql)

push_to_db (0,0)