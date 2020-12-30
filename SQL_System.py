from email.mime.text import MIMEText
import pymysql
import hashlib
import uuid
import random
import smtplib

def startDB():
    global db
    global cursor
    db = pymysql.connect(host="192.168.1.208",  # your host 
             user="servermanager",       # username
             passwd="Server!Manager!",     # password
             db="servermanager")   # name of the database
    cursor = db.cursor()

def stopDB():
    cursor.close()
    db.close()

class SQL_System:

    def checkExisting(username):
        # Checks if the username inputed already exists or not.
        results = SQL_System.searchUsers(username)
        if len(results) == 0:
            return("N")
        else:
            return("Y")

    def generateRandomCode():
        randID = ""
        results = []
        for i in range( 9):
            randID+=str(random.randint(0,9))
        startDB()
        cursor.execute('SELECT userID FROM users WHERE userID  = %s', [randID])
        results.append(cursor.fetchall())
        cursor.execute('SELECT serverID FROM devices WHERE serverID  = %s', [randID])
        results.append(cursor.fetchall())
        cursor.execute('SELECT statusID FROM status WHERE statusID  = %s', [randID])
        results.append(cursor.fetchall())
        for i in range(0,3):
            if len(results[i]) != 0:
                SQL_System.generateRandomCode()
        stopDB()
        return(randID)
            
    def searchUsers(username):
        # Searches the database for a certain username and returns the result
        startDB()
        find_user = 'SELECT * FROM users WHERE username  = %s'            
        cursor.execute(find_user, [username]) # [] replaces the values of %s
        results = cursor.fetchall()
        stopDB()
        return results

    def searchDevicesByUserID(userID, statusTable, password, type):
        # Searches the database for a users devices, then decryptes any data found
        # Then returns those results
        startDB()
        results = []
        finalResults = []
        find_device = 'SELECT serverID, name, IP, type FROM devices WHERE userID  = %s ORDER BY name ASC'
        cursor.execute(find_device, [userID]) # [] replaces the values of %s
        sqlResults = (cursor.fetchall())
        stopDB()
        for i in range(len(sqlResults)):
            results.append([])
            for x in range(0,4):
                results[i].append(sqlResults[i][x])
            status = SQL_System.searchStatusByserverID(sqlResults[i][0])
            if statusTable == "Y":
                results[i].append(status[1])
            for y in range(1,4):
                results[i][y] = SQL_System.vernam(results[i][y], password)
        for i in range(0,len(results)):
            if results[i][3] == type or type == "All":
                finalResults.append(results[i])
        return finalResults
    
    def searchDevicesByServerID(serverID, password):
        startDB()
        find_device = 'SELECT * FROM devices WHERE serverID  = %s'
        cursor.execute(find_device, [serverID]) # [] replaces the values of %s
        sqlResults = cursor.fetchall()
        stopDB()
        results = []
        for i in range(0,11):
            if i <2:
                results.append(sqlResults[0][i])
            else:
                results.append(SQL_System.vernam(sqlResults[0][i], password))
        return results

    def searchStatusByuserID(userID):
        startDB()
        find_status = 'SELECT serverID, state, email FROM status WHERE userID  = %s'
        cursor.execute(find_status, [userID]) # [] replaces the values of %s
        results = cursor.fetchall()
        db.commit()
        stopDB()
        return results

    def searchStatusByuserIDType(userID, type, password):
        startDB()
        find_status_type = '''SELECT s.serverID, s.state, d.type FROM status s JOIN devices d ON s.serverID = d.serverID WHERE s.userID = %s AND type = %s'''
        type = SQL_System.vernam(type, password)
        cursor.execute(find_status_type, [(userID),(type)])
        sqlResults = cursor.fetchall()
        db.commit()
        stopDB()
        return sqlResults
    
    def searchStatusByserverID(serverID):
        startDB()
        find_status = 'SELECT serverID, state, email FROM status WHERE serverID  = %s'
        cursor.execute(find_status, [serverID]) # [] replaces the values of %s
        results = cursor.fetchall()
        db.commit()
        stopDB()
        results = list(results[0])
        return results

    def deviceStatus(serverID, password):
        startDB()
        find_status = 'SELECT * FROM status WHERE serverID  = %s'
        cursor.execute(find_status, [serverID]) # [] replaces the values of %s
        results = cursor.fetchall()
        stopDB()
        results = list(results[0])
        results[3] = SQL_System.vernam(results[3],password)
        return results

    def updateStatus(state,lastseen,serverID,email):
        startDB()
        if state == "Down":
            update_status = 'UPDATE status SET state = %s WHERE serverID = %s;'
            cursor.execute(update_status, [(state), (serverID)])
        else:
            update_status = 'UPDATE status SET state = %s, lastseen = %s WHERE serverID = %s;'
            cursor.execute(update_status, [(state), (lastseen), (serverID)])
        db.commit()
        stopDB()

    def checkStatus(userID, email, password):
        info = SQL_System.searchDevicesByUserID(userID, "N", password, "All")
        status = SQL_System.searchStatusByuserID(userID)
        downDevices = []
        for i in range(0,len(status)):  
            if status[i][1] == "Down" and status[i][2] == "Y":
                downDevices.append(status[i][0])
        SQL_System.emailStatus(downDevices, email, password)
                
    def login(username,password):
        results = SQL_System.searchUsers(username)
        if results == ():#
            return("Username does not exist.")
        else:
            if SQL_System.checkPassword(results[0][2],password) == True:
                return(["Y",results[0][0]])
            else:
                return(["N",results[0][0]])

    def emailChoice(choice,serverID):
        startDB()
        if choice == True:
            email = "Y"
        else:
            email = "N"
        email_choice = 'UPDATE status SET email = %s WHERE serverID = %s;'
        cursor.execute(email_choice, [(email), (serverID)])
        db.commit()
        stopDB()
        
    def newDevice(D,userID,password):
        for i in range(0,9):
            D[i] = SQL_System.vernam(D[i],password)
        deviceDetails = [["name",D[0]],["IP",D[1]],["type",D[2]],["brand",D[3]],["productline",D[4]],["purpose",D[5]],["cpus",D[6]],["ram",D[7]],["psus",D[8]]]
        serverID = SQL_System.generateRandomCode()
        statusID = SQL_System.generateRandomCode()
        state = "Unknown"
        lastseen = "N/A"
        email = "Y"
        startDB()
        insertDevice = '''INSERT INTO devices(serverID,userID,name,IP,type,brand,productline,purpose,cpus,ram,psus)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        insertStatus = '''INSERT INTO status(statusID,userID,serverID,IP,state,lastseen,email)VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(insertDevice,[(serverID), (userID), (deviceDetails[0][1]), (deviceDetails[1][1]), (deviceDetails[2][1]), (deviceDetails[3][1]), (deviceDetails[4][1]), (deviceDetails[5][1]), (deviceDetails[6][1]), (deviceDetails[7][1]), (deviceDetails[8][1])])
        cursor.execute(insertStatus,[(statusID), (userID), (serverID), (deviceDetails[1][1]), (state), (lastseen), (email)])
        db.commit()
        stopDB()

    def updateDevice(D, serverID, password):
        startDB()
        for i in range(0,9):
            D[i] = SQL_System.vernam(D[i],password)
        deviceDetails = [["name",D[0]],["IP",D[1]],["type",D[2]],["brand",D[3]],["productline",D[4]],["purpose",D[5]],["cpus",D[6]],["ram",D[7]],["psus",D[8]]]
        updateDevice = '''UPDATE devices SET name = %s, IP = %s, type = %s, brand = %s, productline = %s, purpose = %s, cpus = %s, ram = %s, psus = %s WHERE serverID = %s'''
        updateStatus = '''UPDATE status SET IP = %s WHERE serverID = %s;'''
        cursor.execute(updateDevice,[(deviceDetails[0][1]), (deviceDetails[1][1]), (deviceDetails[2][1]), (deviceDetails[3][1]), (deviceDetails[4][1]), (deviceDetails[5][1]), (deviceDetails[6][1]), (deviceDetails[7][1]), (deviceDetails[8][1]), (serverID)])
        cursor.execute(updateStatus,[(deviceDetails[1][1]), (serverID)])
        db.commit()
        stopDB()

    def removeDevice(serverID):
        startDB()
        removeDevice = 'DELETE FROM devices WHERE serverID = %s'
        removeStatus = 'DELETE FROM status WHERE serverID = %s'
        cursor.execute(removeDevice, [serverID])
        cursor.execute(removeStatus, [serverID])
        db.commit()
        stopDB()
        
    def newUser(D):
        if SQL_System.checkExisting(D[0]) == "Y":
            return("Exis")
        else:
            usern = D[0]
            firstn = SQL_System.vernam(D[1],D[6])
            secondn = SQL_System.vernam(D[2],D[6])
            company = SQL_System.vernam(D[3],D[6])
            email = SQL_System.vernam(D[4],D[6])
            password = D[6]
            userID = D[8]
            startDB()
            insertUser = '''INSERT INTO users(userID,username,password)VALUES(%s,%s,%s)'''
            cursor.execute(insertUser,[(userID), (usern), (SQL_System.hashPassword(password))])
            insertDetails = '''INSERT INTO udetails(userID,firstname,surname,company,email)VALUES(%s,%s,%s,%s,%s)'''
            cursor.execute(insertDetails,[(userID),(firstn),(secondn),(company),(email)])
            db.commit() #Saves the results into the database
        stopDB()

    def removeUser(userID):
        startDB()
        deleteUser0 = '''DELETE FROM users WHERE userID = %s'''
        deleteUser1 = '''DELETE FROM udetails WHERE userID = %s'''
        deleteUser2 = '''DELETE FROM devices WHERE userID = %s'''
        deleteUser3 = '''DELETE FROM status WHERE userID = %s'''
        cursor.execute(deleteUser3,[(userID)])
        cursor.execute(deleteUser2,[(userID)])
        cursor.execute(deleteUser1,[(userID)])
        cursor.execute(deleteUser0,[(userID)])
        db.commit()
        stopDB()
        print("\nAccount has been fully deleted.")

    def changeDetail(optionBox, newDetail, userID,password):
        startDB()
        details = [["Forename","firstname"],["Surname","surname"],["Company","company"],["Email","email"]]
        for i in range(0,4):
            if optionBox == details[i][0]:
                updateDetail = "UPDATE udetails SET "+details[i][1]+" = %s WHERE userID = %s"     
        newDetail = SQL_System.vernam(newDetail,password)
        cursor.execute(updateDetail,[(newDetail),(userID)])
        db.commit()
        stopDB()
        
    
    def hashPassword(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def emailStatus(devicesDown, email, password):
        sender = 'servermanager@singermail.uk'
        device = "Some of your devices have been identified as having gone down.\n"
        for i in range(0,len(devicesDown)):
            deviceDetails = SQL_System.searchDevicesByServerID(devicesDown[i] , password)
            device+= "\nYour device named "+deviceDetails[2]+" with the IP address "+deviceDetails[3]+" is down. You may want to act now\n"
        msg = MIMEText(device)
        msg['Subject'] = "One or more devices are down."
        msg['From'] = sender
        msg['To'] = email
        server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
        server.login('servermanager@singermail.uk', 'Server!Manag3r!')
        server.sendmail(sender, [email], msg.as_string())
        server.quit()

        
            
    def checkPassword(hashedPassword, userPassword):
        password, salt = hashedPassword.split(':')
        return password == hashlib.sha256(salt.encode() + userPassword.encode()).hexdigest()

    def updatePassword(userID, password):
        startDB()
        updatePassword = '''UPDATE users SET password = %s WHERE userID = %s'''
        cursor.execute(updatePassword, [(password), (userID)])
        db.commit()
        stopDB()

    def changePassword(userID,password,newPassword):
        devices = SQL_System.searchDevicesByUserID(userID, "N", password, "All")
        serverIDs = []
        for i in range(0,len(devices)):
            D = []
            serverIDs.append(devices[i][0])
            deviceInfo = SQL_System.searchDevicesByServerID(serverIDs[i], password)
            for x in range(2,11):
                D.append(deviceInfo[x])
            SQL_System.updateDevice(D, serverIDs[i], newPassword)   
        SQL_System.updateUserDetails(SQL_System.userDetails(userID, newPassword), userID, password)
        newHashedPassword = SQL_System.hashPassword(newPassword)
        SQL_System.updatePassword(userID, newHashedPassword)

    def updateUserDetails(D, userID, password):
        startDB()
        for i in range(0,4):
            D[i] = SQL_System.vernam(D[i],password)
        userDetails = [["name",D[0]],["surname",D[1]],["company",D[2]],["email",D[3]]]
        updateUser = '''UPDATE udetails SET firstname = %s, surname = %s, company = %s, email = %s WHERE userID = %s'''
        cursor.execute(updateUser,[(userDetails[0][1]), (userDetails[1][1]), (userDetails[2][1]), (userDetails[3][1]), (userID)])
        db.commit()
        stopDB()
        print("Password Successfully Changed!")
        return

    def userDetails(userID, password):
        results = []
        startDB()
        find_user = 'SELECT * FROM udetails WHERE userID  = %s'            
        cursor.execute(find_user, [userID]) # [] replaces the values of %s
        sqlResults = cursor.fetchall()
        stopDB()
        for i in range(1,5):
            results.append(SQL_System.vernam(sqlResults[0][i],password))
        return results
        
        
    def vernam(text, key, return_str=False, alphanumerical=False):
        #Code by "roysoup"
        if alphanumerical:
            alphanumerics = [i for i in "0123456789abcdefghijklmbopqrstuvwxyzABCDEFGHIJKLMBOPQRSTUVWXYZ"]
            to_num = lambda x: alphanumerics.index(x)
            to_char = lambda x: alphanumerics[x]
        else:  
            to_num = ord
            to_char = chr
        
        bintext = [ to_num(x) for x in text ]  
        binkey = [ to_num(x) for x in key ]  
        
        for i in range( len(bintext) - len(binkey) ):  # Resize key to length of text
            binkey.append( binkey[i] )
        
        vernamed = [ bintext[i] ^ binkey[i] for i in range(len(bintext)) ]  # XOR vernam operation
        result = [to_char(i) for i in vernamed]  # Convert back to text
        
        if return_str:
            return "".join(result)
        #Code by "roysoup" done

        final = ""
        for i in range(0,len(result)):
            final += result[i]
        return final