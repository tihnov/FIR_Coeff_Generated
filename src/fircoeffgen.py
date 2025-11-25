import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
from pylab import *
import json
import os ,sys, time

#Run FIR

dict_Pairing = {"adc0":"fir0","adc1":"fir1","adc2":"fir2","adc3":"fir3"}

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

        # print("calculte xv : {}".format(self.xv))
        # print("calculte y : {}".format(y))
        # print("calculte output : {}".format(output))
        # time.sleep(5)
        return output


#Plot frequency and phase response
def filter_Test(b, y, n = 0):
    y_filtered = list()
    ywGain = list()
    fir = FIR(b)
    for i in y:
        temp = fir.calculte(i)
        y_filtered.append(temp)
    # y_filtered = signal.lfilter(b, 1, y)
    # print("y : {}".format(y))
    # print("y\' : {}".format(y_filtered))

    b0,b1 = estimate_coef(y_filtered[7:], y[7:])
    print("offset : {} - gain : {}".format(b0,b1))

    for i in y_filtered:
        ywGain.append(i*b1+b0)
    # ywGain = y_filtered*b1 + b0

    x = range(0, len(y))
    plt.plot(x[n:], y[n:], label = "input")
    plt.plot(x[n:], y_filtered[n:], label = "filtered")
    plt.plot(x[n:], ywGain[n:], label = "filteredwGain")
    plt.legend()
    plt.show()

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

def main():
    dict_data = {}
    dict_value = {}
    dirpath = os.path.dirname(sys.argv[0])
    n = 5
    a = signal.firwin(n, cutoff = 0.05, pass_zero=True, window="hamming")
    print("coeff : {}".format(a))
    flists = open("{}".format("coeff.json"), 'w')
    for eachcoeeff in a:
        flists.writelines("{:.6f},".format(round(eachcoeeff,6)))
    flists.close()
    flists = open("{}".format("Controller20201028_0343_u.json"), 'r')
    # print("flist was open : {}".format(flists))
    dat = flists.read()
    flists.close()
    # print("dat : {}".format(dat))
    if dat :
        dict_data = json.loads(dat)
    # print("dict Data : {}".format(dict_data))
    for eachVal in dict_data:
        print("each Data : {}".format(eachVal))
        for key, val in eachVal.items():
            if key in dict_value.keys():
                dict_value[key].extend(val)
            else:
                dict_value.update({key:list(val)})
        # print("dict_value : {}".format(dict_value))
        # listKeys = list(eachVal.keys())
        # listVals = list(eachVal.values())
        # filter_Test(b=a, y=listVals[0], n = n)
    # impz(a)
    print("dict_value : {}".format(dict_value))
    # json_object = json.dumps(dict_value, indent = 4) 
    # print("json_object : {}".format(json_object))
    # flists = open("{}".format("Controller20201028_0343_s1.json"), 'w')
    # flists.write(json_object)
    # flists.close()

    for keypair, valpair in dict_Pairing.items():
        print("key : {} - val : {}".format(keypair, valpair))
        listval = list(dict_value[valpair])
        filter_Test(b=a, y=listval, n = n)



if __name__ == '__main__':
    main()
else:
    print("name : {}".format(__name__))
