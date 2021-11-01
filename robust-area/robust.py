"""
    x = independent variable
    y = dependent variable
"""
from pyDOE import *
from scipy.stats.distributions import uniform
import numpy as np
import matplotlib.pyplot as plt

def area_calculator(x,y,step_size=100,plot=False):

    bin_edges = np.linspace(np.min(x), np.max(x), step_size + 1)
    edge_location = []
    for i in range(len(x)):
        for j in range(step_size):
            if bin_edges[j] <= x[i] <= bin_edges[j+1]:
                edge_location.append(j)
                break

    areas = []
    heights = []

    for i in range(step_size):
        samps = []
        for j in range(len(y)):
            if edge_location[j] == i:
                samps.append(y[j])
        height = np.max(samps)- np.min(samps)
        heights.append(height)
        base = bin_edges[i+1]-bin_edges[i]
        areas.append(height*base)

    absolute_area = np.sum(areas)
    total_area = (np.max(y)-np.min(y))*(np.max(x)-np.min(x))
    if plot == True:
        plt.hist(bin_edges[:-1],bin_edges,weights=heights)
        plt.show()
    return 1-(absolute_area/total_area)


np.random.seed(42)

def ishigami(x, a=5, b=0.1):
    return np.sin(x[0])+a*np.sin(x[1])**2+b*np.sin(x[0])*x[2]**4

lower_bounds = [-3.14, -3.14, -3.14]
upper_bounds = [3.14, 3.14, 3.14]

n_samples = 100000
samples = lhs(len(lower_bounds), samples=n_samples)

#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i], scale=np.subtract(
        upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = []
for sample in samples:
    results.append(ishigami(sample))

print("x1 area:", area_calculator(samples[:,0],results,plot=True))
print("x2 area:", area_calculator(samples[:,1],results,plot=True))
print("x3 area:", area_calculator(samples[:, 2], results,plot=True))


