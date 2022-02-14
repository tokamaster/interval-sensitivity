using IntervalArithmetic, Plots, Distributions

## Define function. Interval box input.
load = 1e6; lengthz = 5; young = 10e9; density = 600

f(x:: IntervalBox) = (density*9.81*x.v[1]*lengthz^4)/(8*young*(x.v[1]*x.v[2]^3/12)) + (load*lengthz^3)/(3*young*(x.v[1]*x.v[2]^3/12))

## Input variables
x1 = interval(0.05, 0.3)
x2 = interval(0.2, 0.5)


# Make interval box
X = x1 × x2

# Sub-intervalise interval box
Nsub = 20;
xs = mince(X, Nsub)

# Eval sub-intervals
outs = f.(xs)

# Extract marginal inputs
x1s = [x.v[1] for x in xs]
x2s = [x.v[2] for x in xs]

# Make input/output boxes
outX1s = x1s .× outs
outX2s = x2s .× outs

# Plots (expensive with many boxes)
#plot(outX1s, alpha = 0.01)
#plot!(outX2s, alpha = 0.01, color = :red)
#plot!(outX3s, alpha = 0.01, color = :green)

###### Compute x1 index  #######

# Marginalisation loop for x1
x1Unique = unique(x1s)
outsUnion1 = Vector{Interval{Float64}}(undef, length(x1Unique))     # Initialise interval vec
for i = 1:length(x1Unique)
    ids = x1s .== x1Unique[i]
    outsUnion1[i] = hull(outs[ids])
end

outU1 = x1Unique .× outsUnion1      # Marginalised shape

bigBoxU1 = hull(x1Unique) × hull(outsUnion1)    # Compute bounding box

bigArea1 = diam(bigBoxU1.v[1]) * diam(bigBoxU1.v[2])    # Area of bounding box
areaU1 = sum([diam(x.v[1]) * diam(x.v[2]) for x in outU1])  # Area of interval shape
SA1 = 1 - areaU1/bigArea1       # Sensativity index

###### Compute x2 index ########

x2Unique = unique(x2s)

outsUnion2 = Vector{Interval{Float64}}(undef, length(x2Unique))
for i = 1:length(x2Unique)
    ids = x2s .== x2Unique[i]
    outsUnion2[i] = hull(outs[ids])
end

outU2 = x2Unique .× outsUnion2


bigBoxU2 = hull(x2Unique) × hull(outsUnion2)

bigArea2 = diam(bigBoxU2.v[1]) * diam(bigBoxU2.v[2])
areaU2 = sum([diam(x.v[1]) * diam(x.v[2]) for x in outU2])
SA2 = 1 - areaU2/bigArea2

plot(outU1)
plot!(outU2)

println("SA_x1: $SA1")
println("SA_x2: $SA2")

