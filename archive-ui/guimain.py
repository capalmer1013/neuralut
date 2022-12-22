import tkinter as tk
from tkinter import filedialog as fd
from tkinter import * 
from tkinter.ttk import *
import tkinter
from PIL import Image, ImageTk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import main
#root = tkinter.Tk()
def callback():
    filename= fd.askopenfilename() 
    if main.isSupported(filename):
        print("valid file")
        # Create a photoimage object of the image in the path
        image1 = Image.open(filename)
        image1.thumbnail((200,200), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)

        label1 = tk.Label(image=test)
        label1.image = test

        # Position image
        label1.place(x=0, y=0)
        drawFigure(main.displayCube(main.makeCube(filename)))
    else:
        print("invalid file")
    print(filename)
    
errmsg = 'Error!'
#tk.Button(text='Click to Open File', command=callback).pack(fill=tk.X)
master = Tk()
def setupGUI():
    tk.Button(text='Click to Open File', command=callback).pack(fill=tk.X)
    # by keyboard or mouse interrupt

def drawFigure(fig):
    canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, master)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    button = tkinter.Button(master=master, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)

def _quit():
    master.quit()     # stops mainloop
    master.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

master.protocol("WM_DELETE_WINDOW", _quit)
setupGUI()
mainloop()