"""
Implements iteration on the Bellman equations to solve the McCall growth model

"""

import numpy as np
from quantecon.distributions import BetaBinomial


class McCallModel:
    """
    Stores the parameters and functions associated with a given model.
    """

    def __init__(self, alpha=0.2, 
                        beta=0.98, 
                        gamma=0.7, 
                        c=6.0,
                        u=np.log, 
                        w_vec=None,
                        p_vec=None):

        self.alpha, self.beta, self.gamma, self.c = alpha, beta, gamma, c
        self.u = u

        # Add a default wage vector and probabilities over the vector using
        # the beta-binomial distribution
        if w_vec is None:
            n = 50  # number of possible outcomes for wage
            self.w_vec = np.linspace(10, 20, n)     # wages between 10 and 20
            a, b = 600, 400  # shape parameters
            dist = BetaBinomial(n-1, a, b)
            self.p_vec = dist.pdf()  
        else:
            self.w_vec = w_vec
            self.p_vec = p_vec


def update_bellman_eqs(mcm, V, U):
    """
    Performs the update step on the Bellman equations 
    
    Parameters
    ----------
    mcm : an instance of McCallModel
    V : array_like(float)
        current guess of the vector V
    U : scalar
        current guess of the scalar U
         
    """

    # Unpack parameters to simplify notation
    alpha, beta, gamma, c, u = mcm.alpha, mcm.beta, mcm.gamma, mcm.c, mcm.u

    new_V = np.empty_like(V)

    for w_idx, w in enumerate(mcm.w_vec):
        # w_idx indexes the vector of possible wages
        new_V[w_idx] = u(w) + beta * ((1 - alpha) * V[w_idx] + alpha * U)
        new_U = u(c) + beta * (1 - gamma) * U + \
                    beta * gamma * np.sum(np.maximum(U, V) * mcm.p_vec)

    return new_V, new_U


def solve_mccall_model(mcm, tol=1e-5, max_iter=500):
    """
    Iterates to convergence on the Bellman equations 
    
    Parameters
    ----------
    mcm : an instance of McCallModel
    tol : float
        error tolerance
    max_iter : int
        the maximum number of iterations
    """

    V = np.ones(len(mcm.w_vec))  # Initial guess of V
    U = 1                        # Initial guess of U
    i = 0
    error = tol + 1

    while error > tol and i < max_iter:
        new_V, new_U = update_bellman_eqs(mcm, V, U)
        error_1 = np.max(np.abs(new_V - V))
        error_2 = np.abs(new_U - U)
        error = max(error_1, error_2)
        V = new_V
        U = new_U
        i += 1

    return V, U


