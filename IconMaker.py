"""
IconMaker:
    Turns an image into the correct windows Icon sizes and provides a helper
    for loading them

Usage:
    IconMaker.py <filename>

"""

# global imports
from docopt import docopt
from PIL import Image
import os

#QtGui
from PyQt4 import QtGui, QtCore


def CreateIcons(filename):
    if not os.path.isdir("icons"):
        os.makedirs("icons")

    im = Image.open(filename)
    for size in [
            (16,16),
            (24,24),
            (32, 32),
            (48, 48),
            (128, 128),
            (256, 256)
        ]:
        out = im.resize(size, Image.BICUBIC)
        impath = os.path.join(
            "icons","%dx%d.png"% (size[0], size[1]))
        out.save(impath)
        print "icon %s generated" % impath

def SetAppIcon(app):
    app_icon = QtGui.QIcon()
    icon_path = "icons"
    app_icon.addFile(os.path.join(icon_path,
                                  '16x16.png'), QtCore.QSize(16,16))
    app_icon.addFile(os.path.join(icon_path,
                                  '24x24.png'), QtCore.QSize(24,24))
    app_icon.addFile(os.path.join(icon_path,
                                  '32x32.png'), QtCore.QSize(32,32))
    app_icon.addFile(os.path.join(icon_path,
                                  '48x48.png'), QtCore.QSize(48,48))
    app_icon.addFile(os.path.join(icon_path,
                                  '128x128.png'), QtCore.QSize(128,128))
    app_icon.addFile(os.path.join(icon_path,
                                  '256x256.png'), QtCore.QSize(256,256))
    app.setWindowIcon(app_icon)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print arguments

    CreateIcons(arguments["<filename>"])

# # set app icon
# app_icon = QtGui.QIcon()
# app_icon.addFile('gui/icons/16x16.png', QtCore.QSize(16,16))
# app_icon.addFile('gui/icons/24x24.png', QtCore.QSize(24,24))
# app_icon.addFile('gui/icons/32x32.png', QtCore.QSize(32,32))
# app_icon.addFile('gui/icons/48x48.png', QtCore.QSize(48,48))
# app_icon.addFile('gui/icons/256x256.png', QtCore.QSize(256,256))
# app.setWindowIcon(app_icon)
