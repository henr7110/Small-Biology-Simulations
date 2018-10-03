#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 11:42:52 2017

@author: Henrik
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def dXdt(X,end,n):
    E,S,ES,P = X[0],X[1],X[2],X[3]
    dt = float(end)/float(n)

    dSdt = S + dt*(ES*0.1-(S*(0.01-ES)))
    dESdt = ES + dt*((0.01-ES)*S-0.001*ES-ES*0.1)
    dPdt = 1-dSdt-dESdt
    dEdt = 0.01-dESdt

    return [dEdt,dSdt,dESdt,dPdt]

#run sim
def prob42():
    n=10000
    E_0 = 0.01
    S_0 = 1
    ES_0 = 0
    P_0 = 0
    inval=[E_0,S_0,ES_0,P_0]

    concentration = inval
    s =[inval]
    t = np.linspace(0,5,n)
    for i in range(n-1):
        concentration = dXdt(concentration,5,n)
        s.append(concentration)

    #plot
    solution = np.array(s)
    plt.semilogy(t,solution[:,0],label="E")
    plt.semilogy(t,solution[:,1],label="S")
    plt.semilogy(t,solution[:,2],label="ES")
    plt.semilogy(t,solution[:,3],label="P")
    plt.xlabel("time")
    plt.title("semilogplot of enzymatic digestion from t=0 to t=5")
    plt.ylabel("log(C)")
    plt.legend()
    plt.axis([0,5,-0.001,1.5])
    plt.show()

    solution = np.array(s)
    plt.plot(t,solution[:,0],label="E")
    plt.plot(t,solution[:,1],label="S")
    plt.plot(t,solution[:,2],label="ES")
    plt.plot(t,solution[:,3],label="P")
    plt.title("plot of enzymatic digestion from t=0 to t=5")
    plt.xlabel("time")
    plt.ylabel("C")
    plt.legend()
    plt.axis([0,5,-0.001,0.01])
    plt.show()

def prob43():
    e = 100000
    n=10000000
    E_0 = 0.01
    S_0 = 1
    ES_0 = 0
    P_0 = 0
    inval=[E_0,S_0,ES_0,P_0]

    concentration = inval
    s =[inval]
    t = np.linspace(0,e,n)
    for i in range(n-1):
        concentration = dXdt(concentration,e,n)
        s.append(concentration)

    #plot
    solution = np.array(s)
    plt.semilogy(t,solution[:,0],label="E")
    plt.semilogy(t,solution[:,1],label="S")
    plt.semilogy(t,solution[:,2],label="ES")
    plt.semilogy(t,solution[:,3],label="P")
    plt.xlabel("time")
    plt.title("semilogplot of enzymatic digestion from t=0 to t=100000")
    plt.ylabel("log(C)")
    plt.axis([0,e,10**-4,1])
    plt.legend()
    plt.show()

    solution = np.array(s)
    plt.plot(t,solution[:,0],label="E")
    plt.plot(t,solution[:,1],label="S")
    plt.plot(t,solution[:,2],label="ES")
    plt.plot(t,solution[:,3],label="P")
    plt.title("plot of enzymatic digestion from t=0 to t=100000")
    plt.xlabel("time")
    plt.ylabel("C")
    plt.axis([0,e,0,1])
    plt.legend()
    plt.show()
    print (solution[-1,2])
def Menten():
    e = 100000
    n=1000000
    E_0 = 0.01
    S_0 = 1
    ES_0 = 0
    P_0 = 0
    inval=[E_0,S_0,ES_0,P_0]

    concentration = inval
    s =[inval]
    t = np.linspace(0,e,n)
    for i in range(n-1):
        concentration = dXdt(concentration,e,n)
        s.append(concentration)
    solution = np.array(s)
    v = []
    for i in range(n-2):
        v.append((solution[i+1,3]-solution[i,3])/2)
    print (v[20000])
    plt.plot(v)
    plt.show()
def b43():
    V = np.array([0.15,0.34,0.35,0.42,0.48,0.60,0.52,0.63,0.63,0.63,0.60,0.66,0.69,0.63,0.73,0.69,0.74,0.77,0.72,0.75])
    S = np.array([0.10,0.15,0.19,0.24,0.29,0.34,0.38,0.43,0.48,0.53,0.57,0.62,0.67,0.72,0.76,0.81,0.86,0.91,0.95,1.00])
    invV = 1/V
    invS = 1/S
    slope, intercept = stats.linregress(S,V)[0:2]
    k_m =( 1/intercept)*slope
    V_max = 1/intercept
    v = lambda s: slope*s+intercept
    t = np.linspace(0,20,20)
    plt.plot(1/S,1/V,"ro",label="data")
    plt.plot(v(t),t,label="regression")
    plt.legend()
    plt.show()
