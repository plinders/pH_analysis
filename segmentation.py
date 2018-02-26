import tifffile as tiff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.filters import threshold_otsu, gaussian
from skimage.morphology import convex_hull_image
from skimage import measure

img_file = "test_img/MGAT2_test1.tif"

def loadImage(img_file):
    """Loads open tiff connection to n-dimensional numpy arrays
    """
    with tiff.TiffFile(img_file) as tif:
        images = tif.asarray().astype(float)
    return(images)

def makeContours(img_arr):
    img = img_arr[0]
    img_gauss = gaussian(img, sigma = 15)
    thresh = threshold_otsu(img_gauss)
    binary = img_gauss > thresh
    contours = measure.find_contours(binary, 0.3)
    return(contours)

def getMinMax(contour):
    ymin = int(round(contour[:, 0].min()))
    ymax = int(round(contour[:, 0].max()))
    xmin = int(round(contour[:, 1].min()))
    xmax = int(round(contour[:, 1].max()))
    return(ymin, ymax, xmin, xmax)

def extractGolgi(orig_img, contour):
    ymin, ymax, xmin, xmax = getMinMax(contour)
    width = xmax - xmin
    height = ymax - ymin
    slices = orig_img.shape[0]
    arr = np.zeros((slices, height, width))
    for i in range(slices):
        arr[i] = orig_img[i][ymin:ymax, xmin:xmax]
    return(arr)


df = loadImage(img_file)
contours = makeContours(df)

golgi_arr = []
if __name__ == '__main__':
    for i in range(len(contours)):
        golgi = extractGolgi(df, contours[i])
        fig, (ax1, ax2, ax3) = plt.subplots(ncols = 3, figsize = (15, 5))
        ax1.imshow(golgi[0], cmap = "Greys_r")
        ax1.axis('off')
        ax2.imshow(golgi[1], cmap = "Greys_r")
        ax2.axis('off')
        ax3.imshow(golgi[2], cmap = "Greys")
        ax3.axis('off')
        plt.ion()
        plt.show()
        plt.pause(0.0001)
        save = input("Good Golgi? Y/N ")
        #plt.draw()
        if save == "y":
            golgi_arr.append(golgi)
        else:
            pass
        plt.close()

print(len(golgi_arr))
    
