from cmath import pi
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
from area_calculator import *

def ishigami(x, a=5, b=0.1):
    solution = []
    for element in x:
        solution.append(
            np.sin(element[0])+a*np.sin(element[1])**2+b*np.sin(element[0])*element[2]**4)
    return np.array(solution)

problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[-pi, pi], [-pi, pi], [-pi, pi]],
    'dists': ['unif', 'unif', 'unif']
}

param_values = saltelli.sample(problem, 1024)
Y = ishigami(param_values)
print("Ishigami function Sobol' results (with uniform distributions):")
Si = sobol.analyze(problem, Y, print_to_console=True)

problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[pi, 0.5], [pi, 0.5], [pi, 0.5]],
    'dists': ['triang', 'triang', 'triang']
}

param_values = saltelli.sample(problem, 1024)
Y = ishigami(param_values)
plt.scatter(param_values[:, 0], Y)
plt.show()
print("Ishigami function Sobol' results:")
Si = sobol.analyze(problem, Y, print_to_console=True)
