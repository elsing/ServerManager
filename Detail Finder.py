import pymysql

def startDB():
    global db
    global cursor
    db = pymysql.connect(host="195.201.95.187",  # your host 
             user="servermanager",       # username
             passwd="Server!Manager!",     # password
             db="servermanager")   # name of the database
    cursor = db.cursor()

def stopDB():
    cursor.close()
    db.close()

startDB()

cursor.execute('SELECT * FROM udetails WHERE userID  = 337965876')
print(cursor.fetchall())

import vernam

stopDB()