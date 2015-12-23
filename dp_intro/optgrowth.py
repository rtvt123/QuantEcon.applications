"""
Filename: optgrowth.py
Authors: John Stachurski, Thomas Sargent

Solving the optimal growth problem via value function iteration.
"""

import numpy as np
from scipy.optimize import fminbound
from scipy import interp
from joblib import Memory
from quantecon import compute_fixed_point
import matplotlib.pyplot as plt

# For persistent caching 
memory = Memory(cachedir='/tmp/joblib_cache')

def bellman_operator(w, grid, alpha, beta, delta, Tw=None, compute_policy=0):
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
    alpha : scalar
        The productivity parameter
    beta : scalar
        The discount factor
    delta : scalar
        The depreciation parameter
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

    # == set Tw[i] = max_c { u(c) + beta w(f(k_i) + (1 - delta)k - c)} == #
    for i, k in enumerate(grid):
        y = k**alpha + (1 - delta) * k  # Available capital
        def objective(c):
            return - np.log(c) - beta * w_func(y - c)
        c_star = fminbound(objective, 1e-10, y)
        if compute_policy:
            sigma[i] = c_star
        Tw[i] = - objective(c_star)

    if compute_policy:
        return Tw, sigma
    else:
        return Tw


@memory.cache
def compute_opt_growth_vf(alpha, beta, delta, grid):
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
            alpha,
            beta,
            delta,
            Tw=Tw,
            compute_policy=False)

    return v_star




class GrowthModel:
    """
    A simple class to store parameters and compute solutions.
    """
    def __init__(self, alpha=0.65, beta=0.95, delta=1, grid_max=2, grid_size=150):

        self.alpha, self.beta, self.delta = alpha, beta, delta
        self.grid = np.linspace(1e-6, grid_max, grid_size)

    def compute_value_function(self, show_plot=False):
        v_star = compute_opt_growth_vf(self.alpha, 
                                    self.beta, self.delta, self.grid)

        if show_plot:
            fig, ax = plt.subplots()
            ax.plot(self.grid, v_star, lw=2, alpha=0.6, label='value function')
            ax.legend(loc='lower right')
            plt.show()

        return v_star

    def compute_greedy(self, w=None, show_plot=False):
        """
        Compute the w-greedy policy on the grid points given w
        (the value of the input function on grid points).  If w is not
        supplied, use the approximate optimal value function.
        """
        if w is None:
            w = self.compute_value_function()
        Tw, sigma = bellman_operator(w, 
                self.grid,  
                self.alpha,  
                self.beta,  
                self.delta,  
                compute_policy=True)

        if show_plot:
            fig, ax = plt.subplots()
            ax.plot(self.grid, sigma, lw=2, alpha=0.6, label='policy function')
            ax.legend(loc='lower right')
            plt.show()

        return sigma


