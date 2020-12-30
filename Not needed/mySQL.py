import pymysql

db = pymysql.connect(host="192.168.1.208",  # your host 
                     user="servermanager",       # username
                     passwd="Server!Manager!",     # password
                     db="servermanager")   # name of the database

cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
userID INTEGER(200) PRIMARY KEY,
username VARCHAR(30) NOT NULL,
password VARCHAR(200) NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS devices(
serverID INTEGER(200) PRIMARY KEY,
userID int,
FOREIGN KEY (userID) REFERENCES users(userID),
name VARCHAR(50) NOT NULL,
IP VARCHAR(20) NOT NULL,
type VARCHAR(20) NOT NULL,
brand VARCHAR(30) NOT NULL,
productline VARCHAR(30) NOT NULL,
purpose TEXT NOT NULL,
cpus VARCHAR(30) NOT NULL,
ram VARCHAR(30) NOT NULL,
psus VARCHAR(30) NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS status(
statusID INTEGER(200) PRIMARY KEY,
userID int,
FOREIGN KEY (userID) REFERENCES users(userID),
serverID int,
FOREIGN KEY (serverID) REFERENCES devices(serverID),
IP VARCHAR(20),
state VARCHAR(20) NOT NULL,
lastseen VARCHAR(20) NOT NULL,
email VARCHAR(20) NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS udetails(
userID int,
FOREIGN KEY (userID) REFERENCES users(userID),
firstname VARCHAR(30) NOT NULL,
surname VARCHAR(30) NOT NULL,
company VARCHAR(200) NOT NULL,
email VARCHAR(200) NOT NULL);
''')


print("Done")
