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

    # elif re.search("(TMEM199KO)_(B4GALT1|MGAT2|MANII)", name, flags=re.IGNORECASE):

    if regexSearch("[p][h]\d.?\d", name):
        if regexSearch("([h]3.?5)", name):
            return("pH3.5")
        elif regexSearch("([h]4.?0)", name):
            return("pH4.0")
        elif regexSearch("([h]4.?5)", name):
            return("pH4.5")
        elif regexSearch("([h]5.?0)", name):
            return("pH5.0")
        elif regexSearch("([h]5.?5)", name):
            return("pH5.5")
        elif regexSearch("([h]6.?0)", name):
            return("pH6.0")
        elif regexSearch("([h]6.?5)", name):
            return("pH6.5")
        elif regexSearch("([h]7.?0)", name):
            return("pH7.0")
        elif regexSearch("([h]7.?5)", name):
            return("pH7.5")
    elif regexSearch("(TMEM199KO)", name):
        if regexSearch("(B4GALT1)", name):
            return("TMEM199KO_B4GALT1")
        elif regexSearch("(MGAT2)", name):
            return("TMEM199KO_MGAT2")
        elif regexSearch("(MANII)", name):
            return("TMEM199KO_MANII")
        elif regexSearch("(TNF)", name):
            return("TMEM199KO_TNFa")
    elif regexSearch("(Parental)", name):
        if regexSearch("(B4GALT1)", name):
            return("Parental_B4GALT1")
        elif regexSearch("(MGAT2)", name):
            return("Parental_MGAT2")
        elif regexSearch("(MANII)", name):
            return("Parental_MANII")
        elif regexSearch("(TNF)", name):
            return("Parental_TNFa")
    else:
        return(name.split("_cell")[0])

def regexSearch(query, name):
    return re.search(query, name, flags=re.IGNORECASE)