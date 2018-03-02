import tifffile as tiff
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import convex_hull_image
from skimage import measure
import re
from os.path import basename
from Golgi_obj import Golgi


#img_file = "test_img/MGAT2_test1.tif"

def loadImage(img_file):
    """Loads open tiff connection to n-dimensional numpy arrays
    """
    with tiff.TiffFile(img_file) as tif:
        images = tif.asarray().astype(float)
    name = basename(img_file).split('.tif')[0]
    return(images, name)

def makeContours(img_arr):
    img = img_arr[0]
    img_gauss = gaussian(img, sigma = 10)
    thresh = threshold_otsu(img_gauss)
    binary = img_gauss > thresh
    contours = measure.find_contours(binary, 0.3)
    return(contours, thresh)

def getMinMax(contour):
    ymin = int(round(contour[:, 0].min()))
    ymax = int(round(contour[:, 0].max()))
    xmin = int(round(contour[:, 1].min()))
    xmax = int(round(contour[:, 1].max()))
    return(ymin, ymax, xmin, xmax)

def extractGolgi(orig_img, contour, thresh):
    ymin, ymax, xmin, xmax = getMinMax(contour)
    width = xmax - xmin
    height = ymax - ymin
    slices = orig_img.shape[0]
    arr = np.zeros((slices, height, width))
    for i in range(slices):
        arr[i] = orig_img[i][ymin:ymax, xmin:xmax]
        # clear = arr[i] < thresh
        # arr[i][clear] = np.nan
    return(arr)

def evaluateGolgi(data, contours, thresh, name):
    golgi_arr = []
    for i in range(len(contours)):
        golgi = extractGolgi(data, contours[i], (thresh * 0.75))
        print(golgi)
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(ncols = 3, nrows = 2, figsize = (15, 8))
        ax1.imshow(golgi[0], cmap = "Greys_r")
        ax1.axis('off')
        ax2.imshow(golgi[1], cmap = "Greys_r")
        ax2.axis('off')
        ax3.imshow((golgi[2]), cmap = "Greys", vmin=100, vmax=2000)
        ax3.axis('off')        
        ax4.imshow(data[0], cmap = "Greys_r")
        ax4.plot(contours[i][:, 1], contours[i][:, 0])
        ax4.axis('off')
        ax5.imshow(data[1], cmap = "Greys_r")
        ax5.plot(contours[i][:, 1], contours[i][:, 0])
        ax5.axis('off')
        ax6.imshow((data[2]), cmap = "Greys", vmin=100, vmax=2000)
        ax6.plot(contours[i][:, 1], contours[i][:, 0])
        ax6.axis('off')
        plt.tight_layout()
        plt.suptitle(name, fontsize=12)
        plt.subplots_adjust(top=0.95)
        plt.ion()
        plt.show()
        plt.pause(0.0001)
        #save = input("Good Golgi? Y/N ")
        save = "y"
        saved = False
        while saved is False:
            if re.match("^[yY]", save):
                golgi_name = name + "_cell_" + str((len(golgi_arr) + 1))
                golgi_arr.append(Golgi(golgi_name, golgi))
                saved = True
            elif re.match("^[nN]", save):
                pass
                saved = True
            else:
                save = input("Invalid input. Good Golgi? Y/N ")       
        plt.close()
    return(golgi_arr)

# df, name = loadImage(img_file)
# contours, thresh = makeContours(df)
# golgis = evaluateGolgi(df, contours, thresh, name)

# print(len(golgis))
# for i in golgis:
#     print(i.name)
#     i.saveImage()
#     #i.calcRatio(0, 1)
#     #print(i.ratio)
    
