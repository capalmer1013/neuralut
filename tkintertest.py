from sys import exit
import os.path
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import filedialog

from neuralut import api

IMG_SIZE = (800, 800)


def listbox_callback(event):
    global img
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print("filename:", data)
        image1 = Image.open(data)
        print(image1)
        image1.thumbnail(IMG_SIZE, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image1)
        canvas.itemconfig(image_id, image=img)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def leftPanel(parent, lboxSelectCallback):
    # Function for opening the
    # file explorer window
    def browseFiles():
        dir = filedialog.askdirectory()
        if dir:
            # Change label contents
            label_file_explorer.configure(text="Folder Opened: " + dir)
            doThatExifStuff(dir)

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
    p = Progressbar(parent, orient=HORIZONTAL, length=100, mode="determinate", takefocus=True, maximum=100)
    l = Listbox(parent)

    label_file_explorer.pack(side=TOP)
    button_explore.pack(side=TOP)
    button_exit.pack(side=TOP)
    p.pack(side=TOP)
    l.pack(fill=BOTH, expand=True)

    l.bind("<<ListboxSelect>>", lboxSelectCallback)
    return parent


def rightPanel(parent):
    canvas = Canvas(parent, width=IMG_SIZE[0], height=IMG_SIZE[1])
    image = Image.open(resource_path('default.png'))
    image.thumbnail(IMG_SIZE, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    image_id = canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.pack(expand=True, fill=X)
    var = StringVar()
    exifLabel = Label(parent, textvariable=var, relief=RAISED)
    var.set("test text")
    exifLabel.pack(side=LEFT)
    return parent, canvas, image_id, img, var


root = Tk()
root.title('File Explorer')
root.config(background="white")

window = Frame(root)
window.pack()

leftFrame = leftPanel(Frame(window, relief=RAISED, borderwidth=1, height=1000), listbox_callback)
rightFrame, canvas, image_id, img, exifText = rightPanel(Frame(window, borderwidth=1, height=1000))

# https://www.pythontutorial.net/tkinter/tkinter-listbox/


leftFrame.grid(column=1, row=1, sticky=NS)
rightFrame.grid(column=2, row=1)

window.mainloop()