import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
from pylab import *
import json
import os ,sys, time

#Run FIR
class FIR:
    coeff = []
    xv = []
    hv = []
    brange = 0
    def __init__(self, coeff = list()):
        if len(coeff) > 0:
            self.coeff = coeff
            self.xv = [0]*len(coeff)
            bCNT = len(coeff)
            bRange = int(bCNT/2)
            if bCNT % 2 == 1:
                bRange += 1 
            self.brange = bRange  
            self.crange = bCNT
            print("__init__ range : {}".format(self.brange))         

    def calculte(self, y):
        output = 0
        self.xv[0] = y
        if self.brange > 0:
            for i in range(0,self.crange):
                output += int(self.xv[i]*self.coeff[i])
            for i in range(0,self.crange):
                self.xv[self.crange-i-1] = self.xv[self.crange-i-2]

        print("calculte xv : {}".format(self.xv))
        print("calculte y : {}".format(y))
        print("calculte output : {}".format(output))
        # time.sleep(5)
        return output


#Plot frequency and phase response
def filtre_Test(b, y, n = 0):
    y_filtered = list()
    fir = FIR(b)
    for i in y:
        y_filtered.append(fir.calculte(i))
    # y_filtered = signal.lfilter(b, 1, y)
    # print("y : {}".format(y))
    # print("y\' : {}".format(y_filtered))
    x = range(0, len(y))
    plt.plot(x[n:], y[n:], label = "input")
    plt.plot(x[n:], y_filtered[n:], label = "filtered")
    plt.legend()
    plt.show()

def main():
    dict_data = {}
    dirpath = os.path.dirname(sys.argv[0])
    n = 4
    a = signal.firwin(n, cutoff = 0.5)
    print("coeff : {}".format(a))
    flists = open("{}".format("datain.json"), 'r')
    # print("flist was open : {}".format(flists))
    dat = flists.read()
    # print("dat : {}".format(dat))
    if dat :
        dict_data = json.loads(dat)
    print("dict Data : {}".format(dict_data))
    filtre_Test(b=a, y=dict_data["1"], n = n)
    filtre_Test(b=a, y=dict_data["2"], n = n)
    filtre_Test(b=a, y=dict_data["3"], n = n)
    filtre_Test(b=a, y=dict_data["T"], n = n)
    filtre_Test(b=a, y=dict_data["B"], n = n)
    # impz(a)


if __name__ == '__main__':
    main()
else:
    print("name : {}".format(__name__))
