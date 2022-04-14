from cmath import pi
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
from area_calculator import *
import matplotlib.pyplot as plt
problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[-1,1],[-1,1],[-1,1]],
    'dists': ['unif', 'unif', 'unif']
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
        solution.append(0.2*element[0]-5*element[1]+10*element[1]*element[2])
    return np.array(solution)


def ishigami(x, a=5, b=0.1):
    solution = []
    for element in x:
        solution.append(np.sin(element[0])+a*np.sin(element[1])**2+b*np.sin(element[0])*element[2]**4)
    return np.array(solution)

print("Cross function Sobol' results:")
param_values = saltelli.sample(problem, 1024)
print(param_values[:, 2])
Y = cross_function(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True)


# Cross function IB
print("Cross function IB")
aa1 = area_calculator(param_values[:, 0], Y, step_size=200)
aa2 = area_calculator(param_values[:, 1], Y, step_size=200)
#aa3 = area_calculator(param_values[:, 2], Y, step_size=20)
#aa4 = area_calculator(param_values[:, 3], Y, step_size=20)
print("x1:", aa1)
print("x2:", aa2)
#print("x3:", aa3)
#print("noise:", aa4)

problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[-pi, pi], [-pi, pi], [-pi, pi]],
    'dists': ['unif', 'unif', 'unif']
}

param_values = saltelli.sample(problem, 1024)
Y = ishigami(param_values)
print("Ishigami function Sobol' results:")
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

st1, st2, st3 = true_total_sobol(5,0.1)
print("True Total Sobol':", st1, st2, st3)
s1, s2, s3 = true_first_sobol(5,0.1)
print("True First-Order Sobol':", s1, s2, s3)

print("Results below: discrepancy between Sobol' indices and Interval-SA for a simple linear function")
print("Interval-SA successfully identifies x2 has no impact.")

def linfun(x):
    solution = []
    for element in x:
        solution.append(-5*element[0])
    return np.array(solution)


problem = {
    'names': ['x1', 'x2'],
    'num_vars': 2,
    'bounds': [[-5, 5], [-5, 5]],
    'dists': ['unif', 'unif']
}

param_values = saltelli.sample(problem, 1024)
Y = linfun(param_values)
Si = sobol.analyze(problem, Y, print_to_console=True, calc_second_order=False)
plt.scatter(param_values[:, 1], Y)
plt.show()
#Linear function IB
aa1 = area_calculator(param_values[:,0], Y, step_size=100)
aa2 = area_calculator(param_values[:,1], Y, step_size=100)
print(aa1,aa2)

# Nonlinear function


def nonlinear_function(x):
    """Found in:
    Section 5.1.1

    Liu, H., Chen, W., and Sudjianto, A. (April 24, 2005).
    "Relative Entropy Based Method for Probabilistic
    Sensitivity Analysis in Engineering Design."
    ASME. J. Mech. Des. March 2006; 128(2): 326–336.
    https://doi.org/10.1115/1.2159025

    Args:
        x (int): input samples
    """
    solution = []
    for element in x:
        solution.append(element[0]*element[1]+element[2]**2)
    return np.array(solution)


problem = {
    'names': ['x1', 'x2', 'x3'],
    'num_vars': 3,
    'bounds': [[-1, 1], [-1, 1], [-1, 1]],
    'dists': ['unif', 'unif', 'unif']
}

param_values = saltelli.sample(problem, 1024)
Y = nonlinear_function(param_values)
print("Nonlinear function Sobol' results:")
Si = sobol.analyze(problem, Y, print_to_console=True)
