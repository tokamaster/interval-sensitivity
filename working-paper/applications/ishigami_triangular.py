from cmath import pi
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from area_calculator import *

np.random.seed(42)

def ishigami(x, a=5, b=0.1):
    solution = []
    for element in x:
        solution.append(
            np.sin(element[0])+a*np.sin(element[1])**2+b*np.sin(element[0])*element[2]**4)
    return np.array(solution)

problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[0, 1]]*3
}

# Generate samples
param_values = saltelli.sample(problem, 2048)

# using triangular inverse CDF
param_values[:,0] = sp.stats.triang.ppf(param_values[:,0],1/2,-pi,2*pi)
param_values[:,1] = sp.stats.triang.ppf(param_values[:,1],1/2,-pi,2*pi)
param_values[:,2] = sp.stats.triang.ppf(param_values[:,2],1/2,-pi,2*pi)

Y = ishigami(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)
