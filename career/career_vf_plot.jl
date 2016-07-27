#=
Shows

@author : Spencer Lyon <spencer.lyon@nyu.edu>
          Victoria Gregory <victoria.gregory@nyu.edu>

@date: 2014-08-05

References
----------

http://quant-econ.net/career.html
=#
using Plots
pyplot()
using QuantEcon

include("career.jl")

srand(41)  # reproducible results
wp = CareerWorkerProblem()
v_init = fill(100.0, wp.N, wp.N)
func(x) = bellman_operator(wp, x)
v = compute_fixed_point(func, v_init, max_iter=500, verbose=false)

surface(wp.theta, wp.epsilon, v', alpha=0.5,
        linewidth=0.25, zlims=(150, 200),
        xlabel="theta", ylabel="epsilon", cbar=false)
