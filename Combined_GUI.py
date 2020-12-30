from appJar import gui
from SQL_System import *
from time import sleep
import datetime
import threading
import random

accountLabels = [["Username:",1,1,1,1,1,2,1,1],["First Name:",2,1,1,1,2,2,1,1],["Surname:",2,4,1,1,2,5,1,1],["Company:",1,4,1,1,1,5,1,1],["Email:",4,1,2,1,4,3,3,1]]
labels = [["serverID",1,1,0,0,1,2,2,0],["Name",2,1,0,0,2,2,2,0],["IP(one)",3,1,0,0,3,2,2,0],["Type",4,1,0,0,4,2,2,0],["Brand",5,1,0,0,5,2,2,0],["Product Line",2,6,0,0,2,7,2,0],["Purpose",7,1,0,0,7,2,7,1],["CPU(s)",3,6,0,0,3,7,2,0],["RAM",4,6,0,0,4,7,2,0],["PSU(s)",5,6,0,0,5,7,2,0]]
sLabels = [["serverID:",1,1,0,0,1,2,1,0],["IP(one):",2,1,0,0,2,2,1,0],["State:",3,1,0,0,3,2,4,0],["Last Checked:",1,4,0,0,1,5,2,0],["Send emails?",2,4,0,0,2,5,2,0]]
opt = ["- Select me -","All","Server","Switch","Printer","Computer"]
modifyOpt = ["- Please Select -","Server","Switch","Printer","Computer"]
windows = ["self.AdminLoginGUI()","self.DebugGUI()","self.AccountGUI()","self.CAccountGUI()","self.SignUpGUI.start(self)","self.LoginGUI.start(self)","self.ManagerGUI.start(self)"]
one = "Welcome to Server Manager.\n\nThis is where you can make sure all your servers are online, and be notified when they are not."
two = "\n\nTo start, please either login or sign up below."
final = one+two
xx = 150
yy = 100


