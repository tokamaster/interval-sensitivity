using ProbabilityBoundsAnalysis, IntervalArithmetic, PyPlot

ProbabilityBoundsAnalysis.setSteps(500)

#a = N(interval(0, 0.5),1)
#a = N(0,3)
a = U(interval(-10,-8),10)

#f(x) = sin(x) + cos(x)
f(x) = x^2

fe_in = interval.(a.u, a.d)
fe_out = f.(fe_in)

#two_d = fe_in .× fe_out

ProbabilityBoundsAnalysis.plotBoxes(fe_in, fe_out)

