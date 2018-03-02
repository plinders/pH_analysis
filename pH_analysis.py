from segmentation import loadImage, makeContours, evaluateGolgi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P
import glob

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
    
    # Then make dataframe from array, using group, name and ratio
    df = pd.DataFrame([a.toDataFrame() for a in arr])
    ph_df = df[df['Group'].str.contains('pH')]
    rest_df = df[~df['Group'].str.contains('pH')]
    ph_df['pH'] = ph_df['Group'].str.split('pH').str[1].astype(float)
    ph_df.drop('Group', axis=1, inplace=True)

    # Save df to a csv
    # df.to_csv()
    return(ph_df, rest_df)

def polyGraph(inFile, pH_df, deg):
    x = pH_df['pH'].values
    y = pH_df['Ratio'].values

    p = P.fit(x, y, deg)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = p(x_new)


    # DF = y.size - p.size

    # print(f"p-size: {p.size}\n")
    # print(f"observations: {y.size}\n")


    #y_err = y - y_new

    plt.plot(x, y, 'o', x_new, y_new)
    plt.xlabel("pH")
    plt.ylabel("Ratio 405/470")
    plt.title(f"{inFile}")  
    plt.savefig(f"{inFile}.pdf", dpi=300, papertype="a4")
    return p

# golgis = folderToArray("C:\\Users\\Peter\\Documents\\!Experiments\\test_phLIF_Tiff")
# for item in golgis:
#     print(item.name, item.group)
