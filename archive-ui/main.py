from bdb import checkfuncname
from email.mime import image
import glob
import sqlite3
import time
import math
import random
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import cv2
from exif import Image
import pandas as pd


SUPPORTED_FILES = ["jpg", "jpeg"]

def findFiles(dir, filetypes, recursive=True):
    return [x for x in glob.glob(dir, recursive=recursive) if x.split('.')[-1].lower() in filetypes]


def isSupported(filename):
    return filename.split('.')[-1].lower() in SUPPORTED_FILES

def checkForExif(filename):
    try:
        with open(filename, 'rb') as image_file:
            my_image = Image(image_file)
        
        if not my_image.has_exif:
            return False
        
        return {x:my_image.get(x, None) for x in my_image.list_all()}

    except:
        return None


class DB:
    def __init__(self, filename="exif.db"):
        self.filename = filename
        self.open()
    
    def open(self):
        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()
        
    
    def createExifTable(self):
        self.cur.execute("""
            create table if not exists exif(
                id integer PRIMARY KEY,
                filename TEXT,
                hash TEXT);""")
        
        self.conn.commit()
    
    def addEntry(self, entry, filename):
        if not entry:
            return
        
        entry['filename'] = filename

        self.cur.execute("select * from exif;")
        columnNames = [x[0] for x in self.cur.description]
        for each in entry:
            if each not in columnNames:
                self.cur.execute("ALTER TABLE exif ADD COLUMN {} TEXT".format(each))

        
        fieldnames = [x for x in entry]
        values = [str(entry[x]) for x in fieldnames]
        insertString = "INSERT INTO exif ("
        for each in fieldnames:
            insertString += each + ", "
        insertString = insertString[:-2]
        insertString += ") VALUES ("
        for each in values:
            insertString += '"' + each + '", '
        
        insertString = insertString[:-2] + ");"

        self.cur.execute(insertString)
        self.conn.commit()

        

def makeCube(filename):
    img = cv2.imread(filename)
    nsamples = 33
    cv2.imwrite("beforetest.jpg", img)
    info = np.iinfo(img.dtype) # Get the information of the incoming image type
    data = img.astype(np.float64) / info.max # normalize the data to 0 - 1
    data = (nsamples-1) * data # Now scale by 255
    img = data.astype(np.uint8)

    CUBE = np.zeros((nsamples, nsamples, nsamples), int)
    for row in img:
        for column in row:
            CUBE[column[2]][column[1]][column[0]] += 1
    
    return CUBE
    #cv2.imwrite("test.jpg", CUBE)


def displayImageAsCube(filename):
    img = cv2.imread(filename)
    x, y, z, c = [], [], [], []
    info = np.iinfo(img.dtype)
    for row in img:
        for column in row:
            r, g, b = column[0], column[1], column[2]
            x.append(r)
            y.append(g)
            z.append(b)
            c.append((r.astype(np.float64)/info.max, g.astype(np.float64)/info.max, b.astype(np.float64)/info.max))

    #fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.scatter3D(x, y, z, c=c, cmap='Greens');
    plt.show()


def displayCube(cube):
    x, y, z, c = [], [], [], []
    max_value = math.log(np.amax(cube))
    nsamples = 33
    r = 0
    for row in cube:
        g = 0
        for column in row:
            b = 0
            for point in column:
                if point:
                    x.append(r)
                    y.append(g)
                    z.append(b)
                    c.append((r/nsamples, g/nsamples, b/nsamples, math.log(point.astype(np.float64))/max_value))
                b += 1
            g += 1
        r += 1
    print("returning display cube ")
    return mpl_3d_graph(x, y, z, c)

def mpl_3d_graph(x, y, z, c):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlabel('r')
    ax.set_ylabel('g')
    ax.set_zlabel('b');
    ax.scatter3D(x, y, z, c=c, cmap="Greens")
    plt.savefig("3dblob.jpg")
    return fig

def plotly_3d_graph(x, y, z, c):
    return pd.DataFrame(dict(R=x, G=y, B=z, C=c))
    

testDir = '/mnt/c/Users/Chris Palmer/Desktop/street photos/**'
if __name__ == "__main__":
    # testDir = '/mnt/e/**'
    #print(findFiles(testDir, SUPPORTED_FILES))
    a = DB()
    a.createExifTable()

    counter = 0
    validFiles = findFiles(testDir, SUPPORTED_FILES)
    lastMeasure = 0.0
    for f in validFiles:
        f = random.choice(validFiles)
        counter += 1
        currentMeasure = (counter/len(validFiles)) * 100.0
        if currentMeasure - lastMeasure > 5.0:
            lastMeasure = currentMeasure
            print(currentMeasure, "%")
        #displayImageAsCube(f)
        displayCube(makeCube(f)).show()
        break
        #a.addEntry(checkForExif(f), f)


    a.close()

