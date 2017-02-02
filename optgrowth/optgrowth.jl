#=
Solving the optimal growth problem via value function iteration.

@authors : Spencer Lyon,

@date : Thu Feb 2 14:39:36 AEDT 2017

References
----------
    
https://lectures.quantecon.org/jl/optgrowth.html

=#

using Interpolations
using Optim


"""
A function that takes two arrays and returns a function that approximates the
data using continuous piecewise linear interpolation.

"""
function lin_interp(x_vals::Vector{Float64}, y_vals::Vector{Float64})
    # == linear interpolation inside grid == #
    w = interpolate((x_vals,), y_vals,  Gridded(Linear()))
    # == constant values outside grid == #
    w = extrapolate(w,  Interpolations.Flat())
    return w
end


"""
The approximate Bellman operator, which computes and returns the
updated value function Tw on the grid points.  An array to store
the new set of values Tw is optionally supplied (to avoid having to
allocate new arrays at each iteration).  If supplied, any existing data in 
Tw will be overwritten.

#### Arguments

w : array_like(float, ndim=1)
    The value of the input function on different grid points
grid : array_like(float, ndim=1)
    The set of grid points
u : function
    The utility function
f : function
    The production function
shocks : numpy array
    An array of draws from the shock, for Monte Carlo integration (to
    compute expectations).
beta : scalar
    The discount factor
Tw : array_like(float, ndim=1) optional (default=None)
    Array to write output values to
compute_policy : Boolean, optional (default=False)
    Whether or not to compute policy function

"""
function bellman_operator(w, grid, beta, u, f, shocks; compute_policy=false)

    # === Apply linear interpolation to w === #
    w_func = lin_interp(grid, w)
    
    Tw = similar(w)

    if compute_policy
        sigma = similar(w)
    end

    # == set Tw[i] = max_c { u(c) + beta E w(f(y  - c) z)} == #
    for (i, y) in enumerate(grid)
        objective(c) = - u(c) - beta * mean(w_func[f(y - c) .* shocks])
        res = optimize(objective, 1e-10, y)

        if compute_policy
            sigma[i] = res.minimum
        end
        Tw[i] = -res.f_minimum
    end

    if compute_policy
        return Tw, sigma
    else
        return Tw
    end
end

