using QuantEcon
using PlotlyJS

include("jv.jl")

wp = JvWorker(grid_size=25)
v_init = wp.x_grid .* 0.5

f(x) = bellman_operator(wp, x)
V = compute_fixed_point(f, v_init, max_iter=200)

s_policy, phi_policy = bellman_operator(wp, V, ret_policies=true)

# === plot solution === #
tr_phi = plot(scatter(; 
    x = wp.x_grid, 
    y = phi_policy, name = "ϕ policy"), 
    Layout(xaxis_range = [0.0, 
                    maximum(wp.x_grid)], 
                    yaxis_range = [-0.1, 1.1], 
                    xaxis_title = "x")
    )

tr_s = plot(scatter(; 
    x = wp.x_grid, 
    y = s_policy, 
    name = "s policy"), 
    Layout(xaxis_range = [0.0, 
            maximum(wp.x_grid)], 
            yaxis_range = [-0.1, 1.1], 
            xaxis_title = "x"))

tr_V = plot(scatter(; 
    x = wp.x_grid, 
    y = V, 
    name = "Value Fn."), 
    Layout(xaxis_range = [0.0, 
                maximum(wp.x_grid)], 
                xaxis_title = "x")
    )

display([tr_s; tr_phi; tr_V])
