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
    label_file_explorer.configure(text="Folder Opened: " + dir)
    doThatExifStuff(dir)


def doThatExifStuff(dirname):
    exifdb = api.DB()
    exifdb.createExifTable()

    validFiles = api.findFiles(dirname+os.path.sep+"**", api.SUPPORTED_FILES)
    print(validFiles)
    count = 0
    for each in validFiles:
        count += 1
        p['value'] = count/len(validFiles)*100
        print(each)
        exifdb.addEntry(api.checkForExif(each), each)

        window.update()

    for each in exifdb.getUniqueFiles():
        l.insert(1, each[0])
    l.pack(side=LEFT, fill=BOTH, expand=True)
    window.update()

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
p = Progressbar(window, orient=HORIZONTAL, length=100, mode="determinate", takefocus=True, maximum=100)
l = Listbox(window)
# https://www.pythontutorial.net/tkinter/tkinter-listbox/
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
# label_file_explorer.grid(column=1, row=1)
# button_explore.grid(column=1, row=2)
# button_exit.grid(column=1, row=3)
# p.grid(column=1, row=4)
# l.grid(column=1, row=5)

label_file_explorer.pack()
button_explore.pack()
button_exit.pack()
p.pack()
l.pack()

# Let the window wait for any events
window.mainloop()