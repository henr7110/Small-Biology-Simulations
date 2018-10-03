"""Fun with oscillations"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
from scipy.optimize import broyden1
from matplotlib.animation import FuncAnimation
from copy import deepcopy
import matplotlib.animation as animation


def laplacian(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    hb = x[1:-1] - x[:-2]
    hf = x[2:] - x[1:-1]
    y_hb = y[:-2]
    y_hf = y[2:]
    hb_hf = hb / hf
    hf_hb = hf / hb
    return (y_hf*(1+hb_hf) - y[1:-1]*(2+hb_hf+hf_hb) +
            y_hb*(1+hf_hb)) / 2 / hb / hf

def dXdt(Bmp,Sox9,Wnt,x):
    """Calculate derivatives dX/dt in center of sample simulation without edges"""
    k_2 = 1
    k_3 = 1
    k_4 = 1.59
    k_5 = 0.1
    k_7 = 1.27
    k_9 = 0.1
    gamma = 1
    d = 2.5

    # Calculate derivatives

    dBmpdt = k_2 * Bmp[1:len(Bmp)-1] - k_3 * Wnt[1:len(Wnt)-1] - Sox9[1:len(Bmp)-1]**3

    dSox9dt = -k_4 * Sox9[1:len(Sox9)-1] - k_5 * Bmp[1:len(Bmp)-1] + gamma * d * laplacian(x,Bmp)

    dWntdt = -k_7 * Sox9[1:len(Sox9)-1] - k_9 * Wnt[1:len(Wnt)-1] + gamma * laplacian(x,Wnt)

    return dBmpdt, dSox9dt, dWntdt


def Euler(steps, h, inits, size):
    Concentrations = deepcopy([[inits[0], inits[1], inits[2]]])
    Bmpnew, Sox9new, Wntnew = inits[0], inits[1], inits[2]

    x = np.linspace(0,size+1,size+2)

    for i in range(steps):
        Bmpbefore = Bmpnew
        Sox9before = Sox9new
        Wntbefore = Wntnew
        #calculate derivative
        dBmpdt, dSox9dt, dWntdt = dXdt(Sox9before,Bmpbefore,Wntbefore,x)

        #update pools
        Bmpnew = np.zeros(len(Bmpbefore))
        Wntnew = np.zeros(len(Bmpbefore))
        Sox9new = np.zeros(len(Bmpbefore))

        Bmpnew[1:-1] = Bmpbefore[1:-1][:] + h*(dBmpdt[:])
        Sox9new[1:-1] = Sox9before[1:-1][:] + h*(dSox9dt[:])
        Wntnew[1:-1] = Wntbefore[1:-1][:] + h*(dWntdt[:])

        #Neuman conditions
        Bmpnew[0] = Bmpnew[1]
        Bmpnew[-1] = Bmpnew[-2]
        Wntnew[0] = Wntnew[1]
        Wntnew[-1] = Wntnew[-2]
        Sox9new[0] = Sox9new[1]
        Sox9new[-1] = Sox9new[-2]
        Concentrations.append([Bmpnew,Sox9new,Wntnew])

    return Concentrations

def Update(num, lines, Concentrations, ax1, size):
        # update plot
        for l, c in zip(lines,Concentrations[num]):
            l[0].set_ydata(c)
        time_text.set_text('frame = %.1d' % num)
        ax1.relim()
        ax1.autoscale()
        return lines, time_text
# Simulate
size = 100
steps = 1000
Bmp = np.random.uniform(-0.001,0.001,size)
Sox9 = np.random.uniform(-0.001,0.001,size)
Wnt = np.random.uniform(-0.001,0.001,size)
inits = [Bmp, Sox9, Wnt]

Concentrations = Euler(steps, 0.2, inits, size-2)


x = np.linspace(0,size,size)

#Animate
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

fig, ax1 = plt.subplots(figsize=(7,5))
ax1.set_xlim(0,size)
ax1.set_ylim(-10,10)
line1 = ax1.plot(x,Concentrations[0][0])
line2 = ax1.plot(x,Concentrations[0][1])
line3 = ax1.plot(x,Concentrations[0][2])
lines = [line1, line2, line3]
ax1.legend(["Bmp","Sox9", "Wnt"])
plt.title("Raspopovic mechanism on %d cells with %d timesteps" % (size,steps))
time_text = ax1.text(0.05, 0.95,'',horizontalalignment='left',verticalalignment='top', transform=ax1.transAxes)

for i in range(size):
    ax1.add_artist(plt.Circle((i,0),0.5, color='g'))
animation = FuncAnimation(fig, Update, steps, fargs=(lines, Concentrations, ax1, size), repeat=False, blit=False)
# animation.save('im.mp4', writer=writer)
plt.show()
