"""Fun with oscillations"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
from scipy.optimize import broyden1


def dXdt(X, t):
    """Calculate derivatives dX/dt, [t] ~ 3-4 days"""
    G, S, RNA = X

    d_G = 1/10
    d_RNA = 10

    def act(X, K): return X**2/(X**2 + K**2)
    def inh(X, K): return K**2/(X**2 + K**2)

    dGdt = act(RNA, 0.1) - ((t > -1)*(t < 0)*3 + d_G)*G
    dSdt = 0
    dRNAdt = inh(S, 0.5) - d_RNA*RNA

    return [dGdt, dSdt, dRNAdt]


"""Integrate ODE"""
n_generations = 15
steps_per_generation = 50

# Find steady solution
G_0, S_0, RNA_0 = 1, 1, 1
for _ in range(50):
    solution = odeint(dXdt, [G_0, G_0, RNA_0],
        np.linspace(0, 1, steps_per_generation))
    G_0, RNA_0 = solution[-1,0], solution[-1,2]

# Apply heat and solve relaxation
G = np.array([G_0])
S = np.empty(0)
RNA = np.array([RNA_0])
for generation in range(-1, n_generations):
    solution = odeint(dXdt, [G[-1], G[-1], RNA[-1]],
        np.linspace(generation, generation+1, steps_per_generation+1))
    G = np.concatenate((G[:-1], solution[:,0]))
    S = np.concatenate((S, solution[:,1]))
    RNA = np.concatenate((RNA[:-1], solution[:,2]))


"""Plot solution"""
print('Max. G:    ', G.max(), '\nMax. RNA:  ', RNA.max(), '\nMax. S:    ', S.max())

sns.set_style('ticks')
plt.ylim(0, 1.02)
# plt.gca().set_yscale('log')

t = np.linspace(-1, n_generations, steps_per_generation*(n_generations+1) + 1)
plt.plot(t, G/G.max(), color=sns.color_palette()[0], label='G')
plt.plot(t, RNA/RNA.max(), color=sns.color_palette()[2], label='RNA')

S = S.reshape((n_generations+1, -1)).T
t = np.concatenate((t[:-1].reshape((n_generations+1, -1)).T,
    [np.arange(n_generations+1)]))
plt.plot(t, S/S.max(), color=sns.color_palette()[1], label='S')

sns.despine()
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles[:2] + [handles[-1]], labels[:2] + [labels[-1]])
plt.tight_layout()
plt.savefig('oscillator.png')
plt.show()
