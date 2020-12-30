from appJar import gui
from SQL_System import *
import random as r

def __main__(username,userID,statusb):
    global Details
    global Status
    

    def Details(row):
        serverID = app.getTableRow("devices", row)
        info = SQL_System.SearchDevicesByServerID(serverID[0])
        app.showSubWindow("Details")
        for i in range (0,len(labels)):
            app.setLabel(labels[i][0], info[0][i+1])

    def Status():
        pass
    
    def dbtable(info,table):
        if table == "devicesstatus":
            start = 'app.addTable("devicesstatus",[["ServerID","Name", "IP","Type"]'
            end = '],1,0,10,7, action=Status,actionHeading="Status...", actionButton="Status")'
        elif table == "devices":
            start = 'app.addTable("devices",[["ServerID","Name", "IP","Type"]'
            end = '],1,0,10,7, action=Details,actionHeading="Details...", actionButton="Details")'
        for i in range(len(info)):
            start+=",info["+str(i)+"]"
        final = start+end
        return(final)

    def StatusBar(statusb):
            app.addStatusbar(fields=3)
            app.setStatusbar("Logged in? "+ statusb[0], 0)
            app.setStatusbar("Name: "+ statusb[1], 1)
            app.setStatusbar("Company: "+ statusb[2], 2)

    def Grid(diff,sizem,offsetr,offsetc):
        for r in range(0,size+offsetr):
            for c in range(0,size+offsetc):
                grid = diff+"r"+str(r)+"c"+str(c)
                name= "row="+str(r)+"\ncolumn="+str(c)
                app.addLabel(grid, "", r, c)

    def press(row):
        info = app.getTableRow("g1", row)

    def devices():
        info = SQL_System.SearchDevicesByUserID(userID)
        return info

    def hide():
        app.hideSubWindow("Details")
        
    def DetailsBox():
        app.startSubWindow("Details")
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(16)
        app.setSize(700, 500)
        Grid("",8, 0,1)
        for i in range(0,len(labels)):
            app.addLabel("l"+labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
            app.addLabel(labels[i][0], "",labels[i][5],labels[i][6],labels[i][7],labels[i][8])
        app.addNamedButton("CLOSE", "CLOSE",hide,8,0,2)
        app.stopSubWindow()

    def close():
        app.stop()

    def refresh(btn):
        if btn == "StatusRefresh":
            tab = "Status"
            table = "devicesstatus"
            optionbox = "StatusOptions"
        elif btn == "ViewDetRefresh":
            tab = "View Details"
            table = "devices"
            optionbox = "ViewDetOptions"
        info = devices()
        app.openTab("Tabs", tab)
        option = app.getOptionBox(optionbox)
        try:
            app.removeTable(table)
        except:
            pass
        exec(str(dbtable(info,table)))
        rows = app.getTableRowCount(table)
        if option != "All" and option != "Server" and option != "Switch":
            app.deleteAllTableRows(table)
        elif option == "All":
            pass
        elif option == "Server":
            for i in range(rows):
                row = app.getTableRow(table, i)
                if row[3] != "Server":
                    app.deleteTableRow(table, i)
        elif option == "Switch":
            for i in reversed(range(rows)):
                row = app.getTableRow(table, i)
                if row[3] != "Switch":
                    app.deleteTableRow(table, i)
        else:
            app.deleteAllTableRows(table)

    def AddDevice():
        D = []
        print(app.getTextArea("AddPurpose"))
        for i in range(1,len(labels)):
            if i == 6:
                if app.getTextArea("AddPurpose") == '':
                    app.setTextAreaBg("AddPurpose","Red")
                else:
                    app.setTextAreaBg("AddPurpose","White")
                    D.append(app.getTextArea("AddPurpose"))
            else:
                if app.getEntry("Add"+labels[i][0]) == '':
                    app.setEntryBg("Add"+labels[i][0],"Red")
                else:
                    app.setEntryBg("Add"+labels[i][0],"White")
                    D.append(app.getEntry("Add"+labels[i][0]))
        if len(D) == 9:
            print("\nAll filled in!")
            SQL_System.NewDevice(D,userID)
            app.clearAllEntries()
            app.clearAllTextAreas()
        else:
            print("\nYou have missed a few boxes!")
            

    def tabs():
        app.startTabbedFrame("Tabs")
        app.setTabbedFrameTabExpand("Tabs", expand=True)

        app.startTab("Status")
        Grid("t0", 9,0,0)
        app.addLabelOptionBox("StatusOptions", opt,0,0,8)
        app.setLabel("StatusOptions","Options")
        app.addNamedButton("Refresh","StatusRefresh",refresh,0,8,2)
        app.addNamedButton("Close","StatusClose",close,8,0)
        app.addTable("devicesstatus",[["Select"]],1,0,10,7)
        app.stopTab()

        
        app.startTab("View Details")
        Grid("t1",9,0,0)
        app.addLabelOptionBox("ViewDetOptions", opt,0,0,8)
        app.setLabel("ViewDetOptions","Options")
        app.addNamedButton("Refresh","ViewDetRefresh",refresh,0,8,2)
        app.addNamedButton("Close","ViewDetClose",close,8,0)
        app.addTable("devices",[["Select"]],1,0,10,7)
        app.stopTab()

        app.startTab("Add")
        Grid("t2",8,1,2)
        app.setSticky("news")
        app.setExpand("both")
        for i in range(1,len(labels)):
            app.addLabel("Ad"+labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
            if i == 6:
                app.addScrolledTextArea("AddPurpose",7,2,7,2)
            else:
                app.addEntry("Add"+labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8])
        app.addNamedButton("Close","AddClose",close,9,0,2)
        app.addNamedButton("Submit","AddSubmit", AddDevice,9,9,2)
        app.addLabel("Details","Please enter your details.",0,3,5,2)
        app.stopTab()

        app.startTab("Remove")
        Grid("t3",9,0,0)
        app.addLabel("Change", "This part has not been coded yet.",3,2,5,2)
        app.stopTab()
        app.stopTabbedFrame()

    def Options(press):
        if press == "Exit":
            app.stop()
            quit()
        else:
            tools()

    def Colours(colour):
        for r in range(0,size):
            for c in range(0,size):
                string = str("r"+str(r)+"c"+str(c))
                app.setLabelBg(string, colour)
        app.setBg(colour, override=False, tint=False)

    def tools():
        app.startSubWindow("About")
        app.setSize(400, 400)
        app.addLabel("By", "Created by: \n\nElliot Singer\n")
        app.addLabel("For", "For an A-level project.")
        app.addButton("Exit", Exit)
        app.showSubWindow("About")
        
    app = gui("Server Manager - Servers", "800x500")
    app.setSticky("news")
    app.setExpand("both")
    app.setFont(16)
    size = 9

    fileMenus = ["About","-","Exit"]
    app.addMenuList("Options", fileMenus, Options)
    app.addMenuList("Colours", ["DeepSkyBlue","Blue","Green"], Colours)

    labels = [["serverID",1,1,0,0,1,2,2,0],["Name",2,1,0,0,2,2,2,0],["IP(one)",3,1,0,0,3,2,2,0],["Type",4,1,0,0,4,2,2,0],["Brand",5,1,0,0,5,2,2,0],["Product Line",2,6,0,0,2,7,2,0],["Purpose",7,1,0,0,7,2,6,2],["CPU(s)",3,6,0,0,3,7,2,0],["RAM",4,6,0,0,4,7,2,0],["PSU(s)",5,6,0,0,5,7,2,0]]

    server = [1,"Test","192.168.1.1"]

    opt = ["- Select me -","All","Server","Switch",]
    tabs()
    StatusBar(statusb)
    DetailsBox()
    Colours("DeepSkyBlue")
    app.go()



#__main__("elliot","337965876",["","",""])
