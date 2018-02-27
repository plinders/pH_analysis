import tifffile as tiff
import numpy as np
import re

class Golgi():
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.ratio = float()
        self.group = classifyGolgi(self.name)

    def calcRatio(self, ch1, ch2):
        self.ratio = np.nanmean(self.data[ch1] / self.data[ch2])

    def saveImage(self):
        img_name = self.name + ".tif"
        tiff.imsave(img_name, self.data.astype('uint16'), 'imagej')

def classifyGolgi(name):
    """Classify Golgis into pH values/markers etc"""
    if re.search("^B4GALT1_unt", name):
        return("B4GALT1_unt")
    elif re.search("^MGAT2_unt", name):
        return("MGAT2_unt")
    elif re.search("pH35", name):
        return("pH35")
    elif re.search("pH40", name):
        return("pH40")
    elif re.search("pH45", name):
        return("pH45")
    elif re.search("pH50", name):
        return("pH50")
    elif re.search("pH55", name):
        return("pH55")
    elif re.search("pH60", name):
        return("pH60")
    elif re.search("pH65", name):
        return("pH65")
    elif re.search("pH70", name):
        return("pH70")
    elif re.search("pH75", name):
        return("pH75")
    else:
        return(None)