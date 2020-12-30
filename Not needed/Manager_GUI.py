from appJar import gui
from SQL_System import *
import random as r
def __main__(username,userID,statusb):
    global details
    global Status
    global Remove
    
    def details(row):
        serverID = app.getTableRow("devices", row)
        info = SQL_System.searchDevicesByServerID(serverID[0])
        app.showSubWindow("Details")
        #app.clearAllTextAreas()
        #print(labels)
        #print(info)
        for i in range (0,len(labels)):
            if i == 0:
                app.setLabel("details"+labels[i][0], info[0][i])
            if i == 6:
                app.setTextArea("detailsPurpose", info[0][i+1])
            else:
                app.setLabel("details"+labels[i][0], info[0][i+1])

    def Status(row):
        serverID = app.getTableRow("devicesStatus", row)
        info = SQL_System.deviceStatus(serverID[0])
        if info [0][6] == "Y":
            emails = True
        else:
            emails = False
        if info[0][4] == "Down":
            app.setLabelBg("State:","Red")
            app.setLabel("State:", "Down")
        elif info[0][4] == "Up":
            app.setLabelBg("State:","LimeGreen")
            app.setLabel("State:", "Up")
        elif info[0][4] == "Unknown":
            app.setLabelBg("State:","Orange")
            app.setLabel("State:", "Unknown")
        for i in range(0,len(sLabels)):
            if i == 4:
                app.setCheckBox("email", ticked=emails)
            else:
                app.setLabel(sLabels[i][0], info[0][i+2])


        app.showSubWindow("Status")
    
    def dbtable(table):
        if table == "devicesStatus":
            start = 'app.addTable("devicesStatus",[["ServerID","Name", "IP","Type","Status"]'
            end = '],1,0,10,7, action=Status,actionHeading="Status...", actionButton="Status")'
            info = SQL_System.searchDevicesByUserID(userID, "Y")
        elif table == "devices":
            start = 'app.addTable("devices",[["ServerID","Name", "IP","Type"]'
            end = '],1,0,10,7, action=details,actionHeading="Details...", actionButton="Details")'
            info = SQL_System.searchDevicesByUserID(userID, "N")
        elif table == "removeDevices":
            start = 'app.addTable("removeDevices",[["ServerID","Name", "IP","Type"]'
            end = '],1,0,10,7, action=Remove,actionHeading="Remove...", actionButton="Remove")'
            info = SQL_System.searchDevicesByUserID(userID, "N")
        for i in range(len(info)):
            start+=",info["+str(i)+"]"
        final = start+end
        return(final, info)

    def statusBar(statusb):
            app.addStatusBar(fields=3)
            app.setStatusBar("Logged in? "+ statusb[0], 0)
            app.setStatusBar("Name: "+ statusb[1], 1)
            app.setStatusBar("Company: "+ statusb[2], 2)

    def grid(diff,sizem,offsetr,offsetc):
        for r in range(0,sizem+offsetr):
            for c in range(0,sizem+offsetc):
                grid = diff+"r"+str(r)+"c"+str(c)
                name= "row="+str(r)+"\ncolumn="+str(c)
                app.addLabel(grid,"", r, c)

    def press(row):
        info = app.getTableRow("g1", row)

    def hide(btn):
        if btn == "StatusCLOSE":
            app.hideSubWindow("Status")
            choice = app.getCheckBox("email")
            serverID = app.getLabel("serverID:")
            SQL_System.emailChoice(choice, serverID)
        else:
            app.hideSubWindow("Details")
            app.clearTextArea("detailsPurpose")        
        
    def detailsBox():
        app.startSubWindow("Details",modal=True)
        grid("",10,0,0)
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(10)
        app.setSize(850, 550)
        app.addNamedButton("CLOSE", "detailsClose",hide,9,1,8)
        #app.addNamedButton("SAVE", "detailsSave",saveDetails,7,10)
        for i in range(0,len(labels)):
            if i != 6:
                app.addLabel(labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
                #app.addScrolledTextArea(labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8],text=None)
                app.addLabel("details"+labels[i][0],"", labels[i][5],labels[i][6],labels[i][7],labels[i][8])
                #app.setLabelBg("details"+labels[i][0],"Blue")
            else:
                app.addLabel(labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
                app.addScrolledTextArea("details"+labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8],text=None)

        app.stopSubWindow()

    def statusBox():
        app.startSubWindow("Status",modal=True)
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(16)
        app.setSize(700, 500)
        grid("s0",5, 0,2)
        for i in range(0,len(sLabels)):
            app.addLabel("Status"+sLabels[i][0], sLabels[i][0],sLabels[i][1],sLabels[i][2],sLabels[i][3],sLabels[i][4])
            if i != 4:
                app.addLabel(sLabels[i][0], "",sLabels[i][5],sLabels[i][6],sLabels[i][7],sLabels[i][8])
            else:
                app.addNamedCheckBox("", "email",sLabels[i][5],sLabels[i][6],sLabels[i][7],sLabels[i][8])
        app.addNamedButton("CLOSE", "StatusCLOSE",hide,4,0,2)
        app.stopSubWindow()

    def close():
        app.stop()

    def refresh(btn):
        if btn == "StatusRefresh":
            tab = "Status"
            table = "devicesStatus"
            optionbox = "StatusOptions"
        elif btn == "ViewDetRefresh":
            tab = "View Details"
            table = "devices"
            optionbox = "ViewDetOptions"
        elif btn == "removeRefresh":
            tab = "Remove"
            table = "removeDevices"
            optionbox = "removeOptions"
        elif btn == "statsRefresh":
            perc = stats(userID)
            app.setLabel("statsUpNum",perc[0])
            app.setLabel("statsDownNum",perc[1])
            app.setLabel("statsUnknNum",perc[2])
            app.setPieChart("statsPie","Up",(perc[0]/perc[3]))
            app.setPieChart("statsPie","Down",(perc[1]/perc[3]))
            app.setPieChart("statsPie","Unknown",(perc[2]/perc[3]))
            return
        app.openTab("Tabs", tab)
        option = app.getOptionBox(optionbox)
        try:
            app.removeTable(table)
        except:
            pass
        data = dbtable(table)
        info = data[1]
        exec(str(data[0]))
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
            elif i == 3:
                if app.getOptionBox("Types") == None:
                    pass
                else:
                    D.append(app.getOptionBox("Types"))
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
            app.clearOptionBox
        else:
            print("\nYou have missed a few boxes!")

    def Remove(row):
        serverID = app.getTableRow("removeDevices", row)
        SQL_System.RemoveDevice(serverID[0])
        app.deleteTableRow("removeDevices", row)

    def stats(userID):
        status  = SQL_System.searchStatusByuserID(userID)
        up = 0
        down = 0
        unkn = 0
        total = 0
        for i in range(0,len(status)):
            if status[i][1] == "Up":
                up+=1
            elif status[i][1] == "Down":
                down+=1
            else:
                unkn+=1
        perc = (up/(up+down+unkn))*100
        total = up+down+unkn
        return [up,down,unkn,total]

    def tabs():
        app.startTabbedFrame("Tabs")
        app.setTabbedFrameTabExpand("Tabs", expand=True)
        app.startTab("Status")
        grid("t0", 9,0,0)
        app.addLabelOptionBox("StatusOptions", opt,0,0,8)
        app.setLabel("StatusOptions","Options")
        app.addNamedButton("Refresh","StatusRefresh",refresh,0,8,2)
        app.addNamedButton("Close","StatusClose",close,8,0)
        app.addTable("devicesStatus",[["Select"]],1,0,10,7)
        app.stopTab()

        
        app.startTab("View Details")
        grid("t1",9,0,0)
        app.addLabelOptionBox("ViewDetOptions", opt,0,0,8)
        app.setLabel("ViewDetOptions","Options")
        app.addNamedButton("Refresh","ViewDetRefresh",refresh,0,8,2)
        app.addNamedButton("Close","ViewDetClose",close,8,0)
        app.addTable("devices",[["Select"]],1,0,10,7)
        app.stopTab()

        app.startTab("Add")
        grid("t2",9,0,1)
        app.setSticky("news")
        app.setExpand("both")
        for i in range(1,len(labels)):
            app.addLabel("Ad"+labels[i][0], labels[i][0]+":",labels[i][1],labels[i][2],labels[i][3],labels[i][4])
            if i == 6:
                app.addScrolledTextArea("AddPurpose",7,2,7,2)
            elif i == 3:
                app.addOptionBox("Types", ["- Please Select -", "Server", "Switch"],4,2,2,0)
                #app.setLabel
            else:
                app.addEntry("Add"+labels[i][0], labels[i][5],labels[i][6],labels[i][7],labels[i][8])
        app.addNamedButton("Close","AddClose",close,9,0,2)
        app.addNamedButton("Submit","AddSubmit", AddDevice,9,9,2)
        app.addLabel("Details","Please enter your details.",0,3,5,2)
        app.stopTab()

        app.startTab("Edit")
        grid("t3",9,0,1)
        app.setSticky("news")
        app.setExpand("both")
        app.stopTab()

        app.startTab("Remove")
        grid("t4",9,0,0)
        app.addLabelOptionBox("removeOptions", opt,0,0,8)
        app.setLabel("removeOptions","Options")
        app.addNamedButton("Refresh","removeRefresh",refresh,0,8,2)
        app.addNamedButton("Close","removeClose",close,8,0)
        app.addTable("removeDevices",[["Select"]],1,0,10,7)
        app.stopTab()

        app.startTab("Stats")
        grid("t5",9,0,0)
        app.addNamedButton("Refresh","statsRefresh",refresh,0,8,2)
        perc = stats(userID) 
        app.addPieChart("statsPie", {"Up":(perc[0]/perc[3]), "Down":(perc[1]/perc[3]), "Unknown":(perc[2]/perc[3])},1,1,4,4)
        app.addLabel("statsUp","Up:",2,6)
        app.addLabel("statsUpNum",perc[0],2,7)
        app.addLabel("statsDown","Down:",3,6)
        app.addLabel("statsDownNum",perc[1],3,7)
        app.addLabel("statsUnkn","Unknown:",4,6)
        app.addLabel("statsUnknNum",perc[2],4,7)
        app.addLabel("statsTotalNum", perc[3],5,7)
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

    labels = [["serverID",1,1,0,0,1,2,2,0],["Name",2,1,0,0,2,2,2,0],["IP(one)",3,1,0,0,3,2,2,0],["Type",4,1,0,0,4,2,2,0],["Brand",5,1,0,0,5,2,2,0],["Product Line",2,6,0,0,2,7,2,0],["Purpose",7,1,0,0,7,2,7,1],["CPU(s)",3,6,0,0,3,7,2,0],["RAM",4,6,0,0,4,7,2,0],["PSU(s)",5,6,0,0,5,7,2,0]]
    sLabels = [["serverID:",1,1,0,0,1,2,1,0],["IP(one):",2,1,0,0,2,2,1,0],["State:",3,1,0,0,3,2,4,0],["Last Checked:",1,4,0,0,1,5,2,0],["Send emails?",2,4,0,0,2,5,2,0]]
    opt = ["- Select me -","All","Server","Switch",]
    
    tabs()
    statusBar(statusb)
    detailsBox()
    statusBox()
    #Colours("DeepSkyBlue")
    app.go()



__main__("elliot","337965876",["","",""])
