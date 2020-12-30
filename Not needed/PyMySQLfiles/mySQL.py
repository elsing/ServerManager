import pymysql

db = pymysql.connect(host="195.201.95.187",  # your host 
                     user="web",       # username
                     passwd="Ell10t1324!Hdmi1324!",     # password
                     db="servermanager")   # name of the database

cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL,
company VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
''')

##cursor.execute('''
##CREATE TABLE IF NOT EXISTS servers(
##serverID INTEGER PRIMARY KEY,
##brand VARCHAR(20) NOT NULL,
##productline VARCHAR(20) NOT NULL,
##usage VARCHAR(1024) NOT NULL,
##cpus VARCHAR(20) NOT NULL,
##ram VARCHAR(20) NOT NULL,
##psus VARCHAR(20) NOT NULL);
##''')


print("Done")
