# Python program to create
# a file explorer in Tkinter
from sys import exit
import os.path
# import all components
# from the tkinter library
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

# import filedialog module
from tkinter import filedialog

from neuralut import api


def listbox_callback(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print("filename:", data)
        image1 = Image.open(data)
        print(image1)
        image1.thumbnail((1080, 1080), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(image1)
        print(img2)
        # canvas.itemconfig(image_container, image=img2)


class LeftPanel(Frame):
    def __init__(self, parent, ext_canvas, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = ext_canvas
        # Create a File Explorer label
        self.label_file_explorer = Label(self, text="NEURALUT", width=100, height=4, fg="blue")
        self.button_explore = Button(self, text="Browse Files", command=self.browseFiles)
        self.button_exit = Button(self, text="Exit", command=exit)
        self.anotherButton = Button(self, text="load the other one", command=self.loadOtherImage)
        self.p = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate", takefocus=True, maximum=100)
        self.l = Listbox(self)

        self.label_file_explorer.pack(side=TOP)
        self.button_explore.pack(side=TOP)
        self.button_exit.pack(side=TOP)
        self.anotherButton.pack(side=TOP)
        self.p.pack(side=TOP)
        self.l.pack(fill=BOTH, expand=True)

        self.l.bind("<<ListboxSelect>>", listbox_callback)

    # Function for opening the
    # file explorer window
    def browseFiles(self):
        dir = filedialog.askdirectory()

        # Change label contents
        self.label_file_explorer.configure(text="Folder Opened: " + dir)
        self.doThatExifStuff(dir)

    def loadOtherImage(self):
        print("loading other image")
        otherImage = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350483_edited.jpg')
        otherImage.thumbnail((1080, 1080), Image.ANTIALIAS)
        # self.canvas.config(image=ImageTk.PhotoImage(otherImage))
        # window.update()

    def doThatExifStuff(self, dirname):
        exifdb = api.DB()
        exifdb.createExifTable()

        validFiles = api.findFiles(dirname + os.path.sep + "**", api.SUPPORTED_FILES)
        print(validFiles)
        count = 0
        for each in validFiles:
            count += 1
            self.p['value'] = count / len(validFiles) * 100
            print(each)
            exifdb.addEntry(api.checkForExif(each), each)

            window.update()

        for each in exifdb.getUniqueFiles():
            self.l.insert(1, each[0])
        self.l.pack(side=LEFT, fill=BOTH, expand=True)
        window.update()

# Create the root window
root = Tk()
# Set window title
root.title('File Explorer')
# Set window size
#window.geometry("1000x500")
# Set window background color
root.config(background="white")

window = Frame(root)
window.pack()

# frame = Frame(window, relief=RAISED, borderwidth=1, height=1000)
canvas = Canvas(window, width=1000, height=1000)

#image = Image.open("default.png")
image = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350235_edited.jpg')
#image = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350193_edited.jpg')
image.thumbnail((1080, 1080), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
#canvas = Label(window, width=1000, height=1000, image=img)
# python_image = PhotoImage(file='default.png')


# image_container = canvas.create_image(0, 0, anchor=NW, image=img)
frame = LeftPanel(window, canvas, relief=RAISED, borderwidth=1)


# https://www.pythontutorial.net/tkinter/tkinter-listbox/


otherImage = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350193_edited.jpg')
otherImage.thumbnail((1080, 1080), Image.ANTIALIAS)
otherImg = ImageTk.PhotoImage(otherImage)
#canvas.itemconfig(image_id, image=ImageTk.PhotoImage(otherImage))
#canvas.create_image(0, 0, anchor=NW, image=otherImage)

frame.pack(side=LEFT)
canvas.pack(side=RIGHT)

# frame.grid(column=1, row=1, sticky=NS)
# canvas.grid(column=2, row=1)

image_id = canvas.create_image(0, 0, anchor=NW, image=img)
img = otherImg
canvas.itemconfig(image_id, image=img)

# Let the window wait for any events
window.mainloop()