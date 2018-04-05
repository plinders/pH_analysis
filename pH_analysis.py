from segmentation import loadImage, makeContours, evaluateGolgi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from Golgi_obj import Golgi

def imgToArray(img_file):
    data, name = loadImage(img_file)
    contours, thresh = makeContours(data)
    golgis = evaluateGolgi(data, contours, thresh, name)
    return(golgis)

def folderToArray(directory):
    golgis = []
    tif_list = glob.glob(directory + "/*.tif")
    for item in tif_list:
        temp = imgToArray(item)
        for golgi in temp:
            golgis.append(golgi)
    return(golgis)

def loadObjs(folder):
    glob_pattern = folder + "/**/*.tif"
    tif_list = glob.glob(glob_pattern, recursive=True)
    objs = []
    for item in tif_list:
        img, name = loadImage(item)
        objs.append(Golgi(name, img))
    return(objs)

def removeOutliers(x):
    a = np.array(x)
    upper_quartile = np.percentile(a, 75)
    lower_quartile = np.percentile(a, 25)
    IQR = (upper_quartile - lower_quartile) * 1.5
    quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
    resultList = []
    for y in a.tolist():
        if y >= quartileSet[0] and y <= quartileSet[1]:
            resultList.append(y)
    return(resultList)

def arrayToDF(arr):
    # First calculate ratio for all items
    for item in arr:
        item.calcRatio(0, 1)

    group_set = set()
    for item in arr:
        group_set.add(item.group)

    d = {}
    for group in group_set:
        temp = []
        for item in arr:
            if group == item.group:
                temp.append(item.ratio)
                #temp = removeOutliers(temp)
                d[group] = temp
    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.T
    df.to_csv('raw_data.csv')
    ph_cols = [col for col in df.columns if 'pH' in col]
    ph_df = df[ph_cols]

    for i, col in enumerate(ph_cols):
        temp = col.split('pH')[1]
        ph_cols[i] = float(temp)

    ph_df.columns = ph_cols
    pH_m = ph_df.melt(var_name="pH", value_name="Ratio")

    rest_cols = [col for col in df.columns if 'pH' not in col]
    rest_df = df[rest_cols]

    pH_m = pH_m.dropna()
    pH_m = pH_m.sort_values(by=['pH']).reset_index(drop=True)

    return(pH_m, rest_df)

def polyGraph(inFile, pH_df, deg):
    x = pH_df['pH'].values
    y = pH_df['Ratio'].values
    print(x)

    popt = np.polyfit(x, y, 3)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = np.polyval(popt, x_new)

    plt.plot(x, y, 'o', label='data')
    plt.plot(x_new, y_new, 'r-', label="fit")
    plt.xlabel("pH")
    plt.ylabel("Ratio 405/470")
    plt.title(f"{inFile}")  
    plt.legend()
    plt.savefig(f"{inFile}.pdf", dpi=300, papertype="a4")
    plt.close()
    return(p)

def solveForY(p, val):
    pc = popt.copy()
    pc[-1] -= y
    return(np.roots(pc))

def calcRest(rest_df, p):
    for col in rest_df.columns:
        out_list = []
        for i in rest_df[col].dropna().values:
            out_list.append(np.absolute(solveForY(p, i)))
        filename = str(col) + ".txt"
        f = open(filename, 'w')
        for item in out_list:
            f.write(f"{item}\n")  

