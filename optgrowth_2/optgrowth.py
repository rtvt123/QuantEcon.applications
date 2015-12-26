"""
Filename: optgrowth.py
Authors: John Stachurski, Thomas Sargent

Solving the optimal growth problem via value function iteration.  The model is
described in 

    http://quant-econ.net/py/optgrowth_2.html
"""

import numpy as np
from scipy.optimize import fminbound
from scipy import interp
from joblib import Memory
from quantecon import compute_fixed_point

# For persistent caching.  Here we're writing to /tmp, which only 
# persists to the next reboot.  Change to the local dir to get a more
# permanent cache.
memory = Memory(cachedir='/tmp/joblib_cache')

def bellman_operator(w, grid, beta, u, f, shocks, Tw=None, compute_policy=0):
    """
    The approximate Bellman operator, which computes and returns the
    updated value function Tw on the grid points.  An array to store
    the new set of values Tw is optionally supplied (to avoid having to
    allocate new arrays at each iteration).  If supplied, any existing data in 
    Tw will be overwritten.

    Parameters
    ----------
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
    # === Apply linear interpolation to w === #
    w_func = lambda x: interp(x, grid, w)

    # == Initialize Tw if necessary == #
    if Tw is None:
        Tw = np.empty(len(w))

    if compute_policy:
        sigma = np.empty(len(w))

    # == set Tw[i] = max_c { u(c) + beta E w(f(y  - c))} == #
    for i, y in enumerate(grid):
        def objective(c):
            return - u(c) - beta * np.mean(w_func(f(y - c) * shocks))
        c_star = fminbound(objective, 1e-10, y)
        if compute_policy:
            sigma[i] = c_star
        Tw[i] = - objective(c_star)

    if compute_policy:
        return Tw, sigma
    else:
        return Tw


@memory.cache
def compute_opt_growth_vf(grid, beta, u, f, shocks):
    """
    Compute the value function by iterating on the Bellman operator.
    The hard work is done by QuantEcon's compute_fixed_point function.
    """
    Tw = np.empty(len(grid))
    initial_w = 5 * np.log(grid) - 25

    v_star = compute_fixed_point(bellman_operator, 
            initial_w, 
            1e-3, # error_tol
            50,   # max_iter
            True, # verbose
            5,    # print_skip
            grid,
            beta,
            u,
            f,
            shocks,
            Tw=Tw,
            compute_policy=False)
    return v_star




