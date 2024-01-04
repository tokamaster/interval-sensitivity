using IntervalArithmetic, Plots, LaTeXStrings


## Define function. Interval box input.
a = 5;
b = 0.1;
f(x::IntervalBox) = sin(x.v[1]) + a * sin(x.v[2])^2 + b * x.v[3]^4 * sin(x.v[1])


## Input variables
x1 = interval(-pi, pi)
x2 = interval(-pi, pi)
x3 = interval(-pi, pi)

# Make interval box
X = x1 × x2 × x3

# Sub-intervalise interval box
Nsub = 100;
xs = mince(X, Nsub)

# Eval sub-intervals
outs = f.(xs)

# Extract marginal inputs
x1s = [x.v[1] for x in xs]
x2s = [x.v[2] for x in xs]
x3s = [x.v[3] for x in xs]

# Make input/output boxes
outX1s = x1s .× outs
outX2s = x2s .× outs
outX3s = x3s .× outs

# Plots (expensive with many boxes)
#plot(outX1s, alpha = 0.01)
#plot!(outX2s, alpha = 0.01, color = :red)
#plot!(outX3s, alpha = 0.01, color = :green)

###### Compute x1 index  #######

# Marginalisation loop for x1
x1Unique = unique(x1s)
outsUnion1 = Vector{Interval{Float64}}(undef, length(x1Unique))     # Initialise interval vec
pinching1 = Vector{Interval{Float64}}(undef, length(x1Unique))
for i = 1:length(x1Unique)
    ids = x1s .== x1Unique[i]
    outsUnion1[i] = hull(outs[ids])
    pinching1[i] = outsUnion1[i] - outsUnion1[i].lo
end

outU1 = x1Unique .× outsUnion1      # Marginalised shape
pinbox1 = x1Unique .× pinching1

bigBoxU1 = hull(x1Unique) × hull(outsUnion1)    # Compute bounding box

bigArea1 = diam(bigBoxU1.v[1]) * diam(bigBoxU1.v[2])    # Area of bounding box
areaU1 = sum([diam(x.v[1]) * diam(x.v[2]) for x in outU1])  # Area of interval shape
SA1 = 1 - areaU1 / bigArea1       # Sensativity index

###### Compute x2 index ########

x2Unique = unique(x2s)

outsUnion2 = Vector{Interval{Float64}}(undef, length(x2Unique))
pinching2 = Vector{Interval{Float64}}(undef, length(x2Unique))
for i = 1:length(x2Unique)
    ids = x2s .== x2Unique[i]
    outsUnion2[i] = hull(outs[ids])
    pinching2[i] = outsUnion2[i] - outsUnion2[i].lo
end

outU2 = x2Unique .× outsUnion2
pinbox2 = x2Unique .× pinching2

bigBoxU2 = hull(x2Unique) × hull(outsUnion2)

bigArea2 = diam(bigBoxU2.v[1]) * diam(bigBoxU2.v[2])
areaU2 = sum([diam(x.v[1]) * diam(x.v[2]) for x in outU2])
SA2 = 1 - areaU2 / bigArea2

#####   Compute x3 index    ######

x3Unique = unique(x3s)

outsUnion3 = Vector{Interval{Float64}}(undef, length(x3Unique))
pinching3 = Vector{Interval{Float64}}(undef, length(x3Unique))
for i = 1:length(x3Unique)
    ids = x3s .== x3Unique[i]
    outsUnion3[i] = hull(outs[ids])
    pinching3[i] = outsUnion3[i] - outsUnion3[i].lo
end

outU3 = x3Unique .× outsUnion3
pinbox3 = x3Unique .× pinching3

bigBoxU3 = hull(x3Unique) × hull(outsUnion3)

bigArea3 = diam(bigBoxU3.v[1]) * diam(bigBoxU3.v[2])
areaU3 = sum([diam(x.v[1]) * diam(x.v[2]) for x in outU3])
SA3 = 1 - areaU3 / bigArea3

#plot(outU1)
#plot!(outU2)
#plot!(outU3)


println("SA_x1: $SA1")
println("SA_x2: $SA2")
println("SA_x3: $SA3")

theme(:dao, palette=:grays, legend=false)

#Plots.plot(bigBoxU3, fillcolor="black", fillalpha=0.2)
#Plots.plot!(outU3, fillcolor="red", xguidefontsize=20, yguidefontsize=20, xtickfontsize=18, ytickfontsize=18, bottom_margin=4Plots.mm)
#Plots.xlabel!(L"x_3")
#Plots.ylabel!("Output")
#Plots.savefig("ishigami_3.pdf")

Plots.plot(pinbox3, fillcolor="red", xguidefontsize=20, yguidefontsize=20, xtickfontsize=18, ytickfontsize=18, bottom_margin=4Plots.mm)
Plots.xlabel!(L"x_3")
Plots.ylabel!("Output width")
Plots.savefig("ishigami_pinching_3.pdf")