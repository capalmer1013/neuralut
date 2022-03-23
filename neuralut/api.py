import glob
import sqlite3
import math

import numpy as np
import matplotlib.pyplot as plt
import cv2
from exif import Image
import pandas as pd
import hashlib

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

        return {x: my_image.get(x, None) for x in my_image.list_all()}

    except:
        return None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ComparisonNode:
    def __init__(self, data=None, parent=None, l=None):
        self.leftChild = None
        self.rightChild = None
        self.parent = parent
        self.data = data
        if l:
            if len(l) == 1:
                self.data = l[0]
            else:
                self.createTreeFromList(l)

    def createTreeFromList(self, l):
        if len(l) > 1:
            self.leftChild = ComparisonNode(parent=self, l=l[len(l)//2:])
            self.rightChild = ComparisonNode(parent=self, l=l[:len(l)//2])
        else:
            if l:
                self.data = l[0]

    def getNextComparison(self):
        try:
            if self.leftChild and not self.leftChild.data:
                return self.leftChild.getNextComparison()
        except Exception as e:
            print(e)
        try:
            if self.rightChild and not self.rightChild.data:
                return self.rightChild.getNextComparison()
        except Exception as e:
            print(e)

        return self

    def chooseWinner(self, leftOrRight):
        # left = 0, right = 1
        if leftOrRight == 0:
            self.data = self.leftChild.data
        elif leftOrRight == 1:
            self.data = self.rightChild.data
        else:
            print("wtf is you doing?")

    def getCurrentSorting(self):
        sortedList = []
        queue = [self]
        while len(queue) > 0:
            if queue[0].data not in sortedList:
                sortedList.append(queue[0].data)
            node = queue.pop(0)
            if node.leftChild is not None:
                queue.append(node.leftChild)

            if node.rightChild is not None:
                queue.append(node.rightChild)

        return sortedList

    def __repr__(self):
        data = ""
        if self.leftChild:
            data += "left: " + str(self.leftChild.data)
        if self.rightChild:
            data += "right: " + str(self.rightChild.data)

        return str(self.data) + data


class DB:
    def __init__(self, filename="exif.db"):
        self.filename = filename
        self.open()

    def open(self):
        self.conn = sqlite3.connect(self.filename)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def createExifTable(self):
        self.cur.execute("""
            create table if not exists exif(
                id integer PRIMARY KEY,
                filename TEXT,
                hash TEXT unique
            );
            """)

        self.conn.commit()

    def getUniqueFiles(self):
        self.cur.execute("select distinct filename from exif order by filename;")
        return self.cur.fetchall()

    def getExifByFilename(self, filename):
        self.cur.execute("select * from exif where filename='{}';".format(filename))
        return self.cur.fetchone()

    def addEntry(self, entry, filename):
        # todo change to upsert logic
        if not entry:
            return 
        entry['hash'] = hashlib.sha256(bytes(str(entry)+filename, 'utf-8')).hexdigest()
        entry['filename'] = filename

        self.cur.execute("select * from exif limit 1;")
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
        try:
            self.cur.execute(insertString)
        except sqlite3.IntegrityError as e:
            print(e)
            # todo: add some way to figure out if this is the unique constraint failure
            # text: UNIQUE constraint failed: exif.hash
            pass
        except ValueError as e:
            # observed as:
            # ValueError: the query contains a null character
            # todo: add a more explicit check for null character, or remove them
            print(e)
            pass
        except Exception as e:
            print(e)
            raise e;

        self.conn.commit()


def makeCube(filename):
    img = cv2.imread(filename)
    nsamples = 33
    cv2.imwrite("beforetest.jpg", img)
    info = np.iinfo(img.dtype)  # Get the information of the incoming image type
    data = img.astype(np.float64) / info.max  # normalize the data to 0 - 1
    data = (nsamples - 1) * data  # Now scale by 255
    img = data.astype(np.uint8)

    CUBE = np.zeros((nsamples, nsamples, nsamples), int)
    for row in img:
        for column in row:
            CUBE[column[2]][column[1]][column[0]] += 1

    return CUBE
    # cv2.imwrite("test.jpg", CUBE)


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
            c.append(
                (r.astype(np.float64) / info.max, g.astype(np.float64) / info.max, b.astype(np.float64) / info.max))

    # fig = plt.figure()
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
                    c.append((r / nsamples, g / nsamples, b / nsamples, math.log(point.astype(np.float64)) / max_value))
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

