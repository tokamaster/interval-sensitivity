from cmath import pi
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from area_calculator import *

def ishigami(x, a=5, b=0.1):
    solution = []
    for element in x:
        solution.append(
            np.sin(element[0])+a*np.sin(element[1])**2+b*np.sin(element[0])*element[2]**4)
    return np.array(solution)


problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[-pi, pi]]*3
}

# Generate samples
param_values = saltelli.sample(problem, 8192)

Y = ishigami(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)


# Interval Based Sensitivity Analysis
x1 = area_calculator(param_values[:, 0], Y, step_size=100)
x2 = area_calculator(param_values[:, 1], Y, step_size=100)
x3 = area_calculator(param_values[:, 2], Y, step_size=100)

print('Interval Area x1:', x1)
print('Interval Area x2:', x2)
print('Interval Area x3:', x3)

#box_plotter(param_values[:, 0], Y, step_size=100)
#plt.show()
