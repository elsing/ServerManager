from appJar import gui
from SQL_System import *
import Manager_GUI
import pymysql

def __main__():


    app = gui("Server Manager - Login", "800x500")
    app.setSticky("news")
    app.setExpand("both")
    app.setFont(8)

    size = 9

    def logingui():
        app.addEntry("r3c3s3", 3, 3, 3)
        app.setEntryDefault("r3c3s3", "Please enter your username")
        app.setEntryAlign("r3c3s3", "center")
        app.setEntryAnchor("r3c3s3", "center")
        app.addSecretEntry("r5c3s3", 5, 3, 3)
        app.setEntryDefault("r5c3s3", "Please enter your password")
        app.setEntryAlign("r5c3s3", "center")
        app.setEntryAnchor("r5c3s3", "center")
        app.addButton("Login", loginb, 7, 4)
        app.setEntryRelief("r3c3s3", "flat")
        app.setEntryRelief("r5c3s3", "flat")
        app.setButtonRelief("Login", "flat")
        
    def loginb():
        username = str(app.getEntry("r3c3s3"))
        password = str(app.getEntry("r5c3s3"))
        L = SQL_System.login(username,password)
        D = SQL_System.userDetails(L[1])
        statusb = []
        if L[0] == "Y":
            app.setEntryBg("r3c3s3","White")
            app.setEntryBg("r5c3s3","White")
            print("\nWelcome", D[0][1], D[0][2])
            print("Your company is", D[0][3])
            statusb.append("Yes")
            statusb.append(D[0][1]+ " "+ D[0][2])
            statusb.append(D[0][3])
            sleep(2)
            app.stop()
            Manager_GUI.__main__(username,L[1],statusb)
        else:
            print("\nUsername or password not recognised.")
            app.setEntryBg("r3c3s3","Red")
            app.setEntryBg("r5c3s3","Red")
        
    def Colours(colour):
        for r in range(0,size):
            for c in range(0,size):
                string = str("r"+str(r)+"c"+str(c))
                app.setLabelBg(string, colour)
        app.setLabelBg("SM", colour)
        app.setBg(colour, override=False, tint=False)

    def Exit():
        app.destroySubWindow("About") 
        
    for r in range(0,size):
        for c in range(0,size):
            grid = "r"+str(r)+"c"+str(c)
            name= "row="+str(r)+"\ncolumn="+str(c)
            app.addLabel(grid, "", r, c)

    align = size / 3

    logingui()

    app.addLabel("SM", "Server Manager", 2, int(align), 3)
    app.getLabelWidget("SM").config(font=("Nothing", "32", "normal"))
    app.setLabelBg("SM", "DeepSkyBlue")
    app.setLabelFg("SM", "white")
    app.getEntryWidget("r3c3s3").config(font=("Nothing", "18", "normal"))
    app.getEntryWidget("r5c3s3").config(font=("Nothing", "18", "normal"))
    app.getButtonWidget("Login").config(font=("Nothing", "16", "normal"))
    Colours("DeepSkyBlue")
    app.go()
