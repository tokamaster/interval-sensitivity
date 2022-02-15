Available functions:
* Ishigami
* Cantilever beam
* Cross function
* Liu function
* Nonlinear function

# Ishigami function

Contains a pure additive input ($x_2$), whilst $x_1$ and $x_3$ have a combination
effect.

Well known in literature, it is possible to get the analytical Sobol' indices when
the inputs follow a uniform distribution.

Analytical Sobol':

|        | Total | First Order |
|--------|-------|-------------|
| $x_1$  | 0.712 (1) | 0.400 (1)|
| $x_2$  | 0.288 (3) | 0.288 (2)|
| $x_3£$ | 0.311 (2) | 0.0   (3)|

Interval metric with sampling (5000 samples, step size = 100):

|        | Index |
|--------|-------|
| $x_1$  | 0.610 (1)|
| $x_2$  | 0.375 (3)|
| $x_3£$ | 0.311 (2)|


Interval metric with sampling (100000 samples, step size = 100):

|        | Index |
|--------|-------|
| $x_1$  | 0.578 (2)|
| $x_2$  | 0.217 (3)|
| $x_3£$ | 0.581 (1)|

Interval metric with arithmetic (subintervals = 20):

|        | Index |
|--------|-------|
| $x_1$  | 0.534 (2)|
| $x_2$  | 0.151 (3)|
| $x_3£$ | 0.549 (1)|

Interval metric with arithmetic (subintervals = 100):

|        | Index |
|--------|-------|
| $x_1$  | 0.568 (2)|
| $x_2$  | 0.181 (3)|
| $x_3£$ | 0.581 (1)|

Interval metric with arithmetic (subintervals = 200):

|        | Index |
|--------|-------|
| $x_1$  | 0.572 (2)|
| $x_2$  | 0.185 (3)|
| $x_3£$ | 0.584 (1)|

It is interesting the discrepancy in the ranking between Sobol' and the interval
metric. Note that in the sampling-based method, the number of samples has to be
relatively large to notice the discrepancy.
Possible sources of discrepancy:

* Sobol' measures variance, whilst interval measures output's interval width.
* Sobol' asumes uniform distribution, whilst interval doesn't assume any.

These are the only two differences between Sobol' and Interval in this example.

A benefit of Sobol' indices is that one can measure first and total order
effects, and therefore account for combination effects. For example, from Sobol'
we can observe that $x_2$ has no combination effects, since its first order and
total order indices are the same. It is not possible to obtain this kind of
information with the Interval-based method (to the best of my knowledge).


# Cantilever beam

# Cross function

# Liu function

# Nonlinear function
