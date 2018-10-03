
"""

simulation of self organized polarized cells using a simple potential model
with spin.
Courtesy of Kim Sneppen
Author: Henrik Pinholt

The code is structured around three sections:
The testfunctions:
    Functions used to test and plot the results of the other blocks of code
The helperfunctions:
    Section containing functions used in the classes that run the simulation
The class definitions:
    Definition of the classes that run the simulation.

The simulation is built around a grid class containing instances of a the
SimpleSpinCell class. The grid runs the simulation by telling each cell
what to do during each timestep. Since the model is based on cell surroundings
the cells update themselves using the appropriate method

"""
import random
from math import *
import numpy as np
from termcolor import *
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
%matplotlib notebook

# testfunctions to test the various classes and functions for inputs
def SimpleSpinCelltester():
    """test that you can initialize the cell with a position and spinvector"""
    try:
        cell = SimpleSpinCell(np.array([1, 2, 3]), np.array([2, 3, 4]))
        print(colored("cell initialized perfectly", "green"))
    except:
        print ("cell initialization didn't work", sys.exc_info()[0])
        raise

    # test that you can retrieve the position x,y and z values
    try:
        pos = cell.GetPos()
        if pos[0] == 1 and pos[1] == 2 and pos[2] == 3:
            print(colored("position was correctly assigned", "green"))
    except:
        print("cell GetPos malfunctioned", sys.exc_info()[0])
        raise

    # test that you can retrieve spinvector coordinates
    try:
        spin = cell.GetSpin()
        if spin[0] == 2 and spin[1] == 3 and spin[2] == 4:
            print(colored("spinvector was correctly assigned", "green"))
    except:
        print("cell GetSpin malfunctioned", sys.exc_info()[0])
        raise

def Gridtester(a):
    """Function that tests if the grid is initialized properly"""
    # initialize a square grid (standard, no other conformations are possible
    # at the moment)
    grid = Grid(a, "sq")

    # collect all cells in grid to analyze spin and position
    x, y, z = [], [], []
    cells = grid.GetCells()
    for i in cells:
        x.append(i.GetPos()[0])
        y.append(i.GetPos()[1])
        z.append(i.GetPos()[2])

    # plot initial cell position
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.scatter(x, y, z)
    plt.title("Grid with cell positions")
    plt.show()

    # test that all the spinvectors are randomly oriented by plotting them

    # first collect all the x,y and z coords
    x2, y2, z2 = [], [], []
    for i in cells:
        x2.append(i.GetSpin()[0])
        y2.append(i.GetSpin()[1])
        z2.append(i.GetSpin()[2])

    # plot the vectors
    fig2 = plt.figure()
    ax2 = fig2.gca(projection='3d')
    ax2.quiver(np.zeros(len(x2)), np.zeros(len(y2)), np.zeros(len(z2)), x2, y2,
               z2, arrow_length_ratio=0.01)
    ax2.set_xlim3d(-1, 1)
    ax2.set_ylim3d(-1, 1)
    ax2.set_zlim3d(-1, 1)
    plt.title("Spin vector distribution in 3D")
    plt.show()

    # code block for checking that the length of all spinvectors are 1
    lengths = []
    fig3 = plt.figure()
    for i in range(len(x2)):
        lengths.append(sqrt(x2[i]**2 + y2[i]**2 + z2[i]**2))
    plt.hist(lengths)
    plt.title("Spin-vector lengths")
    plt.show()

    # Test the voronoi function

    # get cell coords:
    points = []
    for i in grid.GetCells():
        points.append([])
    Voronoi(points)

# The following section contains shorthand functions used to simplify the
# calculations in the definition of the classes tha run the simulation
def Voronoi(points):
    """Function that takes an array of 3D points and calculates the 3D
    Voronois cells and stores them in a voronois object. This object is returned
    """
    # Generate the voronoi object based on the point

