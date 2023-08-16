import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
from pylab import *
import json
import os ,sys, time

def main():
    dict_data = {}
    flists = open("{}".format("Controller20201028_0343_u.json"), 'r')
    # print("flist was open : {}".format(flists))
    dat = flists.read()
    # print("dat : {}".format(dat))
    if dat :
        dict_data = json.loads(dat)
    print("dict Data : {}".format(dict_data))

    for eachVal in dict_data:
        print("each Data : {}".format(eachVal))
        listKeys = list(eachVal.keys())
        listVals = list(eachVal.values())
        print("each Data listKeys : {}".format(listKeys))
        print("each Data listVals : {}".format(listVals))
        x = range(0, len(listVals[0]))
        plt.plot(x, listVals[0], label = "{}".format(listKeys[0]))
        plt.plot(x, listVals[1], label = "{}".format(listKeys[1]))
        plt.legend()
        plt.show()
if __name__ == '__main__':
    main()
else:
    print("name : {}".format(__name__))