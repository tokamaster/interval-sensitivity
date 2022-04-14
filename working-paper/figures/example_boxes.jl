using IntervalArithmetic, Plots, Distributions, ProbabilityBoundsAnalysis

## Define function. Interval box input.
a = -4;
f(x::IntervalBox) = a * x.v[1] + interval(normal(0,sqrt(x.v[1]^2)).u[1],normal(0,sqrt(x.v[1]^2)).d[end] )

## Input variables
x1 = interval(-5, 5)
x2 = interval(-5, 5)


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
SA1 = 1 - areaU1 / bigArea1       # Sensativity index

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
SA2 = 1 - areaU2 / bigArea2

println("SA_x1: $SA1")
println("SA_x2: $SA2")

theme(:dao, palette=:grays, legend=false)

Plots.plot(bigBoxU2, fillcolor="red", fillalpha=0.2)
Plots.plot!(outU2, fillcolor="black", xguidefontsize=20, yguidefontsize=20, xtickfontsize=18, ytickfontsize=18, bottom_margin=4Plots.mm)
Plots.xlabel!(L"x_2")
Plots.ylabel!(L"y")
Plots.savefig("example_boxes_2.pdf")