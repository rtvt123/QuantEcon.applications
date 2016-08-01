"""
Filename: asset_pricing.py

Computes asset prices with a Lucas style discount factor when the endowment
obeys geometric growth driven by a finite state Markov chain.  That is,

.. math::
    d_{t+1} = lambda(X_{t+1}) d_t

where 

    * :math:`\{X_t\}` is a finite Markov chain with transition matrix P.

    * :math:`\lambda` is a given positive-valued function

References
----------

    http://quant-econ.net/py/markov_asset.html

"""
import numpy as np
import quantecon as qe
from numpy.linalg import solve, eigvals


class AssetPriceModel:
    r"""
    A class that stores the primitives of the asset pricing model, plus a few
    useful matrices as attributes

    Parameters
    ----------
    beta : scalar, float
        Discount factor
    mc : MarkovChain
        Contains the transition matrix and set of state values for the state
        proces
    gamma : scalar(float)
        Coefficient of risk aversion
    lambda_func : callable
        The function mapping states to growth rates

    """
    def __init__(self, beta=0.96, mc=None, gamma=2.0, lambda_func=np.exp):
        self.beta, self.gamma = beta, gamma
        self.lambda_func = lambda_func

        # == A default process for the Markov chain == #
        if mc is None:
            self.rho = 0.9
            self.sigma = 0.02
            self.mc = qe.tauchen(self.rho, self.sigma)
        else:
            self.mc = mc

        self.n = self.mc.P.shape[0]

    def test_stability(self, Q):
        """
        Stability test for a given matrix Q.
        """
        sr = np.max(np.abs(eigvals(Q)))
        if not sr < 1 / self.beta:
            msg = "Spectral radius condition failed with radius = %f" % sr
            raise ValueError(msg)



def tree_price(ap):
    """
    Computes the price-dividend ratio of the Lucas tree.

    Parameters
    ----------
    ap: AssetPriceModel
        An instance of AssetPriceModel containing primitives

    Returns
    -------
    v : array_like(float)
        Lucas tree price-dividend ratio

    """
    # == Simplify names, set up matrices  == #
    beta, gamma, P, y = ap.beta, ap.gamma, ap.mc.P, ap.mc.state_values
    J = P * ap.lambda_func(y)**(1 - gamma)

    # == Make sure that a unique solution exists == #
    ap.test_stability(J)

    # == Compute v == #
    I = np.identity(ap.n)
    Ones = np.ones(ap.n)
    v = beta * solve(I - beta * J, J @ Ones)

    return v


def consol_price(ap, zeta):
    """
    Computes price of a consol bond with payoff zeta

    Parameters
    ----------
    ap: AssetPriceModel
        An instance of AssetPriceModel containing primitives

    zeta : scalar(float)
        Coupon of the console

    Returns
    -------
    p : array_like(float)
        Console bond prices

    """
    # == Simplify names, set up matrices  == #
    beta, gamma, P, y = ap.beta, ap.gamma, ap.mc.P, ap.mc.state_values
    M = P * ap.lambda_func(y)**(- gamma)

    # == Make sure that a unique solution exists == #
    ap.test_stability(M)

    # == Compute price == #
    I = np.identity(ap.n)
    Ones = np.ones(ap.n)
    p = beta * solve(I - beta * M, zeta * M @ Ones)

    return p


def call_option(ap, zeta, p_s, T=[], epsilon=1e-8):
    """
    Computes price of a call option on a consol bond, both finite
    and infinite horizon

    Parameters
    ----------
    ap: AssetPriceModel
        An instance of AssetPriceModel containing primitives

    zeta : scalar(float)
        Coupon of the console

    p_s : scalar(float)
        Strike price

    T : iterable(integers)
        Length of option in the finite horizon case

    epsilon : scalar(float), optional(default=1e-8)
        Tolerance for infinite horizon problem

    Returns
    -------
    w_bar : array_like(float)
        Infinite horizon call option prices

    w_bars : dict
        A dictionary of key-value pairs {t: vec}, where t is one of
        the dates in the list T and vec is the option prices at that
        date

    """
    # == Simplify names, initialize variables == #
    beta = ap.beta
    P_check = ap.P_check

    # == Compute consol price == #
    v_bar = consol_price(ap, zeta)

    # == Compute option price == #
    w_bar = np.zeros(ap.n)
    error = epsilon + 1
    t = 0
    w_bars = {}
    while error > epsilon:
        if t in T:
            w_bars[t] = w_bar

        # == Maximize across columns == #
        to_stack = (beta*P_check.dot(w_bar), v_bar-p_s)
        w_bar_new = np.amax(np.vstack(to_stack), axis=0)

        # == Find maximal difference of each component == #
        error = np.amax(np.abs(w_bar-w_bar_new))

        # == Update == #
        w_bar = w_bar_new
        t += 1

    return w_bar, w_bars
