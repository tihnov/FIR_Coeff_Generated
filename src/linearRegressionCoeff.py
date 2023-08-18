import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
from pylab import *
import json
import os ,sys, time

thisData = dict()

def estimate_coef(x, y):
    # number of observations/points
    x = np.array(x)
    y = np.array(y)
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
 
    # calculating cross-deviation and deviation about x
    print("n*m_y*m_x : {}".format(n*m_y*m_x))
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)

def linear_Test(x, y, b_0, b_1,b, a):
    y_predict = list()
    y_test = list()
    for i in x:
        y_predict.append((i*b_1)+b_0)
        y_test.append((i*b)+a)
    # y_filtered = signal.lfilter(b, 1, y)
    # print("y : {}".format(y))
    # print("y\' : {}".format(y_filtered))
    plt.scatter(x, y, label = "input")
    plt.plot(x, y_predict, label = "filtered")
    plt.plot(x, y_test, label = "y_test")
    plt.legend()
    plt.show()

def main():
    dict_data = {}
    dirpath = os.path.dirname(sys.argv[0])
    # n = 15
    # a = signal.firwin(n, cutoff = 0.1)
    # print("coeff : {}".format(a))
    # flists = open("{}".format("linear.json"), 'w')
    # for eachcoeeff in a:
    #     flists.writelines("{:.6f},".format(round(eachcoeeff,6)))
    # flists.close()
    flists = open("{}".format("Controller20201028_0343_z.json"), 'r')
    # print("flist was open : {}".format(flists))
    dat = flists.read()
    print("dat : {}".format(dat))
    if dat :
        dict_data = json.loads(dat)
    print("dict Data : {}".format(dict_data))
    for eachVal in dict_data:
        print("each Data : {}".format(eachVal))
        listKeys = list(eachVal.keys())[0]
        listVals = list(eachVal.values())[0]
        print("listKeys : {} - listVals : {}".format(listKeys, listVals))
        thisData.update({"{}".format(listKeys):{"y":list(),"x":list()}})
        # filtre_Test(b=a, y=listVals[0], n = n)
    for eachVal in dict_data:
        print("each Data : {}".format(eachVal))
        listKeys = list(eachVal.keys())[0]
        listVals = list(eachVal.values())[0]
        print("listKeys : {} - listVals : {}".format(listKeys, listVals))
        thisData["{}".format(listKeys)]["y"].append(listVals[1])
        thisData["{}".format(listKeys)]["x"].append(listVals[2])

    print("thisData : {}".format(thisData))

    for keys, values in thisData.items():
        print("keys : {} - values : {}".format(keys, values))
        b0,b1 = estimate_coef(values["y"],values["x"])
        b, a = np.polyfit(values["y"],values["x"], deg=1)
        print("keys : {} - b0 : {} - b1 : {}".format(keys, b0, b1))
        print("keys : {} - a : {} - b : {}".format(keys, a, b))
        linear_Test(values["y"],values["x"],b0,b1,b, a)
    # impz(a)


if __name__ == '__main__':
    main()
else:
    print("name : {}".format(__name__))