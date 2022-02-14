from pyDOE import *
from scipy.stats.distributions import uniform
import numpy as np
from area_calculator import area_calculator

def displacement(width, height, load=1e6, length=5, young=10e9, density=600):
    disps = []
    for i in range(len(width)):
        inertia = width[i]*height[i]**3/12
        a = (density*9.81*width[i]*length**4)/(8*young*inertia)
        b = (load*length**3)/(3*young*inertia)
        disps.append(a+b)
    return disps

lower_bounds = [0.05, 0.2]
upper_bounds = [0.3, 0.5]

n_samples = 5000
samples = lhs(len(lower_bounds), samples=n_samples)

#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i], scale=np.subtract(
        upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = displacement(samples[:,0], samples[:,1])

print("output interval:", np.max(results)-np.min(results))
print("max y:", np.max(results))
print("min y:", np.min(results))

import matplotlib.pyplot as plt

plt.scatter(samples[:,0],results)
plt.show()
plt.scatter(samples[:,1], results)
plt.show()

x1 = area_calculator(samples[:, 0], results, plot=True, step_size=100)
x2 = area_calculator(samples[:, 1], results, plot=True, step_size=100)

print("x1 area:", x1)
print("x2 area:", x2)
