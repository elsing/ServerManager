from SQL_System import *
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
from appJar import gui
import os
import subprocess
import datetime
import time
import threading

xx = 150
yy = 100

class GUI:
    def __init__(self):
        self.userID = ""
        self.username = ""
        self.password = ""
        self.email = ""
        self.loggedIn = False
        self.running = False
        self.pingRate = 60
        self.emailRate = 300
        self.pingCount = 0
        self.emailCount = 0
        self.updates = 0

    def startMain(self):
        global app
        app = gui("Server Checker", "800x500", showIcon=False)
        app.hide()
        LoginGUI.start(self)
        Server_Checker.start(self)
        app.showSubWindow("Server Manager - Login")
        app.go()

    def grid(self,diff,sizem,offsetr,offsetc):
        for r in range(0,sizem+offsetr):
            for c in range(0,sizem+offsetc):
                grid = diff+"r"+str(r)+"c"+str(c)
                name= "row="+str(r)+"\ncolumn="+str(c)
                app.addLabel(grid,"",r,c)

class Server_Checker:

    def currenttime():
        ts = time.time()
        return(datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'))

    def ping(host):
        reply = subprocess.call(['ping', '-n', '3', '-w', '3', host], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
        if reply == 0:
            app.setTextArea("consoleOutput","Host "+host+ " is up!\n",end=False)
            return("Up")
        else:
            app.setTextArea("consoleOutput","Host "+host+ " is down!\n",end=False)
            return("Down")

    def updateStatus(userID):
        info = SQL_System.searchDevicesByUserID(userID, "N",go.password , "All")
        pool = ThreadPool(16)
        ips = []
        for i in range(0,len(info)):
            ips.append(info[i][2])
        state = pool.map(Server_Checker.ping, ips)
        for i in range(0,len(info)):
            SQL_System.updateStatus(state[i], Server_Checker.currenttime(), info[i][0],go.email)
        pool.close()
        pool.join()

    def statusChecker():
        while True:
            try:
                if go.running == True:
                    if go.pingCount == go.pingRate:
                        Server_Checker.updateStatus(go.userID)
                        go.updates+=1
                        app.setTextArea("consoleOutput","Updated "+str(go.updates)+" times.\n",end=False)
                        go.pingCount = 0
                        sleep(1)
                    if go.emailCount == go.emailRate:
                        app.setTextArea("consoleOutput","\nEmailing now.\n",end=False)
                        SQL_System.checkStatus(go.userID, go.email, go.password)
                        go.emailCount = 0
                        sleep(1)
                    else:
                        go.pingCount+=1
                        app.setLabel("pingCount",go.pingCount)
                        go.emailCount+=1
                        app.setLabel("emailCount",go.emailCount)
                        sleep(1)
                else:
                    app.clearTextArea("consoleOutput")
                    app.setLabel("pingCount",go.pingCount)
                    app.setLabel("emailCount",go.emailCount)
                    sleep(1)
                    return
            except Exception as e:
                app.setTextArea("consoleOutput", "\nThere has been an error\nThis is most likely a time out error to the server.\n", end=False)

    def runSystem(btn):
        if btn == "startChecker":
            if go.running == False:
                app.setTextArea("consoleOutput","\nStarting... \n",end=False)
                app.setTextArea("consoleOutput","\nAll emails will be sent to: "+go.email,end=False)
                go.pingCount = go.pingRate
                go.running = True
                go.updates = 0
                app.setTabbedFrameSelectedTab("ManagerGUITabs","Console Output")
                thread = threading.Thread(target=Server_Checker.statusChecker)
                thread.daemon = True
                thread.start()
        elif btn == "stopChecker":
            if go.running == True:
                app.setTextArea("consoleOutput","\nStopping... \n",end=False)
                go.pingCount = 0
                go.emailCount = 0
                go.running = False

    def changeRates(btn):
        if btn == "setPingRate":
            if go.pingCount > int(app.getOptionBox("pingRateOpt")):
                app.setOptionBox("pingRateOpt",str(go.pingRate))
                print("The time you have chosen is above the current ping timer.")
                print("To avoid this, stop the program, then set the rate")
            else:
                go.pingRate = int(app.getOptionBox("pingRateOpt"))
                app.setOptionBox("pingRateOpt",str(go.pingRate))
                app.setTextArea("consoleOutput","\nPing rate updated to "+str(go.pingRate)+" seconds.\n\n",end=False)
        else:
            if go.emailCount > int(app.getOptionBox("emailRateOpt")):
                app.setOptionBox("emailRateOpt",str(go.emailRate))
                print("The time you have chosen is above the current email timer.")
                print("To avoid this, stop the program, then set the rate")
            else:
                go.emailRate = int(app.getOptionBox("emailRateOpt"))
                app.setOptionBox("emailRateOpt",str(go.emailRate))
                app.setTextArea("consoleOutput","\nEmail rate updated to "+str(go.emailRate)+" seconds.\n\n",end=False)

    def close():
        app.setFastStop(True)
        app.stop()
        exit()

    def prepare(self):
        app.setSize(800,500)
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(16)
        app.setLocation(xx,yy)
        app.startTabbedFrame("ManagerGUITabs")
        app.setTabbedFrameTabExpand("ManagerGUITabs", expand=True)
        app.startTab("Start / Stop")
        GUI.grid(self, "StartTab",6,-2,1)
        app.setSticky("ew")
        app.addNamedButton("Stop","stopChecker",Server_Checker.runSystem,1,4,2)
        app.addNamedButton("Start","startChecker",Server_Checker.runSystem,1,1,2)
        app.addLabel("pingRateLabel","Ping rate(s):",3,0)
        app.addOptionBox("pingRateOpt",["15","30","60","120","300","600","900","1800","3600"],3,1)
        app.setOptionBox("pingRateOpt",str(go.pingRate))
        app.addLabel("emailRateLabel","Email rate(s):",3,4)
        app.addOptionBox("emailRateOpt",["300","600","900","1800","3600","7200","10800"],3,5)
        app.setOptionBox("emailRateOpt",str(go.emailRate))
        app.addNamedButton("Set","setPingRate",Server_Checker.changeRates,3,2)
        app.addNamedButton("Set","setEmailRate",Server_Checker.changeRates,3,6)
        app.addNamedButton("Exit", "exit",Server_Checker.close,0,6)
        app.stopTab()
        app.startTab("Console Output")
        GUI.grid(self, "Console",6,0,0)
        app.addScrolledTextArea("consoleOutput",1,0,6,6)
        app.addLabel("pingCountLabel","Ping timer(s)",0,0)
        app.addLabel("emailCountLabel","Email timer(s)",0,4)
        app.addLabel("pingCount","",0,1)
        app.addLabel("emailCount","",0,5)
        app.stopTab()
        app.stopTabbedFrame()

    def start(self):
        app.startSubWindow("SC","Server Checker")
        Server_Checker.prepare(self)
        app.stopSubWindow()

class LoginGUI:
    def loginButton(self):
        username = str(app.getEntry("LoginGUIUsername"))
        password = str(app.getEntry("LoginGUIPassword"))
        go.password = password
        L = SQL_System.login(username,password)
        if L[0] == "Y":
            D = SQL_System.userDetails(L[1], password)
            app.setEntryBg("LoginGUIUsername","White")
            app.setEntryBg("LoginGUIPassword","White")
            app.clearEntry("LoginGUIUsername")
            app.clearEntry("LoginGUIPassword")
            app.popUp("Welcome "+ D[0]+"!", "Welcome "+D[0]+" "+D[1]+"!\nYour company is "+D[2])
            print("\nWelcome", D[0], D[1])
            print("Your company is", D[2])
            go.userID = L[1]
            go.username = username
            go.password = password
            go.email = D[3]
            app.hideSubWindow("Server Manager - Login")
            app.showSubWindow("SC")
        else:
            print("\nUsername or password not recognised.")
            app.popUp("Unknown PW / UN", "Username or password not recognised.", kind="warning")
            app.setEntryBg("LoginGUIUsername","Red")
            app.setEntryBg("LoginGUIPassword","Red")

    def prepare(self):
        GUI.grid(self, "LoginGUI",9,0,0)
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(8)
        app.setSize(500,300)
        app.setLocation(xx,yy)
        app.addEntry("LoginGUIUsername", 3, 3, 3)
        app.setEntryRelief("LoginGUIUsername", "flat")
        app.getEntryWidget("LoginGUIUsername").config(font=("Nothing", "18", "normal"))
        app.addSecretEntry("LoginGUIPassword", 5, 3, 3)
        app.setEntryRelief("LoginGUIPassword", "flat")
        app.getEntryWidget("LoginGUIPassword").config(font=("Nothing", "18", "normal"))
        app.setEntryDefault("LoginGUIUsername", "Please enter your username")
        app.setEntryDefault("LoginGUIPassword", "Please enter your password")
        app.addNamedButton("Login","LoginGUILoginB", LoginGUI.loginButton, 7, 4)
        app.getButtonWidget("LoginGUILoginB").config(font=("Nothing", "16", "normal"))
        app.addLabel("LoginGUITitle", "Server Checker", 2, 3, 3)
        app.getLabelWidget("LoginGUITitle").config(font=("Nothing", "32", "normal"))

    def start(self):
        app.startSubWindow("Server Manager - Login")
        LoginGUI.prepare(self)
        app.stopSubWindow()

go = GUI()
go.startMain()