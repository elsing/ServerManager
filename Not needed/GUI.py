class GUI:

    def CreateBasic():
        from appJar import gui

        def Colours(colour,size):
            from appJar import gui
            for r in range(0,size):
                for c in range(0,size):
                    string = str("r"+str(r)+"c"+str(c))
                    app.setLabelBg(string, colour)
            #app.setLabelBg("SM", colour)
                    
            app.setBg(colour, override=False, tint=False)

        #app = gui(("Server Manager - ", "Test"), "800x500")
        app.setSticky("news")
        app.setExpand("both")
        app.setFont(8)
        size = 9

        for r in range(0,size):
            for c in range(0,size):
                grid = "r"+str(r)+"c"+str(c)
                name= "row="+str(r)+"\ncolumn="+str(c)
                app.addLabel(grid, name, r, c)

        align = size / 3

        #for i in range(0,len(COM)):
        #    exec(COM[i])




    
