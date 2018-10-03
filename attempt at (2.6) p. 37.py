"""Fun with oscillations"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
from scipy.optimize import broyden1

def dXdt(I,S,R):
    """Calculate derivatives dX/dt, [t] ~ 3-4 days"""
    dSdt = 2+(0.01*R)-(0.0005*S*I)
    dIdt = (0.001*S*I)-(0.1*I)-(0.02*I)
    dRdt = (0.1*I)-(0.01*R)
    return ([dSdt, dIdt, dRdt])

def Euler(steps,h):
    I_0, S_0, R_0 = 10, 990, 0
    t = np.zeros(steps+1)

    S = np.zeros(steps+1)
    S[0] = S_0
    dSdt = np.zeros(steps+1)

    I = np.zeros(steps+1)
    I[0] = I_0
    dIdt = np.zeros(steps+1)

    R = np.zeros(steps+1)
    dRdt = np.zeros(steps+1)

    for i in range(steps):
        #update time
        t[i+1] = t[i]+h
        #calculate derivative
        result = dXdt(I[i],S[i],R[i])
        dSdt[i+1],dIdt[i+1],dRdt[i+1] = result[0],result[1],result[2]
        #update pools
        S[i + 1] = S[i] + h*(dSdt[i+1])
        I[i + 1] = I[i] + h*(dIdt[i+1])
        R[i + 1] = R[i] + h*(dRdt[i+1])
    return t,S,I,R
t,S,I,R = Euler(3000,0.1)
#plot results
plt.plot(t,S,'b',label='S')
plt.plot(t,I,'r',label='I')
plt.plot(t,R,'g',label='R')
plt.legend(loc='best')
plt.xlabel('t')
plt.show()

##"""Plot solution"""
#print('Max. G:    ', G.max(), '\nMax. RNA:  ', RNA.max(), '\nMax. S:    ', S.max())
#
#sns.set_style('ticks')
#plt.ylim(0, 1.02)
## plt.gca().set_yscale('log')
#
#t = np.linspace(-1, n_generations, steps_per_generation*(n_generations+1) + 1)
#plt.plot(t, G/G.max(), color=sns.color_palette()[0], label='G')
#plt.plot(t, RNA/RNA.max(), color=sns.color_palette()[2], label='RNA')
#
#S = S.reshape((n_generations+1, -1)).T
#t = np.concatenate((t[:-1].reshape((n_generations+1, -1)).T,
#    [np.arange(n_generations+1)]))
#plt.plot(t, S/S.max(), color=sns.color_palette()[1], label='S')
#
#sns.despine()
#handles, labels = plt.gca().get_legend_handles_labels()
#plt.legend(handles[:2] + [handles[-1]], labels[:2] + [labels[-1]])
#plt.tight_layout()
#plt.savefig('oscillator.png')
#plt.show()
