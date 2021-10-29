from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
from scipy.stats.distributions import uniform
import numpy as np
from pyDOE import *
np.random.seed(42)

def ishigami(x, a=5, b=0.1):
    return np.sin(x[0])+a*np.sin(x[1])**2+b*np.sin(x[0])*x[2]**4


lower_bounds = [-3.14, -3.14, -3.14]
upper_bounds = [3.14, 3.14, 3.14]

n_samples = 10
samples = lhs(len(lower_bounds), samples=n_samples)

#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i], scale=np.subtract(
        upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = []
for sample in samples:
    results.append(ishigami(sample))

points1 = []
points2 = []
points3 = []

for i in range(len(results)):
    points1.append(samples[i, 0])
    points2.append(samples[i, 1])
    points3.append(samples[i, 2])

points1 = np.array(points1)
points2 = np.array(points2)
points3 = np.array(points3)

from scipy import interpolate
tck,u = interpolate.splprep([points1,results],k=5,s=32)
print(tck)
print(u)

x_eval = np.linspace(-3.14,3.14,10)
spline_prediction = interpolate.splev(x_eval, tck)
print(spline_prediction)

plt.scatter(points1,results,color='blue')
plt.plot(spline_prediction[0],spline_prediction[1],color='black')
plt.show()