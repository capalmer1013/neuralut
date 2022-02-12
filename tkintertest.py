# Python program to create
# a file explorer in Tkinter
from sys import exit
import os.path
# import all components
# from the tkinter library
from tkinter import *
from tkinter.ttk import Progressbar

# import filedialog module
from tkinter import filedialog



from neuralut import api


# Function for opening the
# file explorer window
def browseFiles():
    dir = filedialog.askdirectory()

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + dir)
    doThatExifStuff(dir)


def doThatExifStuff(dirname):
    exifdb = api.DB()
    exifdb.createExifTable()

    validFiles = api.findFiles(dirname+os.path.sep+"**", api.SUPPORTED_FILES)
    print(validFiles)
    p.length = len(validFiles)

    for each in validFiles:
        print(each)
        exifdb.addEntry(api.checkForExif(each), each)
        p.step()
        window.update()

    exifdb.close()

# Create the root window
window = Tk()
# Set window title
window.title('File Explorer')
# Set window size
window.geometry("500x500")
# Set window background color
window.config(background="white")
# Create a File Explorer label
label_file_explorer = Label(window,
                            text="File Explorer using Tkinter",
                            width=100, height=4,
                            fg="blue")

button_explore = Button(window,
                        text="Browse Files",
                        command=browseFiles)

button_exit = Button(window,
                     text="Exit",
                     command=exit)
p = Progressbar(window, orient=HORIZONTAL, length=1000, mode="determinate", takefocus=True, maximum=100)
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=2)

button_exit.grid(column=1, row=3)
p.grid(column=1, row=4)

# Let the window wait for any events
window.mainloop()