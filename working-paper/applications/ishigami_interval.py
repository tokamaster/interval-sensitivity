"""
    x = independent variable
    y = dependent variable
"""
from cmath import pi
from pyDOE import *
from scipy.stats.distributions import uniform
import numpy as np
from area_calculator import area_calculator

np.random.seed(42)

def ishigami(x, a=5, b=0.1):
    return np.sin(x[0])+a*np.sin(x[1])**2+b*np.sin(x[0])*x[2]**4
    #return x[0]+a*x[1]+b*x[2]


lower_bounds = [-pi, -pi, -pi]
upper_bounds = [pi, pi, pi]

n_samples = 1024
samples = lhs(len(lower_bounds), samples=n_samples)

#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i], scale=np.subtract(
        upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = []
for sample in samples:
    results.append(ishigami(sample))
print("output interval:", np.max(results)-np.min(results))
print("max y:", np.max(results))
print("min y:", np.min(results))

x1 = area_calculator(samples[:, 0], results, plot=False, step_size=50)
x2 = area_calculator(samples[:, 1], results, plot=False, step_size=50)
x3 = area_calculator(samples[:, 2], results, plot=False, step_size=50)

print("x1 area:", x1)
print("x2 area:", x2)
print("x3 area:", x3)