class GUI:
    
    def __init__(self, username, userID, loggedIn):
        self.userID = userID
        self.username = username
        self.firstName = ""
        self.secondName = ""
        self.password = ""
        self.company = ""
        self.email = ""
        self.loggedIn = False
        self.perc = -1
        self.time = 0

    def entryDefaults(window):
        app.clearAllEntries()
        if window == "SignUpGUI":
            app.setEntryDefault("username","1 - Username")
            app.setEntryDefault("firstName","2 - First Name")
            app.setEntryDefault("secondName","3 - Second Name")
            app.setEntryDefault("company","4 - Company")
            app.setEntryDefault("email","5 - Email")
            app.setEntryDefault("emailc","Email Confirmation")
            app.setEntryDefault("password","6 - Password")
            app.setEntryDefault("passwordc","Password Confirmation")
        elif window == "LoginGUI":
            app.setEntryDefault("LoginGUIUsername", "Please enter your username")
            app.setEntryDefault("LoginGUIPassword", "Please enter your password")
            
    def grid(self,diff,sizem,offsetr,offsetc):
        for r in range(0,sizem+offsetr):
            for c in range(0,sizem+offsetc):
                grid = diff+"r"+str(r)+"c"+str(c)
                name= "row="+str(r)+"\ncolumn="+str(c)
                app.addLabel(grid,"",r,c)
    
    def logout(self):
        self.username = ""
        self.userID = ""
        self.password = ""
        self.loggedIn = False
        GUI.ManagerGUI.refresh("StatusRefresh")
        GUI.ManagerGUI.refresh("ViewDetRefresh")
        GUI.ManagerGUI.refresh("removeRefresh")
        GUI.ManagerGUI.refresh("statsRefresh")
        app.hideSubWindow("SMGUI")
        app.hideSubWindow("AccountGUI")
        app.hideSubWindow("CAccountGUI")
        app.show()
        app.changeOptionBox("editDevices",["- Will be filled with your devices -"])
        app.clearAllOptionBoxes()
        app.clearAllEntries()
        app.clearAllTextAreas()
        app.setTextArea("guideBox",final)

    def colour(self,diff,colourC,size,offsetr,offsetc):
        for r in range(0,size+offsetr):
            for c in range(0,size+offsetc):
                string = str(diff)+str("r"+str(r)+"c"+str(c))
                app.setLabelBg(string, colourC)
        app.setLabelBg(str(diff)+"Title", colourC)
        app.setBg(colourC, override=False, tint=False)

    def AdminLoginGUI(self):
        app.startSubWindow("AdminLoginGUI","Admin Password",modal=True)
        self.grid("AdminPassword",6,0,0)
        app.setSize(570,320)
        app.addLabel("EnterP","Enter Admin Password",1,1,4)
        app.addSecretEntry("Password",3,1,4)
        app.addNamedButton("Submit","SubmitAdmin",self.admin,5,2,2)
        app.stopSubWindow()
        go.perc+=11

    def AccountGUI(self):
        app.startSubWindow("AccountGUI","Account Options")
        self.grid("AccountGUI",7,1,0)
        app.setSticky("news")
        app.setExpand("both")
        app.addNamedButton("Change Details","AccountGUIChange",self.buttons,6,1,2)
        app.addNamedButton("Delete Account","AccountGUIDelete",self.accountDelete,6,4,2)
        for i in range(0,5):
            app.addLabel(accountLabels[i][0],accountLabels[i][0],accountLabels[i][1],accountLabels[i][2],accountLabels[i][3],accountLabels[i][4])
            app.addLabel("account"+accountLabels[i][0],accountLabels[i][0],accountLabels[i][5],accountLabels[i][6],accountLabels[i][7],accountLabels[i][8])

        app.stopSubWindow()
        go.perc+=5

    def accountDelete(self):
        choice = app.yesNoBox("AccountGUIDeleteConfirm", "Are you sure you want to fully delete your account and all your devices?")
        if choice == True:
            SQL_System.removeUser(self.userID)
            app.popUp("accountRemoved","Your account has been fully deleted.")
            self.logout()
        else:
            app.hideSubWindow("AccountGUI")
            app.showSubWindow("SMGUI")

    def accountDetails(self):
        details = [[self.username],[self.firstName],[self.secondName],[self.company],[self.email]]
        for i in range(0,5):
            app.setLabel("account"+accountLabels[i][0],details[i][0])

    def CAccountGUI(self):
        app.startSubWindow("CAccountGUI","Change Account", modal=True)
        self.grid("CAccountGUI",6,0,0)
        app.addLabelOptionBox("Detail", ["- Choose me -", "Forename", "Surname",
                        "Company", "Email", "Password"],0,0,3)
        app.addNamedButton("Select","CAccountGUISelect",self.buttons,0,5)
        app.addTextArea("CAccountGUIText",2,1,2,2,)
        app.addNamedButton("Change","CAccountGUIChange",self.buttons,3,4)
        app.stopSubWindow()
        go.perc+=5

    def DebugGUI(self):
        app.startSubWindow("DebugGUI","Debug GUI")
        self.grid("DebugGUI",4,0,0)
        app.addTextArea("commandBox",0,0,4)
        app.addNamedButton("Send command!","sendCommand",self.execString,1,0)
        app.stopSubWindow()
        go.perc+=10
    
    def buttons(self,btn):
        details = [["Forename",self.firstName],["Surname",self.secondName],["Company",self.company],["Email",self.email],["Password",self.password]]
        if btn == "Admin":
            app.showSubWindow("AdminLoginGUI")
        elif btn == "Account Options":
            if self.loggedIn == True:
                self.accountDetails()
                app.showSubWindow("AccountGUI")
            else:
                print("Please log in first.")
                app.popUp("loginFirst","Please login first to access this.", kind="warning")
                self.entryDefaults()
                app.show()
        elif btn == "About":
            app.popUp("About","This Server Manager was written for an A-level computing project. \n\n\n By Elliot Singer.")
        elif btn == "AccountGUIChange":
            app.showSubWindow("CAccountGUI")
        elif btn == "CAccountGUISelect":
            app.clearTextArea("CAccountGUIText")
            optionBox = app.getOptionBox("Detail")
            if optionBox == None:
                app.setTextArea("CAccountGUIText","Please choose a detail to change.")
            else:
                for i in range(0,5):
                    if optionBox == details[i][0]:
                        app.setTextArea("CAccountGUIText",details[i][1])
        elif btn == "CAccountGUIChange":
            if app.getOptionBox("Detail") == "Password":
                SQL_System.changePassword(self.userID, self.password, app.getTextArea("CAccountGUIText"))
                self.logout()
            else:
                SQL_System.changeDetail(app.getOptionBox("Detail"),app.getTextArea("CAccountGUIText"),self.userID,go.password)
                self.updateDetails()
                app.popUp("Changed", "That detail has been changed!", kind="info")
                print("\nChanged")
                app.hideSubWindow("AccountGUI")
                app.hideSubWindow("CAccountGUI")
        else:
            app.stop()

    def execString(self):
        exec(str(app.getTextArea("commandBox")))

    def updateDetails(self):
        D = SQL_System.userDetails(self.userID,self.password)
        go.firstName = D[0]
        go.secondName = D[1]
        go.company = D[2]
        go.email = D[3]

    def admin(self):
        if app.getEntry("Password") == "1234":
            app.clearEntry("Password")
            app.hideSubWindow("AdminLoginGUI")
            app.showSubWindow("DebugGUI")
        else:
            app.clearEntry("Password")
            print("Wrong password.")
            app.popUp("Wrong admin password!", "The admin debugging password you entered was wrong", kind="warning")
        
    def updateMeter(self):
        if self.perc < 0:
            for i in range(0,len(windows)):
                exec(windows[i])
            go.perc+=10
        if self.perc == 100:
            self.time+=1
            app.hideMeter("startLoading")
            if self.time == 5:
                app.addToolbar(["Admin","Account Options","About","Exit"],self.buttons)
                app.hideLabel("MainGUILoaded")
                app.showLabel("MainGUITime")
                app.addNamedButton("Sign Up!","MainGUISignUp", self.callSignUp,4,1,2)
                app.addNamedButton("Login!","MainGUILogin", self.callLogin,4,3,2)
                app.addTextArea("guideBox",1,1,4,3,final)
                return
        sleep(1)
        self.updateMeter()

    def timeUpdate(self):
        if self.perc != 100:
            app.setMeter("startLoading", self.perc)
        time = str(datetime.datetime.now().time())
        app.setLabel("MainGUITime",time[0:8])

    def callSignUp(self):
        if go.loggedIn == False:
            GUI.entryDefaults("SignUpGUI")
            app.showSubWindow("SignUpGUI")
        else:
            app.showSubWindow("SMGUI")

    def callLogin(self):
        if go.loggedIn == False:
            GUI.entryDefaults("LoginGUI")
            app.showSubWindow("LoginGUI")
        else:
            app.showSubWindow("SMGUI")
        
    def prepare(self):
        self.grid("MainGUI",6,0,0)
        app.addLabel("MainGUILoaded","All loaded!",2,2,2,2)
        app.addLabel("MainGUITime:","Time:",5,1,2)
        app.addLabel("MainGUITime","Loading...",5,3,2)
        app.addLabel("MainGUITitle","Server Manager",0,1,4)
        app.getLabelWidget("MainGUITitle").config(font=("Nothing", "32", "normal"))
        app.addMeter("startLoading",2,1,4,2)
        app.setMeterFill("startLoading", "DeepSkyBlue")
        app.registerEvent(self.timeUpdate)
        app.setPollTime(1000)
        thread = threading.Thread(target=self.updateMeter)
        thread.daemon = True       
        thread.start()
        app.setLocation(xx-50,yy+50)
                  
    def startMain(self):
        try:
            global app
            app = gui("Server Manager - Main", "800x500", showIcon=False)
            self.prepare()
            app.setLogLevel("ERROR")
            app.go()
        except Exception as error:
            f = open("errorLog.txt","a")
            f.write("------ New Error: ------\n")
            f.write(error)
            f.write("------ Error done ------\n")
            f.close()

    class SignUpGUI:

        def get():
            D = []
            userID = ""
            usern = str(app.getEntry("username"))
            firstn = str(app.getEntry("firstName"))
            secondn = str(app.getEntry("secondName"))
            company = str(app.getEntry("company"))
            email = str(app.getEntry("email"))
            emailc = str(app.getEntry("emailc"))
            password = str(app.getEntry("password"))
            passwordc = str(app.getEntry("passwordc"))
            dBoxes = [usern,firstn,secondn,company,email,emailc,password,passwordc,userID]
            dBoxes[8] = SQL_System.generateRandomCode()
            for i in range(0,9):
                D.append(dBoxes[i])
            GUI.password = password
            return(D)
        
        def submit():
            D = GUI.SignUpGUI.get()
            T1 = 0
            T2 = False
            T3 = False
            box = ["username","firstName","secondName","company","email","password"]
            for i in range(0,4):
                if len(D[i]) > 30:
                    print("Please make sure your entry in box",str(i+1), "is 30 or less.")
                    print("You are currently",str(len(D[i])-30),"characters over.")
                    app.setEntryBg(box[i], "Red")
                    T1+=1
                elif D[i] == '':
                    app.setEntryBg(box[i], "Red")
                    print("You have not entered anything in box number", str(i+1)+".")
                    T1+=1
                else:
                    app.setEntryBg(box[i], "White")
            if D[6] != D[7] or D[6] == '':
                app.popUp("Password error!", "The passwords you have entered do not match.", kind="warning")
                print("Passwords do not match.")
                app.setEntryBg("password", "Red")
                app.setEntryBg("passwordc", "Red")
            else:
                app.setEntryBg("password", "White")
                app.setEntryBg("passwordc", "White")
                T2 = True
                
            if D[4] != D[5] or D[4] == '' or "@" not in D[5] and "@" not in D[4]:
                app.popUp("Email error", "The emails you have entered do not match.", kind="warning")
                print("Emails either do not match or are not valid.")
                app.setEntryBg("email", "Red")
                app.setEntryBg("emailc", "Red")
            else:
                app.setEntryBg("email", "White")
                app.setEntryBg("emailc", "White")
                T3 =  True
            
            if T1 == 0 and T2 == True and T3 == True:
                if SQL_System.newUser(D) == "Exis":
                    app.popUp("Username", "The username: "+D[0]+" already exists, please choose a different one.", kind="error")
                    app.showSubWindow("SignUpGUI")
                    print("\nThis username already exists.\n")
                else:
                    print("Added")
                    app.popUp("Added", "You've been added to the system!", kind="info")
                    app.hideSubWindow("SignUpGUI")
                    app.clearAllEntries()
                    app.showSubWindow("LoginGUI")
                    GUI.entryDefaults("LoginGUI")
            else:
                app.popUp("Error on form.", "You have either missed a box or one is more than 30 characters.\nThe console has more details", kind="warning")
    
        def back():
            app.hideSubWindow("SignUpGUI")
            app.show()

        def prepare(self):
            self.grid("SignUpGUI",9,3,0)
            app.setSticky("news")
            app.setExpand("both")
            app.setFont(8)
            app.setSize(900,550)
            app.setLocation(xx,yy)
            app.addLabel("SignUpGUITitle","Please enter your details", 0, 2, 5)
            app.addEntry("username", 2,1,3)
            app.addEntry("firstName", 4,1,3)
            app.addEntry("secondName", 4,5,3)
            app.addEntry("company", 2,5,3)
            app.addEntry("email", 6,1,3)
            app.addEntry("emailc", 6,5,3)
            app.addSecretEntry("password", 8,1,3)
            app.addSecretEntry("passwordc", 8,5,3)
            app.addNamedButton("Submit","SignUpGUISubmit", self.SignUpGUI.submit, 10, 3, 3)
            app.getLabelWidget("SignUpGUITitle").config(font=("Nothing", "32", "normal"))
            app.getEntryWidget("username").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("firstName").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("secondName").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("company").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("email").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("emailc").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("password").config(font=("Nothing", "18", "normal"))
            app.getEntryWidget("passwordc").config(font=("Nothing", "18", "normal"))
            app.getButtonWidget("SignUpGUISubmit").config(font=("Nothing", "18", "normal"))
            app.addNamedButton("Back","SignUpGUIBack",self.SignUpGUI.back,10,1)
            app.setButtonRelief("SignUpGUIBack", "flat")
            app.setButtonRelief("SignUpGUISubmit", "flat")
            self.colour("SignUpGUI","DeepSkyBlue",9,3,0)

        def start(self):
            app.startSubWindow("SignUpGUI", "Server Manager - Sign Up", modal=True)
            self.SignUpGUI.prepare(self)
            app.stopSubWindow()
            go.perc+=10
        
    class LoginGUI:
        def loginButton():
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
                go.firstName = D[0]
                go.secondName = D[1]
                go.company = D[2]
                go.email = D[3]
                app.hideSubWindow("LoginGUI")
                GUI.ManagerGUI.loggedIn(username,L[1])
            
            else:
                print("\nUsername or password not recognised.")
                app.popUp("Unknown PW / UN", "Username or password not recognised.", kind="warning")
                app.setEntryBg("LoginGUIUsername","Red")
                app.setEntryBg("LoginGUIPassword","Red")

        def back():
            app.hideSubWindow("LoginGUI")
            app.show()

        def prepare(self):
            self.grid("LoginGUI",9,0,0)
            app.setSticky("news")
            app.setExpand("both")
            app.setFont(8)
            app.setSize(800,500)
            app.setLocation(xx,yy)
            app.addEntry("LoginGUIUsername", 3, 3, 3)
            app.setEntryRelief("LoginGUIUsername", "flat")
            app.getEntryWidget("LoginGUIUsername").config(font=("Nothing", "18", "normal"))
            app.addSecretEntry("LoginGUIPassword", 5, 3, 3)
            app.setEntryRelief("LoginGUIPassword", "flat")
            app.getEntryWidget("LoginGUIPassword").config(font=("Nothing", "18", "normal"))
            app.addNamedButton("Login","LoginGUILoginB", self.LoginGUI.loginButton, 7, 4)
            app.setButtonRelief("LoginGUILoginB", "flat")
            app.getButtonWidget("LoginGUILoginB").config(font=("Nothing", "16", "normal"))
            app.addNamedButton("Login","LoginGUIForgotB", self.LoginGUI.loginButton, 7, 4)
            app.setButtonRelief("LoginGUIForgotB", "flat")
            app.getButtonWidget("LoginGUIForgotB").config(font=("Nothing", "16", "normal"))
            app.addLabel("LoginGUITitle", "Server Manager", 2, 3, 3)
            app.getLabelWidget("LoginGUITitle").config(font=("Nothing", "32", "normal"))
            app.setLabelFg("LoginGUITitle", "white")
            app.addNamedButton("Back","LoginGUIBack", self.LoginGUI.back,7,1)
            app.setButtonRelief("LoginGUIBack", "flat")
            self.colour("LoginGUI","DeepSkyBlue",9,0,0)

        def start(self):
            app.startSubWindow("LoginGUI", "Server Manager - Login")
            self.LoginGUI.prepare(self)
            sleep(2)
            app.stopSubWindow()
            go.perc+=20

    class ManagerGUI:

        global labels
        global sLabels
        
        def details(row):
            serverID = app.getTableRow("devices", row)
            info = SQL_System.searchDevicesByServerID(serverID[0], go.password)
            print(info)
            app.showSubWindow("Details")
            for i in range (0,len(labels)):
                if i == 0:
                    app.setLabel("details"+labels[i][0], info[i])
                if i == 6:
                    app.setTextArea("detailsPurpose", info[i+1])
                else:
                    app.setLabel("details"+labels[i][0], info[i+1])

        def status(row):
            serverID = app.getTableRow("devicesStatus", row)
            info = SQL_System.deviceStatus(serverID[0], go.password)
            if info[6] == "Y":
                emails = True
            else:
                emails = False
            if info[4] == "Down":
                app.setLabelBg("State:","Red")
                app.setLabel("State:", "Down")
            elif info[4] == "Up":
                app.setLabelBg("State:","LimeGreen")
                app.setLabel("State:", "Up")
            elif info[4] == "Unknown":
                app.setLabelBg("State:","Orange")
                app.setLabel("State:", "Unknown")
            for i in range(0,len(sLabels)):
                if i == 4:
                    app.setCheckBox("email", ticked=emails)
                else:
                    app.setLabel(sLabels[i][0], info[i+2])
            app.showSubWindow("Status")


        def dbtable(table, type):
            if table == "devicesStatus":
                start = 'app.addTable("devicesStatus",[["ServerID","Name", "IP","Type","Status"]'
                end = '],1,0,10,7, action=GUI.ManagerGUI.status,actionHeading="Status...", actionButton="Status")'
                info = SQL_System.searchDevicesByUserID(go.userID, "Y", go.password, type)
            elif table == "devices":
                start = 'app.addTable("devices",[["ServerID","Name", "IP","Type"]'
                end = '],1,0,10,7, action=GUI.ManagerGUI.details,actionHeading="Details...", actionButton="Details")'
                info = SQL_System.searchDevicesByUserID(go.userID, "N", go.password, type)
            elif table == "removeDevices":
                start = 'app.addTable("removeDevices",[["ServerID","Name", "IP","Type"]'
                end = '],1,0,10,7, action=GUI.ManagerGUI.remove,actionHeading="Remove...", actionButton="Remove")'
                info = SQL_System.searchDevicesByUserID(go.userID, "N", go.password,  type)
            for i in range(len(info)):
                start+=",info["+str(i)+"]"
            final = start+end
            return(final, info)

        def press(row):
            info = app.getTableRow("g1", row)

        def hide(btn):
            if btn == "StatusCLOSE":
                app.hideSubWindow("Status")
                choice = app.getCheckBox("email")
                serverID = app.getLabel("serverID:")
                SQL_System.emailChoice(choice, serverID)
                app.showSubWindow("SMGUI")
            elif btn == "LogoutGUINo":
                app.hideSubWindow("LogoutGUI")
                app.showSubWindow("SMGUI")
            else:
                app.hideSubWindow("Details")
                app.showSubWindow("SMGUI")
                app.clearTextArea("detailsPurpose")

        def detailsBox(self):
            app.startSubWindow("Details",modal=True)
            self.grid("",10,0,0)
            app.setSticky("news")
            app.setExpand("both")
            app.setFont(10)
            app.setSize(850, 550)
            app.setLocation(xx,yy)
            app.addNamedButton("CLOSE", "detailsClose",GUI.ManagerGUI.hide,9,1,8)
            for i in range(0,len(labels)):
                if i != 6:
                    app.addLabel(labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
                    app.addLabel("details"+labels[i][0],"", labels[i][5],labels[i][6],labels[i][7],labels[i][8])
                else:
                    app.addLabel(labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
                    app.addScrolledTextArea("details"+labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8],text=None)
            app.stopSubWindow()

        def statusBox(self):
            app.startSubWindow("Status",modal=True)
            app.setSticky("news")
            app.setExpand("both")
            app.setFont(16)
            app.setSize(700, 500)
            app.setLocation(xx,yy)
            self.grid("s0",5, 0,2)
            for i in range(0,len(sLabels)):
                app.addLabel("Status"+sLabels[i][0], sLabels[i][0],sLabels[i][1],sLabels[i][2],sLabels[i][3],sLabels[i][4])
                if i != 4:
                    app.addLabel(sLabels[i][0], "",sLabels[i][5],sLabels[i][6],sLabels[i][7],sLabels[i][8])
                else:
                    app.addNamedCheckBox("", "email",sLabels[i][5],sLabels[i][6],sLabels[i][7],sLabels[i][8])
            app.addNamedButton("CLOSE", "StatusCLOSE",GUI.ManagerGUI.hide,4,0,2)
            app.stopSubWindow()
            
        def close():
            app.stop()

        def refresh(btn):
            if btn == "StatusRefresh":
                tab = "Status"
                table = "devicesStatus"
                optionbox = "StatusOptions"
                type = app.getOptionBox("StatusOptions")
            elif btn == "ViewDetRefresh":
                tab = "View Details"
                table = "devices"
                optionbox = "ViewDetOptions"
                type = app.getOptionBox("ViewDetOptions")
            elif btn == "removeRefresh":
                tab = "Remove"
                table = "removeDevices"
                optionbox = "removeOptions"
                type = app.getOptionBox("removeOptions")
            elif btn == "editRefresh":
                tab = "Edit"
                optionbox = "editDevices"
                app.changeOptionBox("editDevices",["- Will be filled with your devices -"])
                type = app.getOptionBox("selectDevices")
                info = SQL_System.searchDevicesByUserID(go.userID, "N", go.password, type)
                final = []
                if type != None:
                    for i in range(0,len(info)):
                        temp = ""
                        for x in range(0,3):
                            temp += " "+str(info[i][x])+" "
                        final.append(temp)
                    len(final)
                    if len(final) != 0:
                        app.changeOptionBox("editDevices", final)
                return
            
            elif btn == "statsRefresh":
                pieCharts = [["statsPieAll","All"],["statsPieServer","Server"],["statsPieSwitch","Switch"],["statsPiePrinter","Printer"],["statsPieComputer","Computer"],["Up","Down","Unknown"]]
                perc = GUI.ManagerGUI.stats("All")
                app.setLabel("statsUpNum",perc[0])
                app.setLabel("statsDownNum",perc[1])
                app.setLabel("statsUnknNum",perc[2])
                app.setLabel("statsTotalNum",perc[3])
                for i in range(0,5):
                    if go.loggedIn == False:
                        perc = [0,0,0,-1]
                    else:
                        perc = GUI.ManagerGUI.stats(pieCharts[i][1])
                    for y in range(0,3):
                        if perc[0] == 0 and perc[1] == 0 and perc[2] == 0:
                            perc = [0,0,0,-1]
                            y=3
                        elif perc[y] == 0:
                            perc[y] = 0.00001
                    for x in range(0,3):
                        try:
                            app.setPieChart(pieCharts[i][0],pieCharts[5][x],((perc[x]/perc[3])*100))
                        except:
                            pass
                return
            app.openTab("ManagerGUITabs", tab)
            option = app.getOptionBox(optionbox)
            try:
                app.removeTable(table)
            except:
                pass
            data = GUI.ManagerGUI.dbtable(table, type)
            info = data[1]
            exec(str(data[0])) # This uses info when exectuing the code.

        def AddDevice():
            D = []
            for i in range(1,len(labels)):
                if i == 6:
                    if app.getTextArea("AddPurpose") == '':
                        app.setTextAreaBg("AddPurpose","#ff6262")
                    else:
                        app.setTextAreaBg("AddPurpose","White")
                        D.append(app.getTextArea("AddPurpose"))
                elif i == 3:
                    if app.getOptionBox("addType") == None:
                        pass
                    else:
                        D.append(app.getOptionBox("addType"))
                else:
                    if app.getEntry("Add"+labels[i][0]) == '':
                        app.setEntryBg("Add"+labels[i][0],"#ff6262")
                    else:
                        app.setEntryBg("Add"+labels[i][0],"White")
                        D.append(app.getEntry("Add"+labels[i][0]))
            if len(D) == 9:
                app.popUp("Submitted!", "Your device has been added!", kind="info")
                print("\nAll filled in! Your device has been added!")
                SQL_System.newDevice(D,go.userID,go.password)
                app.clearAllEntries()
                app.clearAllTextAreas()
                app.clearAllOptionBoxes()
            else:
                app.popUp("Missed Boxes!", "You have missed some boxes!", kind="warning")
                print("\nYou have missed a few boxes!")

        def editDevice():
            D = []
            for i in range(1,len(labels)):
                if i == 6:
                    if app.getTextArea("editPurpose") == '':
                        app.setTextAreaBg("editPurpose","#ff6262")
                    else:
                        app.setTextAreaBg("editPurpose","White")
                        D.append(app.getTextArea("editPurpose"))
                elif i == 3:
                    if app.getOptionBox("editType") == None:
                        pass
                    else:
                        D.append(app.getOptionBox("editType"))
                else:
                    if app.getEntry("edit"+labels[i][0]) == '':
                        app.setEntryBg("edit"+labels[i][0],"#ff6262")
                    else:
                        app.setEntryBg("edit"+labels[i][0],"White")
                        D.append(app.getEntry("edit"+labels[i][0]))
            if len(D) == 9 and app.getOptionBox("editDevices") != None:
                app.popUp("Submitted!", "Your device has been updated!", kind="info")
                print("\nAll filled in! Your device has been updated!")
                optionBox = app.getOptionBox("editDevices")
                app.clearAllEntries()
                app.clearAllTextAreas()
                app.clearAllOptionBoxes()
                app.changeOptionBox("editDevices",["- Will be filled with your devices -"])
                SQL_System.updateDevice(D,optionBox[0:9],go.password)
            else:
                app.popUp("Missed Boxes!", "You have missed some boxes!", kind="warning")
                print("\nYou have missed a few boxes!")

        def remove(row):
            serverID = app.getTableRow("removeDevices", row)
            SQL_System.removeDevice(serverID[0])
            app.deleteTableRow("removeDevices", row)

        def edit(btn):
            optionBox = app.getOptionBox("editDevices")
            if optionBox != None:
                serverID = optionBox[0:9]
                info = SQL_System.searchDevicesByServerID(serverID, go.password)
                for i in range(1,len(labels)):
                    if i == 3:
                        app.changeOptionBox("editType",modifyOpt)
                    elif i == 6:
                        app.clearTextArea("editPurpose")
                        app.setTextArea("editPurpose",info[i+1])
                    else:
                        app.setEntry("edit"+labels[i][0],info[i+1])

        def stats(type):
            up = 0
            down = 0
            unkn = 0
            total = 0
            if type == "All":
                status  = SQL_System.searchStatusByuserID(go.userID)
            else:
                status = SQL_System.searchStatusByuserIDType(go.userID, type, go.password)
            for i in range(0,len(status)):
                if status[i][1] == "Up":
                    up+=1
                elif status[i][1] == "Down":
                    down+=1
                else:
                    unkn+=1
            total = up+down+unkn
            if len(status) == 0:
                return [0,0,0,-1]
            return [up,down,unkn,total]

        def prepare(self):
            app.setTransparency(99)
            app.setSticky("news")
            app.setExpand("both")
            app.setFont(16)
            app.setSize(900,600)
            app.setLocation(xx,yy)
            app.startTabbedFrame("ManagerGUITabs")
            app.setTabbedFrameTabExpand("ManagerGUITabs", expand=True)
            app.startTab("Status")
            self.grid("t0", 9,0,0)
            app.addLabelOptionBox("StatusOptions", opt,0,0,8)
            app.setLabel("StatusOptions","Options")
            app.addNamedButton("Refresh","StatusRefresh",self.ManagerGUI.refresh,0,8,2)
            app.addTable("devicesStatus",[["Select"]],1,0,10,7)
            app.stopTab()

            
            app.startTab("View Details")
            self.grid("t1",9,0,0)
            app.addLabelOptionBox("ViewDetOptions", opt,0,0,8)
            app.setLabel("ViewDetOptions","Options")
            app.addNamedButton("Refresh","ViewDetRefresh",self.ManagerGUI.refresh,0,8,2)
            app.addTable("devices",[["Select"]],1,0,10,7)
            app.stopTab()

            app.startTab("Add")
            self.grid("t2",9,0,0)
            app.setSticky("news")
            app.setExpand("both")
            for i in range(1,len(labels)):
                app.addLabel("Ad"+labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
                if i == 6:
                    app.addScrolledTextArea("AddPurpose",7,2,7,2)
                elif i == 3:
                    app.addOptionBox("addType", modifyOpt,4,2,2,0)
                else:
                    app.addEntry("Add"+labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8])
            app.addNamedButton("Close","AddClose",self.ManagerGUI.close,9,0,2)
            app.addNamedButton("Submit","addSubmit", self.ManagerGUI.AddDevice,9,9,2)
            app.addLabel("Details","Please enter your details.",0,3,5,2)
            app.stopTab()

            app.startTab("Edit")
            self.grid("t3",9,0,0)
            app.setSticky("news")
            app.setExpand("both")
            app.addOptionBox("selectDevices", opt, 0,0,8,)
            app.addOptionBox("editDevices", ["- Will be filled with your devices -"], 1,0,8,)
            app.addNamedButton("Refresh", "editRefresh", self.ManagerGUI.refresh,0,8,2)
            app.addNamedButton("Select", "editSelect", self.ManagerGUI.edit,1,8,2)
            for i in range(1,len(labels)):
                app.addLabel("edit"+labels[i][0], labels[i][0]+":",labels[i][1]+1,labels[i][2],labels[i][3],labels[i][4])
                if i == 6:
                    app.addScrolledTextArea("editPurpose",8,2,7)
                elif i == 3:
                    app.addOptionBox("editType", modifyOpt,5,2,2,0)
                    pass
                else:
                    app.addEntry("edit"+labels[i][0], labels[i][5]+1,labels[i][6],labels[i][7],labels[i][8])
            app.addNamedButton("Close","editClose",self.ManagerGUI.close,9,0,2)
            app.addNamedButton("Submit","editSubmit", self.ManagerGUI.editDevice,9,9,2)
            app.stopTab()

            app.startTab("Remove")
            self.grid("t4",9,0,-1)
            app.setSticky("news")
            app.setExpand("both")
            app.addLabelOptionBox("removeOptions", opt,0,0,8)
            app.setLabel("removeOptions","Options")
            app.addNamedButton("Refresh","removeRefresh",self.ManagerGUI.refresh,0,8,2)
            app.addTable("removeDevices",[["Select"]],1,0,10,7)
            app.stopTab()
            
            app.startTab("Stats")
            self.grid("t5",7,1,0)
            app.addNamedButton("Refresh","statsRefresh",self.ManagerGUI.refresh,2,4,2)
            app.addPieChart("statsPieAll", {"Up":(1), "Down":(1), "Unknown":(1)},0,4,2,2)
            app.addPieChart("statsPieServer", {"Up":(1), "Down":(1), "Unknown":(1)},0,0,2,2)
            app.addLabel("typeServer","Servers",2,0,2)
            app.addPieChart("statsPieSwitch", {"Up":(1), "Down":(1), "Unknown":(1)},0,2,2,2)
            app.addLabel("typeSwitch","Switches",2,2,2)
            app.addPieChart("statsPiePrinter", {"Up":(1), "Down":(1), "Unknown":(1)},3,0,2,2)
            app.addLabel("typePrinter","Printers",5,0,2)
            app.addPieChart("statsPieComputer", {"Up":(1), "Down":(1), "Unknown":(1)},3,2,2,2)
            app.addLabel("typeComputer","Computers",5,2,2)
            app.addLabel("statsUp","Up:",3,4)
            app.addLabel("statsUpNum",1,3,5)
            app.addLabel("statsDown","Down:",4,4)
            app.addLabel("statsDownNum",1,4,5)
            app.addLabel("statsUnkn","Unknown:",5,4)
            app.addLabel("statsUnknNum",1,5,5)
            app.addLabel("statsTotal","Total:",6,4)
            app.addLabel("statsTotalNum", 1,6,5)
            app.stopTab()

            app.startTab("Logout")
            self.grid("t6",9,0,0)
            app.setSticky("news")
            app.setExpand("both")
            app.addNamedButton("Logout!","ManagerGUILogoout",self.ManagerGUI.logoutButton,2,2,5,5)
            app.stopTab()
            app.stopTabbedFrame()

        def options(press):
            if press == "Exit":
                app.stop()
                quit()
            else:
                tools()
            
        def logoutButton():
            logout = app.yesNoBox("Logout?","Are you sure you want to logout?")
            if logout == True:
                go.logout()
            else:
                pass
            
        def start(self):
            app.startSubWindow("SMGUI", "Server Manager")
            self.ManagerGUI.detailsBox(self)
            self.ManagerGUI.statusBox(self)
            self.ManagerGUI.prepare(self)
            self.ManagerGUI.refresh("statsRefresh")
            app.stopSubWindow()
            go.perc+=30

        def loggedIn(username,userID):
            app.setTabbedFrameSelectedTab("ManagerGUITabs", "Add")
            app.showSubWindow("SMGUI")
            go.username = username
            go.userID = userID
            go.loggedIn = True

go = GUI("INITIALSTART","710273511",False)
go.startMain()