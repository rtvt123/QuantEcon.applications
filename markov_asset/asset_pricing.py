"""
Filename: asset_pricing.py

Computes asset prices in a Lucas endowment economy when the endowment obeys
geometric growth driven by a finite state Markov chain.  That is,

.. math::
    d_{t+1} = X_{t+1} d_t

where :math:`\{X_t\}` is a finite Markov chain with transition matrix P.

References
----------

    http://quant-econ.net/py/markov_asset.html

"""
import numpy as np
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

    Attributes
    ----------
    beta, mc, gamm : as above

    P_tilde : ndarray
        The matrix :math:`P(x, y) y^(1 - \gamma)`

    """
    def __init__(self, beta, mc, gamma):
        self.beta, self.mc, self.gamma = beta, mc, gamma
        self.n = self.mc.P.shape[0]

        # Create P_tilde
        Ptilde = self.P_tilde
        ev = beta * eigvals(Ptilde)
        lt1 = np.all(ev.real < 1.0)
        if not lt1:
            msg = "All eigenvalues of Ptilde must be less than 1/beta"
            raise ValueError(msg)


    @property
    def P_tilde(self):
        P = self.mc.P
        y = self.mc.state_values
        return P * y**(1 - self.gamma)  # using broadcasting

    @property
    def P_check(self):
        P = self.mc.P
        y = self.mc.state_values
        return P * y**(-self.gamma)  # using broadcasting



def tree_price(apm):
    """
    Computes the price-dividend ratio of the Lucas tree.

    Parameters
    ----------
    apm: AssetPriceModel
        An instance of AssetPriceModel containing primitives

    Returns
    -------
    v : array_like(float)
        Lucas tree price-dividend ratio

    """
    # == Simplify names == #
    beta = apm.beta
    P_tilde = apm.P_tilde

    # == Compute v == #
    I = np.identity(apm.n)
    O = np.ones(apm.n)
    v = beta * solve(I - beta * P_tilde, P_tilde @ O)

    return v


def consol_price(apm, zeta):
    """
    Computes price of a consol bond with payoff zeta

    Parameters
    ----------
    apm: AssetPriceModel
        An instance of AssetPriceModel containing primitives

    zeta : scalar(float)
        Coupon of the console

    Returns
    -------
    p_bar : array_like(float)
        Console bond prices

    """
    # == Simplify names == #
    beta = apm.beta

    # == Compute price == #
    P_check = apm.P_check
    I = np.identity(apm.n)
    O = np.ones(apm.n)
    p_bar = beta * solve(I - beta * P_check, P_check.dot(zeta * O))

    return p_bar


def call_option(apm, zeta, p_s, T=[], epsilon=1e-8):
    """
    Computes price of a call option on a consol bond, both finite
    and infinite horizon

    Parameters
    ----------
    apm: AssetPriceModel
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
    beta = apm.beta
    P_check = apm.P_check

    # == Compute consol price == #
    v_bar = consol_price(apm, zeta)

    # == Compute option price == #
    w_bar = np.zeros(apm.n)
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
