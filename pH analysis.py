import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as P
import glob
import re

# Wrangle data from seperate txt files to a df
def pHWrangler(filename):
    txt_list = glob.glob("*.txt")

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
        return resultList

    B4GALT1_unt = []
    MGAT2_unt = []
    pH35 = []
    pH40 = []
    pH45 = []
    pH50 = []
    pH55 = []
    pH60 = []
    pH65 = []
    pH70 = []
    pH75 = []

    for txt in txt_list:
        with open(txt, 'r') as f:
            if re.search("^B4GALT1_unt", txt):
                B4GALT1_unt.append(float(f.readline().strip()))
            elif re.search("^MGAT2_unt", txt):
                MGAT2_unt.append(float(f.readline().strip()))
            elif re.search("pH35", txt):
                pH35.append(float(f.readline().strip()))
            elif re.search("pH40", txt):
                pH40.append(float(f.readline().strip()))
            elif re.search("pH45", txt):
                pH45.append(float(f.readline().strip()))
            elif re.search("pH50", txt):
                pH50.append(float(f.readline().strip()))
            elif re.search("pH55", txt):
                pH55.append(float(f.readline().strip()))
            elif re.search("pH60", txt):
                pH60.append(float(f.readline().strip()))
            elif re.search("pH65", txt):
                pH65.append(float(f.readline().strip()))
            elif re.search("pH70", txt):
                pH70.append(float(f.readline().strip()))
            elif re.search("pH75", txt):
                pH75.append(float(f.readline().strip()))
    
    B4GALT1_unt = removeOutliers(B4GALT1_unt)
    MGAT2_unt = removeOutliers(MGAT2_unt)
    try:                
        pH35 = removeOutliers(pH35)
    except IndexError:
        pass
    pH40 = removeOutliers(pH40)
    pH45 = removeOutliers(pH45)
    pH50 = removeOutliers(pH50)
    pH55 = removeOutliers(pH55)
    pH60 = removeOutliers(pH60)
    pH65 = removeOutliers(pH65)
    pH70 = removeOutliers(pH70)
    pH75 = removeOutliers(pH75)

    d = {'B4GALT1_unt': B4GALT1_unt,
        'MGAT2_unt': MGAT2_unt,
        'pH35': pH35,
        'pH40': pH40,
        'pH45': pH45,
        'pH50': pH50,
        'pH55': pH55,
        'pH60': pH60,
        'pH65': pH65,
        'pH70': pH70,
        'pH75': pH75}

    df = pd.DataFrame.from_dict(d, orient="index")
    df.transpose().to_csv(filename+'.csv', index=False)

# Start by importing the pre-formatted csv file
def importFile(inFile):
    # Imports csv file, extracts pH data and makes a long df, returns long df + rest of original df
    df = pd.read_csv(inFile)
    pH_cols = [col for col in df.columns if 'pH' in col]
    pH_df = df[pH_cols]

    for i, col in enumerate(pH_cols):
        temp = col.split('pH')[1]
        temp = float(temp) / 10
        pH_cols[i] = temp

    pH_df.columns = pH_cols

    pH_m = pH_df.melt(var_name="pH", value_name="Ratio")

    rest_cols = [col for col in df.columns if 'pH' not in col]
    rest_df = df[rest_cols]

    return pH_m.dropna(), rest_df

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

def solveForY(val, p):
    return (p - val).roots()[2]

pHWrangler("PL002.16")

df, rest = importFile("PL002.16.csv")
p = polyGraph("PL002.16.csv", df, 5)

for col in rest.columns:
    out_list = []
    for i in rest[col].dropna().values:
        out_list.append(np.absolute(solveForY(i, p)))
    filename = str(col) + ".txt"
    f = open(filename, 'w')
    for item in out_list:
        f.write("%s\n" % item)

    

