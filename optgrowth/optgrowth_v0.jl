#=
A first pass at solving the optimal growth problem via value function
iteration.  A more general version is provided in optgrowth.py.

@author : Spencer Lyon <spencer.lyon@nyu.edu>
          Victoria Gregory <victoria.gregory@nyu.edu>
=#

using Optim: optimize
using Grid: CoordInterpGrid, BCnan, InterpLinear
using Plots
pyplot()


## Primitives and grid
alpha = 0.65
bet = 0.95
grid_max = 2
grid_size = 150
grid = 1e-6:(grid_max-1e-6)/(grid_size-1):grid_max

## Exact solution
ab = alpha * bet
c1 = (log(1 - ab) + log(ab) * ab / (1 - ab)) / (1 - bet)
c2 = alpha / (1 - ab)
v_star(k) = c1 .+ c2 .* log(k)


function bellman_operator(grid, w)
    Aw = CoordInterpGrid(grid, w, BCnan, InterpLinear)

    Tw = zeros(w)

    for (i, k) in enumerate(grid)
        objective(c) = - log(c) - bet * Aw[k^alpha - c]
        res = optimize(objective, 1e-6, k^alpha)
        Tw[i] = - objective(res.minimum)
    end
    return Tw
end


function main(n::Int=35)
    w_init = 5 .* log(grid) .- 25  # An initial condition -- fairly arbitrary
    w = copy(w_init)

    ws = []
    colors = []
    for i=1:n
        w = bellman_operator(grid, w)
        push!(ws, w)
        push!(colors, RGBA(0, 0, 0, i/n))
    end

    p = plot(grid, w_init, color=:green, linewidth=2, alpha=0.6,
         label="initial condition")
    plot!(grid, ws, color=colors', label="", linewidth=2)
    plot!(grid, v_star(grid), color=:blue, linewidth=2, alpha=0.8,
         label="true value function")
    plot!(ylims=(-40, -20), xlims=(minimum(grid), maximum(grid)))

    return p
end
