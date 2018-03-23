import sys
from pH_analysis import folderToArray, arrayToDF, polyGraph, solveForY

foldername = sys.argv[1]

golgis = folderToArray(foldername)
ph_df, rest_df = arrayToDF(golgis)
