from DBwriter_class import DbWriter
import  time

writer = DbWriter("173.230.151.37",3306, "root", "BMT4Ever", "mydb")
if writer.connect_to_db() == 0:
    print("no bse connection")

#time_now = time.strftime('%Y-%m-%d %H:%M:%S')
date_now = time.strftime('%Y-%m-%d')
time_now = time.strftime('%H:%M:%S')
print(time_now)
writer.push_to_db(1, 2, 7, date_now, time_now)

