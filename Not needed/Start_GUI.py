from appJar import gui
import pymysql
import Login_GUI
import SignUp_GUI

app = gui("Server Manager - Login", "800x500")
app.setSticky("news")
app.setExpand("both")
app.setFont(8)

size = 8

for r in range(0,size):
    for c in range(0,size):
        grid = "r"+str(r)+"c"+str(c)
        name= "row="+str(r)+"\ncolumn="+str(c)
        app.addLabel(grid, "", r, c)

def Colours(colour):
    for r in range(0,size):
        for c in range(0,size):
            string = str("r"+str(r)+"c"+str(c))
            app.setLabelBg(string, colour)
   # app.setLabelBg("SM", colour)
    app.setBg(colour, override=False, tint=False)

def SignUp():
    app.stop()
    SignUp_GUI.__main__()

def Login():
    app.stop()
    Login_GUI.__main__()
    #app.setStatusbar("test",0)


app.addLabel("SM","Server Manager", 1, 2, 4)
app.addButton("r3c1s2s2", SignUp, 3, 1, 2, 2)
app.addButton("r3c5s2s2", Login, 3, 5, 2, 2)
app.setButton("r3c1s2s2","Sign Up!")
app.setButton("r3c5s2s2","Login!")
app.setLabelFg("SM","white")
app.getLabelWidget("SM").config(font=("Nothing", "32", "normal"))
app.getButtonWidget("r3c1s2s2").config(font=("Nothing", "24", "normal"))
app.getButtonWidget("r3c5s2s2").config(font=("Nothing", "24", "normal"))
app.setButtonRelief("r3c1s2s2", "flat")
app.setButtonRelief("r3c5s2s2", "flat")

Colours("DeepSkyBlue")

app.go()
