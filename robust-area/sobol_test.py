from cmath import pi
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


def ishigami(x, a=5, b=0.1):
    solution = []
    for element in x:
        solution.append(np.sin(element[0])+a*np.sin(element[1])**2+b*np.sin(element[0])*element[2]**4)
    return np.array(solution)

param_values = saltelli.sample(problem, 1024)
Y = cross_function(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)

problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[-pi, pi], [-pi, pi], [-pi, pi]],
    'dists': ['unif', 'unif', 'unif']
}
param_values = saltelli.sample(problem, 1024)
Y = ishigami(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)

def true_total_sobol(a,b):
    #total effects
    vt1 = 0.5*(1+(b*pi**4)/5)**2 + 8*(b**2)*(pi**8)/225
    vt2 = a**2/8
    vt3 = 8*(b**2)*(pi**8)/225
    vy = a**2/8+b*pi**4/5+b**2*pi**8/18+0.5
    st1 = vt1/vy
    st2 = vt2/vy
    st3 = vt3/vy
    return st1, st2, st3

def true_first_sobol(a,b):
    #first order effects
    v1 = 0.5*(1+b*pi**4/5)**2
    v2 = a**2/8
    v3 = 0
    vy = a**2/8+b*pi**4/5+b**2*pi**8/18+0.5
    s1 = v1/vy
    s2 = v2/vy
    s3 = v3/vy
    return s1, s2, s3

st1, st2, st3 = true_total_sobol(7,0.1)
print("True Total Sobol':", st1, st2, st3)
s1, s2, s3 = true_first_sobol(7,0.1)
print("True First-Order Sobol':", s1, s2, s3)
