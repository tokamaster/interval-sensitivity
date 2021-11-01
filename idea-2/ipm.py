from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from scipy.stats.distributions import uniform
import numpy as np
from pyDOE import *
import PyIPM
np.random.seed(42)

def ishigami(x,a=5,b=0.1):
    return np.sin(x[0])+a*np.sin(x[1])**2+b*np.sin(x[0])*x[2]**4

lower_bounds = [-3.14, -3.14, -3.14]
upper_bounds = [3.14, 3.14, 3.14]

n_samples = 10000
samples = lhs(len(lower_bounds), samples=n_samples)

#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i], scale=np.subtract(
        upper_bounds[i], lower_bounds[i])).ppf(samples[:, i])

results = []
x_train = []
for sample in samples:
    results.append(ishigami(sample))
    x_train.append([sample[0]])

model = PyIPM.IPM(polynomial_degree=10)

model.fit(np.array(x_train),np.array(results))
x = np.linspace(-3.14,3.14,1000)
x_pred = []
for i in x:
    x_pred.append([i])
upper_bound, lower_bound = model.predict(np.array(x_pred))

from scipy.stats import wasserstein_distance
print(wasserstein_distance(upper_bound[:, 0], lower_bound[:, 0]))
print(np.max(results)-np.min(results))

plt.scatter(x, lower_bound[:, 0])
plt.scatter(x, upper_bound[:, 0])
plt.scatter(samples[:, 0], results, color='black')
plt.show()

x = np.sort(lower_bound[:, 0])
y = np.arange(len(x))/float(len(x))
plt.plot(x, y, color='blue')
x = np.sort(upper_bound[:, 0])
y = np.arange(len(x))/float(len(x))
plt.plot(x, y, color='red')
plt.show()


"""
points = []

for i in range(len(results)):
    points.append([samples[i,0],results[i]])

points = np.array(points)
hull = ConvexHull(points)

plt.plot(points[:, 0], points[:, 1], 'o')
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
plt.show()
"""
