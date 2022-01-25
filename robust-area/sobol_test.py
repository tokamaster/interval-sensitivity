from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np

problem = {
    'names': ['x1', 'x2', 'x3','noise'],
    'num_vars': 4,
    'bounds': [[-1,1],[-1,1],[-1,1],[0,1]],
    'dists': ['unif', 'unif', 'unif','norm']
}


def cross_function(input):
    """
    From https://arxiv.org/pdf/1309.6392.pdf
    Equation (3):
    0.2*x1-5*x2+10*x2*I+noise
    where x1,x2,I are uniform in [-1,1] and noise normal(0,1)

    I(x3) is a function similar to Kronecker delta:
    1 when x3>=0
    0 when x3<0
    """
    for element in input:
        if element[2] >= 0:
            element[2] = 1
        else:
            element[2] = 0
    solution = []
    for element in input:
        solution.append(0.2*element[0]-5*element[1]+10*element[1]*element[2]+element[3])
    return np.array(solution)


param_values = saltelli.sample(problem, 1024)
Y = cross_function(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)
