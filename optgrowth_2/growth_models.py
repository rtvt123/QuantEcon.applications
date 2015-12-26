"""
Filename: growth_models.py
Authors: John Stachurski, Thomas Sargent

Some growth models, wrapped as classes.  For use with the optgrowth.py module.
"""

import numpy as np
import matplotlib.pyplot as plt
from optgrowth import bellman_operator, compute_opt_growth_vf


class LogLinearGrowthModel:
    """
    Stores parameters and computes solutions for the basic log utility / Cobb
    Douglas production growth model.  Shocks are lognormal.
    """
    def __init__(self, 
            alpha=0.65,         # Productivity parameter
            beta=0.95,          # Discount factor
            mu=1,               # First parameter in lognorm(mu, sigma)
            sigma=0.2,          # Second parameter in lognorm(mu, sigma)
            grid_max=3, 
            grid_size=150):

        self.alpha, self.beta, self.mu, self.sigma = alpha, beta, mu, sigma
        self.grid = np.linspace(1e-6, grid_max, grid_size)
        self.shocks = np.exp(mu + sigma * np.random.randn(250))

    def compute_value_function(self, show_plot=False):
        v_star = compute_opt_growth_vf(self.grid, 
                                       self.beta,
                                       np.log,
                                       lambda k: k**self.alpha,
                                       self.shocks)

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
                                    self.beta,  
                                    np.log,
                                    lambda k: k**self.alpha,
                                    self.shocks,
                                    compute_policy=True)

        if show_plot:
            fig, ax = plt.subplots()
            ax.plot(self.grid, sigma, lw=2, alpha=0.6, label='approximate policy function')
            cstar = (1 - self.alpha * self.beta) * self.grid
            ax.plot(self.grid, cstar, lw=2, alpha=0.6, label='true policy function')
            ax.legend(loc='lower right')
            plt.show()

        return sigma

