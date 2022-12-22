import tkinter as tk
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
from tkinter import filedialog

from fractions import Fraction
import api
import utils as U
from sys import exit
import sys
import os.path


IMG_SIZE = (800, 800)
ISO = "photographic_sensitivity"
SHUTTER_SPEED = "exposure_time"
F_STOP = "f_number"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ## Setting up Initial Things
        self.title("Sample Tkinter Structuring")
        # self.geometry("1800x900")
        self.resizable(True, True)
        self.iconphoto(False, tk.PhotoImage(file='default.png'))
    
        ## Creating a container
        container = tk.Frame(self, bg="#8AA7A9")
        container.grid()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        ## Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.Validation = Validation

        ## Defining Frames and Packing it
        for F in {HomePage, Validation}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")    
           
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        menubar = frame.create_menubar(self)
        self.configure(menu=menubar)
        frame.tkraise()                         ## This line will put the frame on front
 



#---------------------------------------- HOME PAGE FRAME / CONTAINER ------------------------------------------------------------------------
class FileList(tk.Frame):
    def __init__(self, parent, container, preview):
        super().__init__(container)
        self.progressBar = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate", takefocus=True, maximum=100)
        self.listbox = Listbox(self, width=50, height=40)
        self.progressBar.grid(row=0, sticky=N)
        self.listbox.grid(row=1, sticky=N, rowspan=3)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)
        self.preview = preview
        exifdb = api.DB()
        exifdb.createExifTable()
        self.populateFileListFromDB(exifdb)
    
    def browseFiles(self):
        dir = filedialog.askdirectory()
        if dir:
            # Change label contents
            self.doThatExifStuff(dir)

    def readFilesFromDir(self, dirname, exifdb):
        validFiles = api.findFiles(dirname + os.path.sep + "**", api.SUPPORTED_FILES)
        count = 0
        for each in validFiles:
            count += 1
            self.progressBar['value'] = count / len(validFiles) * 100
            print(each)
            exifdb.addEntry(api.checkForExif(each), each)
            self.update()

    def doThatExifStuff(self, dirname):
        exifdb = api.DB()
        self.readFilesFromDir(dirname, exifdb)
        self.populateFileListFromDB(exifdb)

        self.listbox.grid(row=1)
        self.update()
    
    def populateFileListFromDB(self, exifdb):
        for each in exifdb.getUniqueFiles():
            self.listbox.insert(1, each['filename'])

    def listbox_callback(self, event):
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
            self.preview.exifText.set("iso: {}, shutter: {}, f-stop: {}".format(exifData[ISO], shutter_fraction, exifData[F_STOP]))
            self.preview.setPreview(data) # todo: rename to filename

class PreviewWindow(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        self.canvas = Canvas(self, width=IMG_SIZE[0], height=IMG_SIZE[1], bg="#777777")
        self.setPreview('default.png')
        self.canvas.grid(row=0)
        self.exifText = StringVar()
        exifLabel = Label(self, textvariable=self.exifText, relief=RAISED, font=("Arial", 25))
        self.exifText.set("test text")
        exifLabel.grid(row=1)
    
    def setPreview(self, img_filename):
        image = Image.open(img_filename)
        image.thumbnail(IMG_SIZE, Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)  # img has to be stored otherwise loses references and deletes self
        self.image_id = self.canvas.create_image(0, 0, anchor=NW, image=self.img)


class HomePage(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Neuralut", font=('Times', '20'))
        label.grid()
        ## ADD CODE HERE TO DESIGN THIS PAGE
        self.preview = PreviewWindow(self, self)
        self.preview.grid(column=1, row=0)
        self.fileList = FileList(self, self, preview=self.preview)
        self.fileList.grid(column=0, row=0)

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Import", command=lambda: self.fileList.browseFiles())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar


#---------------------------------------- Validation PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Validation(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Validation Page", font=('Times', '20'))
        label.pack(pady=0,padx=0)

        ## ADD CODE HERE TO DESIGN THIS PAGE

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)  

        ## proccessing menu
        processing_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=U.about)
        help_menu.add_separator()

        return menubar


if __name__ == "__main__":
    app = App()
    app.mainloop()

    ## IF you find this useful >> Claps on Medium >> Stars on Github >> Subscription on youtube will help me
