from appJar import gui
app = gui()

counter = 10

def myLoop():
    print(counter)

def acceleratingCountdown():
    global counter
    if counter > 0:
        #app.setLabel("counter", str(counter))
        counter -= 1
        app.after(100*counter, myLoop)

app.after(10, acceleratingCountdown)

print(counter)
