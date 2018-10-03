import matplotlib.pyplot as plt
class X:
    '''module that takes input, and generates an output on the basis on the function
        of an enzyme E'''
    def __init__(self,a,inicon):
        self.a = a
        self.concentration = float(inicon)

    def update(self,Input,E):
    #updates the concentration from differential equation page 8
        oldcon = self.concentration
        self.concentration = Input - (self.a*E*(oldcon**0.5))
        return self.concentration

    def __str__(self):
        return "a = %d con = %f" % (self.a , self.concentration)

class Y(X):
    '''function that inheritates the characteristics of X except for being
        regulated by E and having an input'''
    def update(self,Input):
        oldcon = self.concentration
        self.concentration = Input - self.a*(oldcon**0.5)
        return self.concentration

class Z(Y):
    '''Does the excact same as Y with concentration of Y as input instead of X'''

class E(Y):
    '''an enzyme that is upregulated by Z but serves itself no functional purpose
    is to be inserted as E when updating X)'''
    def getconcentration(self):
        return self.concentration

def runsim():
    record = [(1,1,1,1)]
    #initialize variables and records
    x = X(0.1,1)
    y = Y(0.2,1)
    z = Z(0.5,1)
    e = E(0.1,1)
    concentration = (1,1,1,1)

    #update 10 timestep and record results
    for i in range(30):
        xcon = x.update(2,e.getconcentration())
        ycon = y.update(xcon)
        zcon = z.update(ycon)
        econ = e.update(zcon)
        #record results
        concentration = (xcon,ycon,zcon,econ)
        record.append(concentration)
    #order the data
    x = []
    y = []
    z = []
    e = []
    for i in range(len(record)):
        x.append(record[i][0])
        y.append(record[i][1])
        z.append(record[i][2])
        e.append(record[i][3])

    #plot
    plt.plot(x,label='x')
    plt.plot(y,label = 'y')
    plt.plot(z, label = 'z')
    plt.plot(e, label = 'e')
    plt.legend()
    plt.show()
def test():
    z = Z(1,2)
    print(z)
    print ("updating")
    z.update(12)
    print (z)


runsim()
