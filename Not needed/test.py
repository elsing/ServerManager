from appJar import gui 
app = gui("Server Manager - Servers", "800x500")
app.setSticky("news")
app.setExpand("both")

def Grid(diff,size):
    for r in range(0,size):
        for c in range(0,size):
            grid = diff+"r"+str(r)+"c"+str(c)
            name= "row="+str(r)+"\ncolumn="+str(c)
            app.addLabel(grid, grid, r, c)

Grid("t1",6)
app.addTable("g1",
[["ServerID", "IP", "Brand","Purpose","CPU(s)","RAM"],
["Fred", 45, "Male"],
["Tina", 37, "Female"],
["Clive", 28, "Male"],
["Betty", 51, "Female"]],0,0,6,5, action=None, addRow=None,showMenu=True,actionHeading="Remove")

app.go()
