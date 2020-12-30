import pymysql
import hashlib
import uuid
import random

db = pymysql.connect(host="195.201.95.187",  # your host 
             user="servermanager",       # username
             passwd="Server!Manager!",     # password
             db="servermanager")   # name of the database
cursor = db.cursor()

class SQL_System:

    def Check_Existing(username):
        results = SQL_System.SearchUsers(username)
        if len(results) == 0:
            return("N")
        else:
            return("Y")

    def SearchUsers(username):
        find_user = 'SELECT * FROM users WHERE username  = %s'            
        cursor.execute(find_user, [username]) # [] replaces the values of %s
        results = cursor.fetchall()
        return results

    def SearchDevicesByUserID(userID):
        find_device = 'SELECT serverID, name, IP, type FROM devices WHERE userID  = %s ORDER BY type DESC'
        cursor.execute(find_device, [userID]) # [] replaces the values of %s
        results = cursor.fetchall()
        return results
    
    def SearchDevicesByServerID(serverID):
        find_device = 'SELECT * FROM devices WHERE serverID  = %s ORDER BY type DESC'
        cursor.execute(find_device, [serverID]) # [] replaces the values of %s
        results = cursor.fetchall()
        return results
    
    def Login(username,password):
        results = SQL_System.SearchUsers(username)
        for i in results:
            if SQL_System.check_password(i[2],password) == True:
                return(["Y",i[0]])
            else:
                return(["N",i[0]])
            
    def NewDevice(D,userID):
        serverID = ""
        for i in range(9):
            serverID+=str(random.randint(0,9))
        name = D[0]
        IP = D[1]
        type = D[2]
        brand = D[3]
        productline = D[4]
        purpose = D[5]
        cpus = D[6]
        ram = D[7]
        psus= D[8]
        insertDevice = '''INSERT INTO devices(serverID,userID,name,IP,type,brand,productline,purpose,cpus,ram,psus)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(insertDevice,[(serverID), (userID), (name), (IP), (type), (brand), (productline), (purpose), (cpus), (ram), (psus)])
        db.commit()
        
    def NewUser(D):
        if SQL_System.Check_Existing(D[0][0]) == "Y":
            return("Exis")
        else:
            usern = D[0][0]
            firstn = D[0][1]
            secondn = D[0][2]
            company = D[0][3]
            password = D[0][4]
            userID = D[0][6]
            insertUser = '''INSERT INTO users(userID,username,password)VALUES(%s,%s,%s)'''
            cursor.execute(insertUser,[(userID), (usern), (SQL_System.hash_password(password))])
            insertDetails = '''INSERT INTO details(userID,firstname,surname,company)VALUES(%s,%s,%s,%s)'''
            cursor.execute(insertDetails,[(userID),(firstn),(secondn),(company)])
            db.commit() #saves the results into the database

    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt        
        
        

    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest() 

    def UserDetails(userID):
        find_user = 'SELECT * FROM details WHERE userID  = %s'            
        cursor.execute(find_user, [userID]) # [] replaces the values of %s
        results = cursor.fetchall()
        return list(results)
