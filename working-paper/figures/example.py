import numpy as np
from pyDOE import *
import matplotlib.pyplot as plt
from scipy.stats.distributions import uniform
from publib import set_style, fix_style
from area_calculator import area_calculator
set_style(['origin'])
plt.rcParams['text.usetex'] = True


plt.rc("font", size=25)          # controls default text sizes
plt.rc("axes", labelsize=25)    # fontsize of the x and y labels
plt.rc("xtick", labelsize=23)    # fontsize of the tick labels
plt.rc("ytick", labelsize=23)    # fontsize of the tick labels


np.random.seed(222)

def function_example(x):
    noise = []
    for sample in x:
        noise.append(np.random.normal(loc=0, scale=np.sqrt(sample[0]**2)))
    results = []
    for i in range(len(noise)):
        results.append(-4*x[i][0]+noise[i])
    return results

lower_bounds = [-5, -5]
upper_bounds = [5, 5]
samples = lhs(len(lower_bounds), samples=1000)
#Latin Hypercube Sampling of means
for i in range(len(lower_bounds)):
    samples[:, i] = uniform(loc=lower_bounds[i],
                            scale=np.subtract(upper_bounds[i],
                            lower_bounds[i])).ppf(samples[:, i])

results = function_example(samples)
# Figure 1 generator
#plt.scatter(samples[:,1], results) #0 for x_1, 1 for x_2
#plt.xlabel('$x_2$')
#plt.ylabel('$y$')
#plt.tight_layout()
#fix_style(['origin'])

#plt.savefig('example_x2.pdf', bbox_inches='tight', dpi=300)

x1 = area_calculator(samples[:, 0], results, plot=True, step_size=20)
x2 = area_calculator(samples[:, 1], results, plot=True, step_size=20)

print("x1 sensitivity measure:", x1)
print("x2 sensitivity measure:", x2)
print(np.max(results))
print(np.min(results))
