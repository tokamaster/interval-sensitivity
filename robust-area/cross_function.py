import numpy as np
from area_calculator import *

def cross_function(x1,x2,x3,noise):
    """
    From https://arxiv.org/pdf/1309.6392.pdf
    Equation (3):
    0.2*x1-5*x2+10*x2*I+noise
    where x1,x2,I are uniform in [-1,1] and noise normal(0,1)

    I is an identity function:
    1 when I>=0
    0 when I<0
    """
    a = []
    for element in x3:
        if element >= 0:
            a.append(1)
        else:
            a.append(0)
    return 0.2*x1-5*x2+10*x2*a+noise

x1 = np.random.uniform(-1,1,10000)
x2 = np.random.uniform(-1,1,10000)
x3 = np.random.uniform(-1,1,10000)
noise = np.random.normal(loc=0,scale=1,size=10000)

y = cross_function(x1,x2,x3,noise)

print("x1:", area_calculator(x1,y))
print("x2:", area_calculator(x2,y))
print("x3:", area_calculator(x3, y))
