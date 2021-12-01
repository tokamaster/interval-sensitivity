import matplotlib.pyplot as plt
from area_calculator import area_calculator
from pyDOE import *
from scipy.stats.distributions import uniform
import numpy as np
np.random.seed(66)

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

    return x[0]*x[1]+x[2]**2, x[0], x[1], x[2]

lower_bounds = [-1, -1, -1]
upper_bounds = [1, 1, 1]
samples = lhs(len(lower_bounds), samples=100000)
#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i],
                            scale=np.subtract(upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = []
for sample in samples:
    results.append(nonlinear_function(sample))
print("output interval:", np.max(results)-np.min(results))
print("max y:", np.max(results))
print("min y:", np.min(results))

x1 = area_calculator(samples[:, 0], results, plot=True, step_size=500)
x2 = area_calculator(samples[:, 1], results, plot=True, step_size=500)
x3 = area_calculator(samples[:, 2], results, plot=True, step_size=500)

print("x1 area:", x1)
print("x2 area:", x2)
print("x3 area:", x3)
