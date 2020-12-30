from SQL_System import *
from appJar import gui
from time import sleep
import Login_GUI
import random
import pymysql

def __main__():
    size = 9
    offsetr = 7
    offsetc = 0
    app = gui("Server Manager - Sign Up", "900x800")
    app.setSticky("news")
    app.setExpand("both")
    app.setFont(8)

    for r in range(0,size+offsetr):
        for c in range(0,size+offsetc):
            grid = "r"+str(r)+"c"+str(c)
            name= "row="+str(r)+"\ncolumn="+str(c)
            app.addLabel(grid, "", r, c)

    def SignUp():
        app.addLabel("r0c2s5","Please enter your details", 0, 2, 5)
        app.addEntry("r2c3s3", 2,3,3)
        app.addEntry("r4c3s3", 4,3,3)
        app.addEntry("r6c3s3", 6,3,3)
        app.addEntry("r8c3s3", 8,3,3)
        app.addSecretEntry("r10c3s3", 10,3,3)
        app.addSecretEntry("r12c3s3", 12,3,3)
        app.addButton("Submit", Submit, 14,3,3)
        app.getLabelWidget("r0c2s5").config(font=("Nothing", "32", "normal"))
        app.setEntryDefault("r2c3s3","Username")
        app.getEntryWidget("r2c3s3").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("r4c3s3","First Name")
        app.getEntryWidget("r4c3s3").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("r6c3s3","Second Name")
        app.getEntryWidget("r6c3s3").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("r8c3s3","Company")
        app.getEntryWidget("r8c3s3").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("r10c3s3","Password")
        app.getEntryWidget("r10c3s3").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("r12c3s3","Password Confirmation")
        app.getEntryWidget("r12c3s3").config(font=("Nothing", "18", "normal"))
        app.getButtonWidget("Submit").config(font=("Nothing", "18", "normal"))

    def Colour(colour):
        for r in range(0,size):
            for c in range(0,size):
                string = str("r"+str(r)+"c"+str(c))
                app.setLabelBg(string, colour)
       # app.setLabelBg("SM", colour)
        app.setBg(colour, override=False, tint=False)

    def Get():
        D = []
        userID = ""
        usern = str(app.getEntry("r2c3s3"))
        firstn = str(app.getEntry("r4c3s3"))
        secondn = str(app.getEntry("r6c3s3"))
        company = str(app.getEntry("r8c3s3"))
        password = str(app.getEntry("r10c3s3"))
        passwordc = str(app.getEntry("r12c3s3"))
        for i in range(9):
            userID+=str(random.randint(0,9))
        D.append((usern,firstn,secondn,company,password,passwordc,userID))
        return(D)

    def Submit():
        D = Get()
        T1 = 0
        T2 = False
        box = ["r2c3s3","r4c3s3","r6c3s3","r8c3s3","r10c3s3"]
        for i in range(0,5):
            if D[0][i] == '':
                app.setEntryBg(box[i], "Red")
                print("You have not entered anything in box number ",str(i+1),".")
                print(box[i])
                T1+=1
            else:
                app.setEntryBg(box[i], "White")
        for i in range(0,3):
            if len(D[0][i]) > 20:
                print("Please make sure your entry in box",str(i+1), "is 20 or less.")
                print("You are currently",str(len(D[0][i])-20),"characters over.")
                app.setEntryBg(box[i], "Red")
                T1+=1
            else:
                app.setEntryBg(box[i], "White")
        if D[0][4] != D[0][5]:
            print("Passwords do not match.")
            app.setEntryBg("r10c3s3", "Red")
            app.setEntryBg("r12c3s3", "Red")
        else:
            app.setEntryBg("r10c3s3", "White")
            app.setEntryBg("r12c3s3", "White")
            T2 = True
        
        if T1 == 0 and T2 == True:
            if SQL_System.NewUser(D) == "Exis":
                print("This username already exists.")
            else:
                print("Added")
                app.addLabel("r14c3s3","Added",14,3,3)
                app.getLabelWidget("r14c3s3").config(font=("Nothing", "24", "normal"))
                sleep(5)
                app.stop()
                Login_GUI.__main__()
                



    SignUp()
    Colour("DeepSkyBlue")
    align = size / 3
    app.go()
