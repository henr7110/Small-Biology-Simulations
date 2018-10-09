import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy.random as rd
L = 20
p = 0.5
k = 0.01
j_0 = 1
show = 1

X = np.zeros(L)
def Update(X,i,Broken):
    if i % j_0 == 0:
        X[0] += 1
    piles = np.copy(X)
    for a in range(len(X)):
        if a == 0:
            for b in range(int(piles[a])):
                if rd.random() <= k:
                    X[a] -= 1
                    Broken += 1
                else:
                    if rd.random() <= p:
                        X[a+1] += 1
                        X[a] -= 1
        elif a == L-1:
            if piles[a] != 0:
                for b in range(int(piles[a])):
                    if rd.random() <= k:
                        X[a] -= 1
                        Broken += 1
                    else:
                        if rd.random() <= p:
                            X[a-1] += 1
                            X[a] -= 1
        else:
            if piles[a] != 0:
                for b in range(int(piles[a])):
                    if rd.random() <= k:
                        X[a] -= 1
                        Broken += 1
                    else:
                        rdm = rd.random()
                        if rdm <= p:
                            X[a+1] += 1
                            X[a] -= 1
                        if rdm > p and rdm <= 2*p:
                            X[a-1] += 1
                            X[a] -= 1
    return X,Broken

def animate(i):
    if i % 1 == 0:
        line.set_ydata(animate.X)
        t.set_text("%d Points" % sum(animate.X))
        t1.set_text("%d Broken Down" % animate.Broken)
    animate.X,animate.Broken = Update(animate.X,animate.counter,animate.Broken)
    animate.counter += 1
animate.X = X
animate.Broken = 0
animate.counter = 0
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_ylim((0.5,20))
t = ax1.text(8,18,"0 Points")
t1 = ax1.text(7,17,"0 Broken Down")
line, = ax1.plot(X,color="black")
anim = animation.FuncAnimation(fig, animate,interval=100)
plt.show()
