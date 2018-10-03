import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
a = 2.8e-4
b = 5e-3
tau = .1
k = -.005

size = 100  # size of the 2D grid
dx = 2./size  # space step
T = 10.0  # total time
dt = .9 * dx**2/2  # time step
n = 10

Unew = np.random.rand(size, size)
Vnew = np.random.rand(size, size)

def laplacian(Z):
    Ztop = Z[0:-2,1:-1]
    Zleft = Z[1:-1,0:-2]
    Zbottom = Z[2:,1:-1]
    Zright = Z[1:-1,2:]
    Zcenter = Z[1:-1,1:-1]
    return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2
Concentration = []
# We simulate the PDE with the finite difference method.
for i in range(n):
    Ubef = Unew
    Vbef = Unew
    # We compute the Laplacian of u and v.
    deltaU = laplacian(Ubef)
    deltaV = laplacian(Vbef)
    # We take the values of u and v inside the grid.
    Ucb = Ubef[1:-1,1:-1]
    Vcb = Vbef[1:-1,1:-1]
    # We update the variables.
    Unew[1:-1,1:-1], Vnew[1:-1,1:-1] = \
        Ucb + dt * (a * deltaU + Ucb - Uc**3 - Vcb + k), \
        Vcb + dt * (b * deltaV + Ucb - Vc) / tau
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (Unew, Vnew):
        Z[0,:] = Z[1,:]
        Z[-1,:] = Z[-2,:]
        Z[:,0] = Z[:,1]
        Z[:,-1] = Z[:,-2]
    Concentration.append(Unew)
def Update(frame, Concentration):
    image.set_array(Concentration[frame])
    return image
print "animating"
fig = plt.figure()
image = plt.imshow(U, cmap=plt.cm.copper, extent=[-1,1,-1,1])
animation = FuncAnimation(fig, Update, frames = n, fargs=(Concentration))
plt.show()