def SpinAssign(randspin=True):
        """function that returns a random unit vector of spin coordinates
        in 3 dimensional space"""
        if randspin:
            # generate a random vector
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(-1, 1)

            # calculate the vector length
            lenght = sqrt(x**2 + y**2 + z**2)

            # return the normalized vector
            return (1 / (lenght)) * np.array([x, y, z])

def squareinit(sidelen):
    """function that outputs a list of cellnum cells organized in a
    square in a discretized grid centered at [0,0,0]"""

    # calculate corner coordinates, making sure the sidelen and center
    # is [0,0,0], if the sidelength is odd, the
    # square is displaced one coordinate towards the positive quadrant
    # (x>0,y>0,z>0) by taking half the sidelength
    # and rounding down to get the negative corner (ncorner) of the square
    # (x<0,y<0,z<0) and then finding the other edges

    # if sidelen is even, the square need not be displaced, and is symmetric
    # aroun the center:
    if sidelen % 2 == 0:
        halflen = int(sidelen / 2)
        # generate the list of cells by a triple loop from the bottom-most
        # corner of the square to the topmost.
        cells = []
        for x in range(-halflen, halflen + 1):
            for y in range(-halflen, halflen + 1):
                for z in range(-halflen, halflen + 1):
                    cells.append(SimpleSpinCell(np.array([x, y, z]),
                                 SpinAssign()))
    else:
        halflen = int(sidelen / 2)
        # generate the list of cells by a triple loop from the bottom-most
        # corner of the square to the topmost.
        # Since the sidlenght was odd, the square needs to be displaced by
        # one in the x, y and z-direction. The halflen is smaller than the
        # floating point sidelen/2, so the loops should range from -halflen
        # to halflen+1 (+2 because the range function doesn't include the
        # last number)
        cells = []
        for x in range(-halflen, halflen + 2):
            for y in range(-halflen, halflen + 2):
                for z in range(-halflen, halflen + 2):
                    cells.append(SimpleSpinCell(np.array([x, y, z]),
                                                SpinAssign()))
    return cells

# Define the classes used to run the simulation
class SimpleSpinCell:
    """A basic polarized cell"""
    def __init__(self, pos, spin):
        """initialize, takes a numpy array pos=[x,y,z] containing the initial
        coordinates of the cell, and an array spin=[x,y,z]
        with the initial coordinates of the cell polarization"""
        # check that the position is a numpy array of length 3
        if isinstance(pos, np.ndarray) and len(pos) == 3:
            self.pos = pos
        else:
            raise Exception("position is not a numpy array of length 3")
        # check that the spinvector is a numpy array of length 3
        if isinstance(spin, np.ndarray) and len(pos) == 3:
            self.spin = spin
        else:
            raise Exception("spin is not a numpy array of length 3")

    def GetPos(self):
        """function for getting the current cell position"""
        return self.pos

    def GetSpin(self):
        """function for getting the current cell spin coordinates"""
        return self.spin

    def Update(self):
        """Updates the cell position and polarization based on equation (1) in
        "Self-organization of polar cells into long-lived topological
        structures (Nissen, Rønhild, Trusina, Kim Sneppen) Aug 21 2017"""
class Grid:
    """3-dimensional discrete grid to contain the particles and their positions"""

    def __init__(self, cellnum, geometry, randspin=True):
        """initializes grid as a list of cellnum cells based on the rule passed
        as string in geometry and whether randspin is True or not"""
        # initialize grid parameters
        self.cellnum = cellnum
        self.geometry = geometry
        self.randspin = randspin

        # generate the cells list in the grid based on the initialize method
        self.geometry = geometry
        sidelen = int(cellnum**(1. / 3.))
        if self.geometry == geometry:
            self.cells = squareinit(sidelen)

    def GetCells(self):
        return self.cells

    def GetGeometry(self):
        return self.geometry

    def GetRandspin(self):
        return self.randspin

# command line statments
Gridtester(100)
