import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol

def displacement(width, height, load=1e6, length=5, young=10e9, density=600):
    disps = []
    for i in range(len(width)):
        inertia = width[i]*height[i]**3/12
        a = (density*9.81*width[i]*length**4)/(8*young*inertia)
        b = (load*length**3)/(3*young*inertia)
        disps.append(a+b)
    return np.array(disps)

problem = {
    'names': ['width', 'height'],
    'num_vars': 2,
    'bounds': [[0.05, 0.3], [0.2, 0.5]],
    'dists': ['unif', 'unif']
}
param_values = saltelli.sample(problem, 1024)
Y = displacement(param_values[:,0],param_values[:,1])
Si = sobol.analyze(problem, Y, print_to_console=True)
