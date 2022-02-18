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
    global img
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print("filename:", data)
        image1 = Image.open(data)
        print(image1)
        image1.thumbnail((1080, 1080), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image1)
        canvas.itemconfig(image_id, image=img)


def leftPanel(parent, lboxSelectCallback):
    # Function for opening the
    # file explorer window
    def browseFiles():
        dir = filedialog.askdirectory()

        # Change label contents
        label_file_explorer.configure(text="Folder Opened: " + dir)
        doThatExifStuff(dir)

    def loadOtherImage():
        print("loading other image")
        otherImage = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350483_edited.jpg')
        otherImage.thumbnail((1080, 1080), Image.ANTIALIAS)
        # self.canvas.config(image=ImageTk.PhotoImage(otherImage))
        # window.update()

    def doThatExifStuff(dirname):
        exifdb = api.DB()
        exifdb.createExifTable()

        validFiles = api.findFiles(dirname + os.path.sep + "**", api.SUPPORTED_FILES)
        print(validFiles)
        count = 0
        for each in validFiles:
            count += 1
            p['value'] = count / len(validFiles) * 100
            print(each)
            exifdb.addEntry(api.checkForExif(each), each)

            window.update()

        for each in exifdb.getUniqueFiles():
            l.insert(1, each[0])
        l.pack(side=LEFT, fill=BOTH, expand=True)
        window.update()
    # Create a File Explorer label
    label_file_explorer = Label(parent, text="NEURALUT", width=100, height=4, fg="blue")
    button_explore = Button(parent, text="Browse Files", command=browseFiles)
    button_exit = Button(parent, text="Exit", command=exit)
    anotherButton = Button(parent, text="load the other one", command=loadOtherImage)
    p = Progressbar(parent, orient=HORIZONTAL, length=100, mode="determinate", takefocus=True, maximum=100)
    l = Listbox(parent)

    label_file_explorer.pack(side=TOP)
    button_explore.pack(side=TOP)
    button_exit.pack(side=TOP)
    anotherButton.pack(side=TOP)
    p.pack(side=TOP)
    l.pack(fill=BOTH, expand=True)

    l.bind("<<ListboxSelect>>", lboxSelectCallback)
    return parent




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
image = Image.open('default.png')
#image = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350193_edited.jpg')
image.thumbnail((1080, 1080), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
#canvas = Label(window, width=1000, height=1000, image=img)
# python_image = PhotoImage(file='default.png')


# image_container = canvas.create_image(0, 0, anchor=NW, image=img)
leftFrame = leftPanel(Frame(window, relief=RAISED, borderwidth=1, height=1000), listbox_callback)


# https://www.pythontutorial.net/tkinter/tkinter-listbox/


otherImage = Image.open('C:/Users/Chris Palmer/Desktop/street photos\P1350193_edited.jpg')
otherImage.thumbnail((1080, 1080), Image.ANTIALIAS)
otherImg = ImageTk.PhotoImage(otherImage)
#canvas.itemconfig(image_id, image=ImageTk.PhotoImage(otherImage))
#canvas.create_image(0, 0, anchor=NW, image=otherImage)

#leftFrame.pack(side=LEFT)
#canvas.pack(side=RIGHT)

leftFrame.grid(column=1, row=1, sticky=NS)
canvas.grid(column=2, row=1)

image_id = canvas.create_image(0, 0, anchor=NW, image=img)
# img = otherImg
# canvas.itemconfig(image_id, image=img)

# Let the window wait for any events
window.mainloop()