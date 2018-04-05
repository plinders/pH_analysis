import tifffile as tiff
import numpy as np
import re
import os

class Golgi():
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.ratio = float()
        self.group = classifyGolgi(self.name)
        #self.data_clean = data

    def calcRatio(self, ch1, ch2):
        ratio_arr = [[],[]]
        for i in [ch1, ch2]:
            ratio_arr[i] = self.data[i] - self.data[i].min()
            ratio_arr[i][self.data[i] == 0] = np.nan

        self.ratio = np.nanmean(ratio_arr[ch1]) / np.nanmean(ratio_arr[ch2])

    def saveImage(self):
        img_name = self.name + ".tif"
        # Make folder for each group if it doesn't exist
        if not os.path.exists(self.group):
            os.makedirs(self.group)

        tiff.imsave(self.group + "/" + img_name, self.data.astype('uint16'), 'imagej')

def classifyGolgi(name):
    """Classify Golgis into pH values/markers etc"""

    # pH regex: [pP][hH]\d?.\d
    # Marker regex: (B4GALT1|MGAT2|MAN2A1)_(unt)/gi

    if re.search("(B4GALT1|MGAT2|MANII)_(unt)", name, flags=re.IGNORECASE):
        if re.search("(B4GALT1)", name, flags=re.IGNORECASE):
            return("B4GALT1")
        elif re.search("(MGAT2)", name, flags=re.IGNORECASE):
            return("MGAT2")
        elif re.search("(MAN2A1)", name, flags=re.IGNORECASE):
            return("MAN2A1")
    elif re.search("(TMEM199KO)_(B4GALT1|MGAT2|MANII)", name, flags=re.IGNORECASE):
        if re.search("(B4GALT1)", name, flags=re.IGNORECASE):
            return("TMEM199KO_B4GALT1")
        elif re.search("(MGAT2)", name, flags=re.IGNORECASE):
            return("TMEM199KO_MGAT2")
        elif re.search("(MANII)", name, flags=re.IGNORECASE):
            return("TMEM199KO_MANII")
    elif re.search("[pP][hH]\d.?\d", name):
        if re.search("([hH]3.?5)", name):
            return("pH3.5")
        elif re.search("([hH]4.?0)", name):
            return("pH4.0")
        elif re.search("([hH]4.?5)", name):
            return("pH4.5")
        elif re.search("([hH]5.?0)", name):
            return("pH5.0")
        elif re.search("([hH]5.?5)", name):
            return("pH5.5")
        elif re.search("([hH]6.?0)", name):
            return("pH6.0")
        elif re.search("([hH]6.?5)", name):
            return("pH6.5")
        elif re.search("([hH]7.?0)", name):
            return("pH7.0")
        elif re.search("([hH]7.?5)", name):
            return("pH7.5")
        else:
            return(None)

