
import numpy as np
import tifffile as tiff
import glob


def fluoratio(img):
    """Fluoratio is a simple function that calculates the channel means of a 2 channel tiff image and calculates the ratio between them."""
    # Read in multidimensional numpy array from image
    tiffarrays = tiff.imread(img)
    # split md array into 2 seperate ones
    ch1 = tiffarrays[0]
    ch2 = tiffarrays[1]
    # remove background
    ch1_nobk = ch1 - ch1.min()
    ch2_nobk = ch2 - ch2.min()

    # change type of array to float to be able to remove 0s by index
    ch1_clean = ch1_nobk.astype('float')
    ch2_clean = ch2_nobk.astype('float')
    # replace 0 by NaN
    ch1_clean[ch1_clean == 0] = np.NaN
    ch2_clean[ch2_clean == 0] = np.NaN
    # make sure to run the np.nanmean function to omit NaNs
    ch_ratio = np.nanmean(ch1_clean) / np.nanmean(ch2_clean)

    return ch_ratio


def folderratio(folder):
    """Folderratio applies the previously defined fluoratio function on a whole folder of .tif files"""
    # set pattern for pattern matching to find all tiff files
    tif_pattern = folder + "/*.tif"
    # list tiff files in folder
    filelist = glob.glob(tif_pattern)
    # generate np array of length number of files, quicker than appending
    ratio_array = np.zeros(len(filelist), dtype=np.float64)
    # if a directory is passed as an argument, return output from fluoratio
    # into relevant index of array, else error
    try:
        for tiffile in filelist:
            ratio_array[filelist.index(tiffile)] = fluoratio(tiffile)
    except:
        print('Please pass directory')
    return np.mean(ratio_array)


def autoratio():
    """Sample function to process folder with multiple folders to be analysed"""
    # list all directories
    folderlist = glob.glob("*/")
    # run folderratio on each directory, write to .txt file with same name as folder
    # the fmt argument in np.savetxt gets rid of scientific notation
    for folder in folderlist:
        output = folderratio(folder)
        outputfilename = folder.strip("\\") + ".txt"
        np.savetxt(fname=outputfilename, X=np.array([output]), fmt='%.14f')

autoratio()


