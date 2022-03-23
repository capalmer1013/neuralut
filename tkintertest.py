from sys import exit
import os.path
import random
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import filedialog
from fractions import Fraction

from neuralut import api

IMG_SIZE = (800, 800)
ISO = "photographic_sensitivity"
SHUTTER_SPEED = "exposure_time"
F_STOP = "f_number"


def listbox_callback(event):
    global img
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print("filename:", data)
        exifdb = api.DB()
        exifData = exifdb.getExifByFilename(data)
        shutter_fraction = exifData[SHUTTER_SPEED]
        try:
            shutter_fraction = str(Fraction(exifData[SHUTTER_SPEED]).limit_denominator())
        except Exception as e:
            print(e)
            pass
        exifText.set("iso: {}, shutter: {}, f-stop: {}".format(exifData[ISO], shutter_fraction, exifData[F_STOP]))
        image1 = Image.open(data)
        print(image1)
        image1.thumbnail(IMG_SIZE, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image1)
        canvas.itemconfig(image_id, image=img)

def refreshCompareImages(choiceRight):
    global left
    global right

    exifdb = api.DB()
    if choiceRight:
        pass
    else:
        pass
    try:
        # todo: this should be functionalized
        images = random.sample(exifdb.getUniqueFiles(), 2)
        print(images)
        # refresh left
        l = Image.open(images[0]['filename'])
        l.thumbnail(IMG_SIZE, Image.ANTIALIAS)
        left['img'] = ImageTk.PhotoImage(l)
        left['canvas'].itemconfig(left['image_id'], image=left['img'])
        # refresh right
        r = Image.open(images[1]['filename'])
        r.thumbnail(IMG_SIZE, Image.ANTIALIAS)
        right['img'] = ImageTk.PhotoImage(r)
        right['canvas'].itemconfig(right['image_id'], image=right['img'])

    except Exception as e:
        print(e)



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
        count = 0
        for each in validFiles:
            count += 1
            p['value'] = count / len(validFiles) * 100
            print(each)
            exifdb.addEntry(api.checkForExif(each), each)

            window.update()

        for each in exifdb.getUniqueFiles():
            l.insert(1, each['filename'])
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
    #button_exit.pack(side=TOP)
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
    exifLabel = Label(parent, textvariable=var, relief=RAISED, font=("Arial", 25))
    var.set("test text")
    exifLabel.pack(side=LEFT)
    return parent, canvas, image_id, img, var


def menuBar(parent):
    menubar = Menu(parent)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Main Page", command=lambda: raiseWindow(mainWindow))
    filemenu.add_command(label="Compare", command=lambda: raiseWindow(compareWindow))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit)
    menubar.add_cascade(label="File", menu=filemenu)
    return menubar


def raiseWindow(w):
    global window
    w.pack()
    window.pack_forget()
    window = w


def createImage(parent):
    canvas = Canvas(parent, width=IMG_SIZE[0], height=IMG_SIZE[1])
    image = Image.open(resource_path('default.png'))
    image.thumbnail(IMG_SIZE, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    image_id = canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.pack(expand=True, fill=X)
    return {"img": img, "canvas": canvas, "image_id": image_id, "parent": parent}


def CompareWindow(parent):
    left = createImage(Frame(parent, borderwidth=1, height=1000))
    right = createImage(Frame(parent,  borderwidth=1, height=1000))
    left['parent'].grid(column=1, row=1, sticky=NS)
    right['parent'].grid(column=2, row=1)
    return parent, left, right


def key_press(e):
    if window == compareWindow:
        if e.keycode == 39:  # right
            refreshCompareImages(True)
        elif e.keycode == 37:  # left
            refreshCompareImages(False)



root = Tk()
root.bind('<KeyPress>', key_press)
root.title('File Explorer')
root.config(background="white")

mainWindow = Frame(root)
compareWindow, left, right = CompareWindow(Frame(root))
mainWindow.pack()
menu = menuBar(mainWindow)
leftFrame = leftPanel(Frame(mainWindow, relief=RAISED, borderwidth=1, height=1000), listbox_callback)
rightFrame, canvas, image_id, img, exifText = rightPanel(Frame(mainWindow, borderwidth=1, height=1000))

# https://www.pythontutorial.net/tkinter/tkinter-listbox/


leftFrame.grid(column=1, row=1, sticky=NS)
rightFrame.grid(column=2, row=1)
root.config(menu=menu)
window = mainWindow
window.mainloop()