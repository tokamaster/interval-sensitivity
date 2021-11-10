import matplotlib.pyplot as plt
from area_calculator import area_calculator
from scipy.stats import chi2
import numpy as np
np.random.seed(66)

def liu_function(n):
    """Found in:
    Liu, H., Chen, W., and Sudjianto, A. (April 24, 2005).
    "Relative Entropy Based Method for Probabilistic
    Sensitivity Analysis in Engineering Design."
    ASME. J. Mech. Des. March 2006; 128(2): 326–336.
    https://doi.org/10.1115/1.2159025

    Args:
        x (int): number of input samples
    """
    x1 = chi2.rvs(10, size=n)
    x2 = chi2.rvs(13.978, size=n)

    return x1/x2, x1, x2

samples = liu_function(50000)
plt.scatter(samples[1], samples[0])
plt.show()

print("x1 area:", area_calculator(samples[1],samples[0],step_size=95))
print("x2 area:", area_calculator(samples[2],samples[0],step_size=95))


