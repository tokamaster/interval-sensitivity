from scipy.stats import wasserstein_distance
import alphashape
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from scipy.stats.distributions import uniform
import numpy as np
import math
from pyDOE import *
np.random.seed(42)

def ishigami(x, a=5, b=0.1):
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
for sample in samples:
    results.append(ishigami(sample))

points = []

for i in range(len(results)):
    points.append([samples[i, 1], results[i]])

points = np.array(points)

#alpha = alphashape.optimizealpha(points)
#print(alpha)
#for x3 use 2.0
#for x2 use 1.87
#for x1 use 4.0
hull = alphashape.alphashape(points, 1.87)
hull_pts = hull.exterior.coords.xy

upper = []
lower = []
for i in range(len(hull_pts[0])):
    if i < len(hull_pts[0])/2:
        lower.append([hull_pts[0][i],hull_pts[1][i]])
    if i >= len(hull_pts[0])/2:
        upper.append([hull_pts[0][i], hull_pts[1][i]])
upper = np.array(upper)
lower = np.array(lower)

print(wasserstein_distance(upper[:,1],lower[:,1]))
print(np.max(results)-np.min(results))
plt.scatter(upper[:,0],upper[:,1],color='red')
plt.scatter(lower[:, 0], lower[:, 1], color='blue')
plt.show()

import seaborn as sns
sns.ecdfplot(upper[:, 1], color='red')
sns.ecdfplot(lower[:, 1], color='blue')
plt.show()
"""
fig, ax = plt.subplots()
ax.scatter(samples[:, 0], results)
ax.scatter(hull_pts[0], hull_pts[1], color='red')
ax.add_patch(PolygonPatch(hull, fill=False, color='green'))
plt.show()
"""


