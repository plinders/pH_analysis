import sys
from os.path import basename
from pH_analysis import folderToArray, arrayToDF, polyGraph, solveForY, calcRest, loadCSV, loadObjs




# Use these four lines if you want to perform segmentation first
foldername = sys.argv[1]
golgis = folderToArray(foldername)
ph_df, rest_df = arrayToDF(golgis)
p = polyGraph(basename(foldername), ph_df)

# Use these lines if you want perform pH analysis on a csv file with previously prepared data
# csvfile = sys.argv[1]
# ph_df, rest_df = loadCSV(csvfile)
# p = polyGraph(basename(csvfile), ph_df)

# Load single cell images
# foldername = sys.argv[1]
# golgis = loadObjs(foldername)
# ph_df, rest_df = arrayToDF(golgis)
# p = polyGraph(basename(foldername), ph_df)
# calcRest(rest_df, p)
