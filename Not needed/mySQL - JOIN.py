import pymysql

db = pymysql.connect(host="195.201.95.187",  # your host 
                     user="servermanager",       # username
                     passwd="Server!Manager!",     # password
                     db="servermanager")   # name of the database

cursor = db.cursor()

cursor.execute('''
SELECT s.serverID, s.state, d.type
FROM status s JOIN devices d
ON s.serverID = d.serverID
WHERE s.userID = "148160704";
''')

results = cursor.fetchall()

print(results)

print("Done")
