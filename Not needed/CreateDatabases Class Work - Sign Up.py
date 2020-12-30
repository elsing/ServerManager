import sqlite3
import time

with sqlite3.connect("ProjectDatabase.db") as db:
    cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
userID INTEGAR PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL,
company VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS servers(
serverID INTEGAR PRIMARY KEY,
brand VARCHAR(20) NOT NULL,
productline VARCHAR(20) NOT NULL,
usage VARCHAR(255) NOT NULL,
cpus VARCHAR(20) NOT NULL,
ram VARCHAR(20) NOT NULL,
psus VARCHAR(20) NOT NULL);
''')

##cursor.execute("""
##INSERT INTO user(username,firstname,surname,password)
##VALUES("test_user","Bob","Smith","MrBob")
##""")
db.commit()


def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with sqlite3.connect("ProjectDatabase.db") as db:
            cursor = db.cursor()
        find_user = ('SELECT * FROM users WHERE username  = ? AND password = ?')
        cursor.execute(find_user, [(username), (password)]) # [] replaces the values of ?
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome "+i[2])
                return("exit")
        else:
            print("Username and password not recognised.")
            again= input("Do you want to retry? (Y/N).")
            if again.lower() == "n":
                print("Goodbye.")
                time.sleep(1)
                return("exit")
def newUser():
    print("Add a new user.")
    time.sleep(1)
    #check is user name is taken
    found = 0
    while found == 0:
        username = input("Enter a username: ")
        with sqlite3.connect("ProjectDatabase.db") as db:
            cursor = db.cursor()
        find_user = ('SELECT * FROM users WHERE username = ?') #? stops the SQL injection
        cursor.execute(find_user,[(username)]) # [] replaces the value of ?

        if cursor.fetchall():
            print("Username Taken")
        else:
            found = 1
    firstName = input("Pleas enter your first name: ")
    surname = input("Please enter your last name: ")
    company = input("Please enter your company name: ")
    password = input("Please enter a password: ")
    password1 = input("Please re-enter your password: ")
    while password != password1:
        print("Passwords did not match.")
        password = input("Please enter a password: ")
        password1 = input("Please re-enter your password: ")
    insertData = '''INSERT INTO users(username,firstname,surname,company,password)VALUES(?,?,?,?)'''
    cursor.execute(insertData,[(username), (firstName), (surname), (company), (password)])
    db.commit() #saves the results into the database


while True:
    print("Welcome to the system")
    menu = ('''
    1 - Create New User
    2 - Login
    3 - Exit \n''')

    userChoice = input(menu)

    if userChoice == "1":
        newUser()
    elif userChoice == "2":
        enter = login()
        if enter == "exit":
            break
    elif userChoice == "3":
        print("Goodbye")
        time.sleep(1)
        break
    else:
        print("Input not recognised, please try again.\n")







    
                     
