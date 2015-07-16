from time import sleep
from Tkinter import *
import multiprocessing
from reciever import recieve
from object_matching import match
            
class Gui(object):
    lst = []
    sz = 0
    
    def __init__(self, Parent, que):
        self.pipe = que
        # Defines the size of the GUI and gives it a title
        self.root = Parent
        self.root.geometry("400x300")
        self.root.title("Vision System")
        
        self.myContainer1 = Frame(self.root)
        self.myContainer1.pack()
        self.readSensor()
     
    def addrow(self):
        self.sz += 1
        name = "Object " + str(self.sz)
        # This label is the name (i.e. Zoe, Inara)
        new_row = Label(self.myContainer1, text = name)
        new_row["width"] = "24"
        new_row["height"] = "2"
        new_row["background"] = "blue"
        new_row["fg"] = "white"

        # This is where the coordinates are
        pos = Label(self.myContainer1, text = "#")
        pos["width"] = "24"
        pos["height"] = "2"
        pos["background"] = "gold"

        new_row.grid(row = self.sz, column = 1)
        pos.grid(row = self.sz, column = 2)
        self.lst.append(pos)

        
    def updateGUI(self):
        self.pos["text"] = "UPDATE"
        self.root.update()
        self.label2.after(1000, self.readSensor)

    def readSensor(self):
        try:
            s = self.pipe.recv()
            idx = match(self.lst, s[1])
            print s[1]
            if (-1 < idx):
                self.lst[idx]["text"] = s[1]
                self.root.update()
            else:
                self.addrow()
                self.lst[self.sz - 1]["text"] = s[1]
        except EOFError:
            pass
        finally:
            sleep(.05)
            self.root.after(1, self.readSensor)

def rungui(q):
    """Runs the gui, and updates it"""
    root = Tk()
    inara = Gui(root, q)
    root.mainloop()
    
# Pipe is used to communicate between threads
stream = multiprocessing.Pipe(False)

# Gui thread
gooey = multiprocessing.Process(target = (rungui), args = (stream[0],))
# LCM reciever thread
in_thread = multiprocessing.Process(target = (recieve), args = (stream[1],))
in_thread.start()
gooey.start()


