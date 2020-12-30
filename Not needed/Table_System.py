class Table_System:
    def moreinfo(row):
        serverID = app.getTableRow("devices", row)
        info = SQL_System.SearchDevicesByServerID(serverID[0])
        app.showSubWindow("moreinfo")
        for i in range (0,len(labels)):
            app.setLabel(labels[i][0], info[0][i+1])

    def Status():
        pass
